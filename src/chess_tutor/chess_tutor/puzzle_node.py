"""puzzle_node — owns the chess puzzle state machine.

Loads puzzles at startup, picks one, applies the opponent's setup move,
and publishes the resulting position. When the tutor confirms a correct move,
this node advances the board (and plays the opponent's reply) and publishes
the new state.

Subscribes:
  /tutor_response   (chess_tutor_msgs/TutorResponse) — applied if is_correct;
                    also reads perceived_confidence for difficulty adaptation
  /user_confidence  (std_msgs/Float32, optional) — externally published user
                    confidence in [0, 1]; combined with the LLM-perceived value

Publishes:
  /current_puzzle (chess_tutor_msgs/PuzzleState, latched-style)
  /tts_request    (std_msgs/String) — narration ("Opponent plays Nf6", "Puzzle solved!")
"""

import os
import random

import chess
import rclpy
from ament_index_python.packages import get_package_share_directory
from rclpy.node import Node
from rclpy.qos import QoSDurabilityPolicy, QoSProfile, QoSReliabilityPolicy
from std_msgs.msg import Float32, String

from chess_tutor_msgs.msg import PuzzleState, TutorResponse

from chess_tutor.lib.puzzle_loader import SAMPLE_PUZZLES, Puzzle, load_puzzles


# Latched-style QoS so a node that subscribes late still gets the latest puzzle.
LATCHED_QOS = QoSProfile(
    depth=1,
    reliability=QoSReliabilityPolicy.RELIABLE,
    durability=QoSDurabilityPolicy.TRANSIENT_LOCAL,
)


class PuzzleNode(Node):
    def __init__(self):
        super().__init__("puzzle_node")

        # ---- Parameters ----
        self.declare_parameter("puzzles_csv", "")  # empty -> use bundled CSV
        self.declare_parameter("min_rating", 0)
        self.declare_parameter("max_rating", 9999)
        self.declare_parameter("autostart", True)
        # Adaptive difficulty.
        self.declare_parameter("initial_target_rating", -1)  # -1 -> midpoint
        self.declare_parameter("confidence_low_threshold", 0.4)
        self.declare_parameter("confidence_high_threshold", 0.7)
        self.declare_parameter("difficulty_step", 75)
        self.declare_parameter("external_confidence_weight", 0.5)

        csv_path = self.get_parameter("puzzles_csv").value
        min_r = self.get_parameter("min_rating").value
        max_r = self.get_parameter("max_rating").value
        autostart = self.get_parameter("autostart").value

        self.min_rating = int(min_r)
        self.max_rating = int(max_r)
        init_target = int(self.get_parameter("initial_target_rating").value)
        if init_target < 0:
            init_target = (self.min_rating + self.max_rating) // 2
        self.target_rating = max(self.min_rating, min(self.max_rating, init_target))
        self.conf_low = float(self.get_parameter("confidence_low_threshold").value)
        self.conf_high = float(self.get_parameter("confidence_high_threshold").value)
        self.difficulty_step = int(self.get_parameter("difficulty_step").value)
        self.external_weight = float(
            self.get_parameter("external_confidence_weight").value
        )

        # ---- Load puzzles ----
        if not csv_path:
            try:
                share = get_package_share_directory("chess_tutor")
                csv_path = os.path.join(share, "data", "puzzles.csv")
            except Exception:
                csv_path = ""

        if csv_path and os.path.exists(csv_path):
            self.puzzles = load_puzzles(csv_path, min_rating=min_r, max_rating=max_r)
            self.get_logger().info(f"Loaded {len(self.puzzles)} puzzles from {csv_path}")
        else:
            self.puzzles = SAMPLE_PUZZLES
            self.get_logger().warn(
                f"Puzzles CSV not found at '{csv_path}', using {len(self.puzzles)} built-in samples"
            )

        if not self.puzzles:
            raise RuntimeError("No puzzles available — check rating filters")

        # ---- State ----
        self.puzzle: Puzzle | None = None
        self.board: chess.Board | None = None
        self.move_history: list[str] = []
        # Confidence signals — None until populated.
        self.latest_external_confidence: float | None = None
        # Most recent LLM-perceived confidence for the current puzzle attempt.
        self.latest_perceived_confidence: float | None = None

        # ---- Pub/Sub ----
        self.state_pub = self.create_publisher(
            PuzzleState, "/current_puzzle", LATCHED_QOS
        )
        self.tts_pub = self.create_publisher(String, "/tts_request", 10)
        self.create_subscription(
            TutorResponse, "/tutor_response", self._on_tutor_response, 10
        )
        self.create_subscription(
            Float32, "/user_confidence", self._on_user_confidence, 10
        )

        if autostart:
            # Defer slightly so subscribers (tutor_node, tts_node) come up first.
            self.create_timer(2.0, self._autostart_once)

        self.get_logger().info("puzzle_node ready")

    def _autostart_once(self):
        """Pick a random puzzle on startup, then cancel the timer."""
        if self.puzzle is None:
            self.start_new_puzzle()
        # Cancel by destroying all timers — safe since this is the only one.
        for t in list(self.timers):
            t.cancel()

    def start_new_puzzle(self):
        self.puzzle = self._pick_puzzle_near_target()
        self.board = chess.Board(self.puzzle.fen)

        # Apply the opponent's setup move.
        setup = chess.Move.from_uci(self.puzzle.opponent_move)
        self.board.push(setup)
        self.move_history = []
        # Reset per-puzzle perceived-confidence sample.
        self.latest_perceived_confidence = None

        turn = "White" if self.board.turn == chess.WHITE else "Black"
        narration = (
            f"New puzzle, rating {self.puzzle.rating}. "
            f"You are playing {turn}. Find the best move."
        )
        self.get_logger().info(
            f"Started puzzle {self.puzzle.puzzle_id} "
            f"(rating {self.puzzle.rating}, target {self.target_rating})"
        )
        self._speak(narration)
        self._publish_state()

    def _pick_puzzle_near_target(self) -> Puzzle:
        """Pick a puzzle whose rating is closest to self.target_rating.

        Ties (and a small window around the closest rating) are broken randomly
        so we don't replay the same puzzle every time.
        """
        # Sort by distance to target, take the closest ~10% (min 5), pick one.
        ranked = sorted(self.puzzles, key=lambda p: abs(p.rating - self.target_rating))
        window = max(5, len(ranked) // 10)
        return random.choice(ranked[:window])

    def _on_user_confidence(self, msg: Float32):
        # Clamp to [0, 1] just in case the publisher sends something noisy.
        self.latest_external_confidence = max(0.0, min(1.0, float(msg.data)))

    def _combined_confidence(self) -> float | None:
        """Fuse external + LLM-perceived confidence into a single [0, 1] value.

        Returns None when neither source has reported yet, so the caller can
        decide to leave difficulty unchanged.
        """
        ext = self.latest_external_confidence
        per = self.latest_perceived_confidence
        if ext is None and per is None:
            return None
        if ext is None:
            return per
        if per is None:
            return ext
        w = self.external_weight
        return w * ext + (1.0 - w) * per

    def _adapt_target_rating(self):
        """Shift target_rating up/down based on combined confidence."""
        conf = self._combined_confidence()
        if conf is None:
            return  # no signal yet, hold steady
        old = self.target_rating
        if conf >= self.conf_high:
            self.target_rating = min(
                self.max_rating, self.target_rating + self.difficulty_step
            )
        elif conf <= self.conf_low:
            self.target_rating = max(
                self.min_rating, self.target_rating - self.difficulty_step
            )
        if self.target_rating != old:
            self.get_logger().info(
                f"Adapted difficulty: confidence={conf:.2f} "
                f"target_rating {old} -> {self.target_rating}"
            )

    def _on_tutor_response(self, msg: TutorResponse):
        # Capture perceived confidence regardless of correctness. Sentinel
        # -1.0 means the tutor produced no judgement.
        if msg.perceived_confidence >= 0.0:
            self.latest_perceived_confidence = float(msg.perceived_confidence)

        if not msg.is_correct or not msg.move_uci:
            return  # tutor's natural-language response handles wrong/non-moves
        if self.puzzle is None or self.board is None:
            return

        next_idx = len(self.move_history)
        solution = self.puzzle.solution_moves
        if next_idx >= len(solution):
            return  # already done

        # Apply the player's correct move.
        try:
            self.board.push(chess.Move.from_uci(msg.move_uci))
        except Exception as e:
            self.get_logger().error(f"Couldn't apply move {msg.move_uci}: {e}")
            return
        self.move_history.append(msg.move_uci)

        # Auto-play the opponent's reply, if any.
        if len(self.move_history) < len(solution):
            opp = solution[len(self.move_history)]
            self.board.push(chess.Move.from_uci(opp))
            self.move_history.append(opp)
            self._speak(f"Opponent plays {self._spoken_move(opp)}.")

        # Check completion.
        if len(self.move_history) >= len(solution):
            self._speak("Puzzle complete. Well done. Starting a new one.")
            self._publish_state(complete=True)
            # Use the confidence collected during this puzzle to nudge the
            # target rating before the next pick.
            self._adapt_target_rating()
            # Brief delay then next puzzle.
            self.create_timer(3.0, self._next_puzzle_once)
        else:
            self._publish_state()

    def _next_puzzle_once(self):
        self.start_new_puzzle()
        for t in list(self.timers):
            t.cancel()

    def _publish_state(self, complete: bool = False):
        msg = PuzzleState()
        msg.puzzle_id = self.puzzle.puzzle_id
        msg.rating = self.puzzle.rating
        msg.themes = list(self.puzzle.themes)
        msg.fen = self.board.fen()
        msg.solution_moves = list(self.puzzle.solution_moves)
        msg.move_history = list(self.move_history)
        msg.next_move_index = len(self.move_history)
        msg.is_complete = complete or len(self.move_history) >= len(self.puzzle.solution_moves)
        self.state_pub.publish(msg)

    def _speak(self, text: str):
        m = String()
        m.data = text
        self.tts_pub.publish(m)

    def _spoken_move(self, uci: str) -> str:
        """Convert UCI to something more pronounceable, e.g. 'g1f3' -> 'g1 to f3'."""
        if len(uci) >= 4:
            return f"{uci[0:2]} to {uci[2:4]}"
        return uci


def main():
    rclpy.init()
    node = PuzzleNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()

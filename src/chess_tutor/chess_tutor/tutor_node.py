"""tutor_node — bridges user speech to Claude (Anthropic API).

Subscribes:
  /user_speech    (std_msgs/String)         — transcribed user input
  /current_puzzle (chess_tutor_msgs/PuzzleState) — current board + solution

Publishes:
  /tutor_response (chess_tutor_msgs/TutorResponse) — move + tutor message
"""

import chess
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

from chess_tutor_msgs.msg import PuzzleState, TutorResponse

from chess_tutor.lib.tutor import ChessTutor


class TutorNode(Node):
    def __init__(self):
        super().__init__("tutor_node")

        # ---- Parameters ----
        self.declare_parameter("anthropic_api_key", "")
        api_key = self.get_parameter("anthropic_api_key").value or None

        # ---- AI brain ----
        try:
            self.tutor = ChessTutor(api_key=api_key)
        except Exception as e:
            self.get_logger().error(f"Failed to init ChessTutor: {e}")
            raise

        # ---- State ----
        self.current_puzzle: PuzzleState | None = None

        # ---- Pub/Sub ----
        self.response_pub = self.create_publisher(TutorResponse, "/tutor_response", 10)
        self.create_subscription(String, "/user_speech", self._on_speech, 10)
        self.create_subscription(
            PuzzleState, "/current_puzzle", self._on_puzzle, 10
        )

        self.get_logger().info("tutor_node ready")

    def _on_puzzle(self, msg: PuzzleState):
        # New puzzle or state update — reset progressive hints when puzzle changes.
        if (
            self.current_puzzle is None
            or self.current_puzzle.puzzle_id != msg.puzzle_id
        ):
            self.tutor.reset_hints()
            self.get_logger().info(f"Loaded puzzle {msg.puzzle_id} (rating {msg.rating})")
        self.current_puzzle = msg

    def _on_speech(self, msg: String):
        text = msg.data.strip()
        if not text:
            return

        if self.current_puzzle is None:
            self.get_logger().warn("Got speech but no active puzzle yet — ignoring")
            return

        if self.current_puzzle.is_complete:
            self.get_logger().info("Puzzle already complete; ignoring speech")
            return

        # Reconstruct the python-chess Board from the FEN.
        board = chess.Board(self.current_puzzle.fen)

        try:
            result = self.tutor.interpret(
                user_input=text,
                board=board,
                solution_moves=list(self.current_puzzle.solution_moves),
                move_history=list(self.current_puzzle.move_history),
            )
        except Exception as e:
            self.get_logger().error(f"Anthropic API call failed: {e}")
            return

        move_uci = result.get("move_uci") or ""
        message = result.get("message") or ""

        # Determine correctness against the solution.
        is_correct = False
        if move_uci:
            next_idx = self.current_puzzle.next_move_index
            if next_idx < len(self.current_puzzle.solution_moves):
                is_correct = move_uci == self.current_puzzle.solution_moves[next_idx]

        out = TutorResponse()
        out.move_uci = move_uci
        out.message = message
        out.is_correct = is_correct
        out.user_input = text
        self.response_pub.publish(out)

        self.get_logger().info(
            f"User: '{text}' -> move={move_uci or '(none)'} correct={is_correct}"
        )


def main():
    rclpy.init()
    node = TutorNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()

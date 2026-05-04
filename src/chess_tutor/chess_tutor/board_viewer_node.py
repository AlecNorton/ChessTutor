"""board_viewer_node — pygame window that mirrors /current_puzzle.

Renders the current puzzle position in a separate window so a human in the
loop can see what the tutor sees. Updates whenever a new PuzzleState arrives.

Subscribes:
  /current_puzzle (chess_tutor_msgs/PuzzleState)

Pieces are drawn with Unicode chess glyphs (U+2654-U+265F) so no image assets
are needed; on Linux DejaVu Sans (the usual default) ships these glyphs.
"""

import threading

import chess
import rclpy
from rclpy.node import Node
from rclpy.qos import QoSDurabilityPolicy, QoSProfile, QoSReliabilityPolicy

from chess_tutor_msgs.msg import PuzzleState

try:
    import pygame
except ImportError:
    pygame = None


PIECE_UNICODE = {
    "K": "♔", "Q": "♕", "R": "♖",
    "B": "♗", "N": "♘", "P": "♙",
    "k": "♚", "q": "♛", "r": "♜",
    "b": "♝", "n": "♞", "p": "♟",
}

LIGHT = (240, 217, 181)
DARK = (181, 136, 99)
HILITE = (246, 246, 130)
PIECE_COLOR = (20, 20, 20)
BG = (30, 30, 30)
TITLE_COLOR = (220, 220, 220)

LATCHED_QOS = QoSProfile(
    depth=1,
    reliability=QoSReliabilityPolicy.RELIABLE,
    durability=QoSDurabilityPolicy.TRANSIENT_LOCAL,
)


class BoardViewerNode(Node):
    def __init__(self):
        super().__init__("board_viewer_node")

        if pygame is None:
            self.get_logger().error(
                "pygame not installed. Run: pip install pygame"
            )
            raise RuntimeError("pygame missing")

        self.declare_parameter("board_size", 640)
        self.declare_parameter("flip_for_black", True)
        self.size = int(self.get_parameter("board_size").value)
        self.flip_for_black = bool(self.get_parameter("flip_for_black").value)

        # Shared state between ROS callback and pygame render loop.
        self.lock = threading.Lock()
        self.fen = chess.STARTING_FEN
        self.last_move_squares: set[str] = set()
        self.title = "Chess Tutor — waiting for puzzle..."
        self.dirty = True
        self.running = True

        self.create_subscription(
            PuzzleState, "/current_puzzle", self._on_puzzle, LATCHED_QOS
        )
        self.get_logger().info("board_viewer_node ready")

    def _on_puzzle(self, msg: PuzzleState):
        last_squares: set[str] = set()
        if msg.move_history:
            last = msg.move_history[-1]
            if len(last) >= 4:
                last_squares = {last[0:2], last[2:4]}

        try:
            turn = "White" if chess.Board(msg.fen).turn == chess.WHITE else "Black"
        except Exception:
            turn = "?"
        done = " (complete)" if msg.is_complete else ""
        title = f"Puzzle {msg.puzzle_id}  |  {msg.rating}  |  {turn} to move{done}"

        with self.lock:
            self.fen = msg.fen
            self.last_move_squares = last_squares
            self.title = title
            self.dirty = True

    def run_pygame(self):
        pygame.init()
        title_h = 32
        size = self.size
        screen = pygame.display.set_mode((size, size + title_h))
        pygame.display.set_caption("Chess Tutor — Board")

        # Pick a font that has the chess glyphs. DejaVu Sans is the safe pick
        # on Linux; fall back to whatever pygame finds.
        font_path = (
            pygame.font.match_font("dejavusans")
            or pygame.font.match_font("notosans")
            or pygame.font.match_font("symbola")
        )
        cell = size // 8
        piece_font = pygame.font.Font(font_path, int(cell * 0.75))
        title_font = pygame.font.Font(font_path, 18)
        coord_font = pygame.font.Font(font_path, 14)
        clock = pygame.time.Clock()

        while self.running and rclpy.ok():
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    self.running = False
                    break

            with self.lock:
                fen = self.fen
                last_squares = set(self.last_move_squares)
                title = self.title
                dirty = self.dirty
                self.dirty = False

            if dirty:
                screen.fill(BG)
                screen.blit(
                    title_font.render(title, True, TITLE_COLOR), (10, 6)
                )

                try:
                    board = chess.Board(fen)
                except Exception:
                    board = chess.Board()

                flip = self.flip_for_black and board.turn == chess.BLACK

                for row in range(8):
                    for col in range(8):
                        # row 0 is the top of the window. Map row/col to a
                        # board square depending on orientation.
                        if flip:
                            file_idx = 7 - col
                            rank_idx = row
                        else:
                            file_idx = col
                            rank_idx = 7 - row

                        is_light = (file_idx + rank_idx) % 2 == 1
                        color = LIGHT if is_light else DARK
                        sq_name = chess.square_name(
                            chess.square(file_idx, rank_idx)
                        )
                        if sq_name in last_squares:
                            color = HILITE

                        rect = pygame.Rect(
                            col * cell, row * cell + title_h, cell, cell
                        )
                        pygame.draw.rect(screen, color, rect)

                        piece = board.piece_at(
                            chess.square(file_idx, rank_idx)
                        )
                        if piece is not None:
                            sym = PIECE_UNICODE.get(piece.symbol(), "?")
                            ts = piece_font.render(sym, True, PIECE_COLOR)
                            screen.blit(ts, ts.get_rect(center=rect.center))

                        # File letters along the bottom row, rank numbers
                        # along the leftmost column — matches Lichess.
                        if row == 7:
                            screen.blit(
                                coord_font.render(
                                    "abcdefgh"[file_idx], True, PIECE_COLOR
                                ),
                                (rect.right - 12, rect.bottom - 16),
                            )
                        if col == 0:
                            screen.blit(
                                coord_font.render(
                                    str(rank_idx + 1), True, PIECE_COLOR
                                ),
                                (rect.left + 3, rect.top + 2),
                            )

                pygame.display.flip()

            clock.tick(30)

        pygame.quit()

    def shutdown(self):
        self.running = False


def main():
    rclpy.init()
    node = BoardViewerNode()
    spin_thread = threading.Thread(target=rclpy.spin, args=(node,), daemon=True)
    spin_thread.start()
    try:
        node.run_pygame()
    except KeyboardInterrupt:
        pass
    finally:
        node.shutdown()
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()

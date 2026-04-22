"""
Chess Move Projector ROS2 Node

Projects possible moves for chess pieces onto a physical chess board.
Subscribes to ROS2 topics for square and piece selection.

Subscribed Topics:
    /chess/square (std_msgs/String): Square to select (e.g., "e4")
    /chess/piece (std_msgs/String): Piece type (king/queen/rook/bishop/knight/pawn_white/pawn_black)
    /chess/clear (std_msgs/Empty): Clear all highlights

Parameters:
    calibration_file (string): Path to calibration JSON file
    fullscreen (bool): Start in fullscreen mode
    display_width (int): Window width (default 1280)
    display_height (int): Window height (default 720)
"""

import sys
import math
import json
import threading
import numpy as np
from pathlib import Path
from typing import Dict, Set, Optional
from dataclasses import dataclass
from enum import Enum

import rclpy
from rclpy.node import Node
from std_msgs.msg import String, Empty

try:
    import pygame
except ImportError:
    print("Install pygame: pip install pygame")
    sys.exit(1)


FILES = "abcdefgh"
RANKS = "12345678"


class Mode(Enum):
    CALIBRATE = "calibrate"
    PLAY = "play"


class PieceType(Enum):
    KING = "king"
    QUEEN = "queen"
    ROOK = "rook"
    BISHOP = "bishop"
    KNIGHT = "knight"
    PAWN_WHITE = "pawn_white"
    PAWN_BLACK = "pawn_black"


@dataclass
class Square:
    """A chess square with notation and pixel coordinates."""
    file: str
    rank: str
    x: int
    y: int
    size: int

    @property
    def file_idx(self) -> int:
        return FILES.index(self.file)

    @property
    def rank_idx(self) -> int:
        return RANKS.index(self.rank)


def get_piece_moves(square: str, piece: PieceType) -> Set[str]:
    """Get all possible move squares for a piece (ignores blocking)."""
    if len(square) != 2 or square[0] not in FILES or square[1] not in RANKS:
        return set()

    file_idx = FILES.index(square[0])
    rank_idx = RANKS.index(square[1])
    moves = set()

    def add_if_valid(f: int, r: int) -> bool:
        if 0 <= f < 8 and 0 <= r < 8:
            moves.add(f"{FILES[f]}{RANKS[r]}")
            return True
        return False

    def add_ray(df: int, dr: int):
        f, r = file_idx + df, rank_idx + dr
        while 0 <= f < 8 and 0 <= r < 8:
            moves.add(f"{FILES[f]}{RANKS[r]}")
            f += df
            r += dr

    if piece == PieceType.KING:
        for df in [-1, 0, 1]:
            for dr in [-1, 0, 1]:
                if df != 0 or dr != 0:
                    add_if_valid(file_idx + df, rank_idx + dr)

    elif piece == PieceType.QUEEN:
        for df, dr in [(-1, 0), (1, 0), (0, -1), (0, 1),
                       (-1, -1), (-1, 1), (1, -1), (1, 1)]:
            add_ray(df, dr)

    elif piece == PieceType.ROOK:
        for df, dr in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            add_ray(df, dr)

    elif piece == PieceType.BISHOP:
        for df, dr in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
            add_ray(df, dr)

    elif piece == PieceType.KNIGHT:
        for df, dr in [(-2, -1), (-2, 1), (-1, -2), (-1, 2),
                       (1, -2), (1, 2), (2, -1), (2, 1)]:
            add_if_valid(file_idx + df, rank_idx + dr)

    elif piece == PieceType.PAWN_WHITE:
        add_if_valid(file_idx, rank_idx + 1)
        if rank_idx == 1:
            add_if_valid(file_idx, rank_idx + 2)
        add_if_valid(file_idx - 1, rank_idx + 1)
        add_if_valid(file_idx + 1, rank_idx + 1)

    elif piece == PieceType.PAWN_BLACK:
        add_if_valid(file_idx, rank_idx - 1)
        if rank_idx == 6:
            add_if_valid(file_idx, rank_idx - 2)
        add_if_valid(file_idx - 1, rank_idx - 1)
        add_if_valid(file_idx + 1, rank_idx - 1)

    return moves


class ChessProjectorNode(Node):
    """ROS2 node that projects chess moves onto a physical board."""

    COLORS = {
        "background": (0, 0, 0),
        "calibration": (255, 255, 0),
        "grid": (40, 40, 40),
        "selected": (80, 80, 255, 180),
        "possible_move": (80, 255, 80, 150),
        "text": (255, 255, 255),
        "text_dim": (120, 120, 120),
        "piece_label": (255, 200, 50),
    }

    def __init__(self):
        super().__init__('chess_projector')

        # Declare parameters
        self.declare_parameter('calibration_file', '')
        self.declare_parameter('fullscreen', False)
        self.declare_parameter('display_width', 1280)
        self.declare_parameter('display_height', 720)

        # Get parameters
        self.calibration_file = self.get_parameter('calibration_file').value
        self.start_fullscreen = self.get_parameter('fullscreen').value
        self.width = self.get_parameter('display_width').value
        self.height = self.get_parameter('display_height').value

        # Subscribers
        self.square_sub = self.create_subscription(
            String, '/chess/square', self.square_callback, 10)
        self.piece_sub = self.create_subscription(
            String, '/chess/piece', self.piece_callback, 10)
        self.clear_sub = self.create_subscription(
            Empty, '/chess/clear', self.clear_callback, 10)

        # State (thread-safe access)
        self.lock = threading.Lock()
        self.selected_square: Optional[str] = None
        self.selected_piece: Optional[PieceType] = None
        self.possible_moves: Set[str] = set()
        self.state_changed = False

        # Pygame state
        self.mode = Mode.CALIBRATE
        self.is_fullscreen = False
        self.corners = []
        self.selected_corner = 0
        self.squares: Dict[str, Square] = {}
        self.running = True

        self.get_logger().info('Chess Projector Node initialized')
        self.get_logger().info('Subscribed to: /chess/square, /chess/piece, /chess/clear')

    def square_callback(self, msg: String):
        """Handle square selection from ROS topic."""
        square = msg.data.lower().strip()
        if len(square) == 2 and square[0] in FILES and square[1] in RANKS:
            with self.lock:
                self.selected_square = square
                self._update_moves()
                self.state_changed = True
            self.get_logger().info(f'Square selected: {square}')
        else:
            self.get_logger().warn(f'Invalid square: {msg.data}')

    def piece_callback(self, msg: String):
        """Handle piece selection from ROS topic."""
        piece_str = msg.data.lower().strip()
        piece_map = {
            'king': PieceType.KING,
            'queen': PieceType.QUEEN,
            'rook': PieceType.ROOK,
            'bishop': PieceType.BISHOP,
            'knight': PieceType.KNIGHT,
            'pawn_white': PieceType.PAWN_WHITE,
            'pawn_black': PieceType.PAWN_BLACK,
            'pawn': PieceType.PAWN_WHITE,  # Default to white
        }

        if piece_str in piece_map:
            with self.lock:
                self.selected_piece = piece_map[piece_str]
                self._update_moves()
                self.state_changed = True
            self.get_logger().info(f'Piece selected: {piece_str}')
        else:
            self.get_logger().warn(f'Invalid piece: {msg.data}. Valid: {list(piece_map.keys())}')

    def clear_callback(self, msg: Empty):
        """Handle clear command from ROS topic."""
        with self.lock:
            self.selected_square = None
            self.selected_piece = None
            self.possible_moves = set()
            self.state_changed = True
        self.get_logger().info('Highlights cleared')

    def _update_moves(self):
        """Update possible moves (must be called with lock held)."""
        if self.selected_square and self.selected_piece:
            self.possible_moves = get_piece_moves(self.selected_square, self.selected_piece)
        else:
            self.possible_moves = set()

    def _init_pygame(self):
        """Initialize pygame display."""
        pygame.init()
        pygame.display.set_caption("Chess Projector - ROS2 Node")

        if self.start_fullscreen:
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            info = pygame.display.Info()
            self.width, self.height = info.current_w, info.current_h
            self.is_fullscreen = True
        else:
            self.screen = pygame.display.set_mode(
                (self.width, self.height), pygame.RESIZABLE)

        self.clock = pygame.time.Clock()

        # Initialize corners
        margin = 100
        self.corners = [
            [margin, margin],
            [self.width - margin, margin],
            [self.width - margin, self.height - margin],
            [margin, self.height - margin],
        ]

        self._load_calibration()
        self._compute_squares()

    def _compute_squares(self):
        """Compute pixel positions for all 64 squares."""
        self.squares.clear()

        tl = np.array(self.corners[0])
        tr = np.array(self.corners[1])
        br = np.array(self.corners[2])
        bl = np.array(self.corners[3])

        for file_idx, file in enumerate(FILES):
            for rank_idx, rank in enumerate(RANKS):
                u = (file_idx + 0.5) / 8
                v = 1 - (rank_idx + 0.5) / 8

                top = tl + (tr - tl) * u
                bottom = bl + (br - bl) * u
                pos = top + (bottom - top) * v

                square_width = np.linalg.norm(tr - tl) / 8
                square_height = np.linalg.norm(bl - tl) / 8
                size = int((square_width + square_height) / 2)

                self.squares[f"{file}{rank}"] = Square(
                    file=file, rank=rank,
                    x=int(pos[0]), y=int(pos[1]), size=size
                )

    def _save_calibration(self):
        """Save calibration to file."""
        if self.calibration_file:
            path = Path(self.calibration_file)
        else:
            path = Path.home() / '.chess_projector_calibration.json'

        with open(path, "w") as f:
            json.dump({"corners": self.corners}, f, indent=2)
        self.get_logger().info(f'Calibration saved to {path}')

    def _load_calibration(self):
        """Load calibration from file."""
        if self.calibration_file:
            path = Path(self.calibration_file)
        else:
            path = Path.home() / '.chess_projector_calibration.json'

        if path.exists():
            try:
                with open(path) as f:
                    data = json.load(f)
                    self.corners = data["corners"]
                self.get_logger().info(f'Loaded calibration from {path}')
            except Exception as e:
                self.get_logger().warn(f'Could not load calibration: {e}')

    def _draw_grid_preview(self):
        """Draw chess grid preview."""
        tl = np.array(self.corners[0])
        tr = np.array(self.corners[1])
        br = np.array(self.corners[2])
        bl = np.array(self.corners[3])

        for i in range(9):
            t = i / 8
            left = tl + (bl - tl) * t
            right = tr + (br - tr) * t
            pygame.draw.line(
                self.screen, self.COLORS["grid"],
                (int(left[0]), int(left[1])),
                (int(right[0]), int(right[1])), 1)

        for i in range(9):
            t = i / 8
            top = tl + (tr - tl) * t
            bottom = bl + (br - bl) * t
            pygame.draw.line(
                self.screen, self.COLORS["grid"],
                (int(top[0]), int(top[1])),
                (int(bottom[0]), int(bottom[1])), 1)

    def _draw_calibration(self):
        """Draw calibration interface."""
        self.screen.fill(self.COLORS["background"])

        labels = ["a8 (top-left)", "h8 (top-right)", "h1 (bottom-right)", "a1 (bottom-left)"]

        for i, (corner, label) in enumerate(zip(self.corners, labels)):
            x, y = int(corner[0]), int(corner[1])
            color = (255, 100, 100) if i == self.selected_corner else self.COLORS["calibration"]
            pygame.draw.circle(self.screen, color, (x, y), 15)
            pygame.draw.circle(self.screen, (255, 255, 255), (x, y), 15, 2)

            font = pygame.font.Font(None, 28)
            text = font.render(f"{i+1}: {label}", True, color)
            self.screen.blit(text, (x + 20, y - 10))

        points = [(int(c[0]), int(c[1])) for c in self.corners]
        pygame.draw.lines(self.screen, self.COLORS["calibration"], True, points, 2)

        self._draw_grid_preview()

        # Instructions
        font = pygame.font.Font(None, 28)
        lines = [
            "=== CALIBRATION MODE ===",
            f"Selected corner: {self.selected_corner + 1}",
            "Arrow keys to move (Shift for faster)",
            "ENTER: Save and start | R: Reset | ESC: Quit"
        ]
        y = 20
        for line in lines:
            color = (255, 200, 0) if "===" in line else self.COLORS["text"]
            text = font.render(line, True, color)
            self.screen.blit(text, (20, y))
            y += 30

    def _draw_square_highlight(self, square_name: str, highlight_type: str):
        """Draw a highlight on a square."""
        if square_name not in self.squares:
            return

        sq = self.squares[square_name]
        color = self.COLORS[highlight_type]

        half = sq.size // 2
        surf = pygame.Surface((sq.size, sq.size), pygame.SRCALPHA)
        surf.fill(color)
        self.screen.blit(surf, (sq.x - half, sq.y - half))

        border_color = tuple(min(255, c + 50) for c in color[:3])
        pygame.draw.rect(
            self.screen, border_color,
            (sq.x - half, sq.y - half, sq.size, sq.size), 2)

    def _draw_play_mode(self):
        """Draw play mode with highlights."""
        self.screen.fill(self.COLORS["background"])

        # Get current state (thread-safe)
        with self.lock:
            selected = self.selected_square
            piece = self.selected_piece
            moves = self.possible_moves.copy()

        # Draw possible moves
        for sq_name in moves:
            self._draw_square_highlight(sq_name, "possible_move")

        # Draw selected square
        if selected:
            self._draw_square_highlight(selected, "selected")

        self._draw_grid_preview()

        # Status bar
        font = pygame.font.Font(None, 26)
        piece_name = piece.value if piece else "None"
        square_name = selected if selected else "None"
        status = f"Square: {square_name} | Piece: {piece_name} | Moves: {len(moves)}"
        text = font.render(status, True, self.COLORS["piece_label"])
        self.screen.blit(text, (20, 15))

        font_small = pygame.font.Font(None, 22)
        info = "ROS2: /chess/square, /chess/piece, /chess/clear | ESC: Calibrate | Q: Quit"
        text = font_small.render(info, True, self.COLORS["text_dim"])
        self.screen.blit(text, (20, 45))

    def _handle_events(self) -> bool:
        """Handle pygame events. Returns False to quit."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            elif event.type == pygame.VIDEORESIZE:
                if not self.is_fullscreen:
                    self.width, self.height = event.w, event.h
                    self.screen = pygame.display.set_mode(
                        (self.width, self.height), pygame.RESIZABLE)

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    return False

                elif event.key == pygame.K_f:
                    self.is_fullscreen = not self.is_fullscreen
                    if self.is_fullscreen:
                        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                        info = pygame.display.Info()
                        self.width, self.height = info.current_w, info.current_h
                    else:
                        self.width, self.height = 1280, 720
                        self.screen = pygame.display.set_mode(
                            (self.width, self.height), pygame.RESIZABLE)

                elif self.mode == Mode.CALIBRATE:
                    self._handle_calibration_key(event)

                elif self.mode == Mode.PLAY:
                    if event.key == pygame.K_ESCAPE:
                        self.mode = Mode.CALIBRATE
                    elif event.key == pygame.K_c:
                        with self.lock:
                            self.selected_square = None
                            self.selected_piece = None
                            self.possible_moves = set()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.mode == Mode.CALIBRATE:
                    self._handle_calibration_click(event.pos)
                elif self.mode == Mode.PLAY:
                    self._handle_play_click(event.pos)

        return True

    def _handle_calibration_key(self, event):
        """Handle calibration keyboard input."""
        key = event.key
        mods = pygame.key.get_mods()
        move_amount = 20 if mods & pygame.KMOD_SHIFT else 5

        if key == pygame.K_LEFT:
            self.corners[self.selected_corner][0] -= move_amount
        elif key == pygame.K_RIGHT:
            self.corners[self.selected_corner][0] += move_amount
        elif key == pygame.K_UP:
            self.corners[self.selected_corner][1] -= move_amount
        elif key == pygame.K_DOWN:
            self.corners[self.selected_corner][1] += move_amount
        elif key == pygame.K_1:
            self.selected_corner = 0
        elif key == pygame.K_2:
            self.selected_corner = 1
        elif key == pygame.K_3:
            self.selected_corner = 2
        elif key == pygame.K_4:
            self.selected_corner = 3
        elif key == pygame.K_RETURN:
            self._compute_squares()
            self._save_calibration()
            self.mode = Mode.PLAY
            self.get_logger().info('Calibration complete, entering play mode')
        elif key == pygame.K_r:
            margin = 100
            self.corners = [
                [margin, margin],
                [self.width - margin, margin],
                [self.width - margin, self.height - margin],
                [margin, self.height - margin],
            ]
        elif key == pygame.K_ESCAPE:
            self.running = False

        self._compute_squares()

    def _handle_calibration_click(self, pos):
        """Select nearest corner on click."""
        min_dist = float('inf')
        for i, corner in enumerate(self.corners):
            dist = math.sqrt((pos[0] - corner[0])**2 + (pos[1] - corner[1])**2)
            if dist < min_dist:
                min_dist = dist
                self.selected_corner = i

    def _handle_play_click(self, pos):
        """Handle click in play mode (for manual testing)."""
        for name, sq in self.squares.items():
            half = sq.size // 2
            if (sq.x - half <= pos[0] <= sq.x + half and
                sq.y - half <= pos[1] <= sq.y + half):
                with self.lock:
                    self.selected_square = name
                    self._update_moves()
                self.get_logger().info(f'Manual square select: {name}')
                break

    def run_pygame_loop(self):
        """Main pygame loop (runs in separate thread)."""
        self._init_pygame()

        while self.running and rclpy.ok():
            if not self._handle_events():
                self.running = False
                break

            if self.mode == Mode.CALIBRATE:
                self._draw_calibration()
            else:
                self._draw_play_mode()

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()
        self.get_logger().info('Pygame window closed')

    def shutdown(self):
        """Clean shutdown."""
        self.running = False


def main(args=None):
    rclpy.init(args=args)
    node = ChessProjectorNode()

    # Run pygame in main thread, ROS2 spinning in background
    spin_thread = threading.Thread(target=rclpy.spin, args=(node,), daemon=True)
    spin_thread.start()

    try:
        node.run_pygame_loop()
    except KeyboardInterrupt:
        pass
    finally:
        node.shutdown()
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()

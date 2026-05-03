"""
Combined Chess + Avatar Projector ROS2 Node

Projects both an animated avatar and chess move hints onto a physical display.
Avatar displays in the top portion, chess board in the bottom.

Subscribed Topics:
    Chess:
        /chess/square (std_msgs/String): Square to select (e.g., "e4")
        /chess/piece (std_msgs/String): Piece type (king/queen/rook/bishop/knight/pawn_white/pawn_black)
        /chess/clear (std_msgs/Empty): Clear chess highlights

    Avatar:
        /avatar/mood (std_msgs/String): Set mood (neutral/happy/sad/thinking/surprised/playful/encouraging/concerned/celebrating)
        /avatar/message (std_msgs/String): Display message below avatar
        /avatar/theme (std_msgs/String): Set color theme (default/warm/winning/losing)

Parameters:
    calibration_file (string): Path to calibration JSON file
    fullscreen (bool): Start in fullscreen mode
    display_width (int): Window width (default 1280)
    display_height (int): Window height (default 720)
    avatar_ratio (float): Ratio of screen height for avatar (default 0.35)
"""

import sys
import math
import json
import time
import random
import threading
import numpy as np
from pathlib import Path
from typing import Dict, Set, Optional, Tuple
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


# =============================================================================
# Chess Board Constants
# =============================================================================

FILES = "abcdefgh"
RANKS = "12345678"


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


# =============================================================================
# Avatar Constants
# =============================================================================

class AvatarMood(Enum):
    NEUTRAL = "neutral"
    HAPPY = "happy"
    THINKING = "thinking"
    ENCOURAGING = "encouraging"
    SURPRISED = "surprised"
    PLAYFUL = "playful"
    CONCERNED = "concerned"
    CELEBRATING = "celebrating"
    SAD = "sad"


@dataclass
class AvatarColors:
    background: Tuple[int, int, int]
    face: Tuple[int, int, int]
    eyes: Tuple[int, int, int]
    mouth: Tuple[int, int, int]
    accent: Tuple[int, int, int]


THEMES = {
    "default": AvatarColors(
        background=(20, 20, 30),
        face=(100, 180, 255),
        eyes=(255, 255, 255),
        mouth=(255, 255, 255),
        accent=(150, 220, 255),
    ),
    "warm": AvatarColors(
        background=(30, 20, 20),
        face=(255, 180, 100),
        eyes=(255, 255, 255),
        mouth=(255, 255, 255),
        accent=(255, 220, 150),
    ),
    "winning": AvatarColors(
        background=(20, 30, 20),
        face=(100, 255, 150),
        eyes=(255, 255, 255),
        mouth=(255, 255, 255),
        accent=(150, 255, 200),
    ),
    "losing": AvatarColors(
        background=(30, 20, 30),
        face=(200, 150, 255),
        eyes=(255, 255, 255),
        mouth=(255, 255, 255),
        accent=(220, 180, 255),
    ),
}


# =============================================================================
# Mode Enum
# =============================================================================

class Mode(Enum):
    CALIBRATE = "calibrate"
    PLAY = "play"


# =============================================================================
# Combined Projector Node
# =============================================================================

class CombinedProjectorNode(Node):
    """ROS2 node that projects avatar and chess moves."""

    COLORS = {
        "background": (0, 0, 0),
        "calibration": (255, 255, 0),
        "grid": (40, 40, 40),
        "selected": (80, 80, 255, 180),
        "possible_move": (80, 255, 80, 150),
        "text": (255, 255, 255),
        "text_dim": (120, 120, 120),
    }

    def __init__(self):
        super().__init__('chess_avatar_projector')

        # Declare parameters
        self.declare_parameter('calibration_file', '')
        self.declare_parameter('fullscreen', False)
        self.declare_parameter('display_width', 1280)
        self.declare_parameter('display_height', 720)
        self.declare_parameter('avatar_ratio', 0.35)

        # Get parameters
        self.calibration_file = self.get_parameter('calibration_file').value
        self.start_fullscreen = self.get_parameter('fullscreen').value
        self.width = self.get_parameter('display_width').value
        self.height = self.get_parameter('display_height').value
        self.avatar_ratio = self.get_parameter('avatar_ratio').value

        # Chess subscribers
        self.square_sub = self.create_subscription(
            String, '/chess/square', self.square_callback, 10)
        self.piece_sub = self.create_subscription(
            String, '/chess/piece', self.piece_callback, 10)
        self.clear_sub = self.create_subscription(
            Empty, '/chess/clear', self.clear_callback, 10)

        # Avatar subscribers
        self.mood_sub = self.create_subscription(
            String, '/avatar/mood', self.mood_callback, 10)
        self.message_sub = self.create_subscription(
            String, '/avatar/message', self.message_callback, 10)
        self.theme_sub = self.create_subscription(
            String, '/avatar/theme', self.theme_callback, 10)

        # Thread-safe state
        self.lock = threading.Lock()

        # Chess state
        self.selected_square: Optional[str] = None
        self.selected_piece: Optional[PieceType] = None
        self.possible_moves: Set[str] = set()

        # Avatar state
        self.avatar_mood = AvatarMood.NEUTRAL
        self.avatar_colors = THEMES["default"]
        self.avatar_message = ""
        self.avatar_message_timer = 0

        # Animation state
        self.blink_timer = 0
        self.blink_duration = 0.15
        self.next_blink = time.time() + random.uniform(2, 5)
        self.is_blinking = False
        self.eye_offset_x = 0
        self.eye_offset_y = 0
        self.target_eye_x = 0
        self.target_eye_y = 0
        self.breath_phase = 0

        # Calibration state
        self.mode = Mode.CALIBRATE
        self.corners = []
        self.selected_corner = 0
        self.squares: Dict[str, Square] = {}

        # Display state
        self.is_fullscreen = False
        self.running = True

        self.get_logger().info('Combined Chess+Avatar Projector initialized')
        self.get_logger().info('Chess topics: /chess/square, /chess/piece, /chess/clear')
        self.get_logger().info('Avatar topics: /avatar/mood, /avatar/message, /avatar/theme')

    # =========================================================================
    # ROS2 Callbacks
    # =========================================================================

    def square_callback(self, msg: String):
        square = msg.data.lower().strip()
        if len(square) == 2 and square[0] in FILES and square[1] in RANKS:
            with self.lock:
                self.selected_square = square
                self._update_moves()
            self.get_logger().info(f'Square: {square}')
        else:
            self.get_logger().warn(f'Invalid square: {msg.data}')

    def piece_callback(self, msg: String):
        piece_str = msg.data.lower().strip()
        piece_map = {
            'king': PieceType.KING,
            'queen': PieceType.QUEEN,
            'rook': PieceType.ROOK,
            'bishop': PieceType.BISHOP,
            'knight': PieceType.KNIGHT,
            'pawn_white': PieceType.PAWN_WHITE,
            'pawn_black': PieceType.PAWN_BLACK,
            'pawn': PieceType.PAWN_WHITE,
        }
        if piece_str in piece_map:
            with self.lock:
                self.selected_piece = piece_map[piece_str]
                self._update_moves()
            self.get_logger().info(f'Piece: {piece_str}')
        else:
            self.get_logger().warn(f'Invalid piece: {msg.data}')

    def clear_callback(self, msg: Empty):
        with self.lock:
            self.selected_square = None
            self.selected_piece = None
            self.possible_moves = set()
        self.get_logger().info('Chess highlights cleared')

    def mood_callback(self, msg: String):
        mood_str = msg.data.lower().strip()
        mood_map = {m.value: m for m in AvatarMood}
        if mood_str in mood_map:
            with self.lock:
                self.avatar_mood = mood_map[mood_str]
            self.get_logger().info(f'Mood: {mood_str}')
        else:
            self.get_logger().warn(f'Invalid mood: {msg.data}. Valid: {list(mood_map.keys())}')

    def message_callback(self, msg: String):
        with self.lock:
            self.avatar_message = msg.data
            self.avatar_message_timer = time.time() + 5.0
        self.get_logger().info(f'Message: {msg.data}')

    def theme_callback(self, msg: String):
        theme_str = msg.data.lower().strip()
        if theme_str in THEMES:
            with self.lock:
                self.avatar_colors = THEMES[theme_str]
            self.get_logger().info(f'Theme: {theme_str}')
        else:
            self.get_logger().warn(f'Invalid theme: {msg.data}. Valid: {list(THEMES.keys())}')

    def _update_moves(self):
        """Update possible moves (must be called with lock held)."""
        if self.selected_square and self.selected_piece:
            self.possible_moves = get_piece_moves(self.selected_square, self.selected_piece)
        else:
            self.possible_moves = set()

    # =========================================================================
    # Pygame Initialization
    # =========================================================================

    def _init_pygame(self):
        pygame.init()
        pygame.display.set_caption("Chess + Avatar Projector - ROS2")

        if self.start_fullscreen:
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            info = pygame.display.Info()
            self.width, self.height = info.current_w, info.current_h
            self.is_fullscreen = True
        else:
            self.screen = pygame.display.set_mode(
                (self.width, self.height), pygame.RESIZABLE)

        self.clock = pygame.time.Clock()
        self._update_layout()
        self._load_calibration()
        self._compute_squares()

    def _update_layout(self):
        """Update layout regions for avatar and board."""
        self.avatar_height = int(self.height * self.avatar_ratio)
        self.board_top = self.avatar_height
        self.board_height = self.height - self.avatar_height

        # Avatar center
        self.avatar_center_x = self.width // 2
        self.avatar_center_y = self.avatar_height // 2
        self.face_radius = min(self.width, self.avatar_height) * 0.3

        # Board corners (default)
        margin = 50
        board_size = min(self.width - 2 * margin, self.board_height - 2 * margin)
        board_left = (self.width - board_size) // 2
        board_right = board_left + board_size

        self.corners = [
            [board_left, self.board_top + margin],
            [board_right, self.board_top + margin],
            [board_right, self.board_top + margin + board_size],
            [board_left, self.board_top + margin + board_size],
        ]

    # =========================================================================
    # Calibration
    # =========================================================================

    def _compute_squares(self):
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
        if self.calibration_file:
            path = Path(self.calibration_file)
        else:
            path = Path.home() / '.chess_avatar_calibration.json'
        with open(path, "w") as f:
            json.dump({"corners": self.corners}, f, indent=2)
        self.get_logger().info(f'Calibration saved to {path}')

    def _load_calibration(self):
        if self.calibration_file:
            path = Path(self.calibration_file)
        else:
            path = Path.home() / '.chess_avatar_calibration.json'
        if path.exists():
            try:
                with open(path) as f:
                    data = json.load(f)
                    self.corners = data["corners"]
                self.get_logger().info(f'Loaded calibration from {path}')
            except Exception as e:
                self.get_logger().warn(f'Could not load calibration: {e}')

    # =========================================================================
    # Avatar Drawing
    # =========================================================================

    def _update_avatar_animations(self, dt: float):
        current_time = time.time()

        # Blinking
        if not self.is_blinking and current_time >= self.next_blink:
            self.is_blinking = True
            self.blink_timer = current_time
        if self.is_blinking and current_time - self.blink_timer > self.blink_duration:
            self.is_blinking = False
            self.next_blink = current_time + random.uniform(2, 5)

        # Eye drift
        if random.random() < 0.02:
            self.target_eye_x = random.uniform(-10, 10)
            self.target_eye_y = random.uniform(-5, 5)
        self.eye_offset_x += (self.target_eye_x - self.eye_offset_x) * 0.1
        self.eye_offset_y += (self.target_eye_y - self.eye_offset_y) * 0.1

        # Breathing
        self.breath_phase += dt * 2
        if self.breath_phase > 2 * math.pi:
            self.breath_phase -= 2 * math.pi

        # Message timeout
        with self.lock:
            if self.avatar_message and current_time > self.avatar_message_timer:
                self.avatar_message = ""

    def _draw_avatar(self):
        with self.lock:
            colors = self.avatar_colors
            mood = self.avatar_mood
            message = self.avatar_message

        # Background for avatar region
        pygame.draw.rect(self.screen, colors.background,
                         (0, 0, self.width, self.avatar_height))

        # Face
        breath_scale = 1 + math.sin(self.breath_phase) * 0.01
        radius = int(self.face_radius * breath_scale)

        # Glow
        for i in range(3):
            glow_radius = radius + 10 + i * 5
            glow_surface = pygame.Surface((glow_radius * 2, glow_radius * 2), pygame.SRCALPHA)
            glow_alpha = 50 - i * 15
            pygame.draw.circle(glow_surface, (*colors.accent, glow_alpha),
                               (glow_radius, glow_radius), glow_radius)
            self.screen.blit(glow_surface,
                             (self.avatar_center_x - glow_radius,
                              self.avatar_center_y - glow_radius))

        pygame.draw.circle(self.screen, colors.face,
                           (self.avatar_center_x, self.avatar_center_y), radius)

        # Eyes
        self._draw_avatar_eyes(mood, colors)

        # Mouth
        self._draw_avatar_mouth(mood, colors)

        # Message
        if message:
            font = pygame.font.Font(None, 32)
            text_surface = font.render(message, True, colors.accent)
            text_rect = text_surface.get_rect(
                center=(self.avatar_center_x, self.avatar_height - 30))
            self.screen.blit(text_surface, text_rect)

    def _draw_avatar_eyes(self, mood: AvatarMood, colors: AvatarColors):
        eye_y = self.avatar_center_y - self.face_radius * 0.15
        eye_spacing = self.face_radius * 0.35
        eye_radius = self.face_radius * 0.12
        pupil_radius = eye_radius * 0.5

        left_eye_x = self.avatar_center_x - eye_spacing
        right_eye_x = self.avatar_center_x + eye_spacing

        if self.is_blinking:
            for eye_x in [left_eye_x, right_eye_x]:
                pygame.draw.line(self.screen, colors.eyes,
                                 (eye_x - eye_radius, eye_y),
                                 (eye_x + eye_radius, eye_y), 3)
            return

        if mood in (AvatarMood.HAPPY, AvatarMood.CELEBRATING):
            for eye_x in [left_eye_x, right_eye_x]:
                pygame.draw.arc(self.screen, colors.eyes,
                                (eye_x - eye_radius, eye_y - eye_radius // 2,
                                 eye_radius * 2, eye_radius),
                                0, math.pi, 4)
        elif mood in (AvatarMood.SAD, AvatarMood.CONCERNED):
            for eye_x in [left_eye_x, right_eye_x]:
                pygame.draw.ellipse(self.screen, colors.eyes,
                                    (eye_x - eye_radius, eye_y - eye_radius * 0.7,
                                     eye_radius * 2, eye_radius * 1.4))
        elif mood == AvatarMood.SURPRISED:
            for eye_x in [left_eye_x, right_eye_x]:
                pygame.draw.circle(self.screen, colors.eyes,
                                   (int(eye_x), int(eye_y)), int(eye_radius * 1.3))
                pygame.draw.circle(self.screen, colors.face,
                                   (int(eye_x + self.eye_offset_x),
                                    int(eye_y + self.eye_offset_y)),
                                   int(pupil_radius * 0.8))
        elif mood == AvatarMood.THINKING:
            for eye_x in [left_eye_x, right_eye_x]:
                pygame.draw.circle(self.screen, colors.eyes,
                                   (int(eye_x), int(eye_y)), int(eye_radius))
                pygame.draw.circle(self.screen, colors.face,
                                   (int(eye_x + 8), int(eye_y - 5)), int(pupil_radius))
        elif mood == AvatarMood.PLAYFUL:
            pygame.draw.circle(self.screen, colors.eyes,
                               (int(left_eye_x), int(eye_y)), int(eye_radius))
            pygame.draw.circle(self.screen, colors.face,
                               (int(left_eye_x + self.eye_offset_x),
                                int(eye_y + self.eye_offset_y)), int(pupil_radius))
            pygame.draw.arc(self.screen, colors.eyes,
                            (right_eye_x - eye_radius, eye_y - eye_radius // 2,
                             eye_radius * 2, eye_radius),
                            0, math.pi, 4)
        else:
            for eye_x in [left_eye_x, right_eye_x]:
                pygame.draw.circle(self.screen, colors.eyes,
                                   (int(eye_x), int(eye_y)), int(eye_radius))
                pygame.draw.circle(self.screen, colors.face,
                                   (int(eye_x + self.eye_offset_x),
                                    int(eye_y + self.eye_offset_y)), int(pupil_radius))

    def _draw_avatar_mouth(self, mood: AvatarMood, colors: AvatarColors):
        mouth_y = self.avatar_center_y + self.face_radius * 0.3
        mouth_width = self.face_radius * 0.4

        if mood in (AvatarMood.HAPPY, AvatarMood.CELEBRATING):
            rect = pygame.Rect(
                self.avatar_center_x - mouth_width,
                mouth_y - mouth_width * 0.3,
                mouth_width * 2,
                mouth_width
            )
            pygame.draw.arc(self.screen, colors.mouth, rect, math.pi, 2 * math.pi, 4)
        elif mood == AvatarMood.SAD:
            rect = pygame.Rect(
                self.avatar_center_x - mouth_width,
                mouth_y,
                mouth_width * 2,
                mouth_width * 0.6
            )
            pygame.draw.arc(self.screen, colors.mouth, rect, 0, math.pi, 4)
        elif mood == AvatarMood.SURPRISED:
            pygame.draw.circle(self.screen, colors.mouth,
                               (self.avatar_center_x, int(mouth_y + 10)),
                               int(mouth_width * 0.3), 3)
        elif mood == AvatarMood.THINKING:
            pygame.draw.circle(self.screen, colors.mouth,
                               (int(self.avatar_center_x + 15), int(mouth_y)),
                               int(mouth_width * 0.15), 3)
        elif mood == AvatarMood.PLAYFUL:
            points = [
                (self.avatar_center_x - mouth_width * 0.5, mouth_y),
                (self.avatar_center_x + mouth_width * 0.3, mouth_y - 10),
                (self.avatar_center_x + mouth_width * 0.5, mouth_y - 20),
            ]
            pygame.draw.lines(self.screen, colors.mouth, False, points, 4)
        elif mood == AvatarMood.ENCOURAGING:
            rect = pygame.Rect(
                self.avatar_center_x - mouth_width * 0.7,
                mouth_y - mouth_width * 0.2,
                mouth_width * 1.4,
                mouth_width * 0.5
            )
            pygame.draw.arc(self.screen, colors.mouth, rect, math.pi, 2 * math.pi, 3)
        elif mood == AvatarMood.CONCERNED:
            points = [
                (self.avatar_center_x - mouth_width * 0.5, mouth_y),
                (self.avatar_center_x - mouth_width * 0.2, mouth_y + 5),
                (self.avatar_center_x + mouth_width * 0.2, mouth_y - 5),
                (self.avatar_center_x + mouth_width * 0.5, mouth_y),
            ]
            pygame.draw.lines(self.screen, colors.mouth, False, points, 3)
        else:
            pygame.draw.line(self.screen, colors.mouth,
                             (self.avatar_center_x - mouth_width * 0.5, mouth_y),
                             (self.avatar_center_x + mouth_width * 0.5, mouth_y), 3)

    # =========================================================================
    # Chess Board Drawing
    # =========================================================================

    def _draw_board_grid(self):
        tl = np.array(self.corners[0])
        tr = np.array(self.corners[1])
        br = np.array(self.corners[2])
        bl = np.array(self.corners[3])

        for i in range(9):
            t = i / 8
            left = tl + (bl - tl) * t
            right = tr + (br - tr) * t
            pygame.draw.line(self.screen, self.COLORS["grid"],
                             (int(left[0]), int(left[1])),
                             (int(right[0]), int(right[1])), 1)

        for i in range(9):
            t = i / 8
            top = tl + (tr - tl) * t
            bottom = bl + (br - bl) * t
            pygame.draw.line(self.screen, self.COLORS["grid"],
                             (int(top[0]), int(top[1])),
                             (int(bottom[0]), int(bottom[1])), 1)

    def _draw_square_highlight(self, square_name: str, highlight_type: str):
        if square_name not in self.squares:
            return
        sq = self.squares[square_name]
        color = self.COLORS[highlight_type]
        half = sq.size // 2
        surf = pygame.Surface((sq.size, sq.size), pygame.SRCALPHA)
        surf.fill(color)
        self.screen.blit(surf, (sq.x - half, sq.y - half))
        border_color = tuple(min(255, c + 50) for c in color[:3])
        pygame.draw.rect(self.screen, border_color,
                         (sq.x - half, sq.y - half, sq.size, sq.size), 2)

    def _draw_chess_highlights(self):
        with self.lock:
            selected = self.selected_square
            moves = self.possible_moves.copy()

        for sq_name in moves:
            self._draw_square_highlight(sq_name, "possible_move")
        if selected:
            self._draw_square_highlight(selected, "selected")

    # =========================================================================
    # Calibration Mode
    # =========================================================================

    def _draw_calibration(self):
        self.screen.fill(self.COLORS["background"])

        # Draw avatar region hint
        pygame.draw.rect(self.screen, (30, 30, 40),
                         (0, 0, self.width, self.avatar_height))
        font = pygame.font.Font(None, 36)
        text = font.render("Avatar Region", True, (80, 80, 80))
        self.screen.blit(text, (self.width // 2 - 80, self.avatar_height // 2 - 10))

        # Draw board calibration
        labels = ["a8", "h8", "h1", "a1"]
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
        self._draw_board_grid()

        # Instructions
        font = pygame.font.Font(None, 26)
        lines = [
            "CALIBRATION: Align board corners",
            f"Corner {self.selected_corner + 1} selected (1-4 to change)",
            "Arrows: move | Shift: faster | ENTER: save | R: reset"
        ]
        y = self.board_top + 10
        for line in lines:
            text = font.render(line, True, self.COLORS["text"])
            self.screen.blit(text, (20, y))
            y += 28

    # =========================================================================
    # Play Mode
    # =========================================================================

    def _draw_play_mode(self):
        self.screen.fill(self.COLORS["background"])

        # Avatar
        self._draw_avatar()

        # Separator line
        pygame.draw.line(self.screen, (60, 60, 60),
                         (0, self.avatar_height), (self.width, self.avatar_height), 2)

        # Chess board
        self._draw_chess_highlights()
        self._draw_board_grid()

        # Status
        font = pygame.font.Font(None, 22)
        with self.lock:
            sq = self.selected_square or "-"
            pc = self.selected_piece.value if self.selected_piece else "-"
            mood = self.avatar_mood.value
        status = f"Square: {sq} | Piece: {pc} | Mood: {mood}"
        text = font.render(status, True, self.COLORS["text_dim"])
        self.screen.blit(text, (10, self.height - 25))

    # =========================================================================
    # Event Handling
    # =========================================================================

    def _handle_events(self) -> bool:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            elif event.type == pygame.VIDEORESIZE:
                if not self.is_fullscreen:
                    self.width, self.height = event.w, event.h
                    self.screen = pygame.display.set_mode(
                        (self.width, self.height), pygame.RESIZABLE)
                    self._update_layout()
                    self._compute_squares()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    return False
                elif event.key == pygame.K_f:
                    self._toggle_fullscreen()
                elif self.mode == Mode.CALIBRATE:
                    self._handle_calibration_key(event)
                elif self.mode == Mode.PLAY:
                    if event.key == pygame.K_ESCAPE:
                        self.mode = Mode.CALIBRATE

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.mode == Mode.CALIBRATE:
                    self._handle_calibration_click(event.pos)

        return True

    def _toggle_fullscreen(self):
        self.is_fullscreen = not self.is_fullscreen
        if self.is_fullscreen:
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            info = pygame.display.Info()
            self.width, self.height = info.current_w, info.current_h
        else:
            self.width, self.height = 1280, 720
            self.screen = pygame.display.set_mode(
                (self.width, self.height), pygame.RESIZABLE)
        self._update_layout()
        self._compute_squares()

    def _handle_calibration_key(self, event):
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
            self.get_logger().info('Calibration saved, entering play mode')
        elif key == pygame.K_r:
            self._update_layout()
        elif key == pygame.K_ESCAPE:
            self.running = False

        self._compute_squares()

    def _handle_calibration_click(self, pos):
        min_dist = float('inf')
        for i, corner in enumerate(self.corners):
            dist = math.sqrt((pos[0] - corner[0])**2 + (pos[1] - corner[1])**2)
            if dist < min_dist:
                min_dist = dist
                self.selected_corner = i

    # =========================================================================
    # Main Loop
    # =========================================================================

    def run_pygame_loop(self):
        self._init_pygame()
        last_time = time.time()

        while self.running and rclpy.ok():
            current_time = time.time()
            dt = current_time - last_time
            last_time = current_time

            if not self._handle_events():
                self.running = False
                break

            self._update_avatar_animations(dt)

            if self.mode == Mode.CALIBRATE:
                self._draw_calibration()
            else:
                self._draw_play_mode()

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()
        self.get_logger().info('Display closed')

    def shutdown(self):
        self.running = False


def main(args=None):
    rclpy.init(args=args)
    node = CombinedProjectorNode()

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

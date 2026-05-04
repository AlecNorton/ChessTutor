"""Load puzzles from the Lichess puzzle database (CSV format).

Expected CSV columns (no header in the official DB, but we handle both):
  PuzzleId, FEN, Moves, Rating, RatingDeviation, Popularity, NbPlays,
  Themes, GameUrl, OpeningTags

Download the full database from:
  https://database.lichess.org/lichess_db_puzzle.csv.zst
"""

import csv
import random
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional


COLUMN_NAMES = [
    "PuzzleId", "FEN", "Moves", "Rating", "RatingDeviation",
    "Popularity", "NbPlays", "Themes", "GameUrl", "OpeningTags",
]


@dataclass
class Puzzle:
    puzzle_id: str
    fen: str  # starting position (before the opponent's last move)
    moves: list[str]  # UCI moves: first is opponent's last move, rest are the solution
    rating: int
    themes: list[str] = field(default_factory=list)
    game_url: str = ""

    @property
    def opponent_move(self) -> str:
        """The move that sets up the puzzle (played automatically)."""
        return self.moves[0]

    @property
    def solution_moves(self) -> list[str]:
        """The moves the player must find (player move, opponent reply, …)."""
        return self.moves[1:]


def load_puzzles(
    path: str | Path,
    *,
    min_rating: int = 0,
    max_rating: int = 9999,
    themes: Optional[set[str]] = None,
    limit: int = 500,
) -> list[Puzzle]:
    """Load puzzles from a Lichess-format CSV file.

    Reads up to `limit` puzzles that match the filters.
    """
    path = Path(path)
    puzzles: list[Puzzle] = []

    with open(path, newline="", encoding="utf-8") as f:
        # Detect whether the file has a header row
        first_line = f.readline()
        f.seek(0)

        has_header = first_line.strip().startswith("PuzzleId")
        reader = csv.reader(f)
        if has_header:
            next(reader)  # skip header

        for row in reader:
            if len(row) < 8:
                continue

            rating = int(row[3])
            if rating < min_rating or rating > max_rating:
                continue

            puzzle_themes = row[7].split() if row[7] else []
            if themes and not themes.intersection(puzzle_themes):
                continue

            puzzles.append(Puzzle(
                puzzle_id=row[0],
                fen=row[1],
                moves=row[2].split(),
                rating=rating,
                themes=puzzle_themes,
                game_url=row[8] if len(row) > 8 else "",
            ))

            if len(puzzles) >= limit:
                break

    return puzzles


def pick_random(puzzles: list[Puzzle]) -> Puzzle:
    return random.choice(puzzles)


# ---------------------------------------------------------------------------
# Built-in sample puzzles for quick testing without downloading the full DB
# ---------------------------------------------------------------------------
SAMPLE_PUZZLES = [
    # Easy mate-in-1 / mate-in-2 puzzles (rating < 500) so the fallback list
    # still has options when the rating filter is set to a beginner band.
    Puzzle(
        puzzle_id="00K48",
        fen="6Qk/6pp/p2B4/2pP4/P1q5/6P1/2P1p2P/5RK1 b - - 0 26",
        moves=["h8g8", "f1f8"],
        rating=425,
        themes=["endgame", "mate", "mateIn1", "oneMove"],
        game_url="https://lichess.org/vGu9FCAH/black#52",
    ),
    Puzzle(
        puzzle_id="0HZ4M",
        fen="5R2/8/5Kpk/5p1p/7P/6r1/8/8 b - - 1 65",
        moves=["g3g4", "f8h8"],
        rating=471,
        themes=["endgame", "mate", "mateIn1", "oneMove", "rookEndgame"],
        game_url="https://lichess.org/tYkh2wYL/black#130",
    ),
    Puzzle(
        puzzle_id="0Hv5v",
        fen="7k/pp3rpp/8/8/8/2P5/P5PP/4R2K b - - 0 26",
        moves=["f7f2", "e1e8", "f2f8", "e8f8"],
        rating=455,
        themes=["backRankMate", "endgame", "mate", "mateIn2", "short"],
        game_url="https://lichess.org/Wu4Itd7H/black#52",
    ),
    Puzzle(
        puzzle_id="ueIE9",
        fen="3r1rk1/ppp2pp1/1b5p/8/4NqP1/2P4P/PPQ2PK1/R3R3 w - - 2 22",
        moves=["e4g3", "d8d2", "c2d2", "f4d2"],
        rating=1427,
        themes=["middlegame", "short", "crushing"],
        game_url="https://lichess.org/Ecbh5o6B",
    ),
    Puzzle(
        puzzle_id="MsLLI",
        fen="r3k2r/1bppnppp/p4q2/1p2P3/3p1b2/1B3Q2/PPPP1PPP/RNB2RK1 b kq - 0 12",
        moves=["b7f3", "e5f6", "g7f6", "g2f3"],
        rating=1314,
        themes=["advantage", "intermezzo", "short", "middlegame"],
        game_url="https://lichess.org/BEM11EwS",
    ),
    Puzzle(
        puzzle_id="Ba2Gw",
        fen="r1b2r1k/p1p2q2/1p5p/3R2p1/3P3n/2P3N1/PPB2PPP/R2Q2K1 w - - 3 21",
        moves=["d1h5", "f7f2", "g1h1", "f2g2"],
        rating=1414,
        themes=["mateIn2", "middlegame", "short", "fork"],
        game_url="https://lichess.org/YULrVzBF",
    ),
    Puzzle(
        puzzle_id="RzuDT",
        fen="4k2r/1q1r1p1p/4p1p1/2R3N1/1p2N3/2b1P3/P1Q3PP/6K1 b k - 2 28",
        moves=["d7c7", "e4d6", "e8e7", "d6b7"],
        rating=1415,
        themes=["middlegame", "short", "crushing", "fork"],
        game_url="https://lichess.org/XIiBBhGK",
    ),
    Puzzle(
        puzzle_id="CotyG",
        fen="2kr2nr/ppp1qppp/2nb4/1B6/4P1b1/5N2/PPP2PPP/RNBQR1K1 w - - 8 9",
        moves=["b5c6", "d6h2", "g1h2", "d8d1"],
        rating=1434,
        themes=["short", "advantage", "opening", "kingsideAttack", "discoveredAttack"],
        game_url="https://lichess.org/y5ZnaRhB",
    ),
]

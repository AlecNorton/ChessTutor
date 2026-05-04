"""Fetch puzzles from the Lichess API and save as a local CSV.

Usage:
    python fetch_puzzles.py                  # fetch 50 puzzles
    python fetch_puzzles.py --count 200      # fetch 200 puzzles (in batches of 50)
    python fetch_puzzles.py --output my_puzzles.csv
"""

import argparse
import csv
import json
import sys
import urllib.request

import chess

LICHESS_BATCH_URL = "https://lichess.org/api/puzzle/batch/mix?nb=50"


def pgn_to_board(pgn: str, initial_ply: int) -> tuple[chess.Board, str]:
    """Replay a PGN up to initial_ply and return the board + last move UCI.

    Returns (board_at_puzzle_start, opponent_setup_move_uci).
    The board is the position AFTER the opponent's setup move.
    The opponent's setup move is the move at initial_ply.
    """
    board = chess.Board()
    moves_san = pgn.split()
    last_move_uci = ""

    for i, san in enumerate(moves_san):
        move = board.parse_san(san)
        if i == initial_ply:
            # This is one move past where the puzzle position starts
            break
        last_move_uci = move.uci()
        board.push(move)

    return board, last_move_uci


def fetch_batch() -> list[dict]:
    """Fetch one batch of 50 puzzles from Lichess."""
    req = urllib.request.Request(
        LICHESS_BATCH_URL,
        headers={"Accept": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=15) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    return data.get("puzzles", [])


def convert_puzzle(raw: dict) -> dict | None:
    """Convert a Lichess API puzzle to our CSV row format.

    Returns None if the puzzle can't be converted (e.g., bad PGN).
    """
    puzzle = raw["puzzle"]
    game = raw["game"]
    pgn = game["pgn"]
    initial_ply = puzzle["initialPly"]
    solution = puzzle["solution"]

    try:
        board = chess.Board()
        moves_san = pgn.split()

        # Replay to one move before initialPly to get the FEN before the setup move
        for i, san in enumerate(moves_san):
            if i >= initial_ply:
                break
            move = board.parse_san(san)
            board.push(move)

        # The move at initialPly is the opponent's setup move
        if initial_ply < len(moves_san):
            setup_move = board.parse_san(moves_san[initial_ply])
            setup_uci = setup_move.uci()
        else:
            return None

        fen_before_setup = board.fen()

        # Verify setup move is legal
        if setup_move not in board.legal_moves:
            return None

        # Full move list: setup move + solution
        all_moves = [setup_uci] + solution

        # Verify each solution move is legal
        board.push(setup_move)
        for uci in solution:
            move = chess.Move.from_uci(uci)
            if move not in board.legal_moves:
                return None
            board.push(move)

    except Exception:
        return None

    return {
        "PuzzleId": puzzle["id"],
        "FEN": fen_before_setup,
        "Moves": " ".join(all_moves),
        "Rating": puzzle["rating"],
        "RatingDeviation": 0,
        "Popularity": puzzle["plays"],
        "NbPlays": puzzle["plays"],
        "Themes": " ".join(puzzle["themes"]),
        "GameUrl": f"https://lichess.org/{game['id']}",
        "OpeningTags": "",
    }


def main():
    parser = argparse.ArgumentParser(description="Fetch Lichess puzzles")
    parser.add_argument("--count", type=int, default=50, help="Number of puzzles to fetch")
    parser.add_argument("--output", type=str, default="puzzles.csv", help="Output CSV file")
    args = parser.parse_args()

    puzzles = []
    batches_needed = (args.count + 49) // 50

    print(f"Fetching {args.count} puzzles from Lichess...")
    for i in range(batches_needed):
        print(f"  Batch {i + 1}/{batches_needed}...", end=" ", flush=True)
        try:
            raw_puzzles = fetch_batch()
            for raw in raw_puzzles:
                converted = convert_puzzle(raw)
                if converted:
                    puzzles.append(converted)
            print(f"got {len(raw_puzzles)} puzzles ({len(puzzles)} total valid)")
        except Exception as e:
            print(f"error: {e}")

        if len(puzzles) >= args.count:
            puzzles = puzzles[: args.count]
            break

    if not puzzles:
        print("No puzzles fetched!")
        sys.exit(1)

    # Write CSV
    fieldnames = [
        "PuzzleId", "FEN", "Moves", "Rating", "RatingDeviation",
        "Popularity", "NbPlays", "Themes", "GameUrl", "OpeningTags",
    ]
    with open(args.output, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(puzzles)

    ratings = [p["Rating"] for p in puzzles]
    print(f"\nSaved {len(puzzles)} puzzles to {args.output}")
    print(f"Rating range: {min(ratings)} - {max(ratings)}")


if __name__ == "__main__":
    main()

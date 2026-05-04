"""Chess Puzzle Tutor — Terminal Prototype.

Usage:
    python main.py                                  # use built-in sample puzzles
    python main.py --puzzles lichess_db_puzzle.csv   # load from Lichess CSV
    python main.py --puzzles puzzles.csv --min-rating 1000 --max-rating 1500
"""

import argparse
import os
import sys

import chess

# Ensure Unicode output works on Windows
if sys.platform == "win32":
    os.environ.setdefault("PYTHONIOENCODING", "utf-8")
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

from puzzle_loader import SAMPLE_PUZZLES, Puzzle, load_puzzles, pick_random
from tutor import ChessTutor


def choose_difficulty(puzzles: list[Puzzle]) -> list[Puzzle]:
    """Let the user pick a difficulty level from the available puzzles."""
    if not puzzles:
        return puzzles

    min_r = puzzles[0].rating
    max_r = puzzles[-1].rating

    print("=" * 50)
    print("  CHOOSE YOUR DIFFICULTY")
    print("=" * 50)
    print(f"\n  Available ratings: {min_r} – {max_r}")
    print()

    # Build tiers from the actual rating range
    spread = max_r - min_r
    if spread < 100:
        # All puzzles are close in rating, skip selection
        print(f"  All {len(puzzles)} puzzles are around rating {min_r}.")
        print()
        return puzzles

    tier_size = spread / 3
    tiers = [
        ("Beginner", min_r, int(min_r + tier_size)),
        ("Intermediate", int(min_r + tier_size), int(min_r + 2 * tier_size)),
        ("Advanced", int(min_r + 2 * tier_size), max_r + 1),
    ]

    for i, (name, lo, hi) in enumerate(tiers, 1):
        count = sum(1 for p in puzzles if lo <= p.rating < hi)
        print(f"  {i}. {name:15s} (rating {lo}–{hi - 1}, {count} puzzles)")

    print(f"  4. {'All':15s} (rating {min_r}–{max_r}, {len(puzzles)} puzzles)")
    print(f"  5. Custom range")
    print()

    while True:
        try:
            choice = input("Pick a difficulty [1-5]: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            sys.exit(0)

        if choice == "1":
            lo, hi = tiers[0][1], tiers[0][2]
        elif choice == "2":
            lo, hi = tiers[1][1], tiers[1][2]
        elif choice == "3":
            lo, hi = tiers[2][1], tiers[2][2]
        elif choice == "4":
            print(f"\n  Using all {len(puzzles)} puzzles.\n")
            return puzzles
        elif choice == "5":
            try:
                lo = int(input(f"  Min rating [{min_r}]: ").strip() or str(min_r))
                hi = int(input(f"  Max rating [{max_r}]: ").strip() or str(max_r)) + 1
            except (ValueError, EOFError, KeyboardInterrupt):
                print("Invalid input, try again.")
                continue
        else:
            print("Please enter 1-5.")
            continue

        filtered = [p for p in puzzles if lo <= p.rating < hi]
        if not filtered:
            print(f"  No puzzles in that range. Try again.")
            continue

        print(f"\n  Selected {len(filtered)} puzzles (rating {filtered[0].rating}–{filtered[-1].rating}).\n")
        return filtered


def display_board(board: chess.Board):
    """Print the board with unicode pieces and border."""
    print()
    print(board.unicode(borders=True))
    print()


def apply_setup_move(board: chess.Board, puzzle: Puzzle) -> chess.Board:
    """Apply the opponent's last move that sets up the puzzle."""
    move = chess.Move.from_uci(puzzle.opponent_move)
    board.push(move)
    return board


def run_puzzle(puzzle: Puzzle, tutor: ChessTutor):
    """Run a single puzzle interaction loop."""
    board = chess.Board(puzzle.fen)

    print("=" * 50)
    print(f"  Puzzle {puzzle.puzzle_id}  |  Rating: {puzzle.rating}")
    if puzzle.themes:
        print(f"  Themes: {', '.join(puzzle.themes)}")
    print("=" * 50)

    # Apply the opponent's setup move
    print(f"\nOpponent plays: {puzzle.opponent_move}")
    apply_setup_move(board, puzzle)
    display_board(board)

    turn = "White" if board.turn == chess.WHITE else "Black"
    print(f"Your turn as {turn}. Find the best move!")
    print("(Type moves in natural language, ask for a 'hint', or 'skip')\n")

    solution = puzzle.solution_moves
    move_history: list[str] = []
    tutor.reset_hints()

    while len(move_history) < len(solution):
        try:
            user_input = input("You> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            sys.exit(0)

        if not user_input:
            continue

        # Handle built-in commands
        cmd = user_input.lower()
        if cmd in ("quit", "exit", "q"):
            print("Goodbye!")
            sys.exit(0)
        if cmd in ("skip", "next"):
            print("Skipping puzzle...\n")
            return
        if cmd == "show solution":
            print(f"Solution: {' '.join(solution)}")
            print("Moving on...\n")
            return
        if cmd == "board":
            display_board(board)
            continue

        # Send to the AI tutor
        result = tutor.interpret(user_input, board, solution, move_history)

        move_uci = result.get("move_uci")
        message = result.get("message", "")

        print(f"\nTutor: {message}\n")

        # If the tutor identified a move attempt, check it
        if move_uci:
            expected = solution[len(move_history)]
            if move_uci == expected:
                # Correct move — apply it
                board.push(chess.Move.from_uci(move_uci))
                move_history.append(move_uci)
                display_board(board)

                # Check if there's an opponent reply in the solution
                if len(move_history) < len(solution):
                    opponent_reply = solution[len(move_history)]
                    print(f"Opponent responds: {opponent_reply}")
                    board.push(chess.Move.from_uci(opponent_reply))
                    move_history.append(opponent_reply)
                    display_board(board)

                    if len(move_history) < len(solution):
                        print("Good! Keep going — find the next move.\n")
            else:
                # Wrong move — the tutor's message already explains why
                pass

    # Puzzle complete
    print("*" * 50)
    print("  Puzzle complete! Well done!")
    print("*" * 50)
    print()


def main():
    parser = argparse.ArgumentParser(description="Chess Puzzle Tutor")
    parser.add_argument(
        "--puzzles", type=str, default=None,
        help="Path to Lichess puzzle CSV file",
    )
    parser.add_argument("--min-rating", type=int, default=0)
    parser.add_argument("--max-rating", type=int, default=9999)
    parser.add_argument(
        "--themes", type=str, default=None,
        help="Comma-separated puzzle themes to filter by",
    )
    args = parser.parse_args()

    # Load puzzles
    if args.puzzles:
        theme_filter = set(args.themes.split(",")) if args.themes else None
        puzzles = load_puzzles(
            args.puzzles,
            min_rating=args.min_rating,
            max_rating=args.max_rating,
            themes=theme_filter,
        )
        if not puzzles:
            print("No puzzles matched your filters. Try adjusting --min-rating/--max-rating.")
            sys.exit(1)
        print(f"Loaded {len(puzzles)} puzzles (rating {args.min_rating}-{args.max_rating})")
    else:
        puzzles = SAMPLE_PUZZLES
        print(f"Using {len(puzzles)} built-in sample puzzles")
        print("(Pass --puzzles <path> to load from Lichess CSV)\n")

    # Sort puzzles by rating so difficulty selection works
    puzzles.sort(key=lambda p: p.rating)

    # Let the user pick a difficulty level
    puzzles = choose_difficulty(puzzles)

    # Initialize tutor
    tutor = ChessTutor()

    print("=" * 50)
    print("  CHESS PUZZLE TUTOR")
    print("  Describe your moves in natural language!")
    print("  Commands: hint, skip, board, show solution, quit")
    print("=" * 50)
    print()

    # Main loop
    while True:
        puzzle = pick_random(puzzles)
        run_puzzle(puzzle, tutor)

        try:
            again = input("Press Enter for the next puzzle (or 'quit' to exit): ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break
        if again.lower() in ("quit", "exit", "q"):
            print("Goodbye!")
            break
        print()


if __name__ == "__main__":
    main()

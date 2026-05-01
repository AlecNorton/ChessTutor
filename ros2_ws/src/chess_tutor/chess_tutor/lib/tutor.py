"""Chess tutor powered by Claude (Sonnet 4.6) via the Anthropic API.

Interprets natural language about chess moves and provides Socratic tutoring
in the context of a specific puzzle position.
"""

import json
import os

import anthropic
import chess

MODEL = "claude-sonnet-4-6"

SYSTEM_PROMPT = """\
You are a friendly, encouraging chess tutor helping a student solve a chess puzzle.

## Your personality
- Patient, warm, and Socratic — guide the student toward the answer rather than \
giving it away immediately.
- Celebrate correct moves enthusiastically.
- When the student makes a mistake, gently explain why it doesn't work and nudge \
them in the right direction without revealing the answer.

## Current puzzle context
The board position (FEN): {fen}

Board diagram:
{board_ascii}

It is **{turn}** to move.

The full solution (UCI notation): {solution}
Moves played so far: {history}
Next expected move (UCI): {next_move}

## How to respond

You MUST reply with valid JSON in this exact format:
{{
  "move_uci": <string or null>,
  "message": <string>
}}

### Rules for the "move_uci" field:
- If the student is clearly attempting a specific move (e.g., "knight to f3", \
"take the pawn on e5", "Nf3", "e2e4"), interpret it in the context of the \
current board and return the move in UCI format (e.g., "g1f3").
- For pawn promotions append the piece letter (e.g., "e7e8q").
- If the student is asking a question, requesting a hint, or chatting — set \
move_uci to null.

### Rules for the "message" field:
- If move_uci matches the next expected move: congratulate them and briefly \
explain why it's strong.
- If move_uci is a legal move but NOT the puzzle solution: explain why that \
move isn't the best choice here. Give a small hint toward the correct move \
without revealing it.
- If move_uci is an illegal move: let them know it's not legal and describe \
what pieces can actually move.
- If the student asks for a hint: give a progressive hint. Start vague \
("look at the knight's potential"), get more specific if they ask again.
- If the student asks to see the solution or gives up: reveal the next move \
and explain the idea.
- Keep messages concise — 1-3 sentences usually.

Respond ONLY with the JSON object, no markdown fences or extra text.\
"""


class ChessTutor:
    """Wraps the Anthropic API to provide puzzle-aware chess tutoring."""

    def __init__(self, api_key: str | None = None):
        self.client = anthropic.Anthropic(
            api_key=api_key or os.environ.get("ANTHROPIC_API_KEY"),
        )
        self.hint_count = 0  # track progressive hints per puzzle

    def reset_hints(self):
        self.hint_count = 0

    def interpret(
        self,
        user_input: str,
        board: chess.Board,
        solution_moves: list[str],
        move_history: list[str],
    ) -> dict:
        """Send the user's natural language input to Claude for interpretation.

        Returns a dict with:
          - move_uci: str | None  — the UCI move if the user attempted one
          - message: str — the tutor's response
        """
        next_move_index = len(move_history)
        next_move = (
            solution_moves[next_move_index]
            if next_move_index < len(solution_moves)
            else "puzzle complete"
        )

        system = SYSTEM_PROMPT.format(
            fen=board.fen(),
            board_ascii=str(board),
            turn="White" if board.turn == chess.WHITE else "Black",
            solution=" ".join(solution_moves),
            history=" ".join(move_history) if move_history else "(none yet)",
            next_move=next_move,
        )

        # Add hint context so progressive hints work
        hint_note = ""
        if "hint" in user_input.lower():
            self.hint_count += 1
            hint_note = (
                f"\n\n[System: This is hint request #{self.hint_count}. "
                f"Be progressively more specific with each hint.]"
            )

        response = self.client.messages.create(
            model=MODEL,
            max_tokens=300,
            system=system + hint_note,
            messages=[{"role": "user", "content": user_input}],
        )

        text = response.content[0].text.strip()

        # Parse the JSON response
        try:
            # Handle potential markdown code fences
            if text.startswith("```"):
                text = text.split("\n", 1)[1].rsplit("```", 1)[0].strip()
            result = json.loads(text)
        except json.JSONDecodeError:
            result = {"move_uci": None, "message": text}

        return result

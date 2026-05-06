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
{mood_section}{confidence_section}
## How to respond

You MUST reply with valid JSON in this exact format:
{{
  "move_uci": <string or null>,
  "message": <string>,
  "perceived_confidence": <float between 0.0 and 1.0>
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

### Rules for the "perceived_confidence" field:
- Estimate how confident the student sounds based ONLY on the words of their \
input (you do not have audio prosody). Output a single float in [0.0, 1.0]:
  - ~0.0-0.3: hesitant, confused, asking for hints, "I don't know", lots of \
hedging ("maybe", "I think", "umm"), wrong moves stated tentatively.
  - ~0.4-0.6: neutral — clear statement of a move with no strong signal \
either way, or a casual question.
  - ~0.7-1.0: assertive — confident move declaration, explains reasoning, \
states a plan ("I'll take with the knight then fork the queen").
- This value drives adaptive puzzle difficulty downstream, so be calibrated, \
not encouraging. A wrong-but-confident move is still high confidence.

Respond ONLY with the JSON object, no markdown fences or extra text.\
"""


def _format_confidence_section(confidence: float | None) -> str:
    """Build the confidence-aware coaching block injected into the system prompt.

    `confidence` is a fused user-confidence score in [0, 1] from the
    user_confidence aggregator (face + LLM-perceived, etc.). High = the
    student is doing well and doesn't need much help; low = they're
    struggling and need more support.
    """
    if confidence is None:
        return ""

    if confidence >= 0.7:
        guidance = (
            "The student is highly confident and doing well. Be terse and "
            "direct — drop the warm preamble and the Socratic questions, "
            "and skip hand-holding. Give one-sentence responses where you "
            "can. Do not volunteer hints they didn't ask for. If they make "
            "a correct move, a quick acknowledgement is enough; save the "
            "detailed praise. If they ask a question, answer it directly "
            "rather than turning it back into a question. Trust them to "
            "work things out."
        )
    elif confidence <= 0.4:
        guidance = (
            "The student appears uncertain. Lean warmer and more "
            "supportive, and offer hints a little earlier than usual."
        )
    else:
        guidance = "Maintain your usual friendly Socratic style."

    return (
        f"\n## Student's confidence level\n"
        f"Current confidence score: {confidence:.2f} "
        f"(range 0 to 1; higher = more confident).\n"
        f"{guidance}\n"
    )


def _format_mood_section(mood: float | None) -> str:
    """Build the mood guidance block injected into the system prompt.

    `mood` is an aggregated valence score in roughly [-1, 1]:
        positive  -> happy/engaged
        zero/none -> unknown or neutral
        negative  -> frustrated/anxious
    """
    if mood is None:
        return ""

    if mood < -0.2:
        guidance = (
            "The student appears frustrated or unhappy. Be extra warm and "
            "encouraging, offer a hint sooner if they hesitate, and don't "
            "dwell on mistakes."
        )
    elif mood > 0.5:
        guidance = (
            "The student appears engaged and happy. Feel free to challenge "
            "them a bit more and ask them to articulate their reasoning."
        )
    else:
        guidance = "Maintain your usual friendly Socratic style."

    return (
        f"\n## Student's emotional state\n"
        f"Current mood score: {mood:.2f} "
        f"(range -1 to 1; positive = happy, negative = frustrated).\n"
        f"{guidance}\n"
    )


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
        mood: float | None = None,
        user_confidence: float | None = None,
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
            mood_section=_format_mood_section(mood),
            confidence_section=_format_confidence_section(user_confidence),
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
            result = {"move_uci": None, "message": text, "perceived_confidence": None}

        # Normalize perceived_confidence: clamp to [0,1], or None if missing/bad.
        raw_conf = result.get("perceived_confidence")
        if isinstance(raw_conf, (int, float)):
            result["perceived_confidence"] = max(0.0, min(1.0, float(raw_conf)))
        else:
            result["perceived_confidence"] = None

        return result

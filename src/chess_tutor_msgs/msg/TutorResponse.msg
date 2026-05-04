# Response from the AI chess tutor after interpreting user input.

# UCI move the tutor identified from the user's speech (empty if no move).
string move_uci

# Natural language response to speak/display to the user.
string message

# Set true if move_uci matches the next expected solution move.
# Only meaningful when move_uci is non-empty.
bool is_correct

# Echo of the original transcribed user input (for logging/debugging).
string user_input

# LLM-perceived confidence from the user's speech, in [0.0, 1.0].
# 0.0 = very unsure / hesitant, 1.0 = decisive and confident.
# A negative value (e.g. -1.0) indicates "no judgement available" — consumers
# should treat that as missing rather than as low confidence.
float32 perceived_confidence

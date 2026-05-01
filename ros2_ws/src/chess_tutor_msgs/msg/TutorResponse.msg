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

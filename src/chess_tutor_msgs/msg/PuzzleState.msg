# Current state of the active chess puzzle.

string puzzle_id
int32 rating
string[] themes

# Current board position in FEN notation.
string fen

# Full puzzle solution as a list of UCI moves (the moves the player must find).
string[] solution_moves

# UCI moves played so far in this puzzle (alternating player and opponent).
string[] move_history

# Index into solution_moves of the next move the player must find.
int32 next_move_index

# True when the puzzle is fully solved.
bool is_complete

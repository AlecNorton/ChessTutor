"""Weight table for user_confidence aggregation.
A simple Python dict mapping node names to float weights."""

DEFAULT_WEIGHTS = {
    'face': 0.75,  # weight for facial expression recognition
    # 'gaze': 0.0, # probably wont do this
    'voice': .25, # TODO: tune based on accuracy
    # 'game': 0.0 # TODO: tune for game/position difficulty
}

NORMALIZE = True

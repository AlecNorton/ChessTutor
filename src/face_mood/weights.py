"""Weight table for face_mood aggregation.
A simple Python dict mapping node names to float weights."""

DEFAULT_WEIGHTS = {
    'dummy_node': 1.0,  # weight for the dummy node
    # 'camera_node': 0.8,  # example future entry
}

NORMALIZE = True

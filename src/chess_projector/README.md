# Chess Projector ROS2 Package

Projects chess piece movement hints onto a physical chess board via a projector.

## Usage

### Run the node directly:
```bash
ros2 run chess_projector projector_node
```

### Run with launch file:
```bash
ros2 launch chess_projector projector.launch.py
```

### With parameters:
```bash
ros2 launch chess_projector projector.launch.py fullscreen:=true
ros2 launch chess_projector projector.launch.py calibration_file:=/path/to/calibration.json
```

## ROS2 Topics

### Subscribed Topics

| Topic | Type | Description |
|-------|------|-------------|
| `/chess/square` | `std_msgs/String` | Square to highlight (e.g., "e4", "a1") |
| `/chess/piece` | `std_msgs/String` | Piece type for move calculation |
| `/chess/clear` | `std_msgs/Empty` | Clear all highlights |

### Valid Piece Types

- `king`
- `queen`
- `rook`
- `bishop`
- `knight`
- `pawn` or `pawn_white` (moves up the board)
- `pawn_black` (moves down the board)

## Example Commands

```bash
# Select square e4
ros2 topic pub --once /chess/square std_msgs/String "data: 'e4'"

# Set piece to queen
ros2 topic pub --once /chess/piece std_msgs/String "data: 'queen'"

# Clear highlights
ros2 topic pub --once /chess/clear std_msgs/Empty "{}"
```

## Calibration

1. Start the node - it opens in calibration mode
2. Align the 4 corners (a8, h8, h1, a1) with your physical board
3. Use arrow keys to move corners (Shift for faster)
4. Press ENTER to save and enter play mode
5. Calibration saves to `~/.chess_projector_calibration.json` by default

## Keyboard Controls

### Calibration Mode
- **1-4**: Select corner
- **Arrow keys**: Move corner (Shift for faster)
- **ENTER**: Save and enter play mode
- **R**: Reset corners
- **ESC**: Quit

### Play Mode
- **Click**: Manual square selection
- **C**: Clear highlights
- **F**: Toggle fullscreen
- **ESC**: Return to calibration
- **Q**: Quit

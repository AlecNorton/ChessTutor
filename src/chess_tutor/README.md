# chess_tutor — ROS2 Voice-Controlled Chess Puzzle Tutor

A ROS2 (Humble) package that turns a microphone + speaker + (optionally) a robot
into an interactive chess puzzle coach. Uses:

- **openWakeWord** — always-on wakeword detection
- **faster-whisper** (`base.en`) — local speech-to-text
- **Anthropic Claude Sonnet 4.6** — natural language understanding + tutoring
- **Piper** — local neural TTS

## Node graph

```
microphone ─▶ voice_node ──/user_speech──▶ tutor_node ──/tutor_response──▶ tts_node ─▶ speaker
                                              ▲                                │
                                              │                                ▼
                                       /current_puzzle              (also subscribes
                                              │                      from puzzle_node)
                                              │
                                       puzzle_node ◀────────────────/tutor_response
                                              │
                                              └──/tts_request──▶ tts_node
```

## Setup (Ubuntu 22.04 + ROS2 Humble)

### 1. System packages

```bash
sudo apt install ros-humble-desktop python3-colcon-common-extensions \
    portaudio19-dev libsndfile1
```

### 2. Python deps

```bash
pip install anthropic python-chess openwakeword faster-whisper \
    sounddevice numpy piper-tts
```

For GPU Whisper (much faster transcription):
```bash
pip install ctranslate2  # uses CUDA if available
```

### 3. Download Piper voice

```bash
mkdir -p ~/.local/share/piper/voices && cd ~/.local/share/piper/voices
wget https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/lessac/medium/en_US-lessac-medium.onnx
wget https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/lessac/medium/en_US-lessac-medium.onnx.json
```

Then update [`config/params.yaml`](config/params.yaml) with your home path.

### 4. Set API key

```bash
export ANTHROPIC_API_KEY=sk-ant-...
```

### 5. Build the workspace

```bash
cd ~/your_ros2_ws  # the parent of src/
colcon build --packages-select chess_tutor_msgs chess_tutor
source install/setup.bash
```

### 6. Run

```bash
ros2 launch chess_tutor chess_tutor.launch.py
```

You should hear: *"New puzzle, rating 1200. You are playing White. Find the best move."*

Then say *"Hey Jarvis"* (or whichever wakeword you configured) and after the recording window
say something like *"move my knight to f3"* or *"what should I do here?"*.

## Configuration

All four nodes share `config/params.yaml`. Common tweaks:

| Param | Node | Purpose |
|-------|------|---------|
| `wakeword_model` | voice_node | Built-in (`hey_jarvis`, `alexa`, `hey_mycroft`) or path to a custom `.onnx` |
| `wakeword_threshold` | voice_node | 0.0–1.0; lower = more sensitive |
| `recording_seconds` | voice_node | How long to record after wake |
| `whisper_model` | voice_node | `tiny.en` (fastest) → `small.en` (more accurate) |
| `whisper_device` | voice_node | `cpu` or `cuda` |
| `min_rating` / `max_rating` | puzzle_node | Filter puzzle difficulty |
| `puzzles_csv` | puzzle_node | Override the bundled puzzles.csv |
| `piper_model_path` | tts_node | Path to your downloaded `.onnx` voice |

## Custom wakeword

To train *"Hey Chess"*: follow the [openWakeWord training guide](https://github.com/dscripka/openWakeWord/blob/main/docs/custom_models.md)
and set `wakeword_model` to the resulting `.onnx` path.

## Debugging

```bash
# Verify topics are flowing
ros2 topic echo /user_speech
ros2 topic echo /tutor_response
ros2 topic echo /current_puzzle

# Manually trigger a "user said this" without speaking (skip voice_node)
ros2 topic pub --once /user_speech std_msgs/String "data: 'move my knight to f3'"

# Manually speak something
ros2 topic pub --once /tts_request std_msgs/String "data: 'Hello world'"

# List audio devices (run in Python)
python3 -c "import sounddevice; print(sounddevice.query_devices())"
```

## Replacing the terminal prototype

The standalone files in the project root (`main.py`, `tutor.py`, `puzzle_loader.py`)
are the original terminal prototype. The ROS2 package re-uses the same
`tutor.py` and `puzzle_loader.py` (copied into `chess_tutor/lib/`) — so
improvements to the AI prompt or puzzle logic should be made in **both**
locations until you're ready to delete the prototype.

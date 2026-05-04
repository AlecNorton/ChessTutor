"""Standalone Piper TTS test (no ROS).

Synthesizes the given text with Piper and plays it on the default speaker.

Usage:
    python scripts/test_tts.py
    python scripts/test_tts.py "Find the best move."
    python scripts/test_tts.py --model path/to/voice.onnx "Hello."
"""

import argparse
import os
import sys

import numpy as np
import sounddevice as sd
from piper.voice import PiperVoice


DEFAULT_MODEL = os.path.normpath(
    os.path.join(
        os.path.dirname(__file__),
        "..",
        "piper_voices",
        "en_US-lessac-medium.onnx",
    )
)
DEFAULT_TEXT = (
    "Hello. I am the chess tutor. New puzzle, rating 1200. "
    "You are playing white. Find the best move."
)


def main():
    parser = argparse.ArgumentParser(description="Piper TTS local test")
    parser.add_argument("text", nargs="?", default=DEFAULT_TEXT)
    parser.add_argument(
        "--model",
        default=DEFAULT_MODEL,
        help="Path to Piper .onnx voice (default: piper_voices/en_US-lessac-medium.onnx)",
    )
    parser.add_argument(
        "--config",
        default=None,
        help="Path to matching .json config (default: <model>.json)",
    )
    args = parser.parse_args()

    model_path = os.path.normpath(args.model)
    if not os.path.exists(model_path):
        print(f"Voice model not found: {model_path}", file=sys.stderr)
        print("Download one to piper_voices/ -- see README.", file=sys.stderr)
        sys.exit(1)

    config_path = args.config or model_path + ".json"

    print(f"Loading Piper voice: {model_path}")
    voice = PiperVoice.load(model_path, config_path=config_path)
    sr = voice.config.sample_rate

    print(f"Synthesizing ({sr} Hz): {args.text!r}")
    chunks = [
        np.frombuffer(c, dtype=np.int16)
        for c in voice.synthesize_stream_raw(args.text)
    ]
    if not chunks:
        print("No audio synthesized.", file=sys.stderr)
        sys.exit(1)

    audio = np.concatenate(chunks)
    duration = len(audio) / sr
    print(f"Playing {duration:.2f}s of audio ...")
    sd.play(audio, samplerate=sr)
    sd.wait()
    print("Done.")


if __name__ == "__main__":
    main()

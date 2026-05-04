"""Standalone wakeword + Whisper test (no ROS).

Listens until a wakeword fires, records 5s, transcribes with faster-whisper.

Usage:
    python scripts/test_voice.py                       # default: hey_chess.onnx
    python scripts/test_voice.py hey_jarvis            # built-in model
    python scripts/test_voice.py path/to/custom.onnx   # explicit path
"""

import os
import queue
import sys

import numpy as np
import sounddevice as sd

import openwakeword
from openwakeword.model import Model as OWWModel
from faster_whisper import WhisperModel


SAMPLE_RATE = 16000
CHUNK = 1280
RECORD_SECONDS = 5
THRESHOLD = 0.5

DEFAULT_WAKEWORD = "hey_chess.onnx"
WAKEWORDS_DIR = os.path.normpath(
    os.path.join(os.path.dirname(__file__), "..", "src", "chess_tutor", "wakewords")
)


def resolve_wakeword(name: str) -> str:
    if not name.endswith(".onnx"):
        return name
    if os.path.isabs(name):
        return name
    candidate = os.path.join(WAKEWORDS_DIR, name)
    return candidate if os.path.exists(candidate) else name


def main():
    name = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_WAKEWORD
    wakeword = resolve_wakeword(name)

    print(f"Loading openWakeWord ({wakeword!r}) ...")
    try:
        openwakeword.utils.download_models()
    except Exception:
        pass
    oww = OWWModel(wakeword_models=[wakeword], inference_framework="onnx")

    print("Loading faster-whisper (base.en, CPU int8) ...")
    whisper = WhisperModel("base.en", device="cpu", compute_type="int8")

    audio_q: queue.Queue = queue.Queue()

    def callback(indata, frames, time_info, status):
        if status:
            print(f"audio status: {status}", file=sys.stderr)
        audio_q.put(indata[:, 0].copy())

    print(f"\nListening (threshold {THRESHOLD}). Say the wake word, then talk. Ctrl+C to quit.\n")
    with sd.InputStream(
        samplerate=SAMPLE_RATE, channels=1, dtype="int16",
        blocksize=CHUNK, callback=callback,
    ):
        while True:
            chunk = audio_q.get()
            preds = oww.predict(chunk)
            triggered = next(
                ((ww, score) for ww, score in preds.items() if score > THRESHOLD),
                None,
            )
            if not triggered:
                continue

            ww, score = triggered
            print(f"WAKE: {ww} (score={score:.2f}) -- recording {RECORD_SECONDS}s ...")
            buf = [chunk]
            needed = int(RECORD_SECONDS * SAMPLE_RATE / CHUNK)
            for _ in range(needed):
                buf.append(audio_q.get())

            audio = np.concatenate(buf).astype(np.float32) / 32768.0
            print("Transcribing ...")
            segments, _ = whisper.transcribe(
                audio, language="en", beam_size=1, vad_filter=True
            )
            text = " ".join(seg.text.strip() for seg in segments).strip()
            print(f"You said: {text or '(no speech detected)'}\n")
            oww.reset()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nGoodbye.")

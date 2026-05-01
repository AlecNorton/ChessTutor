"""voice_node — always-on wakeword detection + Whisper transcription.

Owns the microphone. Continuously runs openWakeWord on incoming audio.
On detection, records the next N seconds and transcribes with faster-whisper,
then publishes the transcript on /user_speech.

Mutes detection while TTS is playing (subscribes to /tts_status) to avoid
the robot triggering itself.
"""

import queue
import threading

import numpy as np
import rclpy
from rclpy.node import Node
from std_msgs.msg import Bool, Empty, String

# Heavy imports are guarded so the node can fail with a clear message
# instead of crashing rclpy if a dep is missing.
try:
    import sounddevice as sd
    import openwakeword
    from openwakeword.model import Model as OWWModel
    from faster_whisper import WhisperModel
except ImportError as e:
    sd = None
    OWWModel = None
    WhisperModel = None
    _IMPORT_ERROR = e
else:
    _IMPORT_ERROR = None


# openWakeWord expects 16kHz mono audio in 80ms chunks (1280 samples).
SAMPLE_RATE = 16000
CHUNK_SIZE = 1280


class VoiceNode(Node):
    def __init__(self):
        super().__init__("voice_node")

        if _IMPORT_ERROR is not None:
            self.get_logger().error(
                f"Missing audio dependency: {_IMPORT_ERROR}. "
                "Install with: pip install openwakeword faster-whisper sounddevice"
            )
            raise _IMPORT_ERROR

        # ---- Parameters ----
        self.declare_parameter("wakeword_model", "alexa")  # built-in or path to .onnx
        self.declare_parameter("wakeword_threshold", 0.5)
        self.declare_parameter("recording_seconds", 10.0)
        self.declare_parameter("whisper_model", "base.en")
        self.declare_parameter("whisper_device", "cpu")  # "cpu" or "cuda"
        self.declare_parameter("whisper_compute_type", "int8")
        self.declare_parameter("audio_input_device", -1)  # -1 = default

        wakeword = self.get_parameter("wakeword_model").value
        self.threshold = self.get_parameter("wakeword_threshold").value
        self.record_seconds = self.get_parameter("recording_seconds").value
        whisper_name = self.get_parameter("whisper_model").value
        whisper_device = self.get_parameter("whisper_device").value
        whisper_compute = self.get_parameter("whisper_compute_type").value
        input_device = self.get_parameter("audio_input_device").value

        # ---- Models ----
        self.get_logger().info(f"Loading openWakeWord model: {wakeword}")
        # Pre-download default models on first run; users can supply a custom .onnx path.
        try:
            openwakeword.utils.download_models()
        except Exception:
            pass  # already downloaded, or offline
        self.oww = OWWModel(wakeword_models=[wakeword], inference_framework="onnx")

        self.get_logger().info(f"Loading faster-whisper model: {whisper_name}")
        self.whisper = WhisperModel(
            whisper_name, device=whisper_device, compute_type=whisper_compute
        )

        # ---- Pub/Sub ----
        self.wake_pub = self.create_publisher(Empty, "/wake_event", 10)
        self.speech_pub = self.create_publisher(String, "/user_speech", 10)
        self.create_subscription(Bool, "/tts_status", self._on_tts_status, 10)

        # ---- State ----
        self.tts_active = False
        # We collect audio chunks here so we can feed both wakeword detection
        # and (after wake) the recording-buffer simultaneously.
        self.audio_chunks: queue.Queue = queue.Queue()
        self.recording = False
        self.record_buffer: list[np.ndarray] = []

        # ---- Audio thread ----
        self.audio_input_device = None if input_device < 0 else input_device
        self._stop = threading.Event()
        self.audio_thread = threading.Thread(target=self._run_audio_loop, daemon=True)
        self.audio_thread.start()

        self.get_logger().info(
            f"voice_node ready. Wakeword='{wakeword}' threshold={self.threshold} "
            f"record={self.record_seconds}s"
        )

    # ----- ROS callbacks -----

    def _on_tts_status(self, msg: Bool):
        self.tts_active = msg.data
        if self.tts_active:
            self.get_logger().debug("TTS speaking — pausing wakeword detection")

    # ----- Audio pipeline -----

    def _audio_callback(self, indata, frames, time_info, status):
        """Called by sounddevice on each captured chunk (in audio thread)."""
        if status:
            self.get_logger().warn(f"Audio status: {status}")
        # Copy because the buffer is reused.
        self.audio_chunks.put(indata[:, 0].copy())

    def _run_audio_loop(self):
        """Pulls chunks from the queue, runs wakeword, manages recording state."""
        with sd.InputStream(
            samplerate=SAMPLE_RATE,
            channels=1,
            dtype="int16",
            blocksize=CHUNK_SIZE,
            device=self.audio_input_device,
            callback=self._audio_callback,
        ):
            chunks_to_record = int(self.record_seconds * SAMPLE_RATE / CHUNK_SIZE)
            chunks_collected = 0

            while not self._stop.is_set():
                try:
                    chunk = self.audio_chunks.get(timeout=0.5)
                except queue.Empty:
                    continue

                if self.recording:
                    self.record_buffer.append(chunk)
                    chunks_collected += 1
                    if chunks_collected >= chunks_to_record:
                        self._finalize_recording()
                        chunks_collected = 0
                    continue

                if self.tts_active:
                    continue  # don't react to our own voice

                # Wakeword detection
                prediction = self.oww.predict(chunk)
                for ww_name, score in prediction.items():
                    if score > self.threshold:
                        self.get_logger().info(
                            f"WAKE: '{ww_name}' (score={score:.2f}) — recording {self.record_seconds}s"
                        )
                        self.wake_pub.publish(Empty())
                        self.recording = True
                        # Include the wake chunk so the user's word isn't cut off.
                        self.record_buffer = [chunk]
                        chunks_collected = 1
                        # Reset oWW state so it doesn't re-fire mid-recording.
                        self.oww.reset()
                        break

    def _finalize_recording(self):
        """Concatenate buffer, transcribe, publish."""
        self.recording = False
        audio_int16 = np.concatenate(self.record_buffer)
        self.record_buffer = []

        # faster-whisper wants float32 in [-1, 1].
        audio_float = audio_int16.astype(np.float32) / 32768.0

        try:
            segments, _info = self.whisper.transcribe(
                audio_float,
                language="en",
                vad_filter=True,
                beam_size=1,  # fast, fine for short clips
            )
            text = " ".join(seg.text.strip() for seg in segments).strip()
        except Exception as e:
            self.get_logger().error(f"Whisper failed: {e}")
            return

        if not text:
            self.get_logger().info("No speech detected in recording")
            return

        self.get_logger().info(f"Transcribed: {text}")
        msg = String()
        msg.data = text
        self.speech_pub.publish(msg)

    def shutdown(self):
        self._stop.set()


def main():
    rclpy.init()
    node = VoiceNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.shutdown()
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()

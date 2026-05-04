"""tts_node — speaks text aloud with Piper, also handles tutor messages.

Subscribes:
  /tts_request    (std_msgs/String)         — text to speak directly
  /tutor_response (chess_tutor_msgs/TutorResponse) — speaks the .message field

Publishes:
  /tts_status (std_msgs/Bool) — true while speaking, false when idle.
                                voice_node uses this to mute wakeword detection.
"""

import os
import queue
import threading
import wave

import numpy as np
import rclpy
from rclpy.node import Node
from std_msgs.msg import Bool, String

from chess_tutor_msgs.msg import TutorResponse

try:
    import sounddevice as sd
    from piper.voice import PiperVoice
except ImportError as e:
    sd = None
    PiperVoice = None
    _IMPORT_ERROR = e
else:
    _IMPORT_ERROR = None


class TTSNode(Node):
    def __init__(self):
        super().__init__("tts_node")

        if _IMPORT_ERROR is not None:
            self.get_logger().error(
                f"Missing TTS dependency: {_IMPORT_ERROR}. "
                "Install with: pip install piper-tts sounddevice"
            )
            raise _IMPORT_ERROR

        # ---- Parameters ----
        self.declare_parameter("piper_model_path", "")  # path to .onnx voice model
        self.declare_parameter("piper_config_path", "")  # path to matching .json
        self.declare_parameter("audio_output_device", -1)

        model_path = self.get_parameter("piper_model_path").value
        config_path = self.get_parameter("piper_config_path").value
        out_device = self.get_parameter("audio_output_device").value

        if not model_path or not os.path.exists(model_path):
            raise FileNotFoundError(
                f"Piper voice model not found: '{model_path}'. "
                "Download a voice from https://github.com/rhasspy/piper/releases "
                "(e.g., en_US-lessac-medium.onnx + .onnx.json) and set piper_model_path."
            )

        self.get_logger().info(f"Loading Piper voice: {model_path}")
        self.voice = PiperVoice.load(model_path, config_path=config_path or None)
        self.sample_rate = self.voice.config.sample_rate
        self.audio_output_device = None if out_device < 0 else out_device

        # ---- Pub/Sub ----
        self.status_pub = self.create_publisher(Bool, "/tts_status", 10)
        self.create_subscription(String, "/tts_request", self._on_text, 10)
        self.create_subscription(
            TutorResponse, "/tutor_response", self._on_tutor_response, 10
        )

        # ---- Speech worker (serialized so utterances don't overlap) ----
        self.queue: queue.Queue[str] = queue.Queue()
        self._stop = threading.Event()
        self.worker = threading.Thread(target=self._worker_loop, daemon=True)
        self.worker.start()

        self.get_logger().info("tts_node ready")

    def _on_text(self, msg: String):
        if msg.data.strip():
            self.queue.put(msg.data)

    def _on_tutor_response(self, msg: TutorResponse):
        if msg.message.strip():
            self.queue.put(msg.message)

    def _worker_loop(self):
        while not self._stop.is_set():
            try:
                text = self.queue.get(timeout=0.5)
            except queue.Empty:
                continue
            self._speak(text)

    def _speak(self, text: str):
        """Synthesize with Piper and play through sounddevice."""
        self._publish_status(True)
        try:
            # Piper streams int16 PCM chunks at self.sample_rate.
            audio_chunks = []
            for chunk in self.voice.synthesize_stream_raw(text):
                audio_chunks.append(np.frombuffer(chunk, dtype=np.int16))

            if not audio_chunks:
                return
            audio = np.concatenate(audio_chunks)
            sd.play(audio, samplerate=self.sample_rate, device=self.audio_output_device)
            sd.wait()
        except Exception as e:
            self.get_logger().error(f"TTS playback failed: {e}")
        finally:
            self._publish_status(False)

    def _publish_status(self, speaking: bool):
        msg = Bool()
        msg.data = speaking
        self.status_pub.publish(msg)

    def shutdown(self):
        self._stop.set()


def main():
    rclpy.init()
    node = TTSNode()
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

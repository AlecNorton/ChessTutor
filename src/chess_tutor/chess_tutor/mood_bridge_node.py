"""mood_bridge_node — converts emotion_node's JSON output into a mood score.

The facial_expression_recognition package publishes a DeepFace emotion dict
(percentages 0-100 for each of: angry, disgust, fear, happy, sad, surprise,
neutral) on /user_state. The calculate_mood aggregator wants a single Float32
on /face_mood/source/<name>. This node bridges the two.

Subscribes:
  /user_state (std_msgs/String, JSON-encoded emotion dict)

Publishes:
  /face_mood/source/face_score (std_msgs/Float32) — valence in roughly [-1, 1]

Note: the calculate_mood aggregator only subscribes to topics whose name
appears as a key in DEFAULT_WEIGHTS in calculate_mood/weights.py. Add
'face_score' there with a non-zero weight, or override via the 'weights'
ROS parameter, for this bridge to be picked up.
"""

import json

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32, String


SOURCE_TOPIC = "/face_mood/source/face_score"


def emotions_to_valence(emotions: dict) -> float:
    """Collapse a DeepFace emotion dict into a scalar valence in [-1, 1].

    Positive = happy, negative = angry/sad/fearful. We deliberately exclude
    'surprise' and 'disgust' since they're ambiguous (surprise can be good
    or bad) and treat 'neutral' as a small positive nudge so a calm student
    doesn't read as frustrated.
    """
    happy = float(emotions.get("happy", 0.0)) / 100.0
    neutral = float(emotions.get("neutral", 0.0)) / 100.0
    angry = float(emotions.get("angry", 0.0)) / 100.0
    sad = float(emotions.get("sad", 0.0)) / 100.0
    fear = float(emotions.get("fear", 0.0)) / 100.0

    positive = happy + 0.3 * neutral
    negative = (angry + sad + fear) / 3.0
    return max(-1.0, min(1.0, positive - negative))


class MoodBridgeNode(Node):
    def __init__(self):
        super().__init__("mood_bridge_node")

        self.declare_parameter("smoothing_alpha", 0.3)
        self.alpha = float(self.get_parameter("smoothing_alpha").value)
        self.smoothed: float | None = None

        self.pub = self.create_publisher(Float32, SOURCE_TOPIC, 10)
        self.create_subscription(String, "/user_state", self._on_emotion, 10)

        self.get_logger().info(
            f"mood_bridge_node ready: /user_state -> {SOURCE_TOPIC} "
            f"(EMA alpha={self.alpha})"
        )

    def _on_emotion(self, msg: String):
        try:
            emotions = json.loads(msg.data)
        except json.JSONDecodeError as e:
            self.get_logger().warn(f"Bad JSON on /user_state: {e}")
            return
        if not isinstance(emotions, dict):
            self.get_logger().warn(f"/user_state was not a dict: {emotions!r}")
            return

        raw = emotions_to_valence(emotions)

        if self.smoothed is None:
            self.smoothed = raw
        else:
            self.smoothed = self.alpha * raw + (1.0 - self.alpha) * self.smoothed

        out = Float32()
        out.data = float(self.smoothed)
        self.pub.publish(out)
        self.get_logger().debug(f"raw={raw:.3f} smoothed={self.smoothed:.3f}")


def main():
    rclpy.init()
    node = MoodBridgeNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()

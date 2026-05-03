import json
import rclpy
from rclpy.node import Node
from std_msgs.msg import String, Float32

EMOTION_VALENCE = {
    'happy':    +0.8,
    'neutral':  +0.3,
    'surprise':  0.0,   # not very reliable with this model
    'angry':    -0.2,
    'disgust':  -0.3,
    'sad':      -0.6,
    'fear':     -0.9,
}

class FaceConfidenceNode(Node):
    def __init__(self):
        super().__init__('face_confidence_node')
        self.sub = self.create_subscription(String, 'user_state', self.on_emotion, 10)
        self.pub = self.create_publisher(Float32, '/user_confidence/source/face', 10)
        self.timer = self.create_timer(0.5, self.publish_smoothed)  # 2Hz

        self.alpha = 0.08
        self.smoothed = 0.5  # neutral start
        self.has_data = False

    # On recieving an emotion reading
    def on_emotion(self, msg):
        # {'happy': 12.3, 'sad': 4.1, ...} as percentages
        scores = json.loads(msg.data) 
        total = sum(scores.values()) or 1.0
        probs = {k: v / total for k, v in scores.items()}

        valence = sum(probs.get(e, 0) * v for e, v in EMOTION_VALENCE.items())
        confidence = (valence + 1) / 2  # map [-1,1] → [0,1]

        # Calculate exponential moving average to deal with emotion readings over time
        self.smoothed = self.alpha * confidence + (1 - self.alpha) * self.smoothed
        self.has_data = True

    def publish_smoothed(self):
        if not self.has_data:
            return
        out = Float32()
        out.data = float(self.smoothed)
        self.pub.publish(out)

def main(args=None):
    rclpy.init(args=args)
    node = FaceConfidenceNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
import sys
sys.path.insert(0, "/home/ubuntu/emotion_env/lib/python3.10/site-packages")
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import cv2
from deepface import DeepFace
import json

class EmotionNode(Node):
    def __init__(self):
        super().__init__('emotion_node')

        # Publisher
        self.emotion_pub = self.create_publisher(String, 'user_state', 10)

        # Camera Input
        self.cap = cv2.VideoCapture(0)

        # Timer
        self.timer = self.create_timer(0.1, self.process_frame)
    
    def process_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            return

        try:
            result = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)

            emotion_scores = result[0]['emotion']

            msg = String()
            msg.data = json.dumps(emotion_scores)

            self.publisher_.publish(msg)

        except Exception as e:
            self.get_logger().info(f"Error: {str(e)}")

def main(args=None):
    rclpy.init(args=args)
    node = EmotionNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
    

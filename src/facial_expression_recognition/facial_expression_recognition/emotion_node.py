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
            dominant = result[0]['dominant_emotion']
            
            # Draw the dominant emotion on the frame
            cv2.putText(frame, dominant, (20, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            
            msg = String()
            msg.data = json.dumps(emotion_scores)
            self.emotion_pub.publish(msg)
        except Exception as e:
            self.get_logger().info(f"Error: {str(e)}")
        
        # UNCOMMENT TO SEE CAMERA VIEW
        # cv2.imshow("Emotion", frame)
        # cv2.waitKey(1)

def main(args=None):
    rclpy.init(args=args)
    node = EmotionNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
    

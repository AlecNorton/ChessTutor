#!/usr/bin/env python3
"""Dummy node that publishes a constant face mood score."""
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32

class DummyNode(Node):
    def __init__(self):
        super().__init__('face_mood_dummy')
        self.pub = self.create_publisher(Float32, '/face_mood/source/dummy_node', 10)
        self.declare_parameter('rate', 1.0)
        try:
            rate = float(self.get_parameter('rate').value)
        except Exception:
            rate = 1.0
        self.timer = self.create_timer(1.0 / rate, self.timer_callback)

    def timer_callback(self):
        msg = Float32()
        msg.data = 1.0
        self.pub.publish(msg)
        self.get_logger().debug('Published dummy score 1.0')


def main(args=None):
    rclpy.init(args=args)
    node = DummyNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()

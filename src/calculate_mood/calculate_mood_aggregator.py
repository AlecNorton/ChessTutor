#!/usr/bin/env python3
"""Aggregator node: subscribes to source scores and publishes aggregated score."""
from typing import Dict
try:
    import rclpy
    from rclpy.node import Node
    from std_msgs.msg import Float32
    RCLPY_AVAILABLE = True
except Exception:
    rclpy = None
    Node = object
    class Float32:
        def __init__(self, data: float = 0.0):
            self.data = data
    RCLPY_AVAILABLE = False

try:
    from .weights import DEFAULT_WEIGHTS, NORMALIZE
except Exception:
    DEFAULT_WEIGHTS = {}
    NORMALIZE = True

class AggregatorNode(Node):
    def __init__(self):
        super().__init__('calculate_mood_aggregator')
        self.pub = self.create_publisher(Float32, '/face_mood/aggregate', 10)

        # Load weights from file but allow runtime override via ROS2 parameter
        self.declare_parameter('weights', DEFAULT_WEIGHTS)
        try:
            param_val = self.get_parameter('weights').value
        except Exception:
            param_val = DEFAULT_WEIGHTS
        if isinstance(param_val, dict) and param_val:
            self.weights = param_val
        else:
            self.weights = DEFAULT_WEIGHTS

        # Derive source topics from weights keys
        sources = [f'/face_mood/source/{name}' for name in self.weights.keys()]
        self.latest: Dict[str, float] = {}

        for topic in sources:
            node_name = topic.split('/')[-1]
            # Subscribe and on message arrival compute and publish aggregate
            self.create_subscription(Float32, topic, lambda msg, n=node_name: self.score_cb(n, msg), 10)

    def score_cb(self, node_name: str, msg: Float32):
        self.latest[node_name] = float(msg.data)
        self.get_logger().debug(f'Received {node_name}={msg.data}')

        # Compute and publish aggregate immediately when any source updates
        agg = calculate_mood_from_nodes(self.latest, self.weights, normalize=NORMALIZE)
        out = Float32()
        out.data = float(agg)
        self.pub.publish(out)
        self.get_logger().info(f'Published aggregate={agg}')


def calculate_mood_from_nodes(node_values: Dict[str, float], weights: Dict[str, float], normalize: bool = True) -> float:
    """Compute weighted aggregate.

    - node_values: mapping node_name->value
    - weights: mapping node_name->weight
    - normalize: if True divide by sum of weights for present nodes

    Returns float aggregated score (0.0 if no nodes present)
    """
    if not node_values:
        return 0.0
    total = 0.0
    weight_sum = 0.0
    for name, val in node_values.items():
        w = float(weights.get(name, 1.0))
        total += w * float(val)
        weight_sum += w
    if normalize and weight_sum > 0:
        return total / weight_sum
    return total


def main(args=None):
    rclpy.init(args=args)
    node = AggregatorNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""Aggregator node: subscribes to source scores and publishes aggregated mood."""
from typing import Dict

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32

from user_confidence.weights import DEFAULT_WEIGHTS, NORMALIZE


def calculate_mood_from_nodes(
    node_values: Dict[str, float],
    weights: Dict[str, float],
    normalize: bool = True,
    ) -> float:
    """Compute a weighted aggregate of source scores.

    - node_values: mapping of source name -> value
    - weights: mapping of source name -> weight
    - normalize: if True, divide by sum of weights of present sources
    Returns 0.0 if no sources have reported yet.
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

class AggregatorNode(Node):
    def __init__(self):
        super().__init__('calculate_mood_aggregator')

        # Publisher
        self.pub = self.create_publisher(Float32, '/user_confidence/aggregate', 10)

        # Load weights (allow runtime override via parameter)
        self.weights = DEFAULT_WEIGHTS

        # Subscribe to one topic per weighted source
        self.latest: Dict[str, float] = {}
        for name in self.weights.keys():
            topic = f'/user_confidence/source/{name}'
            self.create_subscription(
                Float32,
                topic,
                lambda msg, n=name: self.score_cb(n, msg),
                10,
            )
            self.get_logger().info(f'Subscribed to {topic}')

    def score_cb(self, source_name: str, msg: Float32):
        self.latest[source_name] = float(msg.data)
        self.get_logger().debug(f'Received {source_name}={msg.data}')

        agg = calculate_mood_from_nodes(self.latest, self.weights, normalize=NORMALIZE)
        out = Float32()
        out.data = float(agg)
        self.pub.publish(out)
        self.get_logger().info(f'Published aggregate={agg:.3f}')


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
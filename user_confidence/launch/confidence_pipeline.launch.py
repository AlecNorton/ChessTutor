"""Launch the facial emotion → confidence → aggregator pipeline."""
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    emotion_node = Node(
        package='facial_expression_recognition',
        executable='emotion_node',
        name='emotion_node',
        output='screen',
    )

    face_confidence_node = Node(
        package='facial_expression_recognition',
        executable='face_confidence_node',
        name='face_confidence_node',
        output='screen',
    )

    aggregator_node = Node(
        package='user_confidence',
        executable='aggregator_node',
        name='aggregator_node',
        output='screen',
    )

    return LaunchDescription([
        emotion_node,
        face_confidence_node,
        aggregator_node,
    ])
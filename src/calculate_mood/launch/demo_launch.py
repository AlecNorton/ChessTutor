from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(package='calculate_mood', executable='calculate_mood_dummy', name='calculate_mood_dummy'),
        Node(package='calculate_mood', executable='calculate_mood_aggregator', name='calculate_mood_aggregator'),
    ])

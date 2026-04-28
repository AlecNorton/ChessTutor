from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(package='face_mood', executable='face_mood_dummy', name='face_mood_dummy'),
        Node(package='face_mood', executable='face_mood_aggregator', name='face_mood_aggregator'),
    ])

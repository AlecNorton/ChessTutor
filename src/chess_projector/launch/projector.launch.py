"""Launch file for chess projector node."""

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        DeclareLaunchArgument(
            'calibration_file',
            default_value='',
            description='Path to calibration JSON file'
        ),
        DeclareLaunchArgument(
            'fullscreen',
            default_value='false',
            description='Start in fullscreen mode'
        ),
        DeclareLaunchArgument(
            'display_width',
            default_value='1280',
            description='Window width'
        ),
        DeclareLaunchArgument(
            'display_height',
            default_value='720',
            description='Window height'
        ),

        Node(
            package='chess_projector',
            executable='projector_node',
            name='chess_projector',
            output='screen',
            parameters=[{
                'calibration_file': LaunchConfiguration('calibration_file'),
                'fullscreen': LaunchConfiguration('fullscreen'),
                'display_width': LaunchConfiguration('display_width'),
                'display_height': LaunchConfiguration('display_height'),
            }]
        ),
    ])

"""Launch all chess-tutor nodes with shared parameters."""

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    pkg_share = get_package_share_directory("chess_tutor")
    default_config = os.path.join(pkg_share, "config", "params.yaml")

    config_arg = DeclareLaunchArgument(
        "config",
        default_value=default_config,
        description="Path to YAML config for all chess_tutor nodes",
    )
    config = LaunchConfiguration("config")

    return LaunchDescription([
        config_arg,
        Node(
            package="chess_tutor",
            executable="puzzle_node",
            name="puzzle_node",
            parameters=[config],
            output="screen",
        ),
        Node(
            package="chess_tutor",
            executable="tutor_node",
            name="tutor_node",
            parameters=[config],
            output="screen",
        ),
        Node(
            package="chess_tutor",
            executable="tts_node",
            name="tts_node",
            parameters=[config],
            output="screen",
        ),
        Node(
            package="chess_tutor",
            executable="voice_node",
            name="voice_node",
            parameters=[config],
            output="screen",
        ),
        Node(
            package="chess_tutor",
            executable="mood_bridge_node",
            name="mood_bridge_node",
            parameters=[config],
            output="screen",
        ),
        Node(
            package="chess_tutor",
            executable="board_viewer_node",
            name="board_viewer_node",
            parameters=[config],
            output="screen",
        ),
    ])

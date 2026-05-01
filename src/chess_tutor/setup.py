from glob import glob
from setuptools import find_packages, setup

package_name = "chess_tutor"

setup(
    name=package_name,
    version="0.1.0",
    packages=find_packages(exclude=["test"]),
    data_files=[
        ("share/ament_index/resource_index/packages",
            ["resource/" + package_name]),
        ("share/" + package_name, ["package.xml"]),
        ("share/" + package_name + "/launch", glob("launch/*.launch.py")),
        ("share/" + package_name + "/config", glob("config/*.yaml")),
        ("share/" + package_name + "/data", glob("data/*.csv")),
    ],
    install_requires=[
        "setuptools",
        "anthropic>=0.40.0",
        "python-chess>=1.10.0",
        "openwakeword>=0.6.0",
        "faster-whisper>=1.0.0",
        "sounddevice>=0.4.6",
        "numpy>=1.24.0",
        "piper-tts>=1.2.0",
    ],
    zip_safe=True,
    maintainer="khyat",
    maintainer_email="khyatsharmaoo7@gmail.com",
    description="Voice-controlled chess puzzle tutor robot",
    license="MIT",
    entry_points={
        "console_scripts": [
            "voice_node = chess_tutor.voice_node:main",
            "tutor_node = chess_tutor.tutor_node:main",
            "puzzle_node = chess_tutor.puzzle_node:main",
            "tts_node = chess_tutor.tts_node:main",
            "mood_bridge_node = chess_tutor.mood_bridge_node:main",
        ],
    },
)

from pathlib import Path


def is_ros_installed():
    return Path('/opt/ros/').exists()
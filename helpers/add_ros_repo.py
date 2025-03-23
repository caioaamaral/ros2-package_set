import platform
import subprocess

import lsb_release

from autoproj_py.osdep import APT_OSDep


def add_ros_repo():
    process = subprocess.run(
        ['curl', '-sSL', 'https://raw.githubusercontent.com/ros/rosdistro/master/ros.key'],
        capture_output=True,
        text=False
    )

    if process.returncode != 0:
        print('Failed to fetch ROS key')
        return

    name = 'ros2'
    key = process.stdout
    key_path = (APT_OSDep.KEYRINGS_DIR / f'{name}').as_posix()
    arch = platform.machine()
    codename = lsb_release.get_distro_information()['CODENAME']

    APT_OSDep.add_repo(name, f'deb [arch={arch} signed-by={key_path}] http://packages.ros.org/ros/ubuntu {codename} main', key=key)

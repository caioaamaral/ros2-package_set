import subprocess
from typing import TYPE_CHECKING

import yaml

from autoproj_py.osdep import APT_OSDep

from . import helper

if TYPE_CHECKING:
    from autoproj_py.autoproj import Autoproj

ros_distro = Autoproj.run(['echo', '$ROS_DISTRO']).stdout.strip()
distributions_url = f'https://raw.githubusercontent.com/ros/rosdistro/master/{ros_distro}/distribution.yaml'

Autoproj.execute_once(name='install-ros-repos', fn=helper.add_ros_repo)
this_pkg_set = Autoproj.manifest.current_package_set

if not Autoproj.config.get('ros2.distributions.sha', None):
    latest_sha = helper.get_latest_commit_from_upstream('ros', 'rosdistro', f'{ros_distro}/distribution.yaml', 'master')
    Autoproj.config.set('ros2.distributions.sha', latest_sha)
    Autoproj.info(f'Updating ros2 package set to latest {ros_distro} distribution')
    index_yaml = Autoproj.run(['curl', distributions_url]).stdout
    repos: dict[str, dict] = yaml.safe_load(index_yaml)['repositories']
    helper.update_osdep(this_pkg_set, ros_distro, repos)
    Autoproj.config.save()

else:
    local_sha = Autoproj.config.get('ros2.distributions.sha')
    latest_sha = helper.get_latest_commit_from_upstream('ros', 'rosdistro', f'{ros_distro}/distribution.yaml', 'master')

    if local_sha != latest_sha:
        Autoproj.info(f'Updating ros2 package set to latest {ros_distro} distribution')
        index_yaml = Autoproj.run(['curl', distributions_url]).stdout
        repos: dict[str, dict] = yaml.safe_load(index_yaml)['repositories']
        helper.update_osdep(this_pkg_set, ros_distro, repos)


from .autobuild.dsl import *

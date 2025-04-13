from typing import TYPE_CHECKING

import yaml

from . import helper

if TYPE_CHECKING:
    from autoproj_py.autoproj import Autoproj

ros_distro = Autoproj.config.ask('ros2.distro', 'Enter the ROS distribution to install')
if not ros_distro:
    Autoproj.error('ROS distribution not specified')
    exit(1)

distributions_url = f'https://raw.githubusercontent.com/ros/rosdistro/master/{ros_distro}/distribution.yaml'

Autoproj.execute_once(name='install-ros-repos', fn=helper.add_ros_repo)
this_pkg_set = Autoproj.manifest.current_package_set()

if not Autoproj.config.get('ros2.distributions.sha', None):
    latest_sha = helper.get_latest_commit_from_upstream('ros', 'rosdistro', f'{ros_distro}/distribution.yaml', 'master')
    Autoproj.config.set('ros2.distributions.sha', latest_sha)

    Autoproj.info(f'updating ros2 osdeps to the latest {ros_distro} distribution')
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
        Autoproj.config.set('ros2.distributions.sha', latest_sha)
        Autoproj.config.save()

from .autobuild.dsl import *

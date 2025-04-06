from autoproj_py.autobuild.registry import AutobuildCollector
from autoproj_py.autobuild import dsl

from .packages import Colcon

@dsl.extension
def colcon_package(name: str, source: str):
    pkg = dsl.common_package(Colcon, name, source)
    pkg.dependencies = ['colcon']
    return pkg

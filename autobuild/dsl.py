from autoproj_py.autobuild.registry import AutobuildCollector
from autoproj_py.autobuild import dsl

from .packages import Colcon

@dsl.extension
def colcon_package(name: str, source: str):
    pkg = Colcon(name, source)
    pkg.dependencies = ['colcon']
    AutobuildCollector.collect(pkg.name, pkg)

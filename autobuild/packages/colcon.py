import os
import shutil

from autoproj_py.autobuild.package import Package
from autoproj_py.autobuild.parsers import ament_manifest_parser


class Colcon(Package):
    def __init__(self, name: str, source: str):
        super().__init__(name, source)
        self.build_dir = self.root_dir / "build" / self.name
        self.install_dir = self.root_dir / "install" / self.name
        self.use_package_xml = True

    def build(self, registry, env=None, cwd=None, envsh=None):
        super().build(registry, env=env, cwd=cwd, envsh=envsh)
        self.make(env=env, cwd=cwd, envsh=envsh)

    def acquire(self):
        super().acquire()

    def hydrate_dependencies(self):
        package_xml_path = self.import_dir / 'package.xml'
        self.dependencies = ament_manifest_parser.get_dependencies(package_xml_path)

    def make(self, envsh, env=None, cwd=None):
        cmd = [
            '.', f'{envsh}', '&&',
            shutil.which('colcon'), 'build', '--base-paths', self.root_dir.as_posix(), '--install-base', self.install_dir.as_posix(),
            '--packages-select', self.name
        ]
        self.run(cmd, cwd=self.build_dir, env=env)

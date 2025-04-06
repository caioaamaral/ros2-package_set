import shutil

from autoproj_py.autobuild.packages.package import Package
from .mixins import UsePackageXmlMixin


class Colcon(UsePackageXmlMixin, Package):

    disable_native_logging = False

    @classmethod
    def disable_native_logging(cls):
        cls.disable_native_logging = True

    def __init__(self, name: str, source: str):
        super().__init__(name, source)

    def build(self, env, cwd):
        super().build(env=env, cwd=cwd)
        self.make(env=env, cwd=cwd)

    def acquire(self):
        super().acquire()

    def make(self, env, cwd):
        global_args = []
        if self.disable_native_logging:
            global_args.append('--log-base /dev/null')

        cmake_args = []

        cmd = f'{shutil.which("colcon")} {" ".join(global_args)} build ' \
              f'--base-paths {self.root_dir.as_posix()} ' \
              f'--install-base {self.install_dir.as_posix()} ' \
              f'--executor sequential ' \
              f'--event-handlers console_start_end+ ' \
              f'--packages-select {self.name}'

        self.run('build', cmd, cwd=cwd, env=env)

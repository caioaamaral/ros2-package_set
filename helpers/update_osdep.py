

import yaml
from autoproj_py.osdep import OSDepManifest


def update_osdep(this_pkg_set, ros_distro, repos):
    with open(this_pkg_set.import_path / 'ros2.osdep', 'w') as file:
        for name, defs in repos.items():
            if 'release' not in defs:
                continue

            if defs['release'].get('packages') is None:
                osdep_definition = {
                    name: {
                        'default': '-'.join(['ros', ros_distro, name])
                    }
                }

                manifest: OSDepManifest = OSDepManifest.from_dict(osdep_definition)
                file.write(f'{yaml.dump(manifest.to_dict())}\n')

            else:
                for pkg in defs['release']['packages']:
                    osdep_definition = {
                        pkg: {
                            'default': '-'.join(['ros', ros_distro, pkg])
                        }
                    }

                    manifest: OSDepManifest = OSDepManifest.from_dict(osdep_definition)
                    file.write(f'{yaml.dump(manifest.to_dict())}\n')

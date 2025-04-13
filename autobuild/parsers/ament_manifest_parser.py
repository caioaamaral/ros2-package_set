import xml.etree.ElementTree as ET

def get_dependencies(package_manifest_path):
    dependencies = []
    tree = ET.parse(package_manifest_path)
    root = tree.getroot()
    package_tag = root.tag
    if package_tag != 'package':
        raise ValueError(f'Invalid package.xml: Root is not <package>, but <{package_tag}>')

    for tag in ('depend', 'build_depend', 'exec_depend'):
        elements = root.findall(tag)
        if elements is not None:
            dependencies.extend([dep.text for dep in elements])

    return set(dependencies)
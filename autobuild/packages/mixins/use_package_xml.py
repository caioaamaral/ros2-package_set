from ...parsers import ament_manifest_parser


class UsePackageXmlMixin:

    def hydrate_dependencies(self):
        print('hydrating dependencies')
        package_xml_path = self.import_dir / 'package.xml'
        self.dependencies.extend(ament_manifest_parser.get_dependencies(package_xml_path))

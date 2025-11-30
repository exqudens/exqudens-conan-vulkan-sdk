import json
from pathlib import Path

required_conan_version = ">=2.0"

from conan import ConanFile
from conan.tools.files import copy

class ConanConfiguration(ConanFile):

    def set_name(self):
        try:
            self.name = json.loads(Path(__file__).parent.joinpath('name-version.json').read_bytes().decode())['name']
        except Exception as e:
            self.output.error(e)
            raise e

    def set_version(self):
        try:
            self.version = json.loads(Path(__file__).parent.joinpath('name-version.json').read_bytes().decode())['version']
        except Exception as e:
            self.output.error(e)
            raise e

    def package(self):
        try:
            build_folder_path: Path = Path(self.build_folder)
            package_folder_path: Path = Path(self.package_folder)

            copy(self, pattern="*.*", src=build_folder_path.as_posix(), dst=package_folder_path.as_posix())
        except Exception as e:
            self.output.error(e)
            raise e

    def package_info(self):
        try:
            self.cpp_info.set_property("cmake_file_name", self.name)
            self.cpp_info.libs = []
        except Exception as e:
            self.output.error(e)
            raise e

    def package_id(self):
        try:
            self.info.clear()
        except Exception as e:
            self.output.error(e)
            raise e

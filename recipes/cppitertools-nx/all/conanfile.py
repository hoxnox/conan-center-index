import os, conan
from conan import ConanFile, tools

required_conan_version = ">=1.32.0"

class CppItertoolsConan(ConanFile):
    name = "cppitertools-nx"
    url = "https://github.com/hoxnox/conan-center-index"
    homepage = "https://github.com/hoxnox/cppitertools"
    description = "Implementation of python itertools and builtin iteration functions for C++17. With some home brew iterators"
    topics = ("cpp17", "iter", "itertools")
    license = "BSD-2-Clause"
    package_type = "header-library"
    no_copy_source = True

    settings = "os", "arch", "compiler", "build_type"

    def source(self):
        tools.files.get(self, **self.conan_data["sources"][self.version], strip_root=True)

    def package(self):
        tools.files.copy(self, "*.hpp", 
                         src=self.source_folder,
                         dst=os.path.join(self.package_folder, "include", "cppitertools"),
                         excludes=('examples/**', 'test/**'))
        tools.files.copy(self, "LICENSE.md", src=self.source_folder, dst=os.path.join(self.package_folder, "licenses"))

    def package_info(self):
        self.cpp_info.names["cmake_find_package"] = "cppitertools"
        self.cpp_info.names["cmake_find_package_multi"] = "cppitertools"

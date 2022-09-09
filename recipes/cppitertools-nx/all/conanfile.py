import os
from conans import ConanFile, tools

required_conan_version = ">=1.32.0"


class CppItertoolsConan(ConanFile):
    name = "cppitertools-nx"
    url = "https://github.com/hoxnox/conan-center-index"
    homepage = "https://github.com/hoxnox/cppitertools"
    description = "Implementation of python itertools and builtin iteration functions for C++17. With some home brew iterators"
    topics = ("cpp17", "iter", "itertools")
    license = "BSD-2-Clause"
    no_copy_source = True

    settings = "os", "arch", "compiler", "build_type"

    @property
    def _source_subfolder(self):
        return "source_subfolder"

    def source(self):
        tools.get(**self.conan_data["sources"][self.version])
        extracted_dir = "cppitertools-" + self.version + ".0-nx"
        os.rename(extracted_dir, self._source_subfolder)

    def package(self):
        self.copy("*.hpp", dst=os.path.join("include", "cppitertools"), src=self._source_subfolder, excludes=('examples/**', 'test/**'))
        self.copy("LICENSE.md", dst="licenses", src=self._source_subfolder)

    def package_info(self):
        self.cpp_info.names["cmake_find_package"] = "cppitertools"
        self.cpp_info.names["cmake_find_package_multi"] = "cppitertools"

    def package_id(self):
        self.info.header_only()

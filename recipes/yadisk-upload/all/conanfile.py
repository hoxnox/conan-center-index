import os, shutil
from conans import ConanFile, tools, CMake

required_conan_version = ">=1.32.0"


class YadiskUpload(ConanFile):
    name = "yadisk-upload"
    url = "https://github.com/hoxnox/conan-center-index"
    homepage = "https://github.com/hoxnox/yadisk-upload"
    description = "Yandex disk file uploader."
    topics = ("yandex-disk", "files")
    options = {"tools":[True, False], "libressl":[True, False], "log":"ANY"}
    default_options = "tools=True", "libressl=True", "log="
    requires = "boost/1.75.0", "zlib/1.2.12"
    license = "BSD-3-Clause"
    no_copy_source = True
    _cmake = None
    generators = "cmake"

    settings = "os", "arch", "compiler", "build_type"

    def requirements(self):
        if self.options.libressl:
            self.requires("libressl/2.5.3")
        else:
            self.requires("openssl/1.1.1g")

        if self.options.tools:
            self.requires("docopt.cpp/0.6.2")

        if len(str(self.options.log)) == 0 or self.options.tools:
            self.requires("easyloggingpp/9.89@hoxnox/stable")

    @property
    def _source_subfolder(self):
        return "source_subfolder"

    def source(self):
        tools.get(**self.conan_data["sources"][self.version])
        extracted_dir = self.name + "-" + self.version
        os.rename(extracted_dir, self._source_subfolder)

    def _configure_cmake(self):
        if self._cmake:
            return self._cmake

        self.cmake_ = CMake(self)
        cmake_defs = {"WITH_TESTS": "0",
                      "WITH_LIBS": "1",
                      "WITH_TOOLS": "1" if self.options.tools else "0"}
        if len(str(self.options.log)) != 0:
            cmake_defs.update({"WITH_LOG": self.options.log})
        self.cmake_.configure(source_folder = self._source_subfolder, defs=cmake_defs)
        return self.cmake_

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        cmake = self._configure_cmake()
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = ["yandex_api"]


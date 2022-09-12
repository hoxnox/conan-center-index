from conans import ConanFile, CMake, tools
import os


class NanomsgConan(ConanFile):
    name = "nanomsg"
    version = "1.2"
    description = "Socket library that provides several common communication patterns. It aims to make the networking layer fast, scalable, and easy to use. Implemented in C, it works on a wide range of operating systems with no further dependencies."
    topics = ("conan", "nanomsg", "communication", "messaging", "protocols")
    url = "https://github.com/hoxnox/conan-center-index"
    homepage = "https://nanomsg.org/"
    license = "MIT"
    exports_sources = ["CMakeLists.txt"]
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"
    short_paths = True
    options = {
        "shared": [True, False],
        "fPIC": [True, False],
        "enable_doc": [True, False],
        "enable_getaddrinfo_a": [True, False],
        "enable_tests": [True, False],
        "enable_tools": [True, False],
        "enable_nanocat": [True, False],
    }
    default_options = {
        'shared': False,
        'fPIC': True,
        'enable_doc': False,
        'enable_getaddrinfo_a': True,
        'enable_tests': False,
        'enable_tools': False,
        'enable_nanocat': False
    }
    _cmake = None

    @property
    def _source_subfolder(self):
        return "source_subfolder"

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def configure(self):
        del self.settings.compiler.libcxx
        del self.settings.compiler.cppstd

    def source(self):
        tools.get(**self.conan_data["sources"][self.version])
        extracted_dir = self.name + "-" + self.version
        os.rename(extracted_dir, self._source_subfolder)

    def _configure_cmake(self):
        if self._cmake:
            return self._cmake

        self.cmake_ = CMake(self)
        self.cmake_.definitions["NN_STATIC_LIB"] = not self.options.shared
        self.cmake_.definitions["NN_ENABLE_DOC"] = self.options.enable_doc
        self.cmake_.definitions["NN_ENABLE_GETADDRINFO_A"] = self.options.enable_getaddrinfo_a
        self.cmake_.definitions["NN_TESTS"] = self.options.enable_tests
        self.cmake_.definitions["NN_TOOLS"] = self.options.enable_tools
        self.cmake_.definitions["NN_ENABLE_NANOCAT"] = self.options.enable_nanocat
        self.cmake_.configure(source_folder = self._source_subfolder)
        return self.cmake_

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        cmake = self._configure_cmake()
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)

        if not self.options.shared:
            self.cpp_info.defines.append("NN_STATIC_LIB=ON")

        if self.settings.os == "Windows" and not self.options.shared:
            self.cpp_info.libs.extend(['mswsock', 'ws2_32'])
        elif self.settings.os == "Linux":
            self.cpp_info.libs.extend(['anl', 'pthread'])

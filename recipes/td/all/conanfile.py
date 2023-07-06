from conans import ConanFile, CMake, tools
import os
import glob


class TdConan(ConanFile):
    name = "td"
    description = "TDLib (Telegram Database library) is a cross-platform library for building [Telegram](https://telegram.org) clients. It can be easily used from almost any programming language."
    topics = ("conan", "telegram", "communication", "messaging", "protocols")
    url = "https://github.com/hoxnox/conan-center-index"
    homepage = "https://core.telegram.org/tdlib"
    license = "Boost v1"
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"
    short_paths = True
    requires = "zlib/1.2.12", "openssl/1.1.1n"
    options = {
        "shared": [True, False],
        "fPIC": [True, False],
    }
    default_options = {
        'shared': False,
        'fPIC': True,
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
        extracted_dir = glob.glob(self.name + "-*/")[0]
        os.rename(extracted_dir, self._source_subfolder)

    def _configure_cmake(self):
        if self._cmake:
            return self._cmake

        self.cmake_ = CMake(self)
        self.cmake_.configure(source_folder = self._source_subfolder)
        return self.cmake_

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        cmake = self._configure_cmake()
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = ["tdapi",
                              "tdclient",
                              "tdjson",
                              "tdjson_static",
                              "tdjson_private",
                              "tdcore",
                              "tdnet",
                              "tddb",
                              "tdsqlite",
                              "tdutils",
                              "tdactor"]

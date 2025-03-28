from conan import ConanFile
from conan.errors import ConanInvalidConfiguration
from conan.tools.files import copy, get, rm, rmdir, chdir
from conan.tools.cmake import CMakeToolchain, CMake, CMakeDeps, cmake_layout
import os

required_conan_version = ">=1.53"

class LibTpm2Pkcs11(ConanFile):
    name = "tpm2-pkcs11"
    description = "A PKCS#11 interface for TPM2 hardware "
    license = "BSD"
    url = "https://github.com/conan-io/conan-center-index"
    homepage = "https://github.com/tpm2-software/tpm2-pkcs11"
    topics = ("tpm", "cryptography", "security", "pkcs11")
    exports_sources = ["CMakeLists.txt", "config.h"]
    package_type = "library"
    settings = "os", "arch", "compiler", "build_type"
    options = {
        "shared": [True, False],
        "fPIC": [True, False],
    }
    default_options = {
        "shared": False,
        "fPIC": True,
        "openssl/*:no_dso": True,
    }

    def configure(self):
        if self.options.shared:
            self.options.rm_safe("fPIC")

    def requirements(self):
        self.requires("openssl/[~3]")
        self.requires("tpm2-tss/[~4.1]")
        self.requires("sqlite3/[~3]")
        self.requires("libyaml/[~0.2]")

    def validate(self):
        if self.settings.os != "Linux":
            raise ConanInvalidConfiguration(f"{self.ref} is only available on Linux")

    def source(self):
        get(self, **self.conan_data["sources"][self.version], strip_root=True)
        copy(self, pattern="config.h", src=self.source_folder, dst=os.path.join(self.source_folder, "src/lib"))

    def generate(self):
        tc = CMakeToolchain(self)
        tc.generate()
        deps = CMakeDeps(self)
        deps.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        copy(self, pattern="LICENSE*", src=self.source_folder, dst=os.path.join(self.package_folder, "licenses"))
        cmake = CMake(self)
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = ["tpm2-pkcs11"]
        self.cpp_info.set_property("pkg_config_name", "tpm2-pkcs11")


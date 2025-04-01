from conan import ConanFile
from conan.tools.layout import basic_layout
from conan.tools.gnu import Autotools, AutotoolsToolchain, AutotoolsDeps
from conan.tools.files import copy, get
from conan.errors import ConanInvalidConfiguration
import os


class LibuuidConan(ConanFile):
    name = "libuuid"
    description = "Portable uuid C library"
    url = "https://github.com/conan-io/conan-center-index"
    homepage = "https://sourceforge.net/projects/libuuid/"
    license = "BSD-3-Clause"
    topics = ("conan", "libuuid", "uuid", "unique-id", "unique-identifier")
    package_type = "library"
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}

    def configure(self):
        del self.settings.compiler.libcxx
        del self.settings.compiler.cppstd

    def layout(self):
        basic_layout(self, src_folder="src")

    def validate(self):
        if self.settings.os != "Linux":
            raise ConanInvalidConfiguration(f"{self.ref} is only available on Linux")

    def source(self):
        get(self, **self.conan_data["sources"][self.version], strip_root=True)

    def generate(self):
        tc = AutotoolsToolchain(self)
        tc.configure_args.append("--enable-shared=%s" % ("yes" if self.options.shared else "no"))
        tc.configure_args.append("--enable-static=%s" % ("no" if self.options.shared else "yes"))
        tc.generate()

        autotoolsdeps = AutotoolsDeps(self)
        autotoolsdeps.generate()

    def build(self):
        autotools = Autotools(self)
        autotools.configure()
        autotools.make()

    def package(self):
        autotools = Autotools(self)
        autotools.install()

    def package_info(self):
        self.cpp_info.libs = ["uuid"]


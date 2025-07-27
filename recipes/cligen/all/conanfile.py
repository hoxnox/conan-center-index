import os
import shutil
from conan.errors import ConanInvalidConfiguration
from conan.tools.env import Environment
from conan.tools.files import apply_conandata_patches, export_conandata_patches, copy, get, rm, chdir
from conan.tools.gnu import Autotools, AutotoolsToolchain, AutotoolsDeps, PkgConfigDeps
from conan.tools.layout import basic_layout

from conan import ConanFile

required_conan_version = ">=1.54.0"


class CligenConan(ConanFile):
    name = "cligen"
    description = "Command-Line Interface generator"
    license = "Apache-2"
    url = "https://github.com/clicon/cligen/"
    homepage = "https://github.com/clicon/cligen/"
    topics = ("cli", "network")

    package_type = "library"
    settings = "os", "arch", "compiler", "build_type"
    options = {
        "shared": [True],
        "libxml2": [True, False],
    }
    default_options = {
        "shared": True,
        "libxml2": True,
    }

    def requirements(self):
        if self.options.libxml2:
            self.requires("libxml2/[~2]", transitive_headers=True)

    def layout(self):
        basic_layout(self, src_folder="src")

    def export_sources(self):
        export_conandata_patches(self)

    def source(self):
        get(self, **self.conan_data["sources"][self.version], strip_root=True)

    def generate(self):
        tc = AutotoolsToolchain(self)
        #tc.make_args.extend([
        #    "PREFIX={}".format(""),
        #    "DESTDIR={}".format(self.package_folder),
        #    "LIBSUBDIR={}".format("lib"),
        #])
        tc.generate()

        pkgdeps = PkgConfigDeps(self)
        pkgdeps.generate()

        autotoolsdeps = AutotoolsDeps(self)
        autotoolsdeps.generate()

    def _patch_sources(self):
        apply_conandata_patches(self)

    def build(self):
        self._patch_sources()
        env = Environment()
        env.define("CLIGEN_VERSION", str(self.version))
        with env.vars(self).apply():
            autotools = Autotools(self)
            configure_args = [f"CLIGEN_VERSION={self.version}"]
            if self.options.libxml2:
                configure_args.append("--with-libxml2")
            autotools.configure(args=configure_args)
            autotools.make()

    def package(self):
        autotools = Autotools(self)
        autotools.install()

    def package_info(self):
        self.cpp_info.libs = ["cligen"]
        self.cpp_info.bindirs = [os.path.join(self.package_folder, "bin")]

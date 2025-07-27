import os
import shutil
from conan.errors import ConanInvalidConfiguration
from conan.tools.env import Environment, VirtualBuildEnv
from conan.tools.files import apply_conandata_patches, export_conandata_patches, copy, get, rm, chdir
from conan.tools.gnu import Autotools, AutotoolsToolchain, AutotoolsDeps, PkgConfigDeps
from conan.tools.layout import basic_layout

from conan import ConanFile

required_conan_version = ">=1.54.0"


class ClixonConan(ConanFile):
    name = "clixon"
    description = "YANG-based configuration manager, with interactive CLI, NETCONF and RESTCONF interfaces, an embedded database and transaction mechanism."
    license = "Apache-2"
    url = "https://github.com/clicon/cligen/"
    homepage = "https://github.com/clicon/clixon/"
    topics = ("yang", "cli", "netconf")

    settings = "os", "arch", "compiler", "build_type"
    options = {
        "libxml2": [True, False],
    }
    default_options = {
        "libxml2": True,
    }

    def requirements(self):
        if self.options.libxml2:
            self.requires("libxml2/[~2]")
        self.requires("cligen/7.4.0", options={"libxml2": self.options.libxml2})
        self.requires("openssl/[~3]")
        self.requires("libnghttp2/[~1]")

    def export_sources(self):
        export_conandata_patches(self)

    def source(self):
        get(self, **self.conan_data["sources"][self.version], strip_root=True)

    def generate(self):
        tc = AutotoolsToolchain(self)
        tc.generate()

        env = VirtualBuildEnv(self)
        env.generate()

        pkgdeps = PkgConfigDeps(self)
        pkgdeps.generate()

        autotoolsdeps = AutotoolsDeps(self)
        autotoolsdeps.generate()

    def _patch_sources(self):
        apply_conandata_patches(self)

    def build_requirements(self):
        self.build_requires("bison/[~3]")
        #self.build_requires("flex/2.6.4")

    def build(self):
        self._patch_sources()
        env = Environment()
        env.define("CLIXON_VERSION", str(self.version))
        env.append("LD_LIBRARY_PATH", self.dependencies["cligen"].cpp_info.libdirs)
        with env.vars(self).apply():
            autotools = Autotools(self)
            configure_args = []
            #configure_args = [f"--with-cligen={self.dependencies["cligen"].package_folder}"]
            autotools.configure(args=configure_args)
            autotools.make()

    def package(self):
        autotools = Autotools(self)
        autotools.install()

    def package_info(self):
        self.cpp_info.libs = ["clixon_cli", "clixon", "clixon_backend", "clixon_restconf"]
        self.cpp_info.bindirs = [os.path.join(self.package_folder, "bin")]

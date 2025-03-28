from conan import ConanFile
from conan.errors import ConanInvalidConfiguration
from conan.tools.files import copy, get, rm, rmdir, chdir
from conan.tools.gnu import Autotools, AutotoolsToolchain, AutotoolsDeps, PkgConfigDeps
from conan.tools.layout import basic_layout
import os

required_conan_version = ">=1.53"

class LibTpm2TssConan(ConanFile):
    name = "tpm2-tss"
    description = "OSS implementation of the TCG TPM2 Software Stack (TSS2)"
    license = "LGPL-2.0"
    url = "https://github.com/conan-io/conan-center-index"
    homepage = "https://github.com/tpm2-software/tpm2-tss"
    topics = ("tpm", "cryptography", "security")

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

    def layout(self):
        basic_layout(self, src_folder="src")

    def requirements(self):
        self.requires("openssl/[~3]", transitive_headers=True)
        self.requires("json-c/[~0.18]", transitive_headers=True)
        self.requires("libuuid/[~1.0.3]", transitive_headers=True)

    def validate(self):
        if self.settings.os != "Linux":
            raise ConanInvalidConfiguration(f"{self.ref} is only available on Linux")

    def source(self):
        get(self, **self.conan_data["sources"][self.version], strip_root=True)

    def generate(self):
        tc = AutotoolsToolchain(self)
        tc.configure_args.append("--disable-fapi")
        tc.configure_args.append("--disable-tcti-cmd")
        tc.configure_args.append("--disable-tcti-libtpms")
        tc.configure_args.append("--disable-tcti-mssim")
        tc.configure_args.append("--disable-tcti-pcap")
        tc.configure_args.append("--disable-tcti-spi-lt2go")
        tc.configure_args.append("--disable-tcti-spi-ftdi")
        tc.configure_args.append("--disable-tcti-swtpm")
        tc.configure_args.append("--disable-doxygen-doc")
        tc.configure_args.append("--enable-nodl")
        tc.generate()

        pkgdeps = PkgConfigDeps(self)
        pkgdeps.generate()

        autotoolsdeps = AutotoolsDeps(self)
        autotoolsdeps.generate()

    def build(self):
        autotools = Autotools(self)
        autotools.configure()
        autotools.make()

    def package(self):
        copy(self, pattern="LICENSE*", src=self.source_folder, dst=os.path.join(self.package_folder, "licenses"))
        autotools = Autotools(self)
        autotools.install()

    def package_info(self):
        self.cpp_info.libs = [
            "tss2-tcti-device",
            "tss2-tcti-i2c-helper",
            "tss2-tctildr",
            "tss2-tcti-spidev",
            "tss2-tcti-spi-helper",
            "tss2-esys",
            "tss2-mu",
            "tss2-policy",
            "tss2-rc",
            "tss2-sys"
        ]
        self.cpp_info.set_property("pkg_config_name", "tpm2-tss")


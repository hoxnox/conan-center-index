import os
from conans import tools, ConanFile, Meson
from conans.errors import ConanInvalidConfiguration, ConanException

required_conan_version = ">=1.35.0"

class DpdkConan(ConanFile):
    name = "dpdk"
    description = "Conan installer for dpdk"
    topics = ("meson", "build", "installer")
    url = "https://github.com/hoxnox/conan-dpdk"
    homepage = "https://www.dpdk.org/"
    license = "BSD-3-Clause"
    requires = "libnuma/2.0.14", "openssl/1.1.1n", "libpcap/1.10.1"
    generators = "cmake"
    settings = "os", "arch", "compiler", "build_type"
    exports_sources = ["*.patch"]
    skip_broken_symlinks_check = True

    _source_subfolder = "source_subfolder"
    _meson = None

    def source(self):
        tools.get(**self.conan_data["sources"][self.version], strip_root=True, destination=self._source_subfolder)

    @property
    def _build_subfolder(self):
        return "build_subfolder"

    def build_requirements(self):
        self.build_requires("meson/0.61.2")
        self.build_requires("ninja/1.10.2")

    def _configure_meson(self):
        if self._meson:
            return self._meson
        self._meson = Meson(self)
        defs = {}
        defs["enable_docs"] = "false"
        defs["tests"] = "false"
        defs["default_library"] = "static"
        defs["disable_libs"]="bitratestats,cfgfile,flow_classify,gpudev,gro,gso,jobstats,kni,latencystats,memver,metrics,node,pdump,pipeline,power,table,vhost"
        defs["disable_drivers"]="disable_drivers=common/*,gpu/*,baseband/*,event/*,vpda/*,crypto/*,raw/*,dma/*"
        args=[]
        #args.append("--wrap-mode=nofallback")
        self._meson.configure(defs=defs, build_folder=self._build_subfolder, source_folder=self._source_subfolder, pkg_config_paths=[self.install_folder], args=args)
        return self._meson

    def build(self):
        for patch in self.conan_data.get("patches", {}).get(self.version, []):
            tools.patch(**patch)

        with tools.environment_append(tools.RunEnvironment(self).vars):
            meson = self._configure_meson()
            meson.build()

    def package(self):
        meson = self._configure_meson()
        meson.install()

    def package_info(self):
        libs=(
            'kvargs', # eal depends on kvargs
            'telemetry', # basic info querying
            'eal', # everything depends on eal
            'ring',
            'rcu', # rcu depends on ring
            'mempool',
            'mempool_ring',
            'mempool_bucket',
            'mempool_stack',
            'mbuf',
            'net',
            'meter',
            'ethdev',
            'pci', # core
            'cmdline',
            'hash',    # efd depends on this
            'timer',   # eventdev depends on this
            'acl',
            'bbdev',
            'compressdev',
            'cryptodev',
            'distributor',
            'efd',
            'eventdev',
            'ip_frag',
            'lpm',
            'member',
            'pcapng',
            'rawdev',
            'regexdev',
            'dmadev',
            'rib',
            'reorder',
            'sched',
            'security',
            'stack',
            'ipsec', # ipsec lib depends on net, crypto and security
            'fib', #fib lib depends on rib
            'port', # pkt framework libs which use other libs from above
            'graph',

            # drivers

            'bus_pci',
            'bus_vdev',
            'bus_vmbus',

            'net_i40e',
            'net_e1000',
            'net_ixgbe',
            'net_virtio',
        )

        # NOTE: As fo rmid 2022 there is no adequate way to link libs as a whole archive. We
        # have to write libs into linkflags as a full path, but not into libs.

        libs_s = "{0}/librte_" + ".a {0}/librte_".join(libs) + ".a"
        self.cpp_info.exelinkflags.append("-Wl,--whole-archive {} -Wl,--no-whole-archive".format(libs_s.format(os.path.join(self.package_folder, "lib"))))
        self.cpp_info.sharedlinkflags.append("")
        self.cpp_info.libs = ["bsd"]

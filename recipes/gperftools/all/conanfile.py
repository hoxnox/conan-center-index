import os
from conans import tools, ConanFile, CMake, AutoToolsBuildEnvironment
from conans.errors import ConanInvalidConfiguration, ConanException

required_conan_version = ">=1.35.0"

class CMakeConan(ConanFile):
    name = "gperftools"
    description = "Conan installer for Google perf tools"
    topics = ("cmake", "build", "installer")
    url = "https://github.com/conan-io/conan-center-index"
    homepage = "https://github.com/gperftools/gperftools"
    license = "BSD-3-Clause"
    generators = "cmake"
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared":[True, False], "cpuprof":[True, False], "heapprof":[True, False], "heapchecker":[True, False]}
    default_options = "shared=False", "cpuprof=False", "heapprof=False", "heapchecker=False"

    _source_subfolder = "source_subfolder"
    _cmake = None
    _autotools = None

    def source(self):
        tools.get(**self.conan_data["sources"][self.version], strip_root=True, destination=self._source_subfolder)

    def _configure_autotools(self):
        if self._autotools:
            return self._autotools
        self._autotools = AutoToolsBuildEnvironment(self)
        args = [
            "" if self.options.cpuprof or self.options.heapprof or self.options.heapchecker else "--enable-minimal",
            "--enable-shared" if self.options.shared else "--enable-static",
            "--disable-static" if self.options.shared else "--disable-shared",
            "--enable-cpu-profiler" if self.options.cpuprof else "--disable-cpu-profiler",
            "--enable-heap-profiler" if self.options.heapprof else "--disable-heap-profiler",
            "--enable-heap-checker" if self.options.heapchecker else "--disable-heap-checker",
        ]
        self._autotools.configure(args=args, configure_dir=self._source_subfolder)
        return self._autotools

    def build(self):
        autotools = self._configure_autotools()
        autotools.make()

    def package(self):
        autotools = self._configure_autotools()
        autotools.install()

    def package_info(self):
        if self.options.cpuprof or self.options.heapprof or self.options.heapchecker:
            self.cpp_info.libs = ["tcmalloc"]
        else:
            self.cpp_info.libs = ["tcmalloc_minimal"]

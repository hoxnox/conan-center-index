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
    options = {"shared":[True, False], "cpuprof":[True, False], "heapprof":[True, False], "heapchecker":[True, False], "debugalloc":[True, False], "minimal":[True, False]}
    default_options = "shared=False", "cpuprof=False", "heapprof=False", "heapchecker=False", "debugalloc=False", "minimal=True"

    _cmake = None

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
        self.cmake_.definitions["BUILD_SHARED_LIBS"] = self.options.shared
        self.cmake_.definitions["DEFAULT_BUILD_CPU_PROFILER"] = self.options.cpuprof
        self.cmake_.definitions["DEFAULT_BUILD_HEAP_PROFILER"] = self.options.heapprof
        self.cmake_.definitions["DEFAULT_BUILD_HEAP_CHECKER"] = self.options.heapchecker
        self.cmake_.definitions["DEFAULT_BUILD_DEBUGALLOC"] = self.options.debugalloc
        self.cmake_.definitions["DEFAULT_BUILD_MINIMAL"] = self.options.minimal
        self.cmake_.configure(source_folder = self._source_subfolder)
        return self.cmake_

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        cmake = self._configure_cmake()
        cmake.install()

    def package_info(self):
        if self.options.cpuprof:
            self.cpp_info.libs = ["tcmalloc_and_profiler"]
        elif self.options.heapprof or self.options.heapchecker or self.options.debugalloc:
            self.cpp_info.libs = ["tcmalloc"]
        else:
            self.cpp_info.libs = ["tcmalloc_minimal"]

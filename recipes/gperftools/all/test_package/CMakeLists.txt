PROJECT(test_package)
cmake_minimum_required(VERSION 2.8.12)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

ADD_EXECUTABLE(test_package test.cpp)
TARGET_LINK_LIBRARIES(test_package ${CONAN_LIBS})

PROJECT(SnappyTest)
cmake_minimum_required(VERSION 2.8.12)
set(CMAKE_CXX_STANDARD 11)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

find_package(Threads REQUIRED)

ADD_EXECUTABLE(test_package test.cpp)
TARGET_LINK_LIBRARIES(test_package ${CONAN_LIBS} ${CMAKE_THREAD_LIBS_INIT} ${CMAKE_DL_LIBS})

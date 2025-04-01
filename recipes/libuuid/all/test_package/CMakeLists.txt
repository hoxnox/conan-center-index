cmake_minimum_required(VERSION 3.8)
project(test_package C)

find_package(libuuid REQUIRED CONFIG)

add_executable(${PROJECT_NAME} test_package.c)
target_link_libraries(${PROJECT_NAME} libuuid::libuuid)
set_property(TARGET ${PROJECT_NAME} PROPERTY C_STANDARD 99)

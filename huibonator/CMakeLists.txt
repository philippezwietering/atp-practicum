cmake_minimum_required(VERSION 2.8.12)
project(lemonator)

find_package(PkgConfig)
pkg_search_module(PYTHON3 REQUIRED python3)

set(CMAKE_CXX_COMPILER g++)

include_directories("../externals/RS-232/")
include_directories("../externals/hwlib/library/")
include_directories("/home/philippe/Downloads/pybind11-master/include/")

set(LIBRARY_SOURCES
    ../externals/RS-232/rs232.c
    ../externals/hwlib/library/hwlib.cpp)

set(CMAKE_C_FLAGS "-fdata-sections -ffunction-sections -DBMPTK_TARGET_native")
set(CMAKE_CXX_FLAGS "-fdata-sections -ffunction-sections -DBMPTK_TARGET_native -std=c++14")

add_executable(lemonator-program reversecpp.cpp ${LIBRARY_SOURCES})
target_link_libraries(lemonator-program ${PYTHON3_LIBRARIES} "-lpthread")
target_include_directories(lemonator-program PUBLIC ${PYTHON3_INCLUDE_DIRS})
target_compile_options(lemonator-program PUBLIC ${PYTHON3_CFLAGS_OTHER})

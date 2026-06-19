cmake_minimum_required(VERSION 3.16)

project(rpg VERSION 0.1.0)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

set(CMAKE_RUNTIME_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/bin")
set(CMAKE_EXPORT_COMPILE_COMMANDS TRUE)

set(CMAKE_CXX_FLAGS "\
    -Wall -Wextra -Wpedantic \
    -Wshadow \
    -Wnon-virtual-dtor \
    -Wold-style-cast \
    -Wcast-align \
    -Wcast-qual \
    -Wunused \
    -Woverloaded-virtual \
    -Wconversion \
    -Wsign-conversion \
    -Wfloat-equal \
    -Wnull-dereference \
    -Wdouble-promotion \
    -Wformat=2 \
    -Wimplicit-fallthrough \
    -Wswitch-enum \
    -Wundef \
    -Wzero-as-null-pointer-constant \
    -Wextra-semi \
    -Wstrict-aliasing=2 \
    -Wno-unused-macros \
    -fdiagnostics-color=always")

set(CMAKE_CXX_FLAGS_DEBUG   "-O0 -g3 -fsanitize=address,undefined")
set(CMAKE_CXX_FLAGS_RELEASE "-O2 -DNDEBUG -Werror")

set(CMAKE_EXE_LINKER_FLAGS_DEBUG   "-fsanitize=address,undefined")
set(CMAKE_EXE_LINKER_FLAGS_RELEASE "")

# Default to Debug if not specified
if(NOT CMAKE_BUILD_TYPE)
    set(CMAKE_BUILD_TYPE Debug CACHE STRING "Build type" FORCE)
endif()

add_subdirectory(src)

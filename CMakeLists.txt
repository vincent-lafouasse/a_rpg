cmake_minimum_required(VERSION 3.16)

project(rpg VERSION 0.1.0)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

set(CMAKE_RUNTIME_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/bin")
set(CMAKE_EXPORT_COMPILE_COMMANDS TRUE)
set(CMAKE_EXE_LINKER_FLAGS "-fsanitize=address,undefined")

set(CMAKE_CXX_FLAGS "\
    -Wall -Wextra -pedantic \
    -Wshadow \
    -Wnon-virtual-dtor \
    -Wold-style-cast \
    -Wcast-align \
    -Wunused \
    -Woverloaded-virtual \
    -Wpedantic \
    -Wconversion \
    -Wsign-conversion \
    -Wnull-dereference \
    -Wdouble-promotion \
    -Wformat=2 \
    -Wimplicit-fallthrough \
    -fdiagnostics-color=always \
    -g3 -fsanitize=address,undefined")

add_subdirectory(src)

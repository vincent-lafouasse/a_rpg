set(RAYLIB_VERSION 5.5)
include(FetchContent)
FetchContent_Declare(
    raylib
    DOWNLOAD_EXTRACT_TIMESTAMP OFF
    URL https://github.com/raysan5/raylib/archive/refs/tags/${RAYLIB_VERSION}.tar.gz
)
FetchContent_MakeAvailable(raylib)

if(NOT TARGET raylib::raylib)
    add_library(raylib::raylib ALIAS raylib)
endif()

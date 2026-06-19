set(TINYXML2_VERSION 10.0.0)
include(FetchContent)
FetchContent_Declare(
    tinyxml2
    DOWNLOAD_EXTRACT_TIMESTAMP OFF
    URL https://github.com/leethomason/tinyxml2/archive/refs/tags/${TINYXML2_VERSION}.tar.gz
)
set(BUILD_TESTING OFF CACHE BOOL "" FORCE)
FetchContent_MakeAvailable(tinyxml2)
set(BUILD_TESTING ON CACHE BOOL "" FORCE)

target_compile_options(tinyxml2 PRIVATE -w)

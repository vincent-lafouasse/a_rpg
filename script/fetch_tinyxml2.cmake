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

# Suppress warnings when tinyxml2.h is included in user TUs
get_target_property(_tinyxml2_includes tinyxml2 INTERFACE_INCLUDE_DIRECTORIES)
set_target_properties(tinyxml2 PROPERTIES
    INTERFACE_SYSTEM_INCLUDE_DIRECTORIES "${_tinyxml2_includes}")

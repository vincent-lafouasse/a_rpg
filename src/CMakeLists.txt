include(${CMAKE_SOURCE_DIR}/script/fetch_raylib.cmake)
include(${CMAKE_SOURCE_DIR}/script/fetch_tinyxml2.cmake)

add_executable(rpg main.cpp)
target_link_libraries(rpg PRIVATE raylib tinyxml2::tinyxml2)

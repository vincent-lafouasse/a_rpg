include(${CMAKE_SOURCE_DIR}/script/fetch_raylib.cmake)

add_executable(rpg
    main.cpp
    TilesetBank.cpp
)
target_link_libraries(rpg PRIVATE raylib::raylib)

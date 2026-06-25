#include <raylib.h>

#include "LogicalMap.hpp"
#include "Renderer.hpp"
#include "Tilemap.hpp"

int main()
{
    Renderer renderer;

    LogicalMap logical_map;
    Tilemap tilemap;

    while (!WindowShouldClose()) {
        renderer.render(tilemap, &logical_map);
    }
}

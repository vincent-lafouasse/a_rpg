#include <raylib.h>

#include "LogicalMap.hpp"
#include "Renderer.hpp"
#include "Tilemap.hpp"

struct GameState {
    Vec2i player_pos;
    // MapId current_map
};

int main()
{
    Renderer renderer;

    LogicalMap logical_map;
    Tilemap tilemap;

    while (!WindowShouldClose()) {
        renderer.render(tilemap, &logical_map);
    }
}

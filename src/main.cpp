#include <raylib.h>

#include "LogicalMap.hpp"
#include "Renderer.hpp"
#include "Tilemap.hpp"

struct KeyboardState {
    bool up_pressed = false;
    bool down_pressed = false;
    bool left_pressed = false;
    bool right_pressed = false;
};

enum class GameCommand {
    go_up,
    go_down,
    go_left,
    go_right,
};

struct GameState {
    Vec2i player_pos {1, 1};
    // MapId current_map
};

int main()
{
    Renderer renderer;

    LogicalMap logical_map;
    Tilemap tilemap;

    KeyboardState keyboard;
    GameState state;
    (void)keyboard;
    (void)state;

    while (!WindowShouldClose()) {
        renderer.render(tilemap, &logical_map);
    }
}

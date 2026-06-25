#include <raylib.h>

#include "GameState.hpp"
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
    none,
    go_up,
    go_down,
    go_left,
    go_right,
};

// default to up-left
GameCommand parse_command(KeyboardState keyboard)
{
    if (keyboard.up_pressed)
        return GameCommand::go_up;
    if (keyboard.left_pressed)
        return GameCommand::go_left;
    if (keyboard.down_pressed)
        return GameCommand::go_down;
    if (keyboard.right_pressed)
        return GameCommand::go_right;
    return GameCommand::none;
}

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

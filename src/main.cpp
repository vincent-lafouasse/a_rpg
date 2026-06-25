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

void update_state(GameState& state, LogicalMap& map, GameCommand command)
{
    if (command == GameCommand::none) {
        return;
    }

    using C = GameCommand;

    Vec2i new_position = state.player_pos;
    switch (command) {
        case C::go_up:
            new_position = new_position.above();
            break;
        case C::go_down:
            new_position = new_position.below();
            break;
        case C::go_left:
            new_position = new_position.to_left();
            break;
        case C::go_right:
            new_position = new_position.to_right();
            break;
        case C::none:
            __builtin_unreachable();
    }
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
        renderer.render(tilemap, state, &logical_map);
    }
}

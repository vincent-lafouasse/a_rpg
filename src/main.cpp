#include <raylib.h>

class Map {
   public:
    static constexpr int width = 10;
    static constexpr int height = 5;
};

class Renderer {
   public:
    static constexpr const char* window_name = "rpg";
    static constexpr int target_fps = 60;
    static constexpr int tile_size = 64;
    static constexpr int window_width = Renderer::tile_size * Map::width;
    static constexpr int window_height = Renderer::tile_size * Map::height;
};

int main() {
    InitWindow(Renderer::window_width, Renderer::window_height,
               Renderer::window_name);
    SetTargetFPS(Renderer::target_fps);

    Texture2D tile = LoadTexture(
        "assets/kenney_micro-roguelike/Tiles/Colored/tile_0000.png");

    while (!WindowShouldClose()) {
        BeginDrawing();
        ClearBackground(RAYWHITE);

        for (int row = 0; row < Map::height; ++row) {
            for (int col = 0; col < Map::width; ++col) {
                Rectangle src{0, 0, (float)tile.width, (float)tile.height};
                Rectangle dst{
                    (float)(col * Renderer::tile_size),
                    (float)(row * Renderer::tile_size),
                    (float)Renderer::tile_size,
                    (float)Renderer::tile_size,
                };
                DrawTexturePro(tile, src, dst, {0, 0}, 0.0f, WHITE);
            }
        }

        EndDrawing();
    }

    UnloadTexture(tile);
    CloseWindow();
}

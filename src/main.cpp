#include <raylib.h>

int main() {
    constexpr int COLS = 10;
    constexpr int ROWS = 5;
    constexpr int TILE_SIZE = 64;
    constexpr int WIN_W = COLS * TILE_SIZE;
    constexpr int WIN_H = ROWS * TILE_SIZE;

    InitWindow(WIN_W, WIN_H, "hello raylib");
    SetTargetFPS(60);

    Texture2D tile = LoadTexture(
        "assets/kenney_micro-roguelike/Tiles/Colored/tile_0000.png");

    while (!WindowShouldClose()) {
        BeginDrawing();
        ClearBackground(RAYWHITE);

        for (int row = 0; row < ROWS; ++row) {
            for (int col = 0; col < COLS; ++col) {
                Rectangle src{0, 0, (float)tile.width, (float)tile.height};
                Rectangle dst{
                    (float)(col * TILE_SIZE),
                    (float)(row * TILE_SIZE),
                    (float)TILE_SIZE,
                    (float)TILE_SIZE,
                };
                DrawTexturePro(tile, src, dst, {0, 0}, 0.0f, WHITE);
            }
        }

        EndDrawing();
    }

    UnloadTexture(tile);
    CloseWindow();
}

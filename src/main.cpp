#include <cstdio>
#include <string>
#include <string_view>

#include <raylib.h>

#include "LogicalMap.hpp"
#include "Tilemap.hpp"
#include "TilesetBank.hpp"
#include "core.hpp"
#include "terrain_ids.gen.hpp"

class Renderer {
   public:
    static constexpr int s_tile_size = 64;

   private:
    static constexpr const char* s_window_name = "rpg";
    static constexpr int s_target_fps = 60;

    // temporary hardcoding
    static constexpr int s_window_width = s_tile_size * 10;
    static constexpr int s_window_height = s_tile_size * 5;

   public:
    Renderer() : m_tileset_bank()
    {
        InitWindow(s_window_width, s_window_height, s_window_name);
        SetTargetFPS(s_target_fps);
        m_tileset_bank.initialize();
    }
    ~Renderer() { CloseWindow(); }

    static constexpr Color orange = {255, 140, 0, 120};
    static constexpr Color blue = {0, 100, 255, 100};
    static constexpr Color transparent = {0, 0, 0, 0};

    static Color terrain_overlay_color(TerrainId id)
    {
        switch (id) {
            case TerrainId::wall:
                return orange;
            case TerrainId::ground:
                return blue;
            case TerrainId::none:
                return transparent;
        }
        std::fprintf(stderr, "unrecognized TerrainId: %d\n",
                     static_cast<int>(id));
        std::exit(1);
    }

    void render(const Tilemap& map) const { render(map, nullptr); }

    void render(const Tilemap& map, const LogicalMap* logical_map) const
    {
        const Tileset& tileset = m_tileset_bank.at(map.tileset_id);

        BeginDrawing();
        ClearBackground(RAYWHITE);

        for (int row = 0; row < map.height; ++row) {
            for (int col = 0; col < map.width; ++col) {
                const uint16_t tile = map.at(row, col);

                if (tile == 0) {
                    continue;
                }

                const Rectangle src = tileset.at(tile - 1);
                const Rectangle dst{
                    FLOAT(col * s_tile_size),
                    FLOAT(row * s_tile_size),
                    FLOAT(s_tile_size),
                    FLOAT(s_tile_size),
                };
                DrawTexturePro(tileset.texture, src, dst, {0, 0}, 0.0f, WHITE);

                if (logical_map != nullptr) {
                    const Color overlay =
                        terrain_overlay_color(logical_map->at(row, col));
                    DrawRectangleRec(dst, overlay);
                }
            }
        }

        EndDrawing();
    }

   private:
    TilesetBank m_tileset_bank;
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

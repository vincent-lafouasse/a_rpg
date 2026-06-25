#include "Renderer.hpp"

#include <cstdio>
#include <cstdlib>

#include "GameState.hpp"
#include "core.hpp"
#include "terrain_ids.gen.hpp"

namespace {
static constexpr const char* const k_player_sprite_path =
    "./assets/sprites/kenney_micro-roguelike/Tiles/Colored/tile_0004.png";

Rectangle rectangle(Vec2f pos, Vec2f sz)
{
    return {.x = pos.x, .y = pos.y, .width = sz.x, .height = sz.y};
}

Rectangle rectangle(Vec2i pos, Vec2i sz)
{
    return rectangle(pos.as_float(), sz.as_float());
}

static constexpr Color orange = {255, 140, 0, 120};
static constexpr Color blue = {0, 100, 255, 100};
static constexpr Color transparent = {0, 0, 0, 0};

Color terrain_overlay_color(TerrainId id)
{
    switch (id) {
        case TerrainId::wall:
            return orange;
        case TerrainId::ground:
            return blue;
        case TerrainId::none:
            return transparent;
    }
    std::fprintf(stderr, "unrecognized TerrainId: %d\n", static_cast<int>(id));
    std::exit(1);
}
}  // namespace

Renderer::Renderer() : m_tileset_bank(), m_player_sprite()
{
    InitWindow(s_window_width, s_window_height, s_window_name);
    SetTargetFPS(s_target_fps);
    m_tileset_bank.initialize();
    m_player_sprite = LoadTexture(k_player_sprite_path);
}
Renderer::~Renderer()
{
    UnloadTexture(m_player_sprite);
    CloseWindow();
}

void Renderer::render(const Tilemap& map, const GameState& state) const
{
    render(map, state, nullptr);
}

void Renderer::render(const Tilemap& map,
                      const GameState& state,
                      const LogicalMap* logical_map) const
{
    const Tileset& tileset = m_tileset_bank.at(map.tileset_id);

    BeginDrawing();
    ClearBackground(RAYWHITE);

    for (int row = 0; row < map.height; ++row) {
        for (int col = 0; col < map.width; ++col) {
            const Vec2i pos{.x = col, .y = row};
            const uint16_t tile = map.at(pos);

            if (tile == 0) {
                continue;
            }

            const Rectangle src = tileset.at(tile - 1);
            const Rectangle dst =
                rectangle(s_tile_size * pos, {s_tile_size, s_tile_size});
            DrawTexturePro(tileset.texture, src, dst, {0, 0}, 0.0f, WHITE);

            if (logical_map != nullptr) {
                const Color overlay =
                    terrain_overlay_color(logical_map->at(row, col));
                DrawRectangleRec(dst, overlay);
            }
        }
    }

    // render player
    {
        const Rectangle src = {0.0f, 0.0f, FLOAT(m_player_sprite.width),
                               FLOAT(m_player_sprite.height)};
        const Rectangle dst = rectangle(s_tile_size * state.player_pos,
                                        {s_tile_size, s_tile_size});
        DrawTexturePro(m_player_sprite, src, dst, {0, 0}, 0.0f, WHITE);
    }

    EndDrawing();
}

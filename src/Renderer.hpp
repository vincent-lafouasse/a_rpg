#pragma once

#include <raylib.h>

#include "GameState.hpp"
#include "LogicalMap.hpp"
#include "Tilemap.hpp"
#include "TilesetBank.hpp"

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
    Renderer();
    ~Renderer();

    void render(const Tilemap& map, const GameState& state) const;
    void render(const Tilemap& map,
                const GameState& state,
                const LogicalMap* logical_map) const;

   private:
    TilesetBank m_tileset_bank;
    Texture2D m_player_sprite;
};

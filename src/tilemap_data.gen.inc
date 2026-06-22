// -*- mode: c++ -*- vim: ft=cpp

#include <array>
#include <cstdint>

#include "tileset_ids.gen.hpp"

static constexpr int k_tilemap_height = 5;
static constexpr int k_tilemap_width = 10;
static constexpr int k_tilemap_tile_size = 8;
static constexpr TilesetId k_tilemap_tileset = TilesetId::colored_tilemap_packed;

static constexpr std::array<uint16_t, k_tilemap_height * k_tilemap_width> k_tile_data = {
     1,  2,  2,  2,  2,  2,  2,  2, 35,  4,
    17, 18, 18, 18, 18, 18, 18, 18, 18, 20,
    17, 18, 18, 18, 18, 18, 18, 18, 18, 20,
    17, 18, 18, 18, 18, 18, 18, 18, 18, 20,
    33, 35,  2,  2,  2,  2,  2,  2,  2, 36,
};

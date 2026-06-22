// -*- mode: c++ -*- vim: ft=cpp

#include <array>

#include "TilesetBank.hpp"

struct TilesetAsset {
    const char* source;
    int tile_size;
    int columns;
};

static constexpr std::array<TilesetAsset, TilesetBank::N> k_tileset_assets = {{
    { /* colored_tilemap_packed */
         "assets/sprites/kenney_micro-roguelike/Tilemap/colored_tilemap_packed.png",
         8,
         16,
    },
}};

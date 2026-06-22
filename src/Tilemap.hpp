#pragma once

#include <span>

#include "tileset_ids.gen.hpp"

struct Tilemap {
    using TileOffset = uint16_t;

    // this is a temporary constructor that constructs the one tilemap i have
    // later i will make a tilemap bank but for now this is fine
    Tilemap();
    ~Tilemap() = default;

    std::span<const TileOffset> tiles;
    TilesetId tileset_id;
    int height;
    int width;
    int tile_size;
};

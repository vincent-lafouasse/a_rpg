#pragma once

#include <span>

#include "tileset_ids.gen.hpp"

struct Tilemap {
    using TileOffset = uint16_t;

    std::span<const TileOffset> tiles;
    TilesetId tileset_id;
    int height;
    int width;
    int tile_size;
};

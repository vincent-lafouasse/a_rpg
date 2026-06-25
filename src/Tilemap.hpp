#pragma once

#include <cstdint>
#include <span>

#include "tileset_ids.gen.hpp"

struct Tilemap {
    using TileOffset = uint16_t;

    // this is a temporary constructor that constructs the one tilemap i have
    // later i will make a tilemap bank but for now this is fine
    Tilemap();
    ~Tilemap() = default;

    TileOffset at(int row, int col) const
    {
        const size_t tile_offset = static_cast<size_t>(col + row * width);
        return tiles[tile_offset];
    }

    std::span<const TileOffset> tiles;
    TilesetId tileset_id;
    int height;
    int width;
    int tile_size;
};

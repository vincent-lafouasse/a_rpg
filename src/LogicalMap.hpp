#pragma once

#include <cstddef>
#include <span>

#include "core.hpp"
#include "terrain_ids.gen.hpp"

struct LogicalMap {
    // this is a temporary constructor that constructs the one logical map i have
    // later i will make a logical map bank but for now this is fine
    LogicalMap();
    ~LogicalMap() = default;

    TerrainId at(int row, int col) const
    {
        const std::size_t offset = static_cast<size_t>(col + row * width);
        return tiles[offset];
    }

    TerrainId at(Vec2i pos) const { return this->at(pos.y, pos.x); }

    bool in_bounds(Vec2i pos) const
    {
        const bool x_ok = (pos.x >= 0) && (pos.x < width);
        const bool y_ok = (pos.y >= 0) && (pos.y < height);
        return x_ok && y_ok;
    }

    std::span<const TerrainId> tiles;
    int height;
    int width;
    int tile_size;
};

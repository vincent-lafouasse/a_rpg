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

    std::span<const TerrainId> tiles;
    int height;
    int width;
    int tile_size;
};

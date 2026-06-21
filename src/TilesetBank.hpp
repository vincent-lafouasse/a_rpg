#pragma once

#include <vector>

#include "tileset_ids.gen.hpp"

struct Tileset {};

struct TilesetBank {
    static constexpr int N = k_tileset_number;

    std::vector<Tileset> tilesets;
};

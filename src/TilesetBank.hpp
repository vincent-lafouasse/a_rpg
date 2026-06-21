#pragma once

#include <vector>

#include "tileset_ids.gen.hpp"

struct Tileset {};

struct TilesetBank {
    TilesetBank() {}
    TilesetBank(const TilesetBank&) = delete;
    TilesetBank(const TilesetBank&&) = delete;
    TilesetBank& operator=(const TilesetBank&) = delete;
    ~TilesetBank() {}

    static constexpr int N = k_tileset_number;

    std::vector<Tileset> tilesets;
};

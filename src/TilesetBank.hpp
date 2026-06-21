#pragma once

#include <vector>

#include <raylib.h>

#include "tileset_ids.gen.hpp"

// dumb struct, does not manage its lifetime
struct Tileset {
    Texture2D texture;
    int tile_size;
    int columns;
};

// manages the tileset lifetimes
struct TilesetBank {
    TilesetBank();
    TilesetBank(const TilesetBank&) = delete;
    TilesetBank(const TilesetBank&&) = delete;
    TilesetBank& operator=(const TilesetBank&) = delete;
    ~TilesetBank();

    static constexpr int N = k_tileset_number;

    std::vector<Tileset> tilesets;
};

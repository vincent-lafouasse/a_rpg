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
class TilesetBank {
   public:
    TilesetBank();
    TilesetBank(const TilesetBank&) = delete;
    TilesetBank(const TilesetBank&&) = delete;
    TilesetBank& operator=(const TilesetBank&) = delete;
    ~TilesetBank();

    void initialize();

    const Tileset& at(const TilesetId tileset_id) const;

    static constexpr int N = k_tileset_number;

   private:
    std::vector<Tileset> tilesets;
};

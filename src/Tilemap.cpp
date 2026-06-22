#include "Tilemap.hpp"

#include <array>

#include "tilemap_data.gen.inc"

// some random data to make sure i can hold a span to static data
static constexpr std::size_t N = 3;

static constexpr int k_height = 1;
static constexpr int k_width = 3;

static constexpr std::array<const Tilemap::TileOffset, N> data = {4, 2, 0};

Tilemap::Tilemap()
    : tiles(data),
      tileset_id(TilesetId::colored_tilemap_packed),
      height(k_height),
      width(k_width),
      tile_size(420)
{
}

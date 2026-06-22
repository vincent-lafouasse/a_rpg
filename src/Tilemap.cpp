#include "Tilemap.hpp"

#include "tilemap_data.gen.inc"

Tilemap::Tilemap()
    : tiles(k_tile_data),
      tileset_id(k_tilemap_tileset),
      height(k_tilemap_height),
      width(k_tilemap_width),
      tile_size(k_tilemap_tile_size)
{
}

#include "LogicalMap.hpp"

#include "logical_map_data.gen.inc"

LogicalMap::LogicalMap()
    : tiles(k_terrain_data),
      height(k_logical_map_height),
      width(k_logical_map_width),
      tile_size(k_logical_map_tile_size)
{
}

#include "Tilemap.hpp"

#include <array>

// #include "tilemap_data.gen.cin

// some random data to make sure i can hold a span to static data
static constexpr std::size_t N = 3;

static constexpr std::array<const Tilemap::TileOffset, N> data = {4, 2, 0};

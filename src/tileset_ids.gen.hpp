#pragma once

enum class TilesetId : int {
    colored_tilemap_packed = 0,
    COUNT
};

inline constexpr int k_tileset_number = static_cast<int>(TilesetId::COUNT);

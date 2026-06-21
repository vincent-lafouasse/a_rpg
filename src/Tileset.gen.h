#pragma once

struct Tileset {
    const char* source;
    int tile_size;
    int columns;
};

inline constexpr Tileset k_tileset = {
    "assets/sprites/kenney_micro-roguelike/Tilemap/colored_tilemap_packed.png",
    8,
    16,
};

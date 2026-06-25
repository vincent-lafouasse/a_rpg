#include "TilesetBank.hpp"

#include <cstdio>
#include <cstdlib>

#include "tileset_assets.gen.inc"

// TODO: probably some error checking but this is fine for now
static Tileset tileset_from_specs(const TilesetAsset& asset)
{
    Texture2D texture = LoadTexture(asset.source);
    return {texture, asset.tile_size, asset.columns};
}

TilesetBank::TilesetBank() : tilesets() {}

void TilesetBank::initialize()
{
    tilesets.reserve(N);

    for (const TilesetAsset& asset : k_tileset_assets) {
        tilesets.push_back(tileset_from_specs(asset));
    }
}

TilesetBank::~TilesetBank()
{
    for (const Tileset& tileset : tilesets) {
        UnloadTexture(tileset.texture);
    }
}

const Tileset& TilesetBank::at(const TilesetId tileset_id) const
{
    const auto index = static_cast<size_t>(tileset_id);

    switch (tileset_id) {
        case TilesetId::colored_tilemap_packed:
            return tilesets[index];
    }

    // should never go here if the pattern match is exhaustive
    std::fprintf(stderr, "Not a tileset id: %i\n",
                 static_cast<int>(tileset_id));
    std::exit(1);
}

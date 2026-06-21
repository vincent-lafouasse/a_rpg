#include "TilesetBank.hpp"

#include "tileset_assets.gen.inc"

// TODO: probably some error checking but this is fine for now
static Tileset tileset_from_specs(const TilesetAsset& asset)
{
    Texture2D texture = LoadTexture(asset.source);
    return {texture, asset.tile_size, asset.columns};
}

TilesetBank::TilesetBank() : tilesets()
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

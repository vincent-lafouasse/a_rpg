# /// script
# requires-python = ">=3.10"
# dependencies = [
#   "lxml",
# ]
# ///

from __future__ import annotations

import sys
import inspect
import os
from pathlib import Path

from Tilemap import Tilemap
from Tileset import Tileset


def codegen_tileset_bank(bank: list[Tileset], project_root: Path, outdir: Path) -> None:
    def rel_source(tileset):
        return tileset.source.relative_to(project_root)

    bank = sorted(bank)
    name_bank = [(tileset.name, tileset) for tileset in bank]

    with open(outdir / "tileset_ids.gen.hpp", "w") as tileset_id_file:
        id_source = ""
        id_source += inspect.cleandoc(
            f"""
            #pragma once

            enum class TilesetId : int {{
        """
        )
        id_source += "\n"
        for i, tileset in enumerate(bank):
            id_source += f"    {tileset.name} = {i},\n"
        id_source += inspect.cleandoc(
            f"""
            }};

            inline constexpr int k_tileset_number = {len(bank)};
        """
        )
        id_source += "\n"
        tileset_id_file.write(id_source)

    with open(outdir / "tileset_assets.gen.inc", "w") as tileset_asset_file:
        asset_source = ""
        asset_source += inspect.cleandoc(
            f"""
            // -*- mode: c++ -*- vim: ft=cpp

            #include <array>

            #include "TilesetBank.hpp"

            struct TilesetAsset {{
                const char* source;
                int tile_size;
                int columns;
            }};

            static constexpr std::array<TilesetAsset, TilesetBank::N> k_tileset_assets = {{{{
        """
        )
        asset_source += "\n"

        for tileset in bank:
            asset_source += f"    {{ /* {tileset.name} */\n"
            asset_source += f'         "{rel_source(tileset)}",\n'
            asset_source += f"         {tileset.tile_size},\n"
            asset_source += f"         {tileset.columns},\n"
            asset_source += f"    }},\n"

        asset_source += "}};\n"

        tileset_asset_file.write(asset_source)


def codegen_terrain_ids(outdir: Path) -> None:
    from Tilemap import Tilemap

    terrain_types = Tilemap.TERRAIN_TYPES  # {int: str}

    src = ""
    src += inspect.cleandoc(
        f"""
        #pragma once

        enum class TerrainId : int {{
    """
    )
    src += "\n"
    for value, name in sorted(terrain_types.items()):
        src += f"    {name} = {value},\n"
    src += inspect.cleandoc(
        f"""
        }};

        inline constexpr int k_terrain_type_number = {len(terrain_types)};
    """
    )
    src += "\n"

    with open(outdir / "terrain_ids.gen.hpp", "w") as f:
        f.write(src)


def codegen_tilemap(map: Tilemap, bank: list[Tileset], outdir: Path) -> None:
    # TODO: store stem and not basename
    tileset_id = map.tileset_id[:-4]

    with open(outdir / "tilemap_data.gen.inc", "w") as tilemap_data:
        data = ""
        data += inspect.cleandoc(
            f"""
            // -*- mode: c++ -*- vim: ft=cpp

            #include <array>
            #include <cstdint>

            #include "tileset_ids.gen.hpp"

            static constexpr int k_tilemap_height = {map.metadata.height};
            static constexpr int k_tilemap_width = {map.metadata.width};
            static constexpr int k_tilemap_tile_size = {map.metadata.tile_size};
            static constexpr TilesetId k_tilemap_tileset = TilesetId::{tileset_id};
        """
        )
        data += "\n\n"
        initializer = map.format_tiles()
        lines = initializer.split("\n")
        lines = ["    " + line for line in lines]
        initializer = "\n".join(lines)

        data += f"static constexpr std::array<uint16_t, k_tilemap_height * k_tilemap_width> k_tile_data = {{\n"
        data += initializer
        data += "\n};\n"
        tilemap_data.write(data)


def main() -> None:
    if len(sys.argv) != 2:
        print(f"usage: uv run {sys.argv[0]} <map.tmx>", file=sys.stderr)
        sys.exit(1)

    map_path = Path(sys.argv[1])

    tilemap = Tilemap.load(map_path)

    tileset_path = map_path.parent / tilemap.tileset_id
    assert tileset_path.exists()

    tileset = Tileset.load(tileset_path)

    tileset_bank = [tileset]

    # yes this is only meant to run on my machine
    project_root = Path("/Users/poss/code/cpp/ff1")
    outdir = project_root / "src"

    codegen_tileset_bank(tileset_bank, project_root, outdir)
    codegen_terrain_ids(outdir)
    codegen_tilemap(tilemap, project_root, outdir)


if __name__ == "__main__":
    main()

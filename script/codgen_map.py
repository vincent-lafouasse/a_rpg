# /// script
# requires-python = ">=3.10"
# dependencies = [
#   "lxml",
# ]
# ///

# yes it all needs to be in 1 script because i use the hash of the script

from __future__ import annotations

import dataclasses
import sys
import inspect
import os
from pathlib import Path
from lxml import etree


### ----- parsing the XML files that Tiled gave me


@dataclasses.dataclass
class Tilemap:
    @dataclasses.dataclass
    class Metadata:
        width: int
        height: int
        tile_size: int

    name: str
    metadata: Tilemap.Metadata
    tiles: list[int]
    tileset_id: str

    @staticmethod
    def load(tmx_path: Path) -> Tilemap:
        assert tmx_path.suffix == ".tmx"
        data = tmx_path.read_bytes()
        return Tilemap.parse(data, tmx_path.stem)

    @staticmethod
    def parse(tmx: bytes, name: str) -> Tilemap:
        root = etree.fromstring(tmx)
        assert root.tag == "map"

        meta = Tilemap.parse_metadata(root)

        tileset_id = Tilemap.identify_tileset(root)

        csv_payload = Tilemap.extract_layer_csv(root, meta)
        tiles = Tilemap.parse_layer(csv_payload, meta)

        return Tilemap(name=name, metadata=meta, tiles=tiles, tileset_id=tileset_id)

    @staticmethod
    def parse_metadata(root) -> Tilemap.Metadata:
        width = int(root.attrib["width"])
        height = int(root.attrib["height"])
        tilewidth = int(root.attrib["tilewidth"])
        tileheight = int(root.attrib["tileheight"])
        assert tilewidth == tileheight
        tile_size = tilewidth

        assert root.attrib["orientation"] == "orthogonal"
        assert root.attrib["renderorder"] == "right-down"

        return Tilemap.Metadata(
            width=width,
            height=height,
            tile_size=tile_size,
        )

    @staticmethod
    def identify_tileset(root) -> str:
        tilesets = root.findall("tileset")
        assert len(tilesets) == 1, f"expected 1 tileset, got {len(tilesets)}"

        source = tilesets[0].attrib["source"]
        assert source[-4:] == ".tsx"

        return source

    @staticmethod
    def extract_layer_csv(root, metadata: Tilemap.Metadata) -> str:
        layers = root.findall("layer")
        assert len(layers) == 1, f"expected 1 layer, got {len(layers)}"

        layer = layers[0]
        assert int(layer.attrib["width"]) == metadata.width
        assert int(layer.attrib["height"]) == metadata.height

        data_el = layer.find("data")
        assert data_el is not None
        assert data_el.attrib.get("encoding") == "csv"

        return data_el.text.strip()

    @staticmethod
    def parse_layer(csv: str, metadata: Metadata) -> list[int]:
        rows = [
            [int(v) for v in row.split(",") if v.strip()] for row in csv.splitlines()
        ]

        assert (
            len(rows) == metadata.height
        ), f"expected {metadata.height} rows, got {len(rows)}"
        for i, row in enumerate(rows):
            assert (
                len(row) == metadata.width
            ), f"row {i}: expected {metadata.width} cols, got {len(row)}"
            for v in row:
                assert 0 <= v <= 0xFFFF, f"row {i}: value {v} does not fit in u16"

        return [v for row in rows for v in row]

    def log(self) -> None:
        print(f"-- map:        {self.name}")
        print(f"width:         {self.metadata.width}")
        print(f"height:        {self.metadata.height}")
        print(f"tile_size:     {self.metadata.tile_size}")
        print(f"tileset:       {self.tileset_id}")
        print(f"-- tiles:\n{self.tiles}")


# primarily stored in the .tsx but worth double checking for consistency with
# the .tmx
@dataclasses.dataclass
class Tileset:
    name: str
    tile_size: int
    columns: int
    source: Path

    @staticmethod
    def load(tsx_path: Path) -> Tileset:
        assert tsx_path.suffix == ".tsx"
        data = tsx_path.read_bytes()
        return Tileset.parse(data, tsx_path.parent)

    @staticmethod
    def parse(tsx: bytes, dir: Path) -> Tileset:
        root = etree.fromstring(tsx)
        assert root.tag == "tileset"

        tilewidth = int(root.attrib["tilewidth"])
        tileheight = int(root.attrib["tileheight"])
        assert tilewidth == tileheight
        tile_size = tilewidth

        columns = int(root.attrib["columns"])

        image_el = root.find("image")
        assert image_el is not None

        source = (dir / image_el.attrib["source"]).resolve()
        assert source.exists()

        # some sanity checks
        tile_count = int(root.attrib["tilecount"])
        width = columns
        height = tile_count / width
        source_pixel_width = int(image_el.attrib["width"])
        source_pixel_height = int(image_el.attrib["height"])

        assert width * tile_size <= source_pixel_width
        assert height * tile_size <= source_pixel_height

        return Tileset(
            name=root.attrib["name"],
            tile_size=tile_size,
            columns=columns,
            source=source,
        )

    def log(self) -> None:
        print(f"-- tileset:    {self.name}")
        print(f"tile_size:     {self.tile_size}")
        print(f"columns:       {self.columns}")
        print(f"source:        {self.source}")


def main() -> None:
    if len(sys.argv) != 2:
        print(f"usage: uv run {sys.argv[0]} <map.tmx>", file=sys.stderr)
        sys.exit(1)

    map_path = Path(sys.argv[1])

    tilemap = Tilemap.load(map_path)
    tilemap.log()

    tileset_path = map_path.parent / tilemap.tileset_id
    assert tileset_path.exists()

    tileset = Tileset.load(tileset_path)
    tileset.log()

    # yes this is only meant to run on my machine
    project_root = Path("/Users/poss/code/cpp/ff1")
    tileset_source_rel = tileset.source.relative_to(project_root)
    print(tileset_source_rel)


if __name__ == "__main__":
    main()

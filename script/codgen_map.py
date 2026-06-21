# /// script
# requires-python = ">=3.10"
# dependencies = [
#   "lxml",
# ]
# ///

# yes it all needs to be in 1 script because i use the hash of the script

from __future__ import annotations

import hashlib
import dataclasses
import sys
import inspect
import os
from pathlib import Path
from lxml import etree

THIS_SCRIPT = Path(__file__)


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
    tile_count: int
    columns: int
    source: Path
    source_pixel_width: int
    source_pixel_height: int
    tsx_hash: str

    @staticmethod
    def read(tmx_root, map_path: Path) -> Tileset:
        tileset_el = tmx_root.find("tileset")
        assert tileset_el is not None
        tsx_path = map_path.parent / tileset_el.attrib["source"]

        tsx_root = etree.parse(tsx_path).getroot()
        assert tsx_root.tag == "tileset"

        tilewidth = int(tsx_root.attrib["tilewidth"])
        tileheight = int(tsx_root.attrib["tileheight"])
        assert tilewidth == tileheight

        image_el = tsx_root.find("image")
        assert image_el is not None

        return Tileset(
            name=tsx_root.attrib["name"],
            tile_size=tilewidth,
            tile_count=int(tsx_root.attrib["tilecount"]),
            columns=int(tsx_root.attrib["columns"]),
            source=(tsx_path.parent / image_el.attrib["source"]).resolve(),
            source_pixel_width=int(image_el.attrib["width"]),
            source_pixel_height=int(image_el.attrib["height"]),
            tsx_hash=hashlib.sha256(tsx_path.read_bytes()).hexdigest(),
        )

    def log(self) -> None:
        print(f"tileset name:  {self.name}")
        print(f"tile_size:     {self.tile_size}")
        print(f"tile_count:    {self.tile_count}")
        print(f"columns:       {self.columns}")
        print(f"source:        {self.source}")
        print(f"px size:       {self.source_pixel_width}x{self.source_pixel_height}")


### ----- hashes and no-op detection


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def map_fingerprint(metadata: Metadata) -> str:
    return inspect.cleandoc(
        f"""
        /*!
         * script_hash : {metadata.script_hash}
         * map_hash    : {metadata.map_hash}
         */
    """
    )


def tileset_fingerprint(tileset: Tileset, script_hash: str) -> str:
    return inspect.cleandoc(
        f"""
        /*!
         * script_hash  : {script_hash}
         * tileset_hash : {tileset.tsx_hash}
         */
    """
    )


def check_fingerprint(path: Path, fingerprint: str) -> bool:
    if not path.exists():
        return False
    lines = path.read_text().splitlines()[:4]
    return "\n".join(lines) == fingerprint


def main() -> None:
    if len(sys.argv) != 2:
        print(f"usage: uv run {sys.argv[0]} <map.tmx>", file=sys.stderr)
        sys.exit(1)

    map_path = Path(sys.argv[1])

    tilemap = Tilemap.load(map_path)
    tilemap.log()

    tileset_path = map_path.parent / tilemap.tileset_id
    assert tileset_path.exists()
    print(tileset_path)


if __name__ == "__main__":
    main()

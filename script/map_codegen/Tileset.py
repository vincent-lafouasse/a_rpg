from __future__ import annotations

import dataclasses
import sys
from pathlib import Path

from lxml import etree


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

from __future__ import annotations

import dataclasses
import sys
from lxml import etree


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

    def format_tiles(self) -> str:
        width = self.metadata.width
        col_width = max(len(str(v)) for v in self.tiles)
        rows = [
            self.tiles[i * width : (i + 1) * width] for i in range(self.metadata.height)
        ]
        return "\n".join(" ".join(f"{v:{col_width}d}," for v in row) for row in rows)

    def log(self) -> None:
        print(f"-- map:        {self.name}")
        print(f"width:         {self.metadata.width}")
        print(f"height:        {self.metadata.height}")
        print(f"tile_size:     {self.metadata.tile_size}")
        print(f"tileset:       {self.tileset_id}")
        print(f"-- tiles:\n{self.tiles}")

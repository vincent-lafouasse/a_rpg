from __future__ import annotations

import dataclasses
from pathlib import Path
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
    terrain: list[int]
    terrain_types: dict[int, str]  # int -> name, e.g. {1: "ground", 2: "wall"}
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

        render_csv = Tilemap.extract_named_layer_csv(root, "render", meta)
        tiles = Tilemap.parse_layer(render_csv, meta)

        terrain_csv = Tilemap.extract_named_layer_csv(root, "terrain", meta)
        terrain = Tilemap.parse_layer(terrain_csv, meta)

        terrain_types = Tilemap.parse_terrain_types(root)
        for tile in terrain:
            if tile not in terrain_types:
                print(f"Unknown terrain key: {tile} in tilemap {name}")
                print(terrain_types)

        return Tilemap(
            name=name,
            metadata=meta,
            tiles=tiles,
            terrain=terrain,
            terrain_types=terrain_types,
            tileset_id=tileset_id,
        )

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

        return Tilemap.Metadata(width=width, height=height, tile_size=tile_size)

    @staticmethod
    def identify_tileset(root) -> str:
        tilesets = root.findall("tileset")
        assert len(tilesets) == 1, f"expected 1 tileset, got {len(tilesets)}"

        source = tilesets[0].attrib["source"]
        assert source[-4:] == ".tsx"

        return source

    @staticmethod
    def parse_terrain_types(root) -> dict[int, str]:
        el = root.find("terraintypes")
        assert el is not None, "missing <terraintypes> element"
        return {int(v): k for k, v in el.attrib.items()}

    @staticmethod
    def extract_named_layer_csv(
        root, layer_name: str, metadata: Tilemap.Metadata
    ) -> str:
        layers = [
            l for l in root.findall("layer") if l.attrib.get("name") == layer_name
        ]
        assert (
            len(layers) == 1
        ), f"expected 1 layer named '{layer_name}', got {len(layers)}"

        layer = layers[0]
        assert int(layer.attrib["width"]) == metadata.width
        assert int(layer.attrib["height"]) == metadata.height

        data_el = layer.find("data")
        assert data_el is not None
        assert data_el.attrib.get("encoding") == "csv"

        return data_el.text.strip()

    @staticmethod
    def parse_layer(csv: str, metadata: Tilemap.Metadata) -> list[int]:
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

    def format_layer(self, data: list[int]) -> str:
        width = self.metadata.width
        col_width = max(len(str(v)) for v in data)
        rows = [data[i * width : (i + 1) * width] for i in range(self.metadata.height)]
        return "\n".join(" ".join(f"{v:{col_width}d}," for v in row) for row in rows)

    def format_tiles(self) -> str:
        return self.format_layer(self.tiles)

    def format_terrain(self) -> str:
        return self.format_layer(self.terrain)

    def log(self) -> None:
        print(f"-- map:          {self.name}")
        print(f"width:           {self.metadata.width}")
        print(f"height:          {self.metadata.height}")
        print(f"tile_size:       {self.metadata.tile_size}")
        print(f"tileset:         {self.tileset_id}")
        print(f"terrain_types:   {self.terrain_types}")
        print(f"-- tiles:\n{self.tiles}")
        print(f"-- terrain:\n{self.terrain}")

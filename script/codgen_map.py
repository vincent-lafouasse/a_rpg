# /// script
# requires-python = ">=3.10"
# dependencies = [
#   "lxml",
# ]
# ///

import hashlib
import dataclasses
import sys
from pathlib import Path
from lxml import etree


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def trace_source() -> str:
    caller_frame = inspect.stack()[1]
    filename = os.path.basename(caller_frame.filename)
    line = caller_frame.lineno
    return f"/* generated from {filename}: l.{line} */"


class FileBuffer:
    def __init__(self, name, path):
        self.buffer = ""
        # vvv still unsure which one i need
        self.name = name
        self.path = path

    def get(self) -> str:
        return self.buffer

    def add(self, s: str) -> None:
        self.buffer += s

    def add_endl(self, s: str) -> None:
        self.add(s)
        self.add("\n")

    def trace_source(self) -> None:
        caller_frame = inspect.stack()[1]
        filename = os.path.basename(caller_frame.filename)
        line = caller_frame.lineno
        self.add_endl(f"/* generated from {filename}: l.{line} */")

    def write(self) -> None:
        with open(self.path, "w") as outfile:
            outfile.write(self.buffer)


@dataclasses.dataclass
class Metadata:
    script_name: str
    map_name: str
    width: int
    height: int
    tile_size: int
    script_hash: str
    map_hash: str


def read_metadata_or_exit(root, script_path: Path, map_path: Path) -> Metadata:
    script_name = script_path.parts[-1]
    map_name = map_path.parts[-1]
    assert script_name[-3:] == ".py"
    assert map_name[-4:] == ".tmx"

    script_basename = script_name[:-3]
    map_basename = map_name[:-4]

    script_hash = sha256(script_path)
    map_hash = sha256(map_path)

    assert root.tag == "map"
    width = int(root.attrib["width"])
    height = int(root.attrib["height"])
    tilewidth = int(root.attrib["tilewidth"])
    tileheight = int(root.attrib["tileheight"])
    assert tilewidth == tileheight
    tile_size = tilewidth

    print(f"script:      {script_basename}")
    print(f"map:         {map_basename}")
    print(f"width:       {width}")
    print(f"height:      {height}")
    print(f"tile_size:   {tile_size}")
    print(f"script_hash: {script_hash}")
    print(f"map_hash:    {map_hash}")

    return Metadata(
        script_basename, map_basename, width, height, tile_size, script_hash, map_hash
    )


# primarily stored in the .tsx but worth double checking for consistency with
# the .tmx
@dataclasses.dataclass
class Tilemap:
    name: str
    tile_size: int
    tile_count: int
    width: int
    source: str
    source_pixel_width: int
    source_pixel_height: int


def main() -> None:
    if len(sys.argv) != 2:
        print(f"usage: uv run {sys.argv[0]} <map.tmx>", file=sys.stderr)
        sys.exit(1)

    script_path = Path(__file__)
    map_path = Path(sys.argv[1])

    root = etree.parse(map_path).getroot()
    metadata = read_metadata_or_exit(root, script_path, map_path)


if __name__ == "__main__":
    main()

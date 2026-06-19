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


def trace_source():
    caller_frame = inspect.stack()[1]
    filename = os.path.basename(caller_frame.filename)
    line = caller_frame.lineno
    return f"/* generated from {filename}: l.{line} */"


class FileBuffer:
    def __init__(self, name):
        self.name = name
        self.buffer = ""

    def get(self):
        return self.buffer

    def add(self, s):
        self.buffer += s

    def add_endl(self, s):
        self.add(s)
        self.add("\n")

    def trace_source(self):
        caller_frame = inspect.stack()[1]
        filename = os.path.basename(caller_frame.filename)
        line = caller_frame.lineno
        self.add_endl(f"/* generated from {filename}: l.{line} */")

    def write(self):
        # do file io
        pass


@dataclasses.dataclass
class ParsingContext:
    script_name: str
    map_name: str
    width: int
    height: int
    tile_size: int
    script_hash: str
    map_hash: str


def main() -> None:
    if len(sys.argv) != 2:
        print(f"usage: uv run {sys.argv[0]} <map.tmx>", file=sys.stderr)
        sys.exit(1)

    script_path = Path(__file__)
    map_path = Path(sys.argv[1])

    script_basename = script_path.parts[-1]
    map_basename = map_path.parts[-1]
    assert script_basename[-3:] == ".py"
    assert map_basename[-4:] == ".tmx"

    script_basename = script_basename[:-3]
    map_basename = map_basename[:-4]

    script_hash = sha256(script_path)
    map_hash = sha256(map_path)

    root = etree.parse(map_path).getroot()
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


if __name__ == "__main__":
    main()

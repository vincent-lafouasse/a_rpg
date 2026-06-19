# /// script
# requires-python = ">=3.10"
# dependencies = [
#   "lxml",
# ]
# ///

import hashlib
import sys
from pathlib import Path
from lxml import etree


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    if len(sys.argv) != 2:
        print(f"usage: uv run {sys.argv[0]} <map.tmx>", file=sys.stderr)
        sys.exit(1)

    script_path = Path(__file__)
    map_path = Path(sys.argv[1])

    script_hash = sha256(script_path)
    map_hash = sha256(map_path)

    root = etree.parse(map_path).getroot()
    assert root.tag == "map"

    width = int(root.attrib["width"])
    height = int(root.attrib["height"])
    tilewidth = int(root.attrib["tilewidth"])
    tileheight = int(root.attrib["tileheight"])

    print(f"width:       {width}")
    print(f"height:      {height}")
    print(f"tilewidth:   {tilewidth}")
    print(f"tileheight:  {tileheight}")
    print(f"script_hash: {script_hash}")
    print(f"map_hash:    {map_hash}")


if __name__ == "__main__":
    main()

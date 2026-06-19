# /// script
# requires-python = ">=3.10"
# dependencies = [
#   "lxml",
# ]
# ///

import sys
from lxml import etree


def main() -> None:
    if len(sys.argv) != 2:
        print(f"usage: {sys.argv[0]} <map.tmx>", file=sys.stderr)
        sys.exit(1)

    path = sys.argv[1]
    root = etree.parse(path).getroot()
    assert root.tag == "map"

    width = int(root.attrib["width"])
    height = int(root.attrib["height"])
    tilewidth = int(root.attrib["tilewidth"])
    tileheight = int(root.attrib["tileheight"])

    print(f"width:      {width}")
    print(f"height:     {height}")
    print(f"tilewidth:  {tilewidth}")
    print(f"tileheight: {tileheight}")


if __name__ == "__main__":
    main()

"""Add width/height to every <img> in the built site so the browser reserves each figure's space before it loads.

Without them a figure has no height until it arrives, so jumping to a section (a link with #anchor) lands, and
then figures above it load and push the section down the screen. Each <img> also gets style="height:auto", so the
attributes only fix the aspect ratio and figures still shrink to the page width.
Usage: python3 site/img_sizes.py <quartz>/public
"""
import os
import re
import struct
import sys
from urllib.parse import unquote

IMG = re.compile(r"<img\b([^>]*?)\bsrc=\"([^\"]+)\"([^>]*)>")


def size(path):
    with open(path, "rb") as f:
        head = f.read(26)
        if head[:8] == b"\x89PNG\r\n\x1a\n":
            return struct.unpack(">II", head[16:24])
        if head[:6] in (b"GIF87a", b"GIF89a"):
            return struct.unpack("<HH", head[6:10])
        if head[:2] == b"\xff\xd8":  # JPEG: find the first start-of-frame marker
            f.seek(2)
            while True:
                marker, length = struct.unpack(">2sH", f.read(4))
                if marker[1] in (0xC0, 0xC1, 0xC2):
                    h, w = struct.unpack(">xHH", f.read(5))
                    return w, h
                f.seek(length - 2, 1)
    return None


def main(public):
    added = missing = 0
    for root, _, files in os.walk(public):
        for name in files:
            if not name.endswith(".html"):
                continue
            page = os.path.join(root, name)
            html = open(page, encoding="utf-8").read()

            def fix(m):
                nonlocal added, missing
                if re.search(r"\bwidth=", m.group(0)) or m.group(2).startswith(("http", "data:")):
                    return m.group(0)
                src = unquote(m.group(2).split("#")[0].split("?")[0])
                path = os.path.join(public, src.lstrip("/")) if src.startswith("/") else os.path.join(root, src)
                wh = size(path) if os.path.isfile(path) else None
                if not wh:
                    missing += 1
                    return m.group(0)
                added += 1
                # inline height:auto: a browser holding an older cached stylesheet would otherwise use the
                # height attribute as is and stretch the figure tall on a narrow screen
                return (f'<img{m.group(1)}src="{m.group(2)}" width="{wh[0]}" height="{wh[1]}" style="height:auto"'
                        f'{m.group(3)}>')

            new = IMG.sub(fix, html)
            if new != html:
                open(page, "w", encoding="utf-8").write(new)
    print(f"img_sizes: {added} sized, {missing} without a readable file")


if __name__ == "__main__":
    main(sys.argv[1])

"""Download the saved AmbitionBox pages used by the Note, from the Wayback Machine.

The live site blocks scripts (October 2026), so we use real copies archived by
web.archive.org. "id_" in the address returns the page exactly as AmbitionBox sent it.
<script> and <style> blocks are removed to keep data/ small; the HTML we parse is untouched.
Run: python fetch_archive.py
"""
import re
import time
from pathlib import Path

import requests

HERE = Path(__file__).parent
SITE = "https://www.ambitionbox.com/list-of-companies"
PAGES = {
    # file name: (archive time stamp, address that was archived)
    "ambitionbox_2022_page1.html": ("20220804073522", SITE + "?campaign=desktop_nav&page=1"),
    "ambitionbox_2022_page2.html": ("20220804073838", SITE + "?campaign=desktop_nav&page=2"),
    "ambitionbox_2026_page1.html": ("20260829101916", SITE),
}
DROP = re.compile(r"<(script|style)\b.*?</\1>", re.S | re.I)

for name, (stamp, url) in PAGES.items():
    html = requests.get(f"https://web.archive.org/web/{stamp}id_/{url}", timeout=60).text
    (HERE / name).write_text(DROP.sub("", html), encoding="utf-8")
    print(name, len(html), "->", (HERE / name).stat().st_size, "bytes")
    time.sleep(3)  # be polite to the archive too

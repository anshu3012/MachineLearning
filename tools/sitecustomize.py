"""Interactive twins for every Plotly figure, with no change to the figure scripts.

tools/build.sh puts this folder on PYTHONPATH, so Python imports this file at start-up. It wraps Plotly's
write_image: whenever a script writes <name>.png, the same figure is also written as <name>.html (hover, zoom,
legend toggling), which the website embeds in place of the PNG. The PDF, Obsidian and GitHub keep the PNG.
Animation frames are skipped: they go to hidden or temporary folders, or are numbered files, and the GIF is their
product. plotly.js is not copied into each twin: every twin points at the one copy in tools/plotly.min.js by a
relative path (which also holds on the website, where the site build copies that file to the same place), so a
twin is a few tens of KB and nothing is fetched from outside the site."""
import re
from pathlib import Path

try:
    from plotly.basedatatypes import BaseFigure
except ImportError:                                   # a script that does not use Plotly
    BaseFigure = None

def plotlyjs_src(html_path):
    """Relative path from an HTML file to the repo's tools/plotly.min.js (same depth on the website)."""
    here = Path(str(html_path)).resolve().parent
    for up in [here, *here.parents]:
        if (up / "tools" / "plotly.min.js").exists():
            return str(Path(*[".."] * len(here.relative_to(up).parts)) / "tools" / "plotly.min.js")
    return "cdn"                                      # outside the repo: fall back to the CDN


FRAME = re.compile(r"^(\d+|frame.*|.*_\d{3,})$")      # 000.png, frame_12.png, scatter_015.png


def is_frame(path):
    return path.parent.name.startswith((".", "frames", "_")) or path.parent.name.endswith("frames") \
        or FRAME.match(path.stem) is not None


if BaseFigure is not None:
    _write_image = BaseFigure.write_image

    def write_image(self, file, *args, **kwargs):
        _write_image(self, file, *args, **kwargs)
        path = Path(str(file))
        if path.suffix.lower() == ".png" and not is_frame(path):
            twin = self
            html = twin.to_html(include_plotlyjs=plotlyjs_src(path), full_html=True, default_width="100%",
                                default_height=f"{twin.layout.height or 500}px",
                                config={"responsive": True, "displaylogo": False})
            # the twin fills its container: drop the fixed pixel width the PNG was rendered at
            if twin.layout.width:
                html = re.sub(r'"width":%d,?' % twin.layout.width, "", html, count=1)
            path.with_suffix(".html").write_text(html)

    BaseFigure.write_image = write_image

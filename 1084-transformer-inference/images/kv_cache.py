"""Extra of section 7: what the KV cache saves. Translating "i think you're right ." takes 8 decoder steps. One row
per step, one cell per input position. Left: without a cache every step recomputes the key and value vectors of
all positions so far. Right: with the cache each step computes them only for the new word and reuses the rest.
The counts are arithmetic (1 + 2 + ... + n against n); the words are the model's own output (data/decode_steps.csv).
Our own design. Run: python kv_cache.py -> kv_cache.gif, kv_cache_frames.png (Plotly frames + ffmpeg)"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from PIL import Image
from common import ORANGE, GREY, FONT

HERE = Path(__file__).parent
SENT = "i think you're right ."
steps = pd.read_csv(HERE.parent / "data" / "decode_steps.csv")
steps = steps[(steps.sentence == SENT) & (steps["rank"] == 1)].sort_values("step")
tokens = ["&lt;start&gt;"] + list(steps.word)[:-1]                 # the decoder input at the last step
n = len(tokens)
assert n == 8 and steps.word.iloc[-1] == "<end>"
SCALE = [[0, "white"], [0.5, "#D9D9D9"], [1, ORANGE]]             # empty, reused, computed


def grid(t, cache):
    z = np.zeros((n, n))
    for s in range(1, t + 1):
        z[s - 1, :s] = 1 if cache else 2
        z[s - 1, s - 1] = 2
    return z


def frame(t):
    fig = make_subplots(1, 2, horizontal_spacing=0.1, subplot_titles=(
        f"no cache: {t * (t + 1) // 2} computed so far", f"KV cache: {t} computed so far"))
    for col, cache in ((1, False), (2, True)):
        fig.add_trace(go.Heatmap(z=grid(t, cache), x=tokens, y=[f"step {s}" for s in range(1, n + 1)], zmin=0, zmax=2,
                                 colorscale=SCALE, showscale=False, xgap=4, ygap=4), 1, col)
        fig.update_yaxes(autorange="reversed", row=1, col=col, showticklabels=(col == 1))
        fig.update_xaxes(side="bottom", tickangle=-40, row=1, col=col)
    fig.update_layout(template="simple_white", width=1100, height=600, font=dict(FONT, size=18),
                      title=dict(text=f"Key and value vectors per decoder step &nbsp; <span style='color:{ORANGE}'>■ computed</span>"
                                      f" &nbsp; <span style='color:#9A9A9A'>■ reused from the cache</span>", x=0.5),
                      margin=dict(l=80, r=20, t=110, b=90), plot_bgcolor="white")
    fig.update_annotations(font_size=20)
    return fig


if __name__ == "__main__":
    tmp = HERE / ".kv_frames"
    tmp.mkdir(exist_ok=True)
    order = list(range(1, n + 1)) + [n] * 3                       # hold the last frame
    for i, t in enumerate(order):
        frame(t).write_image(tmp / f"{i:03d}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "1", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=900:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "kv_cache.gif")], check=True)
    keys = [Image.open(tmp / f"{k:03d}.png").convert("RGB") for k in (2, n - 1)]     # two frames, stacked
    w, h = keys[0].size
    sheet = Image.new("RGB", (w, 2 * h + 16), "white")
    for i, im in enumerate(keys):
        sheet.paste(im, (0, i * (h + 16)))
    sheet.save(HERE / "kv_cache_frames.png")
    shutil.rmtree(tmp)

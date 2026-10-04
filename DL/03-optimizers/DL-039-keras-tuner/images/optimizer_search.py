"""The random search of section 5, trial by trial: each trial builds a model with one optimizer, trains it for
10 epochs and records its validation accuracy; the best so far is highlighted. With only 4 values, a 5th trial
has nothing new to try (Plotly frames + ffmpeg). Run: python optimizer_search.py -> optimizer_search.gif, _frames.png"""
import shutil
import subprocess
from pathlib import Path

import plotly.graph_objects as go
from PIL import Image
from common import BLUE, GREEN, GREY, FONT

HERE = Path(__file__).parent
TRIALS = [("adam", 0.727), ("sgd", 0.740), ("adadelta", 0.338), ("rmsprop", 0.747)]   # trial 0..3, the Note's table
assert max(TRIALS, key=lambda t: t[1])[0] == "rmsprop"
assert len({o for o, _ in TRIALS}) == 4                                                  # every value tried once


def frame(k, final=False):
    shown = TRIALS[:k]
    best = max(range(k), key=lambda i: shown[i][1]) if k else None
    fig = go.Figure(go.Bar(x=[f"trial {i}<br>{o}" for i, (o, _) in enumerate(TRIALS)],
                           y=[a if i < k else 0 for i, (_, a) in enumerate(TRIALS)],
                           marker_color=[GREEN if i == best else (BLUE if i < k else "white") for i in range(4)],
                           text=[f"{a:.3f}" if i < k else "" for i, (_, a) in enumerate(TRIALS)],
                           textposition="outside", textfont=dict(size=24)))
    if final:
        msg = "trial 4: all 4 optimizers tried, search stops; best = rmsprop"
    elif k == 0:
        msg = "hp.Choice('optimizer', 4 values): search starts"
    else:
        msg = f"trial {k - 1}: build with {TRIALS[k - 1][0]}, train 10 epochs, score"
    fig.update_layout(template="simple_white", width=900, height=560, font=dict(FONT, size=22), showlegend=False,
                      title=dict(text=msg, x=0.5, font=dict(size=24)),
                      yaxis=dict(title="validation accuracy", range=[0, 0.9]), margin=dict(l=80, r=20, t=70, b=80))
    return fig


if __name__ == "__main__":
    tmp = HERE / ".opt_frames"
    tmp.mkdir(exist_ok=True)
    seq = [(0, False)] * 3 + [(k, False) for k in (1, 2, 3, 4) for _ in range(5)] + [(4, True)] * 12
    for j, (k, f) in enumerate(seq):
        frame(k, f).write_image(tmp / f"{j:03d}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "4", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=640:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "optimizer_search.gif")], check=True)
    keys = [Image.open(tmp / f"{j:03d}.png").convert("RGB") for j in (3, 8, 13, len(seq) - 1)]
    w, h = keys[0].size
    sheet = Image.new("RGB", (2 * w + 16, 2 * h + 16), "white")
    for i, im in enumerate(keys):
        sheet.paste(im, ((i % 2) * (w + 16), (i // 2) * (h + 16)))
    sheet.save(HERE / "optimizer_search_frames.png")
    shutil.rmtree(tmp)

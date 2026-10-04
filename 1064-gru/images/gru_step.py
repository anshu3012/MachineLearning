"""One GRU time step of section 8 (sentence 4 of the story), built up one vector per frame: reset gate, candidate,
update gate, then the new hidden state as old part + new part. Values are the Note's (and the Notebook's) numbers.
Run: python gru_step.py  -> gru_step.gif, gru_step_frames.png (Plotly frames + ffmpeg)"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from PIL import Image
from common import BLUE, ORANGE, RED, PURPLE

HERE = Path(__file__).parent
ASPECTS = ["power", "conflict", "tragedy", "revenge"]
h_prev, r = np.array([0.6, 0.6, 0.7, 0.1]), np.array([0.8, 0.2, 0.1, 0.9])
h_cand, z = np.array([0.7, 0.2, 0.1, 0.2]), np.array([0.1, 0.7, 0.8, 0.2])
old, new = (1 - z) * h_prev, z * h_cand
h = old + new
assert np.allclose(np.round(h, 2), [0.61, 0.32, 0.22, 0.12])                    # section 8.4

# (row, col, title, values, colour, is a gate) in the order they appear
PANELS = [(1, 1, "old memory h<sub>t-1</sub>", h_prev, RED, False),
          (1, 2, "× reset gate r<sub>t</sub>", r, PURPLE, True),
          (1, 3, "= reset memory", r * h_prev, PURPLE, False),
          (2, 1, "candidate h̃<sub>t</sub>", h_cand, BLUE, False),
          (2, 2, "× update gate z<sub>t</sub>", z, ORANGE, True),
          (2, 3, "= new part", new, BLUE, False),
          (3, 1, "old memory h<sub>t-1</sub>", h_prev, RED, False),
          (3, 2, "× (1 − z<sub>t</sub>)", 1 - z, ORANGE, True),
          (3, 3, "= old part", old, RED, False),
          (4, 1, "new memory h<sub>t</sub> = old part + new part", h, None, False)]
CAPTIONS = ["the memory after sentence 3",
            "reset gate: drop most conflict and tragedy",
            "only this part of the old memory is used",
            "a tanh layer builds the candidate (sentence 4)",
            "update gate: how much candidate to take in",
            "conflict and tragedy take most of the candidate",
            "the old memory again",
            "1 − z: how much old memory to keep",
            "power and revenge keep most of their old value",
            "each entry: a weighted average of old and new"]


def frame(k):
    """Figure with the first k panels filled."""
    fig = make_subplots(rows=4, cols=3, horizontal_spacing=0.07, vertical_spacing=0.1,
                        specs=[[{}, {}, {}]] * 3 + [[{"colspan": 3}, None, None]],
                        subplot_titles=[p[2] if n < k else "" for n, p in enumerate(PANELS)])
    for n, (row, col, _, v, colour, gate) in enumerate(PANELS):
        show = n < k
        if colour is None:                                          # h_t: old part (red) stacked with new part (blue)
            for part, pc, name in ((old, RED, "old part"), (new, BLUE, "new part")):
                fig.add_trace(go.Bar(x=ASPECTS, y=part if show else [0] * 4, marker_color=pc, name=name,
                                     showlegend=show), row=row, col=col)
            fig.add_trace(go.Scatter(x=ASPECTS, y=v + 0.12, mode="text", text=[f"{a:.2f}" for a in v] if show else None,
                                     textfont=dict(size=26), showlegend=False), row=row, col=col)
        else:
            fig.add_trace(go.Bar(x=ASPECTS, y=v if show else [0] * 4, marker_color=colour, showlegend=False,
                                 text=[f"{a:.2f}" for a in v] if show else None, textposition="outside",
                                 textfont=dict(size=22), cliponaxis=False), row=row, col=col)
        fig.update_yaxes(range=[0, 1.25], showticklabels=False, visible=show, row=row, col=col)
        fig.update_xaxes(tickfont=dict(size=19 if row < 4 else 24), visible=show, row=row, col=col)
    fig.update_layout(template="simple_white", width=1100, height=1250, barmode="stack",
                      font=dict(family="Latin Modern Roman", size=22), margin=dict(l=20, r=20, t=110, b=30),
                      title=dict(text=CAPTIONS[k - 1], x=0.5, y=0.975, font=dict(size=32)),
                      legend=dict(x=0.8, y=0.16, yanchor="top", font=dict(size=24)))
    fig.update_annotations(font=dict(family="Latin Modern Roman", size=25))
    return fig


if __name__ == "__main__":
    tmp = HERE / ".step_frames"
    tmp.mkdir(exist_ok=True)
    n = 0
    for k in range(1, len(PANELS) + 1):
        img = tmp / f"k{k}.png"
        frame(k).write_image(img)
        for _ in range(3 if k < len(PANELS) else 8):            # 1.5 s per panel at 2 fps, hold the last one 4 s
            shutil.copy(img, tmp / f"{n:03d}.png")
            n += 1
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "2", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=720:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "gru_step.gif")], check=True)
    # the build-up ends with every panel filled, so the last frame alone is the PDF figure
    Image.open(tmp / f"k{len(PANELS)}.png").convert("RGB").save(HERE / "gru_step_frames.png")
    shutil.rmtree(tmp)

"""One LSTM time step of section 8, built up one vector per frame: each row is "value x gate = result" for the
forget, input and output gates, with the Note's weights (2 units, input "mat"). Bars: unit 1 and unit 2.
Run: python lstm_step.py  -> lstm_step.gif, lstm_step_frames.png (Plotly frames + ffmpeg)"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from PIL import Image
from common import BLUE, ORANGE, GREEN, RED, GREY

HERE = Path(__file__).parent
sig = lambda a: 1 / (1 + np.exp(-a))
h_prev, c_prev, x = np.array([0.3, -0.2]), np.array([0.8, -0.5]), np.array([0, 1, 0])
W = {"f": [[0.5, 0], [0, 0.5], [1, 0], [2, -1], [0, 1]], "i": [[0.2, 0], [0, 0.2], [0.5, 0.5], [-1, 2], [0, 0]],
     "c": [[0.1, 0], [0, 0.1], [0.3, 0.3], [0.5, -1], [0, 0]], "o": [[0.3, 0], [0, 0.3], [0, 0], [1, 0.5], [0, 0]]}
z = {k: np.concatenate([h_prev, x]) @ np.array(w) for k, w in W.items()}       # all biases are 0
f, i, c_cand, o = sig(z["f"]), sig(z["i"]), np.tanh(z["c"]), sig(z["o"])
keep, add = f * c_prev, i * c_cand
c = keep + add
h = o * np.tanh(c)
assert np.allclose(c, [0.853, -0.800], atol=1e-3) and np.allclose(h, [0.518, -0.404], atol=1e-3)   # section 8

# (row, col, title, values, colour, is a gate) in the order they appear
PANELS = [(1, 1, "old cell state c<sub>t-1</sub>", c_prev, GREEN, False),
          (1, 2, "× forget gate f<sub>t</sub>", f, RED, True),
          (1, 3, "= what is kept", keep, GREEN, False),
          (2, 1, "candidate c̃<sub>t</sub>", c_cand, BLUE, False),
          (2, 2, "× input gate i<sub>t</sub>", i, BLUE, True),
          (2, 3, "= what is added", add, BLUE, False),
          (3, 1, "new cell state c<sub>t</sub>", c, GREEN, False),
          (3, 2, "× output gate o<sub>t</sub> (on tanh c<sub>t</sub>)", o, ORANGE, True),
          (3, 3, "= new hidden state h<sub>t</sub>", h, RED, False)]
CAPTIONS = ['the cell reads "mat" with this old memory',
            "forget gate: keep 90% of unit 1, 25% of unit 2",
            "unit 2 forgets most of its old value",
            "a tanh layer proposes new values",
            "input gate: let in 28% and 88% of them",
            "unit 2 takes in a strong negative value",
            "c<sub>t</sub> = kept + added",
            "output gate: how much of tanh(c<sub>t</sub>) to show",
            "h<sub>t</sub> goes to the next step and the output"]


def frame(k):
    """Figure with the first k panels filled."""
    fig = make_subplots(rows=3, cols=3, horizontal_spacing=0.08, vertical_spacing=0.13,
                        subplot_titles=[p[2] if n < k else "" for n, p in enumerate(PANELS)])
    for n, (r, col, _, v, colour, gate) in enumerate(PANELS):
        show = n < k
        if r == 3 and col == 1 and show:                       # c_t as two stacked parts: kept (green) + added (blue)
            for part, pc in ((keep, GREEN), (add, BLUE)):
                fig.add_trace(go.Bar(x=["unit 1", "unit 2"], y=part, marker_color=pc, opacity=0.85), row=r, col=col)
            fig.add_trace(go.Scatter(x=["unit 1", "unit 2"], y=v, mode="markers+text", text=[f"{a:.2f}" for a in v],
                                     textposition=["top center", "bottom center"], marker=dict(color="black", size=12,
                                     symbol="line-ew-open", line=dict(width=4)), textfont=dict(size=24)), row=r, col=col)
        else:
            fig.add_trace(go.Bar(x=["unit 1", "unit 2"], y=v if show else [0, 0], marker_color=colour,
                                 text=[f"{a:.2f}" for a in v] if show else None, textposition="outside",
                                 textfont=dict(size=24), cliponaxis=False), row=r, col=col)
        fig.update_yaxes(range=[0, 1.25] if gate else [-1.3, 1.3], showticklabels=False, zeroline=True,
                         zerolinecolor=GREY, visible=show, row=r, col=col)
        fig.update_xaxes(tickfont=dict(size=20), visible=show, row=r, col=col)
    fig.update_layout(template="simple_white", width=1100, height=1000, showlegend=False, barmode="relative",
                      font=dict(family="Latin Modern Roman", size=22), margin=dict(l=20, r=20, t=110, b=30),
                      title=dict(text=CAPTIONS[k - 1], x=0.5, y=0.97, font=dict(size=32)))
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
                    str(HERE / "lstm_step.gif")], check=True)
    # the build-up ends with every panel filled, so the last frame alone is the PDF figure
    Image.open(tmp / f"k{len(PANELS)}.png").convert("RGB").save(HERE / "lstm_step_frames.png")
    shutil.rmtree(tmp)

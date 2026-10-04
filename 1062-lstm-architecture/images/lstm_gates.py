"""The forget, input and output gates and the cell state of a trained 8-unit LSTM, word by word, on one real IMDB
test review (from the Notebook), with the prediction the model would make if the review ended at that word.
Run: python lstm_gates.py  -> lstm_gates.gif, lstm_gates_frames.png (Plotly frames + ffmpeg)"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from PIL import Image
from common import GREEN, GREY, FONT

HERE = Path(__file__).parent
g = pd.read_csv(HERE.parent / "data" / "gates_review.csv")
p = pd.read_csv(HERE.parent / "data" / "running_prediction.csv")
T, U = p.t.max(), g.unit.max()
words = p.word.tolist()
ROWS = [("f", "forget gate f<sub>t</sub>", "Reds", 0, 1), ("i", "input gate i<sub>t</sub>", "Blues", 0, 1),
        ("o", "output gate o<sub>t</sub>", "Oranges", 0, 1), ("c", "cell state c<sub>t</sub>", "RdBu", -0.6, 0.6)]


def grid(gate, k):
    """Units x words matrix, words after step k left empty."""
    m = g[g.gate == gate].pivot(index="unit", columns="t", values="value").to_numpy().copy()
    m[:, k:] = np.nan
    return m


def frame(k):
    fig = make_subplots(rows=5, cols=1, shared_xaxes=True, vertical_spacing=0.035,
                        subplot_titles=[r[1] for r in ROWS] + ["prediction if the review ended here"])
    for r, (gate, _, scale, lo, hi) in enumerate(ROWS, start=1):
        fig.add_trace(go.Heatmap(z=grid(gate, k), x=list(range(1, T + 1)), y=list(range(1, U + 1)), zmin=lo, zmax=hi,
                                 colorscale=scale, showscale=True, xgap=1, ygap=1,
                                 colorbar=dict(len=0.16, y=1 - (r - 0.5) * 0.2, thickness=12)), row=r, col=1)
        fig.update_yaxes(title_text="unit", tickvals=[1, 8], row=r, col=1)
        fig.add_vrect(x0=k - 0.5, x1=k + 0.5, line=dict(color="black", width=3), fillcolor="rgba(0,0,0,0)",
                      row=r, col=1)   # current word
    fig.add_trace(go.Scatter(x=p.t[:k], y=p.p[:k], mode="lines+markers", line=dict(color=GREEN, width=3),
                             marker=dict(size=7)), row=5, col=1)
    fig.add_hline(y=0.5, line=dict(color=GREY, dash="dot"), row=5, col=1)
    fig.update_yaxes(range=[0, 1], title_text="P(positive)", row=5, col=1)
    fig.update_xaxes(tickvals=list(range(1, T + 1)), ticktext=words, tickangle=-60, range=[0.5, T + 0.5], row=5, col=1)
    fig.update_layout(template="simple_white", width=1000, height=1150, font=dict(family=FONT["family"], size=20),
                      showlegend=False, title=dict(text=f'word {k}: "{words[k - 1]}"', x=0.5, y=0.985,
                                                   font=dict(size=34)),
                      margin=dict(l=80, r=40, t=90, b=120))
    fig.update_annotations(font=dict(family=FONT["family"], size=24))
    return fig


if __name__ == "__main__":
    tmp = HERE / ".gate_frames"
    tmp.mkdir(exist_ok=True)
    for k in range(1, T + 1):
        frame(k).write_image(tmp / f"{k:03d}.png")
    for k in range(T + 1, T + 9):                              # hold the last frame
        shutil.copy(tmp / f"{T:03d}.png", tmp / f"{k:03d}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "2", "-start_number", "1", "-i",
                    str(tmp / "%03d.png"), "-vf",
                    "scale=760:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "lstm_gates.gif")], check=True)
    keys = [Image.open(tmp / f"{k:03d}.png").convert("RGB") for k in (3, 8, 20, T)]
    w, h = keys[0].size
    sheet = Image.new("RGB", (2 * w + 16, 2 * h + 16), "white")
    for n, im in enumerate(keys):
        sheet.paste(im, ((n % 2) * (w + 16), (n // 2) * (h + 16)))
    sheet.save(HERE / "lstm_gates_frames.png")
    shutil.rmtree(tmp)

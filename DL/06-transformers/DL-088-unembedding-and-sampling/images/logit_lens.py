"""Logit lens (nostalgebraist 2020) on GPT-2 small, "Steve Jobs was the founder of": the residual stream of the
last token after each block, put through the final LayerNorm and the unembedding. Bars: the 8 most likely
next tokens at that depth; " Apple" in orange. Data: data/logit_lens_last.csv (Notebook).
Run: python logit_lens.py -> logit_lens.gif, logit_lens_frames.png (Plotly frames + ffmpeg)"""
import shutil
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
from PIL import Image

from common import ORANGE, GREY, FONT, DATA, gif, grid

HERE = Path(__file__).parent
d = pd.read_csv(DATA / "logit_lens_last.csv", keep_default_na=False)


def frame(l):
    r = d.iloc[l]
    toks = [str(r[f"tok{j}"]).strip() or repr(r[f"tok{j}"]) for j in range(8)][::-1]
    ps = [r[f"p{j}"] for j in range(8)][::-1]
    fig = go.Figure(go.Bar(y=[f"{t} " for t in toks], x=ps, orientation="h", text=[f"{p:.2f}" for p in ps],
                           textposition="outside", marker_color=[ORANGE if t == "Apple" else GREY for t in toks]))
    where = "token + position vector only" if l == 0 else f"after block {l} of 12"
    fig.update_layout(template="simple_white", width=860, height=560, font=FONT,
                      title=dict(text=f"Next-token guess read from the stream: {where}", x=0.5, font=dict(size=22)),
                      xaxis=dict(range=[0, 1.08], title="probability"), yaxis=dict(tickfont=dict(size=21)),
                      margin=dict(l=150, r=30, t=70, b=60))
    fig.add_annotation(x=1.06, y=0.02, xref="x", yref="paper", xanchor="right", showarrow=False, align="right",
                       text=f"<b>Apple</b>: rank {int(r.apple_rank):,}, probability {r.apple_prob:.3f}",
                       font=dict(size=20, color=ORANGE), bgcolor="rgba(255,255,255,0.9)")
    return fig


if __name__ == "__main__":
    tmp = HERE / ".lens_frames"
    tmp.mkdir(exist_ok=True)
    k = 0
    for l in range(13):
        frame(l).write_image(tmp / f"{k:03d}.png")
        for _ in range(3 if l < 12 else 8):                       # hold each layer; longer on the last
            k += 1
            shutil.copy(tmp / f"{k-1:03d}.png", tmp / f"{k:03d}.png")
        k += 1
    gif(tmp / "%03d.png", HERE / "logit_lens.gif", fps=3, framerate=3, width=760)
    grid([Image.open(tmp / f"{4 * l:03d}.png") for l in (0, 8, 9, 11)], HERE / "logit_lens_frames.png")
    shutil.rmtree(tmp)

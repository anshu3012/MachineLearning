"""The trained transformer translating "i think you're right ." one step per frame (Plotly frames + ffmpeg):
left, the 5 most likely next words (chosen word in orange); right, the cross-attention weights of the last decoder
block for the position being predicted (mean of 4 heads). Data: data/decode_steps.csv, data/decode_cross.csv.
Run: python decode_anim.py -> decode_anim.gif, decode_anim_frames.png"""
import shutil
import subprocess
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from PIL import Image
from common import BLUE, ORANGE, GREY, FONT

HERE = Path(__file__).parent
SENT = "i think you're right ."
steps = pd.read_csv(HERE.parent / "data" / "decode_steps.csv")
cross = pd.read_csv(HERE.parent / "data" / "decode_cross.csv")
steps, cross = steps[steps.sentence == SENT], cross[cross.sentence == SENT]
n = steps.step.max()
chosen = [steps[(steps.step == t) & (steps["rank"] == 1)].word.iloc[0] for t in range(1, n + 1)]
english = SENT.split()


def frame(t):
    s = steps[steps.step == t].sort_values("rank", ascending=False)
    c = cross[cross.step == t]
    fig = make_subplots(1, 2, column_widths=[0.5, 0.5], horizontal_spacing=0.16,
                        subplot_titles=("5 most likely next words", "cross-attention: which English word it reads"))
    fig.add_trace(go.Bar(x=s.prob, y=s.word, orientation="h", marker_color=[ORANGE if r == 1 else GREY for r in s["rank"]],
                         text=[f"{p:.3f}" for p in s.prob], textposition="outside"), 1, 1)
    fig.add_trace(go.Bar(x=c.english, y=c.weight, marker_color=BLUE, text=[f"{w:.2f}" for w in c.weight],
                         textposition="outside"), 1, 2)
    inp = "&lt;start&gt; " + " ".join(chosen[:t - 1])
    fig.update_layout(template="simple_white", width=1100, height=520, font=FONT, showlegend=False,
                      title=dict(text=f"step {t}:  decoder input <b>{inp}</b>  →  next word <b>{chosen[t - 1].replace('<', '&lt;').replace('>', '&gt;')}</b>"
                                 f"<br>English: {SENT}", x=0.02, y=0.96),
                      margin=dict(l=90, r=30, t=130, b=60))
    fig.update_xaxes(range=[0, 1.25], title="probability", row=1, col=1)
    fig.update_yaxes(range=[0, 1.15], title="weight", row=1, col=2)
    fig.update_yaxes(tickfont=dict(size=17), row=1, col=1)
    return fig


if __name__ == "__main__":
    tmp = HERE / ".decode_frames"
    tmp.mkdir(exist_ok=True)
    for t in range(1, n + 1):
        frame(t).write_image(tmp / f"{t:03d}.png")
    for k in range(n + 1, n + 4):                                 # hold the last frame
        shutil.copy(tmp / f"{n:03d}.png", tmp / f"{k:03d}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "1", "-start_number", "1", "-i", str(tmp / "%03d.png"),
                    "-vf", "scale=900:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "decode_anim.gif")], check=True)
    keys = [Image.open(tmp / f"{k:03d}.png").convert("RGB") for k in (4, 6)]   # two frames, stacked: readable in the PDF
    w, h = keys[0].size
    sheet = Image.new("RGB", (w, 2 * h + 16), "white")
    for i, im in enumerate(keys):
        sheet.paste(im, (0, i * (h + 16)))
    sheet.save(HERE / "decode_anim_frames.png")
    shutil.rmtree(tmp)

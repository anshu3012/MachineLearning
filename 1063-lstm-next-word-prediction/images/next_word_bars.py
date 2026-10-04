"""A test sentence typed word by word into the trained LSTM (seed 0): after each prefix, the model's five most likely
next words, then the real next word is revealed (green if it is among the five). Data: data/typing.csv (Notebook).
Run: python next_word_bars.py  -> next_word_bars.gif, next_word_bars_frames.png (Plotly frames + ffmpeg)"""
import shutil
import subprocess
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
from PIL import Image
from common import BLUE, GREEN, GREY

HERE = Path(__file__).parent
d = pd.read_csv(HERE.parent / "data" / "typing.csv")
STEPS = sorted(d.step.unique())
PMAX = d.p.max() * 1.25


def frame(step, reveal):
    s = d[d.step == step].sort_values("rank")
    nxt, rank, p_next = s.next_word.iloc[0], int(s.next_rank.iloc[0]), s.next_p.iloc[0]
    hit = reveal and rank <= 5
    colours = [GREEN if hit and w == nxt else BLUE for w in s.word]
    fig = go.Figure(go.Bar(x=s.p, y=s.word, orientation="h", marker_color=colours,
                           text=[f"{p:.2f}" for p in s.p], textposition="outside", textfont=dict(size=30),
                           cliponaxis=False))
    typed = s.prefix.iloc[0]
    shown = f"{typed} <b><span style='color:{GREEN}'>{nxt}</span></b>" if reveal else f"{typed} ___"
    fig.update_layout(template="simple_white", width=1000, height=640, showlegend=False,
                      font=dict(family="Latin Modern Roman", size=30),
                      title=dict(text=shown, x=0.5, y=0.95, font=dict(size=40)),
                      xaxis=dict(title="probability of the next word", range=[0, PMAX]),
                      yaxis=dict(autorange="reversed", tickfont=dict(size=34)),
                      margin=dict(l=170, r=40, t=110, b=170))
    if reveal:
        msg = (f'real next word "{nxt}": guess number {rank}' if rank > 1 else f'real next word "{nxt}": top guess')
        if rank > 5:
            msg += f", probability {p_next:.4f}"
        fig.add_annotation(text=msg, x=0.5, y=-0.42, xref="paper", yref="paper", showarrow=False,
                           font=dict(size=30, color=GREEN if rank <= 5 else GREY))
    else:
        fig.add_annotation(text="the model's five best guesses", x=0.5, y=-0.42, xref="paper", yref="paper",
                           showarrow=False, font=dict(size=30, color=GREY))
    return fig


if __name__ == "__main__":
    tmp = HERE / ".typing_frames"
    tmp.mkdir(exist_ok=True)
    n, keys = 0, {}
    for step in STEPS:
        for reveal, hold in ((False, 3), (True, 4 if step < STEPS[-1] else 8)):   # 2 fps: 1.5 s guess, 2 s reveal
            img = tmp / f"s{step}_{int(reveal)}.png"
            frame(step, reveal).write_image(img)
            keys[(step, reveal)] = img
            for _ in range(hold):
                shutil.copy(img, tmp / f"{n:03d}.png")
                n += 1
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "2", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=720:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "next_word_bars.gif")], check=True)
    picks = [Image.open(keys[k]).convert("RGB") for k in ((1, True), (2, True), (3, True), (6, True))]
    w, h = picks[0].size
    sheet = Image.new("RGB", (2 * w + 16, 2 * h + 16), "white")
    for m, im in enumerate(picks):
        sheet.paste(im, ((m % 2) * (w + 16), (m // 2) * (h + 16)))
    sheet.save(HERE / "next_word_bars_frames.png")
    shutil.rmtree(tmp)

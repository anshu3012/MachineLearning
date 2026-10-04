"""The trained encoder-decoder translating one test sentence, one decoder step per frame: the five most likely
French words at that step (from the Notebook), the chosen word in orange, and the translation so far.
Run: python greedy_decoding.py  -> greedy_decoding.gif, greedy_decoding_frames.png (Plotly frames + ffmpeg)"""
import shutil
import subprocess
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
from PIL import Image
from common import BLUE, ORANGE, GREY, FONT

HERE = Path(__file__).parent
d = pd.read_csv(HERE.parent / "data" / "decode_steps.csv", keep_default_na=False)
SOURCE = "i think you're right ."
T = d.step.max()
chosen = [d[(d.step == t) & (d["rank"] == 1)].word.item() for t in range(1, T + 1)]


def frame(k):
    s = d[d.step == k].sort_values("prob")
    fed = "<start>" if k == 1 else chosen[k - 2]
    fig = go.Figure(go.Bar(x=s.prob, y=s.word, orientation="h", text=[f"{p:.2f}" for p in s.prob], textposition="outside",
                           marker_color=[ORANGE if r == 1 else BLUE for r in s["rank"]]))
    so_far = " ".join(w for w in chosen[:k] if w != "<end>")
    fig.update_layout(template="simple_white", width=900, height=520, font=FONT, showlegend=False,
                      title=dict(text=f"English: <b>{SOURCE}</b><br>step {k}: input <b>{fed.replace('<', '&lt;')}</b>"
                                      f" → most likely <b>{chosen[k - 1].replace('<', '&lt;')}</b><br>French so far: <b>{so_far}</b>",
                                 x=0.02, y=0.95),
                      xaxis=dict(title="probability from the softmax layer", range=[0, 1.12]),
                      yaxis=dict(tickfont=dict(size=18)), margin=dict(l=110, r=30, t=150, b=60))
    return fig


if __name__ == "__main__":
    tmp = HERE / ".greedy_frames"
    tmp.mkdir(exist_ok=True)
    for k in range(1, T + 1):
        frame(k).write_image(tmp / f"{k:03d}.png")
    for k in range(T + 1, T + 5):                              # hold the last frame
        shutil.copy(tmp / f"{T:03d}.png", tmp / f"{k:03d}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "1", "-start_number", "1", "-i",
                    str(tmp / "%03d.png"), "-vf", "scale=760:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "greedy_decoding.gif")], check=True)
    keys = [1, 2, (T + 1) // 2 + 1, T]
    ims = [Image.open(tmp / f"{k:03d}.png").convert("RGB") for k in keys]
    w, h = ims[0].size
    sheet = Image.new("RGB", (2 * w + 16, 2 * h + 16), "white")
    for n, im in enumerate(ims):
        sheet.paste(im, ((n % 2) * (w + 16), (n // 2) * (h + 16)))
    sheet.save(HERE / "greedy_decoding_frames.png")
    shutil.rmtree(tmp)

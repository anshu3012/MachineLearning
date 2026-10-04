"""Section 6: Bayes' theorem as areas in a unit square, on the five-passenger data. The square holds every
possibility. Left strip: died, width P(died) = 3/5; right strip: survived, width 2/5. Shade the male part of each
strip: height P(male | died) = 2/3 on the left, P(male | survived) = 1/2 on the right. Learning "male" keeps only the
shaded areas, 2/5 and 1/5; the left one's share is P(died | male) = (2/5) / (3/5) = 2/3.
Run: python bayes_square.py  -> bayes_square.gif, bayes_square_frames.png (Plotly frames + ffmpeg)"""
import shutil
import subprocess
from fractions import Fraction as F
from pathlib import Path

import plotly.graph_objects as go
from PIL import Image

HERE = Path(__file__).parent
RED, BLUE, GREY = "#E45756", "#4C78A8", "#EEEEEE"
PRIOR, L_D, L_S = F(3, 5), F(2, 3), F(1, 2)
A_D, A_S = PRIOR * L_D, (1 - PRIOR) * L_S
assert (A_D, A_S, A_D / (A_D + A_S)) == (F(2, 5), F(1, 5), F(2, 3))
p, ld, ls = float(PRIOR), float(L_D), float(L_S)
TITLES = ["All five passengers: a square of area 1", "Split by the prior: died 3/5, survived 2/5",
          "Shade the males: 2/3 of the died strip, 1/2 of the survived strip",
          "We learn: the new passenger is male", "P(died | male) = (2/5) / (2/5 + 1/5) = 2/3"]


def frame(step):
    fig = go.Figure()
    def rect(x0, x1, y0, y1, colour, opacity=1.0):
        fig.add_shape(type="rect", x0=x0, x1=x1, y0=y0, y1=y1, fillcolor=colour, opacity=opacity,
                      line=dict(color="black", width=2), layer="below")
    rect(0, 1, 0, 1, "white")
    note = ""
    if step >= 1:
        rect(0, p, 0, 1, "rgba(228,87,86,0.12)")
        rect(p, 1, 0, 1, "rgba(76,120,168,0.12)")
        fig.add_annotation(x=p / 2, y=-0.07, text="died: 3/5", showarrow=False, font=dict(color=RED))
        fig.add_annotation(x=(1 + p) / 2, y=-0.07, text="survived: 2/5", showarrow=False, font=dict(color=BLUE))
    if step >= 2:
        fade = 0.15 if step >= 3 else 1.0
        rect(0, p, ld, 1, "white" if step < 3 else GREY, 1.0)
        rect(p, 1, ls, 1, "white" if step < 3 else GREY, 1.0)
        rect(0, p, 0, ld, RED, 0.75)
        rect(p, 1, 0, ls, BLUE, 0.75)
        fig.add_annotation(x=p / 2, y=ld / 2, text="male<br>and died<br>3/5 × 2/3<br>= <b>2/5</b>", showarrow=False,
                           font=dict(color="white", size=24))
        fig.add_annotation(x=(1 + p) / 2, y=ls / 2, text="male and<br>survived<br>2/5 × 1/2<br>= <b>1/5</b>",
                           showarrow=False, font=dict(color="white", size=22))
        if step == 2:
            fig.add_annotation(x=p / 2, y=(1 + ld) / 2, text="female", showarrow=False, font=dict(color=RED))
            fig.add_annotation(x=(1 + p) / 2, y=(1 + ls) / 2, text="female", showarrow=False, font=dict(color=BLUE))
        _ = fade
    if step == 3:
        note = "only the shaded<br>areas are still<br>possible"
    if step == 4:
        note = ("red share of<br>the shaded area:<br><b>2/3</b><br><br>blue share:<br><b>1/3</b>"
                "<br><br>predict: <b>died</b>")
    if note:
        fig.add_annotation(x=1.08, y=0.5, xanchor="left", text=note, showarrow=False, align="left",
                           font=dict(size=26))
    fig.update_layout(template="simple_white", width=1000, height=640, showlegend=False,
                      font=dict(family="Latin Modern Roman", size=26), title=dict(text=TITLES[step], x=0.5, y=0.97,
                                                                                 font=dict(size=24)),
                      xaxis=dict(visible=False, range=[-0.05, 1.6], scaleanchor="y"),
                      yaxis=dict(visible=False, range=[-0.15, 1.05]), margin=dict(l=10, r=10, t=60, b=10))
    return fig


PLAN = [(0, 4), (1, 8), (2, 10), (3, 8), (4, 14)]

if __name__ == "__main__":
    tmp = HERE / ".bayes_frames"
    tmp.mkdir(exist_ok=True)
    n, keys = 0, {}
    for step, hold in PLAN:
        frame(step).write_image(tmp / f"{n:03d}.png")
        keys[step] = n
        for _ in range(hold - 1):
            shutil.copy(tmp / f"{n:03d}.png", tmp / f"{n + 1:03d}.png")
            n += 1
        n += 1
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "3", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=700:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "bayes_square.gif")], check=True)
    ims = [Image.open(tmp / f"{keys[k]:03d}.png").convert("RGB") for k in (1, 2, 3, 4)]
    w, h = ims[0].size
    sheet = Image.new("RGB", (2 * w + 16, 2 * h + 16), "white")
    for i, im in enumerate(ims):
        sheet.paste(im, ((i % 2) * (w + 16), (i // 2) * (h + 16)))
    sheet.save(HERE / "bayes_square_frames.png")
    shutil.rmtree(tmp)

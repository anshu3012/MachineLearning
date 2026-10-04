"""Naive Bayes on Play Tennis, one factor at a time (Plotly). Each row is the yes/no share after multiplying in one
more looked-up probability: prior, then outlook, temperature, humidity, wind (shares = scores divided by their sum).
belief_sunny.gif (section 5): sunny, hot, high, weak -> 79.5% no.
belief_overcast.gif (section 6): overcast, cool, normal, weak -> P(overcast | no) = 0 wipes out "no" for good.
smoothing.png (section 7): the overcast day without and with Laplace smoothing (add 1 to every count)."""
import shutil
from fractions import Fraction
import subprocess
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

HERE = Path(__file__).parent
df = pd.read_csv(HERE.parent / "data" / "play_tennis.csv")
cols = ["outlook", "temperature", "humidity", "wind"]
n = df["play"].value_counts()
BLUE, RED = "#4C78A8", "#E45756"
FONT = dict(family="Latin Modern Roman", size=22)
SUNNY = dict(outlook="Sunny", temperature="Hot", humidity="High", wind="Weak")
OVERCAST = dict(outlook="Overcast", temperature="Cool", humidity="Normal", wind="Weak")


def steps(day, alpha=0):
    """Rows of (label, factor yes, factor no, score yes, score no) as each factor is multiplied in."""
    s = {c: n[c] / len(df) for c in ("Yes", "No")}
    rows = [("prior", s["Yes"], s["No"], s["Yes"], s["No"])]
    for col, v in day.items():
        k = df[col].nunique()
        f = {c: ((df[col][df.play == c] == v).sum() + alpha) / (n[c] + alpha * k) for c in ("Yes", "No")}
        s = {c: s[c] * f[c] for c in s}
        rows.append((f"× {v.lower()}", f["Yes"], f["No"], s["Yes"], s["No"]))
    return rows


def share_no(rows):
    return rows[-1][4] / (rows[-1][3] + rows[-1][4])


S, O, Os, Ss = steps(SUNNY), steps(OVERCAST), steps(OVERCAST, 1), steps(SUNNY, 1)
assert round(S[-1][3], 4) == 0.0071 and round(S[-1][4], 4) == 0.0274 and round(share_no(S), 3) == 0.795
assert O[1][2] == 0 and share_no(O) == 0                       # P(overcast | no) = 0/5: "no" is gone for good
assert O[1][2] == 0 and abs(Os[1][2] - 0.125) < 1e-12          # smoothed: (0 + 1) / (5 + 3)
assert round(share_no(Ss), 3) == 0.688 and round(1 - share_no(Os), 3) == 0.964


def frac(x):
    f = Fraction(x).limit_denominator(20)                      # counts over class sizes, as in the Note's formulas
    return f"{f.numerator}/{f.denominator}" if f else "0"


def add(fig, rows, k, col=1):
    """Draw the first k+1 rows of one run as 100% bars (top row = prior)."""
    for i, (lab, fy, fn, sy, sn) in enumerate(rows[:k + 1]):
        tot = sy + sn
        py = sy / tot
        y = f"{lab}" if i == 0 else f"{lab}  ({frac(fy)} vs {frac(fn)})"
        for share, c, name in ((py, BLUE, "yes"), (1 - py, RED, "no")):
            fig.add_trace(go.Bar(y=[y], x=[share], orientation="h", marker_color=c, name=name,
                                 showlegend=(i == 0 and col == 1), text=[f"{share:.1%}" if share > 0.15 else ""], textangle=0,
                                 textposition="inside", insidetextanchor="middle",
                                 textfont=dict(color="white", size=22)), 1, col)
    labels = [(r[0] if i == 0 else f"{r[0]}  ({frac(r[1])} vs {frac(r[2])})") for i, r in enumerate(rows)]
    fig.update_yaxes(categoryorder="array", categoryarray=labels[::-1], range=[len(rows) - 0.5, -0.5],
                     autorange=False, row=1, col=col)
    fig.update_yaxes(categoryarray=labels, row=1, col=col)
    fig.update_xaxes(range=[0, 1], tickformat=".0%", row=1, col=col)


def frame(rows, k, title):
    fig = make_subplots(rows=1, cols=1)
    add(fig, rows, k)
    fig.update_layout(template="simple_white", barmode="stack", width=1000, height=520, font=FONT,
                      title=dict(text=title, x=0.5, y=0.96), margin=dict(l=20, r=30, t=90, b=60),
                      legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.12, traceorder="normal"))
    return fig


def gif(rows, name, title):
    tmp = HERE / f".{name}_frames"
    tmp.mkdir(exist_ok=True)
    last = len(rows) - 1
    for k in range(last + 1):
        frame(rows, k, title).write_image(tmp / f"{k:03d}.png")
    for k in range(last + 1, last + 4):                       # hold the last frame
        shutil.copy(tmp / f"{last:03d}.png", tmp / f"{k:03d}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "0.8", "-i", str(tmp / "%03d.png"), "-vf",
                    "fps=10,scale=800:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / f"{name}.gif")], check=True)
    shutil.copy(tmp / f"{last:03d}.png", HERE / f"{name}_frames.png")   # the full build-up is in the last frame
    shutil.rmtree(tmp)


if __name__ == "__main__":
    gif(S, "belief_sunny", "Sunny, hot, high, weak: share of yes and no")
    gif(O, "belief_overcast", "Overcast, cool, normal, weak: no smoothing")
    fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.32,
                        subplot_titles=("without smoothing", "with Laplace smoothing (add 1)"))
    add(fig, O, len(O) - 1, 1)
    add(fig, Os, len(Os) - 1, 2)
    fig.update_layout(template="simple_white", barmode="stack", width=1300, height=520, font=FONT,
                      margin=dict(l=20, r=30, t=70, b=60),
                      legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.12, traceorder="normal"))
    fig.update_annotations(font_size=24)
    fig.write_image(HERE / "smoothing.png", scale=2)

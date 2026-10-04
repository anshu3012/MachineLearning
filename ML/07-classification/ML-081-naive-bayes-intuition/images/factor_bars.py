"""Naive Bayes scoring the new match (lost, Mumbai, sunny) on the 8-match table (section 8).
One bar chart per class: how many of the class's matches had each feature value. The three bars of the new
match light up one by one, and the running product (starting at the prior) grows a factor at a time:
win 5/8 x 1/5 x 2/5 x 4/5 = 0.040, loss 3/8 x 2/3 x 2/3 x 1/3 = 0.056.
Idea after StatQuest, "Naive Bayes, Clearly Explained!!!" (one histogram per class); data and code are ours.
Run: python factor_bars.py -> factor_bars.gif, factor_bars_frames.png (Plotly frames + ffmpeg)"""
from fractions import Fraction as F
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from spam_words import save

HERE = Path(__file__).parent
df = pd.read_csv(HERE.parent / "data" / "matches.csv")
q = dict(toss="lost", venue="Mumbai", outlook="sunny")
BARS = [(f, v) for f in q for v in sorted(df[f].unique(), key=lambda v: v != q[f])]   # the new match's value first
COLOR = {"win": "#54A24B", "loss": "#E45756"}
FONT = dict(family="Latin Modern Roman", size=24, color="black")
n = {c: int((df.result == c).sum()) for c in COLOR}
count = {c: [int(((df.result == c) & (df[f] == v)).sum()) for f, v in BARS] for c in COLOR}
factors = {c: [F(n[c], len(df))] + [F(count[c][BARS.index((f, q[f]))], n[c]) for f in q] for c in COLOR}
score = {c: float(factors[c][0] * factors[c][1] * factors[c][2] * factors[c][3]) for c in COLOR}
assert round(score["win"], 3) == 0.040 and round(score["loss"], 3) == 0.056        # section 8


def frac(x, d):
    return f"{x.numerator * (d // x.denominator)}/{d}"       # keep the class total as the denominator


def frame(k, title, verdict=""):
    """k: how many of the new match's features have been multiplied in (0 = prior only)."""
    lit = [(f, q[f]) for f in list(q)[:k]]
    fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.07,
                        subplot_titles=[f"<b>{c}</b>: {n[c]} of 8 matches" for c in COLOR])
    fig.update_annotations(font_size=26)
    for j, c in enumerate(COLOR):
        op = [1 if b in lit else 0.25 for b in BARS]
        fig.add_trace(go.Bar(x=[f"{v}" for f, v in BARS], y=count[c], marker=dict(color=COLOR[c], opacity=op),
                             text=[f"{m}/{n[c]}" for m in count[c]], textposition="outside", cliponaxis=False),
                      1, j + 1)
        parts = [f"{n[c]}/8"] + [frac(x, n[c]) for x in factors[c][1:k + 1]]
        line = "prior " + " × ".join(parts)
        if k == 3:
            line += f" = <b>{score[c]:.3f}</b>"
        fig.add_annotation(xref=f"x{j + 1 if j else ''} domain", yref="paper", x=0.5, y=-0.42, showarrow=False,
                           text=line, font=dict(size=27, color=COLOR[c]))
        for x0, name in [(0.5, "toss"), (2.5, "venue"), (5, "outlook")]:
            fig.add_annotation(x=x0, y=-0.23, xref=f"x{j + 1 if j else ''}", yref="paper", text=f"<i>{name}</i>",
                               showarrow=False, font=dict(size=22))
    if verdict:
        fig.add_annotation(xref="paper", yref="paper", x=0.5, y=-0.62, showarrow=False, text=f"<b>{verdict}</b>",
                           font=dict(size=28))
    fig.update_yaxes(range=[0, 5.8], dtick=1, title="matches", title_font_size=22)
    fig.update_yaxes(title="", row=1, col=2)
    fig.update_xaxes(tickfont_size=19)
    fig.update_layout(width=1300, height=720, font=FONT, template="simple_white", showlegend=False,
                      title=dict(text=f"<b>{title}</b>", x=0.5, y=0.97, font_size=30),
                      margin=dict(l=70, r=20, t=120, b=250))
    return fig


if __name__ == "__main__":
    save("factor_bars", [
        (frame(0, "New match: lost, Mumbai, sunny. Start from the prior"), 4),
        (frame(1, "1. Toss lost: multiply by its share within the class"), 4),
        (frame(2, "2. Venue Mumbai: multiply again"), 4),
        (frame(3, "3. Outlook sunny: multiply again", "0.056 > 0.040: predict loss"), 7)])

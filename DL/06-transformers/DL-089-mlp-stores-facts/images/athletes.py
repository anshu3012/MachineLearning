"""Section 6: GPT-2 small asked "<athlete> plays the sport of": the probability of each athlete's true sport as the
next token, and whether it is the top token. From data/athletes.csv (the Notebook).
Run: python athletes.py  -> athletes.png (Plotly horizontal bars)"""
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go

HERE = Path(__file__).parent
BLUE, RED = "#4C78A8", "#E45756"
a = pd.read_csv(HERE.parent / "data" / "athletes.csv")
assert len(a) == 19 and a.correct_top1.sum() == 18 and list(a.athlete[~a.correct_top1]) == ["Phil Mickelson"]
assert round(a.set_index("athlete").loc["Michael Jordan", "p_true"], 3) == 0.135
a = a.sort_values("p_true")
fig = go.Figure(go.Bar(y=[f"{n} ({s})" for n, s in zip(a.athlete, a.true)], x=a.p_true, orientation="h",
                       marker_color=[BLUE if c else RED for c in a.correct_top1],
                       text=[f"{p:.2f}" + ("" if c else f"  (top: {t})") for p, c, t in zip(a.p_true, a.correct_top1, a.top1)],
                       textposition="outside"))
fig.update_layout(template="simple_white", width=1000, height=820, font=dict(family="Latin Modern Roman", size=20),
                  xaxis=dict(title="probability of the true sport as the next token", range=[0, 0.75]),
                  margin=dict(l=20, r=30, t=30, b=60))

if __name__ == "__main__":
    fig.write_image(HERE / "athletes.png", scale=2)

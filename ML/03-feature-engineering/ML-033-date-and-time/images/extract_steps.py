"""Extracting date parts with the .dt accessor, one new feature per step, on the first five orders: year, month name,
day, weekday name, weekend flag, ISO week, quarter and semester. Values asserted against the Note's tables.
Plotly table frames -> GIF."""
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go
from anim import save_gif, FONT

here = Path(__file__).parent
d = pd.to_datetime(pd.read_csv(here.parent / "data" / "orders.csv")["date"]).head(5)
cols = [("year", d.dt.year), ("month", d.dt.month_name()), ("day", d.dt.day), ("weekday", d.dt.day_name()),
        ("weekend", (d.dt.dayofweek >= 5).astype(int)), ("week", d.dt.isocalendar().week.astype(int)),
        ("quarter", d.dt.quarter), ("semester", (d.dt.quarter > 2).astype(int) + 1)]
assert cols[5][1].tolist() == [50, 33, 43, 33, 1] and cols[4][1].tolist() == [0, 0, 0, 1, 1]
assert cols[7][1].tolist() == [2, 2, 2, 2, 1] and cols[3][1].tolist()[0] == "Tuesday"
CODE = ["d.dt.year", "d.dt.month_name()", "d.dt.day", "d.dt.day_name()", "d.dt.dayofweek >= 5",
        "d.dt.isocalendar().week", "d.dt.quarter", "quarter > 2, plus 1"]


def frame(k):
    heads = ["date"] + [c for c, _ in cols[:k]]
    vals = [d.dt.strftime("%Y-%m-%d")] + [v for _, v in cols[:k]]
    fills = [["#eef3f9"] * 5] + [["#ffe2c4" if j == k - 1 else "white"] * 5 for j in range(k)]
    fig = go.Figure(go.Table(header=dict(values=heads, fill_color="#4C78A8", font=dict(color="white", size=19), height=40),
                             cells=dict(values=vals, fill_color=fills, font=dict(size=19), height=38)))
    head = "Five order dates" if k == 0 else f"Step {k}: <b>{cols[k - 1][0]}</b> from <span style='font-family:monospace'>{CODE[k - 1]}</span>"
    fig.update_layout(width=1400, height=340, font=FONT, title=dict(text=head, x=0.5, y=0.92), margin=dict(l=10, r=10, t=70, b=0))
    return fig


if __name__ == "__main__":
    save_gif([frame(k) for k in range(9)], "extract_steps", here, keys=[3, 8], fps=1, holds=[3] + [2] * 7 + [6], cols=1,
             width=1000)

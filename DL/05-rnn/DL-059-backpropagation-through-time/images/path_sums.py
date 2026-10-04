"""Sections 6.3 and 7: the gradient of a shared weight is a sum of one term per time step.
Waterfalls of the three path terms for w_i and w_h in the one-node example (data/worked_example.csv, the Notebook).
Run: python path_sums.py  -> path_sums.png (Plotly: a chart of numbers adding up)"""
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from common import BLUE, GREEN, GREY, ORANGE, PURPLE, RED

HERE = Path(__file__).parent
v = pd.read_csv(HERE.parent / "data" / "worked_example.csv").set_index("quantity")["value"]
terms = {w: [round(float(v[f"dL/d{w} term t={t}"]), 3) for t in (3, 2, 1)] for w in ("w_i", "w_h")}
total = {w: round(float(v[f"dL/d{w}"]), 3) for w in ("w_i", "w_h")}
assert terms == {"w_i": [-0.196, 0.0, -0.086], "w_h": [-0.069, -0.063, 0.0]}      # the Note's numbers
assert total == {"w_i": -0.282, "w_h": -0.132}
why_zero = {"w_i": "x<sub>2</sub> = 0", "w_h": "h<sub>0</sub> = 0"}

fig = make_subplots(1, 2, subplot_titles=["∂L/∂w<sub>i</sub>: last factor uses x<sub>t</sub>",
                                          "∂L/∂w<sub>h</sub>: last factor uses h<sub>t−1</sub>"], horizontal_spacing=0.1)
for c, w in enumerate(("w_i", "w_h"), start=1):
    ys = terms[w] + [total[w]]
    text = [f"{y:+.3f}" if y else f"0<br>({why_zero[w] if (w == 'w_i' and k == 1) or (w == 'w_h' and k == 2) else ''})"
            for k, y in enumerate(ys)]
    fig.add_trace(go.Waterfall(x=["path 1<br>(t = 3)", "path 2<br>(t = 2)", "path 3<br>(t = 1)", "sum"],
                               y=ys, measure=["relative"] * 3 + ["total"], text=text, textposition="outside",
                               decreasing=dict(marker=dict(color=ORANGE)), totals=dict(marker=dict(color=RED)),
                               connector=dict(line=dict(color=GREY, dash="dot")), showlegend=False), 1, c)
fig.update_yaxes(range=[-0.36, 0.06], zeroline=True, zerolinecolor=GREY)
fig.update_yaxes(title_text="running sum", row=1, col=1)
fig.update_layout(template="simple_white", width=1100, height=520, font=dict(family="Latin Modern Roman", size=20),
                  margin=dict(l=80, r=20, t=70, b=60))
fig.update_annotations(font_size=22)

if __name__ == "__main__":
    fig.write_image(HERE / "path_sums.png", scale=2)

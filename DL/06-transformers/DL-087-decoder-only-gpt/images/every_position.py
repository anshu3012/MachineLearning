"""Section 7.2: one pass of GPT-2 small on "Steve Jobs was the founder of" gives a next-token guess at every position.
Bars: the probability the model gave the true next token (green when it was also the top guess), with the top guess
written above. Last position: the guess used for generation (data/every_position.csv, Notebook). Plotly."""
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go
from common import GREEN, GREY, ORANGE, FONT

here = Path(__file__).parent
E = pd.read_csv(here.parent / "data" / "every_position.csv")
assert round(E.p_actual[4], 2) == 0.74 and E.top1[5].strip() == "Apple" and round(E.p1[5], 2) == 0.69
labels = [f"after<br>{t.strip()}" for t in E.token]
known = E.next_actual.notna()
fig = go.Figure()
p_true = E.p_actual.where(known, E.p1)
cols = [GREEN if (k and a.strip() == b.strip()) else (ORANGE if not k else GREY) for k, a, b in
        zip(known, E.next_actual.fillna(""), E.top1)]
fig.add_bar(x=labels, y=p_true, marker_color=cols, showlegend=False,
            text=[f"true: {a.strip()}<br>{p:.2f}" if k else f"guess: {g.strip()}<br>{p:.2f}"
                  for k, a, g, p in zip(known, E.next_actual.fillna(""), E.top1, p_true)], textposition="outside")
for i, r in E.iterrows():
    if known[i]:
        fig.add_annotation(x=labels[i], y=1.02, text=f"top guess: '{r.top1.strip() or 'newline'}' ({r.p1:.2f})",
                           showarrow=False, font=dict(size=15, color=GREY), yanchor="bottom")
fig.update_layout(template="simple_white", width=1100, height=480, font=dict(FONT, size=18),
                  yaxis=dict(title="probability", range=[0, 1.15]), margin=dict(l=70, r=20, t=30, b=60))
fig.write_image(here / "every_position.png", scale=2)
fig.write_image(here / "every_position.pdf")

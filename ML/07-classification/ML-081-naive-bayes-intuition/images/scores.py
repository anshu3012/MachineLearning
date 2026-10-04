"""Naive Bayes on the 8-match table (Plotly): the four factors per class, and the final scores turned into probabilities."""
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

here = Path(__file__).parent
df = pd.read_csv(here.parent / "data" / "matches.csv")
q = dict(toss="lost", venue="Mumbai", outlook="sunny")
labels = ["P(class)", "P(toss lost | class)", "P(Mumbai | class)", "P(sunny | class)"]
fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.12, column_widths=[0.62, 0.38],
                    subplot_titles=("The four factors", "Product, then divided by the total"))
scores = {}
for cls, col in (("win", "#54A24B"), ("loss", "#E45756")):
    sub = df[df.result == cls]
    f = [len(sub) / len(df)] + [(sub[c] == v).mean() for c, v in q.items()]
    scores[cls] = f[0] * f[1] * f[2] * f[3]
    fig.add_trace(go.Bar(x=labels, y=f, name=cls, marker_color=col, text=[f"{v:.2f}" for v in f], textposition="outside"), 1, 1)
tot = sum(scores.values())
for cls, col in (("win", "#54A24B"), ("loss", "#E45756")):
    fig.add_trace(go.Bar(x=[cls], y=[scores[cls] / tot], marker_color=col, showlegend=False,
                         text=[f"score {scores[cls]:.3f}<br>→ {scores[cls] / tot:.0%}"], textposition="outside"), 1, 2)
print(scores, {k: v / tot for k, v in scores.items()})
fig.update_yaxes(range=[0, 1.05], row=1, col=1)
fig.update_yaxes(range=[0, 0.8], title="probability", row=1, col=2)
fig.update_layout(template="simple_white", width=1150, height=460, barmode="group", font=dict(family="Latin Modern Roman", size=15),
                  legend=dict(x=0.45, y=0.98), margin=dict(l=50, r=20, t=50, b=50))
fig.write_image(here / "scores.png", scale=2); fig.write_image(here / "scores.pdf")

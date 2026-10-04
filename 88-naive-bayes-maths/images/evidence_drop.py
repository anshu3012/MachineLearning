"""Dropping the evidence keeps the order (Plotly), on the cricket example. Left: the scores P(x | C) P(C) for win and
loss, 0.040 and 0.056. Right: the same scores divided by their sum P(x) = 0.096, the posteriors 0.42 and 0.58. Both
panels pick loss."""
from pathlib import Path
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from gifkit import BLUE, FONT, RED
from nb_scores import POST, SCORE, Z

here = Path(__file__).parent
assert round(Z, 3) == 0.096
fig = make_subplots(1, 2, horizontal_spacing=0.14, subplot_titles=["scores P(x | C) P(C)", f"divided by P(x) = {Z:.3f}: posteriors"])
fig.update_annotations(font_size=21)
for col, d, fmt in ((1, SCORE, "{:.3f}"), (2, POST, "{:.2f}")):
    fig.add_trace(go.Bar(x=list(d), y=list(d.values()), marker_color=[BLUE, RED], text=[fmt.format(v) for v in d.values()],
                         textposition="outside", textfont=dict(size=21)), 1, col)
fig.update_yaxes(range=[0, 0.075], row=1, col=1)
fig.update_yaxes(range=[0, 0.75], row=1, col=2)
fig.update_layout(template="simple_white", width=1050, height=480, font=FONT, showlegend=False, margin=dict(l=70, r=30, t=60, b=60))
fig.write_image(here / "evidence_drop.png", scale=2)

"""Section 9: the Notebook's model against the original model of Sutskever et al. (2014), on log scales:
parameters, training pairs and BLEU. Numbers from sections 6 and 9 of the Note. Plotly."""
from pathlib import Path
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from common import BLUE, ORANGE, FONT

here = Path(__file__).parent
rows = [("parameters (log scale)", 4.6e6, 384e6, "4.6 million", "384 million"),
        ("training pairs (log scale)", 40_000, 12e6, "40,000", "12 million"),
        ("test BLEU (0-100)", 13.1, 34.81, "13.1", "34.81")]
fig = make_subplots(rows=1, cols=3, subplot_titles=[r[0] for r in rows], horizontal_spacing=0.08)
for i, (name, ours, theirs, a, b) in enumerate(rows, start=1):
    fig.add_bar(x=["this Note", "Sutskever<br>et al. 2014"], y=[ours, theirs], marker_color=[BLUE, ORANGE],
                text=[a, b], textposition="outside", showlegend=False, row=1, col=i)
    if i < 3:
        fig.update_yaxes(type="log", showticklabels=False, range=[3.5 if i == 2 else 6, 9.5], row=1, col=i)
    else:
        fig.update_yaxes(range=[0, 42], row=1, col=i)
fig.update_layout(template="simple_white", width=1100, height=420, font=dict(FONT, size=18), margin=dict(l=30, r=20, t=50, b=60))
fig.write_image(here / "scale_compare.png", scale=2)
fig.write_image(here / "scale_compare.pdf")

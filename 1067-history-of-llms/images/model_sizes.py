"""How fast language models grew: parameter counts from the original papers, on a log scale (Plotly bar chart)."""
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go
from common import BLUE, ORANGE, FONT

here = Path(__file__).parent
m = pd.read_csv(here.parent / "data" / "model_sizes.csv")
assert m.parameters.max() / m.parameters.min() > 1000
label = lambda p: f"{p / 1e9:.0f} billion" if p >= 1e10 else (f"{p / 1e9:.1f} billion" if p >= 1e9 else f"{p / 1e6:.0f} million")
fig = go.Figure(go.Bar(x=[f"{a}<br>({y})" for a, y in zip(m.model, m.year)], y=m.parameters,
                       marker_color=[ORANGE if "BERT" in a else BLUE for a in m.model],
                       text=[label(p) for p in m.parameters], textposition="outside", textfont=dict(size=18)))
fig.update_layout(template="simple_white", width=900, height=450, font=FONT, showlegend=False,
                  yaxis=dict(type="log", title="parameters (log scale)", range=[7.5, 12.2], dtick=1),
                  margin=dict(l=80, r=20, t=20, b=60))
fig.write_image(here / "model_sizes.png", scale=2)
fig.write_image(here / "model_sizes.pdf")

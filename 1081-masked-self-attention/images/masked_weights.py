"""Self-attention weights on "<start> comment ça va ?" without and with the causal mask (Plotly)."""
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from common import FONT

here = Path(__file__).parent
fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.12,
                    subplot_titles=["without the mask", "with the causal mask"])
for col, name in ((1, "weights_unmasked"), (2, "weights_masked")):
    a = pd.read_csv(here.parent / "data" / f"{name}.csv", index_col=0)
    toks = list(a.columns)
    m = a.values
    fig.add_trace(go.Heatmap(z=m, x=list(range(len(toks))), y=list(range(len(toks))), zmin=0, zmax=1, colorscale="Blues",
                             text=[[f"{v:.2f}" for v in row] for row in m], texttemplate="%{text}", textfont=dict(size=15),
                             showscale=(col == 2), colorbar=dict(title="weight")), row=1, col=col)
    if col == 1:                                            # outline the weights on later words
        for i in range(len(toks)):
            for j in range(i + 1, len(toks)):
                fig.add_shape(type="rect", x0=j - 0.5, x1=j + 0.5, y0=i - 0.5, y1=i + 0.5,
                              line=dict(color="#E45756", width=3), fillcolor="rgba(0,0,0,0)", row=1, col=col)
ticks = dict(tickmode="array", tickvals=list(range(len(toks))), ticktext=toks)
fig.update_xaxes(**ticks, title_text="word taken from (key)")
fig.update_yaxes(**ticks, autorange="reversed")
fig.update_yaxes(title_text="word being computed (query)", col=1)
fig.update_layout(template="simple_white", width=1250, height=560, font=FONT, margin=dict(l=110, r=20, t=50, b=70))
fig.write_image(here / "masked_weights.png", scale=2)
fig.write_image(here / "masked_weights.pdf")

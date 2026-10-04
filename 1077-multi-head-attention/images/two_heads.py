"""Heads 1 and 2 of BERT-base's first layer on "the man saw the astronomer with a telescope", with the weights written in (Plotly)."""
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from common import FONT

here = Path(__file__).parent
a = pd.read_csv(here.parent / "data" / "bert_layer1_attention.csv")
toks = a[a["head"] == 1].drop_duplicates("key_pos").sort_values("key_pos").key.tolist()
fig = make_subplots(rows=1, cols=2, subplot_titles=["head 1", "head 2"], horizontal_spacing=0.1)
for col, h in ((1, 1), (2, 2)):
    m = a[a["head"] == h].pivot(index="query_pos", columns="key_pos", values="weight").values
    fig.add_trace(go.Heatmap(z=m, x=list(range(10)), y=list(range(10)), zmin=0, zmax=0.5, colorscale="Blues",
                             text=[[f"{v:.2f}".lstrip("0") for v in row] for row in m], texttemplate="%{text}",
                             textfont=dict(size=11), showscale=(col == 2), colorbar=dict(title="weight")), row=1, col=col)
    for r in (2, 5):                                   # outline the rows of "man" and "astronomer"
        fig.add_shape(type="rect", x0=-0.5, x1=9.5, y0=r - 0.5, y1=r + 0.5, line=dict(color="#E45756", width=3), fillcolor="rgba(0,0,0,0)",
                      row=1, col=col)
ticks = dict(tickmode="array", tickvals=list(range(10)), ticktext=toks)
fig.update_xaxes(**ticks, tickangle=-50, title_text="key word (looked at)")
fig.update_yaxes(**ticks, autorange="reversed")
fig.update_yaxes(title_text="query word (looking)", col=1)
fig.update_layout(template="simple_white", width=1300, height=640, font=FONT, margin=dict(l=110, r=20, t=40, b=130))
fig.write_image(here / "two_heads.png", scale=2)
fig.write_image(here / "two_heads.pdf")

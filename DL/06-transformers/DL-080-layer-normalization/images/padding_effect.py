"""One real word of an IMDB review after batch norm and layer norm, as the same batch is padded to more positions (Plotly)."""
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go
from common import BLUE, ORANGE, GREY, FONT

here = Path(__file__).parent
r = pd.read_csv(here.parent / "data" / "padding_effect.csv")
fig = go.Figure()
fig.add_trace(go.Scatter(x=r["T"], y=r.bn_value, mode="lines+markers", name="batch norm (statistics include padding)",
                         line=dict(color=BLUE, width=4), marker=dict(size=10)))
fig.add_trace(go.Scatter(x=r["T"], y=r.ln_value, mode="lines+markers", name="layer norm",
                         line=dict(color=ORANGE, width=4), marker=dict(size=10)))
fig.add_trace(go.Scatter(x=r["T"], y=r.bn_real_only, mode="lines", name="batch norm over the real words only",
                         line=dict(color=GREY, width=3, dash="dash")))
for t, s in zip(r["T"], r.padding_share):
    fig.add_annotation(x=t, y=3.55, text=f"{s:.0%}", showarrow=False, font=dict(size=15, color=GREY))
fig.add_annotation(x=r["T"].iloc[0], y=3.8, xanchor="left", text="share of padding:", showarrow=False,
                   font=dict(size=15, color=GREY))
fig.update_layout(template="simple_white", width=950, height=480, font=FONT,
                  xaxis=dict(title="every review padded to this many positions"),
                  yaxis=dict(title="normalised value of one real word", range=[0, 4]),
                  legend=dict(x=0.4, y=0.36, yanchor="top", bgcolor="rgba(255,255,255,0.85)"), margin=dict(l=70, r=20, t=20, b=60))
fig.write_image(here / "padding_effect.png", scale=2)
fig.write_image(here / "padding_effect.pdf")

"""Length of the residual-stream vector of the last token ("of" in "Steve Jobs was the founder of") entering each
GPT-2 small block, and the length of what each attention and MLP sub-block adds. Data: data/resid_norm.csv.
Run: python residual_stream.py -> residual_stream.png"""
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go

from common import BLUE, ORANGE, GREEN, GREY, FONT, DATA

HERE = Path(__file__).parent
d = pd.read_csv(DATA / "resid_norm.csv")
fig = go.Figure()
fig.add_trace(go.Scatter(x=d.layer, y=d.stream_norm_last, mode="lines+markers", name="length of the stream vector x",
                         line=dict(color=GREY, width=4), marker=dict(size=9)))
fig.add_trace(go.Bar(x=d.layer[:12] + 0.3, y=d.attn_add_last[:12], width=0.38, name="added by the attention of the next block", marker_color=ORANGE))
fig.add_trace(go.Bar(x=d.layer[:12] + 0.7, y=d.mlp_add_last[:12], width=0.38, name="added by the MLP of the next block", marker_color=GREEN))
fig.update_layout(template="simple_white", width=900, height=520, font=FONT,
                  xaxis=dict(title="blocks passed (0 = token + position vector only)", dtick=1), yaxis=dict(title="length of the vector"),
                  legend=dict(x=0.02, y=0.98), margin=dict(l=70, r=20, t=20, b=60))
fig.write_image(HERE / "residual_stream.png", scale=2)

"""Section 8: the attention weights one head computes, n^2 for a context of n tokens, with the context sizes of GPT-1,
GPT-2 and GPT-3 marked. Doubling the context multiplies the weights by 4. Plotly (log scales)."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from common import BLUE, GREY, FONT

here = Path(__file__).parent
n = 2.0 ** np.arange(6, 12)
assert 1024 ** 2 == 1_048_576 and 144 * 1024 ** 2 == 150_994_944 and 144 * 2048 ** 2 == 603_979_776
fig = go.Figure(go.Scatter(x=n, y=n ** 2, mode="lines+markers", line=dict(color=BLUE, width=4), marker=dict(size=10),
                           showlegend=False))
for m, name in ((512, "GPT-1: 512"), (1024, "GPT-2: 1,024"), (2048, "GPT-3: 2,048")):
    fig.add_annotation(x=np.log10(m), y=np.log10(m ** 2), text=f"{name}<br>{m ** 2:,} weights", showarrow=True,
                       ax=-70, ay=-50, font=dict(size=16))
fig.update_layout(template="simple_white", width=1000, height=440, font=dict(FONT, size=18),
                  xaxis=dict(type="log", title="context size n (tokens)", tickvals=list(n), ticktext=[f"{int(v):,}" for v in n]),
                  yaxis=dict(type="log", title="attention weights per head, n²", exponentformat="power", dtick=1),
                  margin=dict(l=90, r=30, t=20, b=70))
fig.write_image(here / "context_cost.png", scale=2)
fig.write_image(here / "context_cost.pdf")

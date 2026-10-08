"""The beam model: 0.75 p_hit + 0.12 p_short + 0.05 p_max + 0.08 p_rand for the beam whose expected range is 3 m.
Each weighted part is drawn as a band stacked on the ones below; the top edge is the mixture. The max-range spike
(height 0.05 x 100 = 5) is cut off at the top of the plot. Run -> mixture.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from beammodel import W, ZSTAR, p_hit, p_max, p_rand, p_short
from gifkit import BLUE, FONT, GREEN, ORANGE, PURPLE

here = Path(__file__).parent
z = np.concatenate([np.linspace(0, 4.99, 6000), [4.9949, 4.995, 5.0]])
layers = [("random 0.08 p<sub>rand</sub>", W["rand"] * p_rand(z), GREEN),
          ("unexpected 0.12 p<sub>short</sub>", W["short"] * p_short(z, ZSTAR), ORANGE),
          ("noise 0.75 p<sub>hit</sub>", W["hit"] * p_hit(z, ZSTAR), BLUE),
          ("failure 0.05 p<sub>max</sub>", W["max"] * p_max(z), PURPLE)]
fig = go.Figure()
acc = np.zeros_like(z)
for name, y, c in layers:
    acc = acc + y
    top = name.startswith("failure")
    fig.add_trace(go.Scatter(x=z, y=acc.copy(), mode="lines", line=dict(color="black" if top else c, width=2.5),
                             fill="tonexty" if name[0] != "r" else "tozeroy", fillcolor=c if top else None,
                             name=name + (" (black top edge: the mixture)" if top else "")))
fig.update_layout(template="simple_white", width=1000, height=560, font=FONT, margin=dict(l=80, r=30, t=30, b=70),
                  legend=dict(x=0.02, y=0.8, bgcolor="rgba(255,255,255,0.8)", font_size=19))
fig.update_xaxes(title="reading z (m)", range=[0, 5.08], dtick=0.5)
fig.update_yaxes(title="density (per m)", range=[0, 1.0])
for x, yv, t in ((1.0, 0.0486, "1.00 m: 0.049"), (4.0, 0.016, "4.00 m: 0.016")):
    fig.add_annotation(x=x, y=yv, ax=0, ay=-90, text=t, font=dict(size=18), arrowwidth=2)
fig.add_annotation(x=2.85, y=0.97, text="peak 5.55 at 3 m (cut off)", showarrow=False, xanchor="right", yanchor="top", font_size=18)
fig.add_annotation(x=4.98, y=0.97, text="spike 5.0 at 5 m (cut off)", showarrow=False, xanchor="right", yanchor="top", font_size=18)
fig.write_image(here / "mixture.png", scale=1)

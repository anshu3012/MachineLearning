"""Section 3: an LSTM has four layers in its cell, a GRU three, so a GRU layer has about three quarters of the
parameters at every size. Parameter counts of the recurrent layer for 32-number inputs (the IMDB setup of section 9),
from the formulas of section 9.1 (Keras' default GRU, reset_after=True, has 2u biases per layer).
Run: python param_growth.py  -> param_growth.png (Plotly: counts changing with the number of units)"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go

from common import BLUE, ORANGE

HERE = Path(__file__).parent
lstm = lambda u, d: 4 * ((u + d) * u + u)
gru = lambda u, d: 3 * ((u + d) * u + 2 * u)                  # Keras default
gru_plain = lambda u, d: 3 * ((u + d) * u + u)                # reset_after=False
assert (lstm(4, 3), gru_plain(4, 3), gru(4, 3)) == (128, 96, 108)        # section 9.1
assert (lstm(32, 32), gru(32, 32)) == (8320, 6336)                      # section 9.2
units = np.arange(8, 129, 8)
L, G = lstm(units, 32), gru(units, 32)

fig = go.Figure()
fig.add_trace(go.Scatter(x=units, y=L, mode="lines+markers", name="LSTM: 4 layers", line=dict(color=BLUE, width=4)))
fig.add_trace(go.Scatter(x=units, y=G, mode="lines+markers", name="GRU: 3 layers", line=dict(color=ORANGE, width=4)))
for u in (32, 128):
    for y, c, dy, side in ((lstm(u, 32), BLUE, 16, "right"), (gru(u, 32), ORANGE, -16, "left")):
        fig.add_annotation(x=u, y=y, text=f"{y:,}", showarrow=False, xanchor=side, xshift=-8 if side == "right" else 8,
                           yshift=dy, font=dict(color=c, size=20))
fig.add_annotation(x=70, y=60000, showarrow=False, font=dict(size=22),
                   text=f"GRU / LSTM = {gru(32, 32) / lstm(32, 32):.2f} at 32 units, {gru(128, 32) / lstm(128, 32):.2f} at 128")
fig.update_layout(template="simple_white", width=1000, height=520, font=dict(family="Latin Modern Roman", size=22),
                  title=dict(text="parameters of one recurrent layer (inputs of 32 numbers)", x=0.5),
                  xaxis=dict(title="units"), yaxis=dict(title="parameters"), legend=dict(x=0.02, y=0.98),
                  margin=dict(l=90, r=30, t=70, b=60))

if __name__ == "__main__":
    fig.write_image(HERE / "param_growth.png", scale=2)

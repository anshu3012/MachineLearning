"""Section 6.4: with the input gate closed (i_t = 0), the cell state after t steps is f^t times its start.
First entry of the Note's c = [4, 5, 6], for a forget gate of 1, 0.9 and 0.5 held for 20 time steps.
Run: python carry.py  -> carry.png (Plotly: values changing over time steps, one line per setting)"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go

from common import BLUE, GREEN, RED

HERE = Path(__file__).parent
c0, steps = np.array([4.0, 5.0, 6.0]), np.arange(0, 21)
runs = {}
for f, colour in ((1.0, GREEN), (0.9, BLUE), (0.5, RED)):
    c, path = c0.copy(), [c0[0]]
    for _ in steps[1:]:
        c = f * c                                         # c_t = f ⊙ c_{t-1} + i ⊙ c~_t with i = 0
        path.append(c[0])
    runs[f] = (np.array(path), colour)
    if f == 1.0:
        assert np.array_equal(c, c0)                      # the Note's example: [4, 5, 6] comes out unchanged
assert np.isclose(runs[0.9][0][20], 4 * 0.9 ** 20) and round(runs[0.9][0][20], 2) == 0.49

fig = go.Figure()
for f, (path, colour) in runs.items():
    fig.add_trace(go.Scatter(x=steps, y=path, mode="lines+markers", line=dict(color=colour, width=4),
                             marker=dict(size=8), name=f"forget gate f = {f:g}"))
    fig.add_annotation(x=20, y=path[-1], text=f"{path[-1]:.2f}", showarrow=False, xanchor="left", xshift=10,
                       font=dict(color=colour, size=22))
fig.update_layout(template="simple_white", width=1000, height=520, font=dict(family="Latin Modern Roman", size=22),
                  title=dict(text="first entry of the cell state, input gate closed (i = 0)", x=0.5),
                  xaxis=dict(title="time step", range=[-0.5, 22]), yaxis=dict(title="c<sub>t</sub>", range=[-0.2, 4.5]),
                  legend=dict(x=0.55, y=0.62), margin=dict(l=70, r=30, t=70, b=60))

if __name__ == "__main__":
    fig.write_image(HERE / "carry.png", scale=2)

"""Why PCA keeps the direction with the most variance: two flats far apart in rooms stay apart when projected on
the rooms axis, but land almost on top of each other when projected on the grocery-shops axis."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from flats import rooms, shops

here = Path(__file__).parent
BLUE, ORANGE, GREEN, RED, GREY = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#6B6B6B"
i, j = int(np.argmin(rooms)), int(np.argmax(rooms))
# pick the far-right flat whose shop count is closest to the far-left one
j = int(np.argmin(np.abs(shops - shops[i]) + 10 * (rooms < 4)))
d_full = float(np.hypot(rooms[i] - rooms[j], shops[i] - shops[j]))
d_x, d_y = abs(rooms[i] - rooms[j]), abs(shops[i] - shops[j])
print(f"distance in 2D {d_full:.2f}; on rooms axis {d_x:.2f}; on shops axis {d_y:.2f}")
fig = go.Figure()
fig.add_trace(go.Scatter(x=rooms, y=shops, mode="markers", marker=dict(size=10, color=BLUE, opacity=0.35)))
for k, colour in ((i, RED), (j, GREEN)):
    fig.add_trace(go.Scatter(x=[rooms[k]], y=[shops[k]], mode="markers", marker=dict(size=16, color=colour)))
    fig.add_trace(go.Scatter(x=[rooms[k], rooms[k], None, rooms[k], 0], y=[shops[k], 0, None, shops[k], shops[k]],
                             mode="lines", line=dict(color=colour, dash="dot", width=2)))
    fig.add_trace(go.Scatter(x=[rooms[k], 0], y=[0, shops[k]], mode="markers",
                             marker=dict(size=14, color=colour, symbol="diamond"), cliponaxis=False))
fig.add_annotation(x=(rooms[i] + rooms[j]) / 2, y=0.35, showarrow=False, font=dict(size=17, color=ORANGE),
                   text=f"on the rooms axis: still {d_x:.2f} apart")
fig.add_annotation(x=0.15, y=shops[i] + 0.9, xanchor="left", showarrow=False, font=dict(size=17, color=ORANGE),
                   text=f"on the shops axis: only {d_y:.2f} apart")
fig.update_layout(template="simple_white", width=900, height=520, showlegend=False,
                  font=dict(family="Latin Modern Roman", size=17), margin=dict(l=70, r=20, t=70, b=60),
                  title=dict(text=f"Two flats {d_full:.2f} apart: which axis keeps them apart?", x=0.5),
                  xaxis=dict(title="Rooms (variance 1.33)", range=[0, 5.5]),
                  yaxis=dict(title="Grocery shops (variance 0.10)", range=[0, 4.5]))
fig.write_image(here / "why_max_variance.png", scale=2)
fig.write_image(here / "why_max_variance.pdf")

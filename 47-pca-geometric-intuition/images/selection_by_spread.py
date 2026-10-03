"""Feature selection by spread: project the points on each axis and keep the axis with the bigger spread.
Left: rooms vs grocery shops (easy). Right: rooms vs washrooms (spreads equal, selection cannot choose)."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from flats import rooms, shops, washrooms

here = Path(__file__).parent
BLUE, ORANGE, GREEN, RED, GREY = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#6B6B6B"
pairs = [(shops, "Grocery shops nearby"), (washrooms, "Washrooms")]
var = lambda v: v.var()
titles = [f"Rooms vs grocery shops<br>variance: rooms {var(rooms):.2f}, shops {var(shops):.2f}",
          f"Rooms vs washrooms<br>variance: rooms {var(rooms):.2f}, washrooms {var(washrooms):.2f}"]
fig = make_subplots(1, 2, subplot_titles=titles, horizontal_spacing=0.12)
for c, (other, name) in enumerate(pairs, start=1):
    fig.add_trace(go.Scatter(x=rooms, y=other, mode="markers", marker=dict(size=10, color=BLUE)), 1, c)
    # shadows on each axis
    fig.add_trace(go.Scatter(x=rooms, y=np.full_like(rooms, 0.25), mode="markers",
                             marker=dict(size=9, color=ORANGE, symbol="line-ns-open", line=dict(width=2))), 1, c)
    fig.add_trace(go.Scatter(x=np.full_like(other, 0.25), y=other, mode="markers",
                             marker=dict(size=9, color=GREEN, symbol="line-ew-open", line=dict(width=2))), 1, c)
    for a, b, colour in ((rooms.min(), rooms.max(), ORANGE),):
        fig.add_shape(type="line", x0=a, x1=b, y0=0.05, y1=0.05, line=dict(color=colour, width=5), row=1, col=c)
    fig.add_shape(type="line", x0=0.05, x1=0.05, y0=other.min(), y1=other.max(), line=dict(color=GREEN, width=5),
                  row=1, col=c)
    fig.update_xaxes(title="Rooms", range=[0, 5.6], row=1, col=c)
    fig.update_yaxes(title=name, range=[0, 5.6], scaleanchor=f"x{'' if c == 1 else 2}", row=1, col=c)
print(f"var rooms {var(rooms):.2f} shops {var(shops):.2f} washrooms {var(washrooms):.2f}")
fig.update_layout(template="simple_white", width=1000, height=520, showlegend=False,
                  font=dict(family="Latin Modern Roman", size=17), margin=dict(l=70, r=20, t=90, b=60))
fig.update_annotations(font_size=17)
fig.write_image(here / "selection_by_spread.png", scale=2)
fig.write_image(here / "selection_by_spread.pdf")

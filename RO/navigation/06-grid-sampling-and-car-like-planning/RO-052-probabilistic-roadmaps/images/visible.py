"""Figure: the free floor that sees the corner (6.6, 0.4) along a free straight segment (green, tested every 0.05 m),
27.9 percent of the free floor for the robot's centre; a milestone drawn uniformly from the free floor joins the
corner only if it lands in the green part. Run -> visible.png"""
from pathlib import Path

import prm
import prmdraw as pd
from gifkit import GREEN

here = Path(__file__).parent
w = prm.World()
p, xs, ys, vis = prm.visible_share(w, prm.CORNER)
assert round(p, 3) == 0.279
fig = pd.base(w)
fig.add_scatter(x=xs[vis], y=ys[vis], mode="markers", marker=dict(color="rgba(84,162,75,0.45)", size=4,
                                                                   symbol="square"), hoverinfo="skip")
pd.place(fig, prm.CORNER, "corner", "black", "bottom center")
pd.panel(fig, [("green: free floor from which", GREEN), ("a straight free edge", GREEN),
               ("reaches the corner", GREEN), ("", "black"), ("share of the free floor:", "black"),
               ("p = 0.279", "black"), ("", "black"), ("a milestone drawn at random", "black"),
               ("lands in the green part", "black"), ("with chance p", "black")])
pd.finish(fig, "What the corner sees: p = 0.279 of the free floor")
fig.write_image(here / "visible.png")

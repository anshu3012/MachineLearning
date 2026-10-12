"""The town graph: 11 intersections joined by 13 streets, each labelled with its length and speed limit. The bypass
(80 km/h) runs north of the old town (30 km/h); the main road (50 km/h) joins them; the street from F to C is
one-way, northbound. Run -> town_map.png"""
from pathlib import Path

import plotly.graph_objects as go
import townplot as tp

here = Path(__file__).parent
fig = go.Figure()
off = {frozenset("AN"): (-150, 0), frozenset("MD"): (150, 0), frozenset("BE"): (-160, 0), frozenset("FC"): (200, 0),
       frozenset("LT"): (190, -40), frozenset("ML"): (0, 45), frozenset("NM"): (0, 45), frozenset("EF"): (0, 45),
       frozenset("SA"): (0, -45), frozenset("AB"): (0, -45), frozenset("BC"): (0, -45), frozenset("CD"): (0, -45),
       frozenset("DT"): (0, -45)}
tp.roads(fig, label="len", offset=off)
tp.vertices(fig)
for txt, x, y in (("bypass, 80 km/h", 1250, 1110), ("old town, 30 km/h", 1250, 115)):
    fig.add_annotation(x=x, y=y, text=txt, showarrow=False, font=dict(size=19, color="#333333"))
fig.add_annotation(x=1395, y=300, text="one-way", showarrow=False, font=dict(size=17, color="#333333"))
tp.frame_layout(fig, width=1300, height=520, yr=(70, 1160))
fig.write_image(here / "town_map.png", scale=2)

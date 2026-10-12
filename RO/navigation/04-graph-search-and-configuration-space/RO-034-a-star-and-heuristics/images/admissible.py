"""Is the guess ever too big? For each of the 76 free cells: across, the true shortest distance left to the goal
cell G (a Dijkstra run backwards from G); up, the guess h, octile distance (blue) and straight-line distance (orange).
Every dot is on or below the line guess = true distance: neither guess ever overestimates. The cell S: octile 3.121 m,
straight line 2.915 m, true 3.414 m. Cells behind the table and the cabinet are far below the line: their true
route goes all the way round. Run -> admissible.png"""
from pathlib import Path

import plotly.graph_objects as go
from gifkit import BLUE, FONT, GREY, ORANGE
from searchkit import START, dist_from, free_cells, octile, straight

here = Path(__file__).parent
Hs = dist_from((7, 7))
cells = free_cells()
assert len(cells) == 76
assert all(octile(c) <= Hs[c] + 1e-9 for c in cells) and all(straight(c) <= octile(c) + 1e-9 for c in cells)
n_exact = sum(abs(octile(c) - Hs[c]) < 1e-9 for c in cells)
assert n_exact == 31
assert (round(octile(START), 3), round(straight(START), 3), round(Hs[START], 3)) == (3.121, 2.915, 3.414)

fig = go.Figure()
fig.add_trace(go.Scatter(x=[0, 11.4], y=[0, 11.4], mode="lines", line=dict(color=GREY, dash="dash", width=2),
                         name="h = true distance"))
fig.add_trace(go.Scatter(x=[Hs[c] for c in cells], y=[straight(c) for c in cells], mode="markers",
                         marker=dict(size=10, color=ORANGE, symbol="diamond"), name="straight-line distance"))
fig.add_trace(go.Scatter(x=[Hs[c] for c in cells], y=[octile(c) for c in cells], mode="markers",
                         marker=dict(size=10, color=BLUE), name="octile distance"))
fig.add_annotation(x=Hs[START], y=octile(START), ax=-150, ay=-110, text="S: octile 3.121,<br>true 3.414",
                   showarrow=True, arrowhead=2, arrowwidth=2, font=dict(size=19), bgcolor="white")
fig.add_annotation(x=11.2, y=2.2, text="behind the table:<br>the true route goes round", showarrow=False,
                   font=dict(size=18, color=GREY), xanchor="right")
fig.add_annotation(x=0.3, y=7.4, text="above the line: h too big, would overestimate", showarrow=False, font=dict(size=18, color=GREY),
                   xanchor="left")
fig.add_annotation(x=11.2, y=0.6, text="below the line: h never more than the true distance", showarrow=False,
                   font=dict(size=18, color=GREY), xanchor="right")
fig.update_xaxes(title="true shortest distance left to G (m)", range=[0, 11.4], dtick=1)
fig.update_yaxes(title="heuristic h (m)", range=[0, 11.4], dtick=1, scaleanchor="x")
fig.update_layout(template="simple_white", font=FONT, width=820, height=760, title=dict(
    text="every free cell: heuristic h against the true distance left", x=0.5), legend=dict(x=0.02, y=0.98, bgcolor="white"),
    margin=dict(l=80, r=30, t=70, b=70))
fig.write_image(here / "admissible.png")

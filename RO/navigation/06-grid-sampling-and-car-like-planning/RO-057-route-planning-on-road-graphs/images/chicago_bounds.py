"""How close each heuristic comes to the truth on the Chicago street graph, for the trip's goal: one dot per
intersection, across the true fastest travel time from it to the goal (one Dijkstra run backwards from the goal),
up the heuristic's guess. chicago_bounds_straight.png: the straight line to the goal divided by the top speed,
88.5 km/h (orange); on average it guesses 0.41 of the true time. chicago_bounds_alt.png adds A* with 16 landmarks
(purple): on average 0.93 of the true time. Every dot lies on or under the dashed line guess = truth. Run ->
chicago_bounds_straight.png, chicago_bounds_alt.png"""
from pathlib import Path
from statistics import mean

import plotly.graph_objects as go
import roadkit as rk
from gifkit import FONT, ORANGE, PURPLE

here = Path(__file__).parent
C = rk.chicago()
At, Al, pos = C["adj_time"], C["adj_len"], C["pos"]
vmax = max(Al[u][v] / At[u][v] for u in At for v in At[u])
X, Y = max(p[0] for p in pos.values()), max(p[1] for p in pos.values())
t = rk.nearest(pos, (0.88 * X, 0.9 * Y))
true = rk.dists(rk.reverse(At), t)
hs = rk.straight(pos, t, vmax)
ha = rk.alt_heuristic(rk.landmark_tables(At, rk.farthest_landmarks(At, 16, sorted(At)[0])), t)
us = [u for u in At if u != t]
rs, ra = mean(hs(u) / true[u] for u in us), mean(ha(u) / true[u] for u in us)
assert all(hs(u) <= true[u] + 1e-9 and ha(u) <= true[u] + 1e-9 for u in us)
assert (round(rs, 2), round(ra, 2)) == (0.41, 0.93), (rs, ra)
top = max(true.values())


def plot(with_alt, out):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=[0, top], y=[0, top], mode="lines", line=dict(color="black", dash="dash", width=2),
                             name="guess = true time"))
    fig.add_trace(go.Scatter(x=[true[u] for u in us], y=[hs(u) for u in us], mode="markers",
                             marker=dict(size=5, color=ORANGE, opacity=0.6),
                             name=f"straight line ÷ 88.5 km/h (average {rs:.2f} of the true time)"))
    if with_alt:
        fig.add_trace(go.Scatter(x=[true[u] for u in us], y=[ha(u) for u in us], mode="markers",
                                 marker=dict(size=5, color=PURPLE, opacity=0.6, symbol="diamond"),
                                 name=f"16 landmarks (average {ra:.2f} of the true time)"))
    fig.update_xaxes(title="true fastest time to the goal (s)", range=[0, top * 1.03])
    fig.update_yaxes(title="heuristic h (s)", range=[0, top * 1.03], scaleanchor="x")
    fig.update_layout(template="simple_white", font=FONT, width=820, height=860, margin=dict(l=80, r=20, t=20, b=70),
                      legend=dict(x=0.02, y=0.98, bgcolor="rgba(255,255,255,0.9)", font_size=18))
    fig.write_image(here / out, scale=2)


plot(False, "chicago_bounds_straight.png")
plot(True, "chicago_bounds_alt.png")

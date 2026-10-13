"""Animation: Nav2's bring-up. bringup_launch.py starts one lifecycle manager, lifecycle_manager_nav2, whose
node_names are the localisation nodes (map_server, amcl), the keep-out and speed zone filter servers
(keepout_zone_launch.py, speed_zone_launch.py, both on by default), then the navigation nodes of
navigation_launch.py: 17 nodes. Its
startup() configures every node in that order, then activates every node in that order (lifecycle_manager.cpp).
Then a bond with each node: a heartbeat every 0.25 s, and 4 s without one brings the system down.
Run -> bringup.gif, bringup_frames.png"""
from pathlib import Path

import plotly.graph_objects as go

import nav2sim as N
from gifkit import FONT, GREY, RED, make_gif

here = Path(__file__).parent
B = N.lifecycle_bringup()
assert len(N.NODES) == 17 and len(B) == 34 and B[17] == ("map_server", "activate", "active")
COL = {"unconfigured": "#EEEEEE", "inactive": "#F8C98A", "active": "#9BD39A"}


def frame(states, k_lit, title, note=""):
    fig = go.Figure()
    for i, n in enumerate(N.NODES):
        y = 16 - i
        st = states[n]
        lit = n == k_lit
        fig.add_shape(type="rect", x0=0.0, x1=4.6, y0=y - 0.42, y1=y + 0.42, fillcolor=COL[st], opacity=1,
                      line=dict(color=RED if lit else GREY, width=4 if lit else 1))
        fig.add_annotation(x=0.15, y=y, text=n, showarrow=False, xanchor="left", font=dict(size=21))
        fig.add_annotation(x=4.45, y=y, text=st, showarrow=False, xanchor="right", font=dict(size=19, color="#333333"))
    for j, (st, c) in enumerate(COL.items()):
        fig.add_shape(type="rect", x0=5.0, x1=5.4, y0=15.6 - 1.1 * j, y1=16.2 - 1.1 * j, fillcolor=c,
                      line=dict(color=GREY, width=1), opacity=1)
        fig.add_annotation(x=5.55, y=15.9 - 1.1 * j, text=st, showarrow=False, xanchor="left", font=dict(size=19))
    fig.add_annotation(x=5.0, y=10.5, text=note, showarrow=False, xanchor="left", align="left",
                       font=dict(size=19, color=RED))
    fig.update_xaxes(range=[-0.1, 8.2], visible=False)
    fig.update_yaxes(range=[-0.7, 16.7], visible=False)
    fig.update_layout(template="simple_white", width=1150, height=1050, font=FONT, showlegend=False,
                      margin=dict(l=10, r=10, t=70, b=10), title=dict(text=title, x=0.5, y=0.975, font=dict(size=22)))
    return fig


states = {n: "unconfigured" for n in N.NODES}
figs, holds, keys = [frame(states, None, "lifecycle_manager_nav2 starts: 17 managed nodes, all unconfigured",
                           "node_names: localisation,<br>then the zone filters,<br>then navigation")], [6], [0]
for k, (n, tr, st) in enumerate(B):
    states[n] = st
    title = (f"configure {k + 1} of 17: {n}" if tr == "configure" else f"activate {k - 16} of 17: {n}")
    note = ("configure: read parameters,<br>create publishers, services<br>and action servers" if tr == "configure"
            else "activate: start publishing<br>and accepting goals")
    figs.append(frame(states, n, title, note))
    holds.append(2)
    if k in (8, 16, 25):
        keys.append(len(figs) - 1)
figs.append(frame(states, None, "all 17 active: bonds start (heartbeat every 0.25 s, 4 s without one: bring down)",
                  "a goal can now be sent"))
holds.append(16)
keys.append(len(figs) - 1)
make_gif(figs, here / "bringup", fps=4, holds=holds, keys=keys, cols=2, width=800)

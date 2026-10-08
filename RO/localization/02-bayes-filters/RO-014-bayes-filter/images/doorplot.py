"""Shared door-world model and bar drawing (no output when run on its own).
State: the door is open or closed. Sensor: p(sense open | open) = 0.6, p(sense open | closed) = 0.2.
Push: an open door stays open; a closed door opens with probability 0.8. Do nothing: the door stays as it is."""
import plotly.graph_objects as go

STATES = ("open", "closed")
P_Z = {"open": {"open": 0.6, "closed": 0.4}, "closed": {"open": 0.2, "closed": 0.8}}
P_X = {"push": {"open": {"open": 1.0, "closed": 0.0}, "closed": {"open": 0.8, "closed": 0.2}},
       "do nothing": {"open": {"open": 1.0, "closed": 0.0}, "closed": {"open": 0.0, "closed": 1.0}}}


def predict(bel, u):
    return {x: sum(P_X[u][xp][x] * bel[xp] for xp in STATES) for x in STATES}


def update(bel_bar, z):
    unnorm = {x: P_Z[x][z] * bel_bar[x] for x in STATES}
    s = sum(unnorm.values())
    return {x: v / s for x, v in unnorm.items()}


def door_bars(fig, bel, color, row=None, col=None, fmt="{:.3f}"):
    kw = dict(row=row, col=col) if row else {}
    fig.add_trace(go.Bar(x=list(STATES), y=[bel[s] for s in STATES], marker_color=color, width=0.55,
                         text=[fmt.format(bel[s]) for s in STATES], textposition="outside", textfont=dict(size=20),
                         cliponaxis=False), **kw)
    fig.update_yaxes(range=[0, 1.12], **kw)

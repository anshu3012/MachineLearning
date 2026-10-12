"""Drawing helpers for the town graph of this Note (no output when run on its own).
Roads are grey; their width shows the speed limit (bypass 80 km/h widest, main road 50 km/h, old town 30 km/h
thinnest). Vertices are circles with their letter: white, or light green (on the open list), light red (taken
off it), orange outline (the vertex just taken off). Routes are blue."""
import math

import plotly.graph_objects as go
from gifkit import BLUE, FONT, ORANGE
from roadkit import KMH, ONE_WAY, TOWN_POS as P, TOWN_ROADS

WIDTH = {"bypass": 9, "main": 5, "old": 2.5}
ROAD = "#A8A8A8"
FILL = {"open": "#C3E6B9", "closed": "#F6B8B8", "pale": "#EDEDED", None: "white"}
SEC = {(a, b): length / (KMH[k] / 3.6) for a, b, k, length in TOWN_ROADS}
SEC.update({(b, a): v for (a, b), v in list(SEC.items())})


def fmt_s(x):
    return f"{x:.1f}".rstrip("0").rstrip(".") if abs(x - round(x, 1)) < 1e-9 else f"{x:.2f}"


def roads(fig, label="time", rc=None, dim=(), offset=None):
    """label: 'time' (s), 'len' (m and km/h), or None. dim: roads drawn pale. offset: {frozenset(a, b): (dx, dy)}
    to move a road's label off its line."""
    kw = dict(row=rc[0], col=rc[1]) if rc else {}
    offset = offset or {}
    for a, b, kind, length in TOWN_ROADS:
        (x0, y0), (x1, y1) = P[a], P[b]
        pale = frozenset((a, b)) in dim
        fig.add_trace(go.Scatter(x=[x0, x1], y=[y0, y1], mode="lines", hoverinfo="skip",
                                 line=dict(color="#E2E2E2" if pale else ROAD, width=WIDTH[kind])), **kw)
        if label:
            dx, dy = offset.get(frozenset((a, b)), (0, 0))
            text = (f"{length} m, {KMH[kind]} km/h" if label == "len" else f"{fmt_s(SEC[(a, b)])} s")
            fig.add_annotation(x=(x0 + x1) / 2 + dx, y=(y0 + y1) / 2 + dy, text=text, showarrow=False,
                               font=dict(size=17, color="#555555"), bgcolor="rgba(255,255,255,0.85)", **kw)
    for a, b in ONE_WAY:                      # the one-way street: an arrow along it, pointing the allowed way
        (x0, y0), (x1, y1) = P[a], P[b]
        fig.add_annotation(x=x0 + 0.62 * (x1 - x0), y=y0 + 0.62 * (y1 - y0), ax=x0 + 0.38 * (x1 - x0),
                           ay=y0 + 0.38 * (y1 - y0), xref=kw and f"x{_ax(rc)}" or "x", yref=kw and f"y{_ax(rc)}" or "y",
                           axref=kw and f"x{_ax(rc)}" or "x", ayref=kw and f"y{_ax(rc)}" or "y",
                           showarrow=True, arrowhead=2, arrowsize=1.6, arrowwidth=3, arrowcolor="#333333", text="")


def _ax(rc):
    return "" if rc is None or rc == (1, 1) else str((rc[0] - 1) * 2 + rc[1])


def route(fig, path, color=BLUE, width=6, dash=None, rc=None):
    kw = dict(row=rc[0], col=rc[1]) if rc else {}
    fig.add_trace(go.Scatter(x=[P[v][0] for v in path], y=[P[v][1] for v in path], mode="lines", hoverinfo="skip",
                             line=dict(color=color, width=width, dash=dash)), **kw)


def vertices(fig, status=None, cur=None, rc=None, size=40, hide=()):
    kw = dict(row=rc[0], col=rc[1]) if rc else {}
    status = status or {}
    for v, (x, y) in P.items():
        if v in hide:
            continue
        fig.add_trace(go.Scatter(x=[x], y=[y], mode="markers+text", text=[f"<b>{v}</b>"], hoverinfo="skip",
                                 textfont=dict(size=20),
                                 marker=dict(size=size, color=FILL[status.get(v)],
                                             line=dict(color=ORANGE if v == cur else "black",
                                                       width=5 if v == cur else 2))), **kw)


def frame_layout(fig, title=None, width=1200, height=560, xr=(-250, 3250), yr=(80, 1130)):
    fig.update_xaxes(range=list(xr), visible=False)
    fig.update_yaxes(range=list(yr), visible=False, scaleanchor="x")
    fig.update_layout(template="simple_white", font=FONT, width=width, height=height, showlegend=False,
                      margin=dict(l=10, r=10, t=60 if title else 10, b=10),
                      title=dict(text=title, x=0.5, font_size=23) if title else None)
    return fig


def dist(a, b):
    return math.dist(P[a], P[b])

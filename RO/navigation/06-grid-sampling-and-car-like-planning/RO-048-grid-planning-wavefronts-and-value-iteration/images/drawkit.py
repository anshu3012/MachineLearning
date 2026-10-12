"""Drawing helpers for this Note's grid figures (no output when run on its own): the room's 0.5 m cells as one
heatmap (free white, blocked grey, and the search's colours), grid lines from the gaps between cells, the true table,
cabinet and poles as thin outlines, the walls with the door gap, and helpers for routes, labels and axes.
Colours: closed (taken off the open list) light red, open light green, route blue, the cell being expanded outlined
in orange; a backward search uses light blue."""
import numpy as np
import plotly.graph_objects as go
from gifkit import BLUE, GREY, ORANGE
from roommap import DOOR, POLE_R, POLES, TABLE
from searchkit import BLOCKED, C, GOAL, NX, NY, START

PALETTE = {"free": "#FFFFFF", "blocked": "#8A8A8A", "closed": "#F6B8B8", "open": "#C3E6B9",
           "back": "#9DB9E3", "back_open": "#D6E3F5", "seen": "#FBE3C5", "pale": "#EDEDED"}
CODES = list(PALETTE)
LINE = "#D4D4D4"
VSCALE = [[0, "#FFF3C4"], [0.35, "#BFD7EA"], [1, "#6F9BCB"]]   # distance to the door: low pale yellow, high blue


def centre(c):
    return ((c[0] + 0.5) * C, (c[1] + 0.5) * C)


def _kw(rc):
    return dict(row=rc[0], col=rc[1]) if rc else {}


def room(fig, rc=None, status=None, xr=(0, NX), yr=(0, NY), labels=True, goal=GOAL, start=START, walls=True,
         outlines=True):
    """status: dict cell -> one of PALETTE's names, drawn over free/blocked. Cells outside xr, yr are not drawn."""
    kw = _kw(rc)
    z = np.zeros((yr[1] - yr[0], xr[1] - xr[0]))
    for j in range(*yr):
        for i in range(*xr):
            name = "blocked" if BLOCKED[j, i] else "free"
            if status and (i, j) in status:
                name = status[(i, j)]
            z[j - yr[0], i - xr[0]] = CODES.index(name)
    n = len(CODES)
    scale = []
    for k, name in enumerate(CODES):
        scale += [[k / n, PALETTE[name]], [(k + 1) / n, PALETTE[name]]]
    fig.add_trace(go.Heatmap(z=z + 0.5, x0=(xr[0] + 0.5) * C, dx=C, y0=(yr[0] + 0.5) * C, dy=C, zmin=0, zmax=n,
                             colorscale=scale, showscale=False, xgap=2, ygap=2, hoverinfo="skip"), **kw)
    furniture(fig, rc, xr, yr, walls, outlines)
    if labels:
        sg(fig, rc, xr, yr, goal, start)


def heat(fig, vals, scale, zmax, rc=None, xr=(0, NX), yr=(0, NY)):
    """The room with each cell in vals coloured by its value on the colour scale (0 to zmax); other free cells white,
    blocked cells grey."""
    room(fig, rc, {}, xr, yr, labels=False, walls=False, outlines=False)
    z = np.full((yr[1] - yr[0], xr[1] - xr[0]), np.nan)
    for (i, j), v in vals.items():
        if xr[0] <= i < xr[1] and yr[0] <= j < yr[1] and v < np.inf:
            z[j - yr[0], i - xr[0]] = v
    fig.add_trace(go.Heatmap(z=z, x0=(xr[0] + 0.5) * C, dx=C, y0=(yr[0] + 0.5) * C, dy=C, zmin=0, zmax=zmax,
                             colorscale=scale, showscale=False, xgap=2, ygap=2, hoverinfo="skip"), **_kw(rc))
    furniture(fig, rc, xr, yr, True, True)


def furniture(fig, rc=None, xr=(0, NX), yr=(0, NY), walls=True, outlines=True):
    """The true outlines of the table, cabinet and poles, and the walls with the door gap."""
    kw = _kw(rc)
    dark = "#333333"
    if outlines:
        px, py = zip(*(TABLE + [TABLE[0]]))
        fig.add_trace(go.Scatter(x=px, y=py, mode="lines", line=dict(color=dark, width=2), hoverinfo="skip"), **kw)
        fig.add_trace(go.Scatter(x=[5.6, 7, 7, 6.4, 6.4, 5.6, 5.6], y=[4, 4, 2.4, 2.4, 3.4, 3.4, 4], mode="lines",
                                 line=dict(color=dark, width=2), hoverinfo="skip"), **kw)
        t = np.linspace(0, 2 * np.pi, 40)
        for x, y in POLES.values():
            if xr[0] * C <= x <= xr[1] * C and yr[0] * C <= y <= yr[1] * C:
                fig.add_trace(go.Scatter(x=x + POLE_R * np.cos(t), y=y + POLE_R * np.sin(t), mode="lines",
                                         line=dict(color=dark, width=2), hoverinfo="skip"), **kw)
    if walls:
        x0, x1, y0, y1 = xr[0] * C, xr[1] * C, yr[0] * C, yr[1] * C
        segs = []
        if y0 == 0:
            segs.append(((x0, x1), (0, 0)))
        if x0 == 0:
            segs.append(((0, 0), (y0, y1)))
        if x1 == NX * C:
            segs.append(((x1, x1), (y0, y1)))
        if y1 == NY * C:
            for a, b in ((x0, min(x1, DOOR[0])), (max(x0, DOOR[1]), x1)):
                if b > a:
                    segs.append(((a, b), (y1, y1)))
        for xs, ys in segs:
            fig.add_trace(go.Scatter(x=xs, y=ys, mode="lines", line=dict(color="black", width=6),
                                     hoverinfo="skip"), **kw)


def sg(fig, rc=None, xr=(0, NX), yr=(0, NY), goal=GOAL, start=START, dy=0.0, size=26):
    """The S (start) and G (goal) labels; call last so that routes do not cover them."""
    for c, t in ((start, "S"), (goal, "G")):
        if c is not None and xr[0] <= c[0] < xr[1] and yr[0] <= c[1] < yr[1]:
            x, y = centre(c)
            fig.add_trace(go.Scatter(x=[x], y=[y + dy], mode="markers+text", text=[f"<b>{t}</b>"],
                                     marker=dict(size=size, color="white", line=dict(color="black", width=1.5)),
                                     textfont=dict(size=17, color="black"), hoverinfo="skip"), **_kw(rc))


def label(fig, c, text, rc=None, size=18, color="black", dx=0.0, dy=0.0):
    x, y = centre(c)
    fig.add_trace(go.Scatter(x=[x + dx], y=[y + dy], mode="text", text=[text], textfont=dict(size=size, color=color),
                             hoverinfo="skip"), **_kw(rc))


def outline(fig, c, colour=ORANGE, width=5, rc=None):
    i, j = c
    fig.add_trace(go.Scatter(x=[i * C, (i + 1) * C, (i + 1) * C, i * C, i * C],
                             y=[j * C, j * C, (j + 1) * C, (j + 1) * C, j * C], mode="lines",
                             line=dict(color=colour, width=width), hoverinfo="skip"), **_kw(rc))


def route(fig, path, colour=BLUE, width=6, rc=None, dash=None, points=None):
    """points: draw through these (x, y) points instead of cell centres."""
    xs, ys = zip(*(points or [centre(c) for c in path]))
    fig.add_trace(go.Scatter(x=xs, y=ys, mode="lines", line=dict(color=colour, width=width, dash=dash),
                             hoverinfo="skip"), **_kw(rc))


def _xname(fig, rc):
    if not rc:
        return "x"
    return fig.get_subplot(*rc).xaxis.plotly_name.replace("axis", "")


def axes(fig, rc=None, xr=(0, NX), yr=(0, NY), ticks=True):
    kw = _kw(rc)
    fig.update_xaxes(range=[xr[0] * C - 0.06, xr[1] * C + 0.06], showgrid=False, zeroline=False, showline=False,
                     tickvals=[v for v in range(8) if xr[0] * C <= v <= xr[1] * C] if ticks else [], ticks="",
                     showticklabels=ticks, tickfont=dict(size=16, color=GREY), constrain="domain", **kw)
    fig.update_yaxes(range=[yr[0] * C - 0.06, yr[1] * C + 0.06], showgrid=False, zeroline=False, showline=False,
                     tickvals=[v for v in range(5) if yr[0] * C <= v <= yr[1] * C] if ticks else [], ticks="",
                     showticklabels=ticks, tickfont=dict(size=16, color=GREY), scaleanchor=_xname(fig, rc),
                     scaleratio=1, constrain="domain", **kw)


def title_at(fig, text, y, size=21, x=0.5, color="black"):
    """A line of text at height y in paper units (0 bottom, 1 top)."""
    fig.add_annotation(x=x, y=y, xref="paper", yref="paper", text=text, showarrow=False, xanchor="center",
                       yanchor="bottom", font=dict(size=size, color=color))


def layout(fig, title, width=900, height=620, margin=None):
    fig.update_layout(template="simple_white", width=width, height=height, showlegend=False,
                      font=dict(family="Latin Modern Roman", size=20), plot_bgcolor=LINE,
                      title=dict(text=title, x=0.5, xanchor="center", font_size=23),
                      margin=margin or dict(l=30, r=30, t=80, b=30))
    return fig


def numbers(fig, vals, rc=None, fmt="{:d}", size=19, color="black", xr=(0, NX), yr=(0, NY), dy=0.0, box=None):
    """Write vals[cell] in each cell (cells outside xr, yr skipped). box: a background colour, so that a route line
    passing behind a number does not cross it (the numbers become annotations)."""
    if box:
        xr_, yr_ = _xname(fig, rc), _xname(fig, rc).replace("x", "y")
        for c, v in vals.items():
            if xr[0] <= c[0] < xr[1] and yr[0] <= c[1] < yr[1]:
                x, y = centre(c)
                fig.add_annotation(x=x, y=y + dy, xref=xr_, yref=yr_, text=fmt.format(v) if not isinstance(v, str)
                                   else v, showarrow=False, font=dict(size=size, color=color), bgcolor=box,
                                   borderpad=1)
        return
    xs, ys, ts = [], [], []
    for c, v in vals.items():
        if xr[0] <= c[0] < xr[1] and yr[0] <= c[1] < yr[1]:
            x, y = centre(c)
            xs.append(x)
            ys.append(y + dy)
            ts.append(fmt.format(v) if not isinstance(v, str) else v)
    fig.add_trace(go.Scatter(x=xs, y=ys, mode="text", text=ts, textfont=dict(size=size, color=color),
                             hoverinfo="skip"), **_kw(rc))


def arrows(fig, pairs, rc=None, colour="#333333", width=2, size=1.0, frac=0.62):
    """An arrow from each point a towards b, shortened to frac of the way (pairs of (x, y) points)."""
    xr = _xname(fig, rc)
    yr = xr.replace("x", "y")
    for a, b in pairs:
        ex, ey = a[0] + frac * (b[0] - a[0]), a[1] + frac * (b[1] - a[1])
        sx, sy = a[0] - 0.18 * (b[0] - a[0]), a[1] - 0.18 * (b[1] - a[1])
        fig.add_annotation(x=ex, y=ey, ax=sx, ay=sy, xref=xr, yref=yr, axref=xr, ayref=yr, showarrow=True,
                           arrowhead=2, arrowsize=size, arrowwidth=width, arrowcolor=colour, text="")


def robot(fig, xy, rc=None, colour="#222222", size=22):
    fig.add_trace(go.Scatter(x=[xy[0]], y=[xy[1]], mode="markers", marker=dict(size=size, color=colour,
                             line=dict(color="white", width=2)), hoverinfo="skip"), **_kw(rc))

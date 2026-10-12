"""Draw searches on a street map in the look of the video: a black background, the street network faint dark orange,
streets glowing orange-yellow as the search explores them, then the glow fades and the route glows yellow.

Only the map interface (nodes, xy, edge_xy, start, goal, goals, label) and the search log are used, so any map and
any algorithm can be drawn, and a new algorithm needs no new drawing code:
    animate(streets, space, result, out)
streets is the map drawn underneath; space is the map the search ran on (the streets themselves, a grid made from
them, or a FreeSpace for sampling planners)."""
import base64
import math
import os
import sys
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

sys.path.append(str(Path(__file__).resolve().parent.parent / "grid-pathfinding"))
import gifkit                                           # noqa: E402  (the shared GIF maker)

BG, BASE = "#000000", "#6B3008"
GLOW, CORE, NEW_GLOW, NEW_CORE = "#FF8A1E", "#FFB040", "#FFD86A", "#FFF4C8"
ROUTE_GLOW, ROUTE_CORE = "#FFE34D", "#FFFBD0"
START, GOAL, GOALS = "#4FE8FF", "#FF4F6A", "#7FA0FF"
TEXT = "#BDBDBD"
FONT = dict(family="DejaVu Sans", size=20, color=TEXT)
CREDIT = "© OpenStreetMap contributors"


# ---------------------------------------------------------------- geometry

def lines_xy(space, edges):
    """One x array and one y array for many lines, with a gap (NaN) between them, so one trace draws them all
    (arrays, not lists: Plotly checks them much faster)."""
    pts = []
    for a, b in edges:
        pts.extend(space.edge_xy(a, b))
        pts.append((np.nan, np.nan))
    xy = np.array(pts, dtype=float).reshape(-1, 2)
    return xy[:, 0], xy[:, 1]


def extent(sm, pad=0.02):
    xs, ys = zip(*(sm.xy(n) for n in sm.nodes()))
    dx, dy = max(xs) - min(xs), max(ys) - min(ys)
    return (min(xs) - pad * dx, max(xs) + pad * dx), (min(ys) - pad * dy, max(ys) + pad * dy)


def street_edges(sm):
    return [(a, b) for a in sm.nodes() for b in sm.neighbours(a) if str(a) < str(b)]


# ---------------------------------------------------------------- figures

_backgrounds = {}


def background(sm, width, height):
    """The faint street network, drawn once as a picture and placed under every frame."""
    key = (sm.name, width, height)
    if key not in _backgrounds:
        (x0, x1), (y0, y1) = extent(sm)
        xs, ys = lines_xy(sm, street_edges(sm))
        fig = go.Figure(go.Scatter(x=xs, y=ys, mode="lines", line=dict(color=BASE, width=1.3), hoverinfo="skip"))
        frame(fig, x0, x1, y0, y1, width, height)
        png = fig.to_image(format="png", width=width, height=height)
        _backgrounds[key] = "data:image/png;base64," + base64.b64encode(png).decode()
    return _backgrounds[key]


def frame(fig, x0, x1, y0, y1, width, height, row=None, col=None):
    fig.update_xaxes(range=[x0, x1], visible=False, fixedrange=True, row=row, col=col)
    fig.update_yaxes(range=[y0, y1], visible=False, fixedrange=True, row=row, col=col)
    fig.update_layout(width=width, height=height, margin=dict(l=0, r=0, t=0, b=0), paper_bgcolor=BG,
                      plot_bgcolor=BG, showlegend=False, font=FONT)


def size_for(sm, width):
    (x0, x1), (y0, y1) = extent(sm)
    return width, round(width * (y1 - y0) / (x1 - x0))


def glow_line(xs, ys, glow, core, glow_width, core_width, opacity=1.0):
    return [go.Scatter(x=xs, y=ys, mode="lines", hoverinfo="skip",
                       line=dict(color=glow, width=glow_width), opacity=0.22 * opacity),
            go.Scatter(x=xs, y=ys, mode="lines", hoverinfo="skip",
                       line=dict(color=core, width=core_width), opacity=opacity)]


def dot(space, node, colour, scale=1.0):
    x, y = space.xy(node)
    return [go.Scatter(x=[x], y=[y], mode="markers", hoverinfo="skip",
                       marker=dict(size=s * scale, color=colour, opacity=o, line_width=0))
            for s, o in ((44, 0.15), (26, 0.35), (13, 1.0))] + \
           [go.Scatter(x=[x], y=[y], mode="markers", hoverinfo="skip", marker=dict(size=6 * scale, color="white"))]


def picture(sm, space, explored, new, routes, dim, goals, scale=1.0):
    """The traces of one frame: explored streets (the newest brighter), found routes, the end points."""
    tr = []
    if explored:
        tr += glow_line(*lines_xy(space, explored), GLOW, CORE, 7 * scale, 1.4 * scale, opacity=dim)
    if new:
        tr += glow_line(*lines_xy(space, new), NEW_GLOW, NEW_CORE, 10 * scale, 2.0 * scale)
    for route, bright in routes:
        tr += glow_line(*lines_xy(space, list(zip(route, route[1:]))), ROUTE_GLOW, ROUTE_CORE,
                        (14 if bright else 9) * scale, (3.5 if bright else 1.8) * scale, opacity=1 if bright else 0.55)
    for g in (sm.goals if goals else [sm.goal]):
        tr += dot(sm, g, GOALS if goals else GOAL, scale)
    tr += dot(sm, sm.start, START, scale)
    return tr


def corner_text(fig, sm, top=None, sub=None, size=1.0):
    box = dict(bgcolor="rgba(0,0,0,0.6)", borderpad=3)    # keeps the text readable over glowing streets
    fig.add_annotation(text=sm.label, x=0.02, y=0.02, xref="paper", yref="paper", xanchor="left", yanchor="bottom",
                       showarrow=False, font=dict(size=26 * size, color="#E6E6E6"), **box)
    fig.add_annotation(text=CREDIT, x=0.99, y=0.01, xref="paper", yref="paper", xanchor="right", yanchor="bottom",
                       showarrow=False, font=dict(size=12 * size, color="#8A8A8A"))
    if top:
        fig.add_annotation(text=f"<b>{top}</b>", x=0.02, y=0.985, xref="paper", yref="paper", xanchor="left",
                           yanchor="top", showarrow=False, font=dict(size=24 * size, color="#E6E6E6"), **box)
    if sub:
        fig.add_annotation(text=sub, x=0.02, y=0.94, xref="paper", yref="paper", xanchor="left", yanchor="top",
                           showarrow=False, font=dict(size=20 * size, color=TEXT), **box)


def base_figure(sm, width):
    w, h = size_for(sm, width)
    (x0, x1), (y0, y1) = extent(sm)
    fig = go.Figure()
    frame(fig, x0, x1, y0, y1, w, h)
    fig.add_layout_image(source=background(sm, w, h), xref="x", yref="y", x=x0, y=y1, sizex=x1 - x0, sizey=y1 - y0,
                         sizing="stretch", layer="below")
    return fig


# ---------------------------------------------------------------- replaying the log

def edge_states(log, cuts, tree_only=False):
    """Replay the log; after each position in cuts return the edges explored so far in this round (in order),
    the routes found so far, the visit count and the round text. tree_only keeps only moves that improved a node."""
    edges, seen, routes, visits, round_text = [], set(), [], 0, ""
    out, cuts, i = [], sorted(cuts), 0
    for k, e in enumerate(log, 1):
        if e[0] == "round":
            edges, seen, round_text = [], set(), e[1]
        elif e[0] == "visit":
            visits += 1
        elif e[0] == "look" and (e[3] or not tree_only):
            key = frozenset(e[1:3])
            if key not in seen:
                seen.add(key)
                edges.append((e[1], e[2]))
        elif e[0] == "route":
            routes.append(e[1])
        while i < len(cuts) and cuts[i] == k:
            out.append(dict(edges=list(edges), routes=list(routes), visits=visits, round=round_text))
            i += 1
    return out


def first_looks(log):
    """Log positions (1-based) where a new street was explored for the first time."""
    seen, out = set(), []
    for k, e in enumerate(log, 1):
        if e[0] == "look" and frozenset(e[1:3]) not in seen:
            seen.add(frozenset(e[1:3]))
            out.append(k)
    return out


def cuts_for(log, frames):
    looks = [k for k, e in enumerate(log, 1) if e[0] == "look"]
    step = max(1, math.ceil(len(looks) / frames))
    cuts = set(looks[step - 1::step]) | {k for k, e in enumerate(log, 1) if e[0] == "route"}
    ends = [k - 1 for k, e in enumerate(log, 1) if e[0] == "round" and k > 1]
    cuts |= set(ends[:: max(1, math.ceil(len(ends) / frames))])
    cuts.add(len(log))
    return sorted(c for c in cuts if c > 0)


# ---------------------------------------------------------------- what run.py calls

def preview(sm, out, width=900):
    """The map alone: streets, start, goal, the multi-goal goals and the label (data/<name>.png)."""
    fig = base_figure(sm, width)
    fig.add_traces([t for g in sm.goals for t in dot(sm, g, GOALS, 0.8)] + dot(sm, sm.goal, GOAL) + dot(sm, sm.start, START))
    corner_text(fig, sm, f"{len(sm.nodes())} intersections, {len(street_edges(sm))} streets",
                "cyan: start  ·  red: goal  ·  blue: goals for multi-goal A*")
    fig.write_image(out)


def animate(sm, space, r, out, frames=48, fps=10, width=800, goals=False, tree_only=False, numbers="",
            what="explored"):
    """GIF of result r (out.gif + out_frames.png): the explored streets glow in the order the search reached them,
    then the glow fades and the route glows yellow. space is the map r ran on (sm, or a grid made from sm);
    tree_only draws only the moves that reached a node (for grids, where every cell has 8 moves); numbers is the
    text of the last frames; what names the count while the search runs."""
    cuts = cuts_for(r.log, frames)
    states = edge_states(r.log, cuts, tree_only)
    figs, prev = [], 0
    count = lambda s: (s["round"] + "  ·  " if s["round"] else "") + f"{len(s['edges']):,} {what}"
    first = base_figure(sm, width)
    first.add_traces(picture(sm, space, [], [], [], 1, goals))
    corner_text(first, sm, r.name, "from cyan to " + ("the nearest blue" if goals else "red"))
    figs.append(first)
    for s in states:
        if len(s["edges"]) < prev:
            prev = 0                       # a new round started
        fig = base_figure(sm, width)
        routes = [(rt, False) for rt in s["routes"]]
        fig.add_traces(picture(sm, space, s["edges"][:prev], s["edges"][prev:], routes, 1, goals))
        corner_text(fig, sm, r.name, count(s))
        figs.append(fig)
        prev = len(s["edges"])
    last = states[-1]
    for k, dim in enumerate((0.75, 0.5, 0.3, 0.3)):  # the glow fades, the route appears
        fig = base_figure(sm, width)
        fig.add_traces(picture(sm, space, last["edges"], [], [(r.route, True)] if k else [], dim, goals))
        corner_text(fig, sm, r.name, numbers or f"{len(last['edges']):,} explored  ·  route {r.length:,.0f} m")
        figs.append(fig)
    holds = [fps] + [1] * (len(figs) - 2) + [fps * 4]
    keys = sorted({0, len(states) // 3, 2 * len(states) // 3, len(figs) - 1})
    gifkit.make_gif(figs, out, fps=fps, holds=holds, keys=keys, cols=2, width=width)


def race(sm, results, out, frames=50, fps=10, cols=3, width=1200, fmt=lambda r: f"{r.length / 1000:.2f} km"):
    """The searches side by side on one clock (one explored street each per tick); each map is labelled with its
    explored-street count and, once it is done, its route (fmt writes the route's cost)."""
    rows = math.ceil(len(results) / cols)
    gap, top = 10, 64
    w = (width - (cols - 1) * gap) // cols
    _, h = size_for(sm, w)
    H = rows * (h + top) + (rows - 1) * gap
    (x0, x1), (y0, y1) = extent(sm)
    firsts = [first_looks(r.log) for r in results]          # where each search explored its 1st, 2nd, ... street
    totals = [len(f) for f in firsts]
    ticks = sorted({max(1, round(max(totals) * k / frames)) for k in range(1, frames + 1)})
    states = [edge_states(r.log, [f[t - 1] if t < len(f) else len(r.log) for t in ticks])
              for r, f in zip(results, firsts)]
    bg = background(sm, w, h)
    figs = []
    for t in range(len(ticks) + 1):
        fig = make_subplots(rows=rows, cols=cols, horizontal_spacing=gap / width,
                            vertical_spacing=(top + gap) / (H - top), subplot_titles=[" "] * len(results))
        for i, r in enumerate(results):
            row, col = i // cols + 1, i % cols + 1
            s = states[i][t - 1] if t else dict(edges=[], routes=[])
            done = t > 0 and len(s["edges"]) >= totals[i]
            for tr in picture(sm, sm, s["edges"], [], [(r.route, True)] if done else [], 0.6 if done else 1,
                              False, scale=0.5):
                fig.add_trace(tr, row=row, col=col)
            frame(fig, x0, x1, y0, y1, width, H, row=row, col=col)
            sub = f"{len(s['edges']):,} explored" + (f" · {fmt(r)}" if done else "")
            fig.layout.annotations[i].update(text=f"<b>{r.name}</b><br>{sub}", font=dict(size=19, color="#E6E6E6"))
            n = "" if i == 0 else str(i + 1)
            fig.add_layout_image(source=bg, xref=f"x{n}", yref=f"y{n}", x=x0, y=y1, sizex=x1 - x0, sizey=y1 - y0,
                                 sizing="stretch", layer="below")
        fig.update_layout(width=width, height=H, margin=dict(l=0, r=0, t=top, b=0))
        fig.add_annotation(text=f"{sm.label}  ·  {CREDIT}", x=1, y=-0.0, xref="paper", yref="paper", xanchor="right",
                           yanchor="bottom", showarrow=False, font=dict(size=12, color="#8A8A8A"))
        figs.append(fig)
    holds = [fps] + [1] * (len(figs) - 2) + [fps * 5]
    gifkit.make_gif(figs, out, fps=fps, holds=holds, keys=[0, len(figs) // 3, 2 * len(figs) // 3, len(figs) - 1],
                    cols=2, width=width)


def interactive(sm, results, out, bins=10):
    """One Plotly HTML page: pick a search from the menu; its explored streets are coloured by the order it reached
    them (dark red first, pale yellow last), with its route on top."""
    colours = ["#5A0F0F", "#7A1A0A", "#9A2A08", "#BA3F06", "#D65A05", "#EA7A10", "#F49A2A", "#F8B84A", "#FBD375",
               "#FDEBA8"][:bins]
    (x0, x1), (y0, y1) = extent(sm)
    fig = go.Figure()
    xs, ys = lines_xy(sm, street_edges(sm))
    fig.add_trace(go.Scatter(x=xs, y=ys, mode="lines", line=dict(color=BASE, width=1), hoverinfo="skip", name="streets"))
    groups = []
    for i, r in enumerate(results):
        edges = edge_states(r.log, [len(r.log)])[0]["edges"]
        ids = []
        for b in range(bins):
            part = edges[b * len(edges) // bins:(b + 1) * len(edges) // bins]
            px, py = lines_xy(sm, part)
            fig.add_trace(go.Scatter(x=px.round(1), y=py.round(1), mode="lines",
                                     line=dict(color=colours[b], width=2), visible=i == 0, hoverinfo="skip",
                                     name=f"explored {100 * b // bins}–{100 * (b + 1) // bins} %"))
            ids.append(len(fig.data) - 1)
        rx, ry = lines_xy(sm, list(zip(r.route, r.route[1:])))
        fig.add_trace(go.Scatter(x=rx, y=ry, mode="lines", line=dict(color=ROUTE_GLOW, width=5), visible=i == 0,
                                 name=f"route {r.length:,.0f} m"))
        ids.append(len(fig.data) - 1)
        groups.append((r, ids))
    for node, colour, name in [(sm.start, START, "start"), (sm.goal, GOAL, "goal")]:
        x, y = sm.xy(node)
        fig.add_trace(go.Scatter(x=[x], y=[y], mode="markers", marker=dict(size=14, color=colour), name=name))
    fixed = [0, len(fig.data) - 2, len(fig.data) - 1]
    buttons = []
    for r, ids in groups:
        vis = [k in ids or k in fixed for k in range(len(fig.data))]
        n = len(edge_states(r.log, [len(r.log)])[0]["edges"])
        buttons.append(dict(label=r.name, method="update",
                            args=[{"visible": vis}, {"title.text": f"{r.name}: {n:,} streets explored, "
                                                                   f"route {r.length:,.0f} m"}]))
    r0 = groups[0][0]
    fig.update_layout(updatemenus=[dict(buttons=buttons, x=0, y=1.0, xanchor="left", yanchor="bottom",
                                        bgcolor="#222", font=dict(color="#EEE"))],
                      title=dict(text=buttons[0]["args"][1]["title.text"], x=0.02, y=0.985, font=dict(size=16)),
                      paper_bgcolor=BG, plot_bgcolor=BG, font=dict(color=TEXT), height=760,
                      margin=dict(l=10, r=10, t=90, b=30), legend=dict(font=dict(size=11), bgcolor="rgba(0,0,0,0)"),
                      annotations=[dict(text=f"{sm.label} · {CREDIT}", x=1, y=0, xref="paper", yref="paper",
                                        xanchor="right", yanchor="top", showarrow=False, font=dict(size=11))])
    fig.update_xaxes(range=[x0, x1], visible=False)
    fig.update_yaxes(range=[y0, y1], visible=False, scaleanchor="x")
    js = Path(__file__).resolve().parents[2] / "tools" / "plotly.min.js"   # the repo's one copy of plotly.js
    src = os.path.relpath(js, Path(out).resolve().parent) if js.exists() else "cdn"
    fig.write_html(out, include_plotlyjs=src, full_html=True)

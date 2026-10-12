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
    """Replay the log; after each position in cuts return the edges explored so far in this round (in order, each
    once, for drawing), how many were explored (counted afresh after each found route, so separate runs add up),
    the routes found so far, the visit count and the round text. tree_only keeps only moves that improved a node."""
    edges, drawn, seen, explored, routes, visits, round_text = [], set(), set(), 0, [], 0, ""
    out, cuts, i = [], sorted(cuts), 0
    for k, e in enumerate(log, 1):
        if e[0] == "round":
            edges, drawn, seen, explored, round_text = [], set(), set(), 0, e[1]
        elif e[0] == "visit":
            visits += 1
        elif e[0] == "look" and (e[3] or not tree_only):
            key = frozenset(e[1:3])
            if key not in seen:
                seen.add(key)
                explored += 1
            if key not in drawn:
                drawn.add(key)
                edges.append((e[1], e[2]))
        elif e[0] == "route":
            routes.append(e[1])
            seen = set()                   # the next run counts its streets afresh
        while i < len(cuts) and cuts[i] == k:
            out.append(dict(edges=list(edges), explored=explored, routes=list(routes), visits=visits,
                            round=round_text))
            i += 1
    return out


def first_looks(log):
    """Log positions (1-based) where the explored count of edge_states goes up: the 1st, 2nd, ... street."""
    seen, out = set(), []
    for k, e in enumerate(log, 1):
        if e[0] in ("round", "route"):
            seen = set()
        elif e[0] == "look" and frozenset(e[1:3]) not in seen:
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
    corner_text(fig, sm, f"{len(sm.nodes()):,} intersections",
                f"{len(street_edges(sm)):,} streets  ·  cyan: start  ·  red: goal  ·  blue: goals for multi-goal A*")
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
    count = lambda s: (s["round"] + "  ·  " if s["round"] else "") + f"{s['explored']:,} {what}"
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
        corner_text(fig, sm, r.name, numbers or f"{last['explored']:,} explored  ·  route {r.length:,.0f} m")
        figs.append(fig)
    holds = [fps] + [1] * (len(figs) - 2) + [fps * 4]
    keys = sorted({0, len(states) // 3, 2 * len(states) // 3, len(figs) - 1})
    gifkit.make_gif(figs, out, fps=fps, holds=holds, keys=keys, cols=2, width=width)


def race(sm, results, out, frames=50, fps=10, cols=3, width=1200, fmt=lambda r: f"{r.length / 1000:.2f} km",
         goals=False, spaces=None):
    """The searches side by side on one clock (one explored street each per tick); each map is labelled with its
    explored-street count (separate runs added up) and, once it is done, its route (fmt writes the route's cost).
    goals=True draws the multi-goal goals instead of the goal. spaces[i] draws result i's moves (default: the
    streets; Shortcuts for a contraction hierarchy)."""
    spaces = spaces or [sm] * len(results)
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
            s = states[i][t - 1] if t else dict(edges=[], routes=[], explored=0)
            done = t > 0 and s["explored"] >= totals[i]
            routes = [(rt, False) for rt in s["routes"]] + ([(r.route, True)] if done else [])
            for tr in picture(sm, spaces[i], s["edges"], [], routes, 0.6 if done else 1, goals, scale=0.5):
                fig.add_trace(tr, row=row, col=col)
            frame(fig, x0, x1, y0, y1, width, H, row=row, col=col)
            sub = f"{s['explored']:,} explored" + (f" · {fmt(r)}" if done else "")
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


def band_corner(sm, fs, route, hist, band, out, pad=12.0, width=800, fps=3):
    """The sampling project's elastic band rounding one corner of a street route, one solve per frame: the street
    cells of fs (dark orange squares), the route (yellow, dashed) and the band (cyan, glowing)."""
    x0, x1 = route[:, 0].min() - pad, route[:, 0].max() + pad
    y0, y1 = route[:, 1].min() - pad, route[:, 1].max() + pad
    height = round(width * (y1 - y0) / (x1 - x0))
    rows, cols = fs.grid.free.shape
    xs, ys = np.arange(cols) * fs.cell, np.arange(rows) * fs.cell   # cell centres; row 0 of the grid is the top
    keep_x, keep_y = (xs > x0 - fs.cell) & (xs < x1 + fs.cell), (ys > y0 - fs.cell) & (ys < y1 + fs.cell)
    cells = go.Heatmap(x=xs[keep_x], y=ys[keep_y], z=fs.grid.free[::-1][np.ix_(keep_y, keep_x)].astype(float),
                       colorscale=[[0, BG], [1, "#3A1C06"]], showscale=False, hoverinfo="skip")
    length = lambda P: float(np.sum(np.hypot(*np.diff(P, axis=0).T)))
    figs = []
    for k in range(len(hist) + 1):
        P = band if k == len(hist) else hist[k][0]
        fig = go.Figure(cells)
        frame(fig, x0, x1, y0, y1, width, height)
        fig.add_trace(go.Scatter(x=route[:, 0], y=route[:, 1], mode="lines", hoverinfo="skip",
                                 line=dict(color=ROUTE_GLOW, width=2, dash="dash")))
        fig.add_traces(glow_line(P[:, 0], P[:, 1], START, "#DDFBFF", 12, 3))
        fig.add_trace(go.Scatter(x=P[:, 0], y=P[:, 1], mode="markers", hoverinfo="skip",
                                 marker=dict(size=4, color="#DDFBFF")))
        top = "Elastic band on a street corner"
        sub = ("the shortest route's first corner  ·  dark orange: street cells" if k == 0 else
               f"solve {k} of {len(hist)}  ·  {length(route):.0f} m → {length(P):.1f} m" if k < len(hist) else
               f"{len(hist)} solves  ·  {length(route):.0f} m → {length(P):.1f} m  ·  dark orange: street cells")
        corner_text(fig, sm, top, sub)
        figs.append(fig)
    holds = [fps * 2] + [2] * (len(figs) - 2) + [fps * 5]
    gifkit.make_gif(figs, out, fps=fps, holds=holds, keys=[0, len(figs) // 2, len(figs) - 1], cols=3, width=width)


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


# ---------------------------------------------------------------- replanning and contraction hierarchies (chapter RO-06)
FROM_GOAL_GLOW, FROM_GOAL_CORE = "#4FA8FF", "#CFE6FF"   # the search back from the goal
CLOSED, SHORTCUT = "#FF2A2A", "#3DDC84"


class Shortcuts:
    """The street map with a contraction hierarchy's shortcuts drawn as straight lines between their two ends."""

    def __init__(self, sm, ch):
        self.sm, self.mid = sm, ch["mid"]

    def xy(self, node):
        return self.sm.xy(node)

    def edge_xy(self, a, b):
        return [self.xy(a), self.xy(b)] if (a, b) in self.mid else self.sm.edge_xy(a, b)


def looked(log, side=None):
    """The moves a search looked at, in order, each once (only those of one side if side is given)."""
    seen, out = set(), []
    for e in log:
        if e[0] == "look" and (side is None or e[4] == side) and frozenset(e[1:3]) not in seen:
            seen.add(frozenset(e[1:3]))
            out.append((e[1], e[2]))
    return out


def edges_of(route):
    return list(zip(route, route[1:]))


def replanning(sm, run, closed, out, fps=10, width=1200, drive_frames=10, search_frames=30):
    """The closure drive as a GIF, D* Lite (left) against A* from scratch (right): the car (cyan) drives its route;
    when the streets in `closed` close they turn red, and each method's work glows on one clock, one more street each
    per tick; then the new route glows and the car drives on."""
    e = run.notes["replans"][0]
    move, first = e["move"], run.notes["first"]
    names = ["D* Lite: repairs its numbers", "A* from scratch"]
    work = [looked(e["dstar"].log), looked(e["astar"].log)]
    gap, top = 10, 64
    w = (width - gap) // 2
    _, h = size_for(sm, w)
    (x0, x1), (y0, y1) = extent(sm)
    bg = background(sm, w, h)
    longest = max(len(x) for x in work)
    frames = []                                                 # (car's move, ticks of the repair, phase)
    frames += [(round(k * move / drive_frames), 0, "drive") for k in range(drive_frames + 1)]
    frames += [(move, round(k * longest / search_frames), "repair") for k in range(1, search_frames + 1)]
    rest = len(run.route) - 1 - move
    frames += [(move + round(k * rest / drive_frames), longest, "on") for k in range(drive_frames + 1)]
    figs, holds = [], []
    for car, tick, phase in frames:
        fig = make_subplots(rows=1, cols=2, horizontal_spacing=gap / width, subplot_titles=[" ", " "])
        for i in range(2):
            tr = []
            if phase != "drive":
                tr += glow_line(*lines_xy(sm, work[i][:tick]), GLOW, CORE, 5, 1.0, opacity=1 if phase == "repair"
                                else 0.5)
                tr += glow_line(*lines_xy(sm, closed), CLOSED, CLOSED, 16, 4)
            plan = first[i].route if phase == "drive" else [e["pos"]] + (e["dstar"], e["astar"])[i].route[1:]
            tr += glow_line(*lines_xy(sm, edges_of(plan)), ROUTE_GLOW, ROUTE_CORE, 9, 1.8,
                            opacity=1 if phase == "on" else 0.5)
            tr += glow_line(*lines_xy(sm, edges_of(run.route[:car + 1])), START, START, 10, 2.5)
            tr += dot(sm, sm.goal, GOAL, 0.6) + dot(sm, run.route[car], START, 0.7)
            for t in tr:
                fig.add_trace(t, row=1, col=i + 1)
            frame(fig, x0, x1, y0, y1, width, h + top, row=1, col=i + 1)
            fig.add_layout_image(source=bg, xref="x" if i == 0 else "x2", yref="y" if i == 0 else "y2", x=x0, y=y1,
                                 sizex=x1 - x0, sizey=y1 - y0, sizing="stretch", layer="below")
            plan_r = (e["dstar"], e["astar"])[i]
            if phase == "drive":
                sub = f"the plan: {first[i].length:,.0f} m  ·  first plan {first[i].visited:,} intersections"
            elif phase == "repair":
                sub = f"closed (red)  ·  {min(tick, len(work[i])):,} streets explored"
            else:
                sub = (f"{plan_r.visited:,} intersections, {len(work[i]):,} streets  ·  "
                       f"{plan_r.length:,.0f} m to go")
            fig.layout.annotations[i].update(text=f"<b>{names[i]}</b><br>{sub}", font=dict(size=19, color="#E6E6E6"))
        fig.update_layout(width=width, height=h + top, margin=dict(l=0, r=0, t=top, b=0))
        fig.add_annotation(text=f"{sm.label}  ·  {CREDIT}", x=1, y=0, xref="paper", yref="paper", xanchor="right",
                           yanchor="bottom", showarrow=False, font=dict(size=12, color="#8A8A8A"))
        figs.append(fig)
        holds.append(1)
    holds[0], holds[drive_frames], holds[drive_frames + search_frames], holds[-1] = fps, fps * 2, fps * 2, fps * 4
    keys = [drive_frames, drive_frames + search_frames // 2, drive_frames + search_frames, len(figs) - 1]
    gifkit.make_gif(figs, out, fps=fps, holds=holds, keys=keys, cols=2, width=width)


def hierarchy(sm, ch, q, out, fps=10, width=800, build_frames=16, search_frames=30, fmt=lambda r: f"{r.length:.0f}"):
    """A contraction hierarchy as a GIF: the shortcuts (green, straight lines) appear as the intersections are
    removed, least important first; then the query's two searches that only climb glow one arc at a time, from the
    start (orange) and back from the goal (blue); then the route glows yellow."""
    space = Shortcuts(sm, ch)
    n = len(ch["order"])
    figs, holds = [], []

    def shortcut_traces(upto, opacity):
        chords = [(u, w) for u, w, _, k in ch["shortcuts"] if k < upto]
        return glow_line(*lines_xy(space, chords), SHORTCUT, SHORTCUT, 4, 0.8, opacity) if chords else []

    for k in range(build_frames + 1):
        upto = round(n * k / build_frames)
        fig = base_figure(sm, width)
        fig.add_traces(shortcut_traces(upto, 0.6) + dot(sm, sm.goal, GOAL) + dot(sm, sm.start, START))
        count = sum(1 for *_, j in ch["shortcuts"] if j < upto)
        corner_text(fig, sm, "Contraction hierarchy: adding shortcuts",
                    f"{upto:,} of {n:,} intersections removed  ·  {count:,} shortcuts")
        figs.append(fig)
        holds.append(1)
    sides = [looked(q.log, 0), looked(q.log, 1)]
    longest = max(len(x) for x in sides)
    for k in range(1, search_frames + 1):
        t = round(k * longest / search_frames)
        fig = base_figure(sm, width)
        tr = shortcut_traces(n, 0.08)
        tr += glow_line(*lines_xy(space, sides[0][:t]), GLOW, CORE, 4, 1.0) if sides[0][:t] else []
        tr += glow_line(*lines_xy(space, sides[1][:t]), FROM_GOAL_GLOW, FROM_GOAL_CORE, 4, 1.0) if sides[1][:t] else []
        fig.add_traces(tr + dot(sm, sm.goal, GOAL) + dot(sm, sm.start, START))
        corner_text(fig, sm, "Two searches that only climb",
                    f"from the start (orange) {min(t, len(sides[0]))}  ·  back from the goal (blue) "
                    f"{min(t, len(sides[1]))} arcs")
        figs.append(fig)
        holds.append(1)
    fig = base_figure(sm, width)
    tr = shortcut_traces(n, 0.08)
    tr += glow_line(*lines_xy(space, sides[0]), GLOW, CORE, 4, 1.0, 0.3)
    tr += glow_line(*lines_xy(space, sides[1]), FROM_GOAL_GLOW, FROM_GOAL_CORE, 4, 1.0, 0.3)
    tr += glow_line(*lines_xy(sm, edges_of(q.route)), ROUTE_GLOW, ROUTE_CORE, 14, 3.5)
    fig.add_traces(tr + dot(sm, q.notes["top"], "#FFFFFF", 0.6) + dot(sm, sm.goal, GOAL) + dot(sm, sm.start, START))
    corner_text(fig, sm, "Contraction hierarchy",
                f"{q.notes['taken'][0]} + {q.notes['taken'][1]} intersections taken off  ·  route {fmt(q)}")
    figs.append(fig)
    holds[0], holds[build_frames] = fps, fps * 2
    holds.append(fps * 4)
    gifkit.make_gif(figs, out, fps=fps, holds=holds, keys=[build_frames // 2, build_frames,
                                                            build_frames + search_frames // 2, len(figs) - 1],
                    cols=2, width=width)

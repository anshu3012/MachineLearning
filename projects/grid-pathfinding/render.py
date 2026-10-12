"""Draw searches in the style of a classic grid path-finding visualiser: the floor as white squares, walls dark,
the cells a search has visited, its frontier, and the route, with the counts above the map.

It only uses the map interface (m.nodes(), m.xy(node), m.cell, m.start, m.goal, m.goals) and the search log in a
Result, so any map and any algorithm in algorithms.py can be drawn. A new algorithm needs no new drawing code."""
import math

import plotly.graph_objects as go
from plotly.subplots import make_subplots

import gifkit

WALL, FLOOR = "#555555", "#FFFFFF"
VISITED, VISITED_2, FRONTIER, SCANNED = "#AFEEEE", "#D9C8F5", "#98FB98", "#FFF1A8"
ROUTE, OLD_ROUTE, PATH = "#F5B700", "#C9A43A", "#FF7F0E"
START, GOAL, GOALS = "#1DB954", "#E8412C", "#2F6FDE"
FONT = dict(family=gifkit.FONT["family"], size=22, color="#222222")
TOP = 96                                   # pixels above the map for the title and the counts


# ---------------------------------------------------------------- replaying the log

def snapshots(log, cuts):
    """Replay the log and return the state of the search after each position in cuts (sorted)."""
    visited, frontier, scanned, parent, routes = {}, {}, set(), {}, []
    round_text, rounds, visits, last = "", 0, 0, None
    out, cuts, i = [], sorted(cuts), 0
    for k, e in enumerate(log, 1):
        kind = e[0]
        if kind == "round":
            visited, frontier, scanned, round_text, rounds = {}, {}, set(), e[1], rounds + 1
        elif kind == "visit":
            visited[e[1]] = e[2]
            frontier.pop(e[1], None)
            visits, last = visits + 1, e[1]
        elif kind == "look" and e[3]:
            frontier[e[2]] = e[4]
            parent[e[2]] = e[1]
        elif kind == "scan":
            scanned.add(e[1])
        elif kind == "route":
            routes.append((e[1], e[2]))
        while i < len(cuts) and cuts[i] == k:
            path, n = [], last
            while n is not None and len(path) <= len(parent) + 1:   # the branch the search is on now
                path.append(n)
                n = parent.get(n)
            out.append(dict(visited=dict(visited), frontier=dict(frontier), scanned=set(scanned), routes=list(routes),
                            round=round_text, rounds=rounds, visits=visits, path=path[::-1]))
            i += 1
    return out


def frame_cuts(log, frames):
    """Log positions to draw: about `frames` steps spread over the visits, plus the end of every round."""
    visits = [k for k, e in enumerate(log, 1) if e[0] == "visit"]
    step = max(1, math.ceil(len(visits) / frames))
    cuts = set(visits[step - 1::step]) | {k for k, e in enumerate(log, 1) if e[0] == "route"} \
        | {k - 1 for k, e in enumerate(log, 1) if e[0] == "round" and k > 1}
    cuts.add(len(log))
    return sorted(c for c in cuts if c > 0)


# ---------------------------------------------------------------- drawing one map

def extent(m):
    xs, ys = zip(*(m.xy(n) for n in m.nodes()))
    pad = 1.5 * m.cell                     # one cell of wall all round
    return (min(xs) - pad, max(xs) + pad), (min(ys) - pad, max(ys) + pad)


def squares(m, nodes, colour, px, **kw):
    xs, ys = zip(*(m.xy(n) for n in nodes)) if nodes else ((), ())
    return go.Scatter(x=xs, y=ys, mode="markers", hoverinfo="skip", showlegend=False,
                      marker=dict(symbol="square", size=max(px - 2, 2), color=colour, line_width=0, **kw))


def line(m, route, colour, width, dash=None):
    xs, ys = zip(*(m.xy(n) for n in route)) if route else ((), ())
    return go.Scatter(x=xs, y=ys, mode="lines", hoverinfo="skip", showlegend=False,
                      line=dict(color=colour, width=width, dash=dash))


def map_traces(m, state, px, goals=False, route=None, path=False):
    """The traces for one picture of the map: floor, scanned, frontier, visited, routes, start and goal."""
    state = state or dict(visited={}, frontier={}, scanned=set(), routes=[], path=[])
    v = state["visited"]
    traces = [squares(m, m.nodes(), FLOOR, px),
              squares(m, [n for n in state["scanned"] if n not in v], SCANNED, px),
              squares(m, [n for n in state["frontier"] if n not in v], FRONTIER, px),
              squares(m, [n for n, side in v.items() if side == 0], VISITED, px),
              squares(m, [n for n, side in v.items() if side == 1], VISITED_2, px)]
    for old, _ in state["routes"][:-1] if route is None else state["routes"]:
        traces.append(line(m, old, OLD_ROUTE, max(2, px / 6), "dot"))
    if state["routes"] and route is None:
        traces.append(line(m, state["routes"][-1][0], ROUTE, max(3, px / 4)))
    if path and state["path"]:
        traces.append(line(m, state["path"], PATH, max(3, px / 4)))
    if route:
        traces.append(line(m, route, ROUTE, max(3, px / 3)))
    if goals:
        traces.append(squares(m, list(m.goals), GOALS, px))
    else:
        traces.append(squares(m, [m.goal], GOAL, px))
    traces.append(squares(m, [m.start], START, px))
    return traces


def single_figure(m, px):
    (x0, x1), (y0, y1) = extent(m)
    w, h = round((x1 - x0) / m.cell * px), round((y1 - y0) / m.cell * px)
    fig = go.Figure()
    fig.update_layout(width=w, height=h + TOP, margin=dict(l=0, r=0, t=TOP, b=0), paper_bgcolor="white",
                      plot_bgcolor=WALL, font=FONT)
    fig.update_xaxes(range=[x0, x1], visible=False, fixedrange=True)
    fig.update_yaxes(range=[y0, y1], visible=False, fixedrange=True)
    return fig


def title(fig, top, bottom):
    fig.add_annotation(text=f"<b>{top}</b>", x=0.01, y=1, xref="paper", yref="paper", yshift=TOP - 8,
                       xanchor="left", yanchor="top", showarrow=False, font=dict(size=26))
    fig.add_annotation(text=bottom, x=0.01, y=1, xref="paper", yref="paper", yshift=TOP / 2 - 6,
                       xanchor="left", yanchor="top", showarrow=False, font=dict(size=22, color="#333333"))


def px_for(m, width=820):
    (x0, x1), _ = extent(m)
    return max(6, int(width / ((x1 - x0) / m.cell)))


def counts(r, s, done):
    if s["round"]:
        text = f"{s['round']}  ·  visits so far {s['visits']}"
    else:
        text = f"visited {len(s['visited'])}  ·  frontier {len(s['frontier'])}"
        if r.notes.get("scanned") is not None:
            text += f"  ·  cells scanned {len(s['scanned'])}"
    if done:
        text += f"  ·  route {r.length:.1f} m" if r.route else "  ·  no route"
    return text


# ---------------------------------------------------------------- what run.py calls

def preview(m, out, px=None):
    """A picture of the map: floor, walls, start (S), goal (G), the multi-goal goals (blue) and a metre scale."""
    px = px or px_for(m)
    fig = single_figure(m, px)
    fig.add_traces(map_traces(m, None, px)[:1] + [squares(m, list(m.goals), GOALS, px),
                                                    squares(m, [m.goal], GOAL, px), squares(m, [m.start], START, px)])
    for n, t in [(m.start, "S"), (m.goal, "G")]:
        fig.add_annotation(x=m.xy(n)[0], y=m.xy(n)[1], text=f"<b>{t}</b>", showarrow=False,
                           font=dict(size=max(12, px * 0.7), color="white"))
    (x0, x1), (y0, y1) = extent(m)
    bar = 5 * m.cell if (x1 - x0) < 60 * m.cell else 10 * m.cell
    fig.add_shape(type="line", x0=x1 - m.cell - bar, x1=x1 - m.cell, y0=y0 + 0.75 * m.cell, y1=y0 + 0.75 * m.cell,
                  line=dict(color="white", width=5))
    fig.add_annotation(x=x1 - m.cell - bar, y=y0 + 0.75 * m.cell, text=f"{bar:g} m ", xanchor="right",
                       showarrow=False, font=dict(size=16, color="white"))
    title(fig, m.label, f"cells of {m.cell:g} m  ·  S start  ·  G goal  ·  blue: goals for multi-goal A*")
    fig.write_image(out)


def animate(m, r, out, frames=45, fps=8, goals=False, path=False):
    """A GIF of search result r on map m (out.gif and out_frames.png): visited cells and frontier growing, then the
    route. goals=True draws the multi-goal goals; path=True draws the branch a depth-first search is on."""
    px = px_for(m)
    cuts = frame_cuts(r.log, frames)
    states = snapshots(r.log, cuts)
    figs = []
    for k, s in enumerate([None] + states):
        done = k == len(states)
        fig = single_figure(m, px)
        s0 = s or dict(visited={}, frontier={}, scanned=set(), routes=[], path=[], round="", visits=0)
        fig.add_traces(map_traces(m, s, px, goals=goals, route=r.route if done else None, path=path and not done))
        title(fig, r.name, counts(r, s0, done) if s else f"{m.label}: from green to " + ("the nearest blue" if goals else "red"))
        figs.append(fig)
    holds = [fps] + [1] * (len(figs) - 2) + [fps * 4]
    keys = sorted({0, len(figs) // 3, 2 * len(figs) // 3, len(figs) - 1})
    gifkit.make_gif(figs, out, fps=fps, holds=holds, keys=keys, cols=2, width=figs[0].layout.width)


def race(m, results, out, frames=50, fps=8, cols=3):
    """Several searches side by side, one visit each per tick, so the one that needs fewer visits finishes first.
    Each map is labelled with its visit count and its route length."""
    rows = math.ceil(len(results) / cols)
    (x0, x1), (y0, y1) = extent(m)
    px = max(5, int(420 / ((x1 - x0) / m.cell)))
    w, h = round((x1 - x0) / m.cell * px), round((y1 - y0) / m.cell * px)
    gap_x, gap_y, top = 12, 70, 70                     # pixels between maps, and above the first row for its labels
    W, H = cols * w + (cols - 1) * gap_x, top + rows * h + (rows - 1) * gap_y
    longest = max(r.visited for r in results)
    ticks = sorted({max(1, round(longest * k / frames)) for k in range(1, frames + 1)})
    visit_pos = [[k for k, e in enumerate(r.log, 1) if e[0] == "visit"] for r in results]
    per = [snapshots(r.log, [vp[min(t, len(vp)) - 1] for t in ticks]) for r, vp in zip(results, visit_pos)]
    figs = []
    for t in range(len(ticks) + 1):
        fig = make_subplots(rows=rows, cols=cols, horizontal_spacing=gap_x / W, vertical_spacing=gap_y / (H - top),
                            subplot_titles=[" "] * len(results))
        for i, r in enumerate(results):
            s = per[i][t - 1] if t else None
            done = s is not None and s["visits"] >= r.visited
            for tr in map_traces(m, s, px, route=r.route if done else None):
                fig.add_trace(tr, row=i // cols + 1, col=i % cols + 1)
            label = f"<b>{r.name}</b><br>visited {s['visits'] if s else 0}" + (f" · {r.length:.1f} m" if done else "")
            fig.layout.annotations[i].update(text=label, font=dict(size=20))
        fig.update_xaxes(range=[x0, x1], visible=False)
        fig.update_yaxes(range=[y0, y1], visible=False)
        fig.update_layout(width=W, height=H, margin=dict(l=0, r=0, t=top, b=0),
                          plot_bgcolor=WALL, paper_bgcolor="white", font=FONT)
        figs.append(fig)
    holds = [fps] + [1] * (len(figs) - 2) + [fps * 5]
    gifkit.make_gif(figs, out, fps=fps, holds=holds, keys=[0, len(figs) // 3, 2 * len(figs) // 3, len(figs) - 1],
                    cols=2, width=figs[0].layout.width)

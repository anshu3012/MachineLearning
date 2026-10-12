"""Draw searches in the style of a classic grid path-finding visualiser: the floor as white squares, walls dark,
the cells a search has visited, its frontier, and the route, with the counts above the map.

It only uses the map interface (m.nodes(), m.xy(node), m.cell, m.start, m.goal, m.goals) and the search log in a
Result, so any map and any algorithm in algorithms.py can be drawn. A new algorithm needs no new drawing code."""
import math

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import gifkit

WALL, FLOOR = "#555555", "#FFFFFF"
VISITED, VISITED_2, FRONTIER, SCANNED = "#AFEEEE", "#D9C8F5", "#98FB98", "#FFF1A8"
ROUTE, OLD_ROUTE, PATH = "#F5B700", "#C9A43A", "#FF7F0E"
START, GOAL, GOALS = "#1DB954", "#E8412C", "#2F6FDE"
HIDDEN, TAKEN, RAISED, ROBOT, TRAIL = "#8B5A2B", "#F4A6A6", "#E8761C", "#111111", "#7B3FA0"
VALUES = [[0, "#FFFFD9"], [0.35, "#C7E9B4"], [0.65, "#41B6C4"], [1, "#225EA8"]]   # cost-to-go: pale yellow low, blue high
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
    if m.hidden:                           # noted in the bottom wall, like the scale bar
        fig.add_traces([squares(m, list(m.hidden), HIDDEN, px)])
        fig.add_annotation(x=x0 + m.cell, y=y0 + 0.75 * m.cell, text="brown: missing from the robot's map",
                           xanchor="left", showarrow=False, font=dict(size=16, color="white"))
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


def race(m, results, out, frames=50, fps=8, cols=3, goals=False):
    """Several searches side by side, one visit each per tick, so the one that needs fewer visits finishes first.
    Each map is labelled with its visit count (all runs added up) and its route length. goals=True draws the
    multi-goal goals instead of the goal."""
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
            for tr in map_traces(m, s, px, goals=goals, route=r.route if done else None):
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


# ---------------------------------------------------------------- cost-to-go maps (chapter RO-06)

def boxes(m, nodes, colour, px, width=3):
    """Square outlines round the cells (to mark them without hiding their number)."""
    xs, ys = zip(*(m.xy(n) for n in nodes)) if nodes else ((), ())
    return go.Scatter(x=xs, y=ys, mode="markers", hoverinfo="skip", showlegend=False,
                      marker=dict(symbol="square-open", size=max(px - 3, 3), color=colour, line_width=width))


def numbered(m, V, px, vmax, nodes, numbers=True):
    """The cells in nodes coloured by their value V (pale yellow low, blue high), each with its value rounded to
    whole metres."""
    nodes = [n for n in nodes if V.get(n, math.inf) < math.inf]
    if not nodes:
        return []
    tr = [squares(m, nodes, [V[n] for n in nodes], px, colorscale=VALUES, cmin=0, cmax=vmax)]
    if numbers:
        xs, ys = zip(*(m.xy(n) for n in nodes))
        tr.append(go.Scatter(x=xs, y=ys, mode="text", text=[f"{V[n]:.0f}" for n in nodes], hoverinfo="skip",
                             showlegend=False, textfont=dict(family=FONT["family"], size=max(8, round(px * 0.5)),
                             color=["white" if V[n] > 0.62 * vmax else "#333333" for n in nodes])))
    return tr


def ends(m, px):
    """S and G as outlines, so their numbers stay readable."""
    return [boxes(m, [m.start], START, px), boxes(m, [m.goal], GOAL, px)]


def wavefront(m, V, out, frames=46, fps=8):
    """The wavefront from the goal as a GIF: frame by frame, every cell whose cost-to-go is at most t gets its
    number, t rising in equal steps until every cell is numbered."""
    px, vmax = px_for(m, 900), max(V.values())
    step = vmax / (frames - 1)
    figs = []
    for k in range(frames):
        t = k * step
        shown = [n for n in V if V[n] <= t + 1e-9]
        fig = single_figure(m, px)
        fig.add_traces([squares(m, m.nodes(), FLOOR, px)] + numbered(m, V, px, vmax, shown) + ends(m, px))
        sub = (f"all {len(V)} cells numbered  ·  S: {V[m.start]:.1f} m" if k == frames - 1 else
               f"cells within {t:.1f} m of G: {len(shown)} of {len(V)}")
        title(fig, "Wavefront from G: every cell's metres to the goal", sub)
        figs.append(fig)
    holds = [fps] + [1] * (len(figs) - 2) + [fps * 4]
    gifkit.make_gif(figs, out, fps=fps, holds=holds, keys=[0, len(figs) // 3, 2 * len(figs) // 3, len(figs) - 1],
                    cols=2, width=figs[0].layout.width)


def downhill(m, V, arrow, walks, out, fps=8, steps=12):
    """The navigation function as a GIF: the cost-to-go colours with an arrow in every cell pointing to arrow[cell],
    the neighbour with the smallest move + cost-to-go; then one robot per (name, route) in walks follows the arrows,
    one after another."""
    px, vmax = px_for(m, 900), max(V.values())
    angle = lambda a, b: math.degrees(math.atan2(m.xy(b)[0] - m.xy(a)[0], m.xy(b)[1] - m.xy(a)[1]))
    cells = list(arrow)
    xs, ys = zip(*(m.xy(n) for n in cells))
    arrows = go.Scatter(x=xs, y=ys, mode="markers", hoverinfo="skip", showlegend=False,
                        marker=dict(symbol="arrow", size=px * 0.5, angle=[angle(n, arrow[n]) for n in cells],
                                    color="#444444", line_width=0))
    colours = [gifkit.BLUE, gifkit.ORANGE, gifkit.GREEN, gifkit.PURPLE, gifkit.RED]
    base = [squares(m, m.nodes(), FLOOR, px)] + numbered(m, V, px, vmax, list(V), numbers=False) + [arrows]

    def frame(done, current, upto, sub):
        fig = single_figure(m, px)
        fig.add_traces(base + ends(m, px))
        for i, (_, route) in enumerate(walks[:done]):
            fig.add_trace(line(m, route, colours[i % 5], max(3, px / 4)))
        if current is not None:
            route = walks[current][1][:upto + 1]
            fig.add_trace(line(m, route, colours[current % 5], max(3, px / 4)))
            fig.add_trace(squares(m, [route[-1]], colours[current % 5], px, opacity=0.9))
        title(fig, "Walking downhill: every cell's arrow points to its best neighbour", sub)
        return fig

    figs, holds = [frame(0, None, 0, "arrow: the neighbour with the smallest move + its number")], [fps * 2]
    for i, (name, route) in enumerate(walks):
        length = m.route_length(route)
        marks = sorted({round(k * (len(route) - 1) / steps) for k in range(steps + 1)})
        for k in marks:
            arrived = k == len(route) - 1
            sub = (f"from {name}: {length:.1f} m, the number its cell holds ({V[route[0]]:.1f})" if arrived else
                   f"from {name}: {m.route_length(route[:k + 1]):.1f} m so far")
            figs.append(frame(i, i, k, sub))
            holds.append(fps if arrived else 1)
    figs.append(frame(len(walks), None, 0, "  ·  ".join(f"{name} {m.route_length(r):.1f} m" for name, r in walks)))
    holds.append(fps * 4)
    gifkit.make_gif(figs, out, fps=fps, holds=holds, keys=[0, len(figs) // 3, 2 * len(figs) // 3, len(figs) - 1],
                    cols=2, width=figs[0].layout.width)


def sweeps(m, record, out, fps=4):
    """Value iteration as a GIF, one frame per sweep: each cell's value (white: none yet); blue outline: it got
    its first value in this sweep; orange outline: its value fell."""
    px = px_for(m, 900)
    vmax = max(v for v in record[-1][0].values() if v < math.inf)
    figs = []
    for k, (V, first, fell) in enumerate([({m.goal: 0.0}, [], [])] + record):
        fig = single_figure(m, px)
        fig.add_traces([squares(m, m.nodes(), FLOOR, px)] + numbered(m, V, px, vmax, list(V)) + ends(m, px))
        if first:
            fig.add_trace(boxes(m, first, GOALS, px, 2))
        if fell:
            fig.add_trace(boxes(m, fell, RAISED, px, 3))
        sub = ("before the first sweep: G is 0, every other cell has no value" if k == 0 else
               f"sweep {k}: nothing changed; every value is final" if not first and not fell else
               f"sweep {k}: {len(first)} cells got a value (blue), {len(fell)} values fell (orange)")
        title(fig, "Value iteration: sweep row by row until nothing changes", sub)
        figs.append(fig)
    holds = [fps * 2] + [2] * (len(figs) - 2) + [fps * 4]
    gifkit.make_gif(figs, out, fps=fps, holds=holds, keys=[0, 1, len(figs) // 2, len(figs) - 1], cols=2,
                    width=figs[0].layout.width)


def replanning(m, run, seen_at, out, fps=6):
    """The replanning drive as a GIF, D* Lite (left) against A* from scratch (right), one frame per move. Light red:
    the cells each takes off its queue at this replan; brown: pallets seen, brown outline: pallets not seen yet;
    yellow: the plan; orange: the way driven. seen_at[move] = pallets first seen at that move."""
    first, replans = run.notes["first"], {e["move"]: e for e in run.notes["replans"]}
    cols, gap_x, top = 2, 16, 76
    (x0, x1), (y0, y1) = extent(m)
    px = max(5, int(590 / ((x1 - x0) / m.cell)))
    w, h = round((x1 - x0) / m.cell * px), round((y1 - y0) / m.cell * px)
    W, H = cols * w + gap_x, top + h
    plans, totals, seen, figs, holds = list(first), [0, 0], set(), [], []
    for move, pos in enumerate(run.route):
        e = replans.get(move)
        seen |= set(seen_at.get(move, ()))
        if e:
            plans = [e["dstar"], e["astar"]]
            totals = [totals[0] + e["dstar"].visited, totals[1] + e["astar"].visited]
        work = plans if (e or move == 0) else [None, None]
        fig = make_subplots(rows=1, cols=cols, horizontal_spacing=gap_x / W, subplot_titles=[" ", " "])
        for i, name in enumerate(["D* Lite: repairs its numbers", "A* from scratch"]):
            plan = plans[i].route
            ahead = plan[plan.index(pos):] if pos in plan else plan
            traces = [squares(m, m.nodes(), FLOOR, px)]
            if work[i] is not None:
                traces.append(squares(m, [e[1] for e in work[i].log if e[0] == "visit"], TAKEN, px))
            traces += [boxes(m, [c for c in m.hidden if c not in seen], HIDDEN, px, 2),
                       squares(m, list(seen), HIDDEN, px), squares(m, [m.goal], GOAL, px),
                       line(m, ahead, ROUTE, max(3, px / 4)), line(m, run.route[:move + 1], PATH, max(3, px / 4)),
                       squares(m, [pos], ROBOT, px)]
            for tr in traces:
                fig.add_trace(tr, row=1, col=i + 1)
            if move == 0:
                text = f"first plan: {plans[i].visited} cells taken off"
            elif e:
                text = f"replan at move {move}: {plans[i].visited} cells  ·  replans so far {totals[i]}"
            else:
                text = f"move {move}  ·  replans so far {totals[i]} cells"
            fig.layout.annotations[i].update(text=f"<b>{name}</b><br>{text}", font=dict(size=19))
        fig.update_xaxes(range=[x0, x1], visible=False)
        fig.update_yaxes(range=[y0, y1], visible=False)
        fig.update_layout(width=W, height=H, margin=dict(l=0, r=0, t=top, b=0), plot_bgcolor=WALL,
                          paper_bgcolor="white", font=FONT)
        figs.append(fig)
        holds.append(fps * 2 if (e or move == 0) else 1)
    holds[-1] = fps * 4
    keys = [0] + sorted(replans)[:2] + [len(figs) - 1]
    gifkit.make_gif(figs, out, fps=fps, holds=holds, keys=keys, cols=2, width=W)


def lrta(m, first, last, h0, out, fps=8):
    """LRTA* as a GIF: the first trial move by move (each cell shows the robot's guess of its metres to the goal,
    rounded; orange outline: a guess that was raised; purple: the way driven), then the route of the last trial,
    once nothing changes."""
    px = px_for(m, 900)
    vmax = max(h0.values())
    guess, raised, raises, figs, trail = dict(h0), set(), 0, [], []
    log = [e for e in first.log if e[0] in ("visit", "raise")] + [("visit", first.route[-1], 0)]

    def frame(V, marks, route, sub):
        fig = single_figure(m, px)
        fig.add_traces([squares(m, m.nodes(), FLOOR, px)] + numbered(m, V, px, vmax, list(V)) + ends(m, px))
        if marks:
            fig.add_trace(boxes(m, list(marks), RAISED, px, 3))
        fig.add_trace(line(m, route, TRAIL, max(2, px / 7)))
        fig.add_trace(squares(m, [route[-1]], ROBOT, px * 0.6))
        title(fig, "LRTA*: look one cell ahead, move, raise the guess", sub)
        return fig

    for e in log:
        if e[0] == "raise":
            guess[e[1]], raised, raises = e[3], raised | {e[1]}, raises + 1
            continue
        trail.append(e[1])
        figs.append(frame(guess, raised, trail, f"trial 1  ·  move {len(trail) - 1}  ·  {raises} raises"))
    figs[-1] = frame(guess, raised, trail, f"trial 1: {len(trail) - 1} moves, {first.length:.0f} m  ·  "
                                           f"{raises} raises in {len(raised)} cells")
    learned = {**h0, **last.notes["learned"]}
    changed = {n for n in learned if learned[n] > h0[n] + 1e-9}
    figs.append(frame(learned, changed, last.route, f"trial {last.notes['trial']}: no guess changes  ·  "
                                                     f"{len(last.route) - 1} moves, {last.length:.0f} m"))
    holds = [fps] + [1] * (len(figs) - 3) + [fps * 3, fps * 4]
    gifkit.make_gif(figs, out, fps=fps, holds=holds, keys=[len(figs) // 3, 2 * len(figs) // 3, len(figs) - 2,
                                                            len(figs) - 1], cols=2, width=figs[0].layout.width)


def fronts(m, runs, at, out, frames=40, fps=8, every=2.0):
    """Fronts leaving the goal at 1 m/s on a fine grid m, one panel per (name, {cell: arrival time}) in runs
    (stacked): cells coloured by arrival time once the front has passed, a dark line for the front every `every`
    seconds. at is the cell whose arrival times the last frame gives."""
    rows, cols = m.free.shape
    xs = [m.origin[0] + c * m.cell for c in range(cols)]
    ys = [m.origin[1] + (rows - 1 - r) * m.cell for r in range(rows)]     # row r of z is drawn at ys[r]
    grids = []
    for _, T in runs:
        z = np.full((rows, cols), np.nan)
        for (c, r), t in T.items():
            z[r, c] = t
        grids.append(z)
    tmax = max(np.nanmax(z) for z in grids)
    (x0, x1), (y0, y1) = (xs[0] - m.cell, xs[-1] + m.cell), (ys[-1] - m.cell, ys[0] + m.cell)
    w = 820
    h = round(w * (y1 - y0) / (x1 - x0))
    gap, top = 60, 70
    H = len(runs) * (h + top) - top + top + gap * (len(runs) - 1)
    floor = np.where(m.free, 1.0, np.nan)
    figs = []
    for k in range(frames + 1):
        t = tmax * k / frames
        fig = make_subplots(rows=len(runs), cols=1, vertical_spacing=(gap + top) / H,
                            subplot_titles=[" "] * len(runs))
        for i, ((name, T), z) in enumerate(zip(runs, grids)):
            fig.add_trace(go.Heatmap(x=xs, y=ys, z=floor, colorscale=[[0, FLOOR], [1, FLOOR]], showscale=False,
                                     hoverinfo="skip"), row=i + 1, col=1)
            fig.add_trace(go.Heatmap(x=xs, y=ys, z=np.where(z <= t, z, np.nan), colorscale=VALUES, zmin=0, zmax=tmax,
                                     showscale=False, hoverinfo="skip"), row=i + 1, col=1)
            if t >= every:
                fig.add_trace(go.Contour(x=xs, y=ys, z=np.where(z <= t + every, z, np.nan), showscale=False,
                                         showlegend=False,
                                         hoverinfo="skip", contours=dict(start=every, end=t, size=every,
                                                                         coloring="none"),
                                         line=dict(color="#333333", width=1.6)), row=i + 1, col=1)
            for node, colour in ((m.start, START), (m.goal, GOAL)):
                fig.add_trace(go.Scatter(x=[m.xy(node)[0]], y=[m.xy(node)[1]], mode="markers", showlegend=False,
                                         hoverinfo="skip", marker=dict(size=12, color=colour)), row=i + 1, col=1)
            sub = (f"arrival at S: {T[at]:.2f} s" if k == frames else f"t = {t:.1f} s")
            fig.layout.annotations[i].update(text=f"<b>{name}</b>  ·  {sub}", font=dict(size=20))
        fig.update_xaxes(range=[x0, x1], visible=False, fixedrange=True)
        fig.update_yaxes(range=[y0, y1], visible=False, fixedrange=True)
        fig.update_layout(width=w, height=H, margin=dict(l=0, r=0, t=top, b=0), plot_bgcolor=WALL,
                          paper_bgcolor="white", font=FONT)
        figs.append(fig)
    holds = [fps] + [1] * (len(figs) - 2) + [fps * 4]
    gifkit.make_gif(figs, out, fps=fps, holds=holds, keys=[len(figs) // 3, len(figs) - 1], cols=2, width=w)

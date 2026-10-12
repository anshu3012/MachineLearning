"""Pictures and animations for any world and any planner run (Plotly, saved with Kaleido, joined by gifkit).

Only uses a Space's drawing data (bounds, blocked, start, goal, radius, notes, name) and the planners' event lists,
so a new world needs no change here."""
import math
import warnings

import kaleido
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from gifkit import BLUE, FONT, GREEN, GREY, ORANGE, PURPLE, RED, make_gif

warnings.filterwarnings("ignore", message="The kopts argument")
kaleido.start_sync_server()  # one browser for all frames, instead of one per frame
INK, SHELF, SHELF_EDGE, ROADMAP = "#222222", "#cfcfcf", "#8c8c8c", "#9fb8d6"
W = 900  # figure width, px
RECENT = 20  # blocked steps stay on screen for this many samples


def fmt(x):
    return f"{x:,}"


def grid_step(space):
    """Metres between grid lines: 1, 2 or 5, so a map shows about 10 to 20 of them across."""
    w = space.bounds[2] - space.bounds[0]
    return 1 if w <= 12 else 2 if w <= 25 else 5


def map_height(space, plot_w):
    """Height in px of a map plot_w px wide, so that one metre is as long up as across."""
    x0, y0, x1, y1 = space.bounds
    return round(plot_w * (y1 - y0 + 0.6) / (x1 - x0 + 0.6))


def add_map(fig, space, row=None, col=None, labels=True):
    """Floor, outer walls and blocked areas. Start, goal and notes come last, from marks(), so they stay on top."""
    x0, y0, x1, y1 = space.bounds
    rc = dict(row=row, col=col) if row else {}
    for poly in space.blocked:
        fig.add_trace(go.Scatter(x=list(poly.exterior.xy[0]), y=list(poly.exterior.xy[1]), fill="toself",
                                 fillcolor=SHELF, mode="lines", line=dict(color=SHELF_EDGE, width=1)), **rc)
        for hole in poly.interiors:
            fig.add_trace(go.Scatter(x=list(hole.xy[0]), y=list(hole.xy[1]), fill="toself", fillcolor="white",
                                     mode="lines", line=dict(color=SHELF_EDGE, width=1)), **rc)
    fig.add_trace(go.Scatter(x=[x0, x1, x1, x0, x0], y=[y0, y0, y1, y1, y0], mode="lines",
                             line=dict(color=INK, width=3)), **rc)
    ax = dict(range=[x0 - 0.3, x1 + 0.3], dtick=grid_step(space), showgrid=True, gridcolor="#eeeeee",
              zeroline=False, title="x (m)" if labels else None)
    fig.update_xaxes(**ax, **rc)
    fig.update_yaxes(**dict(ax, range=[y0 - 0.3, y1 + 0.3], title="y (m)" if labels else None), **rc)
    return fig


def marks(fig, space, labels=True, notes=True, **rc):
    """Start (square), goal (star) and the world's notes, drawn over everything else; words on a white patch."""
    mid = (space.bounds[0] + space.bounds[2]) / 2
    for p, name, sym in ((space.start, "start", "square"), (space.goal, "goal", "star")):
        fig.add_trace(go.Scatter(x=[p[0]], y=[p[1]], mode="markers", marker=dict(
            symbol=sym, size=20 if labels else 13, color=INK, line=dict(color="white", width=1.5))), **rc)
        if labels:
            fig.add_annotation(x=p[0], y=p[1], text=name, showarrow=False, font=dict(size=20, color=INK),
                               xanchor="left" if p[0] < mid else "right", xshift=14 if p[0] < mid else -14,
                               bgcolor="rgba(255,255,255,0.6)", **rc)
    for x, y, text in space.notes if labels and notes else []:
        fig.add_annotation(x=x, y=y, text=text, showarrow=False, font=dict(size=18, color="#444444"),
                           bgcolor="rgba(255,255,255,0.7)", **rc)


def figure(space, title, legend, cost_panel=False, bottom=70):
    """A map with a two-line title (what happens, then a key). cost_panel: add a plot of path cost below the map."""
    top, plot_w = 110, W - 110
    h = map_height(space, plot_w)
    if cost_panel:
        fig = make_subplots(rows=2, cols=1, row_heights=[0.75, 0.25], vertical_spacing=0.07)
        h = round(h / (0.75 * 0.93))
        add_map(fig, space, row=1, col=1)
        fig.update_xaxes(title=None, row=1, col=1)
    else:
        fig = add_map(go.Figure(), space)
    fig.update_yaxes(scaleanchor="x", constrain="domain", row=1 if cost_panel else None, col=1 if cost_panel else None)
    fig.update_layout(template="simple_white", width=W, height=h + top + bottom, font=FONT, showlegend=False,
                      margin=dict(l=80, r=30, t=top, b=bottom),
                      title=dict(x=0.5, y=1 - 34 / (h + top + bottom), yanchor="top", font=dict(size=22),
                                 text=f"{title}<br><span style='font-size:18px;color:{GREY}'>{legend}</span>"))
    return fig


def lines(fig, pairs, color, width, dash=None, **rc):
    xs, ys = [], []
    for a, b in pairs:
        xs += [a[0], b[0], None]
        ys += [a[1], b[1], None]
    fig.add_trace(go.Scatter(x=xs, y=ys, mode="lines", line=dict(color=color, width=width, dash=dash)), **rc)


def dots(fig, pts, color, size_, symbol="circle", ring=None, **rc):
    pts = list(pts)
    fig.add_trace(go.Scatter(x=[p[0] for p in pts], y=[p[1] for p in pts], mode="markers", marker=dict(
        color=color, size=size_, symbol=symbol, line=dict(color=ring or color, width=3 if ring else 0))), **rc)


def path_pairs(path):
    return list(zip(path, path[1:])) if path else []


def replay(events):
    """What the planner has built after these events: trees (child -> parent, one dict per tree), roadmap nodes,
    roadmap edges, and how many tree edges were rewired."""
    trees, nodes, edges, rewires = [{}, {}], [], [], 0
    for e in events:
        tree = trees[e.get("tree", 0)]
        for child, parent in e.get("set", []):
            rewires += child in tree
            tree[child] = parent
        if e.get("phase") == "sample" and e["ok"]:
            nodes.append(e["sample"])
        edges += e.get("edges", [])
    return trees, nodes, edges, rewires


def tree_path(tree, root, p):
    if p not in tree:
        return None
    out = [p]
    while out[-1] != root:
        out.append(tree[out[-1]])
    return out[::-1]


def schedule(n, single=6, total=22):
    """Event counts to show: 1..single one at a time, then spaced evenly on a log scale up to n."""
    ks = list(range(1, min(single, n) + 1))
    for i in range(1, total - single + 1):
        ks.append(round(single * (n / single) ** (i / (total - single))))
    return sorted(set(k for k in ks if k <= n) | {n})


def sample_marks(fig, e, **rc):
    """One step up close: the random sample (black ×), the nearest node (orange ring), the new step (orange) or the
    blocked step (red)."""
    dots(fig, [e["sample"]], INK, 18, "x-thin-open", ring=INK, **rc)
    dots(fig, [e["near"]], "rgba(0,0,0,0)", 22, ring=ORANGE, **rc)
    if e["ok"]:
        lines(fig, [(e["near"], e["new"])], ORANGE, 5, **rc)
    else:
        lines(fig, [(e["near"], e["new"])], RED, 3, "dot", **rc)
        dots(fig, [e["new"]], RED, 14, "x", **rc)


def blocked_marks(fig, events, **rc):
    blocked = [e for e in events if e.get("sample") is not None and not e["ok"]]
    lines(fig, [(e["near"], e["new"]) for e in blocked], RED, 2.5, "dot", **rc)
    dots(fig, [e["new"] for e in blocked], RED, 13, "x", **rc)


def world_picture(space, out):
    """worlds/<name>.png: the floor, what blocks it, start and goal, a metre scale."""
    x0, y0, x1, y1 = space.bounds
    fig = figure(space, f"{space.name}: {x1 - x0:g} m × {y1 - y0:g} m",
                 f"grey: blocked · robot: a disk of radius {space.radius:g} m · grid lines every "
                 f"{grid_step(space)} m", bottom=120)
    marks(fig, space)
    bar = 2 * grid_step(space)
    fig.add_shape(type="line", x0=x1 - bar, x1=x1, y0=-0.2, y1=-0.2, xref="x", yref="paper", opacity=1,
                  line=dict(color="black", width=6))
    fig.add_annotation(x=x1 - bar, y=-0.2, xref="x", yref="paper", xanchor="right", text=f"scale: {bar} m ",
                       showarrow=False, font=dict(size=20))
    fig.write_image(out)


def animate_rrt(space, res, out):
    """RRT: the tree growing sample by sample, blocked steps flashing red, then the path."""
    ev = res["events"]
    ks = schedule(len(ev))
    figs = []
    for k in ks:
        trees, _, _, _ = replay(ev[:k])
        done = k == len(ev)
        title = (f"RRT · reached the goal after {k} samples · path {res['length']:.1f} m" if done else
                 f"RRT · sample {k} · {len(trees[0]) + 1} nodes · {sum(not e['ok'] for e in ev[:k])} steps blocked")
        legend = ("× sample · ○ nearest node · orange: new step · red: blocked step" if k <= 6 else
                  "blue: the tree · green: the path, start to goal" if done else
                  f"blue: the tree · red ×: steps blocked in the last {RECENT} samples")
        fig = figure(space, title, legend)
        lines(fig, list(trees[0].items()), BLUE, 1.5)
        dots(fig, trees[0], BLUE, 4)
        if k <= 6:
            sample_marks(fig, ev[k - 1])
        elif not done:
            blocked_marks(fig, ev[max(0, k - RECENT):k])
        if done:
            lines(fig, path_pairs(res["path"]), GREEN, 6)
        marks(fig, space)
        figs.append(fig)
    holds = [5] * 6 + [2] * (len(figs) - 7) + [20]
    make_gif(figs, out, fps=6, holds=holds, keys=key_frames(figs), cols=2, width=W)


def best_rewire(ev):
    """The sample whose rewiring cut the path the most (or, failing that, the first one that rewired 3 nodes)."""
    best, drop, prev = None, 0, None
    for k, e in enumerate(ev, 1):
        if e["cost"] and prev and prev - e["cost"] > drop:  # only a rewire can shorten a path that exists
            best, drop = k, prev - e["cost"]
        prev = e["cost"] or prev
    return best or next(k for k, e in enumerate(ev, 1) if len(e["set"]) >= 4)


def animate_rrt_star(space, res, out):
    """RRT*: the tree growing, one rewire up close, and the path cost falling as samples grow."""
    ev = res["events"]
    costs = [(i + 1, e["cost"]) for i, e in enumerate(ev) if e["cost"]]
    show = best_rewire(ev)
    ks = sorted(set(schedule(len(ev), single=3, total=18)) | {costs[0][0], show - 1})
    frames = [(k, "grow") for k in ks if k < show] + [(show, "join"), (show, "rewire")] + \
             [(k, "grow") for k in ks if k > show]
    rc = dict(row=1, col=1)
    figs, holds = [], []
    for k, mode in frames:
        e, done = ev[k - 1], k == len(ev)
        trees, _, _, rewires = replay(ev[:k] if mode != "join" else ev[:k - 1])
        tree = trees[0]
        if mode == "join":
            tree[e["set"][0][0]] = e["set"][0][1]
        path = tree_path(tree, space.start, space.goal)
        now = sum(math.dist(a, b) for a, b in path_pairs(path)) if path else None
        if mode == "grow":
            title = f"RRT* · sample {k} · {len(tree) + 1} nodes · {rewires} rewires · " + \
                    (f"path {now:.1f} m" if path else "no path yet")
            legend = ("× sample · ○ nearest node · orange: new step · red: blocked step" if k <= 3 else
                      f"blue: the tree · orange: edges rewired in the last {RECENT} samples · green: best path so far")
        elif mode == "join":
            title = f"RRT* · sample {k}, close up · 1. join the new node through its cheapest neighbour"
            legend = (f"dashed circle: neighbours within {e['radius']:.2f} m · orange: the edge it joins by · "
                      "green: path so far")
        else:
            before = next(c for i, c in reversed(costs) if i < k)
            title = f"RRT* · sample {k}, close up · 2. rewire: path {before:.1f} m → {now:.1f} m"
            legend = "orange: neighbours now reached through the new node · grey dashed: the edges they drop"
        fig = figure(space, title, legend, cost_panel=True)
        cost_plot(fig, costs, k if mode != "join" else k - 1, len(ev), res.get("shortest"))
        lines(fig, list(tree.items()), BLUE, 1.5, **rc)
        dots(fig, tree, BLUE, 4, **rc)
        if mode == "grow" and k <= 3:
            sample_marks(fig, e, **rc)
        elif mode == "grow" and not done:
            fresh = {c for x in ev[max(0, k - RECENT):k] for c, _ in x["set"][1:]}
            lines(fig, [(c, tree[c]) for c in fresh], ORANGE, 4, **rc)
        if path:
            lines(fig, path_pairs(path), GREEN, 6, **rc)
        if mode != "grow":
            close_up(fig, space, ev, k, e, mode, rc)
        marks(fig, space, notes=mode == "grow", **rc)  # notes would be cut off at the edges of a close-up
        figs.append(fig)
        holds.append(20 if done else 14 if mode != "grow" else 5 if k <= 3 else 2)
    make_gif(figs, out, fps=6, holds=holds, keys=[0, frames.index((show, "join")), frames.index((show, "rewire")),
                                                     len(figs) - 1], cols=2, width=W)


def close_up(fig, space, ev, k, e, mode, rc):
    """Zoom the map on the new node of event k and draw its neighbourhood and the edges that change."""
    new, (child, parent) = e["new"], e["set"][0]
    t = [x * 2 * math.pi / 60 for x in range(61)]
    fig.add_trace(go.Scatter(x=[new[0] + e["radius"] * math.cos(a) for a in t],
                             y=[new[1] + e["radius"] * math.sin(a) for a in t], mode="lines",
                             line=dict(color=INK, width=2, dash="dash")), **rc)
    if mode == "join":
        lines(fig, [(child, parent)], ORANGE, 6, **rc)
    else:
        old, _, _, _ = replay(ev[:k - 1])
        lines(fig, [(c, old[0][c]) for c, _ in e["set"][1:] if c in old[0]], GREY, 3, "dash", **rc)
        lines(fig, e["set"][1:], ORANGE, 6, **rc)
    dots(fig, [new], ORANGE, 14, **rc)
    x0, y0, x1, y1 = space.bounds
    half = 3.0 * min(x1 - x0, 20) / 20  # 6 m across, less on a map under 20 m wide
    ratio = (y1 - y0 + 0.6) / (x1 - x0 + 0.6)
    cx = min(max(new[0], x0 + half), x1 - half)  # keep the window on the map
    cy = min(max(new[1], y0 + half * ratio), y1 - half * ratio)
    fig.update_xaxes(range=[cx - half, cx + half], dtick=1, row=1, col=1)
    fig.update_yaxes(range=[cy - half * ratio, cy + half * ratio], dtick=1, row=1, col=1)


def cost_plot(fig, costs, k, n, shortest):
    """Lower panel: the best path's length after each sample, so far."""
    shown = [(i, c) for i, c in costs if i <= k]
    if shown:
        fig.add_trace(go.Scatter(x=[i for i, _ in shown] + [k], y=[c for _, c in shown] + [shown[-1][1]],
                                 mode="lines", line=dict(color=GREEN, width=4, shape="hv")), row=2, col=1)
        fig.add_trace(go.Scatter(x=[k], y=[shown[-1][1]], mode="markers", marker=dict(color=GREEN, size=12)),
                      row=2, col=1)
    if shortest:
        fig.add_trace(go.Scatter(x=[0, n], y=[shortest, shortest], mode="lines+text",
                                 text=[f" shortest possible, {shortest:.1f} m", ""], textposition="bottom right",
                                 line=dict(color=GREY, width=2, dash="dash"), textfont=dict(size=17, color=GREY)),
                      row=2, col=1)
    top = max((c for _, c in costs), default=1)
    fig.update_xaxes(range=[0, n], title="samples", showgrid=True, gridcolor="#eeeeee", row=2, col=1)
    fig.update_yaxes(range=[0, top * 1.15], title="path (m)", showgrid=True, gridcolor="#eeeeee", row=2, col=1)


def animate_connect(space, res, out):
    """RRT-Connect: the start tree (blue) and the goal tree (purple) reaching for each other."""
    ev = res["events"]
    ends = [i + 1 for i, e in enumerate(ev) if i + 1 == len(ev) or ev[i + 1]["sample"] is not None]  # round ends
    figs = []
    for j in schedule(len(ends)):
        k = ends[j - 1]
        trees, _, _, _ = replay(ev[:k])
        done = k == len(ev)
        title = (f"RRT-Connect · the trees met after {res['samples']} samples · path {res['length']:.1f} m" if done
                 else f"RRT-Connect · sample {j} · start tree {len(trees[0]) + 1} nodes · "
                      f"goal tree {len(trees[1]) + 1} nodes")
        legend = ("blue: tree from the start · purple: tree from the goal · orange: this sample's steps" if j <= 6
                  else "blue: tree from the start · purple: tree from the goal · green: the path" if done
                  else f"blue: from the start · purple: from the goal · orange: last steps · red ×: blocked, last "
                       f"{RECENT} samples")
        fig = figure(space, title, legend)
        for t, color in ((0, BLUE), (1, PURPLE)):
            lines(fig, list(trees[t].items()), color, 1.5)
            dots(fig, trees[t], color, 4)
        start = ends[j - 2] if j > 1 else 0  # this round's events: the extend step, then the connect steps
        if done:
            lines(fig, path_pairs(res["path"]), GREEN, 6)
        else:
            lines(fig, [s for e in ev[start:k] for s in e["set"]], ORANGE, 5)
            if j <= 6:
                sample_marks(fig, ev[start])
            else:
                blocked_marks(fig, ev[ends[max(0, j - RECENT - 1)]:k])
        marks(fig, space)
        figs.append(fig)
    holds = [5] * 6 + [2] * (len(figs) - 7) + [20]
    make_gif(figs, out, fps=6, holds=holds, keys=key_frames(figs), cols=2, width=W)


def animate_prm(space, res, out):
    """PRM: 1. samples placed, 2. neighbours joined into a roadmap, 3. the query route found by A*."""
    ev = res["events"]
    placed = [i + 1 for i, e in enumerate(ev) if e["phase"] == "sample" and e["ok"]]
    joined = [i + 1 for i, e in enumerate(ev) if e["phase"] == "connect"]
    n = len(placed)
    stops = ([placed[m - 1] for m in sorted({10, 25, 50, 100, 200, n // 2, n}) if m <= n] +
             [joined[m - 1] for m in sorted({10, 50, n // 4, n // 2, n}) if m <= n] + [len(ev), len(ev)])
    figs, prev = [], 0
    for idx, k in enumerate(stops):
        _, nodes, edges, _ = replay(ev[:k])
        window, phase, route = ev[prev:k], ev[k - 1]["phase"], idx == len(stops) - 1
        if phase == "sample":
            rejected = sum(not e["ok"] for e in ev[:k])
            title = f"PRM step 1 of 3 · place samples: {len(nodes)} placed, {rejected} thrown away"
            legend = "blue: samples in free space · red ×: samples that landed on an obstacle"
        elif phase == "connect":
            done = sum(e["phase"] == "connect" for e in ev[:k])
            title = f"PRM step 2 of 3 · join neighbours: {done} of {n} samples, {fmt(len(edges))} edges"
            legend = f"each sample tries its {res['k']} nearest samples · orange: edges added since the last frame"
        else:
            title = (f"PRM step 3 of 3 · query: A* finds the route, {res['length']:.1f} m" if route else
                     "PRM step 3 of 3 · query: join the start and the goal to the roadmap")
            legend = "orange: start and goal joined to their nearest samples · green: the shortest route in the roadmap"
        fig = figure(space, title, legend)
        fresh = [] if route else [s for e in window for s in e.get("edges", [])]
        seen = set(fresh)
        lines(fig, [e for e in edges if e not in seen], ROADMAP, 1.2)
        lines(fig, fresh, ORANGE, 2.5 if phase == "connect" else 4)
        dots(fig, nodes, BLUE, 6)
        if phase == "sample":
            dots(fig, [e["sample"] for e in window if not e["ok"]], RED, 11, "x")
        if route:
            lines(fig, path_pairs(res["path"]), GREEN, 6)
        marks(fig, space)
        figs.append(fig)
        prev = k
    make_gif(figs, out, fps=4, holds=[4] * (len(figs) - 1) + [20], keys=key_frames(figs), cols=2, width=W)


def animate_race(space, results, out):
    """All four planners side by side, on a shared clock: the number of collision checks."""
    names = list(results)
    top = max(r["checks"] for r in results.values())
    clocks = sorted({round(300 * (top / 300) ** (i / 17)) for i in range(18)} | {r["checks"] for r in results.values()})
    panel_h = map_height(space, 0.48 * 940)
    height = round(panel_h / 0.43) + 150
    figs = []
    for clock in clocks:
        heads, state = [], []
        for name in names:
            r = results[name]
            ev = [e for e in r["events"] if e["checks"] <= clock]
            state.append(ev)
            if clock >= r["checks"]:
                heads.append(f"<b>{name}</b> · path {r['length']:.1f} m<br>{fmt(r['samples'])} samples · "
                             f"{fmt(r['checks'])} checks · {r['time']:.2f} s")
            else:
                samples = sum(e.get("sample") is not None for e in ev)
                heads.append(f"<b>{name}</b> · running<br>{fmt(samples)} samples · "
                             f"{fmt(ev[-1]['checks'] if ev else 0)} checks")
        fig = make_subplots(rows=2, cols=2, subplot_titles=heads, vertical_spacing=0.14, horizontal_spacing=0.04)
        for i, (name, ev) in enumerate(zip(names, state)):
            rc = dict(row=i // 2 + 1, col=i % 2 + 1)
            r = results[name]
            add_map(fig, space, labels=False, **rc)
            trees, nodes, edges, _ = replay(ev)
            lines(fig, list(trees[0].items()), BLUE, 1, **rc)
            lines(fig, list(trees[1].items()), PURPLE, 1, **rc)
            lines(fig, edges, ROADMAP, 0.8, **rc)
            dots(fig, nodes, BLUE, 3, **rc)
            path = r["path"] if clock >= r["checks"] else tree_path(trees[0], space.start, space.goal)
            if path and (clock >= r["checks"] or name == "RRT*"):
                lines(fig, path_pairs(path), GREEN, 4, **rc)
            marks(fig, space, labels=False, **rc)
            fig.update_yaxes(scaleanchor=f"x{i + 1 if i else ''}", constrain="domain", **rc)
        fig.update_xaxes(showticklabels=False)
        fig.update_yaxes(showticklabels=False)
        fig.update_annotations(font=dict(size=17))
        fig.update_layout(template="simple_white", width=1000, height=height, font=FONT, showlegend=False,
                          margin=dict(l=30, r=30, t=130, b=20),
                          title=dict(x=0.5, y=1 - 30 / height, yanchor="top", font=dict(size=22),
                                     text=f"The race, timed in collision checks: {fmt(min(clock, top))}<br><span "
                                          f"style='font-size:17px;color:{GREY}'>blue and purple: trees · "
                                          "light blue: roadmap · green: path</span>"))
        figs.append(fig)
    make_gif(figs, out, fps=4, holds=[2] * (len(figs) - 1) + [20], keys=key_frames(figs, 2), cols=2, width=W)


def key_frames(figs, n=4):
    """Indexes for the frames grid: spread over the run, always the last."""
    m = len(figs) - 1
    return sorted({round(m * i / (n - 1)) for i in range(n)})


def animate_all(space, results, folder):
    folder.mkdir(parents=True, exist_ok=True)
    animate_rrt(space, results["RRT"], folder / "rrt")
    animate_rrt_star(space, results["RRT*"], folder / "rrt_star")
    animate_connect(space, results["RRT-Connect"], folder / "rrt_connect")
    animate_prm(space, results["PRM"], folder / "prm")
    animate_race(space, results, folder / "race")

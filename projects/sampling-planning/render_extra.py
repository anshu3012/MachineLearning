"""Animations for the planners after the first four: the potential field (3-D surface, then its contour map), the
randomized potential field, Bug 1 and Bug 2, lazy PRM and the kinodynamic RRT. Same look as render.py, whose map
drawing it reuses; like render.py it needs nothing from a world but its Space."""
import math

import numpy as np
import plotly.graph_objects as go

import render
from gifkit import BLUE, FONT, GREEN, GREY, ORANGE, PURPLE, RED, make_gif
from render import INK, ROADMAP, dots, figure, fmt, lines, marks, path_pairs

UP = 1.0  # m^2 the robot balls and paths float above the surface, so the surface does not hide them


# ------------------------------------------------------------------------------------------------ potential field

def u_grid(space, field, h=0.1):
    x0, y0, x1, y1 = space.bounds
    xs, ys = np.arange(x0, x1 + 1e-9, h), np.arange(y0, y1 + 1e-9, h)
    X, Y = np.meshgrid(xs, ys)
    return xs, ys, field.U(X, Y)


def eye_at(s, r=2.1, elev=30, turn=-25):
    """Camera for tilt fraction s: 0 = side view from the front (low y), 1 = straight above with x to the right."""
    phi, alpha = math.radians(elev + (89.9 - elev) * s), math.radians(turn * (1 - s))
    return dict(x=r * math.sin(alpha) * math.cos(phi), y=-r * math.cos(alpha) * math.cos(phi), z=r * math.sin(phi))


def surface_frame(space, field, grid, robots, s, title, legend, cmax, step=10):
    """The height U as a surface over the floor, contour lines every `step` m^2; shelves and walls with the robot's
    band are holes. robots: (path so far (n x 2), colour). s: camera tilt, 0 side view, 1 straight above."""
    xs, ys, Z = grid
    Zs = np.where(np.isfinite(Z) & (Z <= cmax), Z, np.nan)
    fig = go.Figure(go.Surface(
        x=xs, y=ys, z=Zs, colorscale=[[0, "#eef4fb"], [1, "#3f75b0"]], cmin=0, cmax=cmax, showscale=False,
        contours=dict(z=dict(show=True, start=0, end=cmax, size=step, color="rgba(30,30,30,0.5)", width=2)),
        lighting=dict(ambient=0.75, diffuse=0.5, specular=0.05), hoverinfo="skip"))
    for P, col in robots:
        z = field.U(P[:, 0], P[:, 1]) + UP
        if len(P) > 1:
            fig.add_trace(go.Scatter3d(x=P[:, 0], y=P[:, 1], z=z, mode="lines", line=dict(color=col, width=8)))
        fig.add_trace(go.Scatter3d(x=P[-1:, 0], y=P[-1:, 1], z=z[-1:] + UP, mode="markers",
                                   marker=dict(size=9, color=col, line=dict(color="white", width=2))))
    g = field.goal
    fig.add_trace(go.Scatter3d(x=[g[0]], y=[g[1]], z=[4 * UP], mode="markers+text", text=["goal "],
                               textposition="middle left", textfont=dict(size=18, color=INK),
                               marker=dict(size=8, color=INK, symbol="diamond")))
    x0, y0, x1, y1 = space.bounds
    top = s > 0.97
    fig.update_scenes(
        xaxis=dict(title="x (m)", range=[x0, x1], tickfont=dict(size=14)),
        yaxis=dict(title="y (m)", range=[y0, y1], tickfont=dict(size=14)),
        zaxis=dict(title="" if top else "U (m²)", range=[0, cmax * 1.03], showticklabels=not top,
                   tickfont=dict(size=14), showbackground=not top),
        aspectmode="manual", aspectratio=dict(x=2, y=2 * (y1 - y0) / (x1 - x0), z=0.8),
        camera=dict(eye=eye_at(s), center=dict(x=0, y=0, z=-0.1), up=dict(x=0, y=0, z=1),
                    projection=dict(type="orthographic")))
    fig.update_layout(template="simple_white", width=1000, height=720, font=FONT, showlegend=False,
                      margin=dict(l=0, r=0, t=95, b=0),
                      title=dict(x=0.5, y=0.97, yanchor="top", font=dict(size=22),
                                 text=f"{title}<br><span style='font-size:18px;color:{GREY}'>{legend}</span>"))
    return fig


def animate_field(space, field, runs, out, tilt=10, roll=28):
    """runs: [(path from field.descend, colour, words for the end)]. The surface from the side with the robots at
    their starts; the camera tilts up until the surface is its contour map; then the robots roll downhill."""
    grid = u_grid(space, field)
    cmax = 10 * math.ceil(np.nanmax(np.where(np.isfinite(grid[2]), grid[2], np.nan)) / 10)
    legend = "holes: shelves and walls, with the robot's 0.25 m band · lines: every 10 m² of height"
    starts = [(P[:1], col) for P, col, _ in runs]
    figs = [surface_frame(space, field, grid, starts, 0, "U: a bowl at the goal plus a hill round every obstacle",
                          legend, cmax)]
    holds = [16]
    for i, s in enumerate(np.linspace(0, 1, tilt + 1)[1:]):
        last = i == tilt - 1
        figs.append(surface_frame(space, field, grid, starts, s, "seen from straight above: the contour map" if last
                                  else "tilt the camera up", legend, cmax))
        holds.append(10 if last else 1)
    for k in range(1, roll + 1):
        robots = [(P[:max(1, round(k / roll * (len(P) - 1))) + 1], col) for P, col, _ in runs]
        words = " · ".join(w for _, _, w in runs) if k == roll else "each robot steps down the slope"
        figs.append(surface_frame(space, field, grid, robots, 1, "both robots roll downhill", words, cmax))
        holds.append(1)
    holds[-1] = 24
    make_gif(figs, out, fps=8, holds=holds, keys=[0, tilt, tilt + roll // 2, len(figs) - 1], cols=2, width=900)


def contour_map(fig, space, field, grid=None, step=10, cmax=230):
    """The contour lines of U, every step m^2 up to cmax, under the map drawn by render.figure. Heights above cmax
    (next to an obstacle U grows without bound) are drawn as cmax, so the lines there run under the shelves."""
    xs, ys, Z = grid or u_grid(space, field)
    fig.add_trace(go.Contour(x=xs, y=ys, z=np.minimum(Z, cmax), showscale=False, hoverinfo="skip",
                             contours=dict(start=0, end=cmax - step / 2, size=step, coloring="lines"),
                             line=dict(width=1), colorscale=[[0, "#b9c9de"], [1, "#b9c9de"]]))
    fig.data = (fig.data[-1],) + fig.data[:-1]  # first, so the shelves and the planner's marks cover it


def animate_random_walks(space, field, parts, out, shortest):
    """The randomized potential field's run: walks (black, then grey), descents back into the local minimum
    (orange), the descent that reaches the goal (green), restarts from an earlier walk point (purple, dashed)."""
    grid = u_grid(space, field)
    stuck = parts[0][1][-1]
    u0 = field.u(stuck)
    walks = sum(m == "walk" for m, _ in parts)
    figs, holds, done, driven, w = [], [], [], 0.0, 0
    from potential import path_length
    for i, (mode, P) in enumerate(parts):
        if i == 0:
            done.append((mode, P))
            continue
        w += mode == "walk"
        n = {"walk": 4, "descend": 2, "backtrack": 1}[mode]
        for j in range(1, n + 1):
            part = P[:max(2, round(j / n * len(P)))]
            now = driven + path_length(part)
            final = i == len(parts) - 1 and j == n
            title = (f"reached the goal after {walks} random walks · {now:,.0f} m driven (shortest {shortest:.1f} m)"
                     if final else f"walk {w} of {walks} · {now:,.0f} m driven")
            legend = ("grey: random walks · orange: rolled back into the dip · green: rolled to the goal"
                      if final else f"black: this walk (steps of {field_step(parts):g} m in x and in y) · "
                                    f"red star: the local minimum, U = {u0:.1f} m²")
            fig = figure(space, title, legend)
            contour_map(fig, space, field, grid)
            for m, Q in done + ([(mode, part)] if not final else [(mode, P)]):
                current = Q is part and not final
                colour = {"walk": INK if current else "#a8a8a8", "descend": ORANGE, "backtrack": PURPLE}[m]
                if m == "descend" and field.at_goal(Q[-1]):
                    colour = GREEN
                lines(fig, list(zip(map(tuple, Q[:-1]), map(tuple, Q[1:]))), colour,
                      2.5 if current or m != "walk" else 1, "dash" if m == "backtrack" else None)
            dots(fig, [tuple(stuck)], RED, 22, "star", ring="white")
            dots(fig, [tuple(part[-1])], INK, 12, ring="white")
            marks(fig, space)
            figs.append(fig)
            holds.append(20 if final else 6 if j == n and mode == "walk" else 1)
        done.append((mode, P))
        driven += path_length(P)
    make_gif(figs, out, fps=6, holds=holds, keys=render.key_frames(figs), cols=2, width=900)


def field_step(parts):
    walk = next(P for m, P in parts if m == "walk")
    return round(abs(walk[1][0] - walk[0][0]), 3)


# ------------------------------------------------------------------------------------------------ Bug 1 and Bug 2

def along_path(path, d):
    """The path's points up to distance d along it (the last point interpolated)."""
    out, total = [path[0]], 0.0
    for a, b in zip(path, path[1:]):
        step = math.dist(a, b)
        if total + step >= d:
            t = (d - total) / step if step else 0
            out.append((a[0] + t * (b[0] - a[0]), a[1] + t * (b[1] - a[1])))
            return out
        out.append(b)
        total += step
    return out


def animate_bug(space, res, out, name, shortest, frames=60):
    """The robot's centre driving: straight at the goal (blue), along the edge (purple), back to the nearest point
    (green); H: hit points, C: the edge point nearest the goal, L: where Bug 2 leaves the edge."""
    from bugs import free_piece
    poly = free_piece(space)
    rings = [poly.exterior, *poly.interiors]
    colour = {"to goal": BLUE, "round the edge": PURPLE, "follow the edge": PURPLE, "back to the nearest point": GREEN}
    starts, d = [], 0.0  # where each leg starts, in metres driven
    for kind, pts in res["legs"]:
        starts.append(d)
        d += sum(math.dist(a, b) for a, b in zip(pts, pts[1:]))
    mark_at = {}
    for lab, q in res["marks"]:  # a mark is reached at the end of the leg that ends on it
        mark_at[lab] = next(s + sum(math.dist(a, b) for a, b in zip(pts, pts[1:]))
                            for s, (_, pts) in zip(starts, res["legs"]) if math.dist(pts[-1], q) < 1e-6)
    stops = sorted(set(np.linspace(0, res["length"], frames)) | set(mark_at.values()))
    figs, holds = [], []
    for D in stops:
        final = D >= res["length"] - 1e-9
        kind = next(k for s, (k, _) in reversed(list(zip(starts, res["legs"]))) if s <= D + 1e-9)
        title = (f"{name} · reached the goal: {res['length']:.1f} m driven (shortest path {shortest:.1f} m)" if final
                 else f"{name} · {D:.1f} m driven · {kind}")
        legend = ("orange: grown obstacles' edge · dashed: start–goal line · blue: to the goal · purple: along "
                  "the edge" + (" · green: back to C" if res["bug1"] else ""))
        fig = figure(space, title, legend)
        for r in rings:
            fig.add_trace(go.Scatter(x=list(r.xy[0]), y=list(r.xy[1]), mode="lines", line=dict(color=ORANGE, width=2)))
        lines(fig, [(space.start, space.goal)], GREY, 2, "dash")
        for s, (k, pts) in zip(starts, res["legs"]):
            if s > D:
                break
            seg = along_path(pts, D - s)
            lines(fig, list(zip(seg, seg[1:])), colour[k], 5)
        for lab, q in res["marks"]:
            if mark_at[lab] <= D + 1e-9:
                dots(fig, [q], INK, 12, "diamond", ring="white")
                fig.add_annotation(x=q[0], y=q[1], text=f"<b>{lab}</b>", showarrow=False,
                                   yshift=20 if lab[0] == "H" else -22,
                                   font=dict(size=20, color=INK), bgcolor="rgba(255,255,255,0.75)")
        here = along_path(res["path"], D)[-1]
        dots(fig, [here], INK, 14, ring="white")
        marks(fig, space)
        figs.append(fig)
        holds.append(20 if final else 8 if D in mark_at.values() else 1)
    make_gif(figs, out, fps=8, holds=holds, keys=render.key_frames(figs), cols=2, width=900)


# ------------------------------------------------------------------------------------------------ lazy PRM

def animate_lazy(space, res, out, full_checks):
    """Lazy PRM: every edge to the 10 nearest, unchecked (grey); each search's route (orange); edges checked free
    (green) or colliding and deleted (red); then the route."""
    ev = res["events"]
    nodes = [e["sample"] for e in ev if e["phase"] == "sample" and e["ok"]]
    candidate = next(e["edges"] for e in ev if e["phase"] == "connect")
    searches = [e for e in ev if e["phase"] == "search"]
    figs, holds, safe, cut = [], [], [], []

    def draw(title, legend, route=None, checked=()):
        fig = figure(space, title, legend)
        gone = {frozenset(c) for c in cut}
        lines(fig, [c for c in candidate if frozenset(c) not in gone], ROADMAP, 0.8)
        dots(fig, nodes, BLUE, 4)
        if route:
            lines(fig, path_pairs(route), ORANGE, 6)
        lines(fig, safe, GREEN, 3)
        lines(fig, cut, RED, 4, "dot")
        for (a, b), ok in checked:
            lines(fig, [(a, b)], GREEN if ok else RED, 7)
        marks(fig, space)
        figs.append(fig)

    draw(f"Lazy PRM · {len(nodes)} points, each joined to its {res['k']} nearest: {fmt(len(candidate))} edges",
         "light blue: edges assumed free, none checked yet")
    holds.append(12)
    for i, e in enumerate(searches, 1):
        last = i == len(searches)
        draw(f"Lazy PRM · search {i}: A* finds the shortest route over the edges left",
             "orange: the route · thin green: edges already checked free · red: edges deleted", e["route"])
        holds.append(6)
        bad = [c for c, ok in e["checked"] if not ok]
        draw(f"Lazy PRM · search {i}: check its edges from the start: {len(e['checked'])} checked, "
             + (f"edge {len(e['checked'])} collides" if bad else "all free"),
             "green: free · red: collides, so it is deleted and A* searches again" if bad else
             "green: every edge of the route is free", e["route"], e["checked"])
        holds.append(8)
        safe += [c for c, ok in e["checked"] if ok]
        cut += bad
    route = searches[-1]["route"]
    fig_title = (f"Lazy PRM · route {res['length']:.1f} m · {res['searches']} searches, {res['edge_checks']} edges "
                 f"checked · {fmt(res['checks'])} checks against {fmt(full_checks)}")
    draw(fig_title, "thick green: the route · thin green: other edges checked free · red: edges that collided")
    lines(figs[-1], path_pairs(route), GREEN, 7)
    marks(figs[-1], space)
    holds.append(24)
    make_gif(figs, out, fps=4, holds=holds, keys=render.key_frames(figs), cols=2, width=900)


# ------------------------------------------------------------------------------------------------ kinodynamic RRT

def pose_arrow(fig, p, length, colour, width=3):
    lines(fig, [(p[:2], (p[0] + length * math.cos(p[2]), p[1] + length * math.sin(p[2])))], colour, width)


def animate_kinodynamic(space, res, out, single=10, goal_radius=0.5):
    """The kinodynamic RRT: in the first frames one round each (the sample and its heading, the nearest node, the
    three primitives tried, the closest one green if free and kept, red if it hits); then the tree of arcs grows."""
    ev = res["events"]
    ks = list(range(1, single + 1)) + [k for k in render.schedule(len(ev), single, 30) if k > single]
    figs, holds = [], []
    for k in ks:
        tree = [e["best"] for e in ev[:k] if e["ok"]]
        thrown = sum(not e["ok"] for e in ev[:k])
        done = k == len(ev)
        title = (f"Kinodynamic RRT · reached the goal after {k:,} rounds · path {res['length']:.1f} m, "
                 f"{len(res['motions'])} arcs" if done else
                 f"Kinodynamic RRT · round {k:,} · {len(tree) + 1:,} nodes · {thrown:,} motions thrown away")
        legend = ("× sample and its heading · ○ nearest node · grey: the 3 motions tried · green: the closest, kept · "
                  "red: it hits" if k <= single else f"blue: the tree, every edge a drivable arc · purple: within "
                  f"{goal_radius:g} m of the goal · green: the path" if done else
                  f"blue: the tree, every edge a drivable arc · purple: within {goal_radius:g} m of the goal")
        fig = figure(space, title, legend)
        xs, ys = [], []
        for m in tree:
            for p in m[::10]:
                xs.append(p[0])
                ys.append(p[1])
            xs.append(None)
            ys.append(None)
        fig.add_trace(go.Scatter(x=xs, y=ys, mode="lines", line=dict(color=BLUE, width=1.5)))
        if k <= single:
            e = ev[k - 1]
            for m in e["tries"]:
                lines(fig, list(zip(m[::5], m[5::5])), GREY, 3)
            lines(fig, list(zip(e["best"][::5], e["best"][5::5])), GREEN if e["ok"] else RED, 6)
            dots(fig, [e["sample"][:2]], INK, 18, "x-thin-open", ring=INK)
            pose_arrow(fig, e["sample"], 0.8, INK)
            dots(fig, [e["near"][:2]], "rgba(0,0,0,0)", 22, ring=ORANGE)
        if done:
            p = res["path"]
            fig.add_trace(go.Scatter(x=[q[0] for q in p], y=[q[1] for q in p], mode="lines",
                                     line=dict(color=GREEN, width=6)))
        t = np.linspace(0, 2 * math.pi, 61)
        fig.add_trace(go.Scatter(x=space.goal[0] + goal_radius * np.cos(t), y=space.goal[1] + goal_radius * np.sin(t),
                                 mode="lines", line=dict(color=PURPLE, width=2.5, dash="dash")))
        marks(fig, space)
        figs.append(fig)
        holds.append(20 if done else 6 if k <= single else 2)
    make_gif(figs, out, fps=6, holds=holds, keys=render.key_frames(figs), cols=2, width=900)

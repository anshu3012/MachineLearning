"""Animations for the sections from a path to a drive (local_planner.py): the elastic band relaxing, the local
planner's drive past a person, the two first guesses, and refine once against stop-and-turn. Same look as render.py,
whose map drawing it reuses; it needs nothing from a world but its Space."""
import math

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import render
from gifkit import BLUE, FONT, GREEN, GREY, ORANGE, make_gif
from render import dots, lines, marks

PINK = "#C2185B"  # the person
DISK = np.linspace(0, 2 * np.pi, 41)


def disk(fig, x, y, r, colour, fill, **rc):
    fig.add_trace(go.Scatter(x=x + r * np.cos(DISK), y=y + r * np.sin(DISK), mode="lines", fill="toself",
                             fillcolor=fill, line=dict(color=colour, width=2)), **rc)


def robot(fig, pose, r, colour, fill, **rc):
    """The robot's disk and a line from its centre to its edge along its heading."""
    disk(fig, pose[0], pose[1], r, colour, fill, **rc)
    lines(fig, [(pose[:2], (pose[0] + r * math.cos(pose[2]), pose[1] + r * math.sin(pose[2])))], colour, 3, **rc)


def band(fig, P, colour, size=7, tick=0.12, **rc):
    """A timed elastic band: its poses as dots, each with a short line along its heading."""
    lines(fig, [(p[:2], (p[0] + tick * math.cos(p[2]), p[1] + tick * math.sin(p[2]))) for p in P], colour, 2, **rc)
    dots(fig, [p[:2] for p in P], colour, size, **rc)


def crop_map(fig, space, crop, dtick=1, **rc):
    """The world's map, shown only inside crop (x0, y0, x1, y1), one metre as long up as across."""
    render.add_map(fig, space, labels=True, **rc)
    fig.update_xaxes(range=[crop[0], crop[2]], dtick=dtick, **rc)
    fig.update_yaxes(range=[crop[1], crop[3]], dtick=dtick, scaleanchor="x", constrain="domain", **rc)


def polyline(fig, P, colour, width, dash=None, **rc):
    """One continuous line through the points (a drive sampled every few ms would vanish as separate pieces)."""
    P = np.asarray(P)
    fig.add_trace(go.Scatter(x=P[:, 0], y=P[:, 1], mode="lines", line=dict(color=colour, width=width, dash=dash)),
                  **rc)


def two_line(title, legend, size=18):
    return f"{title}<br><span style='font-size:{size}px;color:{GREY}'>{legend}</span>"


# ------------------------------------------------------------------------------------------------ the elastic band

def animate_band(space, rrt_path, hist, final, out, shortest):
    """The band relaxing, one QP solve per frame: the RRT path (grey dashed), the band (blue), each point's sideways
    bounds (green), and below, the band's length after each pass."""
    lengths = [sum(math.dist(a, b) for a, b in zip(P, P[1:])) for P, *_ in [(rrt_path,)] + hist[1:] + [(final,)]]
    rc = dict(row=1, col=1)
    figs, holds = [], []
    for k in range(len(hist) + 1):
        done = k == len(hist)
        P = final if done else hist[k][0]
        title = (f"Elastic band · {len(hist)} solves · {lengths[0]:.1f} m → {lengths[-1]:.1f} m" if done else
                 "Elastic band · the RRT path, points 0.2 m apart" if k == 0 else
                 f"Elastic band · solve {k} · {lengths[k]:.1f} m")
        legend = ("grey dashed: RRT's path · blue: the band · green: how far each point may move sideways" if not done
                  else f"blue: the band, smooth and {lengths[0] - lengths[-1]:.1f} m shorter · grey dashed: RRT's path")
        fig = render.figure(space, title, legend, cost_panel=True)
        polyline(fig, rrt_path, GREY, 2, "dash", **rc)
        if not done:
            Q, lo, hi, _ = hist[k]
            n = np.vstack([[0, 0], (lambda c: np.stack([-c[:, 1], c[:, 0]], 1) / np.hypot(*c.T)[:, None])(
                Q[2:] - Q[:-2]), [0, 0]])
            lo, hi = np.r_[0, lo, 0], np.r_[0, hi, 0]
            lines(fig, [(q + a * m, q + b * m) for q, a, b, m in zip(Q, lo, hi, n)], GREEN, 1.5, **rc)
        polyline(fig, P, BLUE, 4, **rc)
        marks(fig, space, **rc)
        fig.add_trace(go.Scatter(x=list(range(k + 1)), y=lengths[:k + 1], mode="lines+markers",
                                 line=dict(color=BLUE, width=3), marker=dict(size=8)), row=2, col=1)
        fig.add_trace(go.Scatter(x=[0, len(hist)], y=[shortest, shortest], mode="lines+text",
                                 text=[f" shortest possible, {shortest:.1f} m", ""], textposition="top right",
                                 line=dict(color=GREY, width=2, dash="dash"), textfont=dict(size=17, color=GREY)),
                      row=2, col=1)
        fig.update_xaxes(range=[-0.3, len(hist) + 0.3], title="solves", showgrid=True, gridcolor="#eeeeee", dtick=1,
                         row=2, col=1)
        fig.update_yaxes(range=[0, lengths[0] * 1.15], title="length (m)", showgrid=True, gridcolor="#eeeeee",
                         row=2, col=1)
        figs.append(fig)
        holds.append(20 if done else 8 if k == 0 else 4)
    make_gif(figs, out, fps=4, holds=holds, keys=render.key_frames(figs), cols=2, width=900)


# ------------------------------------------------------------------------------------------------ the local planner

def drive_figure(space, crop, title, legend, t_max, v_title="speed (m/s)"):
    """The map (cropped to the drive) on the left, the speed against time on the right."""
    x0, y0, x1, y1 = crop
    fig = make_subplots(rows=1, cols=2, column_widths=[0.5, 0.5], horizontal_spacing=0.1)
    crop_map(fig, space, crop, row=1, col=1)
    plot_w = 0.5 * 0.9 * (1100 - 150)
    h = round(plot_w * (y1 - y0) / (x1 - x0)) + 170
    fig.update_xaxes(range=[0, t_max], title="time (s)", showgrid=True, gridcolor="#eeeeee", row=1, col=2)
    fig.update_yaxes(range=[0, 0.7], title=v_title, showgrid=True, gridcolor="#eeeeee", row=1, col=2)
    fig.add_trace(go.Scatter(x=[0, t_max], y=[0.6, 0.6], mode="lines", line=dict(color=GREY, width=2, dash="dash")),
                  row=1, col=2)
    fig.add_annotation(x=t_max, y=0.6, text="wheel limit, 0.6 m/s", showarrow=False, xanchor="right",
                       yanchor="bottom", yshift=4, font=dict(size=16, color=GREY), row=1, col=2)
    fig.update_layout(template="simple_white", width=1100, height=h, font=FONT, showlegend=False,
                      margin=dict(l=70, r=30, t=110, b=60),
                      title=dict(x=0.5, y=1 - 30 / h, yanchor="top", font=dict(size=22), text=two_line(title, legend)))
    return fig


def animate_loop(space, route_pts, cycles, drive, person, free_drive, out, crop, every=0.2):
    """The receding-horizon drive: the global plan (grey dashed), the band (orange) re-solved every 0.1 s towards
    the local goal (orange ×), the robot (blue) and the person (pink); right: speed against time, without the
    person in grey. One frame per `every` s; the last holds at the arrival."""
    rc = dict(row=1, col=1)
    t_arr, t_free = drive[-1, 0], free_drive[-1, 0]
    t_max = math.ceil(max(t_arr, t_free) + 1)
    step = round(every / 0.1)
    ks = list(range(0, len(cycles), step)) + [len(cycles)]
    t_seen = person.t0
    figs, holds = [], []
    for k in ks:
        done = k == len(cycles)
        c = cycles[min(k, len(cycles) - 1)]
        t = t_arr if done else c["t"]
        upto = drive[drive[:, 0] <= t + 1e-9]
        pose = upto[-1, 1:4]
        seen = person.at(t)
        title = (f"Arrived at {t_arr:.1f} s · {t_arr - t_free:.1f} s later than with nobody in the way" if done else
                 f"t = {t:.1f} s · speed {c['v']:.2f} m/s · band of {len(c['P'])} poses, solved again every 0.1 s")
        legend = ("grey dashed: global plan, once · orange: local plan, 1.5 m · blue: the robot · pink: the person"
                  if not done else "blue: where the robot drove · pink: the person · right: speed, grey without them")
        fig = drive_figure(space, crop, title, legend, t_max)
        polyline(fig, route_pts, GREY, 2.5, "dash", **rc)
        polyline(fig, upto[:, 1:3], BLUE, 3, **rc)
        if seen:
            disk(fig, seen[0], seen[1], seen[2], PINK, "rgba(194,24,91,0.35)", **rc)
        if not done:
            band(fig, c["P"], ORANGE, **rc)
            dots(fig, [c["goal"][:2]], ORANGE, 16, "x", **rc)
        robot(fig, pose, space.radius, BLUE, "rgba(76,120,168,0.35)", **rc)
        marks(fig, space, notes=False, **rc)
        fig.add_trace(go.Scatter(x=free_drive[:, 0], y=free_drive[:, 4], mode="lines",
                                 line=dict(color="#b5b5b5", width=3)), row=1, col=2)
        fig.add_trace(go.Scatter(x=upto[:, 0], y=upto[:, 4], mode="lines", line=dict(color=BLUE, width=4)),
                      row=1, col=2)
        fig.add_shape(type="line", x0=t_seen, x1=t_seen, y0=0, y1=0.7, line=dict(color=PINK, width=2, dash="dot"),
                      row=1, col=2)
        fig.add_annotation(x=t_seen, y=0.66, text="person steps out ", showarrow=False, xanchor="right",
                           font=dict(size=16, color=PINK), row=1, col=2)
        figs.append(fig)
        holds.append(24 if done else 3 if t_seen - 0.05 <= t <= t_seen + 2.5 else 1)
    near = [i for i, k in enumerate(ks[:-1]) if cycles[k]["t"] >= t_seen][:12:4]
    make_gif(figs, out, fps=6, holds=holds, keys=[0, *near, len(figs) - 1], cols=2, width=1000)


def animate_sides(space, case, out, window):
    """The same cycle solved from two first guesses, one solver step per frame: left, last cycle's band; right, a
    band laid on A*'s route round the person (green dotted)."""
    hw, ha = case["hist_warm"], case["hist_search"]
    n = max(len(hw), len(ha))
    fig0 = make_subplots(rows=1, cols=2, horizontal_spacing=0.06)
    person = case["person"]
    figs = []
    for k in range(n):
        done = k == n - 1
        fig = go.Figure(fig0)
        heads = []
        for col, hist, name in ((1, hw, "from last cycle's band"), (2, ha, "from A*'s route")):
            rc = dict(row=1, col=col)
            P, DT, cost = hist[min(k, len(hist) - 1)]
            render.add_map(fig, space, labels=False, **rc)
            fig.update_xaxes(range=[window[0], window[2]], dtick=0.5, **rc)
            fig.update_yaxes(range=[window[1], window[3]], dtick=0.5, scaleanchor="x" if col == 1 else "x2",
                             constrain="domain", **rc)
            disk(fig, person[0], person[1], person[2], PINK, "rgba(194,24,91,0.35)", **rc)
            if col == 2:
                polyline(fig, case["route"], GREEN, 3, "dot", **rc)
            else:
                band(fig, case["warm"][0], "#f7c99a", size=6, **rc)
            for p in P[1:-1]:
                disk(fig, p[0], p[1], space.radius, "rgba(245,133,24,0.35)", "rgba(0,0,0,0)", **rc)
            band(fig, P, ORANGE, **rc)
            robot(fig, P[0], space.radius, BLUE, "rgba(76,120,168,0.35)", **rc)
            dots(fig, [P[-1][:2]], ORANGE, 16, "x", **rc)
            gap = case["gap"](P)
            heads.append(f"<b>{name}</b><br>cost {cost:.2f} · " + (f"{gap:.3f} m clear" if gap >= 0 else
                                                                  f"overlap {-gap:.3f} m"))
        for i, h in enumerate(heads):
            fig.add_annotation(text=h, x=0.22 + 0.56 * i, y=1.0, xref="paper", yref="paper", xanchor="center",
                               yanchor="bottom", showarrow=False, font=dict(size=18))
        title = ("The same cycle, two first guesses: same solver, two answers" if done else
                 f"Solver step {k} of {n - 1}: 4 passes of up to 5 steps, clearance weight doubled after each")
        legend = "orange: the band (pale rings: the robot's disk at each pose) · pink: the person · green dotted: A*"
        fig.update_xaxes(showticklabels=False)
        fig.update_yaxes(showticklabels=False)
        fig.update_layout(template="simple_white", width=1100, height=680, font=FONT, showlegend=False,
                          margin=dict(l=20, r=20, t=150, b=20),
                          title=dict(x=0.5, y=0.97, yanchor="top", font=dict(size=22), text=two_line(title, legend)))
        figs.append(fig)
    make_gif(figs, out, fps=4, holds=[8] + [2] * (n - 2) + [24], keys=[0, n // 3, 2 * n // 3, n - 1], cols=2,
             width=1000)


# ------------------------------------------------------------------------------------------------ refine once

def animate_refine(space, route_pts, colloc, replay, stop, out, crop, every=0.4):
    """Two drives from the start to the goal on one clock: stop-and-turn along the A* route (grey) and the
    collocation drive (blue, its controls replayed); right: their speeds against time."""
    rc = dict(row=1, col=1)
    t_end = stop[-1, 0]
    t_max = math.ceil(t_end + 1)
    ts = list(np.arange(0, t_end, every)) + [t_end]
    T = colloc["T"]
    figs, holds = [], []
    for t in ts:
        done = t >= t_end
        a = replay[replay[:, 0] <= t + 1e-9]
        b = stop[stop[:, 0] <= t + 1e-9]
        title = (f"Refine once: {T:.1f} s against {t_end:.1f} s for stop-and-turn" if done else
                 f"t = {t:.1f} s" + (f" · collocation arrived at {T:.1f} s" if t >= T else ""))
        legend = ("grey: A*'s route, driven by stopping and turning at each corner · blue: one collocation solve, "
                  "least time")
        fig = drive_figure(space, crop, title, legend, t_max)
        polyline(fig, route_pts, GREY, 2, "dash", **rc)
        polyline(fig, b[:, 1:3], GREY, 4, **rc)
        polyline(fig, a[:, 1:3], BLUE, 4, **rc)
        robot(fig, b[-1, 1:4], space.radius, "#7a7a7a", "rgba(150,150,150,0.35)", **rc)
        robot(fig, a[-1, 1:4], space.radius, BLUE, "rgba(76,120,168,0.35)", **rc)
        marks(fig, space, notes=False, **rc)
        fig.add_trace(go.Scatter(x=b[:, 0], y=b[:, 4], mode="lines", line=dict(color="#8a8a8a", width=3)),
                      row=1, col=2)
        fig.add_trace(go.Scatter(x=a[:, 0], y=a[:, 4], mode="lines", line=dict(color=BLUE, width=4)), row=1, col=2)
        figs.append(fig)
        holds.append(24 if done else 6 if abs(t - T) < every / 2 else 1)
    make_gif(figs, out, fps=6, holds=holds, keys=render.key_frames(figs), cols=2, width=1000)

"""Figure 8 as an animation: feature extraction walks the simulated scan from the robot at (2, 1, 30 deg) beam by
beam (360 beams, 1 degree apart, range noise 1 cm, seeded as in the notebook). A blue cursor marks the beam
being read; an orange line shows the jump at each cut (where the range jumps by more than 0.3 m) while it is tested; when a cut closes
a piece, the piece is tested: narrower than 0.35 m and nearer than the beams on both sides. Only the 3-beam piece
(green pole, 4.004 m, -33.0 deg) and the 5-beam piece (pink pole, 2.232 m, 87.0 deg) pass. The last frame shows the
whole scan. Run: python scan_extract.py -> scan_extract.gif, scan_extract_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from gifkit import BLUE, FONT, GREEN, GREY, ORANGE, RED, make_gif
from roommap import DOOR, H, POLE_R, ROBOT, TABLE, W, extract_poles, scan

here = Path(__file__).parent
PINK = "#E377C2"
b, r = scan(ROBOT, noise=0.01, rng=np.random.default_rng(0))
X, Y, TH = ROBOT
HX, HY = X + r * np.cos(TH + b), Y + r * np.sin(TH + b)
DEG = np.round(np.degrees(b)).astype(int)
N = len(r)
CUTS = [i for i in range(N) if abs(r[i] - r[i - 1]) > 0.3]
found = extract_poles(b, r)
POLES = {149: (found[0], GREEN, range(146, 149)), 270: (found[1], PINK, range(265, 270))}   # closing cut -> pole

assert N == 360 and CUTS == [137, 138, 139, 146, 149, 150, 204, 222, 265, 270]
assert [(round(a, 3), round(float(np.degrees(c)), 1), n) for a, c, n in found] == [(4.004, -33.0, 3), (2.232, 87.0, 5)]


def m(v):
    return f"{v}".replace("-", "−")


def piece(end):
    """The piece closed by the cut at index `end`: (beams, width in m, mean range), as extract_poles computes it."""
    start = CUTS[CUTS.index(end) - 1]
    idx = [(start + j) % N for j in range((end - start) % N)]
    rr = r[idx]
    return len(idx), rr.mean() * np.radians(1) * len(idx), rr.mean()


def frame(k, title, lines, final=False, show=()):
    """Beams 0..k have been read; beam k is under the cursor; `show`: the cuts whose jump is drawn."""
    fig = go.Figure()
    for seg in [[(0, 0), (W, 0), (W, H), (DOOR[1], H)], [(DOOR[0], H), (0, H), (0, 0)]]:
        sx, sy = zip(*seg)
        fig.add_trace(go.Scatter(x=sx, y=sy, mode="lines", line=dict(color="#bbb", width=3)))
    px, py = zip(*(TABLE + [TABLE[0]]))
    fig.add_trace(go.Scatter(x=px, y=py, mode="lines", line=dict(color="#bbb", width=2)))
    fig.add_trace(go.Scatter(x=[5.6, 7, 7, 6.4, 6.4, 5.6, 5.6], y=[4, 4, 2.4, 2.4, 3.4, 3.4, 4], mode="lines",
                             line=dict(color="#bbb", width=2)))
    for c in show:                                                                # orange: the jump at a cut
            fig.add_trace(go.Scatter(x=[HX[c - 1], HX[c]], y=[HY[c - 1], HY[c]], mode="lines",
                                     line=dict(color=ORANGE, width=4)))
    fig.add_trace(go.Scatter(x=HX[:k + 1], y=HY[:k + 1], mode="markers", marker=dict(size=4, color=GREY)))
    for cut, ((rng_, bear, n), col, idx) in POLES.items():
        if cut > k:
            continue
        idx = list(idx)
        fig.add_trace(go.Scatter(x=HX[idx], y=HY[idx], mode="markers", marker=dict(size=6, color=col)))
        lx, ly = X + rng_ * np.cos(TH + bear), Y + rng_ * np.sin(TH + bear)
        fig.add_trace(go.Scatter(x=[X, lx], y=[Y, ly], mode="lines", line=dict(color=col, width=2, dash="dash")))
        fig.add_trace(go.Scatter(x=[lx], y=[ly], mode="markers",
                                 marker=dict(size=16, color=col, symbol="circle-open", line=dict(width=3))))
        right = lx < 3                                                            # pink: right of the pole, clear of the beams
        fig.add_annotation(x=lx, y=ly, text=m(f"r = {rng_:.2f} m, φ = {np.degrees(bear):.0f}°") + f"<br>{n} beams",
                           showarrow=False, yshift=6 if right else -46, xshift=22 if right else 0,
                           xanchor="left" if right else "center", font=dict(size=17, color=col))
    if not final and k >= 0:                                                      # blue: the beam being read
        fig.add_trace(go.Scatter(x=[X, HX[k]], y=[Y, HY[k]], mode="lines+markers", line=dict(color=BLUE, width=3),
                                 marker=dict(size=[0, 13], color=BLUE, symbol="circle-open", line=dict(width=3))))
    fig.add_trace(go.Scatter(x=[X, X + 0.4 * np.cos(TH)], y=[Y, Y + 0.4 * np.sin(TH)], mode="lines+markers",
                             line=dict(color=RED, width=4), marker=dict(size=[10, 0], color=RED)))
    for j, (s, col) in enumerate(lines):
        fig.add_annotation(x=0.0, y=0.165 - 0.06 * j, xref="paper", yref="paper", xanchor="left", showarrow=False,
                           text=s, font=dict(size=20, color=col))
    fig.update_xaxes(range=[-0.3, 7.3], dtick=1, title="x (m)")
    fig.update_yaxes(range=[-0.3, 4.3], dtick=1, title="y (m)", scaleanchor="x", domain=[0.3, 1])
    fig.update_layout(template="simple_white", width=1000, height=880, font=FONT, showlegend=False,
                      margin=dict(l=80, r=30, t=80, b=20), title=dict(text=title, x=0.5, font=dict(size=22)))
    return fig


def beam(k):
    return m(f"beam {DEG[k]}°: {r[k]:.2f} m")


figs, holds, keys = [], [], []


def add(k, title, lines, hold, key=False, final=False, show=()):
    figs.append(frame(k, title, lines, final, show))
    holds.append(hold)
    if key:
        keys.append(len(figs) - 1)


add(-1, "the scan: 360 beams, read in order from −180° (straight behind)",
    [("rule 1: cut wherever the range jumps by more than 0.3 m", ORANGE),
     ("rule 2: keep a piece narrower than 0.35 m that is nearer than both sides", "black"),
     ("rule 3: its bearing = mean of its beams; its range = nearest + 0.1 m", "black"),
     ("blue: the beam being read; grey dots: where the beams hit", GREY)], 10, key=True)
for k in (34, 68, 102, 136):
    add(k, "reading the scan beam by beam", [(beam(k), BLUE), ("no jump above 0.3 m yet: one piece so far", GREY)], 2)
add(139, m("beams −43° to −41°: three cuts"),
    [(m("beams −44° to −41°: 4.15, 4.46, 4.79, 5.11 m"), BLUE),
     ("they graze the bottom wall: each reads over 0.3 m more than the last", ORANGE),
     (m("the piece before −43° is far wider than 0.35 m: wall"), "black"),
     ("the 1-beam pieces at −43° and −42° lie farther than the beam before: wall", "black")], 10, show=CUTS[:3])
add(145, "these beams hit the right wall", [(beam(145), BLUE), ("no jump: same piece", GREY)], 2)
n, w, _ = piece(146)
add(146, m("beam −34°: the range drops: cut"),
    [(m(f"beam −35°: {r[145]:.2f} m; beam −34°: {r[146]:.2f} m"), BLUE),
     (f"jump {r[145] - r[146]:.2f} m > 0.3 m: cut", ORANGE),
     (f"piece before: {n} beams, {w:.2f} m wide: too wide, wall", "black")], 8, show=[146])
assert (n, round(w, 2), round(r[145] - r[146], 2)) == (7, 0.62, 1.09)
for k in (147, 148):
    add(k, m(f"beam {DEG[k]}°: close to the beam before: same piece"), [(beam(k), BLUE)], 3, show=[146])
n, w, mean = piece(149)
add(149, m("beam −31°: the range jumps back up: cut; the piece is a pole"),
    [(m(f"beam −32°: {r[148]:.2f} m; beam −31°: {r[149]:.2f} m: jump {r[149] - r[148]:.2f} m: cut"), ORANGE),
     (f"piece: {n} beams at {mean:.3f} m, {w:.3f} m wide < 0.35 m", "black"),
     (f"nearer than both sides ({r[145]:.2f} m and {r[149]:.2f} m): a pole", "black"),
     (m(f"bearing −33.0°; range {r[147]:.3f} + 0.1 = {r[147] + POLE_R:.3f} m"), GREEN)], 18, key=True, show=[146, 149])
assert (n, round(w, 3), round(mean, 3), round(r[147], 3)) == (3, 0.205, 3.915, 3.904)
n, w, _ = piece(150)
add(150, m("beam −30°: the table, 1.00 m away: cut"),
    [(m(f"jump {r[149]:.2f} − {r[150]:.2f} = {r[149] - r[150]:.2f} m: cut"), ORANGE),
     (f"piece before: 1 beam at {r[149]:.2f} m, not nearer than the {r[148]:.2f} m before it: wall", "black")], 8, show=[150])
for k in (170, 190, 203):
    add(k, "the table's near side, beam by beam", [(beam(k), BLUE), ("no jump: same piece", GREY)], 2)
n, w, _ = piece(204)
add(204, "beam 24°: out through the door: cut",
    [("beam 24°: nothing within 8 m, so it reads 8 m (off the picture)", BLUE),
     (f"jump {r[203]:.2f} → {r[204]:.2f} m: cut", ORANGE),
     (f"piece before: {n} beams, {w:.2f} m wide: the table, too wide", "black")], 8, show=[204])
assert (n, round(w, 2)) == (54, 1.34)
for k in (212, 221):
    add(k, "through the door: about 8 m, off the picture", [(beam(k), BLUE), ("no jump: same piece", GREY)], 2)
n, w, _ = piece(222)
add(222, "beam 42°: the top wall: cut",
    [(beam(222), BLUE), (f"jump {r[221]:.2f} → {r[222]:.2f} m: cut", ORANGE),
     (f"piece before: {n} beams through the door, {w:.2f} m wide: too wide", "black")], 8, show=[222])
for k in (240, 264):
    add(k, "the top wall, beam by beam", [(beam(k), BLUE), ("no jump: same piece", GREY)], 2)
n, w, _ = piece(265)
add(265, "beam 85°: the range drops: cut",
    [(f"beam 84°: {r[264]:.2f} m; beam 85°: {r[265]:.2f} m", BLUE),
     (f"jump {r[264] - r[265]:.2f} m > 0.3 m: cut", ORANGE),
     (f"piece before: {n} beams of top wall, {w:.2f} m wide: too wide", "black")], 8, show=[265])
for k in (267, 269):
    add(k, f"beam {DEG[k]}°: close to the beam before: same piece", [(beam(k), BLUE)], 3, show=[265])
n, w, mean = piece(270)
add(270, "beam 90°: the range jumps back up: cut; the piece is a pole",
    [(f"beam 89°: {r[269]:.2f} m; beam 90°: {r[270]:.2f} m: jump {r[270] - r[269]:.2f} m: cut", ORANGE),
     (f"piece: {n} beams at {mean:.3f} m, {w:.3f} m wide < 0.35 m", "black"),
     (f"nearer than both sides ({r[264]:.2f} m and {r[270]:.2f} m): a pole", "black"),
     (f"bearing 87.0°; range {r[266]:.3f} + 0.1 = {r[266] + POLE_R:.3f} m", PINK)], 18, key=True, show=[265, 270])
assert (n, round(w, 3), round(mean, 3), round(r[266], 3)) == (5, 0.188, 2.153, 2.132)
for k in (300, 330):
    add(k, "the rest of the scan, beam by beam", [(beam(k), BLUE), ("no jump: same piece", GREY)], 2)
n, w, _ = piece(137)                                          # the piece from 90 deg runs on into the first one
add(359, "beam 179°: back where the scan began",
    [(beam(359), BLUE), ("the last piece runs on into the first: the scan is a circle", GREY),
     (f"that piece: {n} beams, {w:.2f} m wide: wall", "black")], 8)
assert (n, round(w, 2)) == (227, 7.19)
add(359, "360 scan points (grey) and the two poles extracted from them",
    [("pink: 5 beams → range 2.232 m, bearing 87.0°", PINK),
     (m("green: 3 beams → range 4.004 m, bearing −33.0°"), GREEN),
     ("every other piece is too wide or not nearer than both sides", GREY)], 28, key=True, final=True)
make_gif(figs, here / "scan_extract", fps=4, holds=holds, keys=keys, cols=2, width=900)

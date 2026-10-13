"""Animation: two quality-of-service settings on the room robot's topics. Top, reliability: the lidar driver sends a
scan every 0.1 s from 2.2 s over a link that loses the 2.4 s scan. With best effort the 2.4 s scan is simply gone and
the 2.5 s scan arrives on time. With reliable delivery the lost scan is sent again; here its copy arrives 0.15 s late,
at 2.55 s (how late depends on the link and the middleware), and the 2.5 s scan is held back until then, because
reliable delivery keeps the order. At 2.5 s the planner's newest scan is 2.5 with best effort but 2.3 with reliable.
Bottom, durability: the map server publishes the map once, at 0 s; a node that starts at 5 s gets nothing with
volatile durability and the stored map at once with transient local. Run -> qos.gif, qos_frames.png"""
from pathlib import Path

import netdraw as nd
from gifkit import BLUE, GREEN, GREY, ORANGE, PURPLE, RED, make_gif

here = Path(__file__).parent
SENT = [2.2, 2.3, 2.4, 2.5, 2.6, 2.7]
BEST = {t: t for t in SENT if t != 2.4}
REL = {}
for t in SENT:
    REL[t] = max([2.55 if t == 2.4 else t] + list(REL.values()))
assert REL[2.4] == 2.55 and REL[2.5] == 2.55 and 2.4 not in BEST


def newest(arr, now):
    got = [t for t, a in arr.items() if a <= now + 1e-9]
    return max(got) if got else None


assert newest(BEST, 2.5) == 2.5 and newest(REL, 2.5) == 2.3
T0, T1, X0, X1 = 2.15, 2.75, 0.30, 0.97
X = lambda t: X0 + (t - T0) / (T1 - T0) * (X1 - X0)
D0, D1 = -0.3, 6.3
XD = lambda t: X0 + (t - D0) / (D1 - D0) * (X1 - X0)
ROWS = {"sent": 0.86, "best": 0.76, "rel": 0.66}
DROWS = {"pub": 0.36, "vol": 0.26, "tl": 0.16}


def frame(phase, now):
    fig = nd.blank()
    a = phase == "A"
    nd.text(fig, 0.02, 0.985, "<b>reliability</b>: a scan is lost on the link", size=21, color="black" if a else GREY)
    for key, y in ROWS.items():
        lab = {"sent": "lidar driver sends", "best": "best effort: planner gets", "rel": "reliable: planner gets"}[key]
        nd.text(fig, 0.02, y, lab, size=18, valign="middle", color="black" if a else GREY)
        fig.add_shape(type="line", opacity=1, xref="paper", yref="paper", x0=X0, x1=X1, y0=y, y1=y,
                      line=dict(color="#DDDDDD", width=2))
    for t in (2.2, 2.3, 2.4, 2.5, 2.6, 2.7):
        nd.text(fig, X(t), 0.60, f"{t:.1f}", size=16, color=GREY, anchor="center")
    nd.text(fig, X1, 0.565, "time (s)", size=16, color=GREY, anchor="right")
    cur = now if a else 2.75
    for t in SENT:
        if t <= cur + 1e-9:
            nd.dot(fig, (X(t), ROWS["sent"]), ORANGE, f"{t:.1f}" if t != 2.4 else None)
    if cur >= 2.4 - 1e-9:
        nd.text(fig, X(2.4), ROWS["best"], "✕ lost", size=19, color=RED, anchor="center", valign="middle")
    for t, arr in BEST.items():
        if arr <= cur + 1e-9:
            nd.dot(fig, (X(arr), ROWS["best"]), BLUE)
    for t, arr in REL.items():
        if arr <= cur + 1e-9:
            if t == 2.4:
                nd.dot(fig, (X(arr), ROWS["rel"] + 0.022), PURPLE, "2.4, sent again", label_side="left", font=15)
            elif t == 2.5:
                nd.dot(fig, (X(arr), ROWS["rel"] - 0.022), BLUE, "2.5, held back", label_side="left", font=15)
            else:
                nd.dot(fig, (X(arr), ROWS["rel"]), BLUE)
    if cur >= 2.4 - 1e-9 and cur < 2.55 - 1e-9:
        nd.text(fig, X(2.47), ROWS["rel"] + 0.035, "2.4 being sent again; 2.5 waits", size=16, color=PURPLE,
                anchor="center", valign="bottom")
    if a:
        fig.add_shape(type="line", opacity=1, xref="paper", yref="paper", x0=X(now), x1=X(now), y0=0.62, y1=0.92,
                      line=dict(color=GREEN, width=3, dash="dot"))
        nb, nr = newest(BEST, now), newest(REL, now)
        nd.text(fig, 0.02, 0.52, f"<b>t = {now:.2f} s</b>: the planner's newest scan is from {nb:.1f} s with best "
                f"effort, {nr:.1f} s with reliable", size=19)
    # durability
    b = phase == "B"
    nd.text(fig, 0.02, 0.45, "<b>durability</b>: a node starts late, at 5 s", size=21, color="black" if b else GREY)
    for key, y in DROWS.items():
        lab = {"pub": "map server: /map, once", "vol": "volatile: late node gets", "tl": "transient local: late node gets"}[key]
        nd.text(fig, 0.02, y, lab, size=18, valign="middle", color="black" if b else GREY)
        fig.add_shape(type="line", opacity=1, xref="paper", yref="paper", x0=X0, x1=X1, y0=y, y1=y,
                      line=dict(color="#DDDDDD", width=2))
    for t in range(0, 7):
        nd.text(fig, XD(t), 0.10, f"{t}", size=16, color=GREY, anchor="center")
    nd.text(fig, X1, 0.065, "time (s)", size=16, color=GREY, anchor="right")
    dcur = now if b else -1
    if dcur >= 0:
        nd.dot(fig, (XD(0), DROWS["pub"]), ORANGE, "the map, 11,200 cells")
    if dcur >= 5:
        nd.text(fig, XD(5), DROWS["vol"], "nothing", size=18, color=RED, anchor="center", valign="middle",
                )
        nd.dot(fig, (XD(5), DROWS["tl"]), BLUE, "the stored map, at once", label_side="left")
    if b:
        fig.add_shape(type="line", opacity=1, xref="paper", yref="paper", x0=XD(now), x1=XD(now), y0=0.12, y1=0.40,
                      line=dict(color=GREEN, width=3, dash="dot"))
        nd.text(fig, 0.02, 0.03, f"<b>t = {now:.0f} s</b>" + (": the late node started at 5 s and subscribed" if now >= 5 else
                ""), size=19, valign="bottom")
    return fig


A = [round(2.20 + 0.05 * i, 2) for i in range(11)]
figs = [frame("A", t) for t in A] + [frame("B", float(t)) for t in range(0, 7)]
holds = [4] + [2] * 10 + [5] + [2] * 5 + [12]
holds[A.index(2.5)] = 6
make_gif(figs, here / "qos", fps=3, holds=holds, keys=[A.index(2.5), A.index(2.6), len(A) + 1, len(figs) - 1],
         cols=2, width=900)

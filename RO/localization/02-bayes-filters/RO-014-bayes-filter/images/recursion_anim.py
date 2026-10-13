"""Figure 3 as an animation: two ways to know the door belief, step by step. Archive (top row): every command and
reading is stored, and the belief is recomputed from all of them, by summing over every door history. Filter (bottom
row): only the last belief is kept; the newest command u_t and reading z_t turn it into the new belief, and then
they and the old belief are dropped. Both give open 0.5 -> 0.75 -> 0.983. The last frame is the general step:
the archive keeps growing (36,000 readings after an hour at 10 a second), the filter stores one belief.
Grey: stored entries; purple: command; green: reading; blue: belief. Run -> recursion_anim.gif"""
from itertools import product
from pathlib import Path

import plotly.graph_objects as go

from doorplot import P_X, P_Z, STATES, predict, update
from gifkit import BLUE, FONT, GREEN, GREY, PURPLE, make_gif

here = Path(__file__).parent
RUN = [("do nothing", "sense open"), ("push", "sense open")]
LIGHT = {GREY: "#EEEEEE", BLUE: "#E4EBF2", PURPLE: "#F4EBF2", GREEN: "#E8F3E7"}
BH = 1.15                                                                      # box height


def archive_belief(steps):
    """The belief from its definition: sum over every door history, weighted by every command and reading so far."""
    w = {x: 0.0 for x in STATES}
    for hist in product(STATES, repeat=len(steps) + 1):
        p = 0.5
        for (u, z), a, b in zip(steps, hist, hist[1:]):
            p *= P_X[u][a][b] * P_Z[b][z.split()[1]]
        w[hist[-1]] += p
    return w["open"] / sum(w.values())


BEL = [0.5]
for u, z in RUN:
    BEL.append(update(predict({"open": BEL[-1], "closed": 1 - BEL[-1]}, u), z.split()[1])["open"])
    assert abs(archive_belief(RUN[:len(BEL) - 1]) - BEL[-1]) < 1e-12           # archive and filter agree
assert [round(b, 3) for b in BEL] == [0.5, 0.75, 0.983]


def num(v):
    return f"{v:.3f}".rstrip("0")


def box(fig, x, y, w, text, col, size=19):
    fig.add_shape(type="rect", x0=x - w / 2, x1=x + w / 2, y0=y - BH / 2, y1=y + BH / 2, line=dict(color=col, width=2),
                  fillcolor=LIGHT[col], opacity=1)
    fig.add_annotation(x=x, y=y, text=text, showarrow=False, font=dict(size=size))


def arrow(fig, a, b):
    fig.add_annotation(x=b[0], y=b[1], ax=a[0], ay=a[1], axref="x", ayref="y", text="", showarrow=True, arrowhead=2,
                       arrowsize=1.2, arrowwidth=2.5, arrowcolor=GREY)


def note(fig, x, y, text, col=GREY, size=18, bold=False):
    fig.add_annotation(x=x, y=y, text=f"<b>{text}</b>" if bold else text, showarrow=False, xanchor="left",
                       font=dict(size=size, color=col))


def sub(t):
    return f"<sub>{t}</sub>"


def entry(k, t):
    """The archive's entries: command then reading for each step, numbered from 1."""
    u, z = RUN[t - 1]
    return [f"u{sub(t)}<br>{u}", f"z{sub(t)}<br>{z}"][k]


def frame(title, subt, n_steps, arch_bel=None, kept=None, step=None, new=None, slide=None, final=False):
    """n_steps: steps stored in the archive; arch_bel: (t, value) of the archive's result box; kept: (t, value) of
    the filter's stored belief; step: t whose u_t and z_t feed the filter; new: (t, value) of the filter's result;
    slide: x position of the new belief moving into the stored place."""
    fig = go.Figure()
    note(fig, 0.0, 7.55, "archive: recompute from everything", "black", 22, bold=True)
    texts = [entry(k, t) for t in range(1, n_steps + 1) for k in (0, 1)]
    if final:
        texts += ["⋯", f"u{sub('t')}", f"z{sub('t')}"]
    x, right = 0.0, None
    for s in texts:
        if s == "⋯":
            fig.add_annotation(x=x + 0.45, y=6.2, text="⋯", showarrow=False, font=dict(size=30, color=GREY))
            x += 0.9
            continue
        w = 1.5 if "<br>" in s else 1.0                       # door-world entries carry their words
        box(fig, x + w / 2, 6.2, w, s, GREY, 20)
        right = x + w
        x += w + 0.15
    if arch_bel or final:
        if right is not None:
            arrow(fig, (right + 0.15, 6.2), (10.6, 6.2))
        t, v = arch_bel if arch_bel else ("t", None)
        box(fig, 11.8, 6.2, 2.3, f"bel(x{sub(t)})" + (f"<br>open {num(v)}" if v is not None else ""), BLUE, 20)
    n = 2 * n_steps
    note(fig, 0.0, 5.15, "after an hour at 10 readings a second: 36,000 readings, and growing" if final else
         (f"{n} entries, all read again at every step" if n else "no entries yet"))
    note(fig, 0.0, 4.25, "filter: update the last belief", "black", 22, bold=True)
    if final:
        kept, step, new = ("t-1", None), "t", ("t", None)
    if kept:
        t, v = kept
        box(fig, 1.5, 2.4, 2.4, f"bel(x{sub(t)})" + (f"<br>open {num(v)}" if v is not None else ""), BLUE, 20)
    if step is not None:
        lab = ([f"u{sub(step)}", f"z{sub(step)}"] if final else
               [f"u{sub(step)}<br>{RUN[step - 1][0]}", f"z{sub(step)}<br>{RUN[step - 1][1]}"])
        box(fig, 5.0, 3.35, 1.9, lab[0], PURPLE)
        box(fig, 5.0, 1.45, 1.9, lab[1], GREEN)
    if new:
        t, v = new
        arrow(fig, (2.75, 2.4), (7.75, 2.4))
        arrow(fig, (5.95, 3.35), (7.75, 2.6))
        arrow(fig, (5.95, 1.45), (7.75, 2.2))
        box(fig, 9.0, 2.4, 2.4, f"bel(x{sub(t)})" + (f"<br>open {num(v)}" if v is not None else ""), BLUE, 20)
    if slide is not None:
        t, v, x = slide
        box(fig, x, 2.4, 2.4, f"bel(x{sub(t)})<br>open {num(v)}", BLUE, 20)
    note(fig, 0.0, 0.55, "stores one belief, whatever the length of the run")
    fig.update_layout(template="simple_white", width=1200, height=700, font=FONT, showlegend=False,
                      margin=dict(l=20, r=20, t=110, b=10),
                      xaxis=dict(range=[-0.1, 13.1], visible=False), yaxis=dict(range=[0, 8.0], visible=False),
                      title=dict(text=f"{title}<br><span style='font-size:19px'>{subt}</span>", x=0.5, y=0.97,
                                 yanchor="top", font=dict(size=24)))
    return fig


figs, holds, keys = [], [], []


def add(f, hold, key=False):
    if key:
        keys.append(len(figs))
    figs.append(f)
    holds.append(hold)


add(frame("t = 0: the robot has no information", "both ways start from the belief 0.5 for open", 0, (0, 0.5), (0, 0.5)),
    9, key=True)
for t, (u, z) in enumerate(RUN, start=1):
    old, v = BEL[t - 1], BEL[t]
    add(frame(f"t = {t}: command u{sub(t)} = {u}, reading z{sub(t)} = {z}",
              "the archive stores both; the filter uses them once", t, None, (t - 1, old), t), 8, key=t == 1)
    add(frame(f"t = {t}: both ways give bel(x{sub(t)}) = {num(v)} for open",
              f"the archive recomputed it from all {2 * t} entries; the filter from {num(old)}, u{sub(t)} and z{sub(t)}",
              t, (t, v), (t - 1, old), t, (t, v)), 10, key=True)
    for x in (6.5, 4.0):
        add(frame(f"the filter keeps {num(v)} and drops {num(old)}, u{sub(t)} and z{sub(t)}",
                  f"the archive keeps all {2 * t} entries", t, (t, v), slide=(t, v, x)), 1)
    add(frame(f"the filter keeps {num(v)} and drops {num(old)}, u{sub(t)} and z{sub(t)}",
              f"the archive keeps all {2 * t} entries", t, (t, v), (t, v)), 8, key=t == 2)
add(frame("the archive grows by two entries every step; the filter keeps one belief",
          "the filter turns bel(x<sub>t-1</sub>) into bel(x<sub>t</sub>) with only u<sub>t</sub> and z<sub>t</sub>",
          2, final=True), 22, key=True)
make_gif(figs, here / "recursion_anim", fps=4, holds=holds, keys=keys, cols=2, width=950)

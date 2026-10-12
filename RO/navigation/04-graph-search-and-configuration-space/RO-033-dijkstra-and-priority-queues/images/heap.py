"""Figure 5: the binary min-heap behind Dijkstra's algorithm on the waypoint graph, step by step. Each entry is a
waypoint with its tentative distance. The heap is a tree filled level by level, left to right, in which every entry
is at most the entries below it, so the smallest sits at the top; the same entries are stored in a list (bottom
row), the children of position i at 2i + 1 and 2i + 2. Insert: place the entry at the end, then swap it with its
parent while it is smaller (sift up). Remove the smallest: take the top, move the last entry to the top, then swap it
with its smaller child while it is larger (sift down). The pushes and removals are those of Dijkstra's run, which
stops when G 3.505 comes off; G 5.022 is a stale entry left behind when G's distance dropped.
Run: python heap.py -> heap.gif, heap_frames.png"""
import math
from pathlib import Path

import plotly.graph_objects as go
from gifkit import BLUE, FONT, GREEN, GREY, ORANGE, RED, make_gif
from roomsearch import MinHeap, dijkstra, wp_dist, wp_nbrs

here = Path(__file__).parent
R = dijkstra(wp_nbrs, "S", "G")
d = lambda a, b: wp_dist(a, b)
SP = d("S", "P")
OPS = [("push", (0.0, "S")), ("pop", None), ("push", (1.0, "A")), ("push", (2.5, "D")), ("push", (SP, "P")),
       ("pop", None), ("push", (3.0, "B")), ("pop", None), ("push", (SP + d("P", "G"), "G")), ("pop", None),
       ("push", (2.5 + d("D", "C"), "C")), ("push", (2.5 + d("D", "G"), "G")), ("pop", None), ("pop", None)]
# the same pushes and removals as Dijkstra's run (one push per new or lowered entry, one removal per settled vertex)
assert [s["cur"] for s in R["snaps"]] == ["S", "A", "P", "D", "B", "G"]


def lab(e):
    return f"{e[1]} {e[0]:.3f}"


def pos(i):
    L = int(math.log2(i + 1))
    p = i - (2 ** L - 1)
    return ((p + 0.5) / 2 ** L - 0.5) * 6, -L


def frame(a, title, lines, hl=(), out=None, done=()):
    """a: the heap list; hl: indexes drawn red (being compared or swapped); out: an entry just taken off."""
    fig = go.Figure()
    for i in range(1, len(a)):
        (x0, y0), (x1, y1) = pos((i - 1) // 2), pos(i)
        fig.add_trace(go.Scatter(x=[x0, x1], y=[y0 - 0.2, y1 + 0.2], mode="lines", line=dict(color="#999", width=2),
                                 hoverinfo="skip"))
    def box(x, y, w, hgt, red):
        fig.add_trace(go.Scatter(x=[x - w, x + w, x + w, x - w, x - w], y=[y - hgt, y - hgt, y + hgt, y + hgt, y - hgt],
                                 mode="lines", fill="toself", fillcolor="#fdd0a2", hoverinfo="skip",
                                 line=dict(color=RED if red else "#666", width=5 if red else 2)))

    for i, e in enumerate(a):
        x, y = pos(i)
        box(x, y, 0.58, 0.2, i in hl)
        fig.add_annotation(x=x, y=y, text=f"<b>{lab(e)}</b>", showarrow=False, font=dict(size=19))
        fig.add_annotation(x=x - 0.66, y=y, text=str(i), showarrow=False, xanchor="right", font=dict(size=16, color=GREY))
    for i, e in enumerate(a):                                   # the same entries as a list
        box(-3.2 + 1.2 * i, -3.25, 0.55, 0.2, i in hl)
        fig.add_annotation(x=-3.2 + 1.2 * i, y=-3.25, text=lab(e), showarrow=False, font=dict(size=17))
        fig.add_annotation(x=-3.2 + 1.2 * i, y=-3.6, text=str(i), showarrow=False, font=dict(size=14, color=GREY))
    fig.add_annotation(x=-3.9, y=-3.25, text="list:", showarrow=False, xanchor="right", font=dict(size=17))
    if out:
        fig.add_annotation(x=2.6, y=0.25, text=f"taken off:<br><b>{lab(out)}</b>", showarrow=False,
                           font=dict(size=19, color=BLUE), align="left")
    if done:
        fig.add_annotation(x=-2.9, y=0.25, text="settled: " + ", ".join(done), showarrow=False, align="left",
                           font=dict(size=17, color=BLUE), xanchor="left")
    fig.update_xaxes(range=[-4.3, 4.0], visible=False)
    fig.update_yaxes(range=[-4.0, 0.6], visible=False)
    fig.update_layout(template="simple_white", width=1000, height=760, font=FONT, showlegend=False,
                      margin=dict(l=20, r=20, t=70, b=150), title=dict(text=title, x=0.5, font=dict(size=22)))
    rows = [("every entry is at most the entries below it, so the smallest is at the top; grey numbers: positions in the list",
             GREY)] + lines
    for k, (s, col) in enumerate(rows):
        fig.add_annotation(x=0.0, y=-0.02 - 0.06 * k, xref="paper", yref="paper", xanchor="left", yanchor="top",
                           showarrow=False, text=s, font=dict(size=19, color=col))
    return fig


h = MinHeap()
figs, holds, keys, done = [], [], [], []
figs.append(frame([], "an empty heap", [("Dijkstra's run puts S in first, with distance 0", "black")]))
holds.append(6)
for op, item in OPS:
    n0 = len(h.steps)
    if op == "push":
        h.push(item)
        new = h.steps[n0:]
        for k, (what, arr, (i, j)) in enumerate(new):
            if what == "place":
                p = (j - 1) // 2
                if j and k + 1 < len(new):
                    lines = [(f"insert {lab(item)}: place it at the end, position {j}", ORANGE),
                             (f"it is smaller than its parent {lab(arr[p])}: swap them (sift up)", RED)]
                elif j:
                    lines = [(f"insert {lab(item)}: place it at the end, position {j}", ORANGE),
                             (f"its parent {lab(arr[p])} is not larger: it stays", GREEN)]
                else:
                    lines = [(f"insert {lab(item)}: the heap was empty, so it is the top", ORANGE)]
                figs.append(frame(arr, f"insert {lab(item)}", lines, hl=(j, p) if j else (0,), done=done))
            else:
                p = (i - 1) // 2
                more = k + 1 < len(new)
                lines = [(f"swapped: {lab(arr[i])} moved up to position {i}", RED)]
                if not more:
                    lines.append(((f"its parent {lab(arr[p])} is smaller: stop" if i else "it reached the top: stop"),
                                  GREEN))
                figs.append(frame(arr, f"insert {lab(item)}: sift up", lines, hl=(i,), done=done))
            holds.append(5)
    else:
        top = h.a[0]
        before = list(h.a)
        h.pop()
        done.append(top[1])
        stop = top[1] == "G"
        figs.append(frame(before, f"remove the smallest: {lab(top)}",
                          [("the smallest entry is at the top: take it off", BLUE)] +
                          ([("G is the goal: Dijkstra stops here", GREEN),
                            ("G 5.022 stays behind: a stale entry, skipped if it ever came off", GREY)] if stop else []),
                          hl=(0,), done=done[:-1]))
        holds.append(6)
        if top[1] in ("P", "B"):
            keys.append(len(figs) - 1)
        for k, (what, arr, (i, j)) in enumerate([] if stop else h.steps[n0:]):
            if what == "last to root":
                kids = [c for c in (1, 2) if c < len(arr)]
                small = min(kids, key=lambda c: arr[c][0]) if kids else None
                lines = [(f"move the last entry, {lab(arr[0])}, to the top", ORANGE)]
                if small is not None and arr[small][0] < arr[0][0]:
                    lines.append((f"its smaller child {lab(arr[small])} is smaller: swap (sift down)", RED))
                else:
                    lines.append(("no child is smaller: the heap is fixed", GREEN))
                figs.append(frame(arr, "remove the smallest: refill the top", lines, hl=(0, small) if small else (0,),
                                  out=top, done=done))
            else:
                figs.append(frame(arr, "remove the smallest: sift down",
                                  [(f"swapped: {lab(arr[i])} moved up, {lab(arr[j])} down to position {j}", RED),
                                   ("no child below it is smaller: stop", GREEN)], hl=(j,), out=top, done=done))
                if top[1] == "B":
                    keys.append(len(figs) - 1)
            holds.append(6)
        if stop:
            holds[-1] = 30
            break
assert [e for e in h.a] == [(2.5 + d("D", "C"), "C"), (SP + d("P", "G"), "G")]
keys = sorted(set([0] + keys + [len(figs) - 1]))
# the frame where G 3.505 sifts up past G 5.022
SIFT = next(k for k, f in enumerate(figs) if "sift up" in (f.layout.title.text or ""))
keys = sorted(set([k for k in keys if k] + [5, SIFT]))[:6]
make_gif(figs, here / "heap.gif", fps=2, holds=holds, keys=keys, cols=2, width=900)
print(len(figs), "frames; keys", keys)

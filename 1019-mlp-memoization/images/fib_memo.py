"""fib(5) call by call, twice on the same tree: plain recursion (all 15 calls, in the order Python makes them), then
with memoization (9 calls: 4 values computed, 5 looked up; the subtrees under a looked-up call are never visited).
The call order and counts come from running the two functions of section 3 with a tracer.
Plotly frames (a fixed tree whose nodes light up) -> ffmpeg GIF, plus a grid of key frames for the PDF."""
import shutil
import subprocess
from pathlib import Path

import plotly.graph_objects as go
from PIL import Image

HERE = Path(__file__).parent
BLUE, ORANGE, GREEN, GREY = "#4C78A8", "#F58518", "#54A24B", "#D0D0D0"

# the full call tree of plain fib(5): node id = path of L/R choices
NODES, EDGES = {}, []


def build(n, path, x, y, w):
    NODES[path] = (n, x, y)
    if n >= 2:
        for side, dx, m in (("L", -w, n - 1), ("R", w, n - 2)):
            EDGES.append((path, path + side))
            build(m, path + side, x + dx, y - 1, w * 0.52)


build(5, "", 0.0, 0.0, 3.6)
assert len(NODES) == 15


def plain_order():
    out = []

    def fib(n, path):
        out.append((path, "computed"))
        if n < 2:
            return 1
        return fib(n - 1, path + "L") + fib(n - 2, path + "R")

    fib(5, "")
    return out


def memo_order():
    out, d = [], {0: 1, 1: 1}

    def fib(n, path):
        if n in d:
            out.append((path, "looked up"))
            return d[n]
        out.append((path, "computed"))
        d[n] = fib(n - 1, path + "L") + fib(n - 2, path + "R")
        return d[n]

    fib(5, "")
    return out


PLAIN, MEMO = plain_order(), memo_order()
assert len(PLAIN) == 15 and len(MEMO) == 9 and sum(k == "computed" for _, k in MEMO) == 4


def frame(order, upto, head):
    state = dict(order[:upto])
    fig = go.Figure()
    for a, b in EDGES:
        on = a in state and b in state
        fig.add_scatter(x=[NODES[a][1], NODES[b][1]], y=[NODES[a][2], NODES[b][2]], mode="lines",
                        line=dict(color="#555" if on else GREY, width=2.5 if on else 1.2), hoverinfo="skip")
    for path, (n, x, y) in NODES.items():
        kind = state.get(path)
        col = {"computed": BLUE, "looked up": ORANGE}.get(kind, "white")
        fig.add_scatter(x=[x], y=[y], mode="markers+text", text=[f"fib({n})"], hoverinfo="skip",
                        textfont=dict(size=17, color="white" if kind else "#AAA"),
                        marker=dict(size=58, symbol="square", color=col, line=dict(color="#555" if kind else GREY,
                                                                                   width=2)))
    comp = sum(k == "computed" for k in state.values())
    look = sum(k == "looked up" for k in state.values())
    tail = f"calls so far: <b>{len(state)}</b>" + (f" ({comp} computed, {look} looked up)" if order is MEMO else "")
    fig.update_layout(template="simple_white", width=1100, height=640, showlegend=False,
                      font=dict(family="Latin Modern Roman", size=21),
                      title=dict(text=f"<b>{head}</b><br>{tail}", x=0.5, y=0.95, font=dict(size=23)),
                      xaxis=dict(visible=False, range=[-8.0, 7.4]), yaxis=dict(visible=False, range=[-4.6, 0.6]),
                      margin=dict(l=10, r=10, t=100, b=10))
    return fig


if __name__ == "__main__":
    tmp = HERE / ".fm_frames"
    tmp.mkdir(exist_ok=True)
    n, last = 0, {}
    for tag, order, head in (("p", PLAIN, "Plain recursion: every call runs its whole subtree"),
                             ("m", MEMO, "With memoization: blue = computed and stored, orange = looked up")):
        for k in range(1, len(order) + 1):
            f = tmp / f"{tag}{k}.png"
            frame(order, k, head).write_image(f)
            for _ in range(1 if k < len(order) else 5):
                shutil.copy(f, tmp / f"{n:03d}.png")
                n += 1
        last[tag] = f
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "2", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=820:-1:flags=lanczos,split[a][b];[a]palettegen=max_colors=64[p];[b][p]paletteuse",
                    str(HERE / "fib_memo.gif")], check=True)
    ims = [Image.open(last[t]).convert("RGB") for t in ("p", "m")]
    w, h = ims[0].size
    sheet = Image.new("RGB", (w, 2 * h + 16), "white")
    for i, im in enumerate(ims):
        sheet.paste(im, (0, i * (h + 16)))
    sheet.save(HERE / "fib_memo_frames.png")
    shutil.rmtree(tmp)

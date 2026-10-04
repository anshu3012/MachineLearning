"""The Learning path, grown backwards from one Note: the perceptron Note (DL-004) lists the Notes to read first, and each
of those lists its own (two rounds). Data: course_map/concepts.yaml through course_map/build_map.py
(read only; the same "Read first" rule as the Learning path table, the last four earlier Notes).
Plotly frames -> ffmpeg GIF, plus a grid of the key frames for the PDF."""
import re
import shutil
import subprocess
import sys
from pathlib import Path

import plotly.graph_objects as go

HERE = Path(__file__).parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(ROOT / "course_map"))
import build_map as bm  # noqa: E402

TARGET, ROUNDS = 1004, 2
FONT = dict(family="Latin Modern Roman", size=20)
COL = ["#F58518", "#4C78A8", "#54A24B", "#B279A2"]


def read_first(v):
    """The Learning path table's rule: the four latest earlier Notes that teach a Concept this Note builds on."""
    _, before, _, _ = bm.neighbours(v)
    return sorted(set(before.values()))[-4:]


def title(v):
    t = bm.note_file(v).read_text()
    t = re.search(r'^title:\s*"?(.*?)"?$', t, re.M).group(1)
    t = re.sub(r"\s*\(.*?\)", "", t)
    t = t.split(":")[0]
    words, lines = t.split(), [""]
    for w in words:                                  # wrap to lines of about 18 characters
        if len(lines[-1]) + len(w) > 18 and lines[-1]:
            lines.append("")
        lines[-1] = (lines[-1] + " " + w).strip()
    if len(lines) > 2:                               # cut a long title at two lines, without a dangling "and"
        lines = lines[:2]
        lines[1] = lines[1].rstrip(",").removesuffix(" and").rstrip(",")
    return "<br>".join(lines)


# Grow the tree one round at a time; a Note already placed is not placed again.
layers, edges, seen = [[TARGET]], [], {TARGET}
for _ in range(ROUNDS):
    nxt = []
    for v in layers[-1]:
        for x in read_first(v):
            edges.append((x, v, len(layers)))
            if x not in seen:
                seen.add(x)
                nxt.append(x)
    layers.append(nxt)                                  # kept in the order of the Note each one feeds
assert layers[1] == [71, 363, 520], layers[1]          # the perceptron Note's own "Read first" entries
assert [len(L) for L in layers] == [1, 3, 6], [len(L) for L in layers]

pos = {}
for d, L in enumerate(layers):
    for i, v in enumerate(L):
        pos[v] = (ROUNDS - d, 1.25 * ((len(L) - 1) / 2 - i))
STEP = ["<b>Goal:</b> read the perceptron Note (DL-004)",
        "Round 1: the Notes that DL-004 builds on",
        "Round 2: the Notes that <i>those</i> build on",
        "Read from left to right: every Note's prerequisites come first"]


def frame(k):
    shown = min(k, ROUNDS)
    fig = go.Figure()
    for a, b, d in edges:
        if d <= shown:
            (x0, y0), (x1, y1) = pos[a], pos[b]
            fig.add_annotation(x=x1 - 0.13, y=y1, ax=x0 + 0.13, ay=y0, xref="x", yref="y", axref="x", ayref="y",
                               showarrow=True, arrowhead=3, arrowsize=1.3, arrowwidth=1.6, arrowcolor="#8A8A8A")
    for d, L in enumerate(layers[:shown + 1]):
        fig.add_scatter(x=[pos[v][0] for v in L], y=[pos[v][1] for v in L], mode="markers+text",
                        marker=dict(size=56, color=COL[d], line=dict(width=2, color="white")),
                        text=[f"<b>{v}</b>" for v in L], textfont=dict(color="white", size=20), showlegend=False,
                        hoverinfo="skip")
        for v in L:
            fig.add_annotation(x=pos[v][0], y=pos[v][1] - 0.5, text=title(v), showarrow=False,
                               font=dict(size=17, color="#333"))
    for d in range(ROUNDS + 1):
        lab = "goal" if d == 0 else f"round {d}"
        fig.add_annotation(x=ROUNDS - d, y=4.25, text=f"<b>{lab}</b>", showarrow=False,
                           font=dict(size=22, color=COL[d] if d <= shown else "#DDDDDD"))
    fig.update_layout(template="simple_white", width=1000, height=900, font=FONT,
                      title=dict(text=STEP[k], x=0.5, y=0.97),
                      xaxis=dict(range=[-0.45, ROUNDS + 0.45], visible=False),
                      yaxis=dict(range=[-4.3, 4.5], visible=False), margin=dict(l=10, r=10, t=70, b=10))
    return fig


if __name__ == "__main__":
    tmp = HERE / ".lp_frames"
    tmp.mkdir(exist_ok=True)
    keys = []
    for k in range(len(STEP)):
        p = tmp / f"k{k}.png"
        frame(k).write_image(p)
        keys.append(p)
    seq = [0] * 3 + [1] * 4 + [2] * 4 + [3] * 7
    for j, k in enumerate(seq):
        shutil.copy(keys[k], tmp / f"{j:03d}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "2", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=820:-1:flags=lanczos,split[a][b];[a]palettegen=max_colors=64[p];[b][p]paletteuse",
                    str(HERE / "learning_path.gif")], check=True)
    shutil.copy(keys[3], HERE / "learning_path_frames.png")     # the final frame alone: readable in the PDF
    shutil.rmtree(tmp)

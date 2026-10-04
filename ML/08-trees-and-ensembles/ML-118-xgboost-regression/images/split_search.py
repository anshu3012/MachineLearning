"""XGBoost split search on the Note's four students (lambda = 0): a threshold slides along CGPA, the residuals
fall into a left and a right leaf, and the gain S_left + S_right - S_parent is recorded at every candidate.
The best root split locks, the left leaf is searched the same way, then the leaf outputs appear.
Run: python split_search.py  -> split_search.gif, split_search_frames.png (Plotly frames + ffmpeg)"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from PIL import Image
from plotly.subplots import make_subplots

HERE = Path(__file__).parent
BLUE, ORANGE, GREEN, GREY = "#4C78A8", "#F58518", "#54A24B", "#9A9A9A"
cgpa = np.array([6.7, 9.0, 7.5, 5.0])
r = np.array([4.5, 11, 6, 8]) - 7.375                      # residuals from the mean
S = lambda v: v.sum() ** 2 / len(v) if len(v) else 0.0      # similarity, lambda = 0


def gain(lo, hi, t):
    m = (cgpa >= lo) & (cgpa < hi)
    left, right = r[m & (cgpa < t)], r[m & (cgpa >= t)]
    return S(left), S(right), S(left) + S(right) - S(r[m])


assert np.isclose(gain(0, 99, 8.25)[2], 17.52, atol=0.01) and np.isclose(gain(0, 8.25, 5.85)[2], 5.04, atol=0.01)
assert np.isclose(gain(0, 99, 7.1)[2], 5.06, atol=0.01) and np.isclose(gain(0, 8.25, 7.1)[2], 0.04, atol=0.01)


def frame(title, lo, hi, t, cands, seen, locked, outputs=False):
    fig = make_subplots(rows=1, cols=2, column_widths=[0.6, 0.4], horizontal_spacing=0.12,
                        subplot_titles=("", "gain of each candidate"))
    in_node = (cgpa >= lo) & (cgpa < hi)
    col = [GREY if not m else (BLUE if t is not None and c < t else ORANGE if t is not None else "black")
           for c, m in zip(cgpa, in_node)]
    fig.add_trace(go.Bar(x=cgpa, y=r, width=0.12, marker_color=col, showlegend=False), 1, 1)
    if outputs:
        col = ["black"] * 4
    else:
        fig.add_trace(go.Scatter(x=cgpa, y=r + np.sign(r) * 0.55, mode="text", text=[f"{v:+.3g}" for v in r],
                                 textfont=dict(size=22), showlegend=False), 1, 1)
    fig.data[0].marker.color = col
    fig.add_hline(y=0, line=dict(color="black", width=1), row=1, col=1, exclude_empty_subplots=False)
    for x in locked:
        fig.add_vline(x=x, line=dict(color=GREEN, width=5), row=1, col=1, exclude_empty_subplots=False)
    if t is not None:
        fig.add_vrect(x0=lo, x1=t, fillcolor=BLUE, opacity=0.12, line_width=0, row=1, col=1, exclude_empty_subplots=False)
        fig.add_vrect(x0=t, x1=min(hi, 9.6), fillcolor=ORANGE, opacity=0.12, line_width=0, row=1, col=1, exclude_empty_subplots=False)
        fig.add_vline(x=t, line=dict(color="black", width=3, dash="dash"), row=1, col=1, exclude_empty_subplots=False)
    if outputs:
        for a, b, v in ((4.6, 5.85, 0.625), (5.85, 8.25, -2.125), (8.25, 9.6, 3.625)):
            fig.add_trace(go.Scatter(x=[a, b], y=[v, v], mode="lines", line=dict(color=GREEN, width=6),
                                     showlegend=False), 1, 1)
            fig.add_annotation(x=(a + b) / 2, y=v + (0.6 if v > 0 else -1.3), text=f"output {v:g}",
                               showarrow=False, font=dict(size=21, color=GREEN), row=1, col=1)
    g = [gain(lo, hi, c)[2] if c in seen else 0 for c in cands]
    best = max(seen, key=lambda c: gain(lo, hi, c)[2]) if len(seen) == len(cands) else None
    fig.add_trace(go.Bar(x=[f"< {c:g}" for c in cands], y=g, text=[f"{v:.2f}" if c in seen else "" for v, c in zip(g, cands)],
                         textposition="outside", textfont=dict(size=22), showlegend=False,
                         marker_color=[GREEN if c == best else GREY for c in cands]), 1, 2)
    fig.update_xaxes(range=[4.6, 9.6], title="CGPA", row=1, col=1)
    fig.update_yaxes(range=[-4.2, 4.8], title="residual", row=1, col=1)
    fig.update_yaxes(range=[0, 21], row=1, col=2)
    fig.update_xaxes(title="split CGPA", row=1, col=2)
    fig.update_annotations(font_size=24, selector=dict(text="gain of each candidate"))
    fig.update_layout(template="simple_white", width=1100, height=620, font=dict(family="Latin Modern Roman", size=22),
                      title=dict(text=title, x=0.5, y=0.96), margin=dict(l=80, r=20, t=100, b=70))
    return fig


def sweep(lo, hi, cands, locked, label):
    """Slide the threshold from the first to the last candidate, holding on each one."""
    seq, seen = [], []
    path = np.concatenate([np.linspace(a, b, 5)[:-1] for a, b in zip(cands[:-1], cands[1:])] + [[cands[-1]]])
    for t in path:
        hit = next((c for c in cands if np.isclose(t, c)), None)
        if hit is not None and hit not in seen:
            seen.append(hit)
            sl, sr, g = gain(lo, hi, hit)
            f = frame(f"{label} < {hit:g}: {sl:.2f} + {sr:.2f} - {S(r[(cgpa >= lo) & (cgpa < hi)]):.2f} = {g:.2f}",
                      lo, hi, t, cands, list(seen), locked)
            seq += [f] * 6
        else:
            seq.append(frame(f"{label}: slide the threshold", lo, hi, t, cands, list(seen), locked))
    best = max(cands, key=lambda c: gain(lo, hi, c)[2])
    seq += [frame(f"best: CGPA < {best:g}, gain {gain(lo, hi, best)[2]:.2f}", lo, hi, None, cands, cands,
                  locked + [best])] * 8
    return seq


if __name__ == "__main__":
    seq = [frame("residuals from the mean 7.375 (all in one leaf)", 0, 99, None, [5.85, 7.1, 8.25], [], [])] * 6
    seq += sweep(0, 99, [5.85, 7.1, 8.25], [], "root: CGPA")
    seq += sweep(0, 8.25, [5.85, 7.1], [8.25], "left leaf: CGPA")
    seq += [frame("leaf output = mean of its residuals (lambda = 0)", 0, 8.25, None, [5.85, 7.1], [5.85, 7.1],
                  [8.25, 5.85], outputs=True)] * 14
    tmp = HERE / ".split_frames"
    tmp.mkdir(exist_ok=True)
    done = {}
    for k, f in enumerate(seq):
        if id(f) in done:
            shutil.copy(tmp / f"{done[id(f)]:03d}.png", tmp / f"{k:03d}.png")
        else:
            f.write_image(tmp / f"{k:03d}.png")
            done[id(f)] = k
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "5", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=760:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "split_search.gif")], check=True)
    firsts = sorted(done.values())                      # one index per distinct picture
    titles = [seq[i].layout.title.text for i in firsts]
    pick = [firsts[i] for i, t in enumerate(titles) if t.startswith(("root: CGPA < 7.1", "best: CGPA < 8.25",
                                                                        "left leaf: CGPA < 7.1", "leaf output"))]
    ims = [Image.open(tmp / f"{k:03d}.png").convert("RGB") for k in pick]
    w, h = ims[0].size
    sheet = Image.new("RGB", (2 * w + 16, 2 * h + 16), "white")
    for i, im in enumerate(ims):
        sheet.paste(im, ((i % 2) * (w + 16), (i // 2) * (h + 16)))
    sheet.save(HERE / "split_search_frames.png")
    shutil.rmtree(tmp)

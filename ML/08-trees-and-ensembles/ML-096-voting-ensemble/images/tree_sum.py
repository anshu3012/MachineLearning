"""Adding up the leaves of the probability tree (section 5): three independent models, each right with
probability 0.7. The 8 right/wrong combinations are listed with their probabilities; the four where at least
two models are right light up one at a time, and their probabilities stack up to 0.784, above one model's 0.7.
Run: python tree_sum.py -> tree_sum.gif, tree_sum_frames.png (Plotly frames + ffmpeg)"""
import shutil
import subprocess
from itertools import product
from pathlib import Path

import plotly.graph_objects as go
from PIL import Image
from plotly.subplots import make_subplots

HERE = Path(__file__).parent
P = 0.7
GREEN, RED, GREY = "#54A24B", "#E45756", "#D9D9D9"
SHADES = ["#2E7D32", "#54A24B", "#7BC47F", "#A8DCA5"]
combos = []
for c in product([1, 0], repeat=3):                                  # 1 = right, 0 = wrong; RRR first
    prob = 1.0
    for r in c:
        prob *= P if r else 1 - P
    combos.append((c, prob, sum(c) >= 2))
wins = [i for i, (_, _, ok) in enumerate(combos) if ok]
assert len(wins) == 4 and round(sum(combos[i][1] for i in wins), 3) == 0.784       # section 5
FONT = dict(family="Latin Modern Roman", size=24, color="black")


def label(c):
    return "  ".join(f"M{i + 1} {'✓' if r else '✗'}" for i, r in enumerate(c))


def frame(k, title):
    """k: how many of the 'majority right' combinations have been added to the total."""
    lit = wins[:k]
    fig = make_subplots(rows=1, cols=2, column_widths=[0.68, 0.32], horizontal_spacing=0.1,
                        subplot_titles=["the 8 combinations", "P(vote right)"])
    names = [label(c) for c, _, _ in combos]
    colors = [SHADES[lit.index(i)] if i in lit else (GREY if k < 5 else "#F3B6B6" if not combos[i][2] else GREY)
              for i in range(8)]
    fig.add_trace(go.Bar(y=names, x=[p for _, p, _ in combos], orientation="h", marker_color=colors,
                         text=[f"{p:.3f}" + ("  majority right" if i in lit else "") for i, (_, p, _) in
                               enumerate(combos)], textposition="outside", cliponaxis=False, showlegend=False), 1, 1)
    total = 0.0
    for j, i in enumerate(lit):
        fig.add_trace(go.Bar(x=["vote"], y=[combos[i][1]], marker_color=SHADES[j], showlegend=False,
                             text=[f"{combos[i][1]:.3f}"], textposition="inside", insidetextanchor="middle"), 1, 2)
        total += combos[i][1]
    fig.add_trace(go.Bar(x=["one model"], y=[P], marker_color="#4C78A8", showlegend=False, text=["0.700"],
                         textposition="inside", insidetextanchor="middle"), 1, 2)
    if k:
        fig.add_annotation(x="vote", y=total, xref="x2", yref="y2", text=f"<b>{total:.3f}</b>", showarrow=False,
                           yshift=18, font=dict(size=28))
    fig.update_yaxes(autorange="reversed", row=1, col=1)
    fig.update_xaxes(range=[0, 0.52], title="probability", row=1, col=1)
    fig.update_yaxes(range=[0, 0.9], row=1, col=2)
    fig.update_xaxes(categoryorder="array", categoryarray=["one model", "vote"], row=1, col=2)
    fig.update_layout(width=1250, height=680, font=FONT, template="simple_white", barmode="stack",
                      title=dict(text=f"<b>{title}</b>", x=0.5, y=0.96, font_size=30),
                      margin=dict(l=20, r=20, t=130, b=70))
    fig.update_annotations(selector=dict(yref="paper"), font_size=26)
    return fig


if __name__ == "__main__":
    tmp = HERE / ".tree_sum"
    tmp.mkdir(exist_ok=True)
    seq = [(frame(0, "Three independent models, each right with probability 0.7"), 3),
           (frame(1, "All three right: 0.7 × 0.7 × 0.7 = 0.343"), 3),
           (frame(2, "M1, M2 right, M3 wrong: 0.7 × 0.7 × 0.3 = 0.147"), 3),
           (frame(3, "M1, M3 right, M2 wrong: another 0.147"), 3),
           (frame(4, "M2, M3 right, M1 wrong: another 0.147"), 3),
           (frame(4, "At least two right: 0.343 + 3 × 0.147 = 0.784 > 0.7"), 7)]
    keys, n = [], 0
    for j, (fig, hold) in enumerate(seq):
        png = tmp / f"{n:03d}.png"
        fig.write_image(png)
        if j in (0, 1, 2, 5):
            keys.append(Image.open(png).convert("RGB"))
        for k in range(1, hold):
            shutil.copy(png, tmp / f"{n + k:03d}.png")
        n += hold
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "1", "-i", str(tmp / "%03d.png"), "-vf",
                    "fps=5,scale=900:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "tree_sum.gif")], check=True)
    w, h = keys[0].size
    sheet = Image.new("RGB", (2 * w + 16, 2 * h + 16), "white")
    for i, f in enumerate(keys):
        sheet.paste(f, ((i % 2) * (w + 16), (i // 2) * (h + 16)))
    sheet.save(HERE / "tree_sum_frames.png")
    shutil.rmtree(tmp)

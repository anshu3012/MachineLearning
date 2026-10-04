"""Sections 5-9 on the Note's worked example: the 5 sample weights through one stage.
Start 0.2 each; model 1 misses observations 2 and 3 (the Note's assumed predictions); error 0.4; alpha 0.2027;
mistakes times e^alpha (0.2449), the rest times e^-alpha (0.1633), sum 0.9798; normalised to 0.25 and 0.1667.
Then step 7: the weights laid end to end on 0 to 1, and the Note's five random numbers (0.13, 0.43, 0.62, 0.50, 0.80)
landing as darts, which pick observations 1, 3, 3, 3 and 4.
Run: python weight_update.py  -> weight_update.gif, weight_update_frames.png (Plotly frames + ffmpeg)"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from PIL import Image

HERE = Path(__file__).parent
w0 = np.full(5, 0.2)
wrong = np.array([False, True, True, False, False])           # observations 2 and 3
err = w0[wrong].sum()
alpha = 0.5 * np.log((1 - err) / err)
w_new = np.where(wrong, w0 * np.exp(alpha), w0 * np.exp(-alpha))
w_norm = w_new / w_new.sum()
# the Note's numbers
assert round(err, 1) == 0.4 and round(alpha, 4) == 0.2027
assert np.allclose(w_new.round(4), np.where(wrong, 0.2449, 0.1633)) and round(w_new.sum(), 4) == 0.9798
assert np.allclose(w_norm.round(4), np.where(wrong, 0.25, 0.1667)) and np.isclose(w_norm[wrong].sum(), 0.5)
GREY, RED, BLUE = "#9A9A9A", "#E45756", "#54A24B"      # BLUE: correct (green)

stages = [(w0, False, "step 1: every observation weighs 1/5 = 0.2", "sum 1"),
          (w0, True, "steps 2–3: model 1 misses 2 and 3", "error = 0.2 + 0.2 = 0.4"),
          (w0, True, "step 4: say α = ½ ln(0.6 / 0.4) = 0.2027", "error = 0.4")]
for t in np.linspace(0, 1, 5)[1:]:                            # step 5: weights grow and shrink
    stages.append((w0 + t * (w_new - w0), True, "step 5: mistakes × e<sup>α</sup> = 1.2247, the rest × e<sup>−α</sup> = 0.8165",
                   f"sum {(w0 + t * (w_new - w0)).sum():.4f}"))
for t in np.linspace(0, 1, 4)[1:]:                            # step 6: normalise
    stages.append((w_new + t * (w_norm - w_new), True, "step 6: divide by the sum 0.9798",
                   f"sum {(w_new + t * (w_norm - w_new)).sum():.4f}"))
stages[-1] = (w_norm, True, "step 6: normalised; mistakes now hold half the weight", "sum 1, mistakes 0.5")


def frame(w, show_wrong, title, note):
    colours = [RED if (show_wrong and m) else (BLUE if show_wrong else GREY) for m in wrong]
    fig = go.Figure(go.Bar(x=[f"obs {i}" for i in range(1, 6)], y=w, marker_color=colours,
                           text=[f"{v:.4f}".rstrip("0").rstrip(".") if v not in (0.2,) else "0.2" for v in w],
                           textposition="outside", textfont_size=22))
    fig.add_hline(y=0.2, line=dict(color="black", dash="dot", width=1.5))
    fig.add_annotation(x=1, xref="paper", xanchor="right", y=0.31, text=note, showarrow=False, font_size=22,
                       bgcolor="white")
    if show_wrong:
        fig.add_annotation(x=0, xref="paper", xanchor="left", y=0.31, text="red: misclassified, green: correct", showarrow=False,
                           font=dict(size=20, color=RED))
    fig.update_layout(template="simple_white", width=900, height=520, font=dict(family="Latin Modern Roman", size=22),
                      title=dict(text=title, x=0.5), yaxis=dict(title="sample weight", range=[0, 0.33]),
                      margin=dict(l=70, r=20, t=70, b=50), showlegend=False)
    return fig


DARTS = [0.13, 0.43, 0.62, 0.50, 0.80]                        # the Note's random numbers
edges = np.r_[0, np.cumsum(w_norm)]
picks = [int(np.searchsorted(edges, d, side="right")) for d in DARTS]
assert picks == [1, 3, 3, 3, 4]                               # the Note's new dataset


def frame_ranges(n_darts, title):
    fig = go.Figure()
    for i in range(5):
        fig.add_shape(opacity=1, type="rect", x0=edges[i], x1=edges[i + 1], y0=0, y1=1, line=dict(color="white", width=3),
                      fillcolor=RED if wrong[i] else BLUE)
        fig.add_annotation(x=(edges[i] + edges[i + 1]) / 2, y=0.5, text=f"obs {i + 1}<br>{w_norm[i]:.3f}".replace("0.250", "0.25"),
                           showarrow=False, font=dict(size=22, color="white"))
    for e in edges:
        fig.add_annotation(x=e, y=-0.18, text=f"{e:.3f}".rstrip("0").rstrip(".") if e not in (0, 1) else f"{e:.0f}",
                           showarrow=False, font_size=19)
    for j, d in enumerate(DARTS[:n_darts]):
        top = 2.2 if d == 0.50 else 1.75                         # 0.50 sits between 0.43 and 0.62: raise it
        fig.add_annotation(x=d, y=1.02, ax=d, ay=top, axref="x", ayref="y", showarrow=True, arrowhead=2, arrowwidth=3,
                           arrowcolor="black", text="")
        fig.add_annotation(x=d, y=top + 0.18, text=f"<b>{d:.2f}</b>", showarrow=False, font_size=22)
    if n_darts:
        fig.add_annotation(x=0.5, y=-0.75, showarrow=False, font_size=24,
                           text="picked: " + ", ".join(f"obs {p}" for p in picks[:n_darts]))
    fig.update_xaxes(range=[-0.04, 1.04], visible=False)
    fig.update_yaxes(range=[-1.1, 2.7], visible=False)
    fig.update_layout(template="simple_white", width=900, height=520, font=dict(family="Latin Modern Roman", size=22),
                      title=dict(text=title, x=0.5), margin=dict(l=20, r=20, t=70, b=20), showlegend=False)
    return fig


range_stages = [(0, "step 7: lay the weights end to end on 0 to 1")]
range_stages += [(k, f"step 7: random number {DARTS[k - 1]:.2f} lands on observation {picks[k - 1]}") for k in range(1, 6)]
range_stages.append((5, "new dataset: 1, 3, 3, 3, 4; every weight starts at 0.2 again"))


if __name__ == "__main__":
    tmp = HERE / ".weight_frames"
    tmp.mkdir(exist_ok=True)
    k = 0
    figs = [(frame(*s), 4 if i < 3 or i == len(stages) - 1 or i == 6 else 1) for i, s in enumerate(stages)]   # pause on each step's result
    figs[-1] = (figs[-1][0], 8)
    figs += [(frame_ranges(*s), 4) for s in range_stages]
    figs[-1] = (figs[-1][0], 10)
    for i, (fig, hold) in enumerate(figs):
        img = tmp / f"s{i:02d}.png"
        fig.write_image(img)
        for _ in range(hold):
            shutil.copy(img, tmp / f"{k:03d}.png")
            k += 1
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "3", "-i", str(tmp / "%03d.png"), "-vf",
                    "fps=6,scale=760:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "weight_update.gif")], check=True)
    keys = [Image.open(tmp / f"s{i:02d}.png").convert("RGB") for i in (1, 6, len(stages) - 1, len(stages), len(stages) + 3, len(figs) - 1)]
    w, h = keys[0].size
    sheet = Image.new("RGB", (2 * w + 16, 3 * h + 32), "white")
    for i, im in enumerate(keys):
        sheet.paste(im, ((i % 2) * (w + 16), (i // 2) * (h + 16)))
    sheet.save(HERE / "weight_update_frames.png")
    shutil.rmtree(tmp)

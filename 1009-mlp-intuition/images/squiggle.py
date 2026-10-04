"""A curve built from two hidden nodes, with one input. Data: a drug that works only at a medium dose (nine toy
patients, the 0-1-0 pattern of Note 1007). Network: 1 input, 2 sigmoid hidden nodes, 1 sigmoid output, trained with
scikit-learn's MLPClassifier (lbfgs). 12 of 20 random starts reach 9 of 9; the figure uses the first that does
(random_state=2). Frames: the data, each hidden node's curve, the two curves times their output weights, their sum
plus the bias, and the sigmoid of that sum. Idea after StatQuest, "The Essential Main Ideas of Neural Networks".
Plotly frames (curves changing) -> ffmpeg GIF, plus a grid of key frames for the PDF."""
import shutil
import subprocess
import warnings
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from PIL import Image
from sklearn.neural_network import MLPClassifier

warnings.filterwarnings("ignore")
HERE = Path(__file__).parent
FONT = dict(family="Latin Modern Roman", size=22)
GREEN, RED, BLUE, ORANGE, PURPLE = "#54A24B", "#E45756", "#4C78A8", "#F58518", "#B279A2"
DOSE = np.array([0.05, 0.10, 0.15, 0.45, 0.50, 0.55, 0.85, 0.90, 0.95])
WORKS = np.array([0, 0, 0, 1, 1, 1, 0, 0, 0])
sig = lambda z: 1 / (1 + np.exp(-z))


def fit(seed):
    return MLPClassifier(hidden_layer_sizes=(2,), activation="logistic", solver="lbfgs", alpha=1e-3, max_iter=5000,
                         random_state=seed).fit(DOSE.reshape(-1, 1), WORKS)


solved = [s for s in range(20) if fit(s).score(DOSE.reshape(-1, 1), WORKS) == 1]
assert len(solved) == 12 and solved[0] == 2, solved
M = fit(solved[0])
(W1, W2), (B1, B2) = M.coefs_[0][0], M.intercepts_[0]
(V1, V2), C = M.coefs_[1].ravel(), M.intercepts_[1][0]
print("hidden:", round(W1, 2), round(B1, 2), "|", round(W2, 2), round(B2, 2), "| output:", round(V1, 2), round(V2, 2),
      round(C, 2))
assert [round(v, 1) for v in (W1, B1, W2, B2, V1, V2, C)] == [11.6, -8.5, -11.6, 3.2, -13.3, -13.3, 6.3]
x = np.linspace(0, 1, 201)
H1, H2 = sig(W1 * x + B1), sig(W2 * x + B2)
Z = V1 * H1 + V2 * H2 + C
for d in (0.1, 0.5, 0.9):
    h1, h2 = sig(W1 * d + B1), sig(W2 * d + B2)
    print(f"dose {d}: h1 {h1:.3f} h2 {h2:.3f} z {V1 * h1 + V2 * h2 + C:.2f} out {sig(V1 * h1 + V2 * h2 + C):.3f}")

f = lambda v: f"{v:.1f}".replace("-", "−")
STEPS = [
    ("The data: the drug works only at a medium dose", [], (-0.2, 1.25), True),
    (f"Hidden node 1: h₁ = σ({f(W1)}·dose {f(B1)}) switches on at high doses", [(H1, BLUE, "h₁")], (-0.2, 1.25), True),
    (f"Hidden node 2: h₂ = σ({f(W2)}·dose + {f(B2)}) switches on at low doses",
     [(H1, BLUE, "h₁"), (H2, ORANGE, "h₂")], (-0.2, 1.25), True),
    (f"The output node multiplies each curve by its weight: {f(V1)}·h₁ and {f(V2)}·h₂",
     [(V1 * H1, BLUE, f"{f(V1)}·h₁"), (V2 * H2, ORANGE, f"{f(V2)}·h₂")], (-15, 8), False),
    (f"It adds them and the bias {f(C)}: z is positive only at medium doses",
     [(V1 * H1, BLUE, f"{f(V1)}·h₁"), (V2 * H2, ORANGE, f"{f(V2)}·h₂"), (Z, PURPLE, "z = sum + bias")], (-15, 8), False),
    ("The sigmoid turns z into the output σ(z): a curve that rises and falls",
     [(sig(Z), GREEN, "output σ(z)")], (-0.2, 1.25), True),
]


def frame(k):
    title, curves, yr, data = STEPS[k]
    fig = go.Figure()
    if not data:
        fig.add_hline(y=0, line=dict(color="grey", dash="dot", width=2))
    for yv, col, name in curves:
        fig.add_scatter(x=x, y=yv, mode="lines", line=dict(color=col, width=5), name=name)
    if data:
        for lab, col, name in ((1, GREEN, "works (1)"), (0, RED, "does not work (0)")):
            m = WORKS == lab
            fig.add_scatter(x=DOSE[m], y=WORKS[m], mode="markers", name=name,
                            marker=dict(size=17, color=col, line=dict(color="white", width=1.5)))
    fig.update_layout(template="simple_white", width=1000, height=700, font=FONT,
                      title=dict(text=f"<b>Step {k + 1} of {len(STEPS)}.</b> {title}", x=0.5, y=0.95,
                                 font=dict(size=21)),
                      xaxis=dict(title="dose", tickvals=[0.1, 0.5, 0.9], ticktext=["low", "medium", "high"],
                                 range=[-0.02, 1.02]),
                      yaxis=dict(title="value", range=list(yr)),
                      legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.18),
                      margin=dict(l=90, r=30, t=90, b=130))
    return fig


if __name__ == "__main__":
    tmp = HERE / ".sq_frames"
    tmp.mkdir(exist_ok=True)
    keys, n = [], 0
    for k in range(len(STEPS)):
        keys.append(tmp / f"k{k}.png")
        frame(k).write_image(keys[-1])
        for _ in range(3 if k < len(STEPS) - 1 else 6):
            shutil.copy(keys[-1], tmp / f"{n:03d}.png")
            n += 1
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "1", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=760:-1:flags=lanczos,split[a][b];[a]palettegen=max_colors=64[p];[b][p]paletteuse",
                    str(HERE / "squiggle.gif")], check=True)
    ims = [Image.open(keys[i]).convert("RGB") for i in (2, 4, 5)]
    w, h = ims[0].size
    sheet = Image.new("RGB", (3 * w + 32, h), "white")
    for i, im in enumerate(ims):
        sheet.paste(im, (i * (w + 16), 0))
    sheet.save(HERE / "squiggle_frames.png")
    shutil.rmtree(tmp)

"""Gaussian Naive Bayes on the 8 people, read off the fitted normal curves (Plotly frames + ffmpeg).
density_read.gif (section 4): the new person's height (185 cm) and weight (170 lb) are marked on the class
  curves; the curve heights there are the likelihoods; prior x both heights gives the two scores.
height_sweep.gif (section 6): the weight stays at 170 lb while the height slides from 150 to 190 cm;
  P(male | height, weight) is traced out and crosses 50 percent at the decision boundary.
Idea for density_read after StatQuest, "Gaussian Naive Bayes, Clearly Explained!!!" (the likelihood is the
y-axis value of the curve); data and code are ours.
Run: python nb_curves.py -> density_read.gif, height_sweep.gif and their _frames.png"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from PIL import Image
from plotly.subplots import make_subplots

HERE = Path(__file__).parent
df = pd.read_csv(HERE.parent / "data" / "people.csv")
Q = {"height_cm": 185, "weight_lb": 170}
NAME = {"height_cm": "height (cm)", "weight_lb": "weight (lb)"}
RANGE = {"height_cm": (140, 205), "weight_lb": (60, 220)}
COL = {"male": "#4C78A8", "female": "#E45756"}
FONT = dict(family="Latin Modern Roman", size=24, color="black")


def pdf(x, mu, sd):
    return np.exp(-0.5 * ((x - mu) / sd) ** 2) / (sd * np.sqrt(2 * np.pi))


par = {(g, c): (df[df.gender == g][c].mean(), df[df.gender == g][c].std()) for g in COL for c in Q}
dens = {(g, c): pdf(Q[c], *par[g, c]) for g in COL for c in Q}
score = {g: 0.5 * dens[g, "height_cm"] * dens[g, "weight_lb"] for g in COL}
assert round(dens["male", "height_cm"], 5) == 0.03615 and round(dens["female", "weight_lb"], 5) == 0.00479
assert round(score["male"] * 1e4, 1) == 5.5 and round(score["female"] * 1e5, 1) == 1.1       # the Note's table
print({k: round(v, 5) for k, v in dens.items()},
      {c: round(dens["male", c] / dens["female", c], 1) for c in Q},
      {g: round(np.log(score[g]), 2) for g in COL}, np.log(0.5),
      {k: round(np.log(v), 3) for k, v in dens.items()})


def p_male(h, w=170):
    s = {g: 0.5 * pdf(h, *par[g, "height_cm"]) * pdf(w, *par[g, "weight_lb"]) for g in COL}
    return s["male"] / (s["male"] + s["female"])


def curves(fig, c, col, legend=False):
    xs = np.linspace(*RANGE[c], 300)
    for g in COL:
        fig.add_trace(go.Scatter(x=xs, y=pdf(xs, *par[g, c]), mode="lines", line=dict(color=COL[g], width=4),
                                 name=g, showlegend=legend), 1, col)
    fig.update_xaxes(title=NAME[c], range=RANGE[c], row=1, col=col)


def read_frame(k, title, foot=""):
    """k: 0 curves only, 1 height read off, 2 weight read off too."""
    fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.1)
    for j, c in enumerate(Q):
        curves(fig, c, j + 1, legend=(j == 0))
        if k > j:
            fig.add_vline(x=Q[c], line=dict(color="black", dash="dash", width=2), row=1, col=j + 1)
            for g in COL:
                fig.add_trace(go.Scatter(x=[Q[c]], y=[dens[g, c]], mode="markers+text", showlegend=False,
                                         marker=dict(size=18, color=COL[g], line=dict(color="black", width=2)),
                                         text=[f"<b>{dens[g, c]:.4f}</b>"], textposition="middle left",
                                         textfont=dict(color=COL[g], size=26)), 1, j + 1)
            ratio = dens["male", c] / dens["female", c]
            fig.add_annotation(xref=f"x{j + 1 if j else ''} domain", yref="paper", x=0.5, y=1.1, showarrow=False,
                               text=f"at {Q[c]}: male curve {ratio:.1f}× higher", font=dict(size=24))
    if foot:
        fig.add_annotation(xref="paper", yref="paper", x=0.5, y=-0.3, yanchor="top", showarrow=False, text=foot, font=dict(size=26))
    fig.update_yaxes(title="density", range=[0, 0.075], row=1, col=1)
    fig.update_yaxes(range=[0, 0.04], row=1, col=2)
    fig.update_layout(width=1250, height=700, font=FONT, template="simple_white",
                      legend=dict(x=0.01, y=0.99, font_size=24),
                      title=dict(text=f"<b>{title}</b>", x=0.5, y=0.97, font_size=30),
                      margin=dict(l=90, r=20, t=130, b=210))
    return fig


HS = np.linspace(150, 190, 21)
PM = np.array([p_male(h) for h in HS])
fine = np.linspace(150, 190, 4001)
BOUNDARY = fine[np.argmin(np.abs(np.array([p_male(h) for h in fine]) - 0.5))]
print("decision boundary height at weight 170:", round(BOUNDARY, 1), "P(male) at 185:", round(p_male(185), 3))


def sweep_frame(i):
    h = HS[i]
    fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.12,
                        subplot_titles=["height curves", "P(male | height, weight = 170)"])
    curves(fig, "height_cm", 1, legend=True)
    fig.add_vline(x=h, line=dict(color="black", dash="dash", width=2), row=1, col=1)
    for g in COL:
        fig.add_trace(go.Scatter(x=[h], y=[pdf(h, *par[g, "height_cm"])], mode="markers", showlegend=False,
                                 marker=dict(size=16, color=COL[g], line=dict(color="black", width=2))), 1, 1)
    fig.add_trace(go.Scatter(x=HS[:i + 1], y=PM[:i + 1], mode="lines", line=dict(color="black", width=4),
                             showlegend=False), 1, 2)
    win = "male" if PM[i] > 0.5 else "female"
    fig.add_trace(go.Scatter(x=[h], y=[PM[i]], mode="markers", showlegend=False,
                             marker=dict(size=20, color=COL[win], line=dict(color="black", width=2))), 1, 2)
    fig.add_hline(y=0.5, line=dict(color="#888888", dash="dot"), row=1, col=2)
    if h >= BOUNDARY:
        fig.add_trace(go.Scatter(x=[BOUNDARY, BOUNDARY], y=[0, 0.5], mode="lines", showlegend=False,
                                 line=dict(color="#888888", dash="dot", width=3)), 1, 2)
        fig.add_annotation(x=BOUNDARY, y=0.12, xref="x2", yref="y2", text=f"decision boundary<br>{BOUNDARY:.0f} cm",
                           showarrow=False, xanchor="left", xshift=8, font=dict(size=22))
    fig.update_yaxes(title="density", range=[0, 0.075], row=1, col=1)
    fig.update_yaxes(title="probability of male", range=[0, 1.05], row=1, col=2)
    fig.update_xaxes(title="height (cm)", range=[148, 192], row=1, col=2)
    fig.update_layout(width=1250, height=620, font=FONT, template="simple_white",
                      legend=dict(x=0.01, y=0.99, font_size=22),
                      title=dict(text=f"<b>height {h:.0f} cm, weight 170 lb: {PM[i]:.0%} male → predict {win}</b>",
                                 x=0.5, y=0.96, font_size=30), margin=dict(l=90, r=20, t=120, b=80))
    fig.update_annotations(selector=dict(yref="paper"), font_size=26)
    return fig


def save(name, seq, rate, keys_at):
    tmp = HERE / f".{name}"
    tmp.mkdir(exist_ok=True)
    keys, n = [], 0
    for i, (fig, hold) in enumerate(seq):
        png = tmp / f"{n:03d}.png"
        fig.write_image(png)
        if i in keys_at:
            keys.append(Image.open(png).convert("RGB"))
        for k in range(1, hold):
            shutil.copy(png, tmp / f"{n + k:03d}.png")
        n += hold
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(rate), "-i", str(tmp / "%03d.png"),
                    "-vf", "fps=6,scale=900:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / f"{name}.gif")], check=True)
    w, h = keys[0].size
    rows = -(-len(keys) // 2)
    sheet = Image.new("RGB", (2 * w + 16, rows * h + 16 * (rows - 1)), "white")
    for i, f in enumerate(keys):
        sheet.paste(f, ((i % 2) * (w + 16), (i // 2) * (h + 16)))
    sheet.save(HERE / f"{name}_frames.png")
    shutil.rmtree(tmp)


if __name__ == "__main__":
    m, f = score["male"], score["female"]
    save("density_read", [
        (read_frame(0, "1. One normal curve per class, for each feature"), 3),
        (read_frame(1, "2. Height 185 cm: read the height of each curve"), 4),
        (read_frame(2, "3. Weight 170 lb: read the height of each curve"), 4),
        (read_frame(2, "4. Score = prior × the two curve heights",
                    f"<span style='color:{COL['male']}'>male: 0.5 × 0.0361 × 0.0307 = {m * 1e4:.1f} × 10⁻⁴</span>"
                    f"<br><span style='color:{COL['female']}'>female: 0.5 × 0.0047 × 0.0048 = {f * 1e5:.1f} × 10⁻⁵"
                    f"</span><br><b>male is {m / f:.0f}× larger: predict male</b>"), 7)], 1, {0, 1, 2, 3})
    seq = [(sweep_frame(i), 1) for i in range(len(HS))]
    seq[-1] = (seq[-1][0], 12)
    save("height_sweep", seq, 5, {3, 8, 12, 20})

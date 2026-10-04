"""Hard vs soft voting, one test point at a time, on the concentric-circles data with logistic regression,
Gaussian naive Bayes and random forest (app.load split and app.base_models, as in hard_soft_surfaces.py).
For three test points where the two votes disagree: the point, each model's probability of class 1 and its vote,
the hard result, then the soft average and result. Last: every disagreement point in the test set, ringed.
Run: python vote_tally.py  -> vote_tally.gif, vote_tally_frames.png (Plotly frames + ffmpeg)"""
import shutil
import subprocess
import sys
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from PIL import Image

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent))
from app import COLOURS, base_models, load  # noqa: E402

X_tr, X_te, y_tr, y_te = load("concentric circles")
names = ["logistic regression", "Gaussian naive Bayes", "random forest"]
short = ["logistic", "naive Bayes", "forest"]
models = [m.fit(X_tr, y_tr) for _, m in base_models(names)]
P = np.array([m.predict_proba(X_te)[:, 1] for m in models])     # P(class 1), one row per model
votes = (P > 0.5).astype(int)
hard = (votes.sum(0) >= 2).astype(int)
soft = (P.mean(0) > 0.5).astype(int)
dis = np.flatnonzero(hard != soft)
soft_right = int((soft[dis] == y_te[dis]).sum())
print(len(dis), "disagreements, soft right on", soft_right)
assert len(dis) == 30 and soft_right == 28                       # the Note's numbers (section 3.4 Extra)
show = dis[:3]


def frame(i, step):
    """step 0: the point; 1: model probabilities and hard vote; 2: soft average. i = None: the summary frame."""
    fig = make_subplots(rows=1, cols=2, column_widths=[0.45, 0.55], horizontal_spacing=0.1,
                        subplot_titles=(" ", " "))
    for cls in (0, 1):
        m = y_te == cls
        fig.add_trace(go.Scatter(x=X_te[m, 0], y=X_te[m, 1], mode="markers", name=f"class {cls}",
                                 marker=dict(color=COLOURS[cls], size=9, line=dict(color="white", width=0.5))), 1, 1)
    if i is None:
        fig.add_trace(go.Scatter(x=X_te[dis, 0], y=X_te[dis, 1], mode="markers", showlegend=False,
                                 marker=dict(size=18, color="rgba(0,0,0,0)", line=dict(color="black", width=2))), 1, 1)
        fig.layout.annotations[0].text = f"hard and soft disagree on {len(dis)} of {len(y_te)}"
        fig.add_annotation(x=0.78, y=0.5, xref="paper", yref="paper", showarrow=False, font=dict(size=30),
                           text=f"soft vote right<br>on {soft_right} of {len(dis)}")
        fig.update_xaxes(visible=False, row=1, col=2)
        fig.update_yaxes(visible=False, row=1, col=2)
    else:
        q = show[i]
        fig.add_trace(go.Scatter(x=[X_te[q, 0]], y=[X_te[q, 1]], mode="markers", showlegend=False,
                                 marker=dict(symbol="star", size=30, color=COLOURS[y_te[q]],
                                             line=dict(color="black", width=2))), 1, 1)
        fig.layout.annotations[0].text = f"test point {i + 1} of 3: true class {y_te[q]}"
        if step >= 1:
            p = P[:, q]
            fig.add_trace(go.Bar(x=short, y=p, marker_color=[COLOURS[v] for v in votes[:, q]], showlegend=False,
                                 text=[f"{v:.2f}" for v in p], textposition="outside"), 1, 2)
            v1 = votes[:, q].sum()
            title = f"hard: {v1} vote{'' if v1 == 1 else 's'} for 1, {3 - v1} for 0 → class {hard[q]}"
            if step >= 2:
                fig.add_trace(go.Bar(x=["average"], y=[p.mean()], marker_color=COLOURS[soft[q]], showlegend=False,
                                     marker_line=dict(color="black", width=3),
                                     text=[f"{p.mean():.2f}"], textposition="outside"), 1, 2)
                title += f"<br>soft: average {p.mean():.2f} → class {soft[q]}"
            fig.layout.annotations[1].text = title
        fig.add_hline(y=0.5, line=dict(color="black", dash="dash", width=2), row=1, col=2)
        fig.update_xaxes(categoryorder="array", categoryarray=short + ["average"], row=1, col=2)
        fig.update_yaxes(range=[0, 1.15], title="probability of class 1", row=1, col=2)
    fig.update_xaxes(showticklabels=False, row=1, col=1)
    fig.update_yaxes(showticklabels=False, scaleanchor="x", row=1, col=1)
    fig.update_layout(template="simple_white", width=1150, height=600, font=dict(family="Latin Modern Roman", size=22),
                      margin=dict(l=20, r=20, t=110, b=50), legend=dict(x=0.0, y=-0.02, orientation="h"))
    fig.update_annotations(font_size=24)
    return fig


if __name__ == "__main__":
    tmp = HERE / ".tally_frames"
    tmp.mkdir(exist_ok=True)
    plan = [(i, s, hold) for i in range(3) for s, hold in ((0, 3), (1, 6), (2, 8))] + [(None, 0, 14)]
    j = 0
    for i, s, hold in plan:
        frame(i, s).write_image(tmp / "f.png")
        for _ in range(hold):                                   # 2 frames a second: hold each step
            shutil.copy(tmp / "f.png", tmp / f"{j:03d}.png")
            j += 1
        if (i, s) in ((0, 1), (0, 2), (1, 2)) or i is None:
            shutil.copy(tmp / "f.png", tmp / f"key_{i}_{s}.png")
    (tmp / "f.png").unlink()
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "2", "-i", str(tmp / "%03d.png"), "-vf",
                    "fps=6,scale=880:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "vote_tally.gif")], check=True)
    keys = [Image.open(tmp / f"key_{k}.png").convert("RGB") for k in ("0_1", "0_2", "1_2", "None_0")]
    w, h = keys[0].size
    sheet = Image.new("RGB", (2 * w + 16, 2 * h + 16), "white")
    for n, im in enumerate(keys):
        sheet.paste(im, ((n % 2) * (w + 16), (n // 2) * (h + 16)))
    sheet.save(HERE / "vote_tally_frames.png")
    shutil.rmtree(tmp)

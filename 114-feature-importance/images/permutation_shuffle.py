"""Section 7: permutation importance as a process, on the forest of mdi_vs_permutation.py (section 6 data).
One feature at a time is shuffled in the 300 test observations, 20 times (permutation_importance, n_repeats=20,
random_state=0). Each dot is the test accuracy after one shuffle; the gap to the unshuffled 0.870 is the drop.
Run: python permutation_shuffle.py  -> permutation_shuffle.gif, permutation_shuffle_frames.png (Plotly frames + ffmpeg)"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from sklearn.datasets import make_classification
from sklearn.ensemble import RandomForestClassifier
from sklearn.inspection import permutation_importance
from sklearn.model_selection import train_test_split

HERE = Path(__file__).parent
X, y = make_classification(n_samples=1000, n_features=4, n_informative=3, n_redundant=1, flip_y=0.1, random_state=0)
df = pd.DataFrame(X.round(1), columns=["x1", "x2", "x3", "x4"])
rng = np.random.default_rng(0)
df["random_id"] = rng.permutation(len(df))
df["random_coin"] = rng.integers(0, 2, len(df))
X_train, X_test, y_train, y_test = train_test_split(df, y, test_size=0.3, random_state=0)
rf = RandomForestClassifier(random_state=0, n_jobs=-1).fit(X_train, y_train)
base = rf.score(X_test, y_test)
perm = permutation_importance(rf, X_test, y_test, n_repeats=20, random_state=0, n_jobs=-1)
acc = base - perm.importances                                 # accuracy after each shuffle, (6 features, 20)
cols = list(df.columns)
mean_drop = dict(zip(cols, perm.importances_mean))
assert round(base, 3) == 0.870
assert round(mean_drop["random_id"], 3) == -0.003 and round(mean_drop["random_coin"], 3) == 0.004
print({k: round(v, 3) for k, v in mean_drop.items()})
STEP = 5                                                      # shuffles added per frame
frames = [(j, n) for j in range(len(cols)) for n in range(STEP, 21, STEP)]


def frame(j_now, n_now):
    fig = go.Figure()
    fig.add_vline(x=base, line=dict(color="black", dash="dash", width=2))
    fig.add_annotation(x=base, y=len(cols) - 0.35, text=f"no shuffle: {base:.3f}", showarrow=False, xanchor="right",
                       font_size=20)
    for j, name in enumerate(cols):
        if j > j_now:
            break
        n = 20 if j < j_now else n_now
        row = len(cols) - 1 - j
        c = "#E45756" if name.startswith("random") else "#4C78A8"
        fig.add_trace(go.Scatter(x=acc[j, :n], y=np.full(n, row) + np.linspace(-0.2, 0.2, 20)[:n], mode="markers",
                                 marker=dict(color=c, size=10, opacity=0.8), showlegend=False))
        if n == 20:
            fig.add_annotation(x=0.892, y=row, text=f"drop {mean_drop[name]:+.3f}", showarrow=False,
                               xanchor="left", font_size=19)
    name = cols[j_now]
    fig.update_layout(template="simple_white", width=1000, height=600, font=dict(family="Latin Modern Roman", size=21),
                      title=dict(text=f"shuffling {name} in the test set: {n_now} of 20 shuffles", x=0.5),
                      margin=dict(l=20, r=20, t=60, b=70),
                      xaxis=dict(title="test accuracy after the shuffle", range=[0.6, 0.99], dtick=0.05),
                      yaxis=dict(tickvals=list(range(len(cols))), ticktext=cols[::-1], range=[-0.6, len(cols) - 0.2]))
    return fig


if __name__ == "__main__":
    tmp = HERE / ".perm_frames"
    tmp.mkdir(exist_ok=True)
    for k, (j, n) in enumerate(frames):
        frame(j, n).write_image(tmp / f"{k:03d}.png")
    last = len(frames) - 1
    for k in range(last + 1, last + 8):                       # hold the last frame
        shutil.copy(tmp / f"{last:03d}.png", tmp / f"{k:03d}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "3", "-i", str(tmp / "%03d.png"), "-vf",
                    "fps=6,scale=800:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "permutation_shuffle.gif")], check=True)
    shutil.copy(tmp / f"{last:03d}.png", HERE / "permutation_shuffle_frames.png")   # PDF: the final frame
    shutil.rmtree(tmp)

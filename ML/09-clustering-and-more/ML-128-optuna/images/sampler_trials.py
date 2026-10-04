"""Where three samplers put their trials, animated (Plotly frames). The grid, random and TPE studies the Notebook saved in
data/optuna.db (random forest on the diabetes data), drawn on the n_estimators x max_depth plane, one trial per frame.
The green box is the best region named in the Note (max_depth 6 to 10, n_estimators up to 120); a counter shows how
many trials each sampler has placed in it: 2 of 16 (grid), 7 of 50 (random), 10 of 50 (TPE).
Run: python sampler_trials.py  -> sampler_trials.gif, sampler_trials_frames.png"""
import shutil
import subprocess
from pathlib import Path

import optuna
import plotly.graph_objects as go
from PIL import Image
from plotly.subplots import make_subplots

HERE = Path(__file__).parent
STORAGE = f"sqlite:///{HERE.parent / 'data' / 'optuna.db'}"
optuna.logging.set_verbosity(optuna.logging.WARNING)
NAMES = [("grid", "grid search"), ("random", "random search"), ("tpe", "TPE (Bayesian)")]
trials = {}
for key, _ in NAMES:
    st = optuna.load_study(study_name=key, storage=STORAGE)
    trials[key] = [(t.params["n_estimators"], t.params["max_depth"], t.value) for t in st.trials]


def inside(t):
    return 6 <= t[1] <= 10 and t[0] <= 120


assert [sum(map(inside, trials[k])) for k, _ in NAMES] == [2, 7, 10]      # the counts quoted in the Note
LO = min(t[2] for ts in trials.values() for t in ts)
HI = max(t[2] for ts in trials.values() for t in ts)


def frame(n):
    fig = make_subplots(1, 3, horizontal_spacing=0.06, shared_yaxes=True, subplot_titles=[
        f"{label}<br>{min(n, len(trials[k]))} trials, {sum(map(inside, trials[k][:n]))} in the green box"
        for k, label in NAMES])
    for c, (k, _) in enumerate(NAMES, start=1):
        ts = trials[k][:n]
        fig.add_shape(type="rect", x0=45, x1=120, y0=5.5, y1=10.5, fillcolor="#54A24B", opacity=0.18,
                      line=dict(color="#54A24B", width=2), row=1, col=c)
        fig.add_trace(go.Scatter(x=[t[0] for t in ts], y=[t[1] for t in ts], mode="markers", showlegend=False,
                                 marker=dict(size=15, color=[t[2] for t in ts], colorscale="Blues", cmin=LO, cmax=HI,
                                             line=dict(color="black", width=1), showscale=c == 3,
                                             colorbar=dict(title="CV accuracy", tickformat=".3f", len=0.8))), 1, c)
        if ts and n <= len(trials[k]):                    # ring around the newest trial
            fig.add_trace(go.Scatter(x=[ts[-1][0]], y=[ts[-1][1]], mode="markers", showlegend=False,
                                     marker=dict(size=26, color="rgba(0,0,0,0)", line=dict(color="#E45756", width=3))),
                          1, c)
        fig.update_xaxes(title_text="n_estimators", range=[40, 210], row=1, col=c)
    fig.update_yaxes(range=[2, 21])
    fig.update_yaxes(title_text="max_depth", row=1, col=1)
    fig.update_annotations(font_size=22)
    fig.update_layout(template="simple_white", width=1500, height=620, font=dict(family="Latin Modern Roman", size=19),
                      margin=dict(l=70, r=20, t=100, b=70))
    return fig


if __name__ == "__main__":
    tmp = HERE / ".sampler_trials_frames"
    tmp.mkdir(exist_ok=True)
    n, keys = 0, []
    for t in range(1, 51):
        rep = 8 if t == 50 else 1
        frame(t).write_image(tmp / f"{n:03d}.png")
        if t in (10, 50):
            keys.append(Image.open(tmp / f"{n:03d}.png").convert("RGB"))
        for j in range(1, rep):
            shutil.copy(tmp / f"{n:03d}.png", tmp / f"{n + j:03d}.png")
        n += rep
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "4", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=900:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "sampler_trials.gif")], check=True)
    w, h = keys[0].size
    grid = Image.new("RGB", (w, 2 * h), "white")
    for i, im in enumerate(keys):
        grid.paste(im, (0, i * h))
    grid.save(HERE / "sampler_trials_frames.png")
    shutil.rmtree(tmp)

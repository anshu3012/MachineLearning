"""AdaGrad and RMSProp (beta 0.9), both with learning rate 0.2, on the sparse-feature loss from (m, b) = (-4, -4).
AdaGrad's steps shrink until it crawls; RMSProp keeps its step size and reaches the minimum.
Run: python rmsprop_race.py -> rmsprop_race.gif, rmsprop_race_frames.png (Plotly frames + ffmpeg)"""
import shutil
import subprocess
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from PIL import Image
from surf import beside, data_quad, quad_surface, BOWL_LEVELS
from common import GREEN, PURPLE, RED, FONT
from shared import X, y, BEST, loss, run, steps_to

HERE = Path(__file__).parent
SHOW = 80
paths = {"RMSProp, β = 0.9": (run("rmsprop")[0], PURPLE), "AdaGrad": (run("adagrad")[0], GREEN)}  # AdaGrad drawn on top
done = {k: steps_to(P) for k, (P, _) in paths.items()}
m, b = np.linspace(-5, 9, 200), np.linspace(-5, 9, 200)
M, B = np.meshgrid(m, b)
Z = np.log10(((y[None, None, :] - M[..., None] * X[:, 0] - B[..., None]) ** 2).mean(-1))
ZMAX = 80                                                   # the walls go higher than drawn
_p, _H, _l = data_quad(X, y)
TRACES = quad_surface(np.linspace(-5, 9, 90), np.linspace(-5, 9, 90), _p, _H, _l, BOWL_LEVELS, ZMAX, -0.6, 2.4)
height = lambda P: np.array([loss(p) for p in P])


def frame(k):
    fig = go.Figure(go.Contour(x=m, y=b, z=Z, colorscale="Greys", reversescale=True, showscale=False,
                               contours=dict(start=-0.6, end=2.4, size=0.2), line=dict(width=0.6), opacity=0.5))
    for name, (P, c) in paths.items():
        Q = P[:k + 1]
        if done[name] is not None and k >= done[name]:
            label = f"{name}: done in {done[name]} steps"
        else:
            label = f"{name}: step {k}"
        fig.add_trace(go.Scatter(x=Q[:, 0], y=Q[:, 1], mode="lines+markers", name=label,
                                 line=dict(color=c, width=5 if name == "AdaGrad" else 3), marker=dict(size=7, color=c)))
    fig.add_trace(go.Scatter(x=[BEST[0]], y=[BEST[1]], mode="markers", showlegend=False,
                             marker=dict(symbol="star", size=18, color=RED)))
    fig.update_layout(template="simple_white", width=820, height=800, font=dict(FONT, size=20),
                      title=dict(text=f"step {k}  (learning rate 0.2 for both)", x=0.5, y=0.98),
                      xaxis=dict(title="m (weight of IIT)", range=[-5, 9]),
                      yaxis=dict(title="b (bias)", range=[-5, 9]), margin=dict(l=70, r=20, t=140, b=55),
                      legend=dict(x=0, y=1.02, yanchor="bottom"))
    beside(fig, TRACES, [(P[:k + 1], height(P[:k + 1]), c, 5) for P, c in paths.values()], (BEST[0], BEST[1], loss(BEST)), ("m", "b"), (1.0, 1.0, 1.0), ZMAX, xr=[-5, 9], yr=[-5, 9])
    return fig


if __name__ == "__main__":
    print(done)
    tmp = HERE / ".race_frames"
    tmp.mkdir(exist_ok=True)
    for k in range(SHOW + 1):
        frame(k).write_image(tmp / f"{k:03d}.png")
    for k in range(SHOW + 1, SHOW + 9):
        shutil.copy(tmp / f"{SHOW:03d}.png", tmp / f"{k:03d}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "8", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=970:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "rmsprop_race.gif")], check=True)
    keys = [Image.open(tmp / f"{k:03d}.png").convert("RGB") for k in (5, 20, 45, SHOW)]
    w, h = keys[0].size
    sheet = Image.new("RGB", (2 * w + 16, 2 * h + 16), "white")
    for i, im in enumerate(keys):
        sheet.paste(im, ((i % 2) * (w + 16), (i // 2) * (h + 16)))
    sheet.save(HERE / "rmsprop_race_frames.png")
    shutil.rmtree(tmp)

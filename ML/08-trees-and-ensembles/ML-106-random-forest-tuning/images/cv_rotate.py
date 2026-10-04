"""Section 4: cross-validation as rotating blocks, on the heart data with the default random forest.
First 4 blocks (train on 3, test on 1, rotate), then the 10 folds the Note uses (mean 0.832, as cross_val_score gives).
Run: python cv_rotate.py  -> cv_rotate.gif, cv_rotate_frames.png (Plotly frames + ffmpeg)"""
import shutil
import subprocess
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
from PIL import Image
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score

HERE = Path(__file__).parent
BLUE, ORANGE = "#4C78A8", "#F58518"
df = pd.read_csv(HERE.parent / "data" / "heart.csv")
X, y = df.iloc[:, :-1], df.iloc[:, -1]
scores = {k: cross_val_score(RandomForestClassifier(random_state=42), X, y, cv=k) for k in (4, 10)}
assert round(scores[10].mean(), 3) == 0.832                      # the Note's 10-fold score
print({k: (v.round(3), v.mean().round(3)) for k, v in scores.items()})


def frame(k, done, final):
    """k blocks; rounds 1..done are drawn; final adds the mean."""
    s = scores[k]
    fig = go.Figure()
    h = 0.62
    for r in range(done):
        yy = k - r
        for b in range(k):
            test = b == k - 1 - r                                 # the test block moves from the last block to the first
            new = r == done - 1 and not final
            fig.add_shape(type="rect", x0=b / k * 100 + 0.4, x1=(b + 1) / k * 100 - 0.4, y0=yy - h / 2, y1=yy + h / 2,
                          line=dict(color="black" if (test and new) else "white", width=2.5),
                          fillcolor=ORANGE if test else BLUE, opacity=1 if (new or final) else 0.55)
        fig.add_annotation(x=-2, y=yy, text=f"round {r + 1}", showarrow=False, xanchor="right", font_size=20)
        fig.add_annotation(x=103, y=yy, text=f"{s[k - 1 - r]:.2f}", showarrow=False, xanchor="left",
                           font=dict(size=22, color=ORANGE))
    fig.add_annotation(x=50, y=k + 0.95, showarrow=False, font_size=20,
                       text=f"<span style='color:{BLUE}'>■</span> train    <span style='color:{ORANGE}'>■</span> test: accuracy on the right")
    if final:
        fig.add_annotation(x=50, y=0.15, text=f"every block tested once: mean accuracy <b>{s.mean():.3f}</b>", showarrow=False,
                           font_size=24)
    fig.update_xaxes(range=[-17, 114], visible=False)
    fig.update_yaxes(range=[-0.3, k + 1.4], visible=False)
    fig.update_layout(template="simple_white", width=1000, height=600, font=dict(family="Latin Modern Roman", size=22),
                      margin=dict(l=5, r=5, t=70, b=5), showlegend=False,
                      title=dict(text=f"{k}-fold cross-validation: the 303 patients in {k} blocks", x=0.5, font_size=24))
    return fig


stages = [(k, d, False) for k in (4, 10) for d in range(1, k + 1)]
stages = stages[:4] + [(4, 4, True)] + stages[4:] + [(10, 10, True)]

if __name__ == "__main__":
    tmp = HERE / ".cv_frames"
    tmp.mkdir(exist_ok=True)
    n = 0
    for i, s in enumerate(stages):
        img = tmp / f"s{i:02d}.png"
        frame(*s).write_image(img)
        for _ in range(8 if s[2] else (4 if s[0] == 4 else 2)):
            shutil.copy(img, tmp / f"{n:03d}.png")
            n += 1
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "3", "-i", str(tmp / "%03d.png"), "-vf",
                    "fps=6,scale=800:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "cv_rotate.gif")], check=True)
    ims = [Image.open(tmp / f"s{i:02d}.png").convert("RGB") for i in (1, 4, 9, len(stages) - 1)]
    w, h = ims[0].size
    sheet = Image.new("RGB", (2 * w + 16, 2 * h + 16), "white")
    for i, im in enumerate(ims):
        sheet.paste(im, ((i % 2) * (w + 16), (i // 2) * (h + 16)))
    sheet.save(HERE / "cv_rotate_frames.png")
    shutil.rmtree(tmp)

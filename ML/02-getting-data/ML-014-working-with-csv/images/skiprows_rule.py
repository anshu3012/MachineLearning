"""The skiprows rule, line by line: pandas calls the rule with each line number i of aug_train.csv and skips the line
when the rule returns True. Rule: i > 0 and i % 2 == 0 (keep the header, skip every even line after it).
The lines shown are the real first seven lines of the file; the row count is checked with read_csv.
Plotly frames -> ffmpeg GIF + _frames.png grid. Run: python skiprows_rule.py -> skiprows_rule.gif, skiprows_rule_frames.png"""
import shutil
import subprocess
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
from PIL import Image

HERE = Path(__file__).parent
BLUE, GREEN, RED, GREY = "#4C78A8", "#54A24B", "#E45756", "#6B6B6B"
MONO = "Latin Modern Mono, Courier New, monospace"
CSV = HERE.parent / "data" / "aug_train.csv"
rule = lambda i: i > 0 and i % 2 == 0
N = 7
lines = [",".join(l.split(",")[:2]) + ",..." for l in CSV.read_text().splitlines()[:N]]
kept = pd.read_csv(CSV, skiprows=rule)
assert len(pd.read_csv(CSV)) == 1000 and len(kept) == 500 and kept.enrollee_id[:3].tolist() == [8949, 11561, 666]


def frame(k):                                                  # lines 0..k-1 are decided; k == N + 1: the summary
    fig = go.Figure()
    fig.add_annotation(x=0, y=N + 0.3, text="<b>skiprows=lambda i: i > 0 and i % 2 == 0</b>", showarrow=False,
                       xanchor="left", font=dict(family=MONO, size=27))
    for i, text in enumerate(lines):
        y = N - 1 - i
        done, now = i < k, i == k - 1
        skip = rule(i)
        colour = GREY if not done else (RED if skip else "black")
        if now:
            fig.add_shape(type="rect", x0=-0.15, x1=10.1, y0=y - 0.42, y1=y + 0.42, line=dict(width=0),
                          fillcolor="#FFF1C9", layer="below")
        fig.add_annotation(x=0, y=y, text=f"i = {i}", showarrow=False, xanchor="left", font=dict(size=24, color=GREY))
        shown = f"<s>{text}</s>" if done and skip else text
        fig.add_annotation(x=1.0, y=y, text=shown, showarrow=False, xanchor="left",
                           font=dict(family=MONO, size=24, color=colour))
        if done:
            why = (f"{i} > 0 is False: <b>kept</b> (header)" if i == 0 else
                   f"{i} % 2 = {i % 2}: " + ("rule is True, <b>skipped</b>" if skip else "rule is False, <b>kept</b>"))
            fig.add_annotation(x=4.9, y=y, text=why, showarrow=False, xanchor="left",
                               font=dict(size=24, color=RED if skip else GREEN))
    if k > N:
        fig.add_annotation(x=5, y=-1.0, text="<b>Whole file: 500 of the 1,000 rows kept</b> (8949, 11561, 666, ...)",
                           showarrow=False, font=dict(size=26, color=BLUE))
    fig.update_xaxes(range=[-0.2, 10.2], visible=False)
    fig.update_yaxes(range=[-1.5, N + 0.9], visible=False)
    fig.update_layout(template="simple_white", width=1200, height=640, showlegend=False,
                      font=dict(family="Latin Modern Roman", size=24), margin=dict(l=20, r=20, t=10, b=10))
    return fig


if __name__ == "__main__":
    tmp = HERE / ".skip_frames"
    tmp.mkdir(exist_ok=True)
    ks = list(range(0, N + 2))
    for j, k in enumerate(ks):
        frame(k).write_image(tmp / f"{j:03d}.png")
    last = len(ks) - 1
    for j in range(last + 1, last + 5):                        # hold the final frame
        shutil.copy(tmp / f"{last:03d}.png", tmp / f"{j:03d}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "1", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=900:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "skiprows_rule.gif")], check=True)
    keys = [Image.open(tmp / f"{j:03d}.png").convert("RGB") for j in (1, 3, 5, last)]
    w, h = keys[0].size
    sheet = Image.new("RGB", (2 * w + 16, 2 * h + 16), "white")
    for j, im in enumerate(keys):
        sheet.paste(im, ((j % 2) * (w + 16), (j // 2) * (h + 16)))
    sheet.save(HERE / "skiprows_rule_frames.png")
    shutil.rmtree(tmp)

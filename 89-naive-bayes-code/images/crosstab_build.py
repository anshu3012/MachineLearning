"""Training Naive Bayes on Play Tennis, for the feature outlook (section 4): the 14 days are counted into a
crosstab (value x class), and each class column is divided by the class size to give P(outlook | play).
Run: python crosstab_build.py -> crosstab_build.gif, crosstab_build_frames.png (Plotly frames + ffmpeg)"""
import shutil
import subprocess
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
from PIL import Image
from plotly.subplots import make_subplots

HERE = Path(__file__).parent
df = pd.read_csv(HERE.parent / "data" / "play_tennis.csv")
BLUE, RED, L_BLUE, L_RED, GREY, HILITE = "#4C78A8", "#E45756", "#DCE6F1", "#F9DCDC", "#F2F2F2", "#F58518"
FONT = dict(family="Latin Modern Roman", size=22, color="black")
tab = pd.crosstab(df["outlook"], df["play"])[["No", "Yes"]]
n = df["play"].value_counts()
assert tab.loc["Overcast", "No"] == 0 and tab.loc["Sunny", "No"] == 3 and n["Yes"] == 9      # section 4
VALUES = list(tab.index)
CELLS = [(v, c) for c in ("No", "Yes") for v in VALUES]                # the order the cells are filled in


def frame(k, divide, title):
    """k: how many crosstab cells are filled; divide: show count / class size instead of the count."""
    done = CELLS[:k]
    cur = CELLS[k - 1] if 0 < k <= len(CELLS) and not divide else None
    fig = make_subplots(rows=1, cols=2, specs=[[{"type": "table"}, {"type": "table"}]], column_widths=[0.4, 0.6],
                        horizontal_spacing=0.06,
                        subplot_titles=["the 14 days", "P(outlook | play)" if divide else "crosstab: counts"])
    hit = [cur is not None and o == cur[0] and p == cur[1] for o, p in zip(df.outlook, df.play)]
    base = [L_BLUE if p == "Yes" else L_RED for p in df.play]
    fill = [HILITE if h else b for h, b in zip(hit, base)]
    fig.add_trace(go.Table(columnwidth=[0.5, 1, 0.7],
                           header=dict(values=["day", "outlook", "play"], fill_color="#444444",
                                       font={**FONT, "color": "white"}, height=34),
                           cells=dict(values=[list(range(1, 15)), list(df.outlook), list(df.play)],
                                      fill_color=[fill] * 3, font=FONT, height=31)), 1, 1)

    def cell(v, c):
        if (v, c) not in done:
            return ""
        m = tab.loc[v, c]
        return f"{m}/{n[c]} = {m / n[c]:.2f}" if divide else str(m)

    rows = VALUES + ["class size"]
    col = {c: [cell(v, c) for v in VALUES] + [str(n[c]) if k >= len(CELLS) else ""] for c in ("No", "Yes")}
    fills = [[GREY] * 4] + [[HILITE if cur == (v, c) else light for v in VALUES] + ["white"]
                            for c, light in (("No", L_RED), ("Yes", L_BLUE))]
    fig.add_trace(go.Table(columnwidth=[1, 1.2, 1.2],
                           header=dict(values=["outlook", "play = No", "play = Yes"], fill_color=["#444444", RED, BLUE],
                                       font={**FONT, "color": "white"}, height=44),
                           cells=dict(values=[rows, col["No"], col["Yes"]], fill_color=fills,
                                      font=dict(family=FONT["family"], size=26, color="black"), height=60)), 1, 2)
    fig.update_layout(width=1200, height=640, font=FONT, margin=dict(l=20, r=20, t=120, b=10),
                      title=dict(text=f"<b>{title}</b>", x=0.5, y=0.96, font_size=30))
    fig.update_annotations(font_size=26)
    return fig


if __name__ == "__main__":
    tmp = HERE / ".crosstab"
    tmp.mkdir(exist_ok=True)
    seq = [(frame(0, False, "Training: count each outlook value, per class"), 3, True)]
    for k, (v, c) in enumerate(CELLS, 1):
        seq.append((frame(k, False, f"{v} days with play = {c}: {tab.loc[v, c]}"), 2, k in (1, 2)))
    seq.append((frame(len(CELLS) + 1, False, "The class sizes: 5 No days, 9 Yes days"), 3, False))
    seq.append((frame(len(CELLS) + 1, True, "Divide each column by its class size"), 7, True))
    keys, i = [], 0
    for fig, hold, key in seq:
        png = tmp / f"{i:03d}.png"
        fig.write_image(png)
        if key:
            keys.append(Image.open(png).convert("RGB"))
        for j in range(1, hold):
            shutil.copy(png, tmp / f"{i + j:03d}.png")
        i += hold
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "1", "-i", str(tmp / "%03d.png"), "-vf",
                    "fps=5,scale=900:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "crosstab_build.gif")], check=True)
    w, h = keys[0].size
    sheet = Image.new("RGB", (2 * w + 16, 2 * h + 16), "white")
    for i, f in enumerate(keys):
        sheet.paste(f, ((i % 2) * (w + 16), (i // 2) * (h + 16)))
    sheet.save(HERE / "crosstab_build_frames.png")
    shutil.rmtree(tmp)

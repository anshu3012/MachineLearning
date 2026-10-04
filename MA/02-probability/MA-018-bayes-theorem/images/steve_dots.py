"""The librarian-or-farmer puzzle as counts (section 2): 210 people, 10 librarians and 200 farmers.
40 percent of librarians (4) and 10 percent of farmers (20) fit the description "meek and tidy".
Keeping only the 24 who fit, 4 are librarians: 4/24 = 16.7 percent.
Idea after Sanderson (3Blue1Brown), "Bayes theorem, the geometry of changing beliefs" (the representative sample).
Run: python steve_dots.py -> steve_dots.gif, steve_dots_frames.png (Plotly frames + ffmpeg)"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from PIL import Image

HERE = Path(__file__).parent
LIB_C, FARM_C = "#F58518", "#4C78A8"
N_LIB, N_FARM, FIT_LIB, FIT_FARM = 10, 200, 0.4, 0.1
ROWS = 10
# one column of librarians, then a gap, then 20 columns of farmers
x = np.array([0.0] * N_LIB + [1.6 + c for c in range(N_FARM // ROWS) for _ in range(ROWS)])
y = np.array(list(range(ROWS)) * (1 + N_FARM // ROWS), dtype=float)
is_lib = np.arange(N_LIB + N_FARM) < N_LIB
fits = np.zeros(N_LIB + N_FARM, dtype=bool)
fits[:int(N_LIB * FIT_LIB)] = True                                   # 4 librarians
for c in range(N_FARM // ROWS):                                      # 10 percent of each farmer column
    fits[N_LIB + c * ROWS + (c * 3) % ROWS] = True
n_fit_lib, n_fit = int((fits & is_lib).sum()), int(fits.sum())
assert (n_fit_lib, n_fit) == (4, 24)                                 # the numbers of section 2
# where the 24 who fit end up: one row, librarians first
order = np.argsort(~is_lib[fits], kind="stable")
tx, ty = x.copy(), y.copy()
slots = np.linspace(1.5, 20.5, n_fit)
tx[np.flatnonzero(fits)[order]] = slots
ty[fits] = 4.5
FONT = dict(family="Latin Modern Roman", size=26, color="black")


def frame(title, fade, t=0.0, note=""):
    """fade: opacity of the people who do not fit; t: 0 = grid positions, 1 = the 24 lined up in a row."""
    fig = go.Figure()
    px, py = x + t * (tx - x), y + t * (ty - y)
    for lib, color, name in [(True, LIB_C, "librarian"), (False, FARM_C, "farmer")]:
        for fit in (False, True):
            m = (is_lib == lib) & (fits == fit)
            fig.add_trace(go.Scatter(x=px[m], y=py[m], mode="markers", showlegend=False,
                                     marker=dict(size=24 + 12 * t * fit, color=color, opacity=1 if fit else fade,
                                                 line=dict(width=3 if fit and fade < 1 else 0, color="black"))))
    if t == 0 and fade > 0.1:
        fig.add_annotation(x=0, y=10.3, text="<b>10<br>librarians</b>", showarrow=False, font=dict(color=LIB_C, size=24))
        fig.add_annotation(x=11, y=10.3, text="<b>200 farmers</b>", showarrow=False, font=dict(color=FARM_C, size=26))
    if note:
        fig.add_annotation(x=10.3, y=-1.6, text=note, showarrow=False, font=dict(size=30))
    fig.update_xaxes(visible=False, range=[-1.6, 22.2])
    fig.update_yaxes(visible=False, range=[-2.6, 11.6])
    fig.update_layout(width=1100, height=700, font=FONT, plot_bgcolor="white", paper_bgcolor="white",
                      title=dict(text=f"<b>{title}</b>", x=0.5, y=0.96, font_size=32),
                      margin=dict(l=10, r=10, t=70, b=10))
    return fig


if __name__ == "__main__":
    tmp = HERE / ".steve_frames"
    tmp.mkdir(exist_ok=True)
    seq = [(frame("1. A sample of 210 people", 1.0, note="20 farmers for every librarian"), 20),
           (frame("2. Who fits “meek and tidy”?", 0.3,
                  note="40% of librarians = 4 &nbsp;&nbsp;&nbsp; 10% of farmers = 20"), 25),
           (frame("3. Keep only the 24 who fit", 0.06, note="4 librarians + 20 farmers = 24"), 20)]
    seq += [(frame("3. Keep only the 24 who fit", 0.06 * (1 - t), t), 1) for t in np.linspace(0.1, 0.9, 9)]
    seq += [(frame("4. Librarians among those who fit", 0.0, 1.0,
                   note="<b>4 of 24 = 16.7%</b> are librarians"), 35)]
    keys, n = [], 0
    for fig, hold in seq:
        png = tmp / f"{n:03d}.png"
        fig.write_image(png)
        if hold > 1:
            keys.append(Image.open(png).convert("RGB"))
        for k in range(1, hold):
            shutil.copy(png, tmp / f"{n + k:03d}.png")
        n += hold
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "10", "-i", str(tmp / "%03d.png"), "-vf",
                    "fps=10,scale=800:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "steve_dots.gif")], check=True)
    w, h = keys[0].size
    sheet = Image.new("RGB", (2 * w + 16, 2 * h + 16), "white")
    for i, f in enumerate(keys):
        sheet.paste(f, ((i % 2) * (w + 16), (i // 2) * (h + 16)))
    sheet.save(HERE / "steve_dots_frames.png")
    shutil.rmtree(tmp)

"""Plotly figures for the measures of dispersion, all from the Note's own numbers:
same mean, different spread (section 2); range and one outlier (section 3); variance against mean absolute
deviation as one value moves out to 50 (section 5, GIF + frame grid); salaries in LPA with the standard
deviation in the same units (section 6)."""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from PIL import Image

here = Path(__file__).parent
FONT = dict(family="Latin Modern Roman", size=20)
BLUE, ORANGE, GREEN, RED, GREY = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#6B6B6B"
LAY = dict(template="simple_white", font=FONT)


def save(fig, name):
    fig.write_image(here / f"{name}.png", scale=2); fig.write_image(here / f"{name}.pdf")


# Section 2: same mean, different spread
A, B = np.array([-5, 0, 5]), np.array([-10, 0, 10])
assert A.mean() == B.mean() == 0
fig = go.Figure()
for y, v, c in ((1, A, BLUE), (0, B, ORANGE)):
    fig.add_trace(go.Scatter(x=v, y=[y] * 3, mode="markers+text", text=[str(t) for t in v],
                             textposition="top center", marker=dict(size=22, color=c), showlegend=False))
    fig.add_shape(type="line", x0=v.min(), x1=v.max(), y0=y, y1=y, line=dict(color=c, width=3), layer="below")
fig.add_vline(x=0, line=dict(color=GREY, dash="dash", width=2))
fig.add_annotation(x=0, y=1.55, text="both means = 0", showarrow=False, bgcolor="white", font=dict(size=20, color=GREY))
fig.update_layout(**LAY, width=900, height=380, margin=dict(l=170, r=30, t=30, b=60),
                  xaxis=dict(title="value", range=[-12, 12], dtick=5),
                  yaxis=dict(range=[-0.6, 1.8], tickvals=[1, 0], ticktext=["-5, 0, 5", "-10, 0, 10"]))
save(fig, "same_mean")

# Section 3: the range uses only the two extremes
base = np.arange(0, 51, 5)                      # values between 0 and 50
withx = np.append(base, 250)                    # ... plus one outlier
assert np.ptp(A) == 10 and np.ptp(B) == 20 and np.ptp(base) == 50 and np.ptp(withx) == 250
rows = [("-5, 0, 5", A), ("-10, 0, 10", B), ("0 to 50", base), ("0 to 50 + one 250", withx)]
fig = go.Figure()
for i, (name, v) in enumerate(rows):
    y = len(rows) - 1 - i
    c = RED if i == 3 else (BLUE if i % 2 == 0 else ORANGE)
    fig.add_shape(type="line", x0=v.min(), x1=v.max(), y0=y, y1=y, line=dict(color=c, width=6), layer="below")
    fig.add_trace(go.Scatter(x=v, y=[y] * len(v), mode="markers", marker=dict(size=13, color=c, line=dict(
        width=1.5, color="white")), showlegend=False))
    fig.add_annotation(x=v.max(), y=y, text=f"range {np.ptp(v)}", showarrow=False, xanchor="left", xshift=12,
                       font=dict(size=20, color=c))
fig.update_layout(**LAY, width=1000, height=420, margin=dict(l=200, r=30, t=20, b=60),
                  xaxis=dict(title="value", range=[-15, 310]),
                  yaxis=dict(range=[-0.6, 3.6], tickvals=[3, 2, 1, 0], ticktext=[r[0] for r in rows]))
save(fig, "range_outlier")

# Section 6: salaries, standard deviation in LPA
sal = np.array([16, 17, 13, 14])
mu, var, sd = sal.mean(), sal.var(), sal.std()
assert mu == 15 and var == 2.5 and round(sd, 2) == 1.58
fig = go.Figure()
fig.add_vrect(x0=mu - sd, x1=mu + sd, fillcolor=GREEN, opacity=0.15, line_width=0)
fig.add_trace(go.Scatter(x=sal, y=[0] * 4, mode="markers+text", text=[f"{s} LPA" for s in sal],
                         textposition="top center", marker=dict(size=22, color=BLUE), showlegend=False))
fig.add_vline(x=mu, line=dict(color=GREY, dash="dash", width=2))
fig.add_annotation(x=mu, y=-0.55, text="mean 15 LPA", showarrow=False, font=dict(color=GREY))
fig.add_annotation(x=mu + sd, y=0.75, ax=mu, ay=0.75, xref="x", yref="y", axref="x", ayref="y", text="",
                   arrowhead=2, arrowwidth=3, arrowcolor=GREEN, showarrow=True)
fig.add_annotation(x=mu + sd / 2, y=0.95, text=f"σ = {sd:.2f} LPA", showarrow=False,
                   font=dict(color=GREEN, size=22))
fig.add_annotation(x=17.75, y=-0.45, text="σ² = 2.5 LPA²: no axis for squared rupees", showarrow=False,
                   xanchor="right", align="left", font=dict(color=GREY, size=18))
fig.update_layout(**LAY, width=950, height=380, margin=dict(l=30, r=30, t=20, b=60),
                  xaxis=dict(title="salary (LPA)", range=[12.5, 17.8], dtick=1), yaxis=dict(visible=False,
                  range=[-0.8, 1.2]))
save(fig, "salary_sd")

# Section 5: one value moves out; variance grows with its square, MAD in proportion
five = np.array([3, 2, 1, 5, 4])
assert five.var() == 2 and np.abs(five - five.mean()).mean() == 1.2
moves = np.arange(3, 51)                                   # the sixth value, from the mean out to 50
def stats(x6):
    d = np.append(five, x6)
    return d, d.var(), np.abs(d - d.mean()).mean()
V = np.array([stats(x)[1] for x in moves]); M = np.array([stats(x)[2] for x in moves])
d50, v50, m50 = stats(50)
assert round(d50.mean(), 2) == 10.83 and round(v50, 1) == 308.5
assert round(v50 / 2) == 154 and round(m50 / 1.2) == 11   # the text's "about 154" and "about 11"
print(f"at 50: variance {v50:.1f} (x{v50 / 2:.0f}), MAD {m50:.2f} (x{m50 / 1.2:.1f})")


def frame(i):
    x6 = moves[i]
    d, v, m = stats(x6)
    fig = make_subplots(rows=2, cols=1, row_heights=[0.32, 0.68], vertical_spacing=0.2,
                        subplot_titles=[f"data 3, 2, 1, 5, 4 and {x6}: mean {d.mean():.2f}",
                                        "spread, as a multiple of its value without the extra point"])
    fig.add_trace(go.Scatter(x=five, y=[0] * 5, mode="markers", marker=dict(size=16, color=BLUE),
                             showlegend=False), 1, 1)
    fig.add_trace(go.Scatter(x=[x6], y=[0], mode="markers", marker=dict(size=20, color=RED), showlegend=False),
                  1, 1)
    fig.add_trace(go.Scatter(x=[d.mean()], y=[0], mode="markers", marker=dict(size=22, color="black",
                             symbol="triangle-up"), showlegend=False), 1, 1)
    fig.add_trace(go.Scatter(x=moves[:i + 1], y=V[:i + 1] / 2, name=f"variance: {v:.1f} (x{v / 2:.0f})",
                             line=dict(color=ORANGE, width=4)), 2, 1)
    fig.add_trace(go.Scatter(x=moves[:i + 1], y=M[:i + 1] / 1.2, name=f"mean absolute deviation: {m:.2f} "
                             f"(x{m / 1.2:.1f})", line=dict(color=GREEN, width=4)), 2, 1)
    fig.update_xaxes(range=[0, 52], row=1, col=1); fig.update_yaxes(visible=False, row=1, col=1)
    fig.update_xaxes(title="the sixth value", range=[0, 52], row=2, col=1)
    fig.update_yaxes(title="times its starting value", range=[0, 160], row=2, col=1)
    fig.update_layout(**LAY, width=900, height=720, margin=dict(l=80, r=20, t=60, b=60),
                      legend=dict(x=0.03, y=0.5, yanchor="top", font=dict(size=20)))
    fig.update_annotations(font=dict(family="Latin Modern Roman", size=21))
    return fig


if __name__ == "__main__":
    tmp = here / ".outlier"
    tmp.mkdir(exist_ok=True)
    idx = list(range(0, len(moves), 2)) + [len(moves) - 1]
    for n, i in enumerate(idx):
        frame(i).write_image(tmp / f"{n:03d}.png")
    for k in range(len(idx), len(idx) + 12):                 # hold the last frame
        shutil.copy(tmp / f"{len(idx) - 1:03d}.png", tmp / f"{k:03d}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "6", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=720:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(here / "outlier_growth.gif")], check=True)
    # the PDF shows the end state: the variance's square growth against the MAD's straight line
    shutil.copy(tmp / f"{len(idx) - 1:03d}.png", here / "outlier_growth_frames.png")
    shutil.rmtree(tmp)

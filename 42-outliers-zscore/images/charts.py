"""Charts for Note 42 (placement data): column shapes, the mean +- 3 std limits, and trimming vs capping."""
from pathlib import Path
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy import stats

here = Path(__file__).parent
BLUE, ORANGE, GREEN, RED, GREY = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#6B6B6B"
df = pd.read_csv(here.parent / "data" / "placement.csv")
mean, std = df["cgpa"].mean(), df["cgpa"].std()
lo, hi = mean - 3 * std, mean + 3 * std
out = (df["cgpa"] < lo) | (df["cgpa"] > hi)

# 1. cgpa is bell-shaped, the exam marks are right-skewed: density histogram (30 bins) and KDE (Scott's bandwidth,
#    drawn 3 bandwidths past the data)
names = {"cgpa": f"cgpa (skew {df['cgpa'].skew():.2f})",
         "placement_exam_marks": f"placement_exam_marks (skew {df['placement_exam_marks'].skew():.2f})"}
fig = make_subplots(1, 2, subplot_titles=list(names.values()), horizontal_spacing=0.1)
for c, col in enumerate(names, start=1):
    x = df[col].to_numpy(float)
    dens, edges = np.histogram(x, bins=30, density=True)
    fig.add_trace(go.Bar(x=(edges[:-1] + edges[1:]) / 2, y=dens, width=np.diff(edges), marker=dict(color=BLUE, line_width=0),
                         opacity=0.5), 1, c)
    k = stats.gaussian_kde(x)
    bw = np.sqrt(k.covariance[0, 0])
    grid = np.linspace(x.min() - 3 * bw, x.max() + 3 * bw, 400)
    fig.add_trace(go.Scatter(x=grid, y=k(grid), mode="lines", line=dict(color=BLUE, width=3, shape="spline")), 1, c)
    fig.update_xaxes(title="value", row=1, col=c)
fig.update_yaxes(title="density", row=1, col=1)
fig.update_layout(template="simple_white", width=1000, height=400, showlegend=False, bargap=0,
                  font=dict(family="Latin Modern Roman", size=20), margin=dict(l=90, r=30, t=60, b=70))
fig.update_annotations(font_size=21)
fig.write_image(here / "distributions.png", scale=2)
fig.write_image(here / "distributions.pdf")

# Plotly helpers
FONT = dict(family="Latin Modern Roman", size=20)
BINS = dict(start=4.8, end=9.2, size=0.1)


def save(fig, name, width, height):
    fig.update_layout(template="simple_white", width=width, height=height, showlegend=False, font=FONT,
                      barmode="overlay", bargap=0.05, margin=dict(l=90, r=30, t=70, b=70))
    fig.update_annotations(font_size=19)
    fig.write_image(here / f"{name}.png", scale=2)
    fig.write_image(here / f"{name}.pdf")


def limits(fig, **rc):
    for v in (lo, hi):
        fig.add_vline(x=v, line=dict(color=GREY, width=2, dash="dash"), **rc)


# 2. the limits on cgpa and the 5 outliers
fig = go.Figure()
fig.add_trace(go.Histogram(x=df.loc[~out, "cgpa"], xbins=BINS, marker_color=BLUE))
fig.add_trace(go.Histogram(x=df.loc[out, "cgpa"], xbins=BINS, marker_color=RED))
limits(fig)
fig.add_annotation(x=lo, y=1.0, yref="paper", yanchor="bottom", showarrow=False, text=f"lower {lo:.2f}")
fig.add_annotation(x=hi, y=1.0, yref="paper", yanchor="bottom", showarrow=False, text=f"upper {hi:.2f}")
fig.add_annotation(x=lo - 0.12, y=12, showarrow=False, font_color=RED, xanchor="right",
                   text="4.89, 4.90, 4.92")
fig.add_annotation(x=hi + 0.12, y=12, showarrow=False, font_color=RED, xanchor="left", text="8.87, 9.12")
fig.add_annotation(x=5.25, y=55, showarrow=False, font_color=BLUE, xanchor="left", align="left",
                   text=f"995 inside<br>mean {mean:.2f}, std {std:.2f}")
fig.update_xaxes(title="cgpa", range=[4.0, 10.0], dtick=0.5)
fig.update_yaxes(title="students")
save(fig, "limits", 1000, 460)

# 3. before and after: original, trimmed, capped
capped = df["cgpa"].clip(lo, hi)
rows = [("original: 1000 rows", df["cgpa"], out),
        ("trimmed: 995 rows", df.loc[~out, "cgpa"], None),
        ("capped: 1000 rows, min 5.11, max 8.81", capped, out)]
fig = make_subplots(3, 1, shared_xaxes=True, vertical_spacing=0.1, subplot_titles=[r[0] for r in rows])
for i, (_, x, flag) in enumerate(rows, start=1):
    keep = x if flag is None else x[~flag]
    fig.add_trace(go.Histogram(x=keep, xbins=BINS, marker_color=BLUE), i, 1)
    if flag is not None:
        fig.add_trace(go.Histogram(x=x[flag], xbins=BINS, marker_color=RED if i == 1 else ORANGE), i, 1)
    limits(fig, row=i, col=1)
fig.add_annotation(x=lo + 0.05, y=3, xref="x3", yref="y3", ax=-30, ay=-60, arrowcolor=ORANGE, font_color=ORANGE,
                   text="3 values set to 5.11", xanchor="right")
fig.add_annotation(x=hi + 0.05, y=2, xref="x3", yref="y3", ax=30, ay=-60, arrowcolor=ORANGE, font_color=ORANGE,
                   text="2 values set to 8.81", xanchor="left")
fig.update_xaxes(range=[4.0, 10.0], dtick=0.5)
fig.update_xaxes(title="cgpa", row=3, col=1)
fig.update_yaxes(title="students", row=2, col=1)
save(fig, "before_after", 1000, 760)

# 4. limits learned on the training set only, then applied to both sets (Section 11)
from sklearn.model_selection import train_test_split
train, test = train_test_split(df[["cgpa", "placement_exam_marks", "placed"]], test_size=0.2, random_state=42)
m, s = train["cgpa"].mean(), train["cgpa"].std()
tlo, thi = m - 3 * s, m + 3 * s
assert (round(tlo, 2), round(thi, 2)) == (5.12, 8.78)
jit = np.random.default_rng(0).uniform(-0.3, 0.3, len(df))
fig = go.Figure()
for yv, (name, part) in enumerate([("test: 200 rows", test), ("training: 800 rows", train)]):
    c = part["cgpa"].to_numpy()
    bad = (c < tlo) | (c > thi)
    fig.add_trace(go.Scatter(x=c[~bad], y=yv + jit[:len(c)][~bad], mode="markers",
                             marker=dict(color=BLUE, size=6, opacity=0.35)))
    fig.add_trace(go.Scatter(x=c[bad], y=np.full(bad.sum(), yv), mode="markers", marker=dict(color=RED, size=13)))
    for side, sel in (("right", c[bad] < tlo), ("left", c[bad] > thi)):
        if sel.any():
            fig.add_annotation(x=c[bad][sel].mean(), y=yv + 0.3, showarrow=False, font_color=RED, xanchor="center",
                               text=", ".join(f"{v:.2f}" for v in sorted(c[bad][sel])))
    assert bad.sum() == (4 if name.startswith("train") else 1)
for v, side in ((tlo, "right"), (thi, "left")):
    fig.add_vline(x=v, line=dict(color=GREY, width=2.5, dash="dash"))
    fig.add_annotation(x=v, y=1.0, yref="paper", yanchor="bottom", xanchor=side, showarrow=False,
                       text=f"training limit {v:.2f}")
fig.update_xaxes(title="cgpa", range=[4.5, 9.5], dtick=0.5)
fig.update_yaxes(tickvals=[0, 1], ticktext=["test", "training"], range=[-0.6, 1.6])
save(fig, "train_limits", 1000, 420)

# 5. the same rule on the right-skewed marks column (Section 12)
mk = df["placement_exam_marks"]
mlo, mhi = mk.mean() - 3 * mk.std(), mk.mean() + 3 * mk.std()
flag = mk > mhi
assert (round(mlo, 2), round(mhi, 2), flag.sum()) == (-25.17, 89.62, 8)
MB = dict(start=0, end=100, size=2)
fig = go.Figure()
fig.add_vrect(x0=-35, x1=0, fillcolor=GREY, opacity=0.15, line_width=0)
fig.add_trace(go.Histogram(x=mk[~flag], xbins=MB, marker_color=BLUE))
fig.add_trace(go.Histogram(x=mk[flag], xbins=MB, marker_color=RED))
for v, side in ((mlo, "left"), (mhi, "right")):
    fig.add_vline(x=v, line=dict(color=GREY, width=2.5, dash="dash"))
    fig.add_annotation(x=v, y=1.0, yref="paper", yanchor="bottom", xanchor=side, showarrow=False,
                       text=f"{'lower' if v < 0 else 'upper'} {v:.2f}")
fig.add_annotation(x=-12, y=40, showarrow=False, text="no mark is<br>below 0:<br>lower limit<br>flags nothing")
fig.add_annotation(x=mhi + 3, y=4, ax=-10, ay=-150, font_color=RED, arrowcolor=RED, xanchor="right",
                   text=f"{flag.sum()} marks flagged (0.8%)")
fig.update_xaxes(title="placement_exam_marks (skew 0.84)", range=[-35, 105], dtick=10)
fig.update_yaxes(title="students")
save(fig, "marks_limits", 1000, 460)

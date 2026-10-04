"""Charts for Note ML-042 (placement data): the IQR fences on the exam marks, and trimming vs capping."""
from pathlib import Path
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

here = Path(__file__).parent
BLUE, ORANGE, RED, GREY = "#4C78A8", "#F58518", "#E45756", "#6B6B6B"
FONT = dict(family="Latin Modern Roman", size=20)
BINS = dict(start=0, end=104, size=4)
df = pd.read_csv(here.parent / "data" / "placement.csv")
x = df["placement_exam_marks"]
q1, med, q3 = x.quantile([0.25, 0.5, 0.75])
iqr = q3 - q1
lo, hi = q1 - 1.5 * iqr, q3 + 1.5 * iqr
out = (x < lo) | (x > hi)


def save(fig, name, width, height):
    fig.update_layout(template="simple_white", width=width, height=height, showlegend=False, font=FONT,
                      barmode="overlay", bargap=0.05, margin=dict(l=90, r=30, t=70, b=70))
    fig.update_annotations(font_size=19)
    fig.write_image(here / f"{name}.png", scale=2)
    fig.write_image(here / f"{name}.pdf")


def box(values):
    # quartilemethod="linear" gives the same quartiles as pandas
    return go.Box(x=values, boxpoints="outliers", quartilemethod="linear", marker=dict(color=RED, size=8),
                  line=dict(color=BLUE, width=2.5), fillcolor="rgba(76,120,168,0.25)", name="")


def fences(fig, **rc):
    for v in (lo, hi):
        fig.add_vline(x=v, line=dict(color=GREY, width=2, dash="dash"), **rc)


# 1. box plot and histogram of the marks with Q1, Q3, IQR and the two fences
fig = make_subplots(2, 1, shared_xaxes=True, vertical_spacing=0.06, row_heights=[0.38, 0.62])
fig.add_trace(box(x), 1, 1)
fig.add_trace(go.Histogram(x=x[~out], xbins=BINS, marker_color=BLUE), 2, 1)
fig.add_trace(go.Histogram(x=x[out], xbins=BINS, marker_color=RED), 2, 1)
fences(fig, row="all", col=1)
fig.add_annotation(x=lo, y=1.0, xref="x", yref="paper", yanchor="bottom", showarrow=False,
                   text=f"lower fence {lo:g}")
fig.add_annotation(x=hi, y=1.0, xref="x", yref="paper", yanchor="bottom", showarrow=False,
                   text=f"upper fence {hi:g}")
for v, t, ay in [(q1, f"Q1 = {q1:g}", 42), (med, f"median {med:g}", -42), (q3, f"Q3 = {q3:g}", 42)]:
    fig.add_annotation(x=v, y=0.3 if ay < 0 else -0.3, xref="x", yref="y", ax=0, ay=ay, text=t,
                       arrowcolor=GREY)
fig.add_annotation(x=(q1 + q3) / 2, y=-0.3, xref="x", yref="y", ax=0, ay=42, arrowcolor="rgba(0,0,0,0)", text=f"IQR = {iqr:g}",
                   font_color=BLUE)
fig.add_annotation(x=hi + 2, y=26, xref="x2", yref="y2", xanchor="left", showarrow=False, font_color=RED,
                   align="left", text="15 outliers<br>86 to 100")
fig.add_annotation(x=-21, y=70, xref="x2", yref="y2", xanchor="left", showarrow=False, font_color=GREY,
                   align="left", text="no mark below<br>the lower fence<br>(lowest mark 0)")
fig.update_xaxes(range=[-30, 108], dtick=10)
fig.update_xaxes(title="placement_exam_marks", row=2, col=1)
fig.update_yaxes(showticklabels=False, showline=False, ticks="", row=1, col=1)
fig.update_yaxes(title="students", row=2, col=1)
save(fig, "fences", 1000, 620)

# 2. before and after: original, trimmed, capped (histogram left, box plot right)
capped = x.clip(lo, hi)
trimmed = x[~out]
rows = [("original: 1000 rows, 15 outliers", x, out, RED),
        (f"trimmed: {len(trimmed)} rows", trimmed, None, None),
        ("capped: 1000 rows, 15 values set to 84.5", capped, out, ORANGE)]
titles = [t for r in rows for t in (r[0], "")]
fig = make_subplots(3, 2, shared_xaxes=True, vertical_spacing=0.11, horizontal_spacing=0.06,
                    column_widths=[0.6, 0.4], subplot_titles=titles)
for i, (_, v, flag, colour) in enumerate(rows, start=1):
    keep = v if flag is None else v[~flag]
    fig.add_trace(go.Histogram(x=keep, xbins=BINS, marker_color=BLUE), i, 1)
    if flag is not None:
        fig.add_trace(go.Histogram(x=v[flag], xbins=BINS, marker_color=colour), i, 1)
    fig.add_trace(box(v), i, 2)
    fig.add_vline(x=hi, line=dict(color=GREY, width=2, dash="dash"), row=i, col=1)
    fig.add_vline(x=hi, line=dict(color=GREY, width=2, dash="dash"), row=i, col=2)
fig.add_annotation(x=83, y=0, xref="x4", yref="y4", ax=-20, ay=62, arrowcolor=RED, font_color=RED,
                   text="83: new fence 82", xanchor="right")
fig.add_annotation(x=86, y=15, xref="x5", yref="y5", ax=0, ay=-40, arrowcolor=ORANGE, font_color=ORANGE,
                   text="15 at 84.5", xanchor="center")
fig.update_xaxes(range=[0, 104], dtick=20)
fig.update_xaxes(title="placement_exam_marks", row=3)
fig.update_yaxes(showticklabels=False, showline=False, ticks="", col=2)
fig.update_yaxes(title="students", row=2, col=1)
fig.update_yaxes(range=[0, 125], col=1)
save(fig, "before_after", 1100, 820)

# 3. detect again after trimming: each round recomputes the fences from the rows that are left (Section 7.1)
rounds, d = [], x.copy()
while True:
    a, b = d.quantile([0.25, 0.75])
    f = b + 1.5 * (b - a)
    rounds.append((d, b, f))
    if not (d > f).any():
        break
    d = d[d <= f]
assert [(len(d), q, fe, (d > fe).sum()) for d, q, fe in rounds] == [(1000, 44, 84.5, 15), (985, 43, 82, 1), (984, 43, 82, 0)]
fig = make_subplots(3, 1, shared_xaxes=True, vertical_spacing=0.17,
                    subplot_titles=[f"round {i + 1}: {len(d)} rows, Q3 = {q:g}, upper fence {fe:g}, {(d > fe).sum()} outside"
                                    for i, (d, q, fe) in enumerate(rounds)])
for i, (d, q, fe) in enumerate(rounds, start=1):
    fig.add_trace(box(d), i, 1)
    fig.add_vline(x=fe, line=dict(color=GREY, width=2.5, dash="dash"), row=i, col=1)
fig.add_annotation(x=83, y=0, xref="x2", yref="y2", ax=-40, ay=-38, arrowcolor=RED, font_color=RED, xanchor="right",
                   text="83: inside 84.5, outside 82")
fig.update_xaxes(range=[0, 104], dtick=10)
fig.update_xaxes(title="placement_exam_marks", row=3, col=1)
fig.update_yaxes(showticklabels=False, showline=False, ticks="")
save(fig, "trim_rounds", 1000, 560)

# 4. robustness: replace the top mark (100) by a typo up to 1000; the z-score limit chases it, the IQR fence stays
top = x.idxmax()
typo = np.arange(100, 1001, 10)
zlim, fence = [], []
for v in typo:
    y = x.copy()
    y[top] = v
    zlim.append(y.mean() + 3 * y.std())
    fence.append(y.quantile(0.75) + 1.5 * (y.quantile(0.75) - y.quantile(0.25)))
assert round(zlim[0], 2) == 89.62 and round(zlim[-1], 1) == 141.2 and set(fence) == {84.5}
fig = go.Figure()
fig.add_trace(go.Scatter(x=typo, y=zlim, mode="lines", line=dict(color=ORANGE, width=4)))
fig.add_trace(go.Scatter(x=typo, y=fence, mode="lines", line=dict(color=BLUE, width=4)))
fig.add_annotation(x=1000, y=zlim[-1], xanchor="right", yanchor="bottom", showarrow=False, font_color=ORANGE,
                   text=f"z-score upper limit: 89.6 to {zlim[-1]:.1f}")
fig.add_annotation(x=1000, y=84.5, xanchor="right", yanchor="top", yshift=-6, showarrow=False, font_color=BLUE,
                   text="IQR upper fence: 84.5 throughout")
fig.update_xaxes(title="the top student's mark (really 100, typed as up to 1000)", range=[80, 1020])
fig.update_yaxes(title="upper limit", range=[70, 150])
save(fig, "robust_fence", 1000, 460)

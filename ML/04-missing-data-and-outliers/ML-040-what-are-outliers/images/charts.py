"""Plotly charts for Note ML-040: trimming vs capping, and the three detection rules. Example data."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

here = Path(__file__).parent
BLUE, ORANGE, GREEN, RED, GREY = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#6B6B6B"
FONT = dict(family="Latin Modern Roman", size=20)


def save(fig, name, width, height, top=80):
    fig.update_layout(template="simple_white", width=width, height=height, showlegend=False, font=FONT,
                      bargap=0.05, margin=dict(l=90, r=30, t=top, b=70))
    fig.update_annotations(font_size=21)
    fig.write_image(here / f"{name}.png", scale=2)
    fig.write_image(here / f"{name}.pdf")


# 1. trimming vs capping on one small column, limits 20 and 90
vals = np.array([5, 12, 28, 33, 38, 41, 45, 47, 50, 52, 55, 58, 61, 64, 68, 72, 77, 83, 96, 99])
lo, hi = 20, 90
out = (vals < lo) | (vals > hi)
rows = ["original", "trimmed", "capped"]
fig = go.Figure()
fig.add_trace(go.Scatter(x=vals, y=["original"] * 20, mode="markers",
                         marker=dict(size=16, color=[RED if o else BLUE for o in out])))
fig.add_trace(go.Scatter(x=vals[~out], y=["trimmed"] * (~out).sum(), mode="markers",
                         marker=dict(size=16, color=BLUE)))
capped = np.clip(vals, lo, hi)
fig.add_trace(go.Scatter(x=capped, y=["capped"] * 20, mode="markers",
                         marker=dict(size=16, color=[ORANGE if o else BLUE for o in out],
                                     line=dict(width=0))))
for v in (lo, hi):
    fig.add_vline(x=v, line=dict(color=GREY, width=2, dash="dash"))
fig.add_annotation(x=lo, y=1.02, yref="paper", text="lower limit 20", showarrow=False, yanchor="bottom")
fig.add_annotation(x=hi, y=1.02, yref="paper", text="upper limit 90", showarrow=False, yanchor="bottom")
fig.add_annotation(x=lo, y="capped", text="5, 12 become 20", ax=-10, ay=45, arrowcolor=ORANGE, font_color=ORANGE)
fig.add_annotation(x=hi, y="capped", text="96, 99 become 90", ax=10, ay=45, arrowcolor=ORANGE, font_color=ORANGE)
fig.add_annotation(x=10, y="trimmed", text="4 rows removed", showarrow=False, font_color=RED, yshift=32)
fig.update_yaxes(categoryorder="array", categoryarray=rows[::-1], showgrid=False)
fig.update_xaxes(title="value", range=[0, 104])
save(fig, "trim_cap", 1000, 460, top=60)

# 2. the three detection rules
rng = np.random.default_rng(1)
normal = rng.normal(60, 10, 2000)
skewed = rng.lognormal(3, 0.6, 2000)
rules = [
    ("normal column: mean ± 3 std", normal, 60 - 30, 60 + 30),
    ("skewed column: IQR fences", skewed, None, None),
    ("any column: 1st and 99th percentile", skewed, np.percentile(skewed, 1), np.percentile(skewed, 99)),
]
q1, q3 = np.percentile(skewed, [25, 75])
rules[1] = (rules[1][0], skewed, q1 - 1.5 * (q3 - q1), q3 + 1.5 * (q3 - q1))
fig = make_subplots(1, 3, horizontal_spacing=0.06, subplot_titles=[r[0] for r in rules])
for j, (_, data, a, b) in enumerate(rules, start=1):
    size = (data.max() - data.min()) / 60
    inside = data[(data >= a) & (data <= b)]
    outside = data[(data < a) | (data > b)]
    for part, col in [(inside, BLUE), (outside, RED)]:
        fig.add_trace(go.Histogram(x=part, marker_color=col,
                                   xbins=dict(start=data.min(), end=data.max() + size, size=size)), 1, j)
    for v in (a, b):
        fig.add_vline(x=v, line=dict(color=GREY, width=2, dash="dash"), row=1, col=j)
    fig.update_xaxes(title="value", row=1, col=j)
    fig.add_annotation(x=0.97 if j > 1 else 0.03, y=0.95, xref=f"x{j} domain" if j > 1 else "x domain",
                       yref=f"y{j} domain" if j > 1 else "y domain", xanchor="right" if j > 1 else "left", showarrow=False,
                       text=f"{len(outside)} of {len(data)} flagged", font=dict(color=RED, size=19))
fig.update_layout(barmode="overlay")
fig.update_yaxes(title="count", col=1)
fig.update_yaxes(range=[0, 135], row=1, col=1)
save(fig, "detection", 1400, 460)

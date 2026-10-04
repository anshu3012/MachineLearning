"""Why the feature map is n - f + 1 wide (section 6): a 3 x 3 filter on a 6 x 6 image can start at columns 0, 1, 2
and 3 of a row and no further, so the row gives 4 values. Each panel shows one starting position. Plotly."""
from pathlib import Path

import plotly.graph_objects as go
from plotly.subplots import make_subplots

HERE = Path(__file__).parent
N, F = 6, 3
POS = list(range(N - F + 1))
assert len(POS) == 4
fig = make_subplots(rows=1, cols=5, horizontal_spacing=0.03,
                    subplot_titles=[f"start at column {p}" for p in POS] + ["column 4: does not fit"])
for k, p in enumerate(POS + [4], start=1):
    for r in range(N):
        for c in range(N):
            fig.add_shape(type="rect", x0=c, x1=c + 1, y0=r, y1=r + 1, line=dict(color="#BBBBBB", width=1),
                          fillcolor="white", row=1, col=k)
    ok = p + F <= N
    fig.add_shape(type="rect", x0=p, x1=p + F, y0=0, y1=F, line=dict(color="#4C78A8" if ok else "#E45756", width=4,
                  dash="solid" if ok else "dash"), fillcolor="rgba(76,120,168,0.25)" if ok else "rgba(228,87,86,0.15)",
                  opacity=1, layer="above", row=1, col=k)
    fig.update_xaxes(range=[-0.3, 7.3], visible=False, row=1, col=k)
    fig.update_yaxes(range=[6.3, -0.3], visible=False, scaleanchor=f"x{'' if k == 1 else k}", row=1, col=k)
fig.update_layout(template="simple_white", width=1400, height=360, font=dict(family="Latin Modern Roman", size=18),
                  title=dict(text="A 3 × 3 filter on a 6 × 6 image: 6 − 3 + 1 = 4 starting positions per row", x=0.5,
                             font=dict(size=22)),
                  margin=dict(l=10, r=10, t=90, b=10))
fig.write_image(HERE / "fit_positions.png", scale=2)

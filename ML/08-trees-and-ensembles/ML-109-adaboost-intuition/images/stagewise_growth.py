"""Section 3, stage-wise additive: the vote of the first 1, 2 and 3 stumps on the Note's 10 students. Each panel
colours the plane by sign(sum of alpha_t h_t) over the stumps added so far; the title gives how many students the
vote gets right. Plotly."""
from pathlib import Path
import numpy as np
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from adaboost_common import X, Y, CGPA, IQ, score, BLUE, ORANGE, FONT

here = Path(__file__).parent
cg, iq = np.meshgrid(np.linspace(0.5, 9.5, 181), np.linspace(40, 135, 191))
grid = np.c_[cg.ravel(), iq.ravel()]
right = [int((np.sign(score(X, t)) == Y).sum()) for t in (1, 2, 3)]
assert right == [8, 8, 10]
titles = [f"after stump 1: {right[0]} of 10 right", f"stumps 1 + 2: {right[1]} of 10 right",
          f"stumps 1 + 2 + 3: {right[2]} of 10 right"]
fig = make_subplots(rows=1, cols=3, subplot_titles=titles, horizontal_spacing=0.05, shared_yaxes=True)
for c, t in enumerate((1, 2, 3), start=1):
    z = np.sign(score(grid, t)).reshape(cg.shape)
    fig.add_trace(go.Heatmap(x=cg[0], y=iq[:, 0], z=z, colorscale=[[0, "#FDE5CC"], [1, "#DCE6F2"]], zmin=-1, zmax=1,
                             showscale=False, hoverinfo="skip"), row=1, col=c)
    for cls, col, sym in ((1, BLUE, "cross"), (-1, ORANGE, "line-ew")):
        m = Y == cls
        fig.add_scatter(x=CGPA[m], y=IQ[m], mode="markers", marker=dict(size=13, color=col, symbol=sym + "-open" if False else "circle",
                        line=dict(width=1.5, color="white")), showlegend=False, row=1, col=c)
    wrong = np.sign(score(X, t)) != Y
    fig.add_scatter(x=CGPA[wrong], y=IQ[wrong], mode="markers", marker=dict(size=24, symbol="circle-open", color="black",
                    line=dict(width=2.5)), showlegend=False, row=1, col=c)
    fig.update_xaxes(title="CGPA", range=[0.5, 9.5], row=1, col=c)
fig.update_yaxes(title="IQ", range=[40, 135], row=1, col=1)
fig.update_layout(template="simple_white", width=1200, height=440, font=FONT, margin=dict(l=60, r=20, t=50, b=60))
fig.write_image(here / "stagewise_growth.png", scale=2)
fig.write_image(here / "stagewise_growth.pdf")

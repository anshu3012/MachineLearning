"""Section 6: the weighted sum 0.69 h1 + 0.97 h2 + 1.28 h3 in every box that the three cuts make. Its sign is the
prediction: blue boxes (placed) form an L shape that no single stump can draw. Plotly."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from adaboost_common import X, Y, CGPA, IQ, STAGES, score, BLUE, ORANGE, FONT

here = Path(__file__).parent
cuts = {}
for s in STAGES:
    t = s["stump"].tree_
    cuts.setdefault(int(t.feature[0]), []).append(float(t.threshold[0]))
xs = [0.5] + sorted(cuts.get(0, [])) + [9.5]
ys = [40] + sorted(cuts.get(1, [])) + [135]
assert (np.sign(score(X)) == Y).all()
fig = go.Figure()
for i in range(len(xs) - 1):
    for j in range(len(ys) - 1):
        cx, cy = (xs[i] + xs[i + 1]) / 2, (ys[j] + ys[j + 1]) / 2
        v = score(np.array([[cx, cy]]))[0]
        fig.add_shape(type="rect", x0=xs[i], x1=xs[i + 1], y0=ys[j], y1=ys[j + 1], line=dict(color="white", width=2),
                      fillcolor="#DCE6F2" if v > 0 else "#FDE5CC", layer="below")
        fig.add_annotation(x=xs[i] + 0.15, y=ys[j + 1] - 5, xanchor="left", text=f"<b>{v:+.2f}</b>", showarrow=False, font=dict(size=20, color=BLUE if v > 0 else ORANGE))
for f, ths in cuts.items():
    for th in ths:
        if f == 0:
            fig.add_vline(x=th, line=dict(color="black", dash="dash", width=2))
        else:
            fig.add_hline(y=th, line=dict(color="black", dash="dash", width=2))
for cls, col in ((1, BLUE), (-1, ORANGE)):
    m = Y == cls
    fig.add_scatter(x=CGPA[m], y=IQ[m], mode="markers", marker=dict(size=13, color=col, line=dict(width=1.5, color="white")),
                    name="placed (+1)" if cls == 1 else "not placed (-1)")
fig.update_layout(template="simple_white", width=900, height=620, font=FONT,
                  xaxis=dict(title="CGPA", range=[0.5, 9.5]), yaxis=dict(title="IQ", range=[40, 135]),
                  legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.15), margin=dict(l=60, r=20, t=20, b=90))
fig.write_image(here / "score_boxes.png", scale=2)
fig.write_image(here / "score_boxes.pdf")

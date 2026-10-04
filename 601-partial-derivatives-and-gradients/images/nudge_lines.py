"""A partial derivative without a graph (Plotly frames). Left: the input plane with the point (1, 1). Right: the output
number line. A nudge of 0.1 in x1 only moves the output from 4 to 4.31 (about 3 x 0.1); the same nudge in x2 only moves
it to 4.52 (about 5 x 0.1). f = x1^2 + x1 x2 + 2 x2^2. Idea after Khan Academy, "Partial derivatives, introduction".
Run: python nudge_lines.py -> nudge_lines.gif, nudge_lines_frames.png"""
from pathlib import Path
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from gifkit import FONT, GREEN, GREY, ORANGE, make_gif

here = Path(__file__).parent
f = lambda a, b: a ** 2 + a * b + 2 * b ** 2
assert round(f(1.1, 1), 2) == 4.31 and round(f(1, 1.1), 2) == 4.52


def frame(d1, d2):
    """d1, d2: the nudge in x1 and in x2 (one of them is 0)."""
    col, which = (ORANGE, "x₁") if d2 == 0 else (GREEN, "x₂")
    out, d = f(1 + d1, 1 + d2), d1 + d2
    fig = make_subplots(rows=1, cols=2, column_widths=[0.5, 0.5], horizontal_spacing=0.12,
                        subplot_titles=("input: a point in the plane", "output: one number f"))
    fig.add_trace(go.Scatter(x=[1], y=[1], mode="markers", marker=dict(size=16, color="black")), row=1, col=1)
    if d > 0:
        fig.add_annotation(x=1 + d1, y=1 + d2, ax=1, ay=1, xref="x", yref="y", axref="x", ayref="y", arrowhead=2,
                           arrowwidth=5, arrowcolor=col)
        fig.add_annotation(x=1 + d1 + (0.012 if d2 == 0 else 0), y=1 + d2 + (0.012 if d1 == 0 else 0), xref="x", yref="y",
                           text=f"nudge {which} by {d:.2f}", showarrow=False, font=dict(color=col, size=22),
                           xanchor="left" if d2 == 0 else "center", yanchor="middle" if d2 == 0 else "bottom")
    fig.update_xaxes(title="x₁", range=[0.9, 1.22], dtick=0.1, row=1, col=1)
    fig.update_yaxes(title="x₂", range=[0.9, 1.22], dtick=0.1, row=1, col=1)
    # output number line
    fig.add_trace(go.Scatter(x=[3.8, 4.7], y=[0, 0], mode="lines", line=dict(color=GREY, width=2)), row=1, col=2)
    fig.add_trace(go.Scatter(x=[4, out], y=[0, 0], mode="lines", line=dict(color=col, width=12)), row=1, col=2)
    fig.add_trace(go.Scatter(x=[4], y=[0], mode="markers", marker=dict(size=16, color="black")), row=1, col=2)
    fig.add_trace(go.Scatter(x=[out], y=[0], mode="markers", marker=dict(size=16, color=col)), row=1, col=2)
    fig.update_xaxes(title="f", range=[3.8, 4.7], dtick=0.1, row=1, col=2)
    fig.update_yaxes(visible=False, range=[-1, 1], row=1, col=2)
    if d > 0:
        fig.add_annotation(x=4.25, y=0.45, xref="x2", yref="y2", showarrow=False, font=dict(color=col, size=22),
                           text=f"f moves by {out - 4:.2f}<br>= {(out - 4) / d:.1f} × the nudge")
    fig.update_layout(template="simple_white", width=1000, height=520, font=FONT, showlegend=False,
                      margin=dict(l=70, r=20, t=110, b=65),
                      title=dict(x=0.5, y=0.96, font=dict(size=22),
                                 text=f"f({1 + d1:.2f}, {1 + d2:.2f}) = <b>{out:.2f}</b>"
                                      + ("" if d else "   (start: the point (1, 1), where f = 4)")))
    fig.update_annotations(selector=dict(yref="paper"), font_size=22)
    return fig


steps = [0.02, 0.04, 0.06, 0.08, 0.1]
figs = [frame(0, 0)] + [frame(s, 0) for s in steps] + [frame(0, 0)] + [frame(0, s) for s in steps]
holds = [6] + [2] * 4 + [12] + [4] + [2] * 4 + [14]
make_gif(figs, here / "nudge_lines", fps=6, holds=holds, keys=[0, 5, 11], cols=1, width=1000)

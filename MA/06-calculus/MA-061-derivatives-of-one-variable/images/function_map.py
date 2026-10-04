"""A function as a map from inputs to outputs (Plotly): f: x -> x^2 on the inputs -2, -1, 0, 1, 2, 3. Every input
gets exactly one arrow; two inputs (-2 and 2, -1 and 1) may share an output, which a function allows."""
from pathlib import Path
import plotly.graph_objects as go
from gifkit import BLUE, FONT, GREY, ORANGE

here = Path(__file__).parent
xs = [-2, -1, 0, 1, 2, 3]
f = lambda x: x * x
fig = go.Figure()
for yv, label in ((1, "input x (domain ℝ)"), (0, "output f(x) (codomain ℝ)")):
    fig.add_shape(type="line", x0=-3, x1=10, y0=yv, y1=yv, line=dict(color=GREY, width=2))
    fig.add_annotation(x=-3, y=yv, text=label, showarrow=False, xanchor="left", yshift=26, font=dict(size=20))
for v in range(-2, 10):
    fig.add_annotation(x=v, y=1, text=str(v), showarrow=False, yshift=-20, font=dict(size=18, color=GREY)) if v <= 3 else None
    fig.add_annotation(x=v, y=0, text=str(v), showarrow=False, yshift=-20, font=dict(size=18, color=GREY))
for x in xs:
    fig.add_annotation(x=f(x), y=0.06, ax=x, ay=0.94, xref="x", yref="y", axref="x", ayref="y", arrowhead=3,
                       arrowsize=1.3, arrowwidth=3, arrowcolor=ORANGE)
fig.add_scatter(x=xs, y=[1] * len(xs), mode="markers", marker=dict(size=14, color=BLUE))
fig.add_scatter(x=sorted({f(x) for x in xs}), y=[0] * 4, mode="markers", marker=dict(size=14, color=BLUE))
fig.add_annotation(x=0.5, y=1.12, xref="paper", yref="paper", showarrow=False, font=dict(size=24),
                   text="f: x ↦ x²   (3 ↦ 9,  −2 ↦ 4,  2 ↦ 4)")
fig.update_layout(template="simple_white", width=1100, height=380, font=FONT, showlegend=False,
                  xaxis=dict(visible=False, range=[-3.2, 10.2]), yaxis=dict(visible=False, range=[-0.35, 1.35]),
                  margin=dict(l=20, r=20, t=70, b=20))
fig.write_image(here / "function_map.png", scale=2)

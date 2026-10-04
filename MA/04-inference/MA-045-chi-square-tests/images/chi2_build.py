"""Building the chi-square statistic cell by cell (Plotly frames -> GIF), for the age groups of the 60 people against
the census shares 0.25, 0.55, 0.20. Left: observed and expected counts with the gap O - E. Right: each cell's
(O - E)^2 / E stacked into the total, chi-square = 1.667 + 1.485 + 0.333 = 3.48."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from gifkit import BLUE, FONT, GREEN, GREY, ORANGE, PURPLE, make_gif

here = Path(__file__).parent
cats = ["child", "adult", "elderly"]
O, E = np.array([20, 26, 14]), 60 * np.array([0.25, 0.55, 0.20])
C = (O - E) ** 2 / E
assert np.allclose(E, [15, 33, 12]) and [round(c, 3) for c in C] == [1.667, 1.485, 0.333] and round(C.sum(), 2) == 3.48
COLS = [GREEN, ORANGE, PURPLE]


def frame(k):
    fig = make_subplots(1, 2, column_widths=[0.62, 0.38], horizontal_spacing=0.12,
                        subplot_titles=["observed O and expected E", "χ² = sum of (O − E)² / E"])
    fig.update_annotations(font_size=22)
    fig.add_trace(go.Bar(x=cats, y=O, name="observed O", marker_color=BLUE, offsetgroup=0, text=O,
                         textposition="outside", textfont=dict(size=20)), 1, 1)
    fig.add_trace(go.Bar(x=cats, y=E, name="expected E = 60 × share", marker_color=GREY, offsetgroup=1,
                         text=[f"{e:.0f}" for e in E], textposition="outside", textfont=dict(size=20)), 1, 1)
    base = 0
    for i in range(k):
        fig.add_trace(go.Bar(x=["χ²"], y=[C[i]], base=[base], marker_color=COLS[i], width=0.5, showlegend=False, offsetgroup="stack",
                             text=[f"{cats[i]}: ({O[i]} − {E[i]:.0f})² / {E[i]:.0f} = {C[i]:.3f}"], textposition="inside",
                             textfont=dict(size=15, color="white")), 1, 2)
        base += C[i]
        fig.add_annotation(x=cats[i], y=max(O[i], E[i]) + 5, text=f"gap {O[i] - E[i]:+.0f}", showarrow=False,
                           font=dict(size=20, color=COLS[i]), row=1, col=1)
    fig.add_annotation(x="χ²", y=max(base, 0.05), text=f"total {base:.2f}", showarrow=False, yshift=18,
                       font=dict(size=22), row=1, col=2)
    fig.update_yaxes(title="number of people", range=[0, 42], row=1, col=1)
    fig.update_yaxes(range=[0, 4], row=1, col=2)
    fig.update_layout(template="simple_white", width=1200, height=580, font=FONT, barmode="group",
                      legend=dict(orientation="h", x=0.3, xanchor="center", y=-0.12), margin=dict(l=70, r=30, t=60, b=110))
    return fig


if __name__ == "__main__":
    make_gif([frame(k) for k in range(4)], here / "chi2_build", fps=1, holds=[3, 2, 2, 5], keys=[3], cols=1)

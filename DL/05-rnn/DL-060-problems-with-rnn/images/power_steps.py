"""The same factor multiplied once per time step: the long-term gradient term after d steps is factor^d.
Factors from the Note: 0.72 (tanh slope 0.8 x w_h 0.9), 1.0, 1.1 and 1.5. Below 1 it vanishes, above 1 it
explodes. Plotly frames -> GIF, plus a key-frame grid for the PDF."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from common import BLUE, RED, GREEN, ORANGE, FONT
from gifkit import save_gif

HERE = Path(__file__).parent
FACTORS = [(0.72, RED, "0.72 (tanh slope 0.8 x w<sub>h</sub> 0.9)"), (1.0, GREEN, "1.0"), (1.1, ORANGE, "1.1"),
           (1.5, BLUE, "1.5")]
assert abs(0.72 ** 99 / 7.5e-15 - 1) < 0.02 and round(1.1 ** 100) == 13781 and abs(1.5 ** 100 / 4.07e17 - 1) < 0.01


def frame(d):
    fig = go.Figure()
    t = np.arange(d + 1)
    for f, c, name in FACTORS:
        fig.add_scatter(x=t, y=f ** t, mode="lines", name=f"factor {name}", line=dict(color=c, width=4))
        fig.add_scatter(x=[d], y=[f ** d], mode="markers+text", marker=dict(color=c, size=12), showlegend=False,
                        text=[f"{f ** d:.1e}" if f != 1 else "1"], textposition="middle right", textfont=dict(size=18, color=c))
    fig.add_hline(y=1, line=dict(color="black", width=1, dash="dot"))
    fig.update_layout(template="simple_white", width=1000, height=600, font=dict(FONT, size=20),
                      title=dict(text=f"after <b>{d}</b> step{'s' if d != 1 else ''}: the gradient term is multiplied by factor<sup>{d}</sup>",
                                 x=0.5, y=0.95),
                      xaxis=dict(title="steps back through time, d", range=[0, 118]),
                      yaxis=dict(type="log", title="size of the long-term term", range=[-16, 19], dtick=4,
                                 exponentformat="power"),
                      legend=dict(x=0.01, y=0.99, bgcolor="rgba(255,255,255,0.8)"), margin=dict(l=90, r=20, t=80, b=70))
    return fig


if __name__ == "__main__":
    ds = [1, 5, 10, 20, 30, 40, 50, 60, 70, 80, 90, 99]
    save_gif([frame(d) for d in ds], "power_steps", HERE, keys=[6, 11], fps=2, cols=2,
             holds=[1] * 11 + [6])

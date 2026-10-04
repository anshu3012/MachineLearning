"""Computing a . b for a = [1, 2, 3] and b = [4, 5, 6]: multiply matching components one pair at a time and keep a
running sum: 4, then 4 + 10 = 14, then 14 + 18 = 32. Plotly frames -> GIF."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from anim import save_gif, FONT, BLUE, ORANGE, GREEN

here = Path(__file__).parent
a, b = np.array([1, 2, 3]), np.array([4, 5, 6])
assert a @ b == 32


def frame(k):
    fig = go.Figure()
    for i in range(3):
        on = i < k
        for row, vec, c in ((0, a, BLUE), (1, b, ORANGE)):
            fig.add_shape(type="rect", x0=i, x1=i + 0.9, y0=2 - row, y1=2.8 - row, fillcolor=c if on else "#eeeeee",
                          opacity=1, line=dict(color="white"))
            fig.add_annotation(x=i + 0.45, y=2.4 - row, text=f"<b>{vec[i]}</b>", showarrow=False,
                               font=dict(size=30, color="white" if on else "black"))
        if on:
            fig.add_shape(type="rect", x0=i, x1=i + 0.9, y0=0, y1=0.8, fillcolor=GREEN, opacity=1, line=dict(color="white"))
            fig.add_annotation(x=i + 0.45, y=0.4, text=f"<b>{a[i] * b[i]}</b>", showarrow=False, font=dict(size=30, color="white"))
    for y, t in ((2.4, "a"), (1.4, "b"), (0.4, "a<sub>i</sub> × b<sub>i</sub>")):
        fig.add_annotation(x=-0.15, y=y, text=t, showarrow=False, xanchor="right", font=dict(size=26))
    s = int((a[:k] * b[:k]).sum())
    head = "a · b: multiply matching components, then add" if k == 0 else \
        (" + ".join(str(int(a[i] * b[i])) for i in range(k)) + f" = <b>{s}</b>" if k > 1 else f"1 × 4 = <b>4</b>")
    fig.update_layout(template="simple_white", width=900, height=480, font=FONT, title=dict(text=head, x=0.5),
                      xaxis=dict(visible=False, range=[-1.4, 3]), yaxis=dict(visible=False, range=[-0.2, 3]),
                      margin=dict(l=10, r=10, t=80, b=10))
    return fig


if __name__ == "__main__":
    save_gif([frame(k) for k in range(4)], "dot_steps", here, keys=[1, 3], fps=1, holds=[3, 3, 3, 6])

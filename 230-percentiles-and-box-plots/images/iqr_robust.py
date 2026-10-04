"""The five-number summary of the Note's ten values, and what happens when the largest value 1500 becomes 15000:
the quartiles and the IQR do not move; the maximum, the mean and the standard deviation do."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go

here = Path(__file__).parent
a = np.array([6, 213, 241, 260, 281, 290, 314, 321, 350, 1500])
b = a.copy(); b[-1] = 15000
q = lambda d: np.percentile(d, [25, 50, 75], method="weibull")
assert np.allclose(q(a), [234, 285.5, 328.25]) and np.allclose(q(b), q(a))
BLUE, RED, GREY = "#4C78A8", "#E45756", "#9a9a9a"
fig = go.Figure()
for y, d, name in ((1, a, "largest value 1500"), (0, b, "largest value 15000")):
    q1, med, q3 = q(d)
    fig.add_shape(type="rect", x0=q1, x1=q3, y0=y - 0.25, y1=y + 0.25, fillcolor="rgba(76,120,168,0.25)", opacity=1,
                  line=dict(color=BLUE, width=3))
    fig.add_shape(type="line", x0=med, x1=med, y0=y - 0.25, y1=y + 0.25, line=dict(color=BLUE, width=4))
    fig.add_scatter(x=d, y=[y] * 10, mode="markers", marker=dict(size=13, color=GREY, line=dict(color="white", width=1)),
                    showlegend=False)
    fig.add_scatter(x=[d.mean()], y=[y + 0.38], mode="markers+text", marker=dict(symbol="triangle-down", size=20, color=RED),
                    text=[f"mean {d.mean():.1f}"], textposition="top center", showlegend=False)
    fig.add_annotation(x=np.log10(6), y=y + 0.42, xanchor="left", showarrow=False, align="left",
                       text=f"<b>{name}</b><br>IQR = {q3:g} − {q1:g} = <b>{q3 - q1:g}</b><br>SD = {d.std(ddof=1):.0f}",
                       font=dict(size=20))
fig.update_layout(template="simple_white", width=1300, height=620, font=dict(family="Latin Modern Roman", size=20),
                  title=dict(text="Making the largest value ten times larger moves the mean and SD, not the box", x=0.5),
                  xaxis=dict(type="log", title="value (log scale)", range=[0.6, 4.4], tickvals=[5, 10, 50, 100, 500, 1000, 5000, 10000], ticktext=["5", "10", "50", "100", "500", "1,000", "5,000", "10,000"]),
                  yaxis=dict(visible=False, range=[-0.5, 1.95]), margin=dict(l=30, r=30, t=70, b=80))
fig.write_image(here / "iqr_robust.png", scale=2)
fig.write_image(here / "iqr_robust.pdf")

"""Which rule stays stable: a low-pass filter with time constant 0.02 s (fast next to the sample period) fed a step
of 1 and run at 10 Hz (one update every 0.1 s), one sample per frame. Grey: the continuous filter, at 0.993 by 0.1 s.
Forward Euler multiplies the remaining gap by 1 - 0.1/0.02 = -4 each sample and blows up (5, -15, 65, -255); backward
Euler divides it by 6 (0.833, 0.972, 0.995); Tustin multiplies it by -0.43 (0.714, 1.122, 0.948). Each row has its
own vertical scale. Run: python filter_stability.py -> filter_stability.gif, filter_stability_frames.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from gifkit import BLUE, FONT, GREY, PURPLE, RED, make_gif

here = Path(__file__).parent
TF, H, K = 0.02, 0.1, 4
tk = np.arange(K + 1) * H
fwd, bwd, tus = [0.0], [], []
for k in range(K + 1):
    if k < K:
        fwd.append(fwd[-1] + H / TF * (1 - fwd[-1]))                  # y[k+1] = y[k] + (h/Tf)(x[k] - y[k])
    bwd.append((TF * (bwd[-1] if bwd else 0.0) + H * 1) / (TF + H))  # y[k] = (Tf y[k-1] + h x[k]) / (Tf + h)
    x_last = 1.0 if k > 0 else 0.0
    tus.append(((2 * TF - H) * (tus[-1] if tus else 0.0) + H * (1 + x_last)) / (2 * TF + H))
fwd, bwd, tus = map(np.array, (fwd, bwd, tus))
assert np.allclose(fwd[:5], [0, 5, -15, 65, -255])
assert np.allclose(np.round(bwd[:3], 3), [0.833, 0.972, 0.995]) and np.allclose(np.round(tus[:3], 3), [0.714, 1.122, 0.948])
assert abs((1 - np.exp(-H / TF)) - 0.993) < 5e-4
tc = np.linspace(0, K * H, 801)
yc = 1 - np.exp(-tc / TF)
ROWS = [("forward Euler: the gap times −4 each sample", fwd, RED, [-290, 150], "{:.0f}"),
        ("backward Euler: the gap divided by 6", bwd, BLUE, [-0.1, 1.35], "{:.3f}"),
        ("Tustin: the gap times −0.43", tus, PURPLE, [-0.1, 1.35], "{:.3f}")]


def frame(k):
    fig = make_subplots(rows=3, cols=1, shared_xaxes=True, vertical_spacing=0.1, subplot_titles=[r[0] for r in ROWS])
    for i, (_, y, col, yr, fmt) in enumerate(ROWS, start=1):
        fig.add_trace(go.Scatter(x=tc, y=yc, mode="lines", line=dict(color=GREY, width=3)), row=i, col=1)
        fig.add_hline(y=1, line=dict(color="black", width=1, dash="dot"), row=i, col=1)
        fig.add_trace(go.Scatter(x=tk[:k + 1], y=y[:k + 1], mode="lines+markers+text", line=dict(color=col, width=3),
                                 marker=dict(color=col, size=13), text=[fmt.format(v) for v in y[:k + 1]],
                                 textposition="top right", textfont=dict(size=18, color=col)), row=i, col=1)
        fig.update_yaxes(range=yr, title="output" if i == 2 else None, row=i, col=1)
    fig.update_xaxes(range=[-0.02, K * H + 0.06], dtick=0.1, title="time (s)", row=3, col=1)
    fig.update_layout(template="simple_white", font=FONT, width=1000, height=1100, showlegend=False,
                      margin=dict(l=100, r=30, t=160, b=80),
                      title=dict(x=0.5, y=0.975, text=f"sample {k}: a filter with time constant 0.02 s run at 10 Hz"
                                                      f"<br><sup>grey: the continuous filter; each row has its own scale"
                                                      f"</sup>"))
    fig.update_annotations(font=dict(size=21))
    return fig


figs = [frame(k) for k in range(K + 1)]
make_gif(figs, here / "filter_stability", fps=1, holds=[2] + [1] * (K - 1) + [5], keys=[2, K], cols=2, width=760)

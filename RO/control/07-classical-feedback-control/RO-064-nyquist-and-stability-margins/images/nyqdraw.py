"""Shared drawing for the Nyquist tracing animations of this Note (no output when run on its own). A point walks the
Nyquist contour clockwise, part by part; its image L(s) is drawn after the radial squeeze of loopkit.squeeze (true
scale inside the dashed circle of radius 2, everything farther pulled in, infinity on the grey circle of radius 4).
A string from -1 to the moving image counts the clockwise turns round -1 so far."""
import numpy as np
import plotly.graph_objects as go

from gifkit import BLUE, FONT, GREY, ORANGE, RED
from loopkit import squeeze

PARTS = [("pos", "s = jω, ω from 0 up to ∞", 12), ("arc", "s on the large half circle", 1),
         ("neg", "s = jω, ω from −∞ up to 0", 10), ("small", "s on the small half circle round s = 0", 8)]


def contour(eps=1e-3, R=1e4, n=6000, small=True):
    w = np.logspace(np.log10(eps), np.log10(R), n)
    out = [("pos", 1j * w, w), ("arc", R * np.exp(1j * np.linspace(np.pi / 2, -np.pi / 2, n // 3)), None),
           ("neg", -1j * w[::-1], -w[::-1])]
    if small:
        out.append(("small", eps * np.exp(1j * np.linspace(-np.pi / 2, np.pi / 2, n // 3)), None))
    return out


def cw_turns(z, about=-1 + 0j):
    a = np.unwrap(np.angle(z - about))
    return -(a - a[0]) / (2 * np.pi)


def frames(L, title, small=True, extra=None):
    """Plotly figures tracing the image of the contour under L. Returns (figs, final clockwise turns)."""
    parts = contour(small=small)
    z = np.concatenate([L(p) for _, p, _ in parts])
    lab = np.concatenate([[k] * len(p) for k, p, _ in parts])
    om = np.concatenate([w if w is not None else np.full(len(p), np.nan) for _, p, w in parts])
    turns = cw_turns(z)
    zq = squeeze(z)
    stops = []
    for key, text, nfr in PARTS:
        idx = np.where(lab == key)[0]
        if len(idx) == 0:
            continue
        stops += [(int(i), text) for i in np.linspace(idx[0], idx[-1], nfr + 1)[1:].round()]
    figs = []
    a = np.linspace(0, 2 * np.pi, 361)
    for n, (i, text) in enumerate(stops):
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=2 * np.cos(a), y=2 * np.sin(a), mode="lines",
                                 line=dict(color=GREY, width=1.5, dash="dot")))
        fig.add_trace(go.Scatter(x=4 * np.cos(a), y=4 * np.sin(a), mode="lines", line=dict(color=GREY, width=2)))
        fig.add_trace(go.Scatter(x=[-4.3, 4.3], y=[0, 0], mode="lines", line=dict(color=GREY, width=1)))
        fig.add_trace(go.Scatter(x=[0, 0], y=[-4.3, 4.3], mode="lines", line=dict(color=GREY, width=1)))
        fig.add_trace(go.Scatter(x=zq.real[:i + 1], y=zq.imag[:i + 1], mode="lines", line=dict(color=BLUE, width=3.5)))
        fig.add_trace(go.Scatter(x=[-1, zq.real[i]], y=[0, zq.imag[i]], mode="lines", line=dict(color=ORANGE, width=3)))
        fig.add_trace(go.Scatter(x=[zq.real[i]], y=[zq.imag[i]], mode="markers", marker=dict(size=14, color=BLUE)))
        fig.add_trace(go.Scatter(x=[-1], y=[0], mode="markers", marker=dict(symbol="x", size=18, color=RED)))
        fig.add_annotation(x=-1, y=0, text="−1", showarrow=False, yshift=-24, font=dict(color=RED, size=20))
        if np.isnan(om[i]):
            where = text
        else:
            where = f"{text}: now ω = {om[i]:.0f} rad/s" if abs(om[i]) >= 100 else f"{text}: now ω = {om[i]:.3g} rad/s"
        count = f"string from −1: clockwise turns so far {round(turns[i], 2) + 0:+.2f}".replace("-", "−")
        head = (f"{title}<br><span style='font-size:18px;color:{GREY}'>{where.replace('-', '−')}</span>"
                f"<br><span style='font-size:20px;color:{ORANGE}'>{count}</span>")
        fig.add_annotation(x=0.5, y=-0.01, xref="paper", yref="paper", showarrow=False, yanchor="top",
                           text="true scale inside the dotted circle (radius 2); farther points pulled in;<br>"
                           "the grey circle (radius 4) is infinitely far", font=dict(size=15, color=GREY))
        if extra and n == len(stops) - 1:
            fig.add_annotation(x=0.5, y=-0.075, xref="paper", yref="paper", showarrow=False, yanchor="top",
                               text=extra, font=dict(size=21, color=RED))
        fig.update_xaxes(range=[-4.4, 4.4], visible=False)
        fig.update_yaxes(range=[-4.4, 4.4], visible=False, scaleanchor="x", scaleratio=1)
        fig.update_layout(template="simple_white", font=FONT, width=820, height=960, showlegend=False,
                          margin=dict(l=20, r=20, t=160, b=120), title=dict(x=0.5, y=0.975, text=head))
        figs.append(fig)
    return figs, turns[-1]

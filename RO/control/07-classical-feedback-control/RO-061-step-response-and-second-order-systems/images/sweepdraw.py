"""Shared drawing for the two sweep animations (no output when run on its own): left, the two roots of
s^2 + 2 zeta wn s + wn^2 = 0 in the plane of complex numbers (real part across, imaginary part up); right, the heading
step response 0 -> 0.5 rad with its overshoot and 2 percent settling time marked."""
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from gifkit import BLUE, FONT, GREEN, GREY, RED
from stepkit import TH_REF, roots, second_order, step_info

T = np.linspace(0, 10, 10001)
T_LONG = np.linspace(0, 60, 60001)                                   # the numbers are read off a longer run


def specs(wn, zeta):
    y = second_order(T, wn, zeta)
    i = step_info(T_LONG, second_order(T_LONG, wn, zeta), TH_REF, TH_REF)
    k = int(np.argmax(y >= y.max() - 1e-4))                         # the first peak inside the drawn window
    i["t_peak"], i["peak"] = T[k], y[k]
    settled = i["settle"] <= 10
    return y, i, settled


def frame(wn, zeta, title, trail=(), circle=None, xr=(-8, 1), yr=(-4.5, 4.5)):
    fig = make_subplots(rows=1, cols=2, column_widths=[0.42, 0.58], horizontal_spacing=0.1,
                        subplot_titles=["the two roots", "heading step response"])
    if circle:
        a = np.linspace(0, 2 * np.pi, 200)
        fig.add_trace(go.Scatter(x=circle * np.cos(a), y=circle * np.sin(a), mode="lines",
                                 line=dict(color=GREY, width=1.5, dash="dot")), 1, 1)
    fig.add_trace(go.Scatter(x=list(xr), y=[0, 0], mode="lines", line=dict(color="black", width=1.5)), 1, 1)
    fig.add_trace(go.Scatter(x=[0, 0], y=list(yr), mode="lines", line=dict(color="black", width=1.5)), 1, 1)
    if len(trail):
        tr = np.array(trail)
        fig.add_trace(go.Scatter(x=tr.real, y=tr.imag, mode="markers", marker=dict(color=BLUE, size=6, opacity=0.3)),
                      1, 1)
    r = roots(wn, zeta)
    fig.add_trace(go.Scatter(x=r.real, y=r.imag, mode="markers", marker=dict(symbol="x", color=RED, size=20,
                                                                           line=dict(width=2))), 1, 1)
    for z in r:
        if z.imag >= -1e-9:
            re = 0.0 if abs(z.real) < 5e-3 else z.real
            lab = f"{re:.2f} ± {abs(z.imag):.2f}j" if abs(z.imag) > 1e-9 else None
            if lab:
                fig.add_annotation(x=z.real, y=z.imag, text=lab, showarrow=False, yanchor="bottom", yshift=14,
                                   font=dict(color=RED, size=18), bgcolor="rgba(255,255,255,0.8)", row=1, col=1)
    if np.all(np.abs(r.imag) < 1e-9):
        lab = " and ".join(f"{x:.2f}" for x in sorted(set(np.round(r.real, 2)))) if abs(r[0] - r[1]) > 1e-6 \
            else f"{r[0].real:.2f} (twice)"
        fig.add_annotation(x=xr[0] + 0.2, y=yr[1] - 0.3, text=f"roots {lab}", showarrow=False, xanchor="left",
                           yanchor="top", font=dict(color=RED, size=18), row=1, col=1)
    y, i, settled = specs(wn, zeta)
    fig.add_trace(go.Scatter(x=[0, 10, 10, 0, 0], y=[0.49, 0.49, 0.51, 0.51, 0.49], fill="toself", mode="lines",
                             line=dict(width=0), fillcolor="rgba(84,162,75,0.3)"), 1, 2)
    fig.add_trace(go.Scatter(x=[0, 10], y=[TH_REF, TH_REF], mode="lines", line=dict(color=GREY, width=2, dash="dash")),
                  1, 2)
    fig.add_trace(go.Scatter(x=T, y=y, mode="lines", line=dict(color=BLUE, width=4)), 1, 2)
    if i["overshoot"] > 1e-3:
        fig.add_trace(go.Scatter(x=[i["t_peak"]], y=[i["peak"]], mode="markers", marker=dict(color=RED, size=13)), 1, 2)
        fig.add_annotation(x=i["t_peak"], y=i["peak"], text=f"overshoot {100 * i['overshoot']:.1f} %", showarrow=False,
                           xanchor="left", yanchor="bottom", xshift=8, yshift=2, font=dict(color=RED, size=19),
                           bgcolor="rgba(255,255,255,0.8)", row=1, col=2)
    else:
        fig.add_annotation(x=9.8, y=0.62, text="overshoot 0 %", showarrow=False, xanchor="right",
                           font=dict(color=RED, size=19), row=1, col=2)
    if settled:
        fig.add_trace(go.Scatter(x=[i["settle"]] * 2, y=[0, 1.05], mode="lines",
                                 line=dict(color=GREEN, width=3, dash="dot")), 1, 2)
        fig.add_annotation(x=i["settle"], y=0.15, text=f"settled {i['settle']:.2f} s", showarrow=False,
                           xanchor="left" if i["settle"] < 7 else "right", xshift=8 if i["settle"] < 7 else -8,
                           font=dict(color=GREEN, size=19), bgcolor="rgba(255,255,255,0.8)", row=1, col=2)
    else:
        fig.add_annotation(x=9.8, y=0.15, text="never settles" if zeta == 0 else f"settles only at {i['settle']:.1f} s",
                           showarrow=False, xanchor="right",
                           font=dict(color=GREEN, size=19), row=1, col=2)
    fig.update_xaxes(range=list(xr), title="real part", zeroline=False, row=1, col=1)
    fig.update_yaxes(range=list(yr), title="imaginary part", zeroline=False, scaleanchor="x", scaleratio=1, row=1, col=1)
    fig.update_xaxes(range=[0, 10], title="time t (s)", row=1, col=2)
    fig.update_yaxes(range=[0, 1.05], title="heading θ (rad)", row=1, col=2)
    fig.update_layout(template="simple_white", font=FONT, width=1250, height=640, showlegend=False,
                      margin=dict(l=70, r=30, t=140, b=70), title=dict(x=0.5, y=0.96, text=title))
    fig.update_annotations(selector=dict(showarrow=False, xref="paper"), font_size=21)
    return fig, i, settled

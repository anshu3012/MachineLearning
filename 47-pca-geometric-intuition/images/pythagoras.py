"""Why 'largest spread of the shadows' and 'line closest to the points' are the same line (Pythagoras).
The Note's 30 flats (rooms, washrooms) are centred, then a line through the origin turns. For one flat the right
triangle a (origin to flat, fixed), c (origin to shadow) and b (flat to line) is drawn. The bars on the right are
the averages of c squared and b squared over all 30 flats: they always add up to the same total, 2.66.
Plotly frames -> GIF (a chart with bars and numbers that change, so Plotly rather than Manim)."""
from pathlib import Path
import numpy as np
from plotly.subplots import make_subplots
from flats import rooms, washrooms
from anim import save_gif, FONT, BLUE, ORANGE, RED, GREY

here = Path(__file__).parent
P = np.c_[rooms, washrooms]
M = P.mean(axis=0)
Z = P - M
TOTAL = (Z ** 2).sum(axis=1).mean()
K = int(np.argmax(Z[:, 1] - Z[:, 0]))          # the flat farthest above the 45-degree line: a clear triangle
ANG = np.arange(0, 180, 0.5)
BEST = float(ANG[np.argmax([((Z @ [np.cos(np.radians(a)), np.sin(np.radians(a))]) ** 2).mean() for a in ANG])])
assert round(TOTAL, 2) == 2.66 and 44 <= BEST <= 46


def base(title, rng):
    fig = make_subplots(rows=1, cols=2, column_widths=[0.62, 0.38], horizontal_spacing=0.1)
    fig.update_layout(template="simple_white", width=1300, height=760, font=FONT, showlegend=False,
                      title=dict(text=title, x=0.5, font=dict(size=24)), margin=dict(l=70, r=30, t=80, b=70),
                      xaxis=dict(range=rng, zeroline=True, zerolinecolor="#bbbbbb"),
                      yaxis=dict(range=rng, scaleanchor="x", zeroline=True, zerolinecolor="#bbbbbb"),
                      xaxis2=dict(showticklabels=True), yaxis2=dict(range=[0, 3.3], title="average squared distance"))
    return fig


def centre_frame(t):
    """t = 0: raw data with its centre marked; t = 1: the centre moved onto the origin."""
    X = P - t * M
    fig = base("Step 1: centre the data (the shape does not change)" if t else "30 flats; the cross marks their centre",
               [-3.5, 6.2])
    fig.add_scatter(x=X[:, 0], y=X[:, 1], mode="markers", marker=dict(size=11, color=BLUE), row=1, col=1)
    c = M * (1 - t)
    fig.add_scatter(x=[c[0]], y=[c[1]], mode="markers", marker=dict(size=18, color="black", symbol="x"), row=1, col=1)
    fig.update_xaxes(title_text="rooms" + (" − mean" if t else ""), row=1, col=1)
    fig.update_yaxes(title_text="washrooms" + (" − mean" if t else ""), row=1, col=1)
    fig.update_xaxes(visible=False, row=1, col=2)
    fig.update_yaxes(visible=False, row=1, col=2)
    return fig


def frame(deg, last=False):
    u = np.array([np.cos(np.radians(deg)), np.sin(np.radians(deg))])
    s = Z @ u
    Q = np.outer(s, u)
    along, off = (s ** 2).mean(), ((Z - Q) ** 2).sum(axis=1).mean()
    fig = base(f"line at {deg:.0f}°: largest spread, smallest distance: this line is PC1" if last else
               f"Step 2: turn the line (now {deg:.0f}°), drop a shadow from every flat", [-3.6, 3.6])
    for z, q in zip(Z, Q):
        fig.add_scatter(x=[z[0], q[0]], y=[z[1], q[1]], mode="lines", line=dict(color="#c9c9c9", width=1.5, dash="dot"),
                        row=1, col=1)
    fig.add_scatter(x=[-3.4 * u[0], 3.4 * u[0]], y=[-3.4 * u[1], 3.4 * u[1]], mode="lines",
                    line=dict(color=GREY, width=2), row=1, col=1)
    fig.add_scatter(x=Z[:, 0], y=Z[:, 1], mode="markers", marker=dict(size=10, color=BLUE), row=1, col=1)
    z, q = Z[K], Q[K]
    for p0, p1, col, w in [((0, 0), z, "black", 4), ((0, 0), q, ORANGE, 6), (z, q, RED, 6)]:
        fig.add_scatter(x=[p0[0], p1[0]], y=[p0[1], p1[1]], mode="lines", line=dict(color=col, width=w), row=1, col=1)
    fig.add_scatter(x=[z[0]], y=[z[1]], mode="markers", marker=dict(size=15, color="black"), row=1, col=1)
    fig.add_annotation(x=z[0] / 2, y=z[1] / 2, text="<b>a</b>", showarrow=False, xshift=-16, yshift=12,
                       font=dict(size=24), row=1, col=1)
    fig.add_annotation(x=-3.4, y=3.35, xanchor="left", showarrow=False, font=dict(size=21), align="left", row=1, col=1,
                       text=f"one flat:  a² = <span style='color:{ORANGE}'>c²</span> + <span style='color:{RED}'>b²</span><br>"
                            f"{z @ z:.2f} = <span style='color:{ORANGE}'>{q @ q:.2f}</span> + "
                            f"<span style='color:{RED}'>{(z - q) @ (z - q):.2f}</span>")
    fig.add_bar(x=["c²: along the line<br>(spread of shadows)", "b²: flat to line<br>(distance)"], y=[along, off],
                marker_color=[ORANGE, RED], text=[f"{along:.2f}", f"{off:.2f}"], textposition="auto",
                textfont=dict(size=26), row=1, col=2)
    fig.add_hline(y=TOTAL, line=dict(color="black", dash="dash", width=2), row=1, col=2)
    fig.add_annotation(x=0.5, y=3.0, showarrow=False, font=dict(size=20), row=1, col=2,
                       text=f"dashed line: the two bars<br>always add up to {TOTAL:.2f}")
    fig.update_xaxes(title_text="rooms − mean", row=1, col=1)
    fig.update_yaxes(title_text="washrooms − mean", row=1, col=1)
    return fig


if __name__ == "__main__":
    degs = [0, 10, 20, 30, 40, BEST, 55, 70, 90, 70, 55]
    figs = [centre_frame(0), centre_frame(1)] + [frame(d) for d in degs] + [frame(BEST, True)]
    save_gif(figs, "pythagoras", here, keys=[1, 2, 10, len(figs) - 1], fps=2, holds=[3, 3] + [2] * len(degs) + [8], width=900)

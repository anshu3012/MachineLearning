"""Shared helper: a surface z = f(x, y) in 3-D whose camera tilts from a side view down to the top view, with contour
lines drawn on the surface and dropped to the floor. The last frame is the contour map used next in the Note.
Uses gifkit.make_gif. Not a figure itself."""
import numpy as np
import plotly.graph_objects as go
from gifkit import FONT, make_gif

CAMS = [0.15, 0.3, 0.45, 0.6, 0.75, 0.9, 1.0]


def tilt_gif(out, X, Y, Z, colorscale, levels, zrange, labels=("x", "y", "f"), extra=None, titles=("", "", ""),
             aspect=0.8, side_eye=(-1.25, -1.75, 1.0), tickn=5, line="#2F4B7C", opacity=1.0, reverse=False, zoom=0.7):
    """levels = (start, end, size) of the contour lines. extra(a) -> list of Scatter3d traces drawn in every frame.
    titles = (side-view title, tilting title, top-view title)."""
    xr, yr = [float(X.min()), float(X.max())], [float(Y.min()), float(Y.max())]

    def frame(a):
        top = a > 0.99
        s, e, z = levels
        fig = go.Figure(go.Surface(x=X, y=Y, z=Z, colorscale=colorscale, reversescale=reverse, cmin=zrange[0], cmax=zrange[1],
                                   showscale=False, opacity=opacity,
                                   lighting=dict(ambient=1.0, diffuse=0.05, specular=0.0, roughness=1.0, fresnel=0.0),
                                   contours=dict(z=dict(show=True, usecolormap=False, color=line, width=3, start=s, end=e, size=z,
                                                        project=dict(z=True)))))
        for t in (extra(a) if extra else []):
            fig.add_trace(t)
        k = 1 - a
        eye = dict(x=zoom * side_eye[0] * k, y=zoom * (side_eye[1] * k - 0.03 * a), z=zoom * (side_eye[2] * k + 2.4 * a))
        tick = dict(tickfont=dict(size=14), showbackground=False)
        fig.update_scenes(xaxis=dict(title=labels[0], range=xr, nticks=tickn, **tick), yaxis=dict(title=labels[1], range=yr, nticks=tickn, **tick),
                          zaxis=dict(title="" if top else labels[2], range=list(zrange), nticks=4, showticklabels=not top, **tick),
                          aspectmode="manual", aspectratio=dict(x=1, y=1, z=aspect),
                          camera=dict(eye=eye, center=dict(x=0, y=0, z=-0.15 * k), projection=dict(type="orthographic")))
        title = titles[0] if a == 0 else titles[2] if top else titles[1]
        fig.update_layout(template="simple_white", width=900, height=720, font=FONT, showlegend=False,
                          margin=dict(l=0, r=0, t=60, b=0), title=dict(text=title, x=0.5, y=0.97, font=dict(size=22)))
        return fig

    figs = [frame(0)] + [frame(a) for a in CAMS]
    holds = [12] + [2] * (len(CAMS) - 1) + [16]
    make_gif(figs, out, fps=6, holds=holds, keys=[0, 3, 5, len(figs) - 1])

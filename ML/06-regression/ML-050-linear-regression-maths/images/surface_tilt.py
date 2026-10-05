"""Tilt animation of a loss surface (Plotly): the camera starts at the side and ends looking straight down, on the
contour map. Contour lines are drawn on the surface and dropped onto the floor. Reused by the regression Notes."""
import numpy as np
import plotly.graph_objects as go

from gifkit import FONT


def surface_traces(ms, bs, Z, levels, mark=None, start=None, zfloor=None, path=None, lift=0.0):
    """Surface + contour lines on it and on the floor. mark = (m, b) of the minimum; start = (m, b) of the start."""
    zmin, zmax = float(Z.min()), float(Z.max())
    zfloor = zmin - 0.35 * (zmax - zmin) if zfloor is None else zfloor
    lo, hi, step = levels
    tr = [go.Surface(x=ms, y=bs, z=Z, colorscale="Blues", reversescale=True, showscale=False, cmin=zmin, cmax=zmax,
                     opacity=0.92, lighting=dict(ambient=0.85, diffuse=0.4),
                     contours=dict(z=dict(show=True, start=lo, end=hi, size=step, color="#1F3B5C", width=2,
                                          usecolormap=False, project=dict(z=True))))]
    if mark is not None:
        zm = float(np.interp(mark[1], bs, [Z[i, np.argmin(abs(ms - mark[0]))] for i in range(len(bs))]))
        tr.append(go.Scatter3d(x=[mark[0]] * 2, y=[mark[1]] * 2, z=[zm, zfloor], mode="lines+markers",
                               line=dict(color="black", width=4), marker=dict(size=[6, 6], symbol=["circle", "x"],
                                                                              color="black")))
    if start is not None:
        zs = float(Z[np.argmin(abs(bs - start[1])), np.argmin(abs(ms - start[0]))])
        tr.append(go.Scatter3d(x=[start[0]] * 2, y=[start[1]] * 2, z=[zs, zfloor], mode="lines+markers",
                               line=dict(color="#6B6B6B", width=4),
                               marker=dict(size=6, symbol=["circle", "square"], color="#6B6B6B")))
    if path is not None:                                    # path[:, 0] = m, path[:, 1] = b; ridden on the surface
        zp = [float(Z[np.argmin(abs(bs - q[1])), np.argmin(abs(ms - q[0]))]) + lift for q in path]
        tr.append(go.Scatter3d(x=path[:, 0], y=path[:, 1], z=zp, mode="lines+markers",
                               line=dict(color="#F58518", width=5), marker=dict(size=3, color="#F58518")))
    return tr, zfloor


def scene(ms, bs, Z, zfloor, xlab, ylab, zlab, eye, nticks=4):
    top = eye[2] > 1.7
    tf = dict(size=14)
    return dict(xaxis=dict(title=dict(text=xlab, font=dict(size=18)), range=[ms[0], ms[-1]], nticks=nticks, tickfont=tf),
                yaxis=dict(title=dict(text=ylab, font=dict(size=18)), range=[bs[0], bs[-1]], nticks=nticks, tickfont=tf),
                zaxis=dict(title=dict(text="" if top else zlab, font=dict(size=18)), range=[zfloor, float(Z.max())],
                           nticks=nticks, tickfont=tf, showticklabels=not top),
                camera=dict(projection=dict(type="orthographic"), eye=dict(x=eye[0], y=eye[1], z=eye[2]), up=dict(x=0, y=1 if eye[2] > 1.85 else 0,
                                                                          z=0 if eye[2] > 1.85 else 1)),
                aspectmode="manual", aspectratio=dict(x=1, y=1, z=0.55))


def eyes(n=9):
    """Camera path: side-on 3/4 view -> straight down. Ends at the same view as a 2D contour map (m right, b up)."""
    out = []
    for t in np.linspace(0, 1, n):
        e = t * t * (3 - 2 * t)                             # smooth
        elev = np.radians(12 + 78 * e)                      # 12 deg -> 90 deg
        az = np.radians(-60 * (1 - e) - 90 * e)
        r = 1.9
        x, y = r * np.cos(elev) * np.cos(az), r * np.cos(elev) * np.sin(az)
        if elev > np.radians(88):
            x, y = 0.0, 0.0
        out.append((x, y, r * np.sin(elev)))
    return out


def tilt_figs(ms, bs, Z, levels, xlab, ylab, zlab, mark=None, start=None, n=9, width=900, height=620, path=None, lift=0.0):
    tr, zf = surface_traces(ms, bs, Z, levels, mark, start, path=path, lift=lift)
    figs = []
    for k, eye in enumerate(eyes(n)):
        f = go.Figure(tr)
        f.update_layout(template="simple_white", width=width, height=height, showlegend=False, font=FONT,
                        scene=scene(ms, bs, Z, zf, xlab, ylab, zlab, eye), margin=dict(l=0, r=0, t=70, b=0),
                        title=dict(text=["side view: the surface", "tilting down", "tilting down", "tilting down",
                                         "tilting down", "tilting down", "almost from above", "almost from above",
                                         "top view: the contour map"][min(k, 8)] if n == 9 else "", x=0.5,
                                   font=dict(size=26)))
        figs.append(f)
    return figs

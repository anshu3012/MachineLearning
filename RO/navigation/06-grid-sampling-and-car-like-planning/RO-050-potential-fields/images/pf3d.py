"""Shared 3-D drawing for this Note's potential surfaces (no output when run on its own): the potential as a surface
over the room's floor, with contour lines every 1 unit of height, the robot as a ball on the surface and its path,
and a camera that tilts from a side view to straight above, where the surface becomes its contour map."""
import numpy as np
import plotly.graph_objects as go
import shapely

import cspace as c
from gifkit import FONT

CMAX = 15.0                                  # heights above this are cut off at this value in every 3-D figure


def ring_xy(geom):
    xs, ys = c.outline(shapely.segmentize(geom, 0.04))
    return xs, ys


def eye_at(s, r=2.3, phi0=26, alpha0=22):
    """Camera for tilt fraction s: 0 = side view from the front (low y), 1 = straight above with x to the right."""
    phi = np.radians(phi0 + (89.9 - phi0) * s)
    alpha = np.radians(alpha0 * (1 - s))
    return dict(x=r * np.sin(alpha) * np.cos(phi), y=-r * np.cos(alpha) * np.cos(phi), z=r * np.sin(phi))


def frame(xs, ys, Z, balls=(), paths=(), labels=(), s=0.0, title="", outlines=(), cmax=CMAX, zlabel="U",
          width=1000, height=720, contours=1.0, cam=(35, -160), holes=False, zaspect=0.75, r0=2.3, r1=1.55, box=1.0, notes=(), notes_x=0.01, zticks=(0, 5, 10, 15), xticks=tuple(range(8)), yticks=tuple(range(5))):
    """balls: (x, y, colour); paths: (P (n x 2), colour); labels: (x, y, text, colour) drawn on the surface;
    outlines: shapely geometries drawn as thin lines lying on the surface; cam: (height angle, turn) of the side view."""
    Zc = np.minimum(np.where(np.isfinite(Z), Z, cmax), cmax)
    Zs = np.where(np.isfinite(Z) & (Z <= cmax), Z, np.nan) if holes else Zc
    top = s > 0.97
    fig = go.Figure(go.Surface(
        x=xs, y=ys, z=Zs, colorscale="Blues", reversescale=True, cmin=0, cmax=cmax, showscale=False, opacity=1.0,
        contours=dict(z=dict(show=True, start=0, end=cmax, size=contours, color="rgba(30,30,30,0.55)", width=2)),
        lighting=dict(ambient=0.75, diffuse=0.5, specular=0.05), hoverinfo="skip"))
    from scipy.interpolate import RegularGridInterpolator
    _ri = RegularGridInterpolator((ys, xs), Zc, bounds_error=False, fill_value=None)
    interp = lambda x, y: float(_ri([[min(max(y, ys[0]), ys[-1]), min(max(x, xs[0]), xs[-1])]])[0])
    for geom in outlines:
        gx, gy = ring_xy(geom)
        gz = [interp(x, y) + 0.02 * cmax if x is not None else None for x, y in zip(gx, gy)]
        fig.add_trace(go.Scatter3d(x=gx, y=gy, z=gz, mode="lines", line=dict(color="rgba(40,40,40,0.8)", width=4)))
    for P, col in paths:
        z = [interp(x, y) + 0.01 * cmax for x, y in P]
        fig.add_trace(go.Scatter3d(x=P[:, 0], y=P[:, 1], z=z, mode="lines", line=dict(color=col, width=8)))
    for x, y, col in balls:
        fig.add_trace(go.Scatter3d(x=[x], y=[y], z=[interp(x, y) + 0.025 * cmax], mode="markers",
                                   marker=dict(size=11, color=col, line=dict(color="white", width=2))))
    for x, y, t, col in labels:
        fig.add_trace(go.Scatter3d(x=[x], y=[y], z=[interp(x, y) + 0.06 * cmax], mode="text", text=[t],
                                   textfont=dict(size=18, color=col)))
    fig.update_scenes(
        xaxis=dict(title="x (m)", range=[xs[0], xs[-1]], tickvals=list(xticks), tickfont=dict(size=15)),
        yaxis=dict(title="y (m)", range=[ys[0], ys[-1]], tickvals=list(yticks), tickfont=dict(size=15)),
        zaxis=dict(title="" if top else zlabel, range=[0, cmax * 1.03], tickvals=[] if top else list(zticks),
                   tickfont=dict(size=15), showbackground=not top),
        aspectmode="manual", aspectratio=dict(x=box * (xs[-1] - xs[0]) / 4, y=box * (ys[-1] - ys[0]) / 4, z=box * zaspect),
        domain=dict(x=[0, notes_x - 0.02] if notes_x > 0.5 else [0, 1], y=[0, 1]),
        camera=dict(eye=eye_at(s, r0 + (r1 - r0) * s, *cam), center=dict(x=0, y=0, z=-0.1), up=dict(x=0, y=0, z=1),
                    projection=dict(type="orthographic")))
    for i, (t, col) in enumerate(notes):
        fig.add_annotation(x=notes_x, y=0.9 - 0.06 * i, xref="paper", yref="paper", xanchor="left", yanchor="top", text=t,
                           showarrow=False, font=dict(size=19, color=col))
    fig.update_layout(template="simple_white", width=width, height=height, font=FONT, showlegend=False,
                      margin=dict(l=0, r=0, t=60, b=0), title=dict(text=title, x=0.5, y=0.97, font=dict(size=22)))
    return fig

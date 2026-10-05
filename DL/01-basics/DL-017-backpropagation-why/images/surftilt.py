"""Helper (no output when run): a surface z = f(x, y) whose camera tilts from a side view down to the top view.
The last frame is the top view with contour lines on the surface and dropped to the floor, i.e. the contour map
used next in the Note. Plotly frames -> GIF through gifkit.  panels: list of dicts (one per scene), keys
x, y, Z, xlab, ylab, zlab, cscale, contours, marks, reverse, zrange, title."""
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import gifkit

FONT = dict(family="Latin Modern Roman", size=22)


def eye(el, az, r=2.6):
    el, az = np.radians(el), np.radians(az)
    return dict(x=r * np.cos(el) * np.cos(az), y=r * np.cos(el) * np.sin(az), z=r * np.sin(el))


def tilt_figs(panels, nf=6, el0=14, az0=-55, zasp=0.7, size=None, floor=0.25, title=None):
    n = len(panels)
    size = size or (900 if n == 1 else 1300, 760 if n == 1 else 620)
    figs = []
    for k in range(nf):
        t = k / (nf - 1)
        t = t * t * (3 - 2 * t) if 0 < t < 1 else t
        top = t > 0.97
        cam = dict(eye=eye(el0 + (89.0 - el0) * t, az0 + (-90 - az0) * t), up=dict(x=0, y=0, z=1),
                   projection=dict(type="orthographic"))
        f = make_subplots(rows=1, cols=n, specs=[[{"type": "scene"}] * n], horizontal_spacing=0.0,
                          subplot_titles=[p.get("title", "") for p in panels] if n > 1 else None)
        for j, p in enumerate(panels, start=1):
            Z = p["Z"]
            lo, hi = (np.nanmin(Z), np.nanmax(Z)) if p.get("zrange") is None else p["zrange"]
            c = p["contours"]
            f.add_trace(go.Surface(
                x=p["x"], y=p["y"], z=Z, colorscale=p["cscale"], reversescale=p.get("reverse", False), cmin=lo, cmax=hi,
                showscale=False, hoverinfo="skip",
                contours_z=dict(show=True, usecolormap=False, color="black", project_z=True, width=2,
                                start=c["start"], end=c["end"], size=c["size"]),
                lighting=dict(ambient=1.0, diffuse=0.0, specular=0.0, roughness=1.0, fresnel=0.0)), 1, j)
            for m in p.get("marks", ()):
                f.add_trace(go.Scatter3d(
                    x=m["x"], y=m["y"], z=list(np.asarray(m["z"]) + 0.04 * (hi - lo)),
                    mode="lines+markers" if m.get("line", True) else "markers",
                    line=dict(color=m["color"], width=7),
                    marker=dict(size=m.get("size", 5), color=m["color"], symbol=m.get("symbol", "circle")),
                    showlegend=False, hoverinfo="skip"), 1, j)
            f.update_layout({f"scene{'' if j == 1 else j}": dict(
                camera=cam,
                xaxis=dict(title=dict(text=p["xlab"], font=dict(size=24)), range=[min(p["x"]), max(p["x"])], tickfont=dict(size=14)),
                yaxis=dict(title=dict(text=p["ylab"], font=dict(size=24)), range=[min(p["y"]), max(p["y"])], tickfont=dict(size=14)),
                zaxis=dict(title=dict(text="" if top else p["zlab"], font=dict(size=24)),
                           range=[lo - floor * (hi - lo), hi], tickfont=dict(size=14), showticklabels=not top),
                aspectmode="manual", aspectratio=dict(x=1, y=1, z=zasp))})
        f.update_layout(width=size[0], height=size[1], font=FONT, margin=dict(l=0, r=0, t=60 if (title or n > 1) else 0, b=0),
                        title=dict(text=title, x=0.5, font=dict(size=24)) if title else None)
        f.update_annotations(font_size=24)
        figs.append(f)
    return figs


def tilt_gif(name, here, panels, nf=6, **kw):
    """panels: one dict, or a list of dicts for side-by-side scenes."""
    figs = tilt_figs(panels if isinstance(panels, list) else [panels], nf=nf, **kw)
    gifkit.save_gif(figs, name, here, keys=[0, nf // 3, 2 * nf // 3, nf - 1], fps=1.5, width=760,
                    holds=[2] + [1] * (nf - 2) + [4])

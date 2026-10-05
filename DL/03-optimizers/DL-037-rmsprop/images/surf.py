"""Helpers for the 3D surface figures (Plotly): the grey surface with contour lines, the side-to-top camera, a GIF writer.
Imported by the figure scripts; prints nothing when run."""
import shutil
import subprocess
import numpy as np
import plotly.graph_objects as go
from PIL import Image


def data_quad(X, y):
    """Squared-error loss mean((y - X p)^2) is a quadratic: L = lmin + (p - p*)' H (p - p*). Returns (p*, H, lmin)."""
    p = np.linalg.lstsq(X, y, rcond=None)[0]
    return p, X.T @ X / len(y), float(np.mean((y - X @ p) ** 2))


def quad_surface(x, y, pstar, H, lmin, levels, zmax, lo, hi, off=0.0):
    """The TRUE loss as height (cut flat at zmax: 'the walls go higher than drawn'; the colours and lines still follow the true loss), coloured like the contour map
    (log10(L + off), cmin lo, cmax hi). Contour lines at the map's own levels (list of log10 values) are drawn on
    the surface and dropped to the floor (z = 0). Returns [surface, lines on surface, lines on floor]."""
    X, Y = np.meshgrid(x, y)
    D = np.stack([X - pstar[0], Y - pstar[1]], -1)
    Z = lmin + np.einsum("...i,ij,...j->...", D, H, D)
    surf = go.Surface(x=x, y=y, z=np.minimum(Z, zmax), surfacecolor=np.log10(Z + off), cmin=lo, cmax=hi,
                      colorscale="Greys", reversescale=True, showscale=False, opacity=1.0,
                      lighting=dict(ambient=1.0, diffuse=0.0, specular=0.0, fresnel=0.0))
    w, V = np.linalg.eigh(H)
    th = np.linspace(0, 2 * np.pi, 361)
    sx, sy, sz, fx, fy, fz = [], [], [], [], [], []
    for lv in levels:
        c = 10 ** lv - off
        if c <= lmin * 1.0001:
            continue
        r = np.sqrt((c - lmin) / w)
        p = pstar[:, None] + V @ np.vstack([r[0] * np.cos(th), r[1] * np.sin(th)])
        keep = (p[0] >= x[0]) & (p[0] <= x[-1]) & (p[1] >= y[0]) & (p[1] <= y[-1])
        px, py = np.where(keep, p[0], np.nan), np.where(keep, p[1], np.nan)
        sx += list(px) + [np.nan]; sy += list(py) + [np.nan]; sz += [min(c, zmax) + 0.006 * zmax] * len(px) + [np.nan]
        fx += list(px) + [np.nan]; fy += list(py) + [np.nan]; fz += [0.0] * len(px) + [np.nan]
    on = go.Scatter3d(x=sx, y=sy, z=sz, mode="lines", line=dict(color="#222", width=3), showlegend=False)
    floor = go.Scatter3d(x=fx, y=fy, z=fz, mode="lines", line=dict(color="#666", width=2), showlegend=False)
    return [surf, on, floor]


VALLEY_LEVELS = list(np.arange(-2, 2.2 + 1e-9, 0.3))   # the valley maps: contours of log10(L + 0.01)
BOWL_LEVELS = list(np.arange(-0.6, 2.4 + 1e-9, 0.2))   # the bowl maps: contours of log10(L)


def path3d(P, z, scene="scene", color="#E45756", width=7, size=4):
    """A path drawn on the surface (z = height of each point, lifted a little so the line stays visible)."""
    return go.Scatter3d(x=P[:, 0], y=P[:, 1], z=z + 0.4, mode="lines+markers", scene=scene, showlegend=False,
                        line=dict(color=color, width=width), marker=dict(size=size, color=color))


def star3d(x, y, z, scene="scene"):
    return go.Scatter3d(x=[x], y=[y], z=[z], mode="markers", scene=scene, showlegend=False,
                        marker=dict(symbol="diamond", size=7, color="#E45756", line=dict(color="black", width=2)))


def camera(t):
    """t = 0: side view; t = 1: straight down, w1 to the right and w2 up, like the contour map."""
    t = t * t * (3 - 2 * t)
    el, az = np.radians(26 + 63.5 * t), np.radians(-90 - 40 * (1 - t))
    r = 2.0
    return dict(eye=dict(x=r * np.cos(el) * np.cos(az), y=r * np.cos(el) * np.sin(az), z=r * np.sin(el)),
                up=dict(x=0, y=0, z=1), center=dict(x=0, y=0, z=-0.1 * (1 - t)),
                projection=dict(type="orthographic"))


def scene(xt, yt, zt, zr, aspect, t, **kw):
    top = t > 0.98                      # top view: no height axis, it would only overlap the map
    return dict(xaxis=dict(title=xt, tickangle=0, **kw.get("x", {})), yaxis=dict(title=yt, tickangle=0, **kw.get("y", {})),
                zaxis=dict(title="" if top else zt, range=zr, showticklabels=not top, **kw.get("z", {})), aspectmode="manual",
                aspectratio=dict(x=aspect[0], y=aspect[1], z=aspect[2]), camera=camera(t))


def phase(t):
    return "side view" if t < 0.02 else ("top view: this is the contour map" if t > 0.98 else "tilting towards the top view")


def gif(here, name, frame, n, hold_start, hold_end, fps, width, keys):
    """frame(k) -> figure for k = 0..n-1; writes <name>.gif and <name>_frames.png (a grid of the key frames)."""
    tmp = here / f".{name}_frames"
    tmp.mkdir(exist_ok=True)
    seq = [0] * hold_start + list(range(n)) + [n - 1] * hold_end
    cache = {}
    for i, k in enumerate(seq):
        if k not in cache:
            cache[k] = tmp / f"k{k:03d}.png"
            frame(k).write_image(cache[k])
        shutil.copy(cache[k], tmp / f"{i:03d}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(fps), "-i", str(tmp / "%03d.png"), "-vf",
                    f"scale={width}:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(here / f"{name}.gif")], check=True)
    ims = [Image.open(cache[k]).convert("RGB") for k in keys]
    w, h = ims[0].size
    sheet = Image.new("RGB", (2 * w + 16, 2 * h + 16), "white")
    for i, im in enumerate(ims):
        sheet.paste(im, ((i % 2) * (w + 16), (i // 2) * (h + 16)))
    sheet.save(here / f"{name}_frames.png")
    shutil.rmtree(tmp)


def beside(fig, traces, paths, minimum, titles, aspect, zmax, extra=640, ydom=(0.02, 0.82), xr=None, yr=None):
    """Add a still 3D view of the same surface to the right of an existing 2D figure: same colours, same contour
    levels, the paths up to the current step, the same minimum. traces = quad_surface(...); paths = [(P, L at each
    point, colour, width)]; minimum = (x, y, L). The 2D plot area keeps its size: the figure grows by `extra` pixels."""
    m = fig.layout.margin
    old = fig.layout.width - m.l - m.r
    f = old / (old + extra)
    for ax in fig.select_xaxes():
        d = ax.domain or (0, 1)
        ax.domain = [d[0] * f, d[1] * f]
    for a in fig.layout.annotations:
        if a.xref == "paper":
            a.x = a.x * f
    fig.layout.width = fig.layout.width + extra
    for t in traces:
        fig.add_trace(t)
    for P, z, c, w in paths:
        fig.add_trace(path3d(P, np.minimum(z, zmax), color=c, width=w, size=3))
    fig.add_trace(star3d(minimum[0], minimum[1], minimum[2] + 0.4))
    xt, yt = titles
    ax = lambda t, r: dict(title=dict(text=t, font=dict(size=18)), showticklabels=False, range=r)
    fig.update_layout(scene=dict(
        domain=dict(x=[f + 0.03, 1], y=list(ydom)), aspectmode="manual", aspectratio=dict(x=aspect[0], y=aspect[1], z=aspect[2]),
        xaxis=ax(xt, xr), yaxis=ax(yt, yr), zaxis=ax("loss L", [0, zmax]),
        camera=dict(eye=dict(x=1.3, y=-1.7, z=1.35), up=dict(x=0, y=0, z=1))))
    fig.add_annotation(text="the same surface in 3D (height = loss)", xref="paper", yref="paper", x=f + 0.03, xanchor="left",
                       y=ydom[1] + 0.06, showarrow=False, font=dict(size=18))
    return fig

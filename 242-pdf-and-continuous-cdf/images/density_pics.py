"""Plotly figures for the PDF Note, from the Note's own curves (CGPA = 10 x Beta(7, 3); heights = Normal(165, 10)):
PMF bars against a PDF curve (section 2); a strip at 8 shrinking, its probability going to 0 while
probability / width settles on f(8) = 0.264 (section 3, GIF + frame grid); normal, log-normal and Poisson side by
side (section 6); a tangent sliding along the heights CDF, its slope tracing the PDF (section 8, GIF + frames)."""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from PIL import Image
from scipy import stats

here = Path(__file__).parent
FONT = dict(family="Latin Modern Roman", size=20)
BLUE, ORANGE, GREEN, RED, GREY = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#6B6B6B"
LAY = dict(template="simple_white", font=FONT)
cgpa = stats.beta(7, 3, scale=10)
height = stats.norm(165, 10)
P = lambda a, b: cgpa.cdf(b) - cgpa.cdf(a)
# the Note's numbers
assert round(P(8, 9), 4) == 0.2088 and round(P(8, 8.1), 4) == 0.0261 and round(P(8, 8.01), 5) == 0.00264
assert round(P(8, 8.001), 6) == 0.000264 and round(cgpa.pdf(8), 3) == 0.264
assert round(height.pdf(165), 4) == 0.0399 and round(height.cdf(150), 3) == 0.067
assert round(height.cdf(165.5) - height.cdf(164.5), 4) == 0.0399 and round(height.pdf(150), 4) == 0.0130
assert round(height.cdf(150.5) - height.cdf(149.5), 4) == 0.0130


def save(fig, name):
    fig.write_image(here / f"{name}.png", scale=2); fig.write_image(here / f"{name}.pdf")


def grid(frames, name, picks):
    ims = [Image.open(frames[i]).convert("RGB") for i in picks]
    w, h = ims[0].size
    sheet = Image.new("RGB", (2 * w + 16, 2 * h + 16), "white")
    for i, im in enumerate(ims):
        sheet.paste(im, ((i % 2) * (w + 16), (i // 2) * (h + 16)))
    sheet.save(here / f"{name}_frames.png")


def gif(tmpdir, name, fps):
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(fps), "-i", str(tmpdir / "%03d.png"),
                    "-vf", "scale=720:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(here / f"{name}.gif")], check=True)


# Section 2: PMF (bars, heights are probabilities) against PDF (curve, height is density)
x2 = np.arange(2, 13); pmf = (6 - np.abs(x2 - 7)) / 36
xs = np.linspace(0, 10, 400)
fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.12,
                    subplot_titles=["PMF: sum of two dice", "PDF: CGPA"])
fig.add_trace(go.Bar(x=x2, y=pmf, marker_color=BLUE, showlegend=False), 1, 1)
fig.add_trace(go.Scatter(x=xs, y=cgpa.pdf(xs), mode="lines", line=dict(color=ORANGE, width=4), fill="tozeroy",
                         fillcolor="rgba(245,133,24,0.15)", showlegend=False), 1, 2)
fig.add_annotation(x=7, y=6 / 36, text="height = probability<br>P(7) = 6/36", ay=-55, ax=70, row=1, col=1)
fig.add_annotation(x=8, y=cgpa.pdf(8), text="height = density<br>f(8) = 0.264, not a probability", ay=-50, ax=-110,
                   row=1, col=2)
fig.update_xaxes(title="sum x", dtick=2, row=1, col=1); fig.update_xaxes(title="CGPA x", row=1, col=2)
fig.update_yaxes(title="probability", range=[0, 0.4], row=1, col=1)
fig.update_yaxes(title="probability density", range=[0, 0.4], row=1, col=2)
fig.update_layout(**LAY, width=1100, height=470, margin=dict(l=70, r=20, t=50, b=60))
fig.update_annotations(font=dict(family="Latin Modern Roman", size=19))
save(fig, "pmf_vs_pdf")

# Section 6: normal and log-normal are PDFs; Poisson is a PMF (illustrative parameters, not from data)
xn = np.linspace(-4, 4, 300); xl = np.linspace(0.001, 5, 300); k = np.arange(0, 11)
fig = make_subplots(rows=1, cols=3, horizontal_spacing=0.08, subplot_titles=[
    "normal, μ = 0, σ = 1", "log-normal, μ = 0, σ = 0.5", "Poisson, λ = 3 (discrete)"])
fig.add_trace(go.Scatter(x=xn, y=stats.norm.pdf(xn), line=dict(color=BLUE, width=4), fill="tozeroy",
                         showlegend=False), 1, 1)
fig.add_trace(go.Scatter(x=xl, y=stats.lognorm(0.5).pdf(xl), line=dict(color=ORANGE, width=4), fill="tozeroy",
                         showlegend=False), 1, 2)
fig.add_trace(go.Bar(x=k, y=stats.poisson(3).pmf(k), marker_color=GREEN, showlegend=False), 1, 3)
fig.update_yaxes(title="density", row=1, col=1); fig.update_yaxes(title="density", row=1, col=2)
fig.update_yaxes(title="probability", row=1, col=3)
fig.update_xaxes(title="x", row=1, col=1); fig.update_xaxes(title="x", row=1, col=2)
fig.update_xaxes(title="count k", dtick=2, row=1, col=3)
fig.update_layout(**LAY, width=1200, height=430, margin=dict(l=70, r=20, t=50, b=60))
fig.update_annotations(font=dict(family="Latin Modern Roman", size=20))
save(fig, "famous_pdfs")

# Section 3: shrink the strip [8, 8 + h]
HS = np.geomspace(1, 0.001, 19)


def strip_frame(h):
    fig = make_subplots(rows=1, cols=2, column_widths=[0.55, 0.45], horizontal_spacing=0.14,
                        subplot_titles=[f"width h = {h:.3g}", "as h shrinks"])
    fig.add_trace(go.Scatter(x=xs, y=cgpa.pdf(xs), line=dict(color=GREY, width=3), showlegend=False), 1, 1)
    xx = np.linspace(8, 8 + h, 50)
    fig.add_trace(go.Scatter(x=np.r_[8, xx, 8 + h], y=np.r_[0, cgpa.pdf(xx), 0], fill="toself", mode="lines",
                             line=dict(color=ORANGE, width=1), fillcolor="rgba(245,133,24,0.6)", showlegend=False),
                  1, 1)
    done = HS[HS >= h - 1e-15]
    fig.add_trace(go.Scatter(x=done, y=[P(8, 8 + d) for d in done], mode="lines+markers", line=dict(color=ORANGE,
                             width=4), name=f"probability P = {P(8, 8 + h):.3g}"), 1, 2)
    fig.add_trace(go.Scatter(x=done, y=[P(8, 8 + d) / d for d in done], mode="lines+markers",
                             line=dict(color=BLUE, width=4), name=f"P / h = {P(8, 8 + h) / h:.4f}"), 1, 2)
    fig.add_hline(y=cgpa.pdf(8), line=dict(color=BLUE, dash="dash", width=2), row=1, col=2, layer="above", opacity=1)
    fig.update_xaxes(title="CGPA", range=[5, 10], row=1, col=1)
    fig.update_yaxes(title="density", range=[0, 0.42], row=1, col=1)
    fig.update_xaxes(title="width h (log scale)", type="log", range=[0.1, -3.1], row=1, col=2)
    fig.update_yaxes(range=[0, 0.42], row=1, col=2)
    fig.update_layout(**LAY, width=1100, height=560, margin=dict(l=70, r=20, t=60, b=60),
                      legend=dict(x=0.66, y=0.42, yanchor="top", font=dict(size=20)))
    fig.update_annotations(font=dict(family="Latin Modern Roman", size=21))
    return fig


# Section 8: slope of the CDF equals the PDF
XT = np.arange(135, 196, 2.5)
xh = np.linspace(130, 200, 300)


def slope_frame(x0):
    s = height.pdf(x0)
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.1,
                        subplot_titles=[f"CDF: slope at {x0:g} = {s:.4f}", f"PDF: height at {x0:g} = {s:.4f}"])
    fig.add_trace(go.Scatter(x=xh, y=height.cdf(xh), line=dict(color=ORANGE, width=4), showlegend=False), 1, 1)
    t = np.array([x0 - 12, x0 + 12])
    fig.add_trace(go.Scatter(x=t, y=height.cdf(x0) + s * (t - x0), line=dict(color=RED, width=3), showlegend=False),
                  1, 1)
    fig.add_trace(go.Scatter(x=[x0], y=[height.cdf(x0)], mode="markers", marker=dict(color=RED, size=14),
                             showlegend=False), 1, 1)
    fig.add_trace(go.Scatter(x=xh, y=height.pdf(xh), line=dict(color="#DDDDDD", width=3), showlegend=False), 2, 1)
    done = xh[xh <= x0]
    fig.add_trace(go.Scatter(x=done, y=height.pdf(done), line=dict(color=BLUE, width=4), showlegend=False), 2, 1)
    fig.add_trace(go.Scatter(x=[x0], y=[s], mode="markers", marker=dict(color=RED, size=14), showlegend=False), 2, 1)
    fig.update_yaxes(title="F(x)", range=[-0.1, 1.1], row=1, col=1)
    fig.update_yaxes(title="f(x)", range=[0, 0.046], row=2, col=1)
    fig.update_xaxes(title="height (cm)", range=[130, 200], row=2, col=1)
    fig.update_layout(**LAY, width=900, height=720, margin=dict(l=80, r=20, t=60, b=60))
    fig.update_annotations(font=dict(family="Latin Modern Roman", size=22))
    return fig


if __name__ == "__main__":
    for name, maker, vals, fps, picks in (("shrink_strip", strip_frame, HS, 3, None),
                                          ("slope_is_pdf", slope_frame, XT, 4, None)):
        tmp = here / f".{name}"
        tmp.mkdir(exist_ok=True)
        files = []
        for n, v in enumerate(vals):
            maker(v).write_image(tmp / f"{n:03d}.png"); files.append(tmp / f"{n:03d}.png")
        for n in range(len(vals), len(vals) + 3 * fps):          # hold the last frame about 3 s
            shutil.copy(files[-1], tmp / f"{n:03d}.png")
        gif(tmp, name, fps)
        L = len(vals) - 1
        if name == "shrink_strip":                               # wide frames: the PDF shows the final one alone
            shutil.copy(files[-1], here / f"{name}_frames.png")
        else:
            grid(files, name, [int(np.argmin(np.abs(vals - v))) for v in (145, 150, 165, 180)])
        shutil.rmtree(tmp)

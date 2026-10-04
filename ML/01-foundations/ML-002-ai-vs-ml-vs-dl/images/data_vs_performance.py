"""Data vs performance: ML levels off, DL keeps improving. Concept curves, not measurements.
A still (png, pdf) plus Plotly frames -> ffmpeg GIF in which both curves are drawn as the amount of data grows."""
import shutil
import subprocess
from pathlib import Path
import numpy as np
import plotly.graph_objects as go

here = Path(__file__).parent
x = np.linspace(0, 10, 200)
ml = 0.62 * (1 - np.exp(-1.1 * x)) + 0.1     # rises fast, then flattens
dl = 0.9 / (1 + np.exp(-0.9 * (x - 5.2))) + 0.04  # weak on small data, keeps climbing


def draw(n=len(x)):
    """The chart with the first n points of each curve drawn."""
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x[:n], y=ml[:n], name="Machine Learning", line=dict(color="#F58518", width=5)))
    fig.add_trace(go.Scatter(x=x[:n], y=dl[:n], name="Deep Learning", line=dict(color="#54A24B", width=5)))
    fig.add_annotation(x=8.6, y=0.76, text="ML: plateaus", showarrow=False, font=dict(color="#F58518", size=18))
    fig.add_annotation(x=8.2, y=0.98, text="DL: continues to improve", showarrow=False, font=dict(color="#54A24B", size=18))
    fig.add_vrect(x0=0, x1=3, fillcolor="#6B6B6B", opacity=0.08, line_width=0)
    fig.add_annotation(x=1.5, y=0.97, text="small data:<br>ML performs better", showarrow=False, font=dict(size=16, color="#6B6B6B"))
    fig.update_layout(
        template="simple_white", width=900, height=540, font=dict(family="Latin Modern Roman", size=18),
        title=dict(text="Performance vs amount of data", x=0.5),
        xaxis=dict(title="Amount of data", showticklabels=False, ticks=""),
        yaxis=dict(title="Performance", showticklabels=False, ticks="", range=[0, 1.05]),
        legend=dict(x=0.62, y=0.3), margin=dict(l=70, r=30, t=70, b=60),
    )
    fig.add_annotation(x=10, y=0.02, xanchor="right", text="illustration, not real measurements", showarrow=False,
                       font=dict(size=13, color="#6B6B6B"))
    fig.update_xaxes(range=[0, 10])
    return fig


fig = draw()
fig.write_image(here / "data_vs_performance.png", scale=2)
fig.write_image(here / "data_vs_performance.pdf")

tmp = here / ".dp_frames"
tmp.mkdir(exist_ok=True)
steps = list(range(10, len(x) + 1, 10))
for j, n in enumerate(steps + [len(x)] * 8):
    draw(n).write_image(tmp / f"{j:03d}.png")
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "6", "-i", str(tmp / "%03d.png"), "-vf",
                "scale=760:-1:flags=lanczos,split[a][b];[a]palettegen=max_colors=64[p];[b][p]paletteuse",
                str(here / "data_vs_performance.gif")], check=True)
shutil.copy(here / "data_vs_performance.png", here / "data_vs_performance_frames.png")   # the PDF shows the full chart
shutil.rmtree(tmp)

"""Interest in neural networks, 1955 to 2020, drawn year by year (Plotly frames). The curve is a sketch of the two
booms and two winters told in the Note, not measured data; the events and their years are the Note's.
Run: python timeline_anim.py -> timeline_anim.gif, timeline_anim_frames.png (the final frame)"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from scipy.interpolate import PchipInterpolator

HERE = Path(__file__).parent
BLUE, ORANGE, PURPLE, GREY = "#4C78A8", "#F58518", "#B279A2", "#6B6B6B"
# sketch points (year, interest 0..4)
PTS = [(1955, 0.4), (1958, 2.6), (1964, 2.4), (1969, 1.3), (1973, 0.5), (1980, 0.5), (1986, 2.4), (1989, 2.9),
       (1993, 0.9), (2001, 0.6), (2006, 1.6), (2012, 3.4), (2016, 3.55), (2020, 3.65)]
curve = PchipInterpolator(*zip(*PTS))
# event: year, label, label offset in pixels (ax, ay)
EVENTS = [(1958, "1958<br>perceptron", 20, -55), (1969, "1969<br>book <i>Perceptrons</i>:<br>no XOR", 90, -100),
          (1986, "1986<br>backpropagation", -75, -50), (1989, "1989<br>zip codes read", 30, -55),
          (2006, "2006<br>deep belief nets", -70, -60), (2012, "2012<br>AlexNet", 45, 75), (2016, "2016<br>AlphaGo", 10, -55)]
WINTERS = [(1969, 1986, "first AI winter"), (1991, 2006, "second AI winter")]
assert all(curve(a + 4) < curve(a) for a, _, _ in WINTERS)       # interest falls at the start of each winter


def frame(year):
    xs = np.linspace(1955, year, 300)
    fig = go.Figure(go.Scatter(x=xs, y=curve(xs), mode="lines", line=dict(color=PURPLE, width=5)))
    for a, b, name in WINTERS:
        if year >= a:
            fig.add_vrect(x0=a, x1=min(b, year), fillcolor=BLUE, opacity=0.13, line_width=0)
            if year >= (a + b) / 2:
                fig.add_annotation(x=(a + b) / 2, y=3.95, text=name, showarrow=False, font=dict(color=BLUE, size=22))
    for yr, text, ax, ay in EVENTS:
        if year >= yr:
            fig.add_trace(go.Scatter(x=[yr], y=[float(curve(yr))], mode="markers", marker=dict(color=ORANGE, size=16)))
            fig.add_annotation(x=yr, y=float(curve(yr)), text=text, ax=ax, ay=ay, arrowcolor=GREY, arrowwidth=1.5,
                               font=dict(size=20), bgcolor="rgba(255,255,255,0.8)")
    fig.update_layout(template="simple_white", width=1100, height=600, showlegend=False,
                      font=dict(family="Latin Modern Roman", size=22), margin=dict(l=70, r=30, t=60, b=60),
                      title=dict(text=f"Interest in neural networks up to <b>{int(year)}</b>", x=0.5),
                      xaxis=dict(range=[1954, 2022], dtick=10),
                      yaxis=dict(range=[0, 4.3], title="interest (a sketch)", showticklabels=False, ticks=""))
    return fig


if __name__ == "__main__":
    tmp = HERE / ".tl_frames"
    tmp.mkdir(exist_ok=True)
    years = []
    for y in range(1955, 2021):
        years += [y] * (6 if y in [e[0] for e in EVENTS] else 1)   # pause at each event
    years += [2020] * 12
    cache = {}
    for i, y in enumerate(years):
        if y not in cache:
            cache[y] = tmp / f"y{y}.png"
            frame(y).write_image(cache[y])
        shutil.copy(cache[y], tmp / f"{i:03d}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "8", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=720:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "timeline_anim.gif")], check=True)
    frame(2020).write_image(HERE / "timeline_anim_frames.png", scale=2)
    shutil.rmtree(tmp)

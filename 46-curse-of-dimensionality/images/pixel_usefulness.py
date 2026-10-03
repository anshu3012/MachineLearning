"""One digit image next to how much each pixel varies across all 1,797 images. Edge pixels barely change."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.datasets import load_digits

here = Path(__file__).parent
d = load_digits()
std = d.data.std(axis=0).reshape(8, 8)
print("constant pixels:", int((std == 0).sum()), " pixels with std < 1:", int((std < 1).sum()))
fig = make_subplots(1, 2, subplot_titles=("One image: a handwritten 0", "How much each pixel varies<br>across all 1,797 images"),
                    horizontal_spacing=0.18)
fig.add_trace(go.Heatmap(z=d.images[0], colorscale="Greys", showscale=False), 1, 1)
fig.add_trace(go.Heatmap(z=std, colorscale="Blues", colorbar=dict(title="std", x=1.0, len=0.85),
                         text=np.round(std, 1), texttemplate="%{text}", textfont=dict(size=12)), 1, 2)
for c in (1, 2):
    fig.update_xaxes(showticklabels=False, ticks="", showline=False, constrain="domain", scaleanchor=f"y{'' if c == 1 else 2}", row=1, col=c)
    fig.update_yaxes(showticklabels=False, ticks="", showline=False, autorange="reversed", row=1, col=c)
fig.update_layout(template="simple_white", width=900, height=400, font=dict(family="Latin Modern Roman", size=17),
                  margin=dict(l=20, r=20, t=90, b=20))
fig.update_annotations(font=dict(size=18))
fig.write_image(here / "pixel_usefulness.png", scale=2)
fig.write_image(here / "pixel_usefulness.pdf")

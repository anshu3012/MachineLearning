"""The Notebook's input: MNIST 0s and 1s at 28 x 28 and shrunk to 6 x 6, the size of the small CNN's input (Plotly)."""
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from mnist_small import HERE, BIG, SMALL, Y
from common import FONT

zeros, ones = [i for i, v in enumerate(Y) if v == 0], [i for i, v in enumerate(Y) if v == 1]
idx = [zeros[0], ones[0], zeros[1], ones[1]]
assert idx[0] == 0                                            # the image of sections 6.2
assert Y[idx[0]] == 0 and Y[idx[1]] == 1 and Y[idx[2]] == 0 and Y[idx[3]] == 1
titles = []
for i in idx:
    titles.append(f"{'1' if Y[i] else '0'}: 28 × 28 (y = {int(Y[i])})")
for i in idx:
    titles.append("shrunk to 6 × 6")
fig = make_subplots(2, 4, subplot_titles=titles, vertical_spacing=0.1, horizontal_spacing=0.04)
for c, i in enumerate(idx):
    fig.add_trace(go.Heatmap(z=BIG[i][::-1], colorscale="Greys", showscale=False), row=1, col=c + 1)
    fig.add_trace(go.Heatmap(z=SMALL[i][::-1], colorscale="Greys", showscale=False, xgap=1, ygap=1), row=2, col=c + 1)
fig.update_xaxes(visible=False)
fig.update_yaxes(visible=False)
fig.update_layout(template="simple_white", width=1000, height=600, font=dict(FONT, size=18),
                  margin=dict(l=10, r=10, t=50, b=10))
fig.update_annotations(font_size=18)
fig.write_image(HERE / "digits_small.png", scale=2)
fig.write_image(HERE / "digits_small.pdf")

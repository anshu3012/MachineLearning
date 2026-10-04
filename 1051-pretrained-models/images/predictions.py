"""The eleven test photos with ResNet50's top answer and its probability (Plotly image grid)."""
from pathlib import Path
import numpy as np
import pandas as pd
from PIL import Image
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from common import FONT, GREEN, RED

here = Path(__file__).parent
data = here.parent / "data"
pred = pd.read_csv(data / "predictions.csv")
cols, n = 4, len(pred)
rows = -(-n // cols)
titles = []
for _, r in pred.iterrows():
    ok = r.photo != "tomato"
    colour = GREEN if ok else RED
    titles.append(f"<span style='color:{colour}'>{r.top1.replace('_', ' ')} {r.p1:.2f}</span><br>"
                  f"<span style='font-size:13px'>photo: {r.photo}</span>")
fig = make_subplots(rows=rows, cols=cols, subplot_titles=titles, vertical_spacing=0.09, horizontal_spacing=0.02)
for i in range(n):
    img = np.array(Image.open(data / "photos" / f"{i:02d}.jpg"))
    fig.add_trace(go.Image(z=img), row=i // cols + 1, col=i % cols + 1)
fig.update_xaxes(visible=False)
fig.update_yaxes(visible=False)
fig.update_annotations(font=dict(size=15))
fig.update_layout(template="simple_white", width=950, height=820, font=FONT, margin=dict(l=10, r=10, t=50, b=10))
fig.write_image(here / "predictions.png", scale=2)
fig.write_image(here / "predictions.pdf")

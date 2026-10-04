"""The 8,400 MNIST test images on PC1 and PC2 (2D) and on PC1 to PC3 (3D), coloured by digit (Plotly)."""
from pathlib import Path
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

here = Path(__file__).parent
d = pd.read_csv(here.parent / "data" / "test_pca3.csv")
d["digit"] = d.label.astype(str)
order = [str(i) for i in range(10)]
colours = px.colors.qualitative.T10
font = dict(family="Latin Modern Roman", size=16)
fig = px.scatter(d, x="PC1", y="PC2", color="digit", category_orders={"digit": order}, opacity=0.5,
                 color_discrete_map={str(i): colours[i] for i in range(10)}, title="MNIST test images on the first two principal components")
fig.update_traces(marker=dict(size=4))
fig.update_layout(template="simple_white", width=950, height=650, font=font, legend=dict(itemsizing="constant"),
                  title_x=0.5, margin=dict(l=70, r=20, t=60, b=60))
fig.write_image(here / "digits_2d.png", scale=2)
fig.write_image(here / "digits_2d.pdf")
sub = d[d.label.isin([0, 1, 3, 8, 7])]
fig = px.scatter_3d(sub, x="PC1", y="PC2", z="PC3", color="digit", category_orders={"digit": order}, opacity=0.6,
                    color_discrete_map={str(i): colours[i] for i in range(10)},
                    title="Digits 0, 1, 3, 7 and 8 on the first three principal components")
fig.update_traces(marker=dict(size=2.5))
fig.update_layout(template="simple_white", width=950, height=700, font=font, legend=dict(itemsizing="constant"),
                  title_x=0.5, margin=dict(l=0, r=0, t=60, b=0),
                  scene_camera=dict(eye=dict(x=1.6, y=1.4, z=0.9)))
fig.write_image(here / "digits_3d.png", scale=2)
fig.write_image(here / "digits_3d.pdf")

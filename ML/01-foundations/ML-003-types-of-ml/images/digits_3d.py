"""Handwritten digits: 64 columns reduced to 3 with PCA, coloured by digit."""
from pathlib import Path
import plotly.express as px
from sklearn.datasets import load_digits
from sklearn.decomposition import PCA

here = Path(__file__).parent


def digits_figure():
    digits = load_digits()
    xyz = PCA(n_components=3, random_state=0).fit_transform(digits.data)
    fig = px.scatter_3d(x=xyz[:, 0], y=xyz[:, 1], z=xyz[:, 2], color=digits.target.astype(str),
                        color_discrete_sequence=px.colors.qualitative.T10,
                        category_orders={"color": [str(d) for d in range(10)]},
                        labels={"x": "PC 1", "y": "PC 2", "z": "PC 3", "color": "Digit"})
    fig.update_traces(marker=dict(size=4, opacity=0.85))
    fig.update_layout(template="simple_white", font=dict(family="Latin Modern Roman", size=15),
                      title=dict(text="1,797 handwritten digits: 64 columns reduced to 3", x=0.5),
                      legend=dict(itemsizing="constant"), margin=dict(l=0, r=0, t=50, b=0))
    return fig


if __name__ == "__main__":
    fig = digits_figure()
    fig.update_layout(width=950, height=700, scene_camera=dict(eye=dict(x=1.3, y=-1.2, z=0.75)),
                      scene=dict(xaxis_showticklabels=False, yaxis_showticklabels=False, zaxis_showticklabels=False))
    fig.write_image(here / "digits_3d.png", scale=2)

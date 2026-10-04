"""One training batch as image_dataset_from_directory serves it (data/batch.npz from experiments/peek.py): 32
photos, each resized to 256 x 256 (shown smaller here), with the label taken from its folder (Cat = 0, Dog = 1).
Plotly."""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

HERE = Path(__file__).parent
D = np.load(HERE.parent / "data" / "batch.npz")
X, y = D["images"], D["labels"]
assert X.shape == (32, 80, 80, 3) and tuple(D["shape"]) == (32, 256, 256, 3)
fig = make_subplots(rows=4, cols=8, horizontal_spacing=0.01, vertical_spacing=0.06,
                    subplot_titles=[f"{'dog' if v else 'cat'} ({v})" for v in y])
for k in range(32):
    fig.add_trace(go.Image(z=X[k]), row=k // 8 + 1, col=k % 8 + 1)
fig.update_xaxes(visible=False)
fig.update_yaxes(visible=False)
fig.update_layout(template="simple_white", width=1300, height=760, font=dict(family="Latin Modern Roman", size=16),
                  title=dict(text="One batch: a tensor of shape (32, 256, 256, 3) and 32 labels", x=0.5,
                             font=dict(size=22)),
                  margin=dict(l=10, r=10, t=80, b=10))
fig.write_image(HERE / "batch.png", scale=2)
print(int(y.sum()), "dogs of 32")

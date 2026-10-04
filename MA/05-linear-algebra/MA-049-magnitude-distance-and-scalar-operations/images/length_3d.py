"""The length of the 3D vector [2, 3, 6] by Pythagoras twice: the floor diagonal of [2, 3] has length sqrt(13);
that diagonal and the height 6 are the legs of a second right triangle whose hypotenuse is sqrt(13 + 36) = 7."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go

here = Path(__file__).parent
v = np.array([2, 3, 6])
assert np.linalg.norm(v) == 7 and np.isclose(np.linalg.norm(v[:2]), np.sqrt(13))
fig = go.Figure()
fig.add_scatter3d(x=[0, 2, 2], y=[0, 0, 3], z=[0, 0, 0], mode="lines", line=dict(color="#9a9a9a", width=6, dash="dash"),
                  name="legs 2 and 3")
fig.add_scatter3d(x=[0, 2], y=[0, 3], z=[0, 0], mode="lines", line=dict(color="#54A24B", width=9), name="floor diagonal √13")
fig.add_scatter3d(x=[2, 2], y=[3, 3], z=[0, 6], mode="lines", line=dict(color="#F58518", width=9), name="height 6")
fig.add_scatter3d(x=[0, 2], y=[0, 3], z=[0, 6], mode="lines+markers", line=dict(color="#4C78A8", width=12),
                  marker=dict(size=[0, 8], color="#4C78A8"), name="[2, 3, 6]: length √(13 + 36) = 7")
fig.update_layout(width=1000, height=760, font=dict(family="Latin Modern Roman", size=19),
                  title=dict(text="‖[2, 3, 6]‖ = √(2² + 3² + 6²) = √49 = 7", x=0.5),
                  scene=dict(xaxis=dict(title="x₁", range=[0, 4], dtick=1, tickfont=dict(size=14)),
                             yaxis=dict(title="x₂", range=[0, 4], dtick=1, tickfont=dict(size=14)),
                             zaxis=dict(title="x₃", range=[0, 7], dtick=1, tickfont=dict(size=14)), aspectmode="manual", aspectratio=dict(x=1, y=1, z=1.4),
                             camera=dict(eye=dict(x=1.7, y=-1.6, z=0.9))),
                  legend=dict(x=0.0, y=0.95), margin=dict(l=0, r=0, t=60, b=0))
fig.write_image(here / "length_3d.png", scale=2)

"""What freezing does to the trainable parameter count of the VGG16 + new top model (counts from the Notebook,
checked against the dense-layer and convolution-layer formulas) (Plotly)."""
from pathlib import Path
import plotly.graph_objects as go
from common import BLUE, GREEN, GREY, FONT

here = Path(__file__).parent
TOTAL, TOP, BLOCK5_ON = 16_812_353, 2_097_665, 9_177_089
assert TOP == (4 * 4 * 512 + 1) * 256 + (256 + 1) * 1                      # Flatten 8,192 -> 256 -> 1
assert BLOCK5_ON - TOP == 3 * (3 * 3 * 512 * 512 + 512)                     # block 5: three 3x3 conv, 512 -> 512
assert TOTAL - TOP == 14_714_688                                            # the VGG16 base (section 4.1)
rows = [("whole model, nothing frozen", TOTAL, BLUE), ("block 5 unfrozen (fine-tuning)", BLOCK5_ON, GREEN),
        ("base frozen (feature extraction)", TOP, GREY)]
fig = go.Figure(go.Bar(y=[r[0] for r in rows], x=[r[1] / 1e6 for r in rows], orientation="h",
                       marker_color=[r[2] for r in rows], text=[f"{r[1]:,}" for r in rows], textposition="outside",
                       textfont=dict(size=18)))
fig.update_layout(template="simple_white", width=950, height=380, font=dict(FONT, size=18),
                  xaxis=dict(title="trainable parameters (millions)", range=[0, 21]),
                  margin=dict(l=20, r=20, t=20, b=60))
fig.write_image(here / "param_counts.png", scale=2)
fig.write_image(here / "param_counts.pdf")

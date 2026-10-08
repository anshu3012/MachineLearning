"""One bell holds one side. The same 16 readings fed to two EKFs: one started at the dock (0 m), one started at 11 m,
the mirror image of the start across the beacon. Both explain the readings, so the second follows the mirror path
with a narrow band, wrong by up to 10.5 m, until the robot passes the beacon. Run: python mirror.py -> mirror.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from gifkit import BLUE, FONT, RED
from ekfsim import X_TRUE, ekf

here = Path(__file__).parent
t = np.arange(1, 17)
fig = go.Figure()
fig.add_trace(go.Scatter(x=t, y=X_TRUE, mode="lines+markers", line=dict(color="black", width=3), name="true"))
for x0, c, name in ((0.0, BLUE, "EKF started at 0 m"), (11.0, RED, "EKF started at 11 m")):
    rows = ekf(x=x0)
    x = np.array([r["x"] for r in rows]); sd = np.sqrt([r["p"] for r in rows])
    fig.add_trace(go.Scatter(x=t, y=x, mode="lines+markers", line=dict(color=c, width=3), name=name,
                             error_y=dict(type="data", array=2 * sd, color=c, thickness=1.5)))
    print(name, np.round(x, 2))
fig.add_hline(y=6, line=dict(color="grey", dash="dot"))
fig.update_layout(template="simple_white", font=FONT, width=1000, height=540, margin=dict(l=90, r=30, t=30, b=70),
                  legend=dict(x=0.65, y=0.99, font=dict(size=17)),
                  xaxis=dict(title="step", dtick=1), yaxis=dict(title="position (m)", range=[0, 12.5]))
fig.write_image(here / "mirror.png")

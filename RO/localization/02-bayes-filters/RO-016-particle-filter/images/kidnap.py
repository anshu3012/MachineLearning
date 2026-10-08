"""The kidnapped robot: after step 30 the robot is moved 5 m without the filter being told. Average error of the
estimate over 200 runs (200 particles each), without and with 5 percent random particles added after every
resampling. Run: python kidnap.py -> kidnap.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from gifkit import BLUE, FONT, RED
from pfsim import kidnap_run

here = Path(__file__).parent
fig = go.Figure()
for inject, c, name in ((0.0, RED, "no random particles"), (0.05, BLUE, "5 percent random particles")):
    E = np.array([kidnap_run(inject, s) for s in range(200)])
    print(name, "error steps 25-29:", E[:, 25:30].mean().round(3), "recovered at step 59:", np.mean(E[:, 59] < 0.5))
    fig.add_trace(go.Scatter(x=np.arange(E.shape[1]), y=E.mean(0), mode="lines", line=dict(color=c, width=4), name=name))
fig.add_vline(x=30, line=dict(color="black", dash="dash", width=2))
fig.add_annotation(x=30.5, y=5.15, text="robot kidnapped: moved 5 m", showarrow=False, xanchor="left", font=dict(size=18))
fig.update_layout(template="simple_white", font=FONT, width=1000, height=520, margin=dict(l=90, r=30, t=60, b=70),
                  legend=dict(x=0.02, y=0.75, font=dict(size=18)),
                  xaxis=dict(title="step (0.5 m driven per step)"), yaxis=dict(title="average error (m)", range=[0, 5.3]))
fig.write_image(here / "kidnap.png")

"""Particle deprivation: with too few particles the filter often ends at the wrong door. For each particle count,
1000 runs of the three-reading example; a run succeeds if most particles end within 0.8 m of door 3's centre.
Run: python deprivation.py -> deprivation.png"""
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from gifkit import BLUE, FONT
from pfsim import run

here = Path(__file__).parent
rng = np.random.default_rng(1)
Ms = [5, 10, 20, 50, 100]
rate = []
for M in Ms:
    ok = [np.mean(np.abs(run(M, rng)[-1][1] - 7.0) < 0.8) > 0.5 for _ in range(1000)]
    rate.append(100 * np.mean(ok))
print(dict(zip(Ms, rate)))
fig = go.Figure(go.Bar(x=[str(m) for m in Ms], y=rate, marker_color=BLUE, text=[f"{r:.1f} percent" for r in rate],
                       textposition="outside", textfont=dict(size=19)))
fig.update_layout(template="simple_white", font=FONT, width=900, height=500, margin=dict(l=90, r=30, t=70, b=70),
                  title=dict(x=0.5, text="runs that end at the right door (1000 runs each)"),
                  xaxis=dict(title="number of particles M"), yaxis=dict(title="percent of runs", range=[0, 115]))
fig.write_image(here / "deprivation.png")

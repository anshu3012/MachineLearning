"""Three base regressors (dash-dot) and the voting regressor (solid) on the noisy sine data (Plotly)."""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent))
from app import figure, run          # same data and models as the app

results = run(["linear regression", "SVR", "decision tree"])
print([(n, round(r, 2), round(m, 2)) for n, _, r, m in results])
fig = figure(results)
fig.update_layout(width=1100, height=700, font=dict(family="Latin Modern Roman", size=21),
                  legend=dict(orientation="h", x=0.5, xanchor="center", y=-0.14, font_size=20),
                  margin=dict(l=70, r=20, t=20, b=170))
fig.write_image(HERE / "voting_fit.png", scale=2)
fig.write_image(HERE / "voting_fit.pdf")

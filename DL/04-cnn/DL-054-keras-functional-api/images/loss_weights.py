"""Section 5.3's worked example as bars: the total loss of the two-output model with and without the 0.1 weight on age.
Values from the example in the text (age error 9 years, gender loss 0.30). Plotly."""
from pathlib import Path
import plotly.graph_objects as go
from common import BLUE, RED

here = Path(__file__).parent
FONT = dict(family="Latin Modern Roman", size=20)
AGE, GENDER = 9.0, 0.30
rows = [("no weights<br>1.0 x age + 1.0 x gender", 1.0), ("loss weights<br>0.1 x age + 1.0 x gender", 0.1)]
totals = [w * AGE + GENDER for _, w in rows]
assert [round(t, 2) for t in totals] == [9.3, 1.2]
fig = go.Figure()
fig.add_bar(y=[r[0] for r in rows], x=[w * AGE for _, w in rows], orientation="h", name="age part (years)",
            marker_color=BLUE, text=[f"{w * AGE:.1f}" for _, w in rows], textposition="inside", insidetextanchor="middle")
fig.add_bar(y=[r[0] for r in rows], x=[GENDER] * 2, orientation="h", name="gender part", marker_color=RED,
            text=["0.3"] * 2, textposition="outside")
for (lab, _), t in zip(rows, totals):
    fig.add_annotation(y=lab, x=t + 0.9, text=f"total {t:.1f}", showarrow=False, xanchor="left", font=dict(size=20))
fig.update_layout(barmode="stack", template="simple_white", width=1000, height=380, font=FONT,
                  xaxis=dict(title="contribution to the total loss L", range=[0, 12.5]),
                  legend=dict(orientation="h", x=0.5, xanchor="center", y=1.15), margin=dict(l=20, r=20, t=50, b=60))
fig.write_image(here / "loss_weights.png", scale=2)
fig.write_image(here / "loss_weights.pdf")

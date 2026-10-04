"""Five new-style lessons against the old 6-minute mean (Plotly): the sample mean is 9, but is that more than chance?"""
from pathlib import Path
import plotly.graph_objects as go

here = Path(__file__).parent
minutes = [7, 9, 5, 11, 13]          # the five new-style lessons from the Note
mean = sum(minutes) / len(minutes)    # 9
fig = go.Figure()
fig.add_hline(y=6, line=dict(color="#6B6B6B", dash="dash", width=3), layer="above", opacity=1)
fig.add_hline(y=mean, line=dict(color="#F58518", width=3), layer="above", opacity=1)
fig.add_trace(go.Bar(x=[f"lesson {i}" for i in range(1, 6)], y=minutes, marker_color="#4C78A8", opacity=0.6, width=0.55,
                     text=[f"{m}" for m in minutes], textposition="outside", textfont=dict(size=22)))
fig.add_annotation(xref="paper", x=1.0, y=6, text="old style: 6", showarrow=False, xanchor="left", xshift=8,
                   font=dict(size=22, color="#6B6B6B"), bgcolor="white")
fig.add_annotation(xref="paper", x=1.0, y=mean, text="sample mean: 9", showarrow=False, xanchor="left", xshift=8,
                   font=dict(size=22, color="#F58518"), bgcolor="white")
fig.update_yaxes(title="mean view duration (minutes)", range=[0, 15.5], dtick=3)
fig.update_layout(template="simple_white", width=1000, height=520, showlegend=False,
                  title=dict(text="9 is above 6. Real effect, or chance?", x=0.5, font=dict(size=26)),
                  font=dict(family="Latin Modern Roman", size=20), margin=dict(l=80, r=190, t=70, b=50))
fig.write_image(here / "lessons.png", scale=2); fig.write_image(here / "lessons.pdf")

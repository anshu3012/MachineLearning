"""When the independence assumption fails: copying the 'toss' column k times on the 8-match data (Plotly).
Each copy multiplies the scores again, so the posterior becomes more and more extreme."""
from pathlib import Path
import plotly.graph_objects as go

here = Path(__file__).parent
ks = [1, 2, 3, 4, 5]
p_loss = []
for k in ks:
    win = 5 / 8 * (1 / 5) ** k * 2 / 5 * 4 / 5
    loss = 3 / 8 * (2 / 3) ** k * 2 / 3 * 1 / 3
    p_loss.append(loss / (win + loss))
print([round(p, 3) for p in p_loss])
fig = go.Figure(go.Bar(x=[f"{k} cop{'y' if k == 1 else 'ies'}" for k in ks], y=p_loss, marker_color="#E45756",
                       text=[f"{p:.1%}" for p in p_loss], textposition="outside"))
fig.update_layout(template="simple_white", width=900, height=420, font=dict(family="Latin Modern Roman", size=16),
                  margin=dict(l=60, r=20, t=50, b=60), yaxis=dict(range=[0, 1.1], title="P(loss | lost, Mumbai, sunny)"),
                  xaxis=dict(title="number of identical 'toss' columns"),
                  title=dict(text="The same information counted again and again makes Naive Bayes over-confident", x=0.5))
fig.write_image(here / "duplicate.png", scale=2); fig.write_image(here / "duplicate.pdf")

"""The complement rule on two tosses: "at least one head" = {HH, HT, TH} and its complement "no heads" = {TT};
P(at least one head) = 1 - P(TT) = 1 - 1/4 = 3/4."""
from pathlib import Path
import plotly.graph_objects as go

here = Path(__file__).parent
S = ["HH", "HT", "TH", "TT"]
A = [s for s in S if "H" in s]
assert len(A) == 3 and 1 - 1 / 4 == 3 / 4
fig = go.Figure()
for i, s in enumerate(S):
    c = "#F58518" if s in A else "#4C78A8"
    fig.add_shape(type="rect", x0=i + 0.08, x1=i + 0.92, y0=0, y1=1, fillcolor=c, opacity=1, line=dict(color="white"))
    fig.add_annotation(x=i + 0.5, y=0.5, text=f"<b>{s}</b>", showarrow=False, font=dict(size=34, color="white"))
fig.add_annotation(x=1.5, y=1.25, text="A = at least one head: 3 of 4 outcomes", showarrow=False, font=dict(size=22, color="#c55a00"))
fig.add_annotation(x=3.5, y=-0.25, text="A<sup>c</sup> = no heads: 1 of 4", showarrow=False, font=dict(size=22, color="#4C78A8"))
fig.update_layout(template="simple_white", width=1000, height=360, font=dict(family="Latin Modern Roman", size=20),
                  title=dict(text="P(A) = 1 − P(A<sup>c</sup>) = 1 − 1/4 = 3/4", x=0.5),
                  xaxis=dict(visible=False, range=[-0.1, 4.1]), yaxis=dict(visible=False, range=[-0.5, 1.5]),
                  margin=dict(l=20, r=20, t=70, b=10))
fig.write_image(here / "complement.png", scale=2)
fig.write_image(here / "complement.pdf")

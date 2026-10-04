"""Reading four probabilities off the students' probability table (section 3.3): the cells that make up each one are
shaded: P(Maths and Bio) = 0.10, P(Maths) = 0.40, P(Maths or Bio) = 0.80, P(neither) = 0.20."""
from pathlib import Path
import plotly.graph_objects as go
from plotly.subplots import make_subplots

here = Path(__file__).parent
P = [[0.10, 0.30], [0.40, 0.20]]                     # rows Maths / not Maths, cols Bio / not Bio
READS = [("P(Maths ∩ Bio) = 0.10", [(0, 0)]), ("P(Maths) = 0.10 + 0.30 = 0.40", [(0, 0), (0, 1)]),
         ("P(Maths ∪ Bio) = 0.10 + 0.30 + 0.40 = 0.80", [(0, 0), (0, 1), (1, 0)]), ("P(neither) = 0.20", [(1, 1)])]
assert abs(sum(P[i][j] for i, j in READS[2][1]) - 0.80) < 1e-12 and abs(sum(map(sum, P)) - 1) < 1e-12
fig = make_subplots(rows=1, cols=4, subplot_titles=[t for t, _ in READS], horizontal_spacing=0.05)
for k, (_, cells) in enumerate(READS, start=1):
    for i, r in enumerate(["Maths", "not Maths"]):
        for j, c in enumerate(["Bio", "not Bio"]):
            on = (i, j) in cells
            fig.add_shape(type="rect", x0=j, x1=j + 0.95, y0=1 - i, y1=1.95 - i, fillcolor="#F58518" if on else "#f4f4f4", opacity=1,
                          line=dict(color="white"), row=1, col=k)
            fig.add_annotation(x=j + 0.475, y=1.475 - i, text=f"{P[i][j]:.2f}", showarrow=False,
                               font=dict(size=24, color="white" if on else "black"), row=1, col=k)
    fig.update_xaxes(range=[-0.05, 2], tickvals=[0.475, 1.475], ticktext=["Bio", "not Bio"], showline=False, row=1, col=k)
    fig.update_yaxes(range=[-0.05, 2], tickvals=[1.475, 0.475], ticktext=["Maths", "not Maths"] if k == 1 else ["", ""],
                     showline=False, row=1, col=k)
for a in fig.layout.annotations[:4]:
    a.font.size = 18
fig.update_layout(template="simple_white", width=1600, height=420, font=dict(family="Latin Modern Roman", size=18),
                  showlegend=False, margin=dict(l=110, r=20, t=60, b=40))
fig.write_image(here / "table_reads.png", scale=2)
fig.write_image(here / "table_reads.pdf")

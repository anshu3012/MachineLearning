"""Three Bernoulli PMFs: a bar at 0 of height 1 - p and a bar at 1 of height p."""
from pathlib import Path
from plotly.subplots import make_subplots

here = Path(__file__).parent
COLOURS = {0.2: "#E45756", 0.5: "#54A24B", 0.8: "#4C78A8"}
fig = make_subplots(rows=1, cols=3, shared_yaxes=True, horizontal_spacing=0.06,
                    subplot_titles=[f"p = {p}" for p in COLOURS])
for i, (p, colour) in enumerate(COLOURS.items(), start=1):
    fig.add_bar(x=[0, 1], y=[1 - p, p], marker_color=colour, width=0.45, text=[f"{1 - p:.1f}", f"{p:.1f}"],
                textposition="outside", textfont_size=18, row=1, col=i)
    fig.update_xaxes(tickvals=[0, 1], ticktext=["0 (failure)", "1 (success)"], range=[-0.6, 1.6], row=1, col=i)
fig.update_yaxes(range=[0, 1.05], title_text="P(X = x)", row=1, col=1)
fig.update_annotations(font_size=20)
fig.update_layout(template="simple_white", width=1000, height=380, showlegend=False,
                  font=dict(family="Latin Modern Roman", size=17), margin=dict(l=70, r=20, t=40, b=40))
fig.write_image(here / "bernoulli_pmf.png", scale=2)
fig.write_image(here / "bernoulli_pmf.pdf")

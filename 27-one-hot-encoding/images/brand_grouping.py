"""Grouping rare brands: the 32 brands of the car data, then the 13 columns left after replacing every brand with
100 cars or fewer by 'uncommon' (538 cars). Plotly frames -> GIF."""
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go
from anim import save_gif, FONT, BLUE, RED

here = Path(__file__).parent
brand = pd.read_csv(here.parent / "data" / "cars.csv")["brand"]
counts = brand.value_counts()
rare = counts[counts <= 100].index
after = brand.replace(rare, "uncommon").value_counts()
assert len(counts) == 32 and len(rare) == 20 and len(after) == 13 and after["uncommon"] == 538


def frame(c, head, colour):
    fig = go.Figure(go.Bar(x=c.index, y=c.values, marker_color=colour, text=c.values, textposition="outside",
                           textfont=dict(size=13), cliponaxis=False))
    fig.add_hline(y=100, line=dict(color="#6B6B6B", dash="dash"))
    fig.update_layout(template="simple_white", width=1200, height=560, font=dict(family="Latin Modern Roman", size=17),
                      title=dict(text=head, x=0.5), xaxis=dict(tickangle=-60),
                      yaxis=dict(title="cars", range=[0, 2650]), margin=dict(l=70, r=20, t=70, b=130))
    return fig


if __name__ == "__main__":
    f1 = frame(counts, "<b>32 brands</b>: red brands have 100 cars or fewer", [BLUE if v > 100 else RED for v in counts])
    f2 = frame(after, "<b>13 columns</b> after grouping: 12 brands + uncommon (538 cars)",
               [RED if i == "uncommon" else BLUE for i in after.index])
    save_gif([f1, f2], "brand_grouping", here, keys=[0, 1], fps=1, holds=[4, 6], cols=1, width=900)

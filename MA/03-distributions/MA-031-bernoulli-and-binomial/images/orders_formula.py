"""Where each piece of the binomial formula comes from: the three orders in which 2 of 3 viewers can like a post.
Each order is a row of three tiles (L = like, N = no like) whose probabilities are multiplied; the three rows are
added; then the formula's pieces are matched to the picture. Last frame: the same three rows with p = 0.1.
Plotly frames (a step-by-step build of tiles and numbers) -> orders_formula.gif, _frames.png"""
from pathlib import Path
import plotly.graph_objects as go
from scipy import stats
from anim import save_gif, FONT, BLUE, ORANGE, GREEN

here = Path(__file__).parent
ORDERS = ["LLN", "LNL", "NLL"]


def frame(title, rows, p=0.5, total=False, formula=False):
    one = p * p * (1 - p)
    assert abs(3 * one - stats.binom.pmf(2, 3, p)) < 1e-12
    fig = go.Figure()
    for r, order in enumerate(ORDERS[:rows]):
        y = 3 - r
        for c, ch in enumerate(order):
            col = BLUE if ch == "L" else ORANGE
            fig.add_shape(type="rect", x0=c + 0.08, x1=c + 0.92, y0=y - 0.4, y1=y + 0.4, fillcolor=col, line_width=0, opacity=1, layer="below")
            fig.add_annotation(x=c + 0.5, y=y, showarrow=False, font=dict(size=30, color="white"),
                               text=f"<b>{ch}</b> {p if ch == 'L' else round(1 - p, 2):g}")
        fig.add_annotation(x=3.15, y=y, showarrow=False, xanchor="left", font_size=28, text=f"product = {one:g}")
    fig.add_annotation(x=1.5, y=3.75, showarrow=False, font_size=22, text="viewer 1 · viewer 2 · viewer 3")
    if total:
        fig.add_annotation(x=3.15, y=0.15, showarrow=False, xanchor="left", font_size=30,
                           text=f"<b>sum = 3 × {one:g} = {3 * one:g}</b>")
    if formula:
        fig.add_annotation(x=0, y=0.15, showarrow=False, xanchor="left", font_size=30,
                           text=f"<span style='color:{GREEN}'><b>3 rows</b></span> × "
                                f"<span style='color:{BLUE}'><b>{p:g}²</b></span> × "
                                f"<span style='color:{ORANGE}'><b>{round(1 - p, 2):g}¹</b></span>")
        fig.add_annotation(x=0, y=-0.55, showarrow=False, xanchor="left", font_size=22,
                           text=f"<span style='color:{GREEN}'>3 choose 2: the orders</span> · "
                                f"<span style='color:{BLUE}'>p<sup>x</sup>: the 2 likes</span> · "
                                f"<span style='color:{ORANGE}'>(1 − p)<sup>n − x</sup>: the 1 no-like</span>")
    fig.update_layout(template="simple_white", width=1100, height=700, font=FONT, title=dict(text=title, x=0.5),
                      xaxis=dict(visible=False, range=[-0.1, 5.6]), yaxis=dict(visible=False, range=[-1, 4.1]),
                      margin=dict(l=20, r=20, t=90, b=20))
    return fig


if __name__ == "__main__":
    figs = [frame("<b>One order</b>: multiply along the row", 1),
            frame("<b>Three orders</b>: the no-like can be 3rd, 2nd or 1st", 3),
            frame("<b>Add the rows</b>: any 2 likes out of 3", 3, total=True),
            frame("<b>The formula is this count</b>", 3, total=True, formula=True),
            frame("<b>Same rows, p = 0.1</b>: only the tiles change", 3, p=0.1, total=True, formula=True)]
    save_gif(figs, "orders_formula", here, keys=[0, 2, 3, 4], fps=1, holds=[3, 3, 3, 5, 6])

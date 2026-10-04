"""The addition rule by counting (Plotly frames -> GIF): a bag of 29 objects, 5 yellow cubes, 7 yellow spheres,
8 green cubes and 9 green spheres. "Yellow" (12) and "cube" (13) share the 5 yellow cubes, so 12 + 13 counts them
twice; subtracting the 5 gives 20 of 29. "Yellow sphere" (7) and "green cube" (8) share nothing (mutually exclusive),
so the counts simply add: 15 of 29."""
from pathlib import Path
import plotly.graph_objects as go
from gifkit import BLUE, FONT, GREEN, RED, make_gif

here = Path(__file__).parent
YEL = "#E3B505"
# (colour, shape, count, x0, y0): yellow on the top row, cubes in the left block; 5 objects per line
GROUPS = [("yellow", "cube", 5, 0, 3), ("yellow", "sphere", 7, 7, 3), ("green", "cube", 8, 0, 0), ("green", "sphere", 9, 7, 0)]
OBJ = [(c, s, x0 + i % 5, y0 - i // 5) for c, s, n, x0, y0 in GROUPS for i in range(n)]
n_y = sum(c == "yellow" for c, *_ in OBJ); n_c = sum(s == "cube" for _, s, *_ in OBJ); n_yc = sum(c == "yellow" and s == "cube" for c, s, *_ in OBJ)
assert (len(OBJ), n_y, n_c, n_yc, n_y + n_c - n_yc) == (29, 12, 13, 5, 20)


def frame(title, lit, twice=lambda c, s: False, boxes=()):
    fig = go.Figure()
    for c, s, x, y in OBJ:
        on = lit(c, s)
        fig.add_trace(go.Scatter(x=[x], y=[y], mode="markers", showlegend=False, opacity=1 if on else 0.18,
                                 marker=dict(size=34, symbol="square" if s == "cube" else "circle", color=YEL if c == "yellow" else GREEN,
                                             line=dict(color=RED if twice(c, s) else "black", width=5 if twice(c, s) else 1.5))))
    for x0, x1, y0, y1, col, text, tx, ty in boxes:
        fig.add_shape(type="rect", x0=x0, x1=x1, y0=y0, y1=y1, fillcolor="rgba(0,0,0,0)", opacity=1, line=dict(color=col, width=4, dash="dash"))
        fig.add_annotation(x=tx, y=ty, text=text, showarrow=False, font=dict(size=22, color=col))
    fig.add_annotation(x=2, y=-2.9, text="cubes", showarrow=False, font=dict(size=20))
    fig.add_annotation(x=9, y=-2.9, text="spheres", showarrow=False, font=dict(size=20))
    fig.update_xaxes(visible=False, range=[-1.2, 12.2])
    fig.update_yaxes(visible=False, range=[-3.4, 5.2], scaleanchor="x")
    fig.update_layout(template="simple_white", width=1000, height=690, font=FONT, margin=dict(l=20, r=20, t=90, b=20),
                      title=dict(text=title, x=0.5, font=dict(size=26)))
    return fig


yel_box = (-0.7, 11.7, 1.4, 3.6, "#9A7B00", "yellow: 12", 5.5, 4.1)
cube_box = (-0.6, 4.6, -1.6, 3.5, BLUE, "cubes: 13", 2, -2.1)
figs = [
    frame("A bag of 29 objects", lambda c, s: True),
    frame("Yellow: 12 of 29", lambda c, s: c == "yellow", boxes=[yel_box]),
    frame("Cube: 13 of 29", lambda c, s: s == "cube", boxes=[cube_box]),
    frame("Yellow or cube: 12 + 13 = 25 counts the 5 yellow cubes twice", lambda c, s: c == "yellow" or s == "cube",
          twice=lambda c, s: c == "yellow" and s == "cube", boxes=[yel_box, cube_box]),
    frame("Subtract the overlap: 12 + 13 − 5 = 20 of 29", lambda c, s: c == "yellow" or s == "cube", boxes=[yel_box, cube_box]),
    frame("No overlap (mutually exclusive): 7 + 8 = 15 of 29", lambda c, s: (c, s) in (("yellow", "sphere"), ("green", "cube")),
          boxes=[(6.3, 11.7, 1.4, 3.6, "#9A7B00", "yellow spheres: 7", 9, 4.1), (-0.6, 4.6, -1.6, 0.6, BLUE, "green cubes: 8", 2, -2.1)]),
]
if __name__ == "__main__":
    make_gif(figs, here / "addition_rule", fps=1, holds=[2, 2, 2, 4, 4, 5], keys=[3, 5], cols=1, width=800)

"""The 2 x 2 table of section 4.6 drawn on die faces: two events per row (orange and blue bands), checked for
overlap (mutually exclusive?) and for gaps (exhaustive?)."""
from pathlib import Path
import plotly.graph_objects as go
from plotly.subplots import make_subplots

here = Path(__file__).parent
CASES = [({1, 2, 3}, {4, 5, 6}), ({1, 2}, {5, 6}), ({1, 2, 3, 4}, {3, 4, 5, 6}), ({1, 2, 3}, {3, 4, 5})]
S = set(range(1, 7))
titles = []
for a, b in CASES:
    excl, exh = not (a & b), (a | b) == S
    titles.append(f"{sorted(a)} and {sorted(b)}<br>mutually exclusive: <b>{'yes' if excl else 'no'}</b> · "
                  f"exhaustive: <b>{'yes' if exh else 'no'}</b>".replace("[", "{").replace("]", "}"))
assert [(not (a & b), (a | b) == S) for a, b in CASES] == [(True, True), (True, False), (False, True), (False, False)]
fig = make_subplots(rows=2, cols=2, subplot_titles=titles, vertical_spacing=0.22, horizontal_spacing=0.08)
for ann in fig.layout.annotations:
    ann.font.size = 21
for i, (a, b) in enumerate(CASES):
    r, c = i // 2 + 1, i % 2 + 1
    for f in range(1, 7):
        both, ina, inb = f in a and f in b, f in a, f in b
        col = "#B279A2" if both else ("#F58518" if ina else ("#4C78A8" if inb else "white"))
        fig.add_shape(type="rect", x0=f - 0.45, x1=f + 0.45, y0=0, y1=1, fillcolor=col, opacity=1,
                      line=dict(color="black", width=2, dash="dot" if col == "white" else "solid"), row=r, col=c)
        fig.add_annotation(x=f, y=0.5, text=f"<b>{f}</b>", showarrow=False, font=dict(size=24,
                           color="white" if col != "white" else "black"), row=r, col=c)
    fig.update_xaxes(visible=False, range=[0.4, 6.6], row=r, col=c)
    fig.update_yaxes(visible=False, range=[-0.2, 1.2], row=r, col=c)
fig.add_annotation(xref="paper", yref="paper", x=0.5, y=-0.12, showarrow=False, font=dict(size=18),
                   text="orange: first event · blue: second event · purple: in both (overlap) · white: in neither (gap)")
fig.update_layout(template="simple_white", width=1300, height=560, font=dict(family="Latin Modern Roman", size=18),
                  margin=dict(l=20, r=20, t=90, b=70))
fig.write_image(here / "exclusive_exhaustive.png", scale=2)
fig.write_image(here / "exclusive_exhaustive.pdf")

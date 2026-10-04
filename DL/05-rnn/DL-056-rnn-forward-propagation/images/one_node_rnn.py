"""The smallest RNN: one ReLU node with a feedback loop, hand-picked weights w_i = 1.8, w_h = -0.5, w_o = 1.1 and
no biases, on scaled share prices (low 0, medium 0.5, high 1). Frame 1: the folded network. Then the loop is
unrolled into two copies for "yesterday high, today medium": h_1 = 1.8, h_2 = ReLU(0.9 - 0.9) = 0, prediction 0
(low). The four rule cases of the Note are asserted below. Idea after StatQuest, "Recurrent Neural Networks
(RNNs), Clearly Explained!!!"; our own drawing and weights check. Tool: Plotly frames (a step-by-step computation
on a fixed diagram). Plotly frames -> GIF, plus a key-frame grid for the PDF."""
from pathlib import Path

import plotly.graph_objects as go
from gifkit import save_gif

HERE = Path(__file__).parent
BLUE, RED, GREEN, PURPLE, GREY = "#4C78A8", "#E45756", "#54A24B", "#B279A2", "#6B6B6B"
FONT = dict(family="Latin Modern Roman", size=20)
WI, WH, WO = 1.8, -0.5, 1.1
relu = lambda z: max(z, 0.0)


def run(x1, x2):
    h1 = relu(WI * x1)
    h2 = relu(WI * x2 + WH * h1)
    return h1, h2, WO * h2


# the Note's table: (yesterday, today) -> tomorrow
for (a, b), want in {(0, 0): 0, (0, 0.5): 1, (1, 0.5): 0, (1, 1): 1}.items():
    assert abs(run(a, b)[2] - want) < 0.02


def base(title):
    fig = go.Figure()
    fig.update_layout(template="simple_white", width=1000, height=600, font=FONT, title=dict(text=title, x=0.5, y=0.95),
                      xaxis=dict(visible=False, range=[0, 10]), yaxis=dict(visible=False, range=[0, 6]),
                      margin=dict(l=10, r=10, t=70, b=10), showlegend=False)
    return fig


def node(fig, x, y, text):
    fig.add_shape(type="circle", x0=x - 0.75, x1=x + 0.75, y0=y - 0.45, y1=y + 0.45, line=dict(color=PURPLE, width=3),
                  fillcolor="#F1E8EF", opacity=1)
    fig.add_annotation(x=x, y=y, text=text, showarrow=False, font=dict(size=24))


def arrow(fig, x0, y0, x1, y1, colour, label=None, lx=0, ly=0):
    fig.add_annotation(x=x1, y=y1, ax=x0, ay=y0, xref="x", yref="y", axref="x", ayref="y", showarrow=True,
                       arrowhead=2, arrowsize=1.2, arrowwidth=3, arrowcolor=colour, text="")
    if label:
        fig.add_annotation(x=(x0 + x1) / 2 + lx, y=(y0 + y1) / 2 + ly, text=label, showarrow=False,
                           font=dict(size=23, color=colour), bgcolor="white")


def txt(fig, x, y, text, colour="black", size=24):
    fig.add_annotation(x=x, y=y, text=text, showarrow=False, font=dict(size=size, color=colour))


def folded():
    fig = base("one node with a <b>feedback loop</b>")
    node(fig, 5, 3, "ReLU")
    txt(fig, 5, 0.6, "price x<sub>t</sub>", BLUE)
    arrow(fig, 5, 0.9, 5, 2.5, BLUE, "× w<sub>i</sub> = 1.8", 1.0)
    arrow(fig, 5, 3.5, 5, 5.0, GREEN, "× w<sub>o</sub> = 1.1", 1.0)
    txt(fig, 5, 5.35, "predicted next price", GREEN)
    fig.add_shape(type="path", path="M 5.75 3.15 C 8.2 4.6, 8.2 1.4, 5.85 2.8", line=dict(color=RED, width=3), fillcolor="rgba(0,0,0,0)", opacity=1)
    arrow(fig, 6.2, 2.62, 5.78, 2.85, RED)
    txt(fig, 8.55, 3, "× w<sub>h</sub> = −0.5<br>back into the node<br>at the next step", RED, 22)
    return fig


def unrolled(stage):
    """stage 1: copy 1 computed; 2: h_1 carried over; 3: copy 2 computed; 4: prediction."""
    h1, h2, y = run(1, 0.5)
    titles = {1: "unrolled, step 1: yesterday's price (high = 1) goes in",
              2: "the loop becomes an arrow: h<sub>1</sub> goes to the next copy, times w<sub>h</sub>",
              3: "step 2: today's price (medium = 0.5) meets what the loop brought",
              4: "prediction for tomorrow: 1.1 × 0 = <b>0, low</b>"}
    fig = base(titles[stage])
    xs = [2.6, 7.0]
    node(fig, xs[0], 3, "ReLU")
    txt(fig, xs[0], 0.5, "yesterday: x<sub>1</sub> = 1", BLUE)
    arrow(fig, xs[0], 0.8, xs[0], 2.5, BLUE, "× 1.8 = 1.8", -1.0)
    txt(fig, xs[0], 3.85, f"h<sub>1</sub> = ReLU(1.8) = {h1:.1f}", PURPLE)
    if stage >= 2:
        arrow(fig, xs[0] + 0.8, 3, xs[1] - 0.8, 3, RED, "× (−0.5) = −0.9", 0, 0.35)
    if stage >= 3:
        node(fig, xs[1], 3, "ReLU")
        txt(fig, xs[1], 0.5, "today: x<sub>2</sub> = 0.5", BLUE)
        arrow(fig, xs[1], 0.8, xs[1], 2.5, BLUE, "× 1.8 = 0.9", 1.0)
        txt(fig, xs[1] + 0.3, 3.85, f"h<sub>2</sub> = ReLU(0.9 − 0.9) = {h2:.0f}", PURPLE)
    if stage >= 4:
        arrow(fig, xs[1], 4.2, xs[1], 5.0, GREEN, "× 1.1", 0.6)
        txt(fig, xs[1], 5.4, f"tomorrow: {y:.0f} (low)", GREEN, 26)
        txt(fig, 5, 1.6, "both copies use the<br>same w<sub>i</sub> and w<sub>h</sub>", GREY, 22)
    return fig


if __name__ == "__main__":
    figs = [folded()] + [unrolled(s) for s in (1, 2, 3, 4)]
    save_gif(figs, "one_node_rnn", HERE, keys=[0, 2, 3, 4], fps=0.6, cols=2, holds=[2, 1, 1, 2, 5])

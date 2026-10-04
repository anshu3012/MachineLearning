"""Building the model of Figure 2 one line of code at a time: each call `Layer(...)(input)` adds a node and an edge
to the graph, and the parameter count grows to the 8,898 that model.summary() reports (Notebook).
Plotly frames -> GIF, plus a grid of key frames for the PDF."""
from pathlib import Path

import plotly.graph_objects as go
from common import BLUE, GREEN, RED, GREY
from gifkit import save_gif

HERE = Path(__file__).parent
FONT = dict(family="Latin Modern Roman", size=22)
# name, label, colour, (x, y), receives from, parameters = inputs x nodes + nodes, code line
NODES = [
    ("x", "Input: 3 features", GREY, (0, 4), None, 0, "x = Input(shape=(3,))"),
    ("h1", "hidden1: Dense 128, ReLU", GREEN, (0, 3), "x", 3 * 128 + 128, 'hidden1 = Dense(128, activation="relu")(x)'),
    ("h2", "hidden2: Dense 64, ReLU", GREEN, (0, 2), "h1", 128 * 64 + 64, 'hidden2 = Dense(64, activation="relu")(hidden1)'),
    ("o1", "age: Dense 1, linear", RED, (-1.6, 0.9), "h2", 64 + 1, 'output1 = Dense(1, name="age")(hidden2)'),
    ("o2", "place: Dense 1, sigmoid", RED, (1.6, 0.9), "h2", 64 + 1, 'output2 = Dense(1, activation="sigmoid", name="place")(hidden2)'),
]
TOTAL = sum(n[5] for n in NODES)
assert TOTAL == 8898                                        # model.summary() in the Notebook


def rgba(hex_colour, a=0.25):
    r, g, b = (int(hex_colour[i:i + 2], 16) for i in (1, 3, 5))
    return f"rgba({r},{g},{b},{a})"


def frame(k, wrap=False):
    fig = go.Figure()
    pos = {n[0]: n[3] for n in NODES}
    for i, (name, label, col, (x, y), src, p, code) in enumerate(NODES[:k + 1]):
        new = i == k and not wrap
        fig.add_shape(type="rect", x0=x - 1.25, x1=x + 1.25, y0=y - 0.3, y1=y + 0.3, fillcolor=rgba(col), opacity=1,
                      line=dict(color="black" if new else col, width=5 if new else 2))
        fig.add_annotation(x=x, y=y, text=label, showarrow=False, font=dict(size=22))
        if p:
            fig.add_annotation(x=x + 1.32, y=y, text=f"+{p:,}", showarrow=False, xanchor="left",
                               font=dict(size=21, color=BLUE))
        if src:
            sx, sy = pos[src]
            fig.add_annotation(x=x, y=y + 0.3, ax=sx, ay=sy - 0.3, xref="x", yref="y", axref="x", ayref="y",
                               showarrow=True, arrowhead=2, arrowsize=1.4, arrowwidth=3,
                               arrowcolor="black" if new else GREY, text="")
    count = sum(n[5] for n in NODES[:k + 1])
    if wrap:
        fig.add_shape(type="rect", x0=-3.15, x1=3.65, y0=0.3, y1=4.45, fillcolor="rgba(0,0,0,0)", line=dict(color=BLUE, width=3, dash="dash"))
        code = "model = Model(inputs=x, outputs=[output1, output2])"
        note = f"<b>Model</b> collects every layer from the input to the two outputs: {count:,} parameters"
    else:
        code = NODES[k][6]
        note = "a new layer, called on its input: one new node and one new edge" if k else "the input fixes the shape: 3 numbers"
    fig.add_annotation(x=0, y=-0.15, text=f"total so far: <b>{count:,}</b> parameters", showarrow=False,
                       font=dict(size=22, color=BLUE))
    fig.update_layout(template="simple_white", width=1000, height=820, font=FONT, showlegend=False,
                      title=dict(text=f"<span style='font-family:monospace;font-size:19px'>{code}</span><br>"
                                      f"<span style='font-size:18px'>{note}</span>", x=0.5, y=0.96),
                      xaxis=dict(range=[-3.3, 3.8], visible=False), yaxis=dict(range=[-0.45, 4.6], visible=False),
                      margin=dict(l=20, r=20, t=110, b=20))
    return fig, count


if __name__ == "__main__":
    figs = [frame(k)[0] for k in range(len(NODES))]
    last, count = frame(len(NODES) - 1, wrap=True)
    assert count == TOTAL
    save_gif(figs + [last], "graph_build", HERE, keys=[0, 2, 4, 5], fps=0.8, holds=[1, 1, 1, 1, 1, 4])

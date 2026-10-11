"""Figure 2 as an animation: a door that nobody touches, read twice, one panel per belief. For each 'sense open'
reading the bars of the belief before it are multiplied by p(sense open | x), 0.6 for open and 0.2 for closed, and
turn grey (products, not yet probabilities: 0.3 + 0.1 = 0.4, then 0.45 + 0.05 = 0.5); then both are multiplied by
eta = one over their sum (2.5, then 2) and grow back to blue. The last frame is the still: 0.5, 0.75, 0.9 for open.
Run -> two_readings_anim.gif, two_readings_anim_frames.png"""
from pathlib import Path

import plotly.graph_objects as go
from plotly.subplots import make_subplots

from doorplot import P_Z, STATES, door_bars, update
from gifkit import BLUE, FONT, GREY, make_gif

here = Path(__file__).parent
PANELS = ["before any reading", "after z<sub>1</sub> = sense open", "after z<sub>2</sub> = sense open"]
b0 = {"open": 0.5, "closed": 0.5}
LIK = {x: P_Z[x]["open"] for x in STATES}                      # p(sense open | x): 0.6, 0.2


def num(v):
    return f"{v:.2f}".rstrip("0").rstrip(".")                 # 0.30 -> 0.3, 2.50 -> 2.5, 2.00 -> 2


def frame(title, sub, shown, work=None, factors=None):
    """shown: finished panels (list of beliefs); work: (heights, colour, labelled) drawn in the next panel;
    factors: text written above each bar of the working panel."""
    fig = make_subplots(rows=1, cols=3, horizontal_spacing=0.07, subplot_titles=PANELS)
    for c, b in enumerate(shown, start=1):
        door_bars(fig, b, BLUE, row=1, col=c, fmt="{:.2f}")
    if work is not None:
        c = len(shown) + 1
        h, col, lab = work
        door_bars(fig, h, col, row=1, col=c, fmt="{:.2f}" if lab else "")
        for x in STATES if factors else ():
            fig.add_annotation(x=x, y=h[x] + 0.15, text=factors[x], showarrow=False, font=dict(size=22, color="black"),
                               xref=f"x{c}", yref=f"y{c}")
    for c in range(1, 4):
        fig.add_trace(go.Scatter(x=list(STATES), y=[0, 0], mode="markers", marker=dict(opacity=0)), row=1, col=c)
        fig.update_xaxes(type="category", categoryarray=list(STATES), range=[-0.5, 1.5], row=1, col=c)
        fig.update_yaxes(range=[0, 1.12], row=1, col=c)
    fig.update_yaxes(title="probability", row=1, col=1)
    fig.update_layout(template="simple_white", width=1200, height=580, font=FONT, showlegend=False,
                      margin=dict(l=70, r=20, t=150, b=50),
                      title=dict(text=f"{title}<br><span style='font-size:19px'>{sub}</span>", x=0.5, y=0.955,
                                 yanchor="top", font=dict(size=24)))
    fig.update_annotations(font_size=22)
    return fig


def mix(a, b, s):
    return {x: (1 - s) * a[x] + s * b[x] for x in STATES}


figs, holds, keys = [frame("before any reading: 0.5 for open, 0.5 for closed",
                           "blue bars: the belief in each door; nobody touches the door", [b0])], [8], []
shown, prior = [b0], b0
for k in (1, 2):
    prod = {x: LIK[x] * prior[x] for x in STATES}
    s = sum(prod.values())
    eta = 1 / s
    post = {x: eta * prod[x] for x in STATES}
    assert all(abs(post[x] - update(prior, "open")[x]) < 1e-12 for x in STATES)
    times = {x: f"× {num(LIK[x])}" for x in STATES}
    start = f"start from the belief before it, {num(prior['open'])} and {num(prior['closed'])}"
    figs.append(frame(f"reading z<sub>{k}</sub> = sense open: multiply each bar by p(z<sub>{k}</sub> | x)",
                      f"{start}; p(sense open | x) is 0.6 for open, 0.2 for closed",
                      shown, (prior, BLUE, True), times))
    holds.append(9)
    keys.append(len(figs) - 1)
    for a in (0.33, 0.67):
        figs.append(frame(f"reading z<sub>{k}</sub> = sense open: multiply each bar by p(z<sub>{k}</sub> | x)",
                          f"open: 0.6 × {num(prior['open'])}     closed: 0.2 × {num(prior['closed'])}",
                          shown, (mix(prior, prod, a), GREY, False), times))
        holds.append(1)
    figs.append(frame(f"the products add to {num(prod['open'])} + {num(prod['closed'])} = {num(s)}, not 1",
                      "grey bars: products, not yet probabilities", shown, (prod, GREY, True)))
    holds.append(9)
    keys.append(len(figs) - 1)
    grow = {x: f"× {num(eta)}" for x in STATES}
    figs.append(frame(f"rescale: multiply both by η = 1 / {num(s)} = {num(eta)}",
                      "η (eta) is one over the sum of the products, so the new bars add to 1", shown,
                      (prod, GREY, True), grow))
    holds.append(8)
    keys.append(len(figs) - 1)
    for a in (0.33, 0.67):
        figs.append(frame(f"rescale: multiply both by η = 1 / {num(s)} = {num(eta)}",
                          f"open: {num(eta)} × {num(prod['open'])}     closed: {num(eta)} × {num(prod['closed'])}",
                          shown, (mix(prod, post, a), BLUE, False), grow))
        holds.append(1)
    shown = shown + [post]
    figs.append(frame(f"after z<sub>{k}</sub>: {num(post['open'])} for open, {num(post['closed'])} for closed",
                      "the robot keeps only this belief" if k == 1 else "the robot never went back to z<sub>1</sub>",
                      shown))
    holds.append(9)
    keys.append(len(figs) - 1)
    prior = post
figs.append(frame("each reading multiplies, then rescales", "belief in open: 0.5, then 0.75, then 0.9", shown))
holds.append(22)
keys.append(len(figs) - 1)
make_gif(figs, here / "two_readings_anim", fps=5, holds=holds, keys=keys[:4] + [keys[5], keys[-1]], cols=2,
         width=950)
# the numbers of Section 3: products 0.3 / 0.1 (sum 0.4, eta 2.5) -> 0.75 / 0.25; 0.45 / 0.05 (sum 0.5, eta 2) -> 0.9 / 0.1
assert [round(v, 12) for v in (shown[1]["open"], shown[1]["closed"], shown[2]["open"], shown[2]["closed"])] == \
    [0.75, 0.25, 0.9, 0.1]
assert abs(0.6 * 0.5 + 0.2 * 0.5 - 0.4) < 1e-12 and abs(0.6 * 0.75 + 0.2 * 0.25 - 0.5) < 1e-12

"""Animation: SayCan's choice, one skill at a time, on the table (numbers from the notebook, data/saycan_scores.csv).
For each of the 7 skills: Say, GPT-2 small's probability for the skill's words after the request, shared out over
the 7 skills (blue); Can, our tests in the current state (red: 1 if a placement, configuration and motion exist,
0 if not, 0.1 for "done"); and their product, shared out (green). Step 1 picks "pick up the cup". At step 2 the
two skills with the highest language scores are impossible (Can 0), and "done" (0.0173 x 0.1) beats "put down the cup
on the table" (0.0016 x 1), so the robot stops with the cup in its hand.
Run -> saycan_anim.gif, saycan_anim_frames.png"""
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from gifkit import BLUE, FONT, GREEN, GREY, RED, make_gif

here = Path(__file__).parent
S = pd.read_csv(here.parent / "data" / "saycan_scores.csv")
s2 = S[S.step == 2].set_index("skill")
assert round(s2.loc["done", "say"], 4) == 0.0173 and round(s2.loc["put down the cup on the table", "say"], 4) == 0.0016
assert round(s2.loc["done", "say_x_can_share"], 4) == 0.5246
assert round(S[(S.step == 1) & (S.skill == "pick up the cup")].say.iloc[0], 4) == 0.9946
SKILLS = list(S[S.step == 1].skill)[::-1]          # first skill at the top
CHOSEN = {1: "pick up the cup", 2: "done"}


def fmt(v):
    return "<0.0001" if 0 < v < 5e-5 else f"{v:.4f}".rstrip("0").rstrip(".") if v in (0, 1, 0.1) else f"{v:.4f}"


def frame(step, stage, title):
    d = S[S.step == step].set_index("skill").loc[SKILLS]
    fig = make_subplots(rows=1, cols=3, shared_yaxes=True, horizontal_spacing=0.03,
                        subplot_titles=["Say: language share", "Can: our tests", "Say x Can, shared out"])
    cols = [("say", BLUE), ("can", RED), ("say_x_can_share", GREEN)]
    for c, (key, color) in enumerate(cols, 1):
        if c > stage:
            vals = [0] * len(SKILLS)
            text = [""] * len(SKILLS)
        else:
            vals = list(d[key])
            text = [fmt(v) for v in vals]
        line = [3 if (c == 3 and stage == 3 and sk == CHOSEN[step]) else 0 for sk in SKILLS]
        fig.add_trace(go.Bar(x=vals, y=SKILLS, orientation="h", marker=dict(color=color, line=dict(color="black",
                             width=line)), text=text, textposition="outside", cliponaxis=False,
                             textfont=dict(size=17)), row=1, col=c)
        fig.update_xaxes(range=[0, 1.45], showticklabels=False, showgrid=False, row=1, col=c)
    fig.update_yaxes(tickfont=dict(size=18), row=1, col=1)
    for a in fig.layout.annotations:
        a.font = dict(size=20)
    fig.update_layout(template="simple_white", width=1500, height=640, font=FONT, showlegend=False,
                      margin=dict(l=330, r=40, t=120, b=40), bargap=0.35,
                      title=dict(text=title, x=0.5, y=0.97, font=dict(size=22)))
    return fig


figs, holds = [], []
TXT = {
    (1, 1): "step 1, the hand is empty: the language model puts 0.9946 on 'pick up the cup'",
    (1, 2): "step 1: our tests say which skills can run now",
    (1, 3): "step 1: Say x Can picks 'pick up the cup'",
    (2, 1): "step 2, the cup is held: the language model still gives 'pick up the cup' the highest share (0.9421)",
    (2, 2): "step 2: 'pick up the cup' and 'put down the cup on spot B' cannot run (Can 0)",
    (2, 3): "step 2: 'done' 0.0173 x 0.1 beats 'put down the cup on the table' 0.0016 x 1",
}
for step in (1, 2):
    for stage in (1, 2, 3):
        figs.append(frame(step, stage, TXT[(step, stage)]))
        holds.append(10 if stage == 3 else 8)
figs.append(frame(2, 3, "SayCan's plan: 1. pick up the cup, 2. done; the cup stays in the hand, spot B is never reached"))
holds.append(20)
make_gif(figs, here / "saycan_anim", fps=2, holds=holds, keys=[1, 2, 4, 5], cols=2, width=1100)

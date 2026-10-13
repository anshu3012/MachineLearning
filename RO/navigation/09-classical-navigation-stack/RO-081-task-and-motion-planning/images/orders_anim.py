"""Animation: the two orders for the two searches (Garrett et al. 2021, Fig. 11), as loops lit step by step. Top,
sequence before satisfy, lit along this Note's run (seed 0, as the notebook): skeleton 1, its numbers fail at B, the
failure becomes a fact, skeleton 2, five samples with one backtrack, the plan (4 actions, 374.5 degrees). Bottom,
satisfy before sequence, PDDLStream's incremental algorithm, drawn as a schematic (not run in the notebook): sample
values, search for a plan with tested values only, sample more if none, until a plan is found.
Run -> orders_anim.gif, orders_anim_frames.png"""
from pathlib import Path

import plotly.graph_objects as go

import tampkit as t
from gifkit import BLUE, FONT, GREEN, GREY, ORANGE, RED, make_gif

here = Path(__file__).parent
steps, history, log = t.tamp(t.World({"cup": t.A_X, "bottle": t.B_X}), {"cup": "A", "bottle": "start"},
                             {"cup": "B"}, seed=0)
assert len(history) == 2 and round(sum(s["length"] for s in steps), 1) == 374.5
n_samples = len({round(e["x"], 6) for e in log if e.get("sampled")})
assert n_samples == 5

W, H = 1500, 760
X = [0.125, 0.385, 0.635, 0.875]                    # box centres, paper coordinates
ROWS = {"top": 0.70, "bottom": 0.22}
LABELS = {"top": ["task planner:<br>next plan skeleton", "fill in the numbers:<br>sample, test, back up",
                  "every test<br>passes?", "plan"],
          "bottom": ["samplers:<br>more values", "task planner: a plan<br>using tested values only",
                     "plan<br>found?", "plan"]}
COLORS = {"top": [BLUE, ORANGE, GREY, GREEN], "bottom": [ORANGE, BLUE, GREY, GREEN]}
TITLES = {"top": "sequence before satisfy (our run)", "bottom": "satisfy before sequence (PDDLStream, incremental: a schematic, not run here)"}


def frame(active, note, title, loop=None, note_color="black"):
    fig = go.Figure()
    for row, y in ROWS.items():
        fig.add_annotation(x=0.02, y=y + 0.17, xref="x", yref="y", text=TITLES[row], showarrow=False,
                           xanchor="left", font=dict(size=22))
        for k, x in enumerate(X):
            on = active == (row, k)
            c = COLORS[row][k]
            fig.add_shape(type="rect", xref="x", yref="y", x0=x - 0.105, x1=x + 0.105, y0=y - 0.07,
                          y1=y + 0.07, line=dict(color=c, width=6 if on else 2),
                          fillcolor=c if on else "white", opacity=0.9 if on else 1)
            fig.add_annotation(x=x, y=y, xref="x", yref="y", text=LABELS[row][k], showarrow=False,
                               font=dict(size=19, color="white" if on else "black"))
            if k < 3:
                fig.add_annotation(x=X[k + 1] - 0.107, y=y, ax=x + 0.107, ay=y, xref="x", yref="y",
                                   axref="x", ayref="y", showarrow=True, arrowhead=2, arrowwidth=2,
                                   arrowcolor=GREY, text="")
        fig.add_annotation(x=0.755, y=y + 0.025, xref="x", yref="y", text="yes", showarrow=False,
                           font=dict(size=17, color=GREY))
        lw = 5 if loop == row else 2
        lc = RED if loop == row else GREY
        fig.add_shape(type="path", xref="x", yref="y", line=dict(color=lc, width=lw), fillcolor="rgba(0,0,0,0)", opacity=1,
                      path=f"M {X[2]},{y - 0.07} L {X[2]},{y - 0.13} L {X[0]},{y - 0.13} L {X[0]},{y - 0.075}")
        fig.add_annotation(x=X[0], y=y - 0.072, ax=X[0], ay=y - 0.12, xref="x", yref="y", axref="x",
                           ayref="y", showarrow=True, arrowhead=2, arrowwidth=lw, arrowcolor=lc, text="")
        fig.add_annotation(x=(X[0] + X[2]) / 2, y=y - 0.155, xref="x", yref="y", showarrow=False,
                           text="no: a failed test at a named place becomes a new fact" if row == "top" else
                           "no: sample more values and search again", font=dict(size=17, color=GREY))
    fig.add_annotation(x=0.5, y=0.95, xref="x", yref="y", text=note, showarrow=False,
                       font=dict(size=21, color=note_color))
    fig.update_xaxes(visible=False, range=[0, 1])
    fig.update_yaxes(visible=False, range=[0, 1])
    fig.update_xaxes(domain=[0, 1])
    fig.update_yaxes(domain=[0, 1])
    fig.update_layout(template="simple_white", width=W, height=H, font=FONT, showlegend=False,
                      margin=dict(l=20, r=20, t=110, b=10), title=dict(text=title, x=0.5, y=0.975, font=dict(size=23)))
    return fig


F = [
    (None, "", "two orders for the search over actions and the search over numbers", None),
    (("top", 0), "skeleton 1: pick up the cup at A, put it down at B", "sequence before satisfy, our run", None),
    (("top", 1), "motion to the lid found (154.6 degrees); the cup at B would overlap the bottle", "", None),
    (("top", 2), "no: the cup at B collides with the bottle where it stands, a new fact", "", "top"),
    (("top", 0), "skeleton 2: move the bottle first, then the cup", "", None),
    (("top", 1), f"{n_samples} samples of the bottle's place, one backtrack; x = 0.485 m works", "", None),
    (("top", 2), "yes: every test passes", "", None),
    (("top", 3), "plan: 4 actions, 374.5 degrees of joint motion", "", None),
    (("bottom", 0), "sample values with the streams: places, joint angles, motions", "satisfy before sequence, PDDLStream (schematic)", None),
    (("bottom", 1), "search for a plan that uses only values already tested", "", None),
    (("bottom", 2), "no plan yet: sample more values", "", "bottom"),
    (("bottom", 0), "more values: more places, joint angles and motions", "", None),
    (("bottom", 1), "search again with the larger set of tested values", "", None),
    (("bottom", 3), "a plan is found among the tested values", "", None),
]
figs, holds = [], []
for active, note, title, loop in F:
    figs.append(frame(active, note, title or "two orders for the two searches", loop,
                      RED if loop else "black"))
    holds.append(5)
holds[0], holds[7], holds[-1] = 6, 10, 14
make_gif(figs, here / "orders_anim", fps=2, holds=holds, keys=[3, 7, 10, 13], cols=2, width=1100)

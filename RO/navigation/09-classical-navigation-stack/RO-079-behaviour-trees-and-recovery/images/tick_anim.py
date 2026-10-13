"""The smallest navigation tree, tick by tick, on the room of RO-058 (our Python version, btkit.mini_tree): a
Fallback (Path valid? or else ComputePathToPose) and then FollowPath, under two different parents. Left: a plain
Sequence, as BehaviorTree.CPP writes it: once a child succeeded it goes on from the running child. Right: Nav2's
PipelineSequence, which ticks the children before the running one again at every tick. The person steps onto the
route at 2.4 s. Boxes: amber running, green success, red failure, white not ticked. Run -> tick_anim.gif,
tick_anim_frames.png"""
from pathlib import Path

import btkit as bt
import navdraw as nd
from gifkit import FONT, make_gif
from plotly.subplots import make_subplots

here = Path(__file__).parent
RES = bt.results()
RUNS = [("mini_seq", "Sequence"), ("mini_pipe", "PipelineSequence")]
NAMES = {"mini_seq": ["Sequence", "Fallback", "Path valid?", "ComputePathToPose", "FollowPath"],
         "mini_pipe": ["PipelineSequence", "Fallback", "Path valid?", "ComputePathToPose", "FollowPath"]}
assert RES["mini_seq"]["planned"] == [(0.01, None)] and RES["mini_pipe"]["planned"] == [(0.01, None), (2.41, None)]
CAP = {0.0: "t = 0.00 s: no path yet: Path valid? fails, so the Fallback ticks ComputePathToPose",
       0.01: "t = 0.01 s: the path arrives: the Fallback succeeds and FollowPath starts",
       0.02: "t = 0.02 s: left: the Sequence goes on from FollowPath; right: Path valid? is checked again",
       1.0: "t = 1.00 s: the same every 10 ms",
       2.4: "t = 2.40 s: the person steps in: only the right-hand tree detects that the path is blocked",
       2.41: "t = 2.41 s: right: a new path round the person; left: still the old path",
       3.1: "t = 3.10 s: left: Path valid? has not been ticked since 0.00 s"}


def frame(t):
    fig = make_subplots(rows=2, cols=2, row_heights=[0.62, 0.38], vertical_spacing=0.05, horizontal_spacing=0.03,
                        subplot_titles=[f"<b>{RUNS[0][1]}</b> (BehaviorTree.CPP)", f"<b>{RUNS[1][1]}</b> (Nav2)", "", ""])
    for c, (key, _) in enumerate(RUNS, start=1):
        recs = RES[key]["records"]
        rec = nd.at(recs, t)
        nd.room(fig, 1, c, person=rec["person"], labels=False)
        nd.goal(fig, bt.GOAL, 1, c)
        nd.track(fig, recs, t, row=1, col=c)
        nd.path(fig, rec["path"], row=1, col=c)
        nd.robot(fig, *rec["robot"], row=1, col=c)
        tree = bt.mini_tree("sequence" if key == "mini_seq" else "pipeline")
        rows = nd.tree_rows(tree, NAMES[key])
        lit, seq = nd.lit_of(rec)
        n = nd.draw_tree(fig, rows, lit, seq, row=2, col=c, step=0.5, size=17)
        fig.update_xaxes(range=[1.3, 4.6], visible=False, constrain="domain", row=1, col=c)
        fig.update_yaxes(range=[0.45, 4.25], visible=False, scaleanchor="x" if c == 1 else "x2", scaleratio=1,
                         constrain="domain", row=1, col=c)
        fig.update_xaxes(range=[-0.1, 4.6], visible=False, row=2, col=c)
        fig.update_yaxes(range=[-n + 0.4, 0.6], visible=False, row=2, col=c)
    fig.add_annotation(x=0.0, y=1.045, xref="paper", yref="paper", text=CAP[t], showarrow=False, xanchor="left",
                       yanchor="bottom", font=dict(size=18))
    fig.update_layout(template="simple_white", font=FONT, width=900, height=820, showlegend=False,
                      margin=dict(l=8, r=8, t=70, b=8))
    return fig


T = list(CAP)
figs = [frame(t) for t in T]
make_gif(figs, here / "tick_anim", fps=1, holds=[3, 3, 3, 2, 4, 4, 6], keys=[0, 2, 4, 6], cols=2,
         width=800)

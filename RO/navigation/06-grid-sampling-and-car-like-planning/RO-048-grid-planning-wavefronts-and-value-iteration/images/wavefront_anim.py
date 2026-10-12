"""The wavefront spreading from the door on the 4-connected room grid, one ring per frame: breadth-first search from
the goal cell G numbers every free cell with its fewest moves to G. The ring just numbered is mid blue, earlier rings
pale blue. Ring 8 reaches the start cell S; the last frame has all 76 free cells numbered, the farthest 24 moves away.
Run -> wavefront_anim.gif, wavefront_anim_frames.png"""
from pathlib import Path

from drawkit import axes, layout, numbers, outline, room, sg
from gifkit import make_gif
from gridplan import CELLS, START, nb4, wavefront
import plotly.graph_objects as go

here = Path(__file__).parent
NUM, RINGS = wavefront(nb4)
assert len(NUM) == 76 == len(CELLS) and NUM[START] == 8 and max(NUM.values()) == 24 and len(RINGS) == 25
assert [len(r) for r in RINGS[:4]] == [1, 3, 4, 4] and len(RINGS[8]) == 5


def frame(k):
    status, shown = {}, {}
    for r in range(k + 1):
        for c in RINGS[r]:
            status[c] = "back" if r == k else "back_open"
            shown[c] = r
    fig = go.Figure()
    room(fig, None, status, labels=False)
    numbers(fig, shown, size=21, dy=0.07)
    if k >= 8:
        outline(fig, START)
    sg(fig, dy=-0.15, size=17)
    axes(fig)
    if k == 0:
        t = "ring 0: the door's cell G gets 0"
    elif k == 8:
        t = "ring 8 reaches S: 8 moves of 0.5 m, 4.0 m to the door"
    elif k == len(RINGS) - 1:
        t = "ring 24: all 76 free cells numbered; none is cut off"
    else:
        t = f"ring {k}: {len(RINGS[k])} cells, each {k} move{'s' if k > 1 else ''} from the door"
    return layout(fig, t, width=900, height=600)


figs = [frame(k) for k in range(len(RINGS))]
holds = [6] + [3] * (len(RINGS) - 2) + [24]
holds[8] = 10
make_gif(figs, here / "wavefront_anim", fps=4, holds=holds, keys=[1, 4, 8, 24], cols=2, width=760)

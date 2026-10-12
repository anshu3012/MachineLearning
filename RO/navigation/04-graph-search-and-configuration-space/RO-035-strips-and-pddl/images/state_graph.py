"""Forward search on the task's state graph, one step per frame. Each box is a state (its true facts); columns are
where the robot is, rows where the cup is. A line joins two states that one action turns into each other (a move
across a row, a pick-up or put-down down a column; every line is two actions, one each way).
state_bfs: breadth-first search takes states from the frontier (a first-in, first-out queue) in the order they were
made: 8 taken, 10 made, 2 of the 12 reachable states never made; the plan is 4 actions.
state_astar: A* with h = the fewest actions still needed takes the state with the smallest f = g + h: 5 taken.
Run: python state_graph.py -> state_bfs.gif, state_astar.gif and their _frames.png"""
from pathlib import Path

import plotly.graph_objects as go
from gifkit import BLUE, FONT, GREEN, GREY, ORANGE, make_gif
from taskplan import INIT, astar, bfs, h_actions_left, reachable, short, successors

here = Path(__file__).parent
COLX = {"start": 0.0, "table": 4.5, "door": 9.0}
ROWY = {"table": 9.0, "held": 6.3, "door": 3.6, "start": 0.9}
ROWNAME = {"table": "cup on the table", "held": "cup in the hand", "door": "cup at the door",
           "start": "cup at the start"}
BW, BH = 3.6, 1.9                                           # box width and height

plan, log, parent = bfs()
REACH = reachable()
assert len(REACH) == 12 and len(log) == 8 and len(parent) == 10 and len(plan) == 4
ORDER = list(parent)                                         # BFS discovery order: S0, S1, ...
NAME = {s: f"S{k}" for k, s in enumerate(ORDER)}
for s in sorted(REACH - set(ORDER), key=lambda t: short(t)[0], reverse=True):
    NAME[s] = f"S{len(NAME)}"
assert [short(s) for s in ORDER[:3]] == [("start", "table"), ("table", "table"), ("door", "table")]


def pos(s):
    r, c = short(s)
    return COLX[r], ROWY[c]


def facts_text(s):
    order = ["robot-at", "cup-at", "holding-cup", "hand-empty"]
    return "<br>".join(sorted(s, key=lambda f: order.index(f.split()[0])))


def edge_xy(a, b):
    """Points of the line between states a and b; the start-door moves and the start column bend round."""
    (x0, y0), (x1, y1) = pos(a), pos(b)
    if y0 == y1 and abs(x1 - x0) > 5:                        # start <-> door across a row: an arc above
        return [x0, x0, x1, x1], [y0 + BH / 2, y0 + BH / 2 + 0.35, y0 + BH / 2 + 0.35, y0 + BH / 2]
    if x0 == x1 and abs(y1 - y0) > 3:                        # start column, held <-> cup at start: round the left
        return [x0 - BW / 2, x0 - BW / 2 - 0.35, x1 - BW / 2 - 0.35, x1 - BW / 2], [y0, y0, y1, y1]
    if y0 == y1:
        s = 1 if x1 > x0 else -1
        return [x0 + s * BW / 2, x1 - s * BW / 2], [y0, y1]
    s = 1 if y1 > y0 else -1
    return [x0, x1], [y0 + s * BH / 2, y1 - s * BH / 2]


ALL_EDGES = {frozenset((s, t)) for s in REACH for _, t in successors(s)}
assert len(ALL_EDGES) == 15                                  # 12 move lines (3 in each of 4 rows) and 3 pick-up/put-down lines


def frame(title, made, taken, now=None, frontier=(), lines=(), new=(), plan_states=(), extra="", fvals=None,
          faint=()):
    fig = go.Figure()
    for c, y in ROWY.items():
        fig.add_annotation(x=-2.45, y=y, text=ROWNAME[c].replace(" the ", "<br>the "), showarrow=False,
                           xanchor="right", font=dict(size=17, color=GREY))
    for p, x in COLX.items():
        fig.add_annotation(x=x, y=10.75, text=f"robot at {p}", showarrow=False, font=dict(size=18, color=GREY))
    for e in ALL_EDGES:                                      # edges seen so far
        a, b = tuple(e)
        if e in lines or e in new:
            xs, ys = edge_xy(a, b)
            on_plan = a in plan_states and b in plan_states
            col, w = (GREEN, 6) if on_plan else ((ORANGE, 4) if e in new else ("#999999", 2))
            fig.add_trace(go.Scatter(x=xs, y=ys, mode="lines", line=dict(color=col, width=w)))
        elif faint and (a in faint or b in faint):
            xs, ys = edge_xy(a, b)
            fig.add_trace(go.Scatter(x=xs, y=ys, mode="lines", line=dict(color="#DDDDDD", width=2, dash="dot")))
    for s in REACH:
        x, y = pos(s)
        if s in made:
            if s == now:
                fill, line, w = "rgba(76,120,168,0.45)", BLUE, 5
            elif s in plan_states:
                fill, line, w = "rgba(84,162,75,0.25)", GREEN, 4
            elif s in taken:
                fill, line, w = "rgba(107,107,107,0.18)", GREY, 2
            else:
                fill, line, w = "rgba(245,133,24,0.22)", ORANGE, 3
            txt = f"<b>{NAME[s]}</b><br>{facts_text(s)}"
            col = "black"
        elif s in faint:
            fill, line, w, col = "rgba(0,0,0,0)", "#CCCCCC", 2, "#BBBBBB"
            txt = f"{NAME[s]}<br>never made"
        else:
            continue
        fig.add_shape(type="rect", x0=x - BW / 2, x1=x + BW / 2, y0=y - BH / 2, y1=y + BH / 2, fillcolor=fill,
                      line=dict(color=line, width=w, dash="dot" if s in faint and s not in made else "solid"),
                      opacity=1)
        fig.add_annotation(x=x, y=y, text=txt, showarrow=False, font=dict(size=19, color=col))
        if fvals and s in fvals:
            g, h = fvals[s]
            fig.add_annotation(x=x + BW / 2 - 0.05, y=y + BH / 2 - 0.05, text=f"{g} + {h} = {g + h}",
                               showarrow=False, xanchor="right", yanchor="top",
                               font=dict(size=18, color=BLUE), bgcolor="white")
    q = ", ".join(NAME[t] + (f" (f = {sum(fvals[t])})" if fvals else "") for t in frontier) or "empty"
    fig.add_annotation(x=-4.4, y=-0.65, text=f"<b>frontier:</b> {q}", showarrow=False, xanchor="left",
                       font=dict(size=21))
    fig.add_annotation(x=-4.4, y=-1.35, text=f"taken from the frontier: {len(taken)}   made: {len(made)}"
                       + (f"   {extra}" if extra else ""), showarrow=False, xanchor="left", font=dict(size=21))
    leg = [f"<span style='color:{BLUE}'>■ taken now</span>   <span style='color:{ORANGE}'>■ in the frontier</span>",
           f"<span style='color:{GREY}'>■ taken before</span>   <span style='color:{GREEN}'>■ the plan</span>"]
    for y, s in zip((-0.65, -1.35), leg):
        fig.add_annotation(x=10.9, y=y, text=s, showarrow=False, xanchor="right", font=dict(size=20))
    fig.update_layout(template="simple_white", font=FONT, width=1150, height=980, showlegend=False,
                      margin=dict(l=10, r=10, t=70, b=10), title=dict(x=0.5, text=title, font=dict(size=22)),
                      xaxis=dict(visible=False, range=[-4.6, 11.0]), yaxis=dict(visible=False, range=[-1.8, 11.1]))
    return fig


def plan_path(plan_list, start=INIT):
    from taskplan import ACTIONS, apply
    act = {a[0]: a for a in ACTIONS}
    states = [start]
    for n in plan_list:
        states.append(apply(states[-1], act[n]))
    return states


# ---------------------------------------------------------------- breadth-first search
figs, holds = [], []
made, taken, lines = {INIT}, [], set()
figs.append(frame("breadth-first forward search: the start state S0 is the frontier", made, taken,
                  frontier=[INIT]))
holds.append(4)
for k, (s, kids, q) in enumerate(log, 1):
    taken.append(s)
    looked = {frozenset((s, t)) for _, t in successors(s)}
    new = {frozenset((s, t)) for _, t in kids}
    for _, t in kids:
        made.add(t)
    if kids:
        what = "makes " + ", ".join(f"{NAME[t]} ({n})" for n, t in kids)
    elif s == ORDER[7]:
        what = "holds cup-at door: goal, stop"
    else:
        what = "makes nothing new"
    figs.append(frame(f"take {NAME[s]}: {what}", made, taken, now=s, frontier=q, lines=lines | looked, new=new))
    holds.append(5 if k < 8 else 4)
    lines |= looked
PATH = plan_path(plan)
assert PATH[-1] == ORDER[7] and [NAME[s] for s in PATH] == ["S0", "S1", "S3", "S5", "S7"]
never = REACH - set(made)
assert len(never) == 2 and all(short(s)[1] == "door" for s in never)
figs.append(frame("plan read back from S7: move start table, pick-up table, move table door, put-down door",
                  made, taken, frontier=log[-1][2], lines=lines, plan_states=set(PATH), faint=never,
                  extra="(12 states reachable)"))
holds.append(14)
make_gif(figs, here / "state_bfs", fps=1, holds=holds, keys=[1, 3, 5, len(figs) - 1], cols=2, width=850)

# ---------------------------------------------------------------- A* with h = fewest actions still needed
p2, closed = astar()
assert p2 == plan and len(closed) == 5 and [NAME[s] for s in closed] == ["S0", "S1", "S3", "S5", "S7"]
assert h_actions_left(INIT) == 4
g = {INIT: 0}
fv = {INIT: (0, 4)}
figs, holds = [], []
made, taken, lines = {INIT}, [], set()
frontier = [INIT]
figs.append(frame("A*: each box shows g + h = f; take the smallest f", made, taken, frontier=frontier, fvals=fv))
holds.append(4)
for s in closed:
    taken.append(s)
    frontier.remove(s)
    if s == closed[-1]:
        figs.append(frame(f"take {NAME[s]} (f = {sum(fv[s])}): goal, stop", made, taken, now=s,
                          frontier=sorted(frontier, key=lambda t: sum(fv[t])), lines=lines, fvals=fv))
        holds.append(4)
        break
    looked = {frozenset((s, t)) for _, t in successors(s)}
    new = set()
    for _, t in successors(s):
        if t not in g or g[s] + 1 < g[t]:
            g[t] = g[s] + 1
            fv[t] = (g[t], h_actions_left(t))
            if t not in made:
                made.add(t)
                frontier.append(t)
                new.add(frozenset((s, t)))
    kids = [t for t in made if frozenset((s, t)) in new]
    what = "makes " + ", ".join(NAME[t] for t in sorted(kids, key=lambda t: NAME[t])) if kids else "nothing new"
    figs.append(frame(f"take {NAME[s]} (f = {sum(fv[s])}): {what}", made, taken, now=s,
                      frontier=sorted(frontier, key=lambda t: sum(fv[t])), lines=lines | looked, new=new, fvals=fv))
    holds.append(5)
    lines |= looked
assert len(taken) == 5 and len(made) == 7
figs.append(frame("A* takes 5 states, breadth-first search 8; same 4-action plan", made, taken,
                  frontier=sorted(frontier, key=lambda t: sum(fv[t])), lines=lines, plan_states=set(PATH), fvals=fv))
holds.append(14)
make_gif(figs, here / "state_astar", fps=1, holds=holds, keys=[0, 2, 4, len(figs) - 1], cols=2, width=850)

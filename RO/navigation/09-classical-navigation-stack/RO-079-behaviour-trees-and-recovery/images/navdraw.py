"""Drawing helpers for this Note's figures (no output when run on its own): the whole room of RO-058 (walls, door,
table, cabinets, poles), the trolley and the person when present, the robot, a path; and a behaviour tree drawn as
an indented list, each node's box coloured by the status it returned in that tick (amber running, green success,
red failure, white not ticked)."""
import math

import bandkit as bk
import btkit as bt
import numpy as np
import plotly.graph_objects as go
from gifkit import BLUE, GREEN, GREY, ORANGE, RED

PINK = "#D6609A"
AMBER = "#F2B134"
COLOUR = {bt.RUNNING: AMBER, bt.SUCCESS: "#7BC86C", bt.FAILURE: "#F08080"}

# Nav2's names for the nodes of btkit.default_tree(), in walk order (the uid); "?" marks a condition
NAV2 = ["RecoveryNode (6 retries): NavigateRecovery", "PipelineSequence: NavigateWithReplanning",
        "5 selectors (planner, controller, checkers)", "RateController (1 Hz)",
        "RecoveryNode (1 retry): ComputePathToPose", "Fallback", "ReactiveSequence: CheckIfNewPathNeeded",
        "Inverter", "GlobalUpdatedGoal?", "IsGoalNearby? (under 4 m of path left)", "TruncatePathLocal",
        "ValidatePath?", "ComputePathToPose", "Sequence", "WouldAPlannerRecoveryHelp?", "ClearEntireCostmap (global)",
        "RecoveryNode (1 retry): FollowPath", "FollowPath", "Sequence", "WouldAControllerRecoveryHelp?",
        "ClearEntireCostmap (local)", "Sequence: recovery", "Fallback", "WouldAControllerRecoveryHelp?",
        "WouldAPlannerRecoveryHelp?", "ReactiveFallback: RecoveryFallback", "GoalUpdated?",
        "RoundRobin: RecoveryActions", "Sequence: ClearingActions", "ClearEntireCostmap (local)",
        "ClearEntireCostmap (global)", "Spin 1.57 rad", "Wait 5 s", "BackUp 0.30 m"]


def tree_rows(tree, names=None):
    """(uid, depth, parent uid, label) for every node, in walk order."""
    rows, stack = [], []
    for i, (n, _) in enumerate(tree.walk()):
        n.uid = i
    for n, d in tree.walk():
        stack = stack[:d]
        rows.append((n.uid, d, stack[-1] if stack else None, names[n.uid] if names else n.label))
        stack.append(n.uid)
    return rows


def lit_of(rec):
    """The status each node returned in this tick (the last one if it was ticked more than once) and the list of
    everything it returned in this tick."""
    lit, seq = {}, {}
    for lab, s, uid in rec["log"]:
        lit[uid] = s
        seq.setdefault(uid, []).append(s)
    return lit, seq


def draw_tree(fig, rows, lit, count=None, row=None, col=None, step=0.42, h=0.78, size=18, width=None, hide=()):
    """Draw the rows top-down (y = -index) in subplot (row, col); x = 0.42 per depth level."""
    kw = dict(row=row, col=col) if row else {}
    shown = [r for r in rows if r[0] not in hide]
    ypos = {r[0]: -i for i, r in enumerate(shown)}
    for uid, d, par, lab in shown:
        y = ypos[uid]
        x0 = d * step
        if par is not None and par in ypos:
            xp = (d - 1) * step + 0.12
            fig.add_trace(go.Scatter(x=[xp, xp, x0], y=[ypos[par] - h / 2, y, y], mode="lines",
                                     line=dict(color="#B0B0B0", width=1.5), hoverinfo="skip"), **kw)
        s = lit.get(uid)
        fill = COLOUR.get(s, "white")
        got = count.get(uid, [s]) if count else [s]
        text = lab + ("  (" + ", then ".join(x.lower() for x in got) + ")" if s else "")
        wd = width if width else 0.112 * len(text) + 0.3
        fig.add_shape(type="rect", x0=x0, x1=x0 + wd, y0=y - h / 2, y1=y + h / 2, fillcolor=fill,
                      line=dict(color="#555555" if s else "#B8B8B8", width=1.5), layer="below", opacity=1, **kw)
        fig.add_annotation(x=x0 + 0.1, y=y, text=text, showarrow=False, xanchor="left",
                           font=dict(size=size, color="black"), **kw)
    return len(shown)


def room(fig, row=None, col=None, trolley=False, person=None, labels=True):
    kw = dict(row=row, col=col) if row else {}
    W, H = bk.ROOM_W, bk.ROOM_H
    t = list(bk.TABLE) + [bk.TABLE[0]]
    fig.add_trace(go.Scatter(x=[p[0] for p in t], y=[p[1] for p in t], fill="toself", fillcolor="#D9D9D9",
                             line=dict(color="#9A9A9A", width=2), mode="lines", hoverinfo="skip"), **kw)
    for x0, x1, y0, y1 in bk.CAB:
        fig.add_trace(go.Scatter(x=[x0, x1, x1, x0, x0], y=[y0, y0, y1, y1, y0], fill="toself", fillcolor="#D9D9D9",
                                 line=dict(color="#9A9A9A", width=2), mode="lines", hoverinfo="skip"), **kw)
    for c in bk.POLES:
        a = np.linspace(0, 2 * math.pi, 30)
        fig.add_trace(go.Scatter(x=c[0] + bk.POLE_R * np.cos(a), y=c[1] + bk.POLE_R * np.sin(a), fill="toself",
                                 fillcolor="#9A9A9A", line=dict(color="#9A9A9A"), mode="lines", hoverinfo="skip"), **kw)
    for a, b in bk.WALLS:
        fig.add_trace(go.Scatter(x=[a[0], b[0]], y=[a[1], b[1]], mode="lines", line=dict(color="black", width=5),
                                 hoverinfo="skip"), **kw)
    if trolley:
        T = list(bt.TROLLEY) + [bt.TROLLEY[0]]
        fig.add_trace(go.Scatter(x=[p[0] for p in T], y=[p[1] for p in T], fill="toself", fillcolor="#8C6D46",
                                 line=dict(color="#5E4A2F", width=2), mode="lines", hoverinfo="skip"), **kw)
    if person is not None:
        a = np.linspace(0, 2 * math.pi, 40)
        fig.add_trace(go.Scatter(x=person[0] + bk.PERSON_R * np.cos(a), y=person[1] + bk.PERSON_R * np.sin(a),
                                 fill="toself", fillcolor=PINK, line=dict(color=PINK), mode="lines",
                                 hoverinfo="skip"), **kw)
    if labels:
        fig.add_annotation(x=4.25, y=1.75, text="table", showarrow=False, font=dict(size=17, color="#555555"), **kw)
        fig.add_annotation(x=6.6, y=3.0, text="cabinet", showarrow=False, font=dict(size=15, color="#555555"),
                           textangle=-90, **kw)
        fig.add_annotation(x=3.6, y=4.12, text="door", showarrow=False, font=dict(size=16, color=GREY), **kw)


def robot(fig, x, y, th, color="black", row=None, col=None, width=3):
    kw = dict(row=row, col=col) if row else {}
    a = np.linspace(0, 2 * math.pi, 40)
    fig.add_trace(go.Scatter(x=x + bk.R_BODY * np.cos(a), y=y + bk.R_BODY * np.sin(a), mode="lines", fill="toself",
                             fillcolor="rgba(255,255,255,0.7)", line=dict(color=color, width=width),
                             hoverinfo="skip"), **kw)
    fig.add_trace(go.Scatter(x=[x, x + bk.R_BODY * math.cos(th)], y=[y, y + bk.R_BODY * math.sin(th)],
                             mode="lines", line=dict(color=color, width=width + 1), hoverinfo="skip"), **kw)


def path(fig, P, color=BLUE, row=None, col=None, dash=None, width=3):
    kw = dict(row=row, col=col) if row else {}
    if P is not None:
        fig.add_trace(go.Scatter(x=P[:, 0], y=P[:, 1], mode="lines", line=dict(color=color, width=width, dash=dash),
                                 hoverinfo="skip"), **kw)


def goal(fig, g, row=None, col=None, color="#333333", text=None):
    kw = dict(row=row, col=col) if row else {}
    fig.add_trace(go.Scatter(x=[g[0]], y=[g[1]], mode="markers", marker=dict(symbol="x", size=14, color=color),
                             hoverinfo="skip"), **kw)
    if text:
        fig.add_annotation(x=g[0], y=g[1], text=text, showarrow=False, yshift=-18, font=dict(size=16, color=color),
                           **kw)


def track(fig, recs, upto, color="#999999", row=None, col=None):
    kw = dict(row=row, col=col) if row else {}
    xy = np.array([r["robot"][:2] for r in recs if r["t"] <= upto + 1e-9])
    if len(xy):
        fig.add_trace(go.Scatter(x=xy[:, 0], y=xy[:, 1], mode="lines", line=dict(color=color, width=2, dash="dot"),
                                 hoverinfo="skip"), **kw)


def at(recs, t):
    """The record of the tick at time t."""
    return min(recs, key=lambda r: abs(r["t"] - t))


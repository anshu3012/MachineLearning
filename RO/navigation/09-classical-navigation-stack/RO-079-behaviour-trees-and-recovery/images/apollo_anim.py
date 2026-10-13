"""Apollo's stop-sign scenario stepping through its stages, on our one-dimensional model (apollokit.py; the rules
that switch scenario and stage are copied from Apollo's code, the speeds are ours). Left: the crossing from above;
blue: our car, going up; orange: a car on the crossing road that stopped at its own stop line first; dark lines: the
stop lines; red dashed: the stop fence 1.0 m before our line; grey dashed: the creep fence 4.0 m past it. Right: the
scenario the manager has chosen and the stage that runs, with the rule that ends each stage and the numbers it
reads in that cycle. Run -> apollo_anim.gif, apollo_anim_frames.png"""
from pathlib import Path

import apollokit as ak
import plotly.graph_objects as go
from gifkit import BLUE, FONT, GREEN, GREY, ORANGE, make_gif
from plotly.subplots import make_subplots

here = Path(__file__).parent
OUT = ak.simulate(26.0)
EV = ak.events(OUT)
T_EV = [e[0] for e in EV]
assert T_EV == [0.0, 5.5, 7.4, 13.2, 17.0, 21.9]
AMBER = "#F2B134"
STAGES = [("PRE_STOP", "ends when stopped (0.2 m/s or less)\nat most 2.0 m before the line"),
          ("STOP", "ends after 1.0 s or more, once no watched\ncar is within 10.0 m of its line (or after 8.0 s)"),
          ("CREEP", "ends when 2.0 m past the line (or after 10.0 s)\nand nothing moving can reach the path\n"
                    "within 6.0 s, 5 cycles in a row"),
          ("INTERSECTION_CRUISE", "ends when the car's rear is 20.0 m\npast the line: the scenario is done")]
SCEN = ["EMERGENCY_PULL_OVER", "EMERGENCY_STOP", "VALET_PARKING", "BARE_INTERSECTION_UNPROTECTED",
        "STOP_SIGN_UNPROTECTED", "YIELD_SIGN", "TRAFFIC_LIGHT_UNPROTECTED_LEFT_TURN",
        "TRAFFIC_LIGHT_UNPROTECTED_RIGHT_TURN", "TRAFFIC_LIGHT_PROTECTED", "PULL_OVER", "PARK_AND_GO", "LANE_FOLLOW"]


def rect(fig, x0, x1, y0, y1, color, col=1, width=2, fill=None, dash=None):
    fig.add_trace(go.Scatter(x=[x0, x1, x1, x0, x0], y=[y0, y0, y1, y1, y0], mode="lines", fill="toself" if fill else None,
                             fillcolor=fill, line=dict(color=color, width=width, dash=dash), hoverinfo="skip"),
                  row=1, col=col)


def status_line(r):
    s = f"t = {r['t']:.1f} s, speed {r['v']:.2f} m/s, front {abs(r['s']):.2f} m {'before' if r['s'] < 0 else 'past'}" \
        " the line"
    extra = []
    if r["stage"] in ("PRE_STOP", "STOP"):
        extra.append("watch list: " + (", ".join(r["watch"]) if r["watch"] else "empty"))
    if r["stage"] == "STOP":
        extra.append(f"stopped for {r['stop_wait']:.1f} s; crossing car {abs(r['cross'] + ak.L_EGO / 2 - ak.CROSS_LINE):.1f} m"
                     " from its line")
    if r["stage"] == "CREEP":
        extra.append(f"creeping for {r['creep_wait']:.1f} s; clear cycles in a row: {r['clear']}")
    if r["stage"] == "INTERSECTION_CRUISE":
        rear = r["s"] - ak.L_EGO
        extra.append(f"rear {abs(rear):.1f} m {'past' if rear >= 0 else 'before'} the line")
    return "<br>".join([s] + extra)


def frame(t):
    r = min(OUT, key=lambda q: abs(q["t"] - t))
    fig = make_subplots(rows=1, cols=2, column_widths=[0.4, 0.6], horizontal_spacing=0.02)
    # the crossing
    rect(fig, -3.5, 3.5, -30, 30, "#E2E2E2", fill="#E2E2E2", width=0)
    rect(fig, -30, 30, 1.0, 8.0, "#E2E2E2", fill="#E2E2E2", width=0)
    fig.add_trace(go.Scatter(x=[0, 0], y=[-30, 1], mode="lines", line=dict(color="white", width=2, dash="dash")))
    fig.add_trace(go.Scatter(x=[0, 0], y=[8, 30], mode="lines", line=dict(color="white", width=2, dash="dash")))
    fig.add_trace(go.Scatter(x=[3.5, 30], y=[4.5, 4.5], mode="lines", line=dict(color="white", width=2, dash="dash")))
    fig.add_trace(go.Scatter(x=[-30, -3.5], y=[4.5, 4.5], mode="lines", line=dict(color="white", width=2, dash="dash")))
    fig.add_trace(go.Scatter(x=[0, 3.5], y=[0, 0], mode="lines", line=dict(color="#333333", width=5)))
    fig.add_trace(go.Scatter(x=[ak.CROSS_LINE] * 2, y=[4.5, 8.0], mode="lines", line=dict(color="#333333", width=5)))
    for x, y in ((4.4, -0.8), (ak.CROSS_LINE + 0.6, 8.9)):
        fig.add_trace(go.Scatter(x=[x], y=[y], mode="markers", marker=dict(symbol="octagon", size=16, color="#D62728")))
    if r["stage"] in ("PRE_STOP", "STOP") or (r["scenario"] == "LANE_FOLLOW" and r["t"] < T_EV[-1]):
        fig.add_trace(go.Scatter(x=[0, 3.5], y=[ak.FENCE] * 2, mode="lines", line=dict(color="#D62728", width=3,
                                                                                         dash="dash")))
    if r["stage"] == "CREEP":
        fig.add_trace(go.Scatter(x=[0, 3.5], y=[ak.CREEP_TARGET] * 2, mode="lines", line=dict(color=GREY, width=3,
                                                                                                dash="dash")))
    rect(fig, 1.75 - ak.W_EGO / 2, 1.75 + ak.W_EGO / 2, r["s"] - ak.L_EGO, r["s"], BLUE, fill="rgba(76,120,168,0.55)")
    fx = r["cross"]
    rect(fig, fx, fx + ak.L_EGO, ak.CROSS_Y - ak.W_EGO / 2, ak.CROSS_Y + ak.W_EGO / 2, ORANGE,
         fill="rgba(245,133,24,0.55)")
    # the manager and the stages
    fig.add_annotation(x=0.2, y=21.3, xref="x2", yref="y2", text="<b>Scenario manager</b>, every 0.1 s: the first that "
                       "applies, in this order;<br>a running scenario is kept unless one above it applies", showarrow=False, xanchor="left", align="left",
                       font=dict(size=18))
    for i, name in enumerate(SCEN):
        on = name == r["scenario"]
        fig.add_annotation(x=0.4, y=19.85 - 0.62 * i, xref="x2", yref="y2", text=("<b>" + name + "</b>") if on else name,
                           showarrow=False, xanchor="left", font=dict(size=16, color="black" if on else GREY),
                           bgcolor=AMBER if on else "white")
    fig.add_annotation(x=0.2, y=12.35, xref="x2", yref="y2", text="<b>Stages of STOP_SIGN_UNPROTECTED</b>",
                       showarrow=False, xanchor="left", font=dict(size=18))
    for i, (name, rule) in enumerate(STAGES):
        y = 10.75 - 2.5 * i
        on = name == r["stage"]
        done = r["stage"] is not None and [s[0] for s in STAGES].index(r["stage"]) > i if r["stage"] else \
            r["t"] >= T_EV[-1]
        fill = AMBER if on else ("#A8D5A0" if done else "white")
        rect(fig, 0.3, 9.7, y - 1.1, y + 1.1, "#555555" if on else "#B8B8B8", col=2, fill=fill, width=2)
        fig.add_annotation(x=0.5, y=y + 0.62, xref="x2", yref="y2", text="<b>" + name + "</b>", showarrow=False,
                           xanchor="left", font=dict(size=17))
        fig.add_annotation(x=0.5, y=y - 0.28, xref="x2", yref="y2", text=rule.replace("\n", "<br>"), showarrow=False,
                           xanchor="left", font=dict(size=15.5), align="left")
        if i < 3:
            fig.add_annotation(x=5.0, y=y - 1.4, ax=5.0, ay=y - 1.1, xref="x2", yref="y2", axref="x2", ayref="y2",
                               text="", showarrow=True, arrowhead=2, arrowwidth=2, arrowcolor="#555555")
    fig.add_annotation(x=0.2, y=2.0, xref="x2", yref="y2", text=status_line(r), showarrow=False, xanchor="left",
                       yanchor="top", align="left", font=dict(size=17))
    fig.update_xaxes(range=[-8, 12], visible=False, row=1, col=1)
    fig.update_yaxes(range=[-23, 28], visible=False, scaleanchor="x", scaleratio=1, row=1, col=1)
    fig.update_xaxes(range=[0, 10], visible=False, row=1, col=2)
    fig.update_yaxes(range=[-1.5, 21.9], visible=False, row=1, col=2)
    fig.update_layout(template="simple_white", font=FONT, width=980, height=1000, showlegend=False,
                      margin=dict(l=8, r=8, t=8, b=8))
    return fig


T = sorted(set([round(3.0 + 0.5 * k, 1) for k in range(40)] + T_EV[1:]))
T = [t for t in T if t <= 22.5]
holds = [6 if t in T_EV else 1 for t in T]
holds[-1] = 12
keys = [T.index(5.5), T.index(10.5), T.index(17.0), len(T) - 1]
figs = [frame(t) for t in T]
make_gif(figs, here / "apollo_anim", fps=4, holds=holds, keys=sorted(set(keys)), cols=2, width=760)
for e in EV:
    print(e)

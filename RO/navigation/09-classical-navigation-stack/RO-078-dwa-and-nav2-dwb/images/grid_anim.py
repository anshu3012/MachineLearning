"""The two distance grids of the map-grid critics in the person's cycle (t = 2.4 s), filled out from their source
cells in order of distance (costmap_queue: 4 neighbours, each cell keeps its Manhattan distance, in cells, to the
source that reached it first). Top: from every cell of the local plan (PathDist, PathAlign). Bottom: from the
local plan's last cell on the costmap (GoalDist). One frame per 3 cells of distance. Last frame: the chosen
rollout ends on a cell worth 0 on the top grid and 21 on the bottom grid. Run -> grid_anim.gif,
grid_anim_frames.png"""
import dwbkit as d
import numpy as np
import plotly.graph_objects as go
import roomdraw as rd
from gifkit import BLUE, FONT, ORANGE, make_gif
from plotly.subplots import make_subplots

R = d.results()
o = [c for c in R["replan"]["cycles"] if abs(c["t"] - d.T_PERSON) < 1e-9][0]
cm, rec = o["cm"], o["rec"]
cr = d.Critics()
cr.prepare(cm, o["x"].copy(), (o["v"], o["w"]), d.GOAL, o["local"])
end = rec["traj"][-1]
ie, je, _ = cm.world_to_map(end[0], end[1])
PG, GG = cr.path_grid, cr.goal_grid
assert PG[je, ie] == 0 and GG[je, ie] == 21
gc = cr.goal_cell
xs = cm.ox + (np.arange(cm.n) + 0.5) * cm.res
ys = cm.oy + (np.arange(cm.n) + 0.5) * cm.res
cells = d.plan_cells(cm, o["local"])
SCALE = [[0, "#08306B"], [0.3, "#4292C6"], [0.6, "#9ECAE1"], [1, "#F7FBFF"]]


def frame(D, final=False):
    fig = make_subplots(rows=2, cols=1, vertical_spacing=0.06,
                        subplot_titles=["distance from the local plan's cells (PathDist)",
                                        "distance from the plan's last cell on the costmap (GoalDist)"])
    for r, G in ((1, PG), (2, GG)):
        Z = np.where(G <= D, G, np.nan)
        fig.add_trace(go.Heatmap(x=xs, y=ys, z=Z, zmin=0, zmax=60, colorscale=SCALE, showscale=(r == 1),
                                 colorbar=dict(title=dict(text="cells", side="right"), len=0.4, y=0.8, thickness=16)),
                      row=r, col=1)
        t = list(d.TABLE) + [d.TABLE[0]]
        fig.add_trace(go.Scatter(x=[p[0] for p in t], y=[p[1] for p in t], mode="lines",
                                 line=dict(color="#555555", width=2)), row=r, col=1)
        tt = np.linspace(0, 2 * np.pi, 60)
        fig.add_trace(go.Scatter(x=d.PERSON[0] + d.PERSON_R * np.cos(tt), y=d.PERSON[1] + d.PERSON_R * np.sin(tt),
                                 mode="lines", line=dict(color="#C2185B", width=2)), row=r, col=1)
        src = cells if r == 1 else [gc]
        fig.add_trace(go.Scatter(x=[xs[i] for i, j in src], y=[ys[j] for i, j in src], mode="markers",
                                 marker=dict(size=6 if r == 1 else 12, color=ORANGE, symbol="square")),
                      row=r, col=1)
        rd.robot(fig, o["x"][0], o["x"][1], o["x"][2], BLUE, rc=(r, 1), fill="rgba(0,0,0,0)")
        if final:
            rd.arcs(fig, [rec["traj"]], BLUE, rc=(r, 1), width=4)
            val = int(G[je, ie])
            fig.add_annotation(x=end[0], y=end[1], xref=f"x{r}", yref=f"y{r}", text=f"<b>{val}</b> cells",
                               ax=-110, ay=-10, font=dict(size=19, color=BLUE), arrowcolor=BLUE,
                               bgcolor="rgba(255,255,255,0.9)")
        fig.update_xaxes(range=[cm.ox, cm.ox + 3], row=r, col=1, visible=False)
        fig.update_yaxes(range=[cm.oy, cm.oy + 3], row=r, col=1, visible=False, scaleanchor=f"x{r}")
    fig.add_annotation(x=0.5, y=-0.02, xref="paper", yref="paper", showarrow=False, font=dict(size=19),
                       text=("filled out to " + (f"{D} cells" if not final else "every cell")
                             + ": orange = source cells; one cell = 0.05 m"))
    for a in fig.layout.annotations[:2]:
        a.font.size = 19
    fig.update_layout(template="simple_white", font=FONT, width=800, height=1480, showlegend=False,
                      margin=dict(l=20, r=20, t=50, b=50))
    return fig


Ds = list(range(0, 46, 3))
figs = [frame(D) for D in Ds] + [frame(200, final=True)]
holds = [3] + [1] * (len(Ds) - 1) + [14]
make_gif(figs, "grid_anim", fps=3, holds=holds, keys=[2, 6, 11, len(figs) - 1], cols=2)

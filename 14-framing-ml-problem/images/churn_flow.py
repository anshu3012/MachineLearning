"""Section 3.1: a customer base works like a population. Example numbers: 1,000 users, 4 percent leave every month.
Left panel: 50 new users join each month (more than leave), so the base grows. Right panel: 30 join (fewer than leave),
so it shrinks. Each frame adds one month: users next month = users - 4 percent of users + new users.
Plotly frames (a line growing month by month) -> GIF, plus a key-frame grid for the PDF."""
from pathlib import Path
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from gifkit import save_gif

HERE = Path(__file__).parent
GREEN, RED, BLUE = "#54A24B", "#E45756", "#4C78A8"
MONTHS, CHURN = 12, 0.04


def run(joins):
    users, left = [1000.0], []
    for _ in range(MONTHS):
        left.append(CHURN * users[-1])
        users.append(users[-1] - left[-1] + joins)
    return users, left


RUNS = [(50, *run(50)), (30, *run(30))]


def frame(m):
    fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.12,
                        subplot_titles=[f"{j} join each month: " + ("the base grows" if j == 50 else "the base shrinks") for j, _, _ in RUNS])
    for c, (joins, users, left) in enumerate(RUNS, start=1):
        fig.add_scatter(x=list(range(m + 1)), y=users[:m + 1], mode="lines+markers", line=dict(color=BLUE, width=4),
                        marker=dict(size=9), showlegend=False, row=1, col=c)
        text = "start: 1,000 users" if m == 0 else f"month {m}: {left[m - 1]:.0f} left, {joins} joined<br><b>{users[m]:,.0f} users</b>"
        fig.add_annotation(x=6, y=1235, text=text, showarrow=False, font=dict(size=20, color=GREEN if joins == 50 else RED), row=1, col=c)
        fig.update_xaxes(title="month", range=[-0.5, MONTHS + 0.5], dtick=2, row=1, col=c)
        fig.update_yaxes(title="users" if c == 1 else None, range=[800, 1280], showgrid=True, row=1, col=c)
    fig.add_hline(y=1000, line=dict(color="#9A9A9A", dash="dot"))
    fig.update_layout(template="simple_white", width=1100, height=540, font=dict(family="Latin Modern Roman", size=18),
                      title=dict(text="Monthly churn rate 4 percent in both panels (example numbers)", x=0.5),
                      margin=dict(l=80, r=30, t=110, b=70))
    fig.update_annotations(font_size=20)
    return fig


if __name__ == "__main__":
    save_gif([frame(m) for m in range(MONTHS + 1)], "churn_flow", HERE, keys=[1, 4, 8, 12], fps=1.5)
    print([round(u[-1]) for _, u, _ in RUNS], [round(l[0]) for _, _, l in RUNS])

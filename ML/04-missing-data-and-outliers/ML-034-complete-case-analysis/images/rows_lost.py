"""Why the losses add up: complete case analysis on the job data (19,158 rows), adding the five chosen columns one at a
time. Each column alone is missing at most 4 percent, but a row is dropped if any chosen column has a gap, so the rows
kept fall to 17,182 (89.7 percent). Plotly frames -> GIF."""
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go
from anim import save_gif, FONT, BLUE, RED

here = Path(__file__).parent
df = pd.read_csv(here.parent / "data" / "data_science_job.csv.gz")
cols = ["experience", "enrolled_university", "education_level", "city_development_index", "training_hours"]
kept = [len(df)] + [len(df.dropna(subset=cols[:k])) for k in range(1, 6)]
alone = [df[c].isnull().mean() for c in cols]
assert kept[-1] == 17_182 and len(df) == 19_158 and max(alone) < 0.05


def frame(k):
    labels = ["all rows"] + [f"+ {c}" for c in cols]
    y = [100 * v / len(df) for v in kept[:k + 1]]
    fig = go.Figure(go.Bar(x=labels[:k + 1], y=y, marker_color=[BLUE] + [RED] * k,
                           text=[f"{v:,} rows<br>{p:.1f}%" for v, p in zip(kept[:k + 1], y)], textposition="outside",
                           textfont=dict(size=17)))
    head = "19,158 job applicants" if k == 0 else (f"adding <b>{cols[k - 1]}</b> ({100 * alone[k - 1]:.1f}% missing alone):"
                                                      f" {kept[k - 1] - kept[k]:,} more rows dropped")
    fig.update_layout(template="simple_white", width=1300, height=560, font=FONT, title=dict(text=head, x=0.5),
                      xaxis=dict(range=[-0.5, 5.5], tickangle=-20), yaxis=dict(title="rows kept (percent)", range=[80, 104]),
                      margin=dict(l=90, r=30, t=80, b=110))
    return fig


if __name__ == "__main__":
    save_gif([frame(k) for k in range(6)], "rows_lost", here, keys=[1, 5], fps=1, holds=[3, 2, 2, 2, 2, 6], cols=1, width=950)

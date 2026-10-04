"""Section 8: a box plot built step by step from the 714 known Titanic ages: sorted dots, the median, the box from Q1 to Q3,
the fences 1.5 IQR beyond the box, the whiskers to the last value inside each fence, and the outliers beyond.
Plotly frames (parts appearing one at a time) -> GIF, plus a key-frame grid for the PDF."""
from pathlib import Path
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from gifkit import save_gif

HERE = Path(__file__).parent
BLUE, RED, ORANGE, GREY = "#4C78A8", "#E45756", "#F58518", "#6B6B6B"
age = pd.read_csv(HERE.parent / "data" / "titanic_train.csv")["Age"].dropna().sort_values().to_numpy()
q1, med, q3 = np.quantile(age, [0.25, 0.5, 0.75])
iqr = q3 - q1
lo_f, hi_f = q1 - 1.5 * iqr, q3 + 1.5 * iqr
lo_w, hi_w = age[age >= lo_f].min(), age[age <= hi_f].max()
out = age[(age < lo_f) | (age > hi_f)]
jit = np.random.default_rng(0).uniform(-0.3, 0.3, len(age))      # spread the dots up and down so they do not hide each other


def frame(step, title):
    fig = go.Figure()
    is_out = np.isin(age, out) & (step >= 5)
    fig.add_scatter(x=age[~is_out], y=jit[~is_out] - 1, mode="markers", marker=dict(color=BLUE, size=5, opacity=0.45))
    fig.add_scatter(x=age[is_out], y=jit[is_out] - 1, mode="markers", marker=dict(color=RED, size=7))

    def vline(x, text, colour=BLUE, dash="solid", y0=0.6, y1=1.4, ty=1.62):
        fig.add_scatter(x=[x, x], y=[y0, y1], mode="lines", line=dict(color=colour, width=4, dash=dash))
        fig.add_annotation(x=x, y=ty, text=text, showarrow=False, font=dict(size=21, color=colour))

    if step >= 1:
        vline(med, f"median {med:.0f}", ty=1.9)
    if step >= 2:
        fig.add_scatter(x=[q1, q3, q3, q1, q1], y=[0.6, 0.6, 1.4, 1.4, 0.6], mode="lines", fill="toself", line=dict(color=BLUE, width=4), fillcolor="rgba(76,120,168,0.18)")
        fig.add_annotation(x=q1, y=1.62, text=f"Q1 {q1:.1f}", showarrow=False, xanchor="right", font=dict(size=21, color=BLUE))
        fig.add_annotation(x=q3, y=1.62, text=f"Q3 {q3:.0f}", showarrow=False, xanchor="left", font=dict(size=21, color=BLUE))
    if step >= 3:
        vline(lo_f, f"lower fence {lo_f:.2f}", ORANGE, "dash", 0.3, 1.7, 0.1)
        vline(hi_f, f"upper fence {hi_f:.2f}", ORANGE, "dash", 0.3, 1.7, 0.1)
    if step >= 4:
        for a, b, name in [(q1, lo_w, f"whisker ends at {lo_w:.2f}"), (q3, hi_w, f"whisker ends at {hi_w:.0f}")]:
            fig.add_scatter(x=[a, b, None, b, b], y=[1, 1, None, 0.8, 1.2], mode="lines", line=dict(color=BLUE, width=4))
            fig.add_annotation(x=b, y=2.2, text=name, showarrow=False, xanchor="left" if b < 30 else "right", font=dict(size=21, color=GREY))
    if step >= 5:
        fig.add_scatter(x=out, y=np.ones(len(out)), mode="markers", marker=dict(color=RED, size=10))
        fig.add_annotation(x=74, y=1.35, text=f"{len(out)} outliers", showarrow=False, font=dict(size=21, color=RED))
    fig.update_layout(template="simple_white", width=1000, height=560, showlegend=False, font=dict(family="Latin Modern Roman", size=19),
                      title=dict(text=title, x=0.5), xaxis=dict(title="Age (years)", range=[-12, 86], dtick=10),
                      yaxis=dict(visible=False, range=[-1.6, 2.5]), margin=dict(l=30, r=30, t=90, b=70))
    return fig


if __name__ == "__main__":
    figs = [frame(0, "714 ages, each a dot (minimum 0.42, maximum 80)"),
            frame(1, "The median: half of the ages on each side"),
            frame(2, "The box: from Q1 to Q3, the middle half of the ages"),
            frame(3, "The fences: 1.5 IQR beyond each edge of the box"),
            frame(4, "Each whisker runs to the last age inside its fence"),
            frame(5, "Ages beyond a fence are drawn as dots: possible outliers")]
    save_gif(figs, "box_build", HERE, keys=[1, 2, 3, 5], fps=0.7)
    print(q1, med, q3, lo_f, hi_f, lo_w, hi_w, len(out))

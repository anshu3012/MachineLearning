"""The exact binomial test for 26 men out of 60 under H0: share of men = 0.5. Bars: the binomial PMF B(60, 0.5).
Frame 1: every possible count of men. Frame 2: the observed count, 26. Frame 3: every count that is as rare as 26 or
rarer, on both sides; their bars add up to the p-value, 0.37.
Tool: Plotly frames -> GIF (bars changing colour). Idea after StatQuest, "The Binomial Distribution and Test"."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from scipy import stats
from gifkit import make_gif, FONT, BLUE, RED

here = Path(__file__).parent
N, K = 60, 26
k = np.arange(N + 1)
pmf = stats.binom.pmf(k, N, 0.5)
rare = pmf <= pmf[K] * (1 + 1e-7)                       # as rare as the observed count, or rarer
p_value = pmf[rare].sum()
assert np.isclose(p_value, stats.binomtest(K, N, 0.5).pvalue) and round(p_value, 2) == 0.37
PALE = "#c9d6e6"


def frame(step):
    colours = [PALE] * (N + 1)
    if step == 1:
        colours[K] = RED
    if step == 2:
        colours = [RED if r else PALE for r in rare]
    fig = go.Figure(go.Bar(x=k, y=pmf, marker_color=colours if step else BLUE))
    head = ["If men and women are equally common: how many men in 60 people?",
            f"Our sample: 26 men. P(exactly 26) = {pmf[K]:.3f}",
            f"All counts as rare as 26 or rarer, both sides: p = {p_value:.2f}"][step]
    if step == 2:
        fig.add_annotation(x=20, y=0.075, text="26 or fewer<br>" + f"{pmf[:K + 1].sum():.3f}", showarrow=False,
                           font=dict(size=22, color=RED))
        fig.add_annotation(x=40, y=0.075, text="34 or more<br>" + f"{pmf[N - K:].sum():.3f}", showarrow=False,
                           font=dict(size=22, color=RED))
    fig.update_layout(template="simple_white", width=1000, height=560, font=FONT, showlegend=False, bargap=0.15,
                      title=dict(text=head, x=0.5), xaxis=dict(title="number of men in 60", range=[9.5, 50.5]),
                      yaxis=dict(title="probability", range=[0, 0.115]), margin=dict(l=80, r=30, t=70, b=70))
    return fig


if __name__ == "__main__":
    make_gif([frame(s) for s in range(3)], here / "binomial_exact", fps=1, holds=[3, 3, 6], keys=[1, 2], cols=1)

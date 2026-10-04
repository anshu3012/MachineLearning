"""Mean normalization in two steps on the Note's five weights: subtract the mean (68.6) so the centre sits at 0,
then divide by the range (98) so the values land between -1 and 1. Plotly frames -> GIF."""
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
from anim import save_gif, FONT, BLUE, RED, GREY

here = Path(__file__).parent
w = np.array([32, 54, 60, 67, 130.0])
m, r = w.mean(), np.ptp(w)
assert m == 68.6 and r == 98
out = (w - m) / r
assert np.allclose(out[[0, 4]], [-0.3735, 0.6265], atol=1e-4)
STEPS = [(w, "The five weights (kg)", "mean 68.6", m), (w - m, "Step 1: subtract the mean 68.6", "centre now at 0", 0),
         (out, "Step 2: divide by the range 98", "values between −1 and 1", 0)]


def frame(v, head, note, centre, xr):
    fig = go.Figure()
    fig.add_vline(x=centre, line=dict(color=RED, width=3, dash="dash"))
    fig.add_annotation(x=centre, y=0.9, text=note, showarrow=False, xanchor="left", xshift=8, font=dict(size=20, color=RED))
    fig.add_scatter(x=v, y=[0.3] * 5, mode="markers+text", marker=dict(size=22, color=BLUE),
                    text=[f"{x:.3f}".rstrip("0").rstrip(".") if abs(x) < 1 else f"{x:.3g}" for x in v],
                      textposition=["bottom center", "top center", "bottom center", "top center", "bottom center"], textfont=dict(size=19))
    fig.update_layout(template="simple_white", width=1100, height=380, font=FONT, showlegend=False,
                      title=dict(text=f"<b>{head}</b>", x=0.5), xaxis=dict(range=xr, zeroline=True, zerolinewidth=2),
                      yaxis=dict(visible=False, range=[-0.4, 1.1]), margin=dict(l=30, r=30, t=70, b=60))
    return fig


if __name__ == "__main__":
    figs = [frame(*STEPS[0], [-45, 140]), frame(*STEPS[1], [-45, 140]), frame(*STEPS[1], [-1.1, 1.1]),
            frame(*STEPS[2], [-1.1, 1.1])]
    figs[2].update_layout(title_text="<b>Zoom in: the same values, axis −1 to 1</b>")
    save_gif(figs, "mean_norm_steps", here, keys=[0, 1, 3], fps=1, holds=[3, 3, 2, 6], cols=1, width=860)

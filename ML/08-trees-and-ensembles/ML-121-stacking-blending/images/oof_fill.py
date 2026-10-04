"""K-fold stacking with K = 4, one fit per frame (Plotly frames -> GIF). A schematic of section 7: the 800 training
observations sit in 4 folds of 200. Each fit trains one base model on three folds (grey) and predicts the fourth
(orange); the predicted fold fills one cell of that model's out-of-fold column (blue). After 12 fits the three
columns are full and the meta-model is trained on them. No data: the picture is the procedure itself."""
from pathlib import Path
import plotly.graph_objects as go
from gifkit import BLUE, FONT, GREY, ORANGE, make_gif

here = Path(__file__).parent
MODELS = [("linear regression", "LR pred."), ("decision tree", "DT pred."), ("KNN", "KNN pred.")]
K = 4


def box(fig, x0, x1, y0, y1, fill, text, colour="black"):
    fig.add_shape(type="rect", x0=x0, x1=x1, y0=y0, y1=y1, fillcolor=fill, line=dict(color="black", width=1.5), opacity=1)
    fig.add_annotation(x=(x0 + x1) / 2, y=(y0 + y1) / 2, text=text, showarrow=False, font=dict(size=19, color=colour))


def frame(step):
    """step 0..11: one fit; step 12: everything filled, meta-model trained."""
    fig = go.Figure()
    m, j = divmod(min(step, 11), K)
    held = K - 1 - j                                           # fold 4 is predicted first, as in the Note
    done = step == 12
    for f in range(K):                                         # left: the folds of D_train
        y1 = K - f
        if done:
            fill, txt, col = "#E8E8E8", f"fold {f + 1}", "black"
        elif f == held:
            fill, txt, col = ORANGE, f"fold {f + 1}: predict", "black"
        else:
            fill, txt, col = "#C9C9C9", f"fold {f + 1}: train", "black"
        box(fig, 0, 3.2, y1 - 0.9, y1, fill, txt, col)
    for c, (_, colname) in enumerate(MODELS):                  # right: the meta-model's dataset
        x0 = 4.6 + c * 1.7
        fig.add_annotation(x=x0 + 0.8, y=K + 0.3, text=colname, showarrow=False, font=dict(size=19))
        for f in range(K):
            filled = done or c < m or (c == m and f >= held)
            new = (not done) and c == m and f == held
            box(fig, x0, x0 + 1.6, K - f - 0.9, K - f, ORANGE if new else (BLUE if filled else "white"),
                "200" if filled else "", "white" if filled and not new else "black")
    if not done:
        fig.add_annotation(x=4.6 + m * 1.7, y=K - held - 0.45, ax=3.2, ay=K - held - 0.45, xref="x", yref="y", axref="x", ayref="y",
                           arrowhead=3, arrowwidth=3, arrowcolor=ORANGE, text="")
        others = ", ".join(str(f + 1) for f in range(K) if f != held)
        title = f"fit {step + 1} of 12: train {MODELS[m][0]} on folds {others}, predict fold {held + 1}"
    else:
        title = "3 columns of 800 out-of-fold predictions: train the meta-model on them"
    fig.add_annotation(x=1.6, y=K + 0.3, text="training set: 800 observations", showarrow=False, font=dict(size=19))
    fig.add_annotation(x=7.15, y=-0.35, text="the meta-model's training data", showarrow=False, font=dict(size=19, color=GREY))
    fig.update_xaxes(range=[-0.2, 9.9], visible=False)
    fig.update_yaxes(range=[-0.7, K + 0.7], visible=False)
    fig.update_layout(template="simple_white", width=1100, height=520, font=FONT, margin=dict(l=20, r=20, t=80, b=10),
                      title=dict(text=title, x=0.5, y=0.95, font=dict(size=24)))
    return fig


if __name__ == "__main__":
    make_gif([frame(s) for s in range(13)], here / "oof_fill", fps=1, holds=[2] * 12 + [5], keys=[5, 12], cols=1)

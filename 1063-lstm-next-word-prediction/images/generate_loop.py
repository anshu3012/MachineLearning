"""Section 8.2's generation loop for the prompt "the wolf" (data/generated.csv, seed 0): predict a word, append it,
feed the longer text back in. The new word is green.
Plotly frames -> GIF, plus a key-frame grid for the PDF."""
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go
from gifkit import save_gif

HERE = Path(__file__).parent
FONT = dict(family="Latin Modern Roman", size=26)
G = pd.read_csv(HERE.parent / "data" / "generated.csv").set_index("prompt")
PROMPT = "the wolf"
NEW = G.loc[PROMPT, "generated"].split()
assert NEW[:4] == ["was", "very", "angry", "and"] and len(NEW) == 10


def frame(k):
    """k words generated so far (k = 0: the prompt alone)."""
    old = PROMPT.split() + NEW[:max(k - 1, 0)]
    words = [(w, "black") for w in old] + ([(NEW[k - 1], "#54A24B")] if k else [])
    text = " ".join(f"<span style='color:{c}'>{'<b>' + w + '</b>' if c != 'black' else w}</span>" for w, c in words)
    fig = go.Figure()
    fig.add_annotation(x=0.5, y=0.62, xref="paper", yref="paper", text=text, showarrow=False, font=dict(size=30))
    step = ("the prompt" if k == 0 else
            f"step {k}: the model read the {len(old)} words before it and predicted <b>{NEW[k - 1]}</b>")
    fig.add_annotation(x=0.5, y=0.3, xref="paper", yref="paper", text=step, showarrow=False, font=dict(size=22, color="#6B6B6B"))
    loop = "append it, then feed the longer text back in" if 0 < k < 10 else ("" if k == 0 else "10 words written, one prediction at a time")
    fig.add_annotation(x=0.5, y=0.12, xref="paper", yref="paper", text=loop, showarrow=False, font=dict(size=22, color="#4C78A8"))
    fig.update_layout(template="simple_white", width=1100, height=300, font=FONT, xaxis=dict(visible=False),
                      yaxis=dict(visible=False), margin=dict(l=10, r=10, t=10, b=10))
    return fig


if __name__ == "__main__":
    save_gif([frame(k) for k in range(11)], "generate_loop", HERE, keys=[3, 10], fps=1.2, cols=1,
             holds=[2] + [1] * 9 + [5])

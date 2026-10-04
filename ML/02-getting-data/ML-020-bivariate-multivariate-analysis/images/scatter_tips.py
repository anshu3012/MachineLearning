"""Tips: total bill vs tip (bivariate), then one more column per frame: sex as colour, smoker as marker shape,
party size as dot size (multivariate). Plotly frames (encodings added one at a time) -> GIF, plus a key-frame grid for the PDF."""
import plotly.graph_objects as go
from common import load, layout, here, BLUE, ORANGE, GREY
from gifkit import save_gif

tips = load("tips")


def frame(step, title):
    fig = go.Figure()
    groups = [(None, None)] if step == 0 else [(s, k) for s in ("Male", "Female") for k in (("No", "Yes") if step >= 2 else (None,))]
    for sex, smoker in groups:
        d = tips if sex is None else tips[tips.sex == sex]
        d = d if smoker is None else d[d.smoker == smoker]
        name = "all bills" if sex is None else sex.lower() + ("" if smoker is None else (", smoker" if smoker == "Yes" else ", non-smoker"))
        fig.add_scatter(x=d.total_bill, y=d.tip, mode="markers", name=name,
                        marker=dict(color=GREY if sex is None else (BLUE if sex == "Male" else ORANGE), opacity=0.75,
                                    symbol="x" if smoker == "Yes" else "circle", size=d["size"] * 4 + 3 if step >= 3 else 10))
    layout(fig, title, "Total bill (US dollars)", "Tip (US dollars)", width=1000, height=600, showlegend=step > 0,
           legend=dict(x=0.01, y=0.99, bgcolor="rgba(255,255,255,0.7)"))
    fig.update_xaxes(range=[0, 53], showgrid=True)
    fig.update_yaxes(range=[0, 10.8], showgrid=True)
    return fig


if __name__ == "__main__":
    figs = [frame(0, "244 restaurant bills: 2 columns (bill, tip)"),
            frame(1, "Colour shows sex: 3 columns"),
            frame(2, "Marker shape shows smoker: 4 columns"),
            frame(3, "Dot size shows party size (1 to 6): 5 columns")]
    save_gif(figs, "scatter_tips", here, keys=[0, 1, 2, 3], fps=0.6)

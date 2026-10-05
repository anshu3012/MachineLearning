"""pd.get_dummies on the first four cars, step by step: fuel becomes 4 columns, owner becomes 5 (12 columns in all),
then drop_first removes fuel_CNG and owner_First Owner (10 columns). Plotly table frames -> GIF."""
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go
from anim import save_gif, FONT

here = Path(__file__).parent
df = pd.read_csv(here.parent / "data" / "cars.csv")
full = pd.get_dummies(df, columns=["fuel", "owner"], dtype=int)
k1 = pd.get_dummies(df, columns=["fuel", "owner"], drop_first=True, dtype=int)
assert full.shape == (8128, 12) and k1.shape == (8128, 10)
one = pd.get_dummies(df, columns=["fuel"], dtype=int)
SHORT = {"owner_First Owner": "own_1st", "owner_Second Owner": "own_2nd", "owner_Third Owner": "own_3rd",
         "owner_Fourth & Above Owner": "own_4th+", "owner_Test Drive Car": "own_test"}
HOT = "#F58518"


def frame(t, head, new):
    t = t.head(4).drop(columns="selling_price")
    cols = list(t.columns)
    fill = [["#ffe2c4" if (c in new and v == 1) else ("#eef3f9" if c in new else "white") for v in t[c]] for c in cols]
    fig = go.Figure(go.Table(columnwidth=[1.3 if c in ("brand", "km_driven", "fuel", "owner") else 1 for c in cols],
                             header=dict(values=[SHORT.get(c, c) for c in cols], fill_color="#4C78A8",
                                         font=dict(color="white", size=17), height=38),
                             cells=dict(values=[t[c] for c in cols], fill_color=fill, font=dict(size=18), height=36)))
    fig.update_layout(width=1500, height=300, font=FONT, margin=dict(l=10, r=10, t=90, b=0),
                      title=dict(text=head, x=0.5, y=0.93))
    return fig


if __name__ == "__main__":
    fuelcols = [c for c in one.columns if c.startswith("fuel_")]
    allnew = [c for c in full.columns if c.startswith(("fuel_", "owner_"))]
    figs = [frame(df, "<b>The car data</b>: fuel and owner are text", []),
            frame(one, "<b>fuel</b> → 4 columns, one 1 per row", fuelcols),
            frame(full, "<b>owner</b> → 5 columns: 12 columns in all (selling_price not shown)", allnew),
            frame(k1, "<b>drop_first=True</b>: fuel_CNG and owner_First Owner removed, 10 columns (selling_price not shown)",
                  [c for c in k1.columns if c.startswith(("fuel_", "owner_"))])]
    save_gif(figs, "dummies_steps", here, keys=[0, 2, 3], fps=1, holds=[3, 3, 3, 6], cols=1, width=1000)

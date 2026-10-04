"""One Titanic passenger travelling through the life-cycle stages: the first row of the file with no age.
Gathered (Age empty) -> preprocessed (Age filled with the median, Age and Fare standardized) -> EDA (row unchanged)
-> features (Sex as a number, SibSp + Parch + 1 = family size) -> model (logistic regression on all 891 rows)
-> deployed (the prediction as JSON). Every number is computed here from data/titanic_train.csv.
Plotly frames -> ffmpeg GIF + _frames.png grid. Run: python row_journey.py -> row_journey.gif, row_journey_frames.png"""
import shutil
import subprocess
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
from PIL import Image
from sklearn.linear_model import LogisticRegression

HERE = Path(__file__).parent
BLUE, ORANGE, GREEN, RED, GREY, PURPLE, TEAL = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#6B6B6B", "#B279A2", "#72B7B2"
FONT = dict(family="Latin Modern Roman", size=24)

df = pd.read_csv(HERE.parent / "data" / "titanic_train.csv")
i = df.index[df.Age.isnull()][0]                               # first passenger with no age
raw = df.loc[i]
assert raw.PassengerId == 6 and raw.Survived == 0
median_age = df.Age.median()
assert median_age == 28
X = pd.DataFrame({"Pclass": df.Pclass, "Sex": (df.Sex == "male").astype(int), "Age": df.Age.fillna(median_age),
                  "Fare": df.Fare, "Family": df.SibSp + df.Parch + 1})
mean, std = X[["Age", "Fare"]].mean(), X[["Age", "Fare"]].std(ddof=0)
X[["Age", "Fare"]] = (X[["Age", "Fare"]] - mean) / std
model = LogisticRegression(max_iter=1000).fit(X, df.Survived)
p = model.predict_proba(X.loc[[i]])[0, 1]
z_age, z_fare = X.loc[i, "Age"], X.loc[i, "Fare"]
print(f"passenger {raw.PassengerId}: fare {raw.Fare:.2f}, z_age {z_age:.2f}, z_fare {z_fare:.2f}, "
      f"family {X.loc[i, 'Family']}, P(survive) {p:.2f}, training accuracy {model.score(X, df.Survived):.3f}")
assert (round(z_age, 2), round(z_fare, 2), round(p, 2)) == (-0.10, -0.48, 0.11)

STAGES = ["2 Gather", "3 Preprocess", "4 EDA", "5 Features", "6 Train", "7 Deploy"]
COLOURS = [BLUE, BLUE, BLUE, GREEN, ORANGE, TEAL]
# (active stage, caption, cells as (header, value, changed?))
STEPS = [
    (0, "Gathered: one passenger, as the file gives it. Age is empty.",
     [("Pclass", "3", 0), ("Sex", "male", 0), ("Age", "empty", 2), ("SibSp", "0", 0), ("Parch", "0", 0), ("Fare", "8.46", 0)]),
    (1, "Preprocess: fill the empty Age with the median age, 28.",
     [("Pclass", "3", 0), ("Sex", "male", 0), ("Age", "28", 1), ("SibSp", "0", 0), ("Parch", "0", 0), ("Fare", "8.46", 0)]),
    (1, "Preprocess: put Age and Fare on the same scale (standardize).",
     [("Pclass", "3", 0), ("Sex", "male", 0), ("Age", f"{z_age:.2f}", 1), ("SibSp", "0", 0), ("Parch", "0", 0),
      ("Fare", f"{z_fare:.2f}", 1)]),
    (2, "EDA: we study the data. The row itself does not change.",
     [("Pclass", "3", 0), ("Sex", "male", 0), ("Age", f"{z_age:.2f}", 0), ("SibSp", "0", 0), ("Parch", "0", 0),
      ("Fare", f"{z_fare:.2f}", 0)]),
    (3, "Features: Sex becomes a number; SibSp + Parch + 1 = family size.",
     [("Pclass", "3", 0), ("Sex", "1", 1), ("Age", f"{z_age:.2f}", 0), ("Family size", "1", 1), ("Fare", f"{z_fare:.2f}", 0)]),
    (4, f"Train: a model fitted on all 891 passengers reads the row: P(survived) = {p:.2f}.",
     [("Pclass", "3", 0), ("Sex", "1", 0), ("Age", f"{z_age:.2f}", 0), ("Family size", "1", 0), ("Fare", f"{z_fare:.2f}", 0),
      ("P(survived)", f"{p:.2f}", 1)]),
    (5, "Deploy: the API sends the prediction back as JSON.",
     [("JSON reply", f'{{"survived": 0, "probability": {p:.2f}}}', 1)]),
]


def frame(k):
    active, caption, cells = STEPS[k]
    fig = go.Figure()
    for s, (name, colour) in enumerate(zip(STAGES, COLOURS)):       # the stage strip
        on = s == active
        fig.add_shape(type="rect", x0=s + 0.04, x1=s + 0.96, y0=2.55, y1=3.25, line=dict(color=colour, width=3),
                      fillcolor=colour, opacity=1 if on else 0.18, layer="below")
        fig.add_annotation(x=s + 0.5, y=2.9, text=f"<b>{name}</b>" if on else name, showarrow=False,
                           font=dict(size=22, color="white" if on else "black"))
        if s < 5:
            fig.add_annotation(x=s + 1.04, y=2.9, ax=s + 0.96, ay=2.9, xref="x", yref="y", axref="x", ayref="y",
                               showarrow=True, arrowhead=2, arrowwidth=2, arrowcolor=GREY, text="")
    w = 6 / len(cells)
    for c, (head, value, changed) in enumerate(cells):              # the row
        colour = {0: "white", 1: "#CFE8CB", 2: "#F6C6C5"}[changed]
        fig.add_shape(type="rect", x0=c * w + 0.03, x1=(c + 1) * w - 0.03, y0=0.55, y1=1.45,
                      line=dict(color="black", width=2), fillcolor=colour, layer="below")
        fig.add_annotation(x=(c + 0.5) * w, y=1.75, text=head, showarrow=False, font=dict(size=22, color=GREY))
        fig.add_annotation(x=(c + 0.5) * w, y=1.0, text=f"<b>{value}</b>", showarrow=False, font=dict(size=28))
    fig.add_annotation(x=3, y=-0.05, text=caption, showarrow=False, font=dict(size=25))
    fig.update_xaxes(range=[-0.05, 6.05], visible=False)
    fig.update_yaxes(range=[-0.5, 3.5], visible=False)
    fig.update_layout(template="simple_white", width=1200, height=520, font=FONT, showlegend=False,
                      margin=dict(l=20, r=20, t=20, b=20))
    return fig


if __name__ == "__main__":
    tmp = HERE / ".row_frames"
    tmp.mkdir(exist_ok=True)
    n = 0
    for k in range(len(STEPS)):
        frame(k).write_image(tmp / f"k{k}.png")
        for _ in range(3 if k < len(STEPS) - 1 else 6):            # hold each step; hold the last longer
            shutil.copy(tmp / f"k{k}.png", tmp / f"{n:03d}.png")
            n += 1
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "1", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=900:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "row_journey.gif")], check=True)
    keys = [Image.open(tmp / f"k{k}.png").convert("RGB") for k in (0, 1, 2, 4, 5, 6)]
    w, h = keys[0].size
    sheet = Image.new("RGB", (2 * w + 16, 3 * h + 32), "white")
    for j, im in enumerate(keys):
        sheet.paste(im, ((j % 2) * (w + 16), (j // 2) * (h + 16)))
    sheet.save(HERE / "row_journey_frames.png")
    shutil.rmtree(tmp)

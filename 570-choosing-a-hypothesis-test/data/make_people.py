"""Builds data/people.csv: a simulated sample of 60 people with gender, age group, height (m) and weight (kg).
The gender by age-group counts are fixed; heights and weights are drawn with a fixed seed."""
from pathlib import Path
import numpy as np
import pandas as pd

rng = np.random.default_rng(7)
counts = {("child", "male"): 8, ("child", "female"): 12, ("adult", "male"): 14,
          ("adult", "female"): 12, ("elderly", "male"): 4, ("elderly", "female"): 10}
# mean height (m) and weight (kg) per age group and gender
means = {("child", "male"): (1.32, 32), ("child", "female"): (1.30, 31), ("adult", "male"): (1.75, 76),
         ("adult", "female"): (1.62, 62), ("elderly", "male"): (1.70, 74), ("elderly", "female"): (1.58, 63)}
rows = []
for (age, gender), n in counts.items():
    h_mean, w_mean = means[(age, gender)]
    height = rng.normal(h_mean, 0.07, n)
    # weight follows height: 1 cm more height adds about 0.5 kg, plus noise
    weight = w_mean + 50 * (height - h_mean) + rng.normal(0, 4, n)
    rows += [dict(gender=gender, age_group=age, height=round(h, 2), weight=round(w, 1))
             for h, w in zip(height, weight)]
people = pd.DataFrame(rows).sample(frac=1, random_state=7).reset_index(drop=True)
people.to_csv(Path(__file__).parent / "people.csv", index=False)

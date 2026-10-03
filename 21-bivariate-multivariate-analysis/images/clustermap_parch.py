"""Titanic: crosstab of Parch (parents/children aboard) vs survival, as a clustermap."""
import pandas as pd
from common import load, save_px, clustermap

t = load("titanic_train")
ct = pd.crosstab(t.Parch, t.Survived)
ct.columns.name = "Survived"
fig = clustermap(ct, "Parch vs survival: similar rows grouped", "Passengers", width=760, height=600)
save_px(fig, "clustermap_parch")

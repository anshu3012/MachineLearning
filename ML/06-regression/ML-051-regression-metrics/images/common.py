"""Shared data for the figures: the placement test set and the line's predictions (no output when run)."""
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

df = pd.read_csv(Path(__file__).parent.parent / "data" / "placement.csv")
X_train, X_test, y_train, y_test = train_test_split(df[["cgpa"]], df["package"], test_size=0.2, random_state=2)
lr = LinearRegression().fit(X_train, y_train)
x, y = X_test["cgpa"].to_numpy(), y_test.to_numpy()
pred = lr.predict(X_test)
BLUE, ORANGE, GREEN, RED, GREY = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#6B6B6B"
FONT = dict(family="Latin Modern Roman", size=16)

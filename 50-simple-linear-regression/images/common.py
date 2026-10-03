"""Shared data for the figures: the 160 training students and the fitted line (no output when run)."""
from pathlib import Path
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

df = pd.read_csv(Path(__file__).parent.parent / "data" / "placement.csv")
X_train, X_test, y_train, y_test = train_test_split(df[["cgpa"]], df["package"], test_size=0.2, random_state=2)
lr = LinearRegression().fit(X_train, y_train)
M, B = float(lr.coef_[0]), float(lr.intercept_)

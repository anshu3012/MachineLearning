"""Shared data for the figures: the 200-row data, a 70/30 split and the residuals (no output when run)."""
from pathlib import Path
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

df = pd.read_csv(Path(__file__).parent.parent / "data" / "data.csv")
X, y = df.iloc[:, :3].to_numpy(), df["target"].to_numpy()
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=1)
model = LinearRegression().fit(X_train, y_train)
y_pred = model.predict(X_test)
residual = y_test - y_pred
BLUE, ORANGE, GREEN, RED, GREY = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#6B6B6B"
FONT = dict(family="Latin Modern Roman", size=15)

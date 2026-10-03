"""The Note's model, shared by the figures: placement.csv -> split -> scale -> logistic regression."""
from pathlib import Path
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

DATA = Path(__file__).parent.parent / "data" / "placement.csv"


def load():
    df = pd.read_csv(DATA).iloc[:, 1:]                  # drop the unneeded index column
    X, y = df.iloc[:, 0:2], df.iloc[:, -1]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=1)
    scaler = StandardScaler().fit(X_train)
    clf = LogisticRegression().fit(scaler.transform(X_train), y_train)
    return df, X_train, X_test, y_train, y_test, scaler, clf

"""The second admission network's test predictions after chosen epochs, with the Notebook's exact steps (seed 1,
deterministic ops, CPU; the first network is trained first, as in the Notebook, so the random numbers line up).
Writes data/pred_epochs.npz. Run: CUDA_VISIBLE_DEVICES= python experiments/pred_epochs.py"""
import os
from pathlib import Path

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
import tensorflow as tf  # noqa: E402
import keras  # noqa: E402
from keras import layers  # noqa: E402
from sklearn.metrics import r2_score  # noqa: E402
from sklearn.model_selection import train_test_split  # noqa: E402
from sklearn.preprocessing import MinMaxScaler  # noqa: E402

HERE = Path(__file__).resolve().parent.parent
keras.utils.set_random_seed(1)
tf.config.experimental.enable_op_determinism()
df = pd.read_csv(HERE / "data" / "Admission_Predict_Ver1.1.csv")
df.columns = df.columns.str.strip()
df = df.drop(columns="Serial No.")
X, y = df.iloc[:, 0:-1], df.iloc[:, -1]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1)
scaler = MinMaxScaler()
X_train_scaled, X_test_scaled = scaler.fit_transform(X_train), scaler.transform(X_test)

model = keras.Sequential([keras.Input(shape=(7,)), layers.Dense(7, activation="relu"), layers.Dense(1, activation="linear")])
model.compile(loss="mean_squared_error", optimizer="adam")
model.fit(X_train_scaled, y_train, epochs=10, validation_split=0.2, verbose=0)
print("R2 first network:", r2_score(y_test, model.predict(X_test_scaled, verbose=0)))

model2 = keras.Sequential([keras.Input(shape=(7,)), layers.Dense(7, activation="relu"),
                           layers.Dense(7, activation="relu"), layers.Dense(1, activation="linear")])
model2.compile(loss="mean_squared_error", optimizer="adam")
KEEP = [1, 2, 3, 5, 10, 20, 50, 100]
preds = {0: model2.predict(X_test_scaled, verbose=0).ravel()}


class Keep(keras.callbacks.Callback):
    def on_epoch_end(self, epoch, logs=None):
        if epoch + 1 in KEEP:
            preds[epoch + 1] = self.model.predict(X_test_scaled, verbose=0).ravel()


model2.fit(X_train_scaled, y_train, epochs=100, validation_split=0.2, verbose=0, callbacks=[Keep()])
for e in [0] + KEEP:
    print(e, round(r2_score(y_test, preds[e]), 4))
np.savez_compressed(HERE / "data" / "pred_epochs.npz", epochs=np.array([0] + KEEP), y=y_test.values,
                    preds=np.array([preds[e] for e in [0] + KEEP], np.float32))

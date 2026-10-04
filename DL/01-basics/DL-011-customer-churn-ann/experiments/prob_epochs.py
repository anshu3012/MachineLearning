"""The first churn network's test probabilities after every epoch, , with the Notebook's exact steps (seed 1, deterministic ops, CPU). Writes data/prob_epochs.npz.
Run: CUDA_VISIBLE_DEVICES= python experiments/prob_epochs.py"""
import os
from pathlib import Path

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
import tensorflow as tf  # noqa: E402
import keras  # noqa: E402
from keras import layers  # noqa: E402
from sklearn.model_selection import train_test_split  # noqa: E402
from sklearn.preprocessing import StandardScaler  # noqa: E402

HERE = Path(__file__).resolve().parent.parent
keras.utils.set_random_seed(1)
tf.config.experimental.enable_op_determinism()
df = pd.read_csv(HERE / "data" / "Churn_Modelling.csv").drop(columns=["RowNumber", "CustomerId", "Surname"])
df = pd.get_dummies(df, columns=["Geography", "Gender"], drop_first=True, dtype=int)
X, y = df.drop(columns="Exited"), df["Exited"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1)
scaler = StandardScaler()
X_train_scaled, X_test_scaled = scaler.fit_transform(X_train), scaler.transform(X_test)

model = keras.Sequential([keras.Input(shape=(11,)), layers.Dense(3, activation="sigmoid"),
                          layers.Dense(1, activation="sigmoid")])
model.compile(loss="binary_crossentropy", optimizer="adam")
probs = [model.predict(X_test_scaled, verbose=0).ravel()]


class Keep(keras.callbacks.Callback):
    def on_epoch_end(self, epoch, logs=None):
        probs.append(self.model.predict(X_test_scaled, verbose=0).ravel())


h1 = model.fit(X_train_scaled, y_train, epochs=10, verbose=0, callbacks=[Keep()])
print("loss", np.round(h1.history["loss"], 4))
print("model 1 acc", ((probs[-1] > 0.5) == y_test.values).mean(), "range", probs[-1].min(), probs[-1].max())
np.savez_compressed(HERE / "data" / "prob_epochs.npz", probs=np.array(probs, np.float32), y=y_test.values, loss=np.array(h1.history["loss"]))

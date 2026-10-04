"""Batch normalisation and the learning rate: the Note's circles data (500, noise 0.1, factor 0.5, seed 1,
standardised) and its two networks (2-3-2-1 ReLU, with or without BatchNormalization after each hidden layer),
trained with plain SGD at learning rates from 0.01 to 3 for 100 epochs, batch 32, 20% validation, 5 seeds each.
Records the final validation accuracy. Writes data/lr_range.json. Run: python experiments/lr_range.py"""
import json
import os
from pathlib import Path

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
import numpy as np  # noqa: E402
import keras  # noqa: E402
from sklearn.datasets import make_circles  # noqa: E402

HERE = Path(__file__).resolve().parent.parent
X, y = make_circles(n_samples=500, noise=0.1, factor=0.5, random_state=1)
X = ((X - X.mean(0)) / X.std(0)).astype("float32")


def model(bn):
    L = [keras.Input(shape=(2,)), keras.layers.Dense(3, activation="relu")]
    if bn:
        L.append(keras.layers.BatchNormalization())
    L.append(keras.layers.Dense(2, activation="relu"))
    if bn:
        L.append(keras.layers.BatchNormalization())
    L.append(keras.layers.Dense(1, activation="sigmoid"))
    return keras.Sequential(L)


LRS = [0.01, 0.03, 0.1, 0.3, 1.0, 3.0]
out = {"lrs": LRS}
for bn in (False, True):
    rows = []
    for lr in LRS:
        accs = []
        for seed in range(5):
            keras.utils.set_random_seed(seed)
            m = model(bn)
            m.compile(optimizer=keras.optimizers.SGD(lr), loss="binary_crossentropy", metrics=["accuracy"])
            h = m.fit(X, y, epochs=100, batch_size=32, validation_split=0.2, verbose=0)
            accs.append(float(h.history["val_accuracy"][-1]))
        rows.append(accs)
        print("BN" if bn else "no BN", lr, np.round(accs, 2), round(float(np.mean(accs)), 3), flush=True)
    out["bn" if bn else "plain"] = rows
json.dump(out, open(HERE / "data" / "lr_range.json", "w"), indent=1)

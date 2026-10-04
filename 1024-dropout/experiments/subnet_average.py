"""The ensemble view of dropout, measured. A 2-128-128-1 network with Dropout(0.5) after each hidden layer learns
make_moons (200 points, noise 0.25, seed 0) for 500 epochs (Adam, CPU, seed 0). Then, on a grid over the plane, we
compare the full network (all nodes, Keras' scaling: what predict() does) with the average of K random sub-networks
(one random dropout mask per hidden layer, the same for every grid point, applied to the trained weights), for K = 1 to 50.
Writes data/subnet_average.npz. Run: CUDA_VISIBLE_DEVICES= python experiments/subnet_average.py"""
import os
from pathlib import Path

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
import numpy as np  # noqa: E402
import keras  # noqa: E402
from sklearn.datasets import make_moons  # noqa: E402

HERE = Path(__file__).resolve().parent.parent
keras.utils.set_random_seed(0)
X, y = make_moons(200, noise=0.25, random_state=0)
net = keras.Sequential([keras.Input((2,)), keras.layers.Dense(128, activation="relu"), keras.layers.Dropout(0.5),
                        keras.layers.Dense(128, activation="relu"), keras.layers.Dropout(0.5),
                        keras.layers.Dense(1, activation="sigmoid")])
net.compile("adam", "binary_crossentropy", metrics=["accuracy"])
net.fit(X, y, epochs=500, batch_size=32, verbose=0)
g1, g2 = np.meshgrid(np.linspace(-2, 3, 101), np.linspace(-1.6, 2.1, 81))
G = np.c_[g1.ravel(), g2.ravel()].astype("float32")
full = net.predict(G, verbose=0).ravel()
W1, b1, W2, b2, W3, b3 = net.get_weights()
rng = np.random.default_rng(1)


def sub_network():
    """One sub-network: one random mask per hidden layer, kept nodes scaled by 1/0.5 as Keras does in training."""
    m1, m2 = rng.random(128) >= 0.5, rng.random(128) >= 0.5
    h1 = np.maximum(G @ W1 + b1, 0) * m1 / 0.5
    h2 = np.maximum(h1 @ W2 + b2, 0) * m2 / 0.5
    return 1 / (1 + np.exp(-(h2 @ W3 + b3))).ravel()


assert np.allclose(1 / (1 + np.exp(-(np.maximum(np.maximum(G @ W1 + b1, 0) @ W2 + b2, 0) @ W3 + b3))).ravel(), full,
                   atol=1e-4)                                   # the full network by hand equals predict()
subs = np.array([sub_network() for _ in range(50)], np.float32)
np.savez_compressed(HERE / "data" / "subnet_average.npz", X=X, y=y, g1=g1, g2=g2, full=full.astype(np.float32),
                    subs=subs.astype(np.float16))
for k in (1, 2, 5, 10, 20, 50):
    avg = subs[:k].mean(0)
    print(k, "same class", round(((avg > 0.5) == (full > 0.5)).mean(), 4), "mean gap", round(np.abs(avg - full).mean(), 4))

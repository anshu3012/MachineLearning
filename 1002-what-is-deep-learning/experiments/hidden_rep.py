"""Representation learning, measured. An MLP (784-64-32-10, ReLU) learns MNIST digits; after each chosen epoch we
save the 32 numbers of its last hidden layer for 1,500 test images, and the raw pixels' 2D PCA for comparison.
Writes data/hidden_rep.npz: 2D PCA views and the share of images whose nearest neighbour is the same digit. Run once (CPU, seeded): CUDA_VISIBLE_DEVICES= python experiments/hidden_rep.py"""
import os
from pathlib import Path

import numpy as np

os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "3")
import keras  # noqa: E402

HERE = Path(__file__).resolve().parent.parent
d = np.load(Path.home() / ".keras/datasets/mnist.npz")
Xtr, ytr = d["x_train"].reshape(-1, 784) / 255.0, d["y_train"]
Xte, yte = d["x_test"].reshape(-1, 784) / 255.0, d["y_test"]
idx = np.random.default_rng(0).permutation(10000)[:1500]
keras.utils.set_random_seed(0)
inp = keras.Input((784,))
h1 = keras.layers.Dense(64, activation="relu")(inp)
h2 = keras.layers.Dense(32, activation="relu", name="hidden")(h1)
out = keras.layers.Dense(10, activation="softmax")(h2)
net = keras.Model(inp, out)
probe = keras.Model(inp, h2)
net.compile("adam", "sparse_categorical_crossentropy", metrics=["accuracy"])
EPOCHS = [0, 1, 2, 5, 10]
reps, accs, done = {}, {}, 0
for e in EPOCHS:
    if e > done:
        net.fit(Xtr, ytr, epochs=e - done, batch_size=128, verbose=0)
        done = e
    reps[f"h{e}"] = probe.predict(Xte[idx], verbose=0)
    accs[f"a{e}"] = net.evaluate(Xte, yte, verbose=0)[1]
    print(e, accs[f"a{e}"])
from sklearn.decomposition import PCA  # noqa: E402
from sklearn.neighbors import NearestNeighbors  # noqa: E402


SUB = np.isin(yte[idx], [3, 5, 8])                     # three digits that are easy to confuse


def summary(Z):
    """2D PCA of the 3s, 5s and 8s, and the share of them whose nearest neighbour (full space) is the same digit."""
    Z, lab = Z[SUB], yte[idx][SUB]
    _, nb = NearestNeighbors(n_neighbors=2).fit(Z).kneighbors(Z)
    return PCA(2, random_state=0).fit_transform(Z).astype(np.float32), float((lab[nb[:, 1]] == lab).mean())


out = {"labels": yte[idx][SUB], "epochs": np.array(EPOCHS)}
out["p_pixels"], out["s_pixels"] = summary(Xte[idx])
for e in EPOCHS:
    out[f"p{e}"], out[f"s{e}"] = summary(reps[f"h{e}"])
    print(e, "same-digit neighbour", out[f"s{e}"])
print("pixels", out["s_pixels"])
np.savez_compressed(HERE / "data" / "hidden_rep.npz", **out, **accs)

"""Batch size on MNIST: the 32-32-32 ReLU network of the shapes experiment, trained for 10 epochs with Adam (default
learning rate) at batch sizes 8 to 8,192, 2 seeds each. Records the time per epoch (GPU, this machine) and the test
accuracy. Writes data/batch_size.json. Run: python experiments/batch_size.py"""
import json
import os
import time
from pathlib import Path

import numpy as np

os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "3")
import keras  # noqa: E402

HERE = Path(__file__).resolve().parent.parent
d = np.load(Path.home() / ".keras/datasets/mnist.npz")
Xtr, ytr = d["x_train"].reshape(-1, 784) / 255.0, d["y_train"]
Xte, yte = d["x_test"].reshape(-1, 784) / 255.0, d["y_test"]
out = {}
for bs in [8, 32, 128, 512, 2048, 8192]:
    accs, times = [], []
    for seed in range(2):
        keras.utils.set_random_seed(seed)
        net = keras.Sequential([keras.Input((784,))] + [keras.layers.Dense(32, activation="relu") for _ in range(3)]
                               + [keras.layers.Dense(10, activation="softmax")])
        net.compile("adam", "sparse_categorical_crossentropy", metrics=["accuracy"])
        net.fit(Xtr[:bs], ytr[:bs], epochs=1, batch_size=bs, verbose=0)             # warm-up (graph building)
        keras.utils.set_random_seed(seed)
        net = keras.models.clone_model(net)
        net.compile("adam", "sparse_categorical_crossentropy", metrics=["accuracy"])
        t = time.perf_counter()
        net.fit(Xtr, ytr, epochs=10, batch_size=bs, verbose=0)
        times.append((time.perf_counter() - t) / 10)
        accs.append(net.evaluate(Xte, yte, verbose=0)[1])
    out[bs] = {"acc": float(np.mean(accs)), "sec_per_epoch": float(np.mean(times)), "updates_per_epoch": -(-60000 // bs)}
    print(bs, out[bs], flush=True)
json.dump(out, open(HERE / "data" / "batch_size.json", "w"), indent=1)

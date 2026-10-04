"""Neurons per layer on MNIST: a pyramid (64-32-16) against three equal layers with the same number of parameters
(58-58-58), and a first hidden layer of 1, 2 or 32 neurons followed by two layers of 32 (the bottleneck of Figure 2c). ReLU hidden layers, softmax output, Adam, batch 128,
10 epochs, 3 seeds each; test accuracy on the 10,000 test images. Writes data/shapes.json.
Run: python experiments/shapes.py (GPU is fine; these are new experiments)."""
import json
import os
from pathlib import Path

import numpy as np

os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "3")
import keras  # noqa: E402

HERE = Path(__file__).resolve().parent.parent
d = np.load(Path.home() / ".keras/datasets/mnist.npz")
Xtr, ytr = d["x_train"].reshape(-1, 784) / 255.0, d["y_train"]
Xte, yte = d["x_test"].reshape(-1, 784) / 255.0, d["y_test"]
SHAPES = {"64-32-16": [64, 32, 16], "58-58-58": [58, 58, 58], "1-32-32": [1, 32, 32], "2-32-32": [2, 32, 32],
          "32-32-32": [32, 32, 32]}
out = {}
for name, hidden in SHAPES.items():
    accs, params = [], None
    for seed in range(3):
        keras.utils.set_random_seed(seed)
        net = keras.Sequential([keras.Input((784,))] + [keras.layers.Dense(h, activation="relu") for h in hidden]
                               + [keras.layers.Dense(10, activation="softmax")])
        net.compile("adam", "sparse_categorical_crossentropy", metrics=["accuracy"])
        net.fit(Xtr, ytr, epochs=10, batch_size=128, verbose=0)
        accs.append(net.evaluate(Xte, yte, verbose=0)[1])
        params = net.count_params()
    out[name] = {"accs": accs, "mean": float(np.mean(accs)), "params": int(params)}
    print(name, params, np.round(accs, 4), round(float(np.mean(accs)), 4), flush=True)
json.dump(out, open(HERE / "data" / "shapes.json", "w"), indent=1)

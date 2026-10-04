"""The Notebook's small CNN (Conv 8, pool, Conv 16, pool, Dense 10; 3 epochs) on normal MNIST and on the same
scrambled MNIST the Notebook gives the ANN (one fixed permutation of the 784 pixel positions, rng seed 0).
3 seeds each, laptop CPU. Appends nothing to the Notebook's files: writes data/scramble_cnn.csv.
Run: CUDA_VISIBLE_DEVICES= python experiments/scrambled_cnn.py"""
import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
os.environ["CUDA_VISIBLE_DEVICES"] = ""
from pathlib import Path
import numpy as np
import pandas as pd
import keras

HERE = Path(__file__).resolve().parent.parent
(x_train, y_train), (x_test, y_test) = keras.datasets.mnist.load_data()
perm = np.random.default_rng(0).permutation(784)
scramble = lambda x: x.reshape(len(x), -1)[:, perm].reshape(x.shape)
rows = []
for name, (xtr, xte) in (("normal", (x_train, x_test)), ("scrambled", (scramble(x_train), scramble(x_test)))):
    for seed in (1, 2, 3):
        keras.utils.set_random_seed(seed)
        m = keras.Sequential([keras.Input(shape=(28, 28, 1)),
                              keras.layers.Conv2D(8, 3, activation="relu"), keras.layers.MaxPooling2D(),
                              keras.layers.Conv2D(16, 3, activation="relu"), keras.layers.MaxPooling2D(),
                              keras.layers.Flatten(), keras.layers.Dense(10, activation="softmax")])
        m.compile(loss="sparse_categorical_crossentropy", optimizer="adam", metrics=["accuracy"])
        m.fit(xtr[..., None] / 255.0, y_train, epochs=3, batch_size=128, verbose=0)
        rows.append(dict(images=name, seed=seed, test_acc=m.evaluate(xte[..., None] / 255.0, y_test, verbose=0)[1]))
        print(rows[-1], flush=True)
res = pd.DataFrame(rows)
res.to_csv(HERE / "data" / "scramble_cnn.csv", index=False)
print(res.groupby("images").test_acc.agg(["mean", "min", "max"]).round(4))

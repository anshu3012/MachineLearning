"""Symmetry, followed through training: the Notebook's section 5 run (3 ReLU hidden nodes, every weight and bias
starting at 0.5, Adam 0.01, batch 32, 100 epochs, moons 300, seed 0, CPU) next to the same network with Keras'
default random start. Records the hidden layer's weights after every epoch. Writes data/twins.npz.
Run: CUDA_VISIBLE_DEVICES= python experiments/twins.py"""
import os
from pathlib import Path

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
import numpy as np  # noqa: E402
import keras  # noqa: E402
import tensorflow as tf  # noqa: E402
from sklearn.datasets import make_moons  # noqa: E402

HERE = Path(__file__).resolve().parent.parent
tf.config.experimental.enable_op_determinism()
X, y = make_moons(n_samples=300, noise=0.1, random_state=42)
X = ((X - X.mean(0)) / X.std(0)).astype("float32")


def run(constant):
    keras.utils.set_random_seed(0)
    m = keras.Sequential([keras.Input(shape=(2,)), keras.layers.Dense(3, activation="relu"),
                          keras.layers.Dense(1, activation="sigmoid")])
    if constant:
        m.set_weights([np.full(w.shape, 0.5, "float32") for w in m.get_weights()])
    m.compile(optimizer=keras.optimizers.Adam(0.01), loss="binary_crossentropy", metrics=["accuracy"])
    traj = [m.layers[0].kernel.numpy().copy()]

    class Keep(keras.callbacks.Callback):
        def on_epoch_end(self, epoch, logs=None):
            traj.append(self.model.layers[0].kernel.numpy().copy())

    h = m.fit(X, y, epochs=100, batch_size=32, verbose=0, callbacks=[Keep()])
    return np.array(traj), np.array(h.history["accuracy"])


Wc, ac = run(True)
Wr, ar = run(False)
print("constant: from x1", Wc[-1][0].round(3), "from x2", Wc[-1][1].round(3), "acc", ac[-1].round(3))
print("random:   from x1", Wr[-1][0].round(3), "from x2", Wr[-1][1].round(3), "acc", ar[-1].round(3))
np.savez_compressed(HERE / "data" / "twins.npz", Wc=Wc, Wr=Wr, ac=ac, ar=ar)

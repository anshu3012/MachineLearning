"""The dead-node shares of Figure 3, followed through training: the Notebook's exact setup (make_moons 500, two hidden
layers of 32, SGD, batch 32, 200 epochs, seed 0, deterministic ops, CPU), recording after every epoch the share of
nodes in each hidden layer whose z is negative on every training observation. For the learning-rate-10 run, also
after every one of the 16 batches of epoch 1. Writes data/dead_over_time.npz.
Run: CUDA_VISIBLE_DEVICES= python experiments/dead_over_time.py"""
import os
from pathlib import Path

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
import numpy as np  # noqa: E402
import keras  # noqa: E402
import tensorflow as tf  # noqa: E402
from sklearn.datasets import make_moons  # noqa: E402

HERE = Path(__file__).resolve().parent.parent
tf.config.experimental.enable_op_determinism()
X, y = make_moons(n_samples=500, noise=0.2, random_state=0)
X = ((X - X.mean(0)) / X.std(0)).astype("float32")


def build(act, lr, bias, seed=0):
    keras.utils.set_random_seed(seed)
    hidden = lambda: keras.layers.Dense(32, activation=act, bias_initializer=keras.initializers.Constant(bias))
    m = keras.Sequential([keras.Input(shape=(2,)), hidden(), hidden(), keras.layers.Dense(1, activation="sigmoid")])
    m.compile(optimizer=keras.optimizers.SGD(learning_rate=lr), loss="binary_crossentropy", metrics=["accuracy"])
    return m


def negative_everywhere(m):
    out, h = [], X
    for layer in m.layers[:2]:
        z = h @ layer.kernel.numpy() + layer.bias.numpy()
        out.append(float(np.mean((z <= 0).all(axis=0))))
        h = layer(h).numpy()
    return out


RUNS = {"relu_lr10": ("relu", 10.0, 0.0), "relu_bias": ("relu", 0.1, -1.0), "leaky_bias": ("leaky_relu", 0.1, -1.0),
        "elu_bias": ("elu", 0.1, -1.0), "relu_lr01": ("relu", 0.1, 0.0)}
out = {}
for key, (act, lr, bias) in RUNS.items():
    m = build(act, lr, bias)
    per_epoch, per_batch = [negative_everywhere(m)], [negative_everywhere(m)]

    class Track(keras.callbacks.Callback):
        def on_train_batch_end(self, batch, logs=None):
            if len(per_epoch) == 1 and key == "relu_lr10":
                per_batch.append(negative_everywhere(self.model))

        def on_epoch_end(self, epoch, logs=None):
            per_epoch.append(negative_everywhere(self.model))

    h = m.fit(X, y, epochs=200, batch_size=32, verbose=0, callbacks=[Track()])
    out[key] = np.array(per_epoch)
    out[key + "_acc"] = np.array(h.history["accuracy"])
    if key == "relu_lr10":
        out["relu_lr10_batches"] = np.array(per_batch)
    print(key, np.round(out[key][[0, 1, 10, 200]], 3).tolist(), round(h.history["accuracy"][-1], 3))
np.savez_compressed(HERE / "data" / "dead_over_time.npz", **out)

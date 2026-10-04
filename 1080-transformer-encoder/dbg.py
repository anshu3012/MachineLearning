import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
import gc
import numpy as np
import pandas as pd
import keras
import tensorflow as tf

np.set_printoptions(precision=3, suppress=True)
tf.config.experimental.enable_tensor_float_32_execution(False)   # exact float32 on the GPU, for the by-hand checks


def positional_encoding(n_pos, d_model):
    """PE[pos, 2i] = sin(pos / 10000^(2i/d)), PE[pos, 2i+1] = cos(same angle) (Vaswani et al. 2017, 3.5)."""
    pos = np.arange(n_pos)[:, None]
    i = np.arange(d_model // 2)[None, :]
    angle = pos / 10000 ** (2 * i / d_model)
    pe = np.zeros((n_pos, d_model))
    pe[:, 0::2] = np.sin(angle)
    pe[:, 1::2] = np.cos(angle)
    return pe.astype("float32")


class EncoderBlock(keras.layers.Layer):
    """Multi-head attention -> add & norm -> feed-forward (ReLU) -> add & norm (Vaswani et al. 2017, 3.1).
    residual=False drops the two "x +" paths and keeps everything else."""
    def __init__(self, d_model, heads, d_ff, residual=True, **kw):
        super().__init__(**kw)
        self.residual = residual
        self.mha = keras.layers.MultiHeadAttention(num_heads=heads, key_dim=d_model // heads)
        self.norm1 = keras.layers.LayerNormalization()
        self.ffn1 = keras.layers.Dense(d_ff, activation="relu")
        self.ffn2 = keras.layers.Dense(d_model)
        self.norm2 = keras.layers.LayerNormalization()

    def call(self, x):
        z = self.mha(x, x)
        z_norm = self.norm1(x + z if self.residual else z)
        y = self.ffn2(self.ffn1(z_norm))
        return self.norm2(z_norm + y if self.residual else y)

import gc
V = 10000
(xtr, ytr), (xte, yte) = keras.datasets.imdb.load_data(num_words=V)
L, D, H, DFF, N = 100, 32, 2, 64, 6
xtr_p = keras.utils.pad_sequences(xtr, maxlen=L)
xte_p = keras.utils.pad_sequences(xte, maxlen=L)
PE = positional_encoding(L, D)


def build(residual, seed):
    keras.utils.set_random_seed(seed)
    inp = keras.Input((L,), dtype="int32")
    emb = keras.layers.Embedding(V, D)
    x = emb(inp) + PE
    for _ in range(N):
        x = EncoderBlock(D, H, DFF, residual)(x)
    out = keras.layers.Dense(1, activation="sigmoid")(keras.layers.GlobalAveragePooling1D()(x))
    return keras.Model(inp, out), emb



for N in (12, 24):
  for seed in range(2):
    for residual in (True, False):
        keras.backend.clear_session(); gc.collect()
        m, _ = build(residual, seed)
        lr = keras.optimizers.schedules.CosineDecay(0.0, decay_steps=2 * 391, warmup_target=1e-3, warmup_steps=391)
        m.compile(optimizer=keras.optimizers.Adam(lr), loss="binary_crossentropy", metrics=["accuracy"])
        hist = m.fit(xtr_p, ytr, epochs=3, batch_size=64, validation_data=(xte_p[:5000], yte[:5000]), verbose=0).history
        print("RES N", N, residual, seed, np.round(hist["accuracy"], 3), np.round(hist["val_accuracy"], 3), flush=True)

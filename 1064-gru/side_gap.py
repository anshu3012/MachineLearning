# side test (not part of the Note): GRU on the gap-25 task, default init vs update-gate bias 1
import os; os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
import numpy as np, keras
VOCAB, KEEP, N = 10000, 50, 5000
(x_tr, y_tr), (x_te, y_te) = keras.datasets.imdb.load_data(num_words=VOCAB)
def with_gap(x, gap):
    first = keras.utils.pad_sequences(x[:N], maxlen=KEEP, padding="pre", truncating="post")
    return np.concatenate([first, np.zeros((N, gap), dtype="int32")], axis=1)
xa, xb, ya, yb = with_gap(x_tr, 25), with_gap(x_te, 25), y_tr[:N].astype("float32"), y_te[:N].astype("float32")
for zbias in (0.0, 1.0):
    for seed in (0, 1, 2):
        keras.utils.set_random_seed(seed)
        rnn = keras.layers.GRU(32)
        m = keras.Sequential([keras.Input(shape=(75,)), keras.layers.Embedding(VOCAB, 32), rnn, keras.layers.Dense(1, activation="sigmoid")])
        w = rnn.get_weights(); w[2][:, :32] = zbias; rnn.set_weights(w)   # Keras z (weighs the old state) comes first
        m.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"])
        h = m.fit(xa, ya, epochs=8, batch_size=64, validation_data=(xb, yb), verbose=0)
        print(f"z bias {zbias}: seed {seed} final {h.history['val_accuracy'][-1]:.3f}", flush=True)

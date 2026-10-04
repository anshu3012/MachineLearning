"""Which validation photos does the overfitted CNN get wrong, and how sure is it?
One extra run (seed 0, 10 epochs) of the Note's two models, the plain CNN and the CNN with batch normalisation and
dropout, on the Note's split (seed 1337, 18,728 training and 4,682 validation photos). For every validation photo we
keep P(dog) from both models. Saved: the 12 photos the plain CNN gets wrong with the highest confidence (as 80 x 80
thumbnails), and counts of how confident its mistakes are.
Runs on a GPU, like the Notebook. Run: python experiments/mistakes.py [path to PetImages]
Writes data/mistakes.npz and data/mistakes.json."""
import json
import os
import sys
from pathlib import Path

os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "3")
os.environ.setdefault("TF_GPU_ALLOCATOR", "cuda_malloc_async")
import numpy as np  # noqa: E402
import tensorflow as tf  # noqa: E402
import keras  # noqa: E402
from keras import layers  # noqa: E402

HERE = Path(__file__).resolve().parent.parent
ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else Path.home() / "datasets" / "PetImages")
train_ds, val_ds = keras.utils.image_dataset_from_directory(
    str(ROOT), labels="inferred", label_mode="int", batch_size=32, image_size=(256, 256),
    validation_split=0.2, subset="both", seed=1337)
process = lambda image, label: (tf.cast(image, tf.float32) / 255.0, label)
to_uint8 = lambda image, label: (tf.cast(image, tf.uint8), label)
train = train_ds.unbatch().map(to_uint8).cache().shuffle(20000, seed=0).batch(32).map(process).prefetch(tf.data.AUTOTUNE)
val = val_ds.map(to_uint8).cache().map(process).prefetch(tf.data.AUTOTUNE)


def make_model(bn_dropout=False):                       # the Notebook's model
    model = keras.Sequential([keras.Input(shape=(256, 256, 3))])
    for filters in (32, 64, 128):
        model.add(layers.Conv2D(filters, kernel_size=(3, 3), padding="valid", activation="relu"))
        if bn_dropout:
            model.add(layers.BatchNormalization())
        model.add(layers.MaxPooling2D(pool_size=(2, 2), strides=2, padding="valid"))
    model.add(layers.Flatten())
    model.add(layers.Dense(128, activation="relu"))
    if bn_dropout:
        model.add(layers.Dropout(0.1))
    model.add(layers.Dense(64, activation="relu"))
    if bn_dropout:
        model.add(layers.Dropout(0.1))
    model.add(layers.Dense(1, activation="sigmoid"))
    model.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"])
    return model


y = np.concatenate([lab.numpy() for _, lab in val])
P, info = {}, {}
for name, flag in (("plain", False), ("bn_dropout", True)):
    keras.utils.set_random_seed(0)
    model = make_model(flag)
    h = model.fit(train, epochs=10, validation_data=val, verbose=2)
    P[name] = model.predict(val, verbose=0)[:, 0]
    wrong = (P[name] > 0.5) != (y == 1)
    conf = np.where(P[name] > 0.5, P[name], 1 - P[name])            # confidence in the predicted class
    info[name] = dict(train_acc=float(h.history["accuracy"][-1]), val_acc=float(1 - wrong.mean()),
                      n_val=int(len(y)), n_wrong=int(wrong.sum()),
                      wrong_conf_over_90=int((wrong & (conf > 0.9)).sum()), wrong_conf_over_99=int((wrong & (conf > 0.99)).sum()),
                      wrong_median_conf=float(np.median(conf[wrong])))
    print(name, info[name], flush=True)

wrong = (P["plain"] > 0.5) != (y == 1)
conf = np.where(P["plain"] > 0.5, P["plain"], 1 - P["plain"])
pick = np.argsort(-(conf * wrong))[:12]                              # the 12 most confident mistakes of the plain CNN
images = np.concatenate([img.numpy() for img, _ in val_ds])          # same order: the validation set is not shuffled
thumbs = tf.image.resize(images[pick], (80, 80)).numpy().clip(0, 255).astype(np.uint8)
np.savez_compressed(HERE / "data" / "mistakes.npz", images=thumbs, labels=y[pick], p_plain=P["plain"][pick],
                    p_bn=P["bn_dropout"][pick])
info["both_wrong"] = int((wrong & ((P["bn_dropout"] > 0.5) != (y == 1))).sum())
json.dump(info, open(HERE / "data" / "mistakes.json", "w"), indent=1)
print(json.dumps(info, indent=1))

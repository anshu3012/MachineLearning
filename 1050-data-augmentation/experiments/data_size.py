"""Augmentation as a function of the amount of data: the Note's model (section 6.1), with and without its three
random layers, trained on 250, 500 and 1,000 photos per class taken from the training folder of the Notebook's
small subset (~/datasets/cats_vs_dogs_small, first files by name), 60 epochs, 4 seeds; scored on the same 1,000 test
photos. GPU. Writes data/data_size.json. Run: python experiments/data_size.py"""
import json
import os
import shutil
import tempfile
from pathlib import Path

os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "3")
import numpy as np  # noqa: E402
import keras  # noqa: E402
from keras import layers  # noqa: E402

HERE = Path(__file__).resolve().parent.parent
SMALL = Path.home() / "datasets" / "cats_vs_dogs_small"
load = lambda d, seed=0: keras.utils.image_dataset_from_directory(str(d), image_size=(150, 150), batch_size=16,
                                                                    seed=seed, label_mode="int")
test_ds = load(SMALL / "test")


def model(aug):
    L = [keras.Input(shape=(150, 150, 3))]
    if aug:
        L += [layers.RandomFlip("horizontal"), layers.RandomRotation(0.1), layers.RandomZoom(0.2)]
    L += [layers.Rescaling(1 / 255), layers.Conv2D(32, 3, activation="relu"), layers.MaxPooling2D(2),
          layers.Conv2D(32, 3, activation="relu"), layers.MaxPooling2D(2), layers.Conv2D(64, 3, activation="relu"),
          layers.MaxPooling2D(2), layers.Flatten(), layers.Dense(64, activation="relu"), layers.Dropout(0.5),
          layers.Dense(1, activation="sigmoid")]
    m = keras.Sequential(L)
    m.compile(optimizer="rmsprop", loss="binary_crossentropy", metrics=["accuracy"])
    return m


out = {}
for per_class in (250, 500, 1000):
    tmp = Path(tempfile.mkdtemp())
    for cls in ("cat", "dog"):
        (tmp / cls).mkdir()
        for f in sorted((SMALL / "train" / cls).iterdir())[:per_class]:
            (tmp / cls / f.name).symlink_to(f.resolve())
    for aug in (False, True):
        accs = []
        for seed in range(4):
            keras.utils.set_random_seed(seed)
            m = model(aug)
            m.fit(load(tmp, seed), epochs=60, verbose=0)
            accs.append(float(m.evaluate(test_ds, verbose=0)[1]))
        out[f"{2 * per_class}_{'aug' if aug else 'plain'}"] = accs
        print(2 * per_class, "aug" if aug else "plain", np.round(accs, 3), flush=True)
    shutil.rmtree(tmp)
json.dump(out, open(HERE / "data" / "data_size.json", "w"), indent=1)

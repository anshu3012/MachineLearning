"""Two looks at the data for the figures: (1) the width and height of every photo in PetImages (after the Keras
example's cleaning, 23,410 JPEG files); (2) the first training batch exactly as image_dataset_from_directory serves
it (the Note's call: seed 1337, 80/20 split, 256 x 256), stored at 80 x 80 to keep data/ small.
Writes data/sizes.csv.gz and data/batch.npz. Run: python experiments/peek.py [path to PetImages]"""
import os
import sys
from pathlib import Path

os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "3")
os.environ.setdefault("CUDA_VISIBLE_DEVICES", "")
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from PIL import Image  # noqa: E402
import keras  # noqa: E402
import tensorflow as tf  # noqa: E402

HERE = Path(__file__).resolve().parent.parent
ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else Path.home() / "datasets" / "PetImages")
rows = []
for cls in ("Cat", "Dog"):
    for f in sorted((ROOT / cls).glob("*.jpg")):
        with Image.open(f) as im:
            rows.append((cls, im.size[0], im.size[1]))
S = pd.DataFrame(rows, columns=["cls", "width", "height"])
print(len(S), S.cls.value_counts().to_dict(), S[["width", "height"]].drop_duplicates().shape[0], "sizes")
S.to_csv(HERE / "data" / "sizes.csv.gz", index=False)
train_ds, _ = keras.utils.image_dataset_from_directory(str(ROOT), labels="inferred", label_mode="int", batch_size=32,
                                                       image_size=(256, 256), validation_split=0.2, subset="both",
                                                       seed=1337)
x, y = next(iter(train_ds))
small = tf.image.resize(x, (80, 80)).numpy().clip(0, 255).astype(np.uint8)
np.savez_compressed(HERE / "data" / "batch.npz", images=small, labels=y.numpy(), shape=np.array(x.shape),
                    vmin=float(x.numpy().min()), vmax=float(x.numpy().max()))
print(x.shape, y.numpy().tolist())

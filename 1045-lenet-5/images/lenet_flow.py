"""One MNIST test digit flowing through LeNet-5, stage by stage: the real feature maps after each convolution and
pooling layer, the flattened 400 numbers, the 120 and 84 dense activations and the 10 output probabilities.
The model is the Notebook's LeNet-5 (seed 1, 10 epochs, batch 128); its activations are cached in
data/lenet_flow.npz (Plotly frames + ffmpeg). Run: python lenet_flow.py -> lenet_flow.gif, lenet_flow_frames.png"""
import os
import shutil
import subprocess
from pathlib import Path

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from PIL import Image
from common import BLUE, ORANGE, GREEN, GREY, FONT

HERE = Path(__file__).parent
CACHE = HERE.parent / "data" / "lenet_flow.npz"
SHAPES = [(32, 32, 1), (28, 28, 6), (14, 14, 6), (10, 10, 16), (5, 5, 16), (400,), (120,), (84,), (10,)]


def compute():
    os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
    import keras
    (x_train, y_train), (x_test, y_test) = keras.datasets.mnist.load_data()
    x_train = np.pad(x_train, ((0, 0), (2, 2), (2, 2)))[..., None] / 255.0
    x_test = np.pad(x_test, ((0, 0), (2, 2), (2, 2)))[..., None] / 255.0
    keras.utils.set_random_seed(1)
    m = keras.Sequential([
        keras.Input(shape=(32, 32, 1)),
        keras.layers.Conv2D(6, kernel_size=(5, 5), strides=1, padding="valid", activation="tanh"),
        keras.layers.AveragePooling2D(pool_size=(2, 2), strides=2),
        keras.layers.Conv2D(16, kernel_size=(5, 5), strides=1, padding="valid", activation="tanh"),
        keras.layers.AveragePooling2D(pool_size=(2, 2), strides=2),
        keras.layers.Flatten(),
        keras.layers.Dense(120, activation="tanh"),
        keras.layers.Dense(84, activation="tanh"),
        keras.layers.Dense(10, activation="softmax")])
    m.compile(loss="sparse_categorical_crossentropy", optimizer="adam", metrics=["accuracy"])
    m.fit(x_train, y_train, epochs=10, batch_size=128, validation_split=0.1, verbose=0)
    acc = m.evaluate(x_test, y_test, verbose=0)[1]
    x = x_test[:1]
    outs = [x[0]]
    for layer in m.layers:
        x = layer(x)
        outs.append(np.asarray(x)[0])
    np.savez_compressed(CACHE, acc=acc, label=y_test[0], **{f"a{i}": o for i, o in enumerate(outs)})


if not CACHE.exists():
    compute()
D = np.load(CACHE)
A = [D[f"a{i}"] for i in range(9)]
assert [a.shape for a in A] == SHAPES
assert D["acc"] > 0.975                                       # the Note: 98.46% mean test accuracy over 3 seeds
assert np.isclose(A[8].sum(), 1, atol=1e-5) and A[8].argmax() == D["label"]
NAMES = ["input digit", "convolution 1: 6 filters 5 × 5, tanh", "average pooling 1", "convolution 2: 16 filters 5 × 5, tanh",
         "average pooling 2", "flatten", "dense, 120 nodes", "dense, 84 nodes", "output: softmax over 10 digits"]


def maps(a, cols, title):
    n = a.shape[-1]
    rows = int(np.ceil(n / cols))
    fig = make_subplots(rows, cols, horizontal_spacing=0.02, vertical_spacing=0.03)
    for k in range(n):
        fig.add_trace(go.Heatmap(z=a[::-1, :, k], colorscale="RdBu", zmid=0, zmin=-1, zmax=1, showscale=False),
                      row=k // cols + 1, col=k % cols + 1)
    fig.update_xaxes(visible=False, constrain="domain", scaleanchor="y")
    fig.update_yaxes(visible=False, constrain="domain")
    return fig


def stage(i):
    a, shp = A[i], " × ".join(map(str, SHAPES[i]))
    if i == 0:
        fig = go.Figure(go.Heatmap(z=a[::-1, :, 0], colorscale="Greys", showscale=False))
        fig.update_xaxes(visible=False, scaleanchor="y", constrain="domain")
        fig.update_yaxes(visible=False, constrain="domain")
    elif a.ndim == 3:
        fig = maps(a, 3 if a.shape[-1] == 6 else 4, NAMES[i])
    elif i < 8:
        side = {5: 20, 6: 12, 7: 12}[i]
        z = np.full(side * int(np.ceil(len(a) / side)), np.nan)
        z[:len(a)] = a
        fig = go.Figure(go.Heatmap(z=z.reshape(-1, side)[::-1], colorscale="RdBu", zmid=0, zmin=-1, zmax=1,
                                   showscale=False, xgap=1, ygap=1))
        fig.update_xaxes(visible=False, scaleanchor="y", constrain="domain")
        fig.update_yaxes(visible=False, constrain="domain")
    else:
        fig = go.Figure(go.Bar(x=list(range(10)), y=a, marker_color=[GREEN if d == a.argmax() else GREY for d in range(10)],
                               text=[f"{v:.3f}" if v > 0.01 else "" for v in a], textposition="outside",
                               textfont=dict(size=22)))
        fig.update_xaxes(tickvals=list(range(10)), title="digit")
        fig.update_yaxes(range=[0, 1.12], title="probability")
    sub = {5: "400 numbers, shown 20 per row", 6: "shown 12 per row", 7: "shown 12 per row"}.get(i, "")
    fig.update_layout(template="simple_white", width=900, height=680, font=dict(FONT, size=22),
                      title=dict(text=f"<b>{NAMES[i]}</b><br>{shp}" + (f"  ({sub})" if sub else ""), x=0.5,
                                 font=dict(size=24)),
                      margin=dict(l=60, r=30, t=110, b=50))
    return fig


if __name__ == "__main__":
    tmp = HERE / ".flow_frames"
    tmp.mkdir(exist_ok=True)
    files = []
    for i in range(9):
        f = tmp / f"s{i}.png"
        stage(i).write_image(f)
        files.append(f)
    seq = [files[i] for i in range(9) for _ in range(3)] + [files[8]] * 6
    for j, f in enumerate(seq):
        shutil.copy(f, tmp / f"{j:03d}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "2", "-i", str(tmp / "%03d.png"), "-vf",
                    "scale=640:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "lenet_flow.gif")], check=True)
    keys = [Image.open(files[i]).convert("RGB") for i in (0, 1, 3, 8)]
    w, h = keys[0].size
    sheet = Image.new("RGB", (2 * w + 16, 2 * h + 16), "white")
    for i, im in enumerate(keys):
        sheet.paste(im, ((i % 2) * (w + 16), (i // 2) * (h + 16)))
    sheet.save(HERE / "lenet_flow_frames.png")
    shutil.rmtree(tmp)

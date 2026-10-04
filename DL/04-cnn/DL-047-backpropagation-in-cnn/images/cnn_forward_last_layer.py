"""The small CNN of the Note on the Notebook's first 6 x 6 digit (a 0, so y = 0), with the Notebook's starting
weights: forward pass (convolution, ReLU, max pooling, flatten, sigmoid), then the last layer's gradient
dL/dW2 = (a2 - y) F^T. Data: data/digit_example.npz and data/last_layer_grads.csv (both written by the Notebook).
Run: python cnn_forward_last_layer.py  -> .mp4, .gif, _frames.png"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import pandas as pd
from manim import *
from PIL import Image
import manimpango

for _f in Path("/usr/share/texmf/fonts/opentype/public/lm").glob("lmroman10-*.otf"):
    manimpango.register_font(str(_f))

HERE = Path(__file__).parent
NAME = "cnn_forward_last_layer"
BLUE_C, ORANGE_C, GREEN_C, RED_C, PURPLE_C, GREY_C = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#B279A2", "#6B6B6B"
Text.set_default(color=BLACK, font="Latin Modern Roman")
MarkupText.set_default(color=BLACK, font="Latin Modern Roman")

d = np.load(HERE.parent / "data" / "digit_example.npz")
X, t, W1, b1, W2, b2 = d["X"], float(d["t"]), d["W1"], float(d["b1"]), d["W2"], float(d["b2"])
Z1 = np.array([[(X[i:i + 3, j:j + 3] * W1).sum() for j in range(4)] for i in range(4)]) + b1
A1 = np.maximum(Z1, 0)
P1 = A1.reshape(2, 2, 2, 2).max(axis=(1, 3))
F = P1.reshape(4)
a2 = 1 / (1 + np.exp(-(W2.ravel() @ F + b2)))
dW2 = (a2 - t) * F
ref = pd.read_csv(HERE.parent / "data" / "last_layer_grads.csv").set_index("name")["value"]
assert np.allclose(dW2, ref[["dW2_1", "dW2_2", "dW2_3", "dW2_4"]]) and abs(a2 - t - ref["db2"]) < 1e-9


def grid(vals, cell, at, fill=None, fs=18, show=True):
    """Grid of squares; fill(v) gives the colour; numbers shown if show."""
    g = VGroup()
    for r in range(vals.shape[0]):
        for c in range(vals.shape[1]):
            v = vals[r, c]
            sq = Square(cell, stroke_color=GREY_C, stroke_width=1.5,
                        fill_color=fill(v) if fill else WHITE, fill_opacity=1)
            sq.move_to([c * cell, -r * cell, 0])
            g.add(VGroup(sq, Text(f"{v:.2f}", font_size=fs).move_to(sq)) if show else VGroup(sq))
    return g.move_to(at)


ink = lambda v: ManimColor(WHITE).interpolate(ManimColor("#222222"), min(v / 0.7, 1))
warm = lambda v: ManimColor(ORANGE_C).interpolate(WHITE, 1 - min(v / 0.8, 1) * 0.7)


class CNNForward(Scene):
    def snap(self):
        self.snaps.append(Image.fromarray(self.renderer.get_frame()))

    def construct(self):
        self.snaps = []
        Y0 = -0.2
        title = Text("Forward pass on one 6 × 6 digit", font_size=40).to_edge(UP, buff=0.3)
        gx = grid(X, 0.45, [-5.6, Y0, 0], ink, show=False)
        lx = Text("image X", font_size=30, color=GREY_C).next_to(gx, UP, buff=0.2)
        self.play(FadeIn(title), FadeIn(gx), FadeIn(lx))

        # convolution: the filter window slides, each position fills one cell of Z1
        gz = grid(Z1, 0.95, [-1.95, Y0, 0], warm, fs=30)
        lz = MarkupText("Z<sub>1</sub> = X ∗ W<sub>1</sub> + b<sub>1</sub>", font_size=30, color=GREY_C
                        ).next_to(gz, UP, buff=0.2)
        self.play(FadeIn(lz), *[FadeIn(c[0]) for c in gz], run_time=0.5)
        win = Square(1.35, stroke_color=ORANGE_C, stroke_width=6).move_to(gx[0][0].get_center() + 0.45 * (RIGHT + DOWN))
        wlab = MarkupText("filter W<sub>1</sub>, 3 × 3", font_size=30, color=ORANGE_C).next_to(gx, DOWN, buff=0.3)
        self.play(Create(win), FadeIn(wlab), run_time=0.5)
        for k in range(16):
            i, j = divmod(k, 4)
            centre = gx[i * 6 + j][0].get_center() + 0.45 * (RIGHT + DOWN)
            rt = 0.5 if k < 2 else 0.15
            self.play(win.animate.move_to(centre), run_time=rt)
            self.play(FadeIn(gz[k][1]), Indicate(gz[k][0], color=ORANGE_C, scale_factor=1.15), run_time=rt)
        relu = Text("ReLU: all 16 positive, unchanged", font_size=30, color=GREY_C).next_to(gz, DOWN, buff=0.3)
        self.play(FadeOut(win), FadeOut(wlab), FadeIn(relu), run_time=0.6)
        self.wait(0.4)
        self.snap()

        # max pooling: each 2 x 2 window sends its largest value
        gp = grid(P1, 0.95, [1.3, Y0, 0], warm, fs=30)
        lp = MarkupText("P<sub>1</sub>", font_size=30, color=GREY_C).next_to(gp, UP, buff=0.2)
        self.play(FadeIn(lp), *[FadeIn(c[0]) for c in gp], run_time=0.5)
        for w in range(4):
            wi, wj = divmod(w, 2)
            cells = [(2 * wi + a) * 4 + 2 * wj + b for a in (0, 1) for b in (0, 1)]
            box = SurroundingRectangle(VGroup(*[gz[c] for c in cells]), buff=0, color=PURPLE_C, stroke_width=6)
            best = max(cells, key=lambda c: A1.ravel()[c])
            self.play(Create(box), run_time=0.3)
            self.play(TransformFromCopy(gz[best][1], gp[w][1]), Indicate(gz[best][0], color=PURPLE_C), run_time=0.6)
            self.play(FadeOut(box), run_time=0.2)
        mp = Text("max pool", font_size=30, color=PURPLE_C).next_to(gp, DOWN, buff=0.3)
        self.play(FadeIn(mp), run_time=0.3)
        self.wait(0.4)
        self.snap()

        # flatten and output node
        gf = grid(F.reshape(4, 1), 0.85, [3.2, Y0, 0], warm, fs=30)
        lf = Text("F", font_size=30, color=GREY_C).next_to(gf, UP, buff=0.2)
        self.play(FadeIn(lf), *[TransformFromCopy(gp[k], gf[k]) for k in range(4)], run_time=1.0)
        node = Circle(0.6, stroke_color=GREEN_C, stroke_width=5, fill_color=WHITE, fill_opacity=1).move_to([5.4, Y0, 0])
        ntxt = MathTex(r"\sigma", font_size=50, color=BLACK).move_to(node)
        lines = VGroup(*[Line(gf[k].get_right(), node.get_left(), stroke_color=GREEN_C, stroke_width=3) for k in range(4)])
        yh = VGroup(MarkupText(f"ŷ = {a2:.2f}", font_size=36, color=GREEN_C),
                    Text(f"target y = {t:.0f}", font_size=30, color=GREY_C)).arrange(DOWN, buff=0.1).next_to(node, UP, buff=0.3)
        self.play(Create(lines), FadeIn(node), FadeIn(ntxt), run_time=0.8)
        self.play(FadeIn(yh, shift=UP * 0.2), run_time=0.6)
        self.wait(0.8)
        self.snap()

        # backward, last layer only
        keep = VGroup(gf, lf)
        self.play(FadeOut(VGroup(gx, lx, gz, lz, relu, gp, lp, mp, lines, node, ntxt, yh)),
                  Transform(title, MarkupText("Last layer: ∂L/∂W<sub>2</sub> = (a<sub>2</sub> − y) F<sup>T</sup>",
                                              font_size=40).to_edge(UP, buff=0.3)),
                  keep.animate.move_to([-1.6, Y0, 0]), run_time=1.0)
        err = VGroup(Circle(0.6, stroke_width=0, fill_color=RED_C, fill_opacity=0.85),
                     Text(f"{a2 - t:.2f}", font_size=36, color=WHITE, weight=BOLD))
        err[1].move_to(err[0])
        err.move_to([-5.0, Y0, 0])
        elab = MarkupText(f"a<sub>2</sub> − y = {a2:.2f} − {t:.0f}", font_size=30, color=RED_C).next_to(err, DOWN, buff=0.25)
        self.play(FadeIn(err, scale=1.3), FadeIn(elab), run_time=0.7)
        gw = VGroup(*[MarkupText(f"× {F[k]:.2f} = <b>{dW2[k]:.3f}</b>", font_size=36, color=RED_C
                                 ).move_to([1.7, gf[k].get_center()[1], 0], aligned_edge=LEFT)
                      for k in range(4)])
        for k in range(4):
            self.play(Indicate(gf[k], color=RED_C), TransformFromCopy(err[1], gw[k]), run_time=0.7)
        lw = MarkupText("∂L/∂W<sub>2</sub>", font_size=34, color=RED_C).next_to(gw, UP, buff=0.3)
        lb = MarkupText(f"∂L/∂b<sub>2</sub> = {a2 - t:.3f}", font_size=34, color=RED_C).next_to(gw, DOWN, buff=0.4)
        self.play(FadeIn(lw), FadeIn(lb), run_time=0.6)
        self.wait(2.0)
        self.snap()


def key_frames_grid(frames, out, gap=16):
    w, h = frames[0].size
    sheet = Image.new("RGB", (2 * w + gap, 2 * h + gap), "white")
    for i, f in enumerate(frames[:4]):
        sheet.paste(f.convert("RGB"), ((i % 2) * (w + gap), (i // 2) * (h + gap)))
    sheet.save(out)


if __name__ == "__main__":
    media = HERE / ".manim"
    with tempconfig({"quality": "medium_quality", "background_color": WHITE, "media_dir": str(media),
                     "output_file": NAME, "disable_caching": True, "verbosity": "WARNING", "progress_bar": "none"}):
        scene = CNNForward()
        scene.render()
    mp4 = HERE / f"{NAME}.mp4"
    shutil.copy(next(media.rglob(f"{NAME}.mp4")), mp4)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(mp4), "-vf",
                    "fps=10,scale=720:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / f"{NAME}.gif")], check=True)
    key_frames_grid(scene.snaps, HERE / f"{NAME}_frames.png")
    shutil.rmtree(media)

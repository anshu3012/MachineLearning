"""The whole backward pass of the small CNN on the 6 x 6 digit of the part 1 Note (same image and weights):
a2 - y -> dL/dF = W2^T (a2 - y) -> reshape to 2 x 2 -> route to the max of each pooling window -> ReLU mask
-> dL/dW1 = X * dL/dZ1 (slide dL/dZ1 over X) and dL/db1 = sum of dL/dZ1.
Data: data/digit_backward.npz (written by the Notebook's last cell). Run: python cnn_backward_strip.py"""
import shutil
import subprocess
from pathlib import Path

import manimpango
import numpy as np
from manim import *
from PIL import Image

for _f in Path("/usr/share/texmf/fonts/opentype/public/lm").glob("lmroman10-*.otf"):
    manimpango.register_font(str(_f))

HERE = Path(__file__).parent
NAME = "cnn_backward_strip"
BLUE_C, ORANGE_C, GREEN_C, RED_C, PURPLE_C, GREY_C = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#B279A2", "#6B6B6B"
Text.set_default(color=BLACK, font="Latin Modern Roman")
MarkupText.set_default(color=BLACK, font="Latin Modern Roman")

d = np.load(HERE.parent / "data" / "digit_backward.npz")
X, Z1, A1, W2, dZ2 = d["X"], d["Z1"], d["A1"], d["W2"].ravel(), float(d["dZ2"])
dF = W2 * dZ2
dP1 = dF.reshape(2, 2)
assert np.allclose(dP1, d["dP1"])
dZ1 = d["dZ1"]
dW1 = np.array([[(X[i:i + 4, j:j + 4] * dZ1).sum() for j in range(3)] for i in range(3)])
assert np.allclose(dW1, d["dW1"]) and abs(dZ1.sum() - float(d["db1"])) < 1e-12


def num(v, k=2):
    if abs(v) < 1e-12:                               # exact zero only; 0.004 shows as 0.00
        return "0"
    return f"{v:.{k}f}".replace("-", "−")


def gcol(v):
    """Gradient colour: red for negative, blue for positive, paler near 0."""
    if abs(v) < 1e-12:
        return WHITE
    return ManimColor(BLUE_C if v > 0 else RED_C).interpolate(WHITE, 1 - min(abs(v) / 0.25, 1) * 0.75)


def cell(v, size, fs, colour, text=None):
    sq = Square(size, stroke_color=GREY_C, stroke_width=1.5, fill_color=colour, fill_opacity=1)
    return VGroup(sq, Text(text if text is not None else num(v), font_size=fs).move_to(sq))


def grid(vals, size, at, fs=28, colour=gcol, text=None):
    g = VGroup()
    for r in range(vals.shape[0]):
        for c in range(vals.shape[1]):
            g.add(cell(vals[r, c], size, fs, colour(vals[r, c]), text(vals[r, c]) if text else None
                       ).move_to([c * size, -r * size, 0]))
    return g.move_to(at)


ink = lambda v: ManimColor(WHITE).interpolate(ManimColor("#222222"), min(v / 0.7, 1))
warm = lambda v: ManimColor(ORANGE_C).interpolate(WHITE, 1 - min(v / 0.8, 1) * 0.7)


class CNNBackward(Scene):
    def snap(self):
        self.snaps.append(Image.fromarray(self.renderer.get_frame()))

    def construct(self):
        self.snaps = []
        Y0 = -0.2
        title = Text("Backward: from the output to the feature map", font_size=40).to_edge(UP, buff=0.3)
        err = VGroup(Circle(0.55, stroke_width=0, fill_color=RED_C, fill_opacity=0.85),
                     Text(f"{dZ2:.2f}", font_size=34, color=WHITE, weight=BOLD))
        err[1].move_to(err[0])
        err.move_to([6.25, Y0, 0])
        elab = MarkupText("a<sub>2</sub> − y", font_size=30, color=RED_C).next_to(err, UP, buff=0.2)
        self.play(FadeIn(title), FadeIn(err, scale=1.3), FadeIn(elab), run_time=0.8)

        # into F: multiply by W2^T
        gF = grid(dF.reshape(4, 1), 1.05, [4.4, Y0, 0])
        lF = MarkupText("∂L/∂F", font_size=30, color=GREY_C).next_to(gF, UP, buff=0.2)
        sF = MarkupText("× W<sub>2</sub><sup>T</sup>", font_size=30, color=GREEN_C).next_to(gF, DOWN, buff=0.3)
        self.play(FadeIn(lF), FadeIn(sF), *[TransformFromCopy(err, gF[k]) for k in range(4)], run_time=1.2)
        self.wait(0.3)

        # flatten backward: reshape
        gP = grid(dP1, 1.05, [1.95, Y0, 0])
        lP = MarkupText("∂L/∂P<sub>1</sub>", font_size=30, color=GREY_C).next_to(gP, UP, buff=0.2)
        sP = Text("reshape", font_size=30, color=PURPLE_C).next_to(gP, DOWN, buff=0.3)
        self.play(FadeIn(lP), FadeIn(sP), *[TransformFromCopy(gF[k], gP[k]) for k in range(4)], run_time=1.2)
        self.wait(0.5)
        self.snap()

        # max pooling backward: A1 from the forward pass, maxima marked, gradients routed there
        gA = grid(A1, 1.0, [-2.3, Y0, 0], colour=warm)
        lA = MarkupText("A<sub>1</sub> (forward)", font_size=30, color=GREY_C).next_to(gA, UP, buff=0.2)
        self.play(FadeIn(gA), FadeIn(lA), run_time=0.7)
        targets = []
        for w in range(4):
            wi, wj = divmod(w, 2)
            cells = [(2 * wi + a) * 4 + 2 * wj + b for a in (0, 1) for b in (0, 1)]
            best = max(cells, key=lambda c: A1.ravel()[c])
            targets.append(best)
            box = SurroundingRectangle(VGroup(*[gA[c] for c in cells]), buff=0, color=PURPLE_C, stroke_width=6)
            self.play(Create(box), Indicate(gA[best][0], color=PURPLE_C, scale_factor=1.1), run_time=0.5)
            self.play(FadeOut(box), run_time=0.2)
        gdA = grid(d["dA1"], 1.0, [-2.3, Y0, 0])
        ldA = MarkupText("∂L/∂A<sub>1</sub>", font_size=30, color=GREY_C).next_to(gdA, UP, buff=0.2)
        sA = Text("route to each max, 0 elsewhere", font_size=30, color=PURPLE_C).next_to(gdA, DOWN, buff=0.3)
        self.play(*[TransformFromCopy(gP[w], gdA[targets[w]]) for w in range(4)],
                  *[FadeTransform(gA[c], gdA[c]) for c in range(16) if c not in targets],
                  FadeOut(VGroup(*[gA[c] for c in targets])), Transform(lA, ldA), FadeIn(sA), run_time=1.5)
        self.wait(0.6)
        relu = MarkupText("ReLU: Z<sub>1</sub> &gt; 0 in all 16 cells, so ∂L/∂Z<sub>1</sub> = ∂L/∂A<sub>1</sub>",
                          font_size=30, color=GREY_C).to_edge(DOWN, buff=0.45)
        self.play(FadeIn(relu), run_time=0.6)
        self.wait(1.0)
        self.snap()

        # convolution backward: slide dL/dZ1 over X
        gZ = grid(dZ1, 0.75, [-5.45, Y0, 0], fs=22)
        self.play(FadeOut(VGroup(err, elab, gF, lF, sF, gP, lP, sP, sA, relu, lA)),
                  Transform(title, MarkupText("Filter: slide ∂L/∂Z<sub>1</sub> over X", font_size=40
                                              ).to_edge(UP, buff=0.3)),
                  Transform(gdA, gZ), run_time=1.0)
        lZ = MarkupText("∂L/∂Z<sub>1</sub>", font_size=30, color=GREY_C).next_to(gZ, UP, buff=0.2)
        CS = 0.8
        gX = grid(X, CS, [-1.0, Y0, 0], colour=ink, text=lambda v: "")
        lX = Text("image X, 6 × 6", font_size=30, color=GREY_C).next_to(gX, UP, buff=0.2)
        gW = grid(np.zeros((3, 3)), 1.05, [4.65, Y0, 0], fs=32, colour=lambda v: WHITE, text=lambda v: "")
        lW = MarkupText("∂L/∂W<sub>1</sub>", font_size=30, color=GREY_C).next_to(gW, UP, buff=0.2)
        self.play(FadeIn(lZ), FadeIn(gX), FadeIn(lX), FadeIn(gW), FadeIn(lW), run_time=0.8)
        # the sliding window: only the non-zero gradients drawn, as coloured dots on X's cells
        nz = [(r, c) for r in range(4) for c in range(4) if abs(dZ1[r, c]) > 1e-12]
        def make_win(i, j):
            frame = Square(4 * CS, stroke_color=RED_C, stroke_width=6).move_to(
                gX[i * 6 + j].get_center() + 1.5 * CS * (RIGHT + DOWN))
            dots = VGroup(*[Square(CS * 0.8, stroke_width=0, fill_color=gcol(dZ1[r, c]), fill_opacity=0.9
                                   ).move_to(gX[(i + r) * 6 + j + c].get_center()) for r, c in nz])
            return VGroup(frame, dots)

        win = make_win(0, 0)
        self.play(TransformFromCopy(gdA, win), run_time=1.0)
        for k in range(9):
            i, j = divmod(k, 3)
            if k:
                self.play(Transform(win, make_win(i, j)), run_time=0.5 if k < 3 else 0.3)
            val = cell(dW1[i, j], 1.05, 28, gcol(dW1[i, j] / 0.8), num(dW1[i, j])).move_to(gW[k])
            self.play(FadeIn(val, scale=1.2), run_time=0.6 if k < 3 else 0.3)
            if k == 0:
                expl = Text("multiply cell by cell, add up", font_size=30, color=RED_C).to_edge(DOWN, buff=0.45)
                self.play(FadeIn(expl), run_time=0.5)
                self.wait(0.6)
                self.snap()
                self.play(FadeOut(expl), run_time=0.3)
        bias = MarkupText(f"∂L/∂b<sub>1</sub> = sum of ∂L/∂Z<sub>1</sub> = {num(dZ1.sum())}", font_size=32,
                          color=RED_C).to_edge(DOWN, buff=0.45)
        self.play(FadeOut(win), FadeIn(bias), run_time=0.8)
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
        scene = CNNBackward()
        scene.render()
    mp4 = HERE / f"{NAME}.mp4"
    shutil.copy(next(media.rglob(f"{NAME}.mp4")), mp4)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(mp4), "-vf",
                    "fps=10,scale=720:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse=dither=bayer:bayer_scale=5:diff_mode=rectangle",
                    str(HERE / f"{NAME}.gif")], check=True)
    key_frames_grid(scene.snaps, HERE / f"{NAME}_frames.png")
    shutil.rmtree(media)

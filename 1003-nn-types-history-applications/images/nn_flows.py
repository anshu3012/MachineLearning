"""How data moves through the five network types, one type at a time (Manim):
1 MLP: a signal passes layer by layer, one way.      2 CNN: a 3x3 filter slides over a real 8x8 digit (true convolution values).
3 RNN: words enter one at a time; the hidden state loops back.
4 Autoencoder: a real 64-8-64 network (scikit-learn digits) squeezes a digit to 8 numbers and rebuilds it.
5 GAN: generator makes a fake, discriminator judges it, the verdict goes back (schematic).
Run: python nn_flows.py -> nn_flows.mp4, .gif, _frames.png"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
from manim import *
from PIL import Image
import manimpango
from sklearn.datasets import load_digits
from sklearn.neural_network import MLPRegressor

for f in Path("/usr/share/texmf/fonts/opentype/public/lm").glob("lmroman10-*.otf"):   # pango on topgro misses LM
    manimpango.register_font(str(f))

HERE = Path(__file__).parent
BLUE_C, ORANGE_C, GREEN_C, RED_C, GREY_C = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#6B6B6B"
Text.set_default(color=BLACK, font="Latin Modern Roman")

# real data: one 8x8 digit, its convolution with a vertical-edge filter, and its rebuild by a 64-8-64 autoencoder
digits = load_digits()
X = digits.data / 16.0
IDX = 3                                                     # a "3"
img = X[IDX].reshape(8, 8)
KERNEL = np.array([[-1, 0, 1]] * 3)
fmap = np.array([[(img[r:r + 3, c:c + 3] * KERNEL).sum() for c in range(6)] for r in range(6)])
auto = MLPRegressor(hidden_layer_sizes=(8,), activation="relu", max_iter=3000, random_state=0).fit(X, X)
rebuilt = np.clip(auto.predict(X[IDX:IDX + 1]).reshape(8, 8), 0, 1)
REBUILD_ERR = float(np.abs(rebuilt - img).mean())
assert REBUILD_ERR < 0.15                                   # the rebuilt digit is close, not exact


def pixels(arr, cell, color=BLACK):
    """A grid of squares; darker = larger value (arr in 0..1)."""
    g = VGroup(*[Square(side_length=cell, stroke_width=1, stroke_color=GREY_C, fill_opacity=1,
                        fill_color=interpolate_color(ManimColor(WHITE), ManimColor(color), float(v)))
                 .move_to([c * cell, -r * cell, 0]) for r, row in enumerate(arr) for c, v in enumerate(row)])
    return g.move_to(ORIGIN)


def node(pos, color=GREY_C, r=0.3):
    return Circle(radius=r, color=color, stroke_width=4, fill_color=WHITE, fill_opacity=1).move_to(pos)


def column(n, x, color, gap=0.95, y0=-0.5):
    return [node([x, (i - (n - 1) / 2) * gap + y0, 0], color) for i in range(n)]


def edges(a, b):
    return [Line(p.get_center(), q.get_center(), color=GREY_C, stroke_width=2).set_z_index(-1) for p in a for q in b]


class Flows(Scene):
    def head(self, name, line):
        t = Text(name, font_size=40, weight=BOLD).to_edge(UP, buff=0.3)
        s = Text(line, font_size=30, color=GREY_C).next_to(t, DOWN, buff=0.2)
        self.play(FadeIn(t, s), run_time=0.4)

    def done(self, hold=1.2):
        self.wait(hold)
        self.snaps.append(Image.fromarray(self.renderer.get_frame()))
        self.play(FadeOut(*self.mobjects), run_time=0.4)

    def pulse(self, lines, color=ORANGE_C, t=0.7):
        self.play(*[ShowPassingFlash(e.copy().set_stroke(color, 7), time_width=0.6) for e in lines], run_time=t)

    def mlp(self):
        self.head("1. Multi-layer perceptron (MLP)", "The signal moves one way: input, hidden layers, output")
        cols = [column(n, x, c) for n, x, c in zip((3, 4, 4, 2), (-4.5, -1.5, 1.5, 4.5), (BLUE_C, GREEN_C, GREEN_C, ORANGE_C))]
        es = [edges(a, b) for a, b in zip(cols, cols[1:])]
        labs = VGroup(*[Text(s, font_size=28).move_to([x, -3.3, 0]) for s, x in
                        (("input layer", -4.5), ("hidden layers", 0), ("output layer", 4.5))])
        self.play(FadeIn(*[n for c in cols for n in c], *[e for g in es for e in g], labs), run_time=0.5)
        for _ in range(2):
            self.play(*[n.animate.set_fill(ORANGE_C) for n in cols[0]], run_time=0.25)
            for i, g in enumerate(es):
                self.pulse(g)
                self.play(*[n.animate.set_fill(WHITE) for n in cols[i]], *[n.animate.set_fill(ORANGE_C) for n in cols[i + 1]],
                          run_time=0.25)
            self.wait(0.4)
            if _ == 0:
                self.play(*[n.animate.set_fill(WHITE) for n in cols[-1]], run_time=0.2)
        self.done()

    def cnn(self):
        self.head("2. Convolutional neural network (CNN)", "A small filter slides over the image and writes one number per stop")
        cell = 0.55
        im = pixels(img, cell).move_to([-3.6, -0.9, 0])
        out_cells = pixels(np.abs(fmap) / np.abs(fmap).max(), cell, BLUE_C).move_to([3.6, -0.9, 0])
        frame = Square(side_length=cell * 6, stroke_color=GREY_C, stroke_width=2).move_to(out_cells)
        win = Square(side_length=3 * cell, stroke_color=ORANGE_C, stroke_width=7)
        labs = VGroup(Text("image, 8 × 8 pixels", font_size=28).next_to(im, DOWN, buff=0.25),
                      Text("feature map, 6 × 6", font_size=28).next_to(frame, DOWN, buff=0.25))
        arrow = Arrow([-1.1, -0.9, 0], [1.6, -0.9, 0], color=GREY_C, stroke_width=4)
        flab = Text("3 × 3 filter", font_size=28, color=ORANGE_C).next_to(arrow, UP, buff=0.15)
        self.play(FadeIn(im, frame, labs, arrow, flab), run_time=0.5)
        self.add(win)
        for r in range(6):
            for c in range(6):
                win.move_to(im[(r + 1) * 8 + (c + 1)])            # centre pixel of the 3x3 patch
                self.add(out_cells[r * 6 + c])
                self.wait(0.13 if r else 0.3)                      # slower on the first row
        self.done()

    def rnn(self):
        self.head("3. Recurrent neural network (RNN)", "Words enter one at a time; the hidden layer's output loops back")
        x, h, y = node([0, -2.6, 0], BLUE_C, 0.45), node([0, -0.6, 0], GREEN_C, 0.6), node([0, 1.3, 0], ORANGE_C, 0.45)
        up1 = Arrow(x.get_top(), h.get_bottom(), buff=0.05, color=GREY_C, stroke_width=4)
        up2 = Arrow(h.get_top(), y.get_bottom(), buff=0.05, color=GREY_C, stroke_width=4)
        loop = CurvedArrow(h.get_right() + UP * 0.25, h.get_right() + DOWN * 0.25, angle=-4.6, color=RED_C, stroke_width=5)
        looplab = Text("memory of\nearlier words", font_size=28, color=RED_C).next_to(loop, RIGHT, buff=0.2)
        names = VGroup(Text("input", font_size=28).next_to(x, LEFT, buff=0.3), Text("hidden", font_size=28).next_to(h, LEFT, buff=0.3),
                       Text("output", font_size=28).next_to(y, LEFT, buff=0.3))
        words = ["the", "film", "was", "good"]
        queue = VGroup(*[Text(w, font_size=34) for w in words]).arrange(RIGHT, buff=0.45).move_to([-4.8, -2.6, 0])
        self.play(FadeIn(x, h, y, up1, up2, loop, looplab, names, queue), run_time=0.5)
        seen = VGroup()
        for k, w in enumerate(queue):
            self.play(w.animate.scale(0.75).move_to(x), run_time=0.45)
            self.pulse([Line(x.get_top(), h.get_bottom())], BLUE_C, 0.4)
            self.play(h.animate.set_fill(interpolate_color(ManimColor(WHITE), ManimColor(GREEN_C), (k + 1) / 4)), run_time=0.25)
            self.pulse([loop], RED_C, 0.6)
            tag = Text(words[k], font_size=26, color=GREEN_C)
            seen.add(tag)
            seen.arrange(RIGHT, buff=0.25).move_to([4.3, -2.6, 0])
            self.play(FadeOut(w), FadeIn(tag), run_time=0.25)
        held = Text("held in the hidden layer:", font_size=28, color=GREEN_C).next_to(seen, UP, buff=0.25)
        self.pulse([Line(h.get_top(), y.get_bottom())], ORANGE_C, 0.4)
        self.play(FadeIn(held), y.animate.set_fill(ORANGE_C), run_time=0.4)
        self.done()

    def auto(self):
        self.head("4. Autoencoder", "Squeeze the input through a narrow middle, then rebuild it")
        cell = 0.36
        a, b = pixels(img, cell).move_to([-5.2, -0.7, 0]), pixels(rebuilt, cell).move_to([5.2, -0.7, 0])
        cols = [column(n, x, c, gap=0.62, y0=-0.7) for n, x, c in zip((6, 2, 6), (-2.3, 0, 2.3), (BLUE_C, GREEN_C, ORANGE_C))]
        es = [edges(p, q) for p, q in zip(cols, cols[1:])]
        labs = VGroup(Text("input: 64 pixels", font_size=28).move_to([-4.2, -3.3, 0]),
                      Text("middle: 8 numbers", font_size=28, color=GREEN_C).move_to([0, -3.3, 0]),
                      Text("rebuilt: 64 pixels", font_size=28).move_to([4.2, -3.3, 0]))
        self.play(FadeIn(a, *[n for c in cols for n in c], *[e for g in es for e in g], labs[0]), run_time=0.5)
        self.play(*[n.animate.set_fill(BLUE_C) for n in cols[0]], run_time=0.3)
        self.pulse(es[0], BLUE_C, 0.9)
        self.play(*[n.animate.set_fill(GREEN_C) for n in cols[1]], FadeIn(labs[1]), run_time=0.4)
        self.wait(0.5)
        self.pulse(es[1], GREEN_C, 0.9)
        self.play(*[n.animate.set_fill(ORANGE_C) for n in cols[2]], FadeIn(b, labs[2]), run_time=0.5)
        self.done(1.6)

    def gan(self):
        self.head("5. Generative adversarial network (GAN)", "One network makes fakes, the other judges them")
        def box(s, color, pos):
            r = RoundedRectangle(corner_radius=0.15, width=3.3, height=1.2, color=color, stroke_width=5,
                                 fill_color=color, fill_opacity=0.12).move_to(pos)
            return VGroup(r, Text(s, font_size=32).move_to(r))
        g, d = box("generator", GREEN_C, [-4.2, -0.4, 0]), box("discriminator", RED_C, [3.6, -0.4, 0])
        real = box("real images", BLUE_C, [3.6, -2.7, 0])
        ra = Arrow(real.get_top(), d.get_bottom(), buff=0.08, color=GREY_C, stroke_width=4)
        back = CurvedArrow(d.get_top() + LEFT * 0.4, g.get_top() + RIGHT * 0.4, angle=0.9, color=GREY_C, stroke_width=4)
        backlab = Text("verdict goes back: the generator adjusts", font_size=28, color=GREY_C).next_to(back, UP, buff=0.05)
        self.play(FadeIn(g, d, real, ra), run_time=0.5)
        rng = np.random.default_rng(0)
        for k, (noise, verdict, col) in enumerate(((1.0, "fake", RED_C), (0.5, "fake", RED_C), (0.0, "real?", GREEN_C))):
            fake = pixels(np.clip(img + noise * rng.uniform(-1, 1, img.shape), 0, 1), 0.14).move_to(g.get_right() + RIGHT * 0.8)
            self.play(FadeIn(fake), run_time=0.25)
            self.play(fake.animate.move_to(d.get_left() + LEFT * 0.8), run_time=0.6)
            v = Text(verdict, font_size=36, color=col, weight=BOLD).next_to(d, RIGHT, buff=0.25)
            self.play(FadeIn(v), run_time=0.25)
            if k == 0:
                self.play(FadeIn(back, backlab), run_time=0.3)
            self.pulse([back], col, 0.6)
            if k < 2:
                self.play(FadeOut(fake, v), run_time=0.25)
        self.done(1.6)

    def construct(self):
        self.snaps = []
        for part in (self.mlp, self.cnn, self.rnn, self.auto, self.gan):
            part()


if __name__ == "__main__":
    print("autoencoder mean absolute rebuild error on the shown digit:", round(REBUILD_ERR, 3))
    media = HERE / ".manim"
    with tempconfig({"quality": "medium_quality", "background_color": WHITE, "media_dir": str(media),
                     "output_file": "nn_flows", "disable_caching": True, "verbosity": "WARNING", "progress_bar": "none"}):
        scene = Flows()
        scene.render()
    mp4 = HERE / "nn_flows.mp4"
    shutil.copy(next(media.rglob("nn_flows.mp4")), mp4)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(mp4), "-vf",
                    "fps=8,scale=640:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "nn_flows.gif")], check=True)
    w, h = scene.snaps[0].size
    sheet = Image.new("RGB", (2 * w + 16, 3 * h + 32), "white")
    for i, f in enumerate(scene.snaps):
        sheet.paste(f.convert("RGB"), ((i % 2) * (w + 16), (i // 2) * (h + 16)))
    sheet.save(HERE / "nn_flows_frames.png")
    shutil.rmtree(media)

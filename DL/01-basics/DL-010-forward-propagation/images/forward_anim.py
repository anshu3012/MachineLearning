"""Forward propagation through the 4-3-2-1 network, layer by layer, with the weights of the Note.
Run: python forward_anim.py -> forward_anim.mp4, .gif, _frames.png"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
from manim import *
from PIL import Image

HERE = Path(__file__).parent
BLUE_C, ORANGE_C, GREEN_C, RED_C, GREY_C = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#6B6B6B"
Text.set_default(color=BLACK, font="Latin Modern Roman")
MathTex.set_default(color=BLACK)

# the Note's numbers (also in the Notebook)
A0 = np.array([0.72, 0.72, 0.69, 0.81])
W = {1: np.array([[0.2, -0.3, 0.5], [0.4, 0.1, -0.2], [-0.5, 0.2, 0.1], [0.3, -0.4, 0.2]]),
     2: np.array([[0.6, -0.4], [-0.2, 0.5], [0.3, 0.7]]),
     3: np.array([[0.8], [-0.6]])}
B = {1: np.array([0.1, -0.1, 0.2]), 2: np.array([0.1, -0.2]), 3: np.array([0.2])}
sig = lambda z: 1 / (1 + np.exp(-z))


def forward():
    a, out = A0, {0: (None, A0)}
    for k in (1, 2, 3):
        z = W[k].T @ a + B[k]
        a = sig(z)
        out[k] = (z, a)
    return out


SIZES = [4, 3, 2, 1]
COLS = [-5.2, -3.5, -1.8, -0.1]
LAYER_C = {1: BLUE_C, 2: ORANGE_C, 3: GREEN_C}


def vec(v, d=3):
    return r"\begin{bmatrix}" + r"\\".join(f"{x:.{d}f}" for x in v) + r"\end{bmatrix}"


class Forward(Scene):
    def snap(self):
        self.snaps.append(Image.fromarray(self.renderer.get_frame()))

    def construct(self):
        self.snaps = []
        res = forward()
        title = Text("Forward propagation: one row through the network", font_size=30, weight=BOLD).to_edge(UP, buff=0.25)
        nodes = {}
        for l, (n, x) in enumerate(zip(SIZES, COLS)):
            for j in range(n):
                y = ((n - 1) / 2 - j) * 1.35 - 0.3
                nodes[l, j] = Circle(radius=0.45, color=GREY_C, stroke_width=4, fill_color=WHITE, fill_opacity=1).move_to([x, y, 0])
        edges = {k: VGroup(*[Line(nodes[k - 1, i].get_center(), nodes[k, j].get_center(), color=GREY_C, stroke_width=2,
                                  stroke_opacity=0.35).set_z_index(-1)
                             for i in range(SIZES[k - 1]) for j in range(SIZES[k])]) for k in (1, 2, 3)}
        labels = VGroup(*[Text(t, font_size=22, color=GREY_C).move_to([x, -3.45, 0])
                          for t, x in zip(["layer 0", "layer 1", "layer 2", "layer 3"], COLS)])
        names = VGroup(*[Text(t, font_size=20).next_to(nodes[0, j], LEFT, buff=0.15)
                         for j, t in enumerate(["CGPA", "IQ", "10th", "12th"])])
        self.add(title, *edges.values(), *nodes.values(), labels, names)
        vals = VGroup(*[Text(f"{v:.2f}", font_size=22).move_to(nodes[0, j]) for j, v in enumerate(A0)])
        head = MathTex(r"a^{0} = " + vec(A0, 2), font_size=34).move_to([4.0, 1.0, 0])
        cap = Text("the row, scaled, enters layer 0", font_size=22, color=GREY_C).next_to(head, DOWN, buff=0.4)
        self.play(FadeIn(vals), FadeIn(head), FadeIn(cap), run_time=1)
        self.wait(0.8)
        self.snap()
        panel = VGroup(head, cap)
        for k in (1, 2, 3):
            c = LAYER_C[k]
            z, a = res[k]
            eq = MathTex(rf"a^{{{k}}} = \sigma\!\left(W^{{{k}\mathsf T}} a^{{{k-1}}} + b^{{{k}}}\right)", font_size=36)
            n_in, n_out = SIZES[k - 1], SIZES[k]
            shp = MathTex(rf"({n_out}\times{n_in})({n_in}\times1) + ({n_out}\times1) = {n_out}\times1", font_size=30, color=GREY_C)
            zz = MathTex(rf"z^{{{k}}} = " + vec(z), r"\;\Rightarrow\;", rf"a^{{{k}}} = " + vec(a), font_size=32)
            zz[2].set_color(c)
            new = VGroup(eq, shp, zz).arrange(DOWN, buff=0.45).move_to([4.0, 0.0, 0])
            self.play(FadeOut(panel), edges[k].animate.set_stroke(color=c, opacity=1, width=3),
                      *[nodes[k, j].animate.set_stroke(color=c) for j in range(n_out)], run_time=0.8)
            self.play(Write(eq), FadeIn(shp), run_time=1.2)
            self.play(FadeIn(zz), run_time=0.8)
            out_vals = [Text(f"{v:.3f}", font_size=20, color=c).move_to(nodes[k, j]) for j, v in enumerate(a)]
            self.play(*[TransformFromCopy(zz[2], t) for t in out_vals], run_time=1.0)
            self.play(edges[k].animate.set_stroke(color=GREY_C, opacity=0.35, width=2), run_time=0.4)
            panel = new
            self.wait(1.0 if k < 3 else 0.3)
            if k in (1, 2):
                self.snap()
        yhat = MathTex(rf"\hat{{y}} = {res[3][1][0]:.3f}", font_size=40, color=GREEN_C).next_to(nodes[3, 0], DOWN, buff=0.35)
        prob = Text("probability of placement", font_size=20, color=GREEN_C).next_to(yhat, DOWN, buff=0.15)
        self.play(FadeIn(yhat), FadeIn(prob))
        self.wait(1.5)
        self.snap()


def key_frames_grid(frames, out, gap=16):
    w, h = frames[0].size
    sheet = Image.new("RGB", (2 * w + gap, 2 * h + gap), "white")
    for i, f in enumerate(frames[:4]):
        sheet.paste(f.convert("RGB"), ((i % 2) * (w + gap), (i // 2) * (h + gap)))
    sheet.save(out)


if __name__ == "__main__":
    for k, (z, a) in forward().items():
        print(k, z, a)
    media = HERE / ".manim"
    with tempconfig({"quality": "medium_quality", "background_color": WHITE, "media_dir": str(media),
                     "output_file": "forward_anim", "disable_caching": True, "verbosity": "WARNING",
                     "progress_bar": "none"}):
        scene = Forward()
        scene.render()
    mp4 = HERE / "forward_anim.mp4"
    shutil.copy(next(media.rglob("forward_anim.mp4")), mp4)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(mp4), "-vf",
                    "fps=12,scale=720:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "forward_anim.gif")], check=True)
    key_frames_grid(scene.snaps, HERE / "forward_anim_frames.png")
    shutil.rmtree(media)

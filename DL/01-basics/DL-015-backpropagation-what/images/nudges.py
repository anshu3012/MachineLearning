"""Backpropagation as a list of wishes, on the Note's 2-2-1 network and student 1 (Manim).
The prediction 0.32 must rise towards 4. Three ways to raise it: its bias, its two weights (which count 1.6 times as much,
because each is multiplied by a hidden output of 1.6), and the hidden outputs (which count only 0.1 each, the size of
their weights). The wish on each hidden output is passed back one layer in the same way. Arrow lengths are the sizes
of the gradients of the Note: 11.78, 7.36, 5.89, 0.74.
Run: python nudges.py -> nudges.mp4, .gif, _frames.png"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
from manim import *
from PIL import Image
import manimpango

for f in Path("/usr/share/texmf/fonts/opentype/public/lm").glob("lmroman10-*.otf"):   # pango on topgro misses LM
    manimpango.register_font(str(f))

HERE = Path(__file__).parent
BLUE_C, ORANGE_C, GREEN_C, RED_C, GREY_C = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#6B6B6B"
Text.set_default(color=BLACK, font="Latin Modern Roman")
MathTex.set_default(color=BLACK)

# the Note's numbers
x, y = np.array([8.0, 8.0]), 4.0
W1, W2 = np.full((2, 2), 0.1), np.full(2, 0.1)
O1 = W1.T @ x
y_hat = W2 @ O1
g = 2 * (y - y_hat)                                  # size of dL/dy_hat
G = {"W2": g * O1[0], "b2": g, "O": g * W2[0], "W1": g * W2[0] * x[0], "b1": g * W2[0]}
assert [round(v, 2) for v in G.values()] == [11.78, 7.36, 0.74, 5.89, 0.74]
SCALE = 0.11                                         # arrow length per unit of gradient


def up(pos, size, color, label, side=RIGHT):
    """An up arrow whose length is the gradient size, with its number."""
    L = max(size * SCALE, 0.16)
    a = Arrow(np.array(pos) + DOWN * L / 2, np.array(pos) + UP * L / 2, buff=0, color=color, stroke_width=7,
              max_tip_length_to_length_ratio=0.5, max_stroke_width_to_length_ratio=40)
    t = Text(label, font_size=24, color=color).next_to(a, side, buff=0.08)
    return VGroup(a, t)


class Nudges(Scene):
    def construct(self):
        snaps = []
        snap = lambda: snaps.append(Image.fromarray(self.renderer.get_frame()))
        title = Text("Who should change, and by how much?", font_size=34, weight=BOLD).to_edge(UP, buff=0.2)
        P = {"x1": [-5.9, 1.7, 0], "x2": [-5.9, -1.7, 0], "h1": [-3.0, 1.7, 0], "h2": [-3.0, -1.7, 0], "o": [-0.2, 0, 0]}
        node = lambda p: Circle(radius=0.5, color=GREY_C, stroke_width=4, fill_color=WHITE, fill_opacity=1).move_to(p)
        nodes = {k: node(v) for k, v in P.items()}
        e1 = {(i, j): Line(P[f"x{i}"], P[f"h{j}"], color=GREY_C, stroke_width=3).set_z_index(-1) for i in (1, 2) for j in (1, 2)}
        e2 = {j: Line(P[f"h{j}"], P["o"], color=GREY_C, stroke_width=3).set_z_index(-1) for j in (1, 2)}
        vals = VGroup(*[Text(s, font_size=30).move_to(nodes[k]) for k, s in
                        (("x1", "8"), ("x2", "8"), ("h1", "1.6"), ("h2", "1.6"), ("o", "0.32"))])
        names = VGroup(Text("CGPA", font_size=26).next_to(nodes["x1"], UP, buff=0.1), Text("profile", font_size=26).next_to(nodes["x2"], DOWN, buff=0.1))
        self.add(title, *e1.values(), *e2.values(), *nodes.values(), vals, names)

        def say(lines, color=BLACK):
            t = VGroup(*[Text(s, font_size=25, color=color) for s in lines]).arrange(DOWN, buff=0.16, aligned_edge=LEFT).move_to([4.2, -0.3, 0])
            if getattr(self, "cap", None):
                self.remove(self.cap)
            self.cap = t
            self.play(FadeIn(t), run_time=0.4)

        # 1. the output must rise
        want = up([0.75, 0.0, 0], 12, GREEN_C, "")
        say(["The network says 0.32,", "the data says 4.", "The output must rise."], GREEN_C)
        self.play(GrowFromEdge(want[0], DOWN), run_time=0.7)
        self.wait(1.4)
        # 2. three ways
        b2 = up([-0.2, -1.05, 0], G["b2"], BLUE_C, "bias 7.36")
        say(["Way 1: raise the output bias.", "It is added as it is: it counts 1."], BLUE_C)
        self.play(FadeIn(b2), run_time=0.5)
        self.wait(1.5)
        w2 = VGroup(up(e2[1].point_from_proportion(0.6) + UP * 0.95, G["W2"], BLUE_C, "weight 11.78"),
                    up(e2[2].point_from_proportion(0.6) + DOWN * 1.2, G["W2"], BLUE_C, "weight 11.78"))
        say(["Way 2: raise the two weights.", "Each is multiplied by a hidden", "output of 1.6, so it counts", "1.6 times the bias:", "7.36 × 1.6 = 11.78."], BLUE_C)
        self.play(FadeIn(w2), e2[1].animate.set_stroke(BLUE_C, 5), e2[2].animate.set_stroke(BLUE_C, 5), run_time=0.6)
        self.wait(2.4)
        snap()
        wish = VGroup(up(P["h1"] + np.array([0.8, 0.3, 0]), G["O"], ORANGE_C, "0.74", UP), up(P["h2"] + np.array([0.8, 0.45, 0]), G["O"], ORANGE_C, "0.74", UP))
        say(["Way 3: raise the hidden outputs.", "Each is multiplied by a weight", "of only 0.1: 7.36 × 0.1 = 0.74.", "We cannot set them directly,", "so this wish is passed back."], ORANGE_C)
        self.play(FadeIn(wish), nodes["h1"].animate.set_stroke(ORANGE_C), nodes["h2"].animate.set_stroke(ORANGE_C), run_time=0.6)
        self.wait(2.6)
        snap()
        # 3. one layer back
        b1 = VGroup(up(P["h1"] + UP * 0.75, G["b1"], BLUE_C, "bias 0.74", UP), up(P["h2"] + DOWN * 0.75, G["b1"], BLUE_C, "bias 0.74", DOWN))
        pos = {(1, 1): UP * 0.5, (2, 2): DOWN * 0.5, (1, 2): LEFT * 0.45, (2, 1): LEFT * 0.45}
        prop = {(1, 1): 0.4, (2, 2): 0.4, (1, 2): 0.3, (2, 1): 0.3}
        w1 = VGroup(*[up(e1[k].point_from_proportion(prop[k]) + pos[k], G["W1"], BLUE_C, "5.89", LEFT if k[0] != k[1] else RIGHT) for k in e1])
        say(["One layer back, the same rule.", "Each hidden bias counts 1:", "0.74.", "Each weight is multiplied by", "an input of 8: 0.74 × 8 = 5.89."], BLUE_C)
        self.play(FadeIn(b1, w1), *[e.animate.set_stroke(BLUE_C, 5) for e in e1.values()], run_time=0.7)
        self.wait(2.8)
        snap()
        say(["Each blue arrow is one gradient.", "A parameter multiplied by a", "larger number gets a larger arrow."], BLACK)
        self.wait(2.5)
        snap()
        self.snaps = snaps


if __name__ == "__main__":
    media = HERE / ".manim"
    with tempconfig({"quality": "medium_quality", "frame_rate": 15, "background_color": WHITE, "media_dir": str(media),
                     "output_file": "nudges", "disable_caching": True, "verbosity": "WARNING", "progress_bar": "none"}):
        scene = Nudges()
        scene.render()
    mp4 = HERE / "nudges.mp4"
    shutil.copy(next(media.rglob("nudges.mp4")), mp4)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(mp4), "-vf",
                    "fps=8,scale=720:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse", str(HERE / "nudges.gif")], check=True)
    w, h = scene.snaps[0].size
    sheet = Image.new("RGB", (2 * w + 16, 2 * h + 16), "white")
    for i, f in enumerate(scene.snaps[:4]):
        sheet.paste(f.convert("RGB"), ((i % 2) * (w + 16), (i // 2) * (h + 16)))
    sheet.save(HERE / "nudges_frames.png")
    shutil.rmtree(media)

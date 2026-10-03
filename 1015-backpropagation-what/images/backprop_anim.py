"""Backpropagation on the 2-2-1 regression network for the first student: forward values, the loss, then the
gradients flowing backward onto every weight and bias, then the update (learning rate 0.001).
Run: python backprop_anim.py -> backprop_anim.mp4, .gif, _frames.png"""
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
x, y, lr = np.array([8.0, 8.0]), 4.0, 0.001
W1, b1, W2, b2 = np.full((2, 2), 0.1), np.zeros(2), np.full(2, 0.1), 0.0
O1 = W1.T @ x + b1
y_hat = W2 @ O1 + b2
L = (y - y_hat) ** 2
g = -2 * (y - y_hat)
gW2, gb2, gO1 = g * O1, g, g * W2
gW1, gb1 = np.outer(x, gO1), gO1


class Backprop(Scene):
    def snap(self):
        self.snaps.append(Image.fromarray(self.renderer.get_frame()))

    def node(self, pos, color=GREY_C):
        return Circle(radius=0.42, color=color, stroke_width=4, fill_color=WHITE, fill_opacity=1).move_to(pos)

    def construct(self):
        self.snaps = []
        title = Text("Backpropagation: one student, one update", font_size=28, weight=BOLD).to_edge(UP, buff=0.25)
        P = {"x1": [-6.3, 1.3, 0], "x2": [-6.3, -1.3, 0], "h1": [-4.0, 1.3, 0], "h2": [-4.0, -1.3, 0],
             "o": [-1.9, 0, 0]}
        nodes = {k: self.node(v) for k, v in P.items()}
        e1 = {(i, j): Line(nodes[f"x{i}"].get_center(), nodes[f"h{j}"].get_center(), color=GREY_C,
                           stroke_width=3).set_z_index(-1) for i in (1, 2) for j in (1, 2)}
        e2 = {j: Line(nodes[f"h{j}"].get_center(), nodes["o"].get_center(), color=GREY_C, stroke_width=3).set_z_index(-1)
              for j in (1, 2)}
        names = VGroup(Text("CGPA", font_size=20).next_to(nodes["x1"], UP, buff=0.12),
                       Text("profile", font_size=20).next_to(nodes["x2"], DOWN, buff=0.12))
        lossbox = RoundedRectangle(corner_radius=0.15, width=1.0, height=0.8, color=RED_C, stroke_width=4).move_to([-0.35, 0, 0])
        losslab = MathTex(r"L", font_size=40).move_to(lossbox)
        arrow = Arrow(nodes["o"].get_right(), lossbox.get_left(), buff=0.05, color=GREY_C, stroke_width=4)
        # weight labels: W1 labels near the input side, W2 labels mid-edge
        def lab(tex, line, t, shift, color=GREY_C, fs=24):
            return MathTex(tex, font_size=fs, color=color).move_to(line.point_from_proportion(t) + shift)
        w1pos = {(1, 1): (0.5, UP * 0.3), (2, 2): (0.5, DOWN * 0.3), (1, 2): (0.22, RIGHT * 0.45), (2, 1): (0.22, RIGHT * 0.45)}
        w1lab = {k: lab(f"W^1_{{{k[0]}{k[1]}}}", e1[k], *w1pos[k]) for k in e1}
        w2lab = {j: lab(f"W^2_{{{j}1}}", e2[j], 0.5, (UP if j == 1 else DOWN) * 0.35) for j in (1, 2)}
        self.add(title, *e1.values(), *e2.values(), *nodes.values(), names, lossbox, losslab, arrow,
                 *w1lab.values(), *w2lab.values())
        panel_pos = [3.75, 0.4, 0]
        # forward pass
        vals = [Text("8", font_size=24).move_to(nodes["x1"]), Text("8", font_size=24).move_to(nodes["x2"])]
        cap = Text("Forward: all weights 0.1, biases 0", font_size=22, color=BLUE_C).move_to([3.75, 2.3, 0])
        self.play(FadeIn(*vals), FadeIn(cap), run_time=0.8)
        hv = [Text(f"{v:.1f}", font_size=22, color=BLUE_C).move_to(nodes[f"h{j+1}"]) for j, v in enumerate(O1)]
        f1 = MathTex(r"O_{11} = O_{12} = 0.1(8) + 0.1(8) = 1.6", font_size=28).move_to(panel_pos + UP * 0.9)
        self.play(*[e.animate.set_stroke(color=BLUE_C) for e in e1.values()], FadeIn(*hv), Write(f1), run_time=1.2)
        ov = Text(f"{y_hat:.2f}", font_size=22, color=BLUE_C).move_to(nodes["o"])
        f2 = MathTex(r"\hat y = 0.1(1.6) + 0.1(1.6) = 0.32", font_size=28).next_to(f1, DOWN, buff=0.3)
        self.play(*[e.animate.set_stroke(color=BLUE_C) for e in e2.values()], FadeIn(ov), Write(f2), run_time=1.2)
        f3 = MathTex(r"L = (4 - 0.32)^2 = 13.54", font_size=28, color=RED_C).next_to(f2, DOWN, buff=0.3)
        self.play(Write(f3), losslab.animate.set_color(RED_C), run_time=1.0)
        self.wait(0.8)
        self.snap()
        # backward pass, layer 2
        fwd = VGroup(cap, f1, f2, f3)
        cap2 = Text("Backward: chain rule, from L to each weight", font_size=22, color=RED_C).move_to([3.75, 2.3, 0])
        b1t = MathTex(r"\frac{\partial L}{\partial \hat y} = -2(y - \hat y) = -7.36", font_size=28).move_to(panel_pos + UP * 0.8)
        gy = MathTex(r"-7.36", font_size=26, color=RED_C).next_to(nodes["o"], DOWN, buff=0.15)
        self.play(FadeOut(fwd), FadeIn(cap2), Write(b1t), FadeIn(gy),
                  *[e.animate.set_stroke(color=GREY_C) for e in [*e1.values(), *e2.values()]], run_time=1.2)
        b2t = MathTex(r"\frac{\partial L}{\partial W^2_{11}} = -7.36 \times O_{11} = -11.78", font_size=28).next_to(b1t, DOWN, buff=0.3)
        b3t = MathTex(r"\frac{\partial L}{\partial b_{21}} = -7.36", font_size=28).next_to(b2t, DOWN, buff=0.3)
        g2 = {j: MathTex(f"{gW2[j-1]:.2f}", font_size=26, color=RED_C).move_to(w2lab[j]) for j in (1, 2)}
        self.play(*[e.animate.set_stroke(color=RED_C, width=5) for e in e2.values()], Write(b2t), Write(b3t),
                  *[Transform(w2lab[j], g2[j]) for j in (1, 2)], run_time=1.4)
        self.wait(0.6)
        self.snap()
        # backward pass, layer 1
        b4t = MathTex(r"\frac{\partial L}{\partial W^1_{11}} = -7.36 \times W^2_{11} \times x_{1}", font_size=28)
        b5t = MathTex(r"= -7.36 \times 0.1 \times 8 = -5.89", font_size=28)
        grp = VGroup(b4t, b5t).arrange(DOWN, buff=0.2, aligned_edge=LEFT).next_to(b3t, DOWN, buff=0.35)
        gh = [MathTex(f"{v:.3f}", font_size=24, color=RED_C).next_to(nodes[f"h{j+1}"], UP if j == 0 else DOWN, buff=0.12)
              for j, v in enumerate(gO1)]
        g1 = {k: MathTex(f"{gW1[k[0]-1, k[1]-1]:.2f}", font_size=24, color=RED_C).move_to(w1lab[k]) for k in e1}
        self.play(*[e.animate.set_stroke(color=RED_C, width=5) for e in e1.values()], FadeIn(*gh), Write(grp),
                  *[Transform(w1lab[k], g1[k]) for k in e1], run_time=1.6)
        self.wait(0.8)
        self.snap()
        # update
        old = VGroup(cap2, b1t, b2t, b3t, grp)
        cap3 = Text("Update: new = old − 0.001 × gradient", font_size=22, color=GREEN_C).move_to([3.75, 2.3, 0])
        u1 = MathTex(r"W^2_{11}: 0.1 + 0.001(11.78) = 0.1118", font_size=28).move_to(panel_pos + UP * 0.9)
        u2 = MathTex(r"W^1_{11}: 0.1 + 0.001(5.89) = 0.1059", font_size=28).next_to(u1, DOWN, buff=0.3)
        u3 = MathTex(r"\text{new } \hat y = 0.386,\ L = 13.06", font_size=28, color=GREEN_C).next_to(u2, DOWN, buff=0.3)
        nw2 = {j: MathTex(f"{0.1 - lr * gW2[j-1]:.4f}", font_size=22, color=GREEN_C).move_to(w2lab[j]) for j in (1, 2)}
        nw1 = {k: MathTex(f"{0.1 - lr * gW1[k[0]-1, k[1]-1]:.4f}", font_size=22, color=GREEN_C).move_to(w1lab[k]) for k in e1}
        self.play(FadeOut(old), FadeOut(gy), FadeOut(*gh), FadeIn(cap3), Write(u1), Write(u2),
                  *[e.animate.set_stroke(color=GREEN_C, width=3) for e in [*e1.values(), *e2.values()]],
                  *[Transform(w2lab[j], nw2[j]) for j in (1, 2)], *[Transform(w1lab[k], nw1[k]) for k in e1],
                  run_time=1.6)
        self.play(Write(u3), run_time=0.8)
        self.wait(1.5)
        self.snap()


def key_frames_grid(frames, out, gap=16):
    w, h = frames[0].size
    sheet = Image.new("RGB", (2 * w + gap, 2 * h + gap), "white")
    for i, f in enumerate(frames[:4]):
        sheet.paste(f.convert("RGB"), ((i % 2) * (w + gap), (i // 2) * (h + gap)))
    sheet.save(out)


if __name__ == "__main__":
    print("y_hat", y_hat, "L", L, "gW2", gW2, "gW1", gW1[0], "gb1", gb1)
    media = HERE / ".manim"
    with tempconfig({"quality": "medium_quality", "background_color": WHITE, "media_dir": str(media),
                     "output_file": "backprop_anim", "disable_caching": True, "verbosity": "WARNING",
                     "progress_bar": "none"}):
        scene = Backprop()
        scene.render()
    mp4 = HERE / "backprop_anim.mp4"
    shutil.copy(next(media.rglob("backprop_anim.mp4")), mp4)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(mp4), "-vf",
                    "fps=12,scale=720:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "backprop_anim.gif")], check=True)
    key_frames_grid(scene.snaps, HERE / "backprop_anim_frames.png")
    shutil.rmtree(media)

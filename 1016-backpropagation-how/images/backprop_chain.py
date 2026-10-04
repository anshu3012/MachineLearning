"""The chain rule on the 2-2-1 classification network, student 1 (CGPA 8, profile 8, placed 1), all weights 0.1,
biases 0. Values flow forward node by node; then the gradient flows backward edge by edge, each edge or node
multiplying it by its local derivative, until every weight holds its number. Intuition after 3Blue1Brown,
"Backpropagation calculus" (Neural Networks, chapter 4); network and numbers are the Note's own.
Run: python backprop_chain.py -> backprop_chain.gif, backprop_chain_frames.png"""
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
BLUE_C, ORANGE_C, GREEN_C, RED_C, PURPLE_C, GREY_C = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#B279A2", "#6B6B6B"
Text.set_default(color=BLACK, font="Latin Modern Roman")
MathTex.set_default(color=BLACK)

# the Note's numbers (Section 7.3, Notebook)
x, y = np.array([8.0, 8.0]), 1.0
W1, W2 = np.full((2, 2), 0.1), np.full(2, 0.1)
sig = lambda z: 1 / (1 + np.exp(-z))
zp = W1.T @ x                      # 1.6, 1.6
O = sig(zp)                        # 0.832
zf = W2 @ O                        # 0.166
y_hat = sig(zf)                    # 0.5415
L = -np.log(y_hat)                 # 0.613
d_zf = y_hat - y                   # -0.4585
gW2 = d_zf * O                     # -0.3815
d_O = d_zf * W2                    # -0.04585
s_slope = O * (1 - O)              # 0.140
d_zp = d_O * s_slope               # -0.00641
gW1 = np.outer(x, d_zp)            # -0.0513

P = {"x1": [-5.6, 1.8, 0], "x2": [-5.6, -1.2, 0], "h1": [-1.6, 1.8, 0], "h2": [-1.6, -1.2, 0], "o": [2.4, 0.3, 0]}
LPOS = [5.3, 0.3, 0]


class BackpropChain(Scene):
    def snap(self):
        self.snaps.append(Image.fromarray(self.renderer.get_frame()))

    def tag(self, tex, pos, color, fs=40):
        t = MathTex(tex, font_size=fs, color=color)
        bg = BackgroundRectangle(t, color=WHITE, fill_opacity=1, buff=0.06)
        return VGroup(bg, t).move_to(pos)

    def pulse(self, a, b, color, run_time=0.7):
        dot = Dot(a, radius=0.13, color=color).set_z_index(5)
        self.add(dot)
        self.play(MoveAlongPath(dot, Line(a, b)), run_time=run_time, rate_func=smooth)
        self.remove(dot)

    def construct(self):
        self.snaps = []
        nodes = {k: Circle(radius=0.62, color=GREY_C, stroke_width=4, fill_color=WHITE, fill_opacity=1).move_to(v)
                 for k, v in P.items()}
        e1 = {(i, j): Line(P[f"x{i}"], P[f"h{j}"], color=GREY_C, stroke_width=3).set_z_index(-1)
              for i in (1, 2) for j in (1, 2)}
        e2 = {j: Line(P[f"h{j}"], P["o"], color=GREY_C, stroke_width=3).set_z_index(-1) for j in (1, 2)}
        lossbox = RoundedRectangle(corner_radius=0.15, width=1.5, height=1.0, color=RED_C, stroke_width=4).move_to(LPOS)
        to_loss = Arrow(nodes["o"].get_right(), lossbox.get_left(), buff=0.05, color=GREY_C, stroke_width=4)
        names = VGroup(Text("CGPA", font_size=30).next_to(nodes["x1"], UP, buff=0.12),
                       Text("profile", font_size=30).next_to(nodes["x2"], DOWN, buff=0.12),
                       MathTex(r"\sigma", font_size=36, color=GREY_C).next_to(nodes["h1"], UP, buff=0.1),
                       MathTex(r"\sigma", font_size=36, color=GREY_C).next_to(nodes["h2"], DOWN, buff=0.1),
                       MathTex(r"\sigma", font_size=36, color=GREY_C).next_to(nodes["o"], UP, buff=0.1),
                       Text("loss", font_size=26, color=RED_C).next_to(lossbox, UP, buff=0.1))
        title = Text("Forward: every weight 0.1, student 1 is placed (y = 1)", font_size=32).to_edge(UP, buff=0.3)
        self.add(*e1.values(), *e2.values(), *nodes.values(), lossbox, to_loss, names)
        self.play(FadeIn(title), run_time=0.6)

        # ---------- forward: values flow left to right ----------
        xin = [MathTex("8", font_size=40).move_to(P[f"x{i}"]) for i in (1, 2)]
        self.play(FadeIn(*xin), run_time=0.5)
        self.play(*[e.animate.set_stroke(BLUE_C, 5) for e in e1.values()], run_time=0.6)
        zt = [MathTex(f"{zp[j]:.1f}", font_size=40, color=GREY_C).move_to(P[f"h{j+1}"]) for j in (0, 1)]
        self.play(FadeIn(*zt), run_time=0.5)
        ot = [MathTex(f"{O[j]:.3f}", font_size=36, color=BLUE_C).move_to(P[f"h{j+1}"]) for j in (0, 1)]
        self.play(*[Transform(zt[j], ot[j]) for j in (0, 1)], run_time=0.7)
        self.play(*[e.animate.set_stroke(BLUE_C, 5) for e in e2.values()], run_time=0.6)
        zft = MathTex(f"{zf:.3f}", font_size=36, color=GREY_C).move_to(P["o"])
        self.play(FadeIn(zft), run_time=0.5)
        self.play(Transform(zft, MathTex(f"{y_hat:.3f}", font_size=36, color=BLUE_C).move_to(P["o"])), run_time=0.7)
        lt = MathTex(f"{L:.3f}", font_size=34, color=RED_C).move_to(lossbox)
        self.play(GrowArrow(to_loss.copy().set_color(BLUE_C)), FadeIn(lt), run_time=0.6)
        self.wait(1.0)
        self.snap()

        # ---------- backward: one chain, edge by edge ----------
        self.play(*[e.animate.set_stroke(GREY_C, 3) for e in [*e1.values(), *e2.values()]],
                  Transform(title, Text("Backward: each step multiplies by its local derivative", font_size=32,
                                        color=RED_C).to_edge(UP, buff=0.3)), run_time=0.8)
        # running product along the bottom
        steps = [(r"\hat y - y", f"{d_zf:.4f}", r"\frac{\partial L}{\partial z_f}"),
                 (r"\times W^2_{11}", r"\times 0.1", r"\frac{\partial L}{\partial O_{11}}"),
                 (r"\times O_{11}(1-O_{11})", rf"\times {s_slope[0]:.3f}", r"\frac{\partial L}{\partial z_p}"),
                 (r"\times x_1", r"\times 8", r"\frac{\partial L}{\partial W^1_{11}}")]
        sym = VGroup(*[MathTex(s[0], font_size=32, color=GREY_C) for s in steps])
        num = VGroup(*[MathTex(s[1], font_size=44, color=RED_C) for s in steps])
        for k in range(4):
            num[k].move_to([-5.8 + 2.7 * k, -3.3, 0])
            sym[k].next_to(num[k], UP, buff=0.12)
        running = None

        def show_running(k, value):
            nonlocal running
            if k == 0:
                return [FadeIn(sym[k], shift=UP * 0.1), FadeIn(num[k], shift=UP * 0.1)]
            new = MathTex(rf"= {value:.4f}", font_size=44, color=RED_C).move_to([4.9, -3.3, 0])
            anims = [FadeIn(sym[k], shift=UP * 0.1), FadeIn(num[k], shift=UP * 0.1)]
            anims.append(Transform(running, new) if running is not None else FadeIn(new))
            if running is None:
                running = new
            return anims

        # step 1: loss and output sigmoid together give y_hat - y
        self.pulse(lossbox.get_left(), P["o"], RED_C)
        gzf = self.tag(rf"{d_zf:.4f}", [P["o"][0], -0.8, 0], RED_C)
        self.play(FadeIn(gzf), *show_running(0, d_zf), run_time=0.8)
        self.wait(0.4)
        # output weights: times O_11
        g2 = {j: self.tag(f"{gW2[j-1]:.3f}", e2[j].point_from_proportion(0.5) + (UP if j == 1 else DOWN) * 0.45, RED_C)
              for j in (1, 2)}
        self.play(*[e.animate.set_stroke(RED_C, 6) for e in e2.values()], FadeIn(g2[1]), FadeIn(g2[2]), run_time=0.9)
        side = MathTex(rf"\frac{{\partial L}}{{\partial W^2_{{11}}}} = {d_zf:.4f} \times {O[0]:.3f}",
                       font_size=34, color=RED_C).move_to([4.0, 2.1, 0])
        self.play(Write(side), run_time=0.8)
        self.wait(0.8)
        self.snap()
        self.play(FadeOut(side), run_time=0.4)

        # step 2: back along W2_11 into hidden node 1
        self.pulse(P["o"], P["h1"], RED_C)
        gO = self.tag(rf"{d_O[0]:.5f}", [P["h1"][0], 3.05, 0], RED_C, fs=36)
        self.play(*show_running(1, d_O[0]), FadeIn(gO), Indicate(nodes["h1"], color=RED_C), run_time=0.9)
        self.wait(0.4)
        # step 3: through the hidden sigmoid
        gzp = self.tag(rf"{d_zp[0]:.5f}", [P["h1"][0], 3.05, 0], RED_C, fs=36)
        self.play(*show_running(2, d_zp[0]), Transform(gO, gzp), Flash(nodes["h1"], color=RED_C), run_time=0.9)
        self.wait(0.4)
        # step 4: back along x1 -> h1, times the input 8
        self.pulse(P["h1"], P["x1"], RED_C)
        g11 = self.tag(f"{gW1[0, 0]:.4f}", e1[(1, 1)].point_from_proportion(0.5) + UP * 0.35, RED_C)
        self.play(*show_running(3, gW1[0, 0]), e1[(1, 1)].animate.set_stroke(RED_C, 6), FadeIn(g11), run_time=0.9)
        self.wait(1.2)
        self.snap()

        # every other first-layer weight: the same chain, other factors
        pos = {(2, 1): 0.3, (1, 2): 0.3, (2, 2): 0.5}
        shift = {(2, 1): RIGHT * 0.75, (1, 2): RIGHT * 0.75, (2, 2): DOWN * 0.4}
        rest = [self.tag(f"{gW1[k[0]-1, k[1]-1]:.4f}", e1[k].point_from_proportion(pos[k]) + shift[k], RED_C, fs=36)
                for k in pos]
        self.play(*[e1[k].animate.set_stroke(RED_C, 6) for k in pos], *[FadeIn(r) for r in rest], run_time=1.0)
        end = Text("Every weight has its gradient. Hidden ones are 7 times smaller:",
                   font_size=30, color=GREY_C).move_to([0, -3.0, 0])
        end2 = Text("× 0.1 and × 0.14 shrank them on the way back", font_size=30, color=GREY_C).next_to(end, DOWN, buff=0.12)
        self.play(FadeOut(sym), FadeOut(num), FadeOut(running), FadeIn(end), FadeIn(end2), run_time=0.8)
        self.wait(2.0)
        self.snap()


def key_frames_grid(frames, out, gap=16):
    w, h = frames[0].size
    rows = (len(frames) + 1) // 2
    sheet = Image.new("RGB", (2 * w + gap, rows * h + (rows - 1) * gap), "white")
    for i, f in enumerate(frames):
        sheet.paste(f.convert("RGB"), ((i % 2) * (w + gap), (i // 2) * (h + gap)))
    sheet.save(out)


if __name__ == "__main__":
    assert abs(y_hat - 0.5415) < 1e-4 and abs(gW2[0] + 0.3815) < 1e-4 and abs(gW1[0, 0] + 0.0513) < 1e-4
    media = HERE / ".manim"
    with tempconfig({"quality": "medium_quality", "background_color": WHITE, "media_dir": str(media),
                     "output_file": "backprop_chain", "disable_caching": True, "verbosity": "WARNING",
                     "progress_bar": "none"}):
        scene = BackpropChain()
        scene.render()
    mp4 = next(media.rglob("backprop_chain.mp4"))
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(mp4), "-vf",
                    "fps=12,scale=720:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "backprop_chain.gif")], check=True)
    key_frames_grid(scene.snaps, HERE / "backprop_chain_frames.png")
    shutil.rmtree(media)

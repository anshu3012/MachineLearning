"""BPTT on the one-node worked example (w_i = 0.5, w_h = 0.8, w_o = 1, x = (1, 0, 1), y = 1).
The error at the output travels back through h_3, h_2, h_1. At each step it is multiplied by the tanh slope,
drops one term into dL/dw_i and one into dL/dw_h, then is multiplied by w_h to reach the step before: it shrinks.
Numbers recomputed here and checked against data/worked_example.csv (written by the Notebook).
Run: python bptt_pulse.py  -> bptt_pulse.mp4, bptt_pulse.gif, bptt_pulse_frames.png"""
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
BLUE_C, ORANGE_C, GREEN_C, RED_C, PURPLE_C, GREY_C = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#B279A2", "#6B6B6B"
Text.set_default(color=BLACK, font="Latin Modern Roman")
MarkupText.set_default(color=BLACK, font="Latin Modern Roman")

# forward and backward pass, one node
w_i, w_h, w_o, xs, y = 0.5, 0.8, 1.0, [1.0, 0.0, 1.0], 1.0
h = [0.0]
for x in xs:
    h.append(np.tanh(w_i * x + w_h * h[-1]))
y_hat = 1 / (1 + np.exp(-w_o * h[3]))
delta = {3: (y_hat - y) * w_o}                      # dL/dh_3
a, term_i, term_h = {}, {}, {}
for t in (3, 2, 1):
    a[t] = delta[t] * (1 - h[t] ** 2)               # through tanh at step t
    term_i[t], term_h[t] = a[t] * xs[t - 1], a[t] * h[t - 1]
    delta[t - 1] = a[t] * w_h                       # error reaching the step before
ref = pd.read_csv(HERE.parent / "data" / "worked_example.csv").set_index("quantity")["value"]
for t in (1, 2, 3):
    assert abs(term_i[t] - ref[f"dL/dw_i term t={t}"]) < 1e-5 and abs(term_h[t] - ref[f"dL/dw_h term t={t}"]) < 1e-5
assert abs(sum(term_i.values()) - ref["dL/dw_i"]) < 1e-5 and abs(sum(term_h.values()) - ref["dL/dw_h"]) < 1e-5

XS = {1: -5.6, 2: -2.4, 3: 0.8}                     # x of each time step
Y_BOX = 0.25


def num(v):
    if abs(v) < 5e-7:
        return "0"
    return f"{v:.3f}".replace("-", "−")


def box(t):
    r = RoundedRectangle(corner_radius=0.15, width=2.3, height=1.05, stroke_color=PURPLE_C, stroke_width=3,
                         fill_color=ManimColor(PURPLE_C).interpolate(WHITE, 0.85), fill_opacity=1)
    lab = MarkupText(f"h<sub>{t}</sub> = {h[t]:.2f}", font_size=36).move_to(r)
    return VGroup(r, lab).move_to([XS[t], Y_BOX, 0])


def pulse(v, at):
    """Orange disc whose size and strength show the size of the error."""
    s = abs(v) / abs(delta[3])
    d = Circle(radius=0.15 + 0.4 * s, stroke_width=0, fill_color=ORANGE_C, fill_opacity=0.3 + 0.65 * s).move_to(at)
    return VGroup(d, Text(num(v), font_size=38, weight=BOLD, color=ORANGE_C).next_to(d, RIGHT, buff=0.12))


class BPTTPulse(Scene):
    def snap(self):
        self.snaps.append(Image.fromarray(self.renderer.get_frame()))

    def construct(self):
        self.snaps = []
        title = Text("Forward through time", font_size=40).to_edge(UP, buff=0.3)
        self.play(FadeIn(title))
        boxes, inputs = {}, {}
        for t in (1, 2, 3):
            boxes[t] = box(t)
            inputs[t] = MarkupText(f"x<sub>{t}</sub> = {xs[t - 1]:.0f}", font_size=34, color=BLUE_C
                                   ).move_to([XS[t], -1.3, 0])
            up = Arrow(inputs[t].get_top(), boxes[t].get_bottom(), buff=0.08, color=BLUE_C, stroke_width=4)
            anims = [FadeIn(boxes[t]), FadeIn(inputs[t]), GrowArrow(up)]
            if t > 1:
                rec = Arrow(boxes[t - 1].get_right(), boxes[t].get_left(), buff=0.08, color=PURPLE_C, stroke_width=4)
                anims.append(GrowArrow(rec))
                anims.append(FadeIn(MarkupText("w<sub>h</sub> = 0.8", font_size=28, color=PURPLE_C
                                               ).next_to(rec, UP, buff=0.6)))
            self.play(*anims, run_time=0.7)
        out = VGroup(MarkupText(f"ŷ = {y_hat:.2f}", font_size=36, color=GREEN_C),
                     Text("target y = 1", font_size=28, color=GREY_C)).arrange(DOWN, buff=0.12).move_to([3.95, Y_BOX, 0])
        self.play(GrowArrow(Arrow(boxes[3].get_right(), out.get_left(), buff=0.1, color=GREEN_C, stroke_width=4)),
                  FadeIn(out), run_time=0.7)
        self.wait(0.6)
        self.snap()

        # backward
        self.play(Transform(title, Text("Backward through time: the error travels left", font_size=40
                                        ).to_edge(UP, buff=0.3)))
        head_i = MarkupText("∂L/∂w<sub>i</sub>", font_size=34, color=BLUE_C).move_to([2.55, -2.3, 0], aligned_edge=LEFT)
        head_h = MarkupText("∂L/∂w<sub>h</sub>", font_size=34, color=PURPLE_C).move_to([2.55, -3.1, 0], aligned_edge=LEFT)
        self.play(FadeIn(head_i), FadeIn(head_h), run_time=0.5)
        p = pulse(delta[3], out.get_center() + DOWN * 1.15)
        self.play(FadeIn(p, scale=1.4), run_time=0.6)
        for t in (3, 2, 1):
            above = boxes[t].get_top() + UP * 1.0
            self.play(p.animate.shift(above - p[0].get_center()), run_time=0.9)
            slope = MarkupText(f"× tanh slope {1 - h[t] ** 2:.2f}", font_size=32, color=GREY_C
                               ).move_to(above + UP * 0.8)
            self.play(FadeIn(slope), Transform(p, pulse(a[t], above)), run_time=0.8)
            ti = MarkupText(f"× x<sub>{t}</sub> → {num(term_i[t])}", font_size=30, color=BLUE_C).move_to([XS[t], -2.3, 0])
            th = MarkupText(f"× h<sub>{t - 1}</sub> → {num(term_h[t])}", font_size=30, color=PURPLE_C
                            ).move_to([XS[t], -3.1, 0])
            self.play(TransformFromCopy(p[1], ti), TransformFromCopy(p[1], th), run_time=0.9)
            self.play(FadeOut(slope), run_time=0.3)
            if t > 1:
                nxt = boxes[t - 1].get_top() + UP * 1.0
                lab = MarkupText("× w<sub>h</sub>", font_size=32, color=PURPLE_C).move_to((above + nxt) / 2 + UP * 0.8)
                self.play(FadeIn(lab), p.animate.shift((above + nxt) / 2 - p[0].get_center()), run_time=0.5)
                self.play(Transform(p, pulse(delta[t - 1], (above + nxt) / 2)), run_time=0.6)
                self.play(FadeOut(lab), run_time=0.2)
            self.wait(0.4)
            if t in (3, 2):
                self.snap()
        tot_i = MarkupText(f"= {num(sum(term_i.values()))}", font_size=34, color=BLUE_C, weight=BOLD
                           ).next_to(head_i, RIGHT, buff=0.15)
        tot_h = MarkupText(f"= {num(sum(term_h.values()))}", font_size=34, color=PURPLE_C, weight=BOLD
                           ).next_to(head_h, RIGHT, buff=0.15)
        self.play(FadeIn(tot_i, shift=LEFT * 0.3), FadeIn(tot_h, shift=LEFT * 0.3), run_time=0.8)
        note = MarkupText(f"error reaching h<sub>3</sub>, h<sub>2</sub>, h<sub>1</sub>: "
                          f"{abs(delta[3]):.2f} → {abs(delta[2]):.2f} → {abs(delta[1]):.2f}",
                          font_size=38, color=ORANGE_C).to_edge(UP, buff=0.3)
        self.play(Transform(title, note), run_time=0.8)
        self.wait(2.0)
        self.snap()


def key_frames_grid(frames, out, gap=16):
    w, hh = frames[0].size
    sheet = Image.new("RGB", (2 * w + gap, 2 * hh + gap), "white")
    for i, f in enumerate(frames[:4]):
        sheet.paste(f.convert("RGB"), ((i % 2) * (w + gap), (i // 2) * (hh + gap)))
    sheet.save(out)


if __name__ == "__main__":
    media = HERE / ".manim"
    with tempconfig({"quality": "medium_quality", "background_color": WHITE, "media_dir": str(media),
                     "output_file": "bptt_pulse", "disable_caching": True, "verbosity": "WARNING",
                     "progress_bar": "none"}):
        scene = BPTTPulse()
        scene.render()
    mp4 = HERE / "bptt_pulse.mp4"
    shutil.copy(next(media.rglob("bptt_pulse.mp4")), mp4)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(mp4), "-vf",
                    "fps=12,scale=720:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "bptt_pulse.gif")], check=True)
    key_frames_grid(scene.snaps, HERE / "bptt_pulse_frames.png")
    shutil.rmtree(media)

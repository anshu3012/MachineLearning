"""Toy MLP neuron as an AND gate (idea after Sanderson 2024, Ch 7; numbers ours): 5 perpendicular directions
(Michael, Jordan, Phelps, Alexis, basketball). The neuron's W_up row is Michael + Jordan, its bias -1, then ReLU;
its W_down column is the basketball direction, added to the input vector. Inputs in turn: Michael Jordan,
Michael Phelps, Alexis Jordan, Phelps. Data: data/toy_and_gate.csv (Notebook).
Run: python and_gate.py -> and_gate.gif, and_gate_frames.png (Manim CE)"""
from pathlib import Path

import numpy as np
import pandas as pd
from manim import *
from PIL import Image

from common import BLUE as B, GREY as GR, ORANGE as O, GREEN as G, RED as R, DATA, render_manim

HERE = Path(__file__).parent
Text.set_default(color=BLACK, font="Latin Modern Roman")
MathTex.set_default(color=BLACK)
toy = pd.read_csv(DATA / "toy_and_gate.csv").set_index("input")
NAMES = ["Michael", "Jordan", "Phelps", "Alexis", "basketball"]
VEC = {"Michael Jordan": [1, 1, 0, 0, 0], "Michael Phelps": [1, 0, 1, 0, 0], "Alexis Jordan": [0, 1, 0, 1, 0],
       "Phelps": [0, 0, 1, 0, 0]}
YS = [1.2 - 0.62 * i for i in range(5)]
fmt = lambda v: f"{v:g}"


def column(vals, x, color, highlight=None):
    g = VGroup()
    for i, (v, y) in enumerate(zip(vals, YS)):
        c = color if v != 0 else GR
        box = Square(0.55, stroke_color=c, stroke_width=3, fill_color=c, fill_opacity=0.15 if v != 0 else 0.03).move_to([x, y, 0])
        if highlight is not None and i == highlight:
            box.set_stroke(O, 5)
        g.add(VGroup(box, Text(fmt(v), font_size=24, color=c if v != 0 else GR).move_to(box)))
    return g


class AndGate(Scene):
    def snap(self):
        self.snaps.append(Image.fromarray(self.renderer.get_frame()))

    def construct(self):
        self.snaps = []
        title = Text("One MLP neuron as an AND gate (toy)", font_size=32, weight=BOLD).to_edge(UP, buff=0.2)
        labels = VGroup(*[Text(n, font_size=20, color=GR).move_to([-5.15, y, 0], aligned_edge=RIGHT) for n, y in zip(NAMES, YS)])
        row = VGroup(*[VGroup(Square(0.5, stroke_color=B if v else GR, fill_color=B, fill_opacity=0.15 if v else 0.02),
                              Text(str(v), font_size=22, color=B if v else GR)) for v in (1, 1, 0, 0, 0)])
        for k, r in enumerate(row):
            r[1].move_to(r[0])
        row.arrange(RIGHT, buff=0.05).move_to([-1.9, 2.55, 0])
        rowlab = Text("row of W_up = Michael + Jordan", font_size=20, color=B).next_to(row, DOWN, buff=0.12)
        colW = column([0, 0, 0, 0, 1], 2.4, B)
        collab = Text("column of W_down\n= basketball", font_size=20, color=B).next_to(colW, UP, buff=0.15)
        ax = Axes(x_range=[-2, 2, 1], y_range=[-0.5, 2, 1], x_length=2.6, y_length=1.6, tips=False,
                  axis_config=dict(color=GR, stroke_width=2)).move_to([-1.9, -1.55, 0])
        relu = ax.plot(lambda t: max(t, 0), color=B, stroke_width=4, use_smoothing=False)
        relulab = Text("ReLU", font_size=20, color=B).next_to(ax, LEFT, buff=0.1)
        self.add(title, labels, row, rowlab, colW, collab, ax, relu, relulab)
        e_lab = Text("input e", font_size=22).move_to([-4.7, 1.75, 0])
        o_lab = Text("e + added", font_size=22).move_to([5.3, 1.75, 0])
        self.add(e_lab, o_lab)
        state = VGroup()
        for k, (name, vec) in enumerate(VEC.items()):
            r = toy.loc[name]
            e = column(vec, -4.7, GR)
            head = Text(f'input: "{name}"', font_size=26, color=BLACK).move_to([0.2, -3.45, 0])
            self.play(FadeOut(state), FadeIn(e), FadeIn(head), run_time=0.7)
            dot = MathTex(rf"\text{{row}}\cdot e = {fmt(r.row_dot_e)}", font_size=34).move_to([-1.9, 1.15, 0])
            self.play(Indicate(row, color=B, scale_factor=1.05), FadeIn(dot), run_time=0.9)
            pre = MathTex(rf"+\,\text{{bias}}\,(-1) = {fmt(r.plus_bias)}", font_size=34).move_to([-1.9, 0.45, 0])
            self.play(FadeIn(pre), run_time=0.6)
            pt = Dot(ax.c2p(r.plus_bias, r.after_relu), color=O, radius=0.09)
            neuron = VGroup(Circle(0.5, color=O if r.after_relu > 0 else GR, fill_opacity=0.15, stroke_width=4),
                            Text(fmt(r.after_relu), font_size=30, color=O if r.after_relu > 0 else GR)).move_to([0.55, -0.4, 0])
            nlab = Text("neuron", font_size=18, color=GR).next_to(neuron, DOWN, buff=0.08)
            self.play(FadeIn(pt), FadeIn(neuron), FadeIn(nlab), run_time=0.7)
            out = column(np.array(vec) + r.after_relu * np.array([0, 0, 0, 0, 1]), 5.3, GR,
                         highlight=4 if r.after_relu > 0 else None)
            arrow = Arrow([0.95, -0.4, 0], [1.95, -0.4, 0], color=O if r.after_relu > 0 else GR, buff=0.05)
            times = MathTex(rf"{fmt(r.after_relu)}\times", font_size=30).next_to(colW, LEFT, buff=0.1).shift(DOWN * 1.6)
            plus = MathTex(r"\Rightarrow", font_size=40, color=GR).move_to([3.85, -0.4, 0])
            self.play(GrowArrow(arrow), FadeIn(times), FadeIn(plus), FadeIn(out), run_time=1.0)
            if r.after_relu > 0:
                note = Text("both names present: the neuron fires and writes basketball", font_size=22, color=O)
            elif r.plus_bias < 0:
                note = Text(f"without ReLU it would write {fmt(r.plus_bias)} × basketball; ReLU clips it to 0", font_size=22, color=R)
            else:
                note = Text("only one name: 1 - 1 = 0, so nothing is written", font_size=22, color=GR)
            note.move_to([0.2, -2.95, 0])
            self.play(FadeIn(note), run_time=0.5)
            self.wait(2.2)
            if k in (0, 1, 3):
                self.snap()
            state = VGroup(e, head, dot, pre, pt, neuron, nlab, out, arrow, times, plus, note)
        final = Text("Rows ask, ReLU decides AND, columns write.", font_size=28, color=B, weight=BOLD).move_to([0.2, -2.95, 0])
        self.play(FadeOut(state[-1]), FadeIn(final))
        self.wait(2.5)
        self.snap()


if __name__ == "__main__":
    render_manim(AndGate, "and_gate", HERE)

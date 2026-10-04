"""Softmax temperature on GPT-2 small's real next-token logits for "Once upon a time there was a": the 10 most
likely tokens plus one bar for all the other 50,247, as T moves 1 -> 0.3 -> 0.05 -> 1.5 -> 3. Under the bars, a
real 12-token continuation sampled at that temperature. Idea after Sanderson (2024, Ch 5); data and code ours.
Data: data/story_logits.npy (all 50,257 logits), data/samples.csv (Notebook).
Run: python temperature.py -> temperature.gif, temperature_frames.png (Manim CE)"""
from pathlib import Path

import numpy as np
import pandas as pd
from manim import *
from PIL import Image

from common import GREY as GR, ORANGE as O, BLUE as B, DATA, render_manim

HERE = Path(__file__).parent
Text.set_default(color=BLACK, font="Latin Modern Roman")
MathTex.set_default(color=BLACK)
z = np.load(DATA / "story_logits.npy").astype(np.float64)
order = np.argsort(-z)[:10]
names = pd.read_csv(DATA / "story_top10.csv").token.str.strip().tolist()
samples = pd.read_csv(DATA / "samples.csv")
SAMPLE = {T: samples[samples["T"] == T].text.iloc[0] for T in (0.0, 0.3, 1.0, 1.5)}
SCALE, X0, ROWS = 7.5, -3.2, 11


def probs(T):
    q = np.exp((z - z.max()) / T)
    q /= q.sum()
    top = q[order]
    return np.append(top, 1 - top.sum())


class Temperature(Scene):
    def snap(self):
        self.snaps.append(Image.fromarray(self.renderer.get_frame()))

    def construct(self):
        self.snaps = []
        T = ValueTracker(1.0)
        title = Text("Temperature reshapes the next-token distribution", font_size=32, weight=BOLD).to_edge(UP, buff=0.2)
        prompt = Text('GPT-2 small, after "Once upon a time there was a ..."', font_size=22, color=GR).next_to(title, DOWN, buff=0.12)
        ys = [2.0 - 0.42 * i for i in range(ROWS)]
        labels = VGroup(*[Text(n, font_size=22).move_to([X0 - 0.2, y, 0], aligned_edge=RIGHT) for n, y in zip(names, ys)])
        labels.add(Text("all other 50,247", font_size=22, color=O).move_to([X0 - 0.2, ys[-1], 0], aligned_edge=RIGHT))
        formula = MathTex(r"p_k = \frac{e^{z_k/T}}{\sum_j e^{z_j/T}}", font_size=36).move_to([4.9, 1.6, 0])

        def bars():
            p = probs(T.get_value())
            g = VGroup()
            for i, (pi, y) in enumerate(zip(p, ys)):
                w = max(pi * SCALE, 0.02)
                g.add(Rectangle(width=w, height=0.3, stroke_width=0, fill_color=O if i == ROWS - 1 else GR,
                                fill_opacity=0.85).move_to([X0 + w / 2, y, 0]))
                g.add(Text(f"{pi:.2f}", font_size=18, color=GR).move_to([X0 + w + 0.35, y, 0]))
            return g

        def readout():
            t = T.get_value()
            q = np.exp((z - z.max()) / t); q /= q.sum()
            n = 2 ** -(q[q > 0] * np.log2(q[q > 0])).sum()        # 2^entropy: "like a fair choice among n tokens"
            return VGroup(MathTex(rf"T = {t:.2f}", font_size=48, color=B),
                          Text(f"as spread as a fair pick\namong {n:,.0f} tokens", font_size=20, color=GR)
                          ).arrange(DOWN, buff=0.2).move_to([4.9, -0.1, 0])

        self.add(title, prompt, labels, formula)
        bar_group, ro = always_redraw(bars), always_redraw(readout)
        self.add(bar_group, ro)
        note = Text("", font_size=22)

        def caption(s, sample_T=None, color=GR):
            nonlocal note
            parts = [Text(s, font_size=24, color=color)]
            if sample_T is not None:
                txt = SAMPLE[sample_T].replace("\n", " ")
                parts.append(Text(f"sample at T = {sample_T:g}:  ...a{txt}", font_size=20, color=BLACK))
            new = VGroup(*parts).arrange(DOWN, buff=0.15, aligned_edge=LEFT).move_to([0, -3.35, 0])
            self.play(FadeOut(note), FadeIn(new), run_time=0.5)
            note = new

        caption("T = 1: the model's own probabilities. Most of the mass is outside the top 10", 1.0)
        self.wait(2.5)
        self.snap()
        self.play(T.animate.set_value(0.3), run_time=3)
        caption("Lower T: the likely tokens take over", 0.3)
        self.wait(2)
        self.play(T.animate.set_value(0.03), run_time=2.5)
        caption("T near 0: the top token takes almost everything (greedy)", 0.0)
        self.wait(2.5)
        self.snap()
        self.play(T.animate.set_value(1.5), run_time=3.5)
        caption("Higher T: rare tokens get picked, and the text falls apart", 1.5, color=O)
        self.wait(2.5)
        self.snap()
        self.play(T.animate.set_value(3.0), run_time=2.5)
        caption("T = 3: almost uniform over all 50,257 tokens", None, color=O)
        self.wait(2.5)
        self.snap()


if __name__ == "__main__":
    render_manim(Temperature, "temperature", HERE)

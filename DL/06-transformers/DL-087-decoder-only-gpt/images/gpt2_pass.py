"""One pass of GPT-2 small on "Steve Jobs was the founder of": look up each token's row of W_E (drawn upright) (+ position),
12 blocks of masked attention (columns read only to their left) and MLP (each column alone), then a guess for
the next token at EVERY position; the last guess is appended and the pass runs again.
Numbers: data/every_position.csv and data/greedy_steps.csv from the Notebook (real GPT-2 small weights).
Run: python gpt2_pass.py -> gpt2_pass.gif, gpt2_pass_frames.png (Manim CE)"""
from pathlib import Path

import numpy as np
import pandas as pd
from manim import *
from PIL import Image

from common import BLUE as B, GREEN as G, GREY as GR, ORANGE as O, DATA, render_manim

HERE = Path(__file__).parent
Text.set_default(color=BLACK, font="Latin Modern Roman")
ev = pd.read_csv(DATA / "every_position.csv", keep_default_na=False)
N = len(ev)
XS = np.linspace(-4.4, 4.0, N)
show = lambda t: t.strip() if t.strip() else repr(t)     # tokens carry a leading space; draw the word


class GPTPass(Scene):
    def snap(self):
        self.snaps.append(Image.fromarray(self.renderer.get_frame()))

    def column(self, x, y, h=0.9, color=GR):
        bars = VGroup(*[Rectangle(width=0.34, height=h / 6, stroke_width=1, stroke_color=WHITE, fill_color=color,
                                  fill_opacity=0.35 + 0.1 * (k % 3)) for k in range(6)]).arrange(DOWN, buff=0)
        return bars.move_to([x, y, 0])

    def construct(self):
        self.snaps = []
        title = Text("GPT-2 small: one pass, a guess at every position", font_size=32, weight=BOLD).to_edge(UP, buff=0.2)
        sub = Text("", font_size=24)
        def say(s, color=GR):
            new = Text(s, font_size=24, color=color).next_to(title, DOWN, buff=0.15)
            self.play(FadeOut(sub), FadeIn(new), run_time=0.5)
            return new
        toks = VGroup(*[Text(show(t), font_size=26).move_to([x, -3.25, 0]) for t, x in zip(ev.token, XS)])
        self.add(title)
        sub = say("1. The text is split into tokens")
        self.play(LaggedStart(*[FadeIn(t, shift=UP * 0.2) for t in toks], lag_ratio=0.15), run_time=1.5)
        # embedding lookup
        WE = VGroup(Rectangle(width=0.9, height=1.5, color=B, fill_color=B, fill_opacity=0.25),
                    MathTex(r"W_E", color=B, font_size=34)).move_to([-6.3, -2.1, 0])
        WE[1].move_to(WE[0])
        WP = MathTex(r"+\,W_P", color=B, font_size=28).next_to(WE, DOWN, buff=0.1)
        sub = say("2. Each token takes its row of the embedding matrix (drawn upright), plus a position vector")
        self.play(FadeIn(WE), FadeIn(WP))
        cols = VGroup(*[self.column(x, -2.05) for x in XS])
        for c in cols:
            sl = Rectangle(width=0.12, height=1.5, color=B, fill_color=B, fill_opacity=0.8).move_to(WE[0])
            self.play(ReplacementTransform(sl, c), run_time=0.35)
        self.wait(0.4)
        self.snap()
        # the 12 blocks
        block = RoundedRectangle(corner_radius=0.2, width=9.6, height=1.95, color=B, stroke_width=3).move_to([(XS[0] + XS[-1]) / 2, -0.35, 0])
        blab = Text("12 blocks", font_size=24, color=B).next_to(block, LEFT, buff=0.15)
        sub = say("3. Masked attention: each column reads only the columns to its left")
        self.play(Create(block), FadeIn(blab))
        arcs = VGroup(*[CurvedArrow([XS[i], -1.1, 0], [XS[j] - 0.05, -1.1, 0], angle=-min(PI / 2, 1.6 / np.sqrt(j - i)), color=GR,
                                    stroke_width=2, tip_length=0.15) for j in range(1, N) for i in range(j)])
        self.play(LaggedStart(*[Create(a) for a in arcs], lag_ratio=0.05), run_time=2.5)
        self.wait(0.6)
        self.snap()
        sub = say("4. MLP: every column alone, same weights. Both results are added to the column")
        mlps = VGroup(*[Square(0.62, color=B, fill_color=B, fill_opacity=0.25).move_to([x, -0.85, 0]) for x in XS])
        mtxt = Text("MLP", font_size=15, color=B)
        self.play(FadeOut(arcs), LaggedStart(*[FadeIn(m) for m in mlps], lag_ratio=0.1), run_time=1.2)
        self.play(*[FadeIn(mtxt.copy().move_to(m)) for m in mlps], run_time=0.5)
        counter = Text("block 1 of 12", font_size=20, color=B).move_to(block.get_corner(UL) + np.array([1.0, -0.3, 0]))
        self.play(FadeIn(counter), run_time=0.3)
        for k in range(2, 13):
            self.play(Transform(counter, Text(f"block {k} of 12", font_size=22, color=B).move_to(counter)), run_time=0.12)
        up = VGroup(*[self.column(x, 1.25, h=0.7) for x in XS])
        self.play(*[TransformFromCopy(c, u) for c, u in zip(cols, up)], run_time=1.2)
        # guesses
        sub = say("5. Each column, times W_E again (tied), gives the next-token guess")
        guesses, actual = VGroup(), VGroup()
        for i, r in ev.iterrows():
            ok = r.next_actual != "" and r.top1 == r.next_actual
            col = G if ok else (O if r.next_actual == "" else BLACK)
            guesses.add(Text(f"{show(r.top1)} {r.p1:.2f}", font_size=22, color=col, weight=BOLD if r.next_actual == "" else NORMAL)
                        .move_to([XS[i], 2.4, 0]))
            if r.next_actual != "":
                actual.add(Text(f"{show(r.next_actual)} {float(r.p_actual):.2f}" if float(r.p_actual) >= 0.01 else f"{show(r.next_actual)} <0.01", font_size=19, color=GR).move_to([XS[i], 1.95, 0]))
        self.play(LaggedStart(*[FadeIn(gu, shift=UP * 0.2) for gu in guesses], lag_ratio=0.2), run_time=2)
        heads = VGroup(Text("top guess:", font_size=19, color=GR).move_to([XS[0] - 1.45, 2.4, 0]),
                       Text("true next:", font_size=19, color=GR).move_to([XS[0] - 1.45, 1.95, 0]))
        self.play(FadeIn(actual), FadeIn(heads), run_time=0.8)
        self.wait(1.2)
        sub = say("Training: raise the probability of every true next token at once", GR)
        self.wait(1.5)
        self.snap()
        # generation
        sub = say("6. Generating: keep the last guess, append it, run the pass again", O)
        new = Text(show(ev.top1.iloc[-1]), font_size=26, color=O).move_to(guesses[-1])
        self.play(new.animate.move_to([XS[-1] + 1.6, -3.25, 0]), run_time=1.5)
        loop = CurvedArrow([XS[-1] + 1.6, -2.9, 0], [XS[-1] + 0.5, 2.2, 0], angle=PI / 2.2, color=O, stroke_width=3)
        self.play(Create(loop), run_time=0.8)
        steps = pd.read_csv(DATA / "greedy_steps.csv")
        tail = Text("next passes add:  " + "   ".join(f"'{show(t)}'" for t in steps.top1.iloc[1:]) + "   ...", font_size=22,
                    color=O).move_to([0.0, -3.85, 0])
        self.play(FadeIn(tail))
        self.wait(2.5)
        self.snap()


if __name__ == "__main__":
    render_manim(GPTPass, "gpt2_pass", HERE)

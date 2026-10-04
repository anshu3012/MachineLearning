"""From outcomes to a PMF: the 8 outcomes of 3 fair coin flips are grouped by X = number of heads,
and each group collapses into a bar of height count / 8.
Run: python coin_pmf.py -> coin_pmf.mp4, .gif, _frames.png (Manim; render on topgro)"""
import itertools
import shutil
import subprocess
from pathlib import Path

from manim import *
from PIL import Image

HERE = Path(__file__).parent
BLUE_C, ORANGE_C, GREY_C = "#4C78A8", "#F58518", "#6B6B6B"
Text.set_default(color=BLACK, font="Latin Modern Roman")
MathTex.set_default(color=BLACK)
OUTCOMES = ["".join(t) for t in itertools.product("HT", repeat=3)]   # HHH, HHT, ..., TTT
COUNTS = [sum(o.count("H") == k for o in OUTCOMES) for k in range(4)]
assert COUNTS == [1, 3, 3, 1] and sum(COUNTS) == 8


class CoinPMF(Scene):
    def snap(self):
        self.snaps.append(Image.fromarray(self.renderer.get_frame()))

    def caption(self, title, detail):
        return VGroup(Text(title, font_size=34, weight=BOLD), Text(detail, font_size=26, color=GREY_C)
                      ).arrange(DOWN, buff=0.15).to_edge(UP, buff=0.25)

    def tile(self, o):
        letters = VGroup(*[Text(c, font_size=30, weight=BOLD, color=ORANGE_C if c == "H" else GREY_C) for c in o]
                         ).arrange(RIGHT, buff=0.08)
        box = RoundedRectangle(corner_radius=0.1, width=1.25, height=0.6, stroke_color=GREY_C, stroke_width=2)
        return VGroup(box, letters.move_to(box))

    def construct(self):
        self.snaps = []
        tiles = VGroup(*[self.tile(o) for o in OUTCOMES]).arrange(RIGHT, buff=0.22).shift(UP * 1.6)
        cap = self.caption("Flip a fair coin 3 times", "8 equally likely outcomes, each with probability 1/8")
        self.play(FadeIn(cap), LaggedStart(*[FadeIn(t, shift=DOWN * 0.3) for t in tiles], lag_ratio=0.12))
        self.wait(0.8)
        self.snap()
        heads = VGroup(*[MathTex(f"X={o.count('H')}", font_size=30, color=BLUE_C).next_to(t, DOWN, buff=0.15)
                         for o, t in zip(OUTCOMES, tiles)])
        self.play(Transform(cap, self.caption("X = number of heads", "write X under each outcome")),
                  LaggedStart(*[FadeIn(h) for h in heads], lag_ratio=0.1))
        self.wait(1)
        self.snap()

        ax = Axes(x_range=[0, 4.4, 1], y_range=[0, 0.5, 0.125], x_length=8, y_length=3.8,
                  axis_config={"color": GREY_C, "include_tip": False}, x_axis_config={"include_ticks": False},
                  ).shift(DOWN * 0.75 + RIGHT * 0.6)
        ticks = VGroup(*[MathTex(str(k), font_size=32, color=GREY_C).next_to(ax.c2p(k + 0.7, 0), DOWN, buff=0.2)
                         for k in range(4)])
        yticks = VGroup(*[MathTex(f"{j}/8", font_size=32, color=GREY_C).next_to(ax.c2p(0, j / 8), LEFT, 0.3)
                          for j in range(1, 5)])
        xl = Text("X = number of heads", font_size=24, color=GREY_C).next_to(ax.x_axis, DOWN, buff=0.6)
        yl = Text("probability", font_size=24, color=GREY_C).rotate(PI / 2).next_to(yticks, LEFT, buff=0.25)
        moves, stacks = [], [VGroup() for _ in range(4)]
        for o, t in zip(OUTCOMES, tiles):
            k = o.count("H")
            target = t.copy().scale(0.8).move_to(ax.c2p(k + 0.7, 0) + UP * (0.3 + 0.52 * len(stacks[k])))
            stacks[k].add(t)
            moves.append(t.animate.scale(0.8).move_to(target))
        self.play(FadeOut(heads), Create(ax), FadeIn(ticks, xl),
                  Transform(cap, self.caption("Group the outcomes by X", "1, 3, 3 and 1 outcomes")))
        self.play(*moves, run_time=2)
        counts = VGroup(*[MathTex(rf"{c}\ \text{{of}}\ 8", font_size=30, color=BLUE_C).next_to(s, UP, buff=0.15)
                          for c, s in zip(COUNTS, stacks)])
        self.play(FadeIn(counts))
        self.wait(1)
        self.snap()

        bars = VGroup()
        for k, c in enumerate(COUNTS):
            p0, p1 = ax.c2p(k + 0.4, 0), ax.c2p(k + 1.0, c / 8)
            bars.add(Rectangle(width=p1[0] - p0[0], height=p1[1] - p0[1], fill_color=BLUE_C, fill_opacity=0.8,
                               stroke_color=WHITE).move_to((p0 + p1) / 2))
        probs = VGroup(*[MathTex(rf"\frac{{{c}}}{{8}}", font_size=40, color=BLUE_C).next_to(b, UP, buff=0.12)
                         for c, b in zip(COUNTS, bars)])
        self.play(*[ReplacementTransform(s, b) for s, b in zip(stacks, bars)], ReplacementTransform(counts, probs),
                  FadeIn(yticks, yl),
                  Transform(cap, self.caption("Each group becomes a bar: count / 8",
                                              "this bar chart is the PMF of X")), run_time=2)
        self.wait(1)
        total = MathTex(r"\tfrac18+\tfrac38+\tfrac38+\tfrac18=1", font_size=38).to_corner(UR, buff=0.4).shift(DOWN * 1.3)
        gap = MathTex(r"P(X=1.5)=0", font_size=34, color=ORANGE_C).next_to(total, DOWN, buff=0.35)
        self.play(FadeIn(total), FadeIn(gap))
        self.wait(2.5)
        self.snap()


def key_frames_grid(frames, out, gap=16):
    w, h = frames[0].size
    cols = 2
    rows = (len(frames) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * w + (cols - 1) * gap, rows * h + (rows - 1) * gap), "white")
    for i, f in enumerate(frames):
        sheet.paste(f.convert("RGB"), ((i % cols) * (w + gap), (i // cols) * (h + gap)))
    sheet.save(out)


if __name__ == "__main__":
    media = HERE / ".manim"
    with tempconfig({"quality": "medium_quality", "background_color": WHITE, "media_dir": str(media),
                     "output_file": "coin_pmf", "disable_caching": True, "verbosity": "WARNING",
                     "progress_bar": "none"}):
        scene = CoinPMF()
        scene.render()
    mp4 = HERE / "coin_pmf.mp4"
    shutil.copy(next(media.rglob("coin_pmf.mp4")), mp4)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(mp4), "-vf",
                    "fps=12,scale=720:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "coin_pmf.gif")], check=True)
    key_frames_grid(scene.snaps, HERE / "coin_pmf_frames.png")
    shutil.rmtree(media)

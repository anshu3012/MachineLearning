"""The CDF of the sum of two dice, built by stacking the PMF bars: the column at x holds every bar up to x.
Run: python cdf_build.py -> cdf_build.mp4, cdf_build.gif, cdf_build_frames.png"""
import shutil
import subprocess
from pathlib import Path

from manim import *
from PIL import Image

HERE = Path(__file__).parent
BLUE_C, ORANGE_C, GREEN_C, GREY_C = "#4C78A8", "#F58518", "#54A24B", "#6B6B6B"
Text.set_default(color=BLACK, font="Latin Modern Roman")
XS = list(range(2, 13))
COUNTS = [6 - abs(x - 7) for x in XS]          # pairs giving each sum, out of 36


class CdfBuild(Scene):
    def snap(self):
        self.snaps.append(Image.fromarray(self.renderer.get_frame()))

    def caption(self, title, detail):
        return VGroup(Text(title, font_size=34, weight=BOLD), Text(detail, font_size=26, color=GREY_C)
                      ).arrange(DOWN, buff=0.2).to_edge(UP, buff=0.3)

    def construct(self):
        self.snaps = []
        ax = Axes(x_range=[1, 13, 1], y_range=[0, 1.0, 0.25], x_length=11, y_length=5,
                  axis_config={"color": GREY_C, "include_tip": False, "font_size": 30},
                  x_axis_config={"numbers_to_include": XS},
                  y_axis_config={"numbers_to_include": [0, 0.25, 0.5, 0.75, 1.0], "decimal_number_config": {"num_decimal_places": 2}}
                  ).shift(DOWN * 0.7)
        for n in list(ax.x_axis.numbers) + list(ax.y_axis.numbers):
            n.set_color(GREY_C)
        w = ax.x_axis.unit_size * 0.7

        def bar(x, y0, c, colour):                     # a bar of height c/36 starting at y0/36
            lo, hi = ax.c2p(x, y0 / 36), ax.c2p(x, (y0 + c) / 36)
            return Rectangle(width=w, height=hi[1] - lo[1], fill_color=colour, fill_opacity=0.85,
                             stroke_color=WHITE, stroke_width=1.5).move_to((lo + hi) / 2)

        pmf = VGroup(*[bar(x, 0, c, BLUE_C) for x, c in zip(XS, COUNTS)])
        cap = self.caption("PMF of the sum of two dice", "bar height = P(X = x), from 1/36 to 6/36")
        self.play(Create(ax), FadeIn(pmf, lag_ratio=0.1), FadeIn(cap), run_time=1.5)
        self.wait(0.5)
        self.snap()

        # Column x of the CDF = all PMF bars from 2 up to x, stacked.
        new_cap = self.caption("CDF: stack every bar up to x", "F(x) = P(X ≤ x) = running total of the PMF")
        self.play(Transform(cap, new_cap))
        total = 0
        for i, (x, c) in enumerate(zip(XS, COUNTS)):
            moves = []
            stack_base = 0
            for j in range(i):                         # copies of the earlier bars slide over to column x
                piece = bar(XS[j], 0, COUNTS[j], BLUE_C)    # a fresh blue copy of bar j, at its PMF place
                moves.append(piece.animate.move_to(bar(x, stack_base, COUNTS[j], BLUE_C)))
                self.add(piece)
                stack_base += COUNTS[j]
            moves.append(pmf[i].animate.move_to(bar(x, stack_base, c, ORANGE_C)).set_fill(ORANGE_C))
            self.play(*moves, run_time=0.45 if i > 2 else 0.8)
            total += c
            if x in (5, 9):
                lbl = Text(f"F({x}) = {total}/36 = {total / 36:.3f}", font_size=24, color=ORANGE_C)
                lbl.next_to(ax.c2p(x, total / 36), UL, buff=0.15)
                self.play(FadeIn(lbl), run_time=0.4)
                self.wait(0.4)
                self.snap()
        cum, steps = 0, []
        for x, c in zip(XS, COUNTS):
            cum += c
            steps.append(Line(ax.c2p(x, cum / 36), ax.c2p(x + 1, cum / 36), color=GREEN_C, stroke_width=6))
        self.play(Transform(cap, self.caption("The CDF climbs in steps from 0 to 1",
                                              "it jumps at each possible sum and is flat in between")),
                  Create(VGroup(*steps), lag_ratio=0.2), run_time=1.6)
        self.wait(1.5)
        self.snap()


def key_frames_grid(frames, out, gap=16):
    w, h = frames[0].size
    sheet = Image.new("RGB", (2 * w + gap, 2 * h + gap), "white")
    for i, f in enumerate(frames[:4]):
        sheet.paste(f.convert("RGB"), ((i % 2) * (w + gap), (i // 2) * (h + gap)))
    sheet.save(out)


if __name__ == "__main__":
    media = HERE / ".manim"
    with tempconfig({"quality": "medium_quality", "background_color": WHITE, "media_dir": str(media),
                     "output_file": "cdf_build", "disable_caching": True, "verbosity": "WARNING",
                     "progress_bar": "none"}):
        scene = CdfBuild()
        scene.render()
    mp4 = HERE / "cdf_build.mp4"
    shutil.copy(next(media.rglob("cdf_build.mp4")), mp4)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(mp4), "-vf",
                    "fps=12,scale=720:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "cdf_build.gif")], check=True)
    key_frames_grid(scene.snaps, HERE / "cdf_build_frames.png")
    shutil.rmtree(media)

"""Building a box plot by hand for 6, 213, 241, 260, 281, 290, 314, 321, 350, 1500:
quartiles -> box -> fences -> whiskers and outliers.
Run: python boxplot_build.py -> boxplot_build.mp4, boxplot_build.gif, boxplot_build_frames.png"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
from manim import *
from PIL import Image

HERE = Path(__file__).parent
BLUE_C, ORANGE_C, GREEN_C, RED_C, GREY_C = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#6B6B6B"
Text.set_default(color=BLACK, font="Latin Modern Roman")
DATA = [6, 213, 241, 260, 281, 290, 314, 321, 350, 1500]
Q1, Q2, Q3 = np.percentile(DATA, [25, 50, 75], method="weibull")      # (n + 1) p positions
IQR = Q3 - Q1
LO, HI = Q1 - 1.5 * IQR, Q3 + 1.5 * IQR


class BoxplotBuild(Scene):
    def snap(self):
        self.snaps.append(Image.fromarray(self.renderer.get_frame()))

    def caption(self, title, detail):
        return VGroup(Text(title, font_size=34, weight=BOLD), Text(detail, font_size=26, color=GREY_C)
                      ).arrange(DOWN, buff=0.2).to_edge(UP, buff=0.5)

    def construct(self):
        self.snaps = []
        line = NumberLine(x_range=[0, 600, 100], length=12, color=GREY_C, include_numbers=True,
                          font_size=26, numbers_to_include=range(0, 601, 100)).shift(DOWN * 2.2)
        line.numbers.set_color(GREY_C)
        y0 = line.n2p(0)[1]

        def x(v):                                     # 1500 does not fit: park it at the right edge
            return line.n2p(min(v, 590))[0]

        def dot(v, colour=BLACK):
            return Dot([x(v), y0 + 0.45, 0], radius=0.09, color=colour)

        dots = VGroup(*[dot(v) for v in DATA])
        far = Text("1500 →", font_size=24, color=GREY_C).next_to(dots[-1], UP, buff=0.15)
        cap = self.caption("1. Sort the data", "10 values; 1500 is far off to the right")
        self.play(Create(line), FadeIn(dots, lag_ratio=0.1), FadeIn(far), FadeIn(cap))
        self.wait(0.6)
        self.snap()

        # Step 2: quartiles and the box
        top, bottom = y0 + 2.6, y0 + 1.3
        box = Polygon([x(Q1), bottom, 0], [x(Q3), bottom, 0], [x(Q3), top, 0], [x(Q1), top, 0],
                      color=BLUE_C, fill_color=BLUE_C, fill_opacity=0.18, stroke_width=4)
        med = Line([x(Q2), bottom, 0], [x(Q2), top, 0], color=ORANGE_C, stroke_width=6)
        labels = VGroup(*[Text(t, font_size=22, color=c).next_to([x(v), top, 0], UP, buff=0.12)
                          for t, v, c in [(f"Q1 = {Q1:g}", Q1, BLUE_C), (f"Q2 = {Q2:g}", Q2, ORANGE_C),
                                          (f"Q3 = {Q3:g}", Q3, BLUE_C)]])
        labels[0].next_to([x(Q1), top - 0.2, 0], LEFT, buff=0.15)     # Q1 left of the box, Q3 right of it
        labels[2].next_to([x(Q3), top - 0.2, 0], RIGHT, buff=0.15)
        self.play(Transform(cap, self.caption("2. Quartiles make the box", f"IQR = Q3 - Q1 = {IQR:g}")),
                  Create(box), Create(med), FadeIn(labels), run_time=1.4)
        self.wait(0.6)
        self.snap()

        # Step 3: fences 1.5 IQR beyond the box
        mid = (top + bottom) / 2
        fences = VGroup(*[DashedLine([x(v), y0 + 0.1, 0], [x(v), top + 0.1, 0], color=RED_C, dash_length=0.12)
                          for v in (LO, HI)])
        flabels = VGroup(Text(f"lower fence\n{LO:g}", font_size=20, color=RED_C).next_to(fences[0], LEFT, buff=0.1),
                         Text(f"upper fence\n{HI:g}", font_size=20, color=RED_C).next_to(fences[1], RIGHT, buff=0.1))
        self.play(Transform(cap, self.caption("3. Fences: 1.5 IQR beyond the box",
                                              f"Q1 - 1.5 IQR and Q3 + 1.5 IQR  (1.5 IQR = {1.5 * IQR:g})")),
                  Create(fences), FadeIn(flabels), run_time=1.4)
        self.wait(0.6)
        self.snap()

        # Step 4: whiskers stop at the last value inside the fences; the rest are outliers
        inside = [v for v in DATA if LO <= v <= HI]
        wl, wh = min(inside), max(inside)
        whiskers = VGroup(Line([x(wl), mid, 0], [x(Q1), mid, 0], color=BLUE_C, stroke_width=4),
                          Line([x(Q3), mid, 0], [x(wh), mid, 0], color=BLUE_C, stroke_width=4),
                          Line([x(wl), mid - 0.3, 0], [x(wl), mid + 0.3, 0], color=BLUE_C, stroke_width=4),
                          Line([x(wh), mid - 0.3, 0], [x(wh), mid + 0.3, 0], color=BLUE_C, stroke_width=4))
        outs = VGroup(*[dot(v, RED_C).scale(1.5) for v in DATA if v < LO or v > HI])
        self.play(Transform(cap, self.caption("4. Whiskers and outliers",
                                              f"whiskers end at {wl} and {wh}; 6 and 1500 are outliers")),
                  Create(whiskers), Transform(VGroup(dots[0], dots[-1]), outs), run_time=1.4)
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
                     "output_file": "boxplot_build", "disable_caching": True, "verbosity": "WARNING",
                     "progress_bar": "none"}):
        scene = BoxplotBuild()
        scene.render()
    mp4 = HERE / "boxplot_build.mp4"
    shutil.copy(next(media.rglob("boxplot_build.mp4")), mp4)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(mp4), "-vf",
                    "fps=12,scale=720:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "boxplot_build.gif")], check=True)
    key_frames_grid(scene.snaps, HERE / "boxplot_build_frames.png")
    shutil.rmtree(media)

"""k-means binning on one column, step by step: place centres, assign each value to the nearest centre,
move each centre to the mean of its values, repeat until nothing changes, then cut halfway between centres.
Twelve made-up values in three groups, k = 3. The final edges (20.83, 44.33) match
KBinsDiscretizer(n_bins=3, strategy="kmeans") on the same values.
Run: python kmeans_steps.py  -> kmeans_steps.mp4, kmeans_steps.gif, kmeans_steps_frames.png"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
from manim import *
from PIL import Image, ImageOps

HERE = Path(__file__).parent
BLUE_C, ORANGE_C, GREEN_C, RED_C, GREY_C = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#6B6B6B"
COLOURS = [BLUE_C, ORANGE_C, GREEN_C]
Text.set_default(color=BLACK, font="Latin Modern Roman")

X = np.array([2, 5, 8, 10, 12, 15, 30, 33, 36, 52, 55, 60.0])
START = np.array([14, 22, 40.0])   # starting centres, placed by hand


class KMeansSteps(Scene):
    def snap(self):
        self.snaps.append(Image.fromarray(self.renderer.get_frame()))

    def caption(self, title, sub):
        return VGroup(Text(title, font_size=32, weight=BOLD), Text(sub, font_size=23, color=GREY_C)
                      ).arrange(DOWN, buff=0.15).move_to(DOWN * 2.0)

    def construct(self):
        self.snaps = []
        line = NumberLine(x_range=[0, 65, 5], length=12, color=GREY_C, include_numbers=True,
                          numbers_to_include=range(0, 66, 10), font_size=26,
                          decimal_number_config={"color": BLACK, "num_decimal_places": 0}).shift(UP * 0.6)
        dots = VGroup(*[Dot(line.n2p(v), radius=0.11, color=GREY_C) for v in X])
        heading = Text("k-means binning, k = 3", font_size=34, weight=BOLD).to_edge(UP, buff=0.4)

        def centre_marks(cs):
            return VGroup(*[Triangle(color=c, fill_color=c, fill_opacity=1).scale(0.18).rotate(PI)
                            .move_to(line.n2p(v) + UP * 0.55) for v, c in zip(cs, COLOURS)])

        def labels(cs):
            return VGroup(*[Text(f"{v:.1f}", font_size=22, color=c).move_to(line.n2p(v) + UP * 1.0)
                            for v, c in zip(cs, COLOURS)])

        def colour_dots(lab):
            return [d.animate.set_color(COLOURS[k]) for d, k in zip(dots, lab)]

        # Step 0: the values and the starting centres
        c = START.copy()
        marks, labs = centre_marks(c), labels(c)
        cap = self.caption("1. Place k = 3 centres", "here at 14, 22 and 40; scikit-learn starts at the middles of equal-width bins")
        self.play(FadeIn(heading), Create(line), FadeIn(dots), FadeIn(marks), FadeIn(labs), FadeIn(cap))
        self.wait(0.8)
        self.snap()

        # Steps 1 to 3: assign, move, repeat until the groups stop changing
        it = 1
        while True:
            lab = np.abs(X[:, None] - c).argmin(1)
            self.play(*colour_dots(lab), Transform(cap, self.caption(
                "2. Each value joins its nearest centre", f"round {it}: colour = the centre it is closest to")))
            self.wait(0.6)
            if it == 1:
                self.snap()
            new = np.array([X[lab == k].mean() for k in range(3)])
            if np.allclose(new, c):
                break
            self.play(Transform(marks, centre_marks(new)), Transform(labs, labels(new)), Transform(cap, self.caption(
                "3. Each centre moves to the mean of its values",
                "then assign again; stop when no value changes group")), run_time=1.4)
            self.wait(0.6)
            if it == 2:
                self.snap()
            c, it = new, it + 1

        # Step 4: the bin edges are halfway between neighbouring centres
        edges = (c[1:] + c[:-1]) / 2
        cuts = VGroup(*[DashedLine(line.n2p(e) + DOWN * 0.5, line.n2p(e) + UP * 1.4, color=RED_C, stroke_width=5)
                        for e in edges])
        cut_labs = VGroup(*[Text(f"edge {e:.2f}", font_size=24, color=RED_C).next_to(l, DOWN, buff=0.45)
                            for e, l in zip(edges, cuts)])
        self.play(Create(cuts), FadeIn(cut_labs), Transform(cap, self.caption(
            "4. Nothing changed: cut halfway between centres",
            "(8.67 + 33) / 2 = 20.83 and (33 + 55.67) / 2 = 44.33: three bins")))
        self.wait(1.5)
        self.snap()


def key_frames_grid(frames, out, gap=16, pad=20):
    boxes = [ImageOps.invert(f.convert("RGB")).getbbox() for f in frames[:4]]
    l, t = min(b[0] for b in boxes) - pad, min(b[1] for b in boxes) - pad
    r, b_ = max(b[2] for b in boxes) + pad, max(b[3] for b in boxes) + pad
    frames = [f.crop((max(l, 0), max(t, 0), r, b_)) for f in frames]
    w, h = frames[0].size
    sheet = Image.new("RGB", (2 * w + gap, 2 * h + gap), "white")
    for i, f in enumerate(frames[:4]):
        sheet.paste(f.convert("RGB"), ((i % 2) * (w + gap), (i // 2) * (h + gap)))
    sheet.save(out)


if __name__ == "__main__":
    media = HERE / ".manim"
    with tempconfig({"quality": "medium_quality", "background_color": WHITE, "media_dir": str(media),
                     "output_file": "kmeans_steps", "disable_caching": True, "verbosity": "WARNING",
                     "progress_bar": "none"}):
        scene = KMeansSteps()
        scene.render()
    mp4 = HERE / "kmeans_steps.mp4"
    shutil.copy(next(media.rglob("kmeans_steps.mp4")), mp4)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(mp4), "-vf",
                    "fps=12,scale=720:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "kmeans_steps.gif")], check=True)
    key_frames_grid(scene.snaps, HERE / "kmeans_steps_frames.png")
    shutil.rmtree(media)

"""How SVM scores a line: slide parallel copies out to the first point of each class, measure the gap, keep the widest.
Run: python margin_search.py  -> margin_search.mp4, margin_search.gif, margin_search_frames.png"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
from manim import *
from PIL import Image

HERE = Path(__file__).parent
BLUE_C, GREEN_C, RED_C, GREY_C = "#4C78A8", "#54A24B", "#E45756", "#6B6B6B"
Text.set_default(color=BLACK, font="Latin Modern Roman")
G = np.array([(2, 6), (3.5, 7.5), (4.5, 6), (6, 7.5), (2.5, 8.5), (5, 9), (7, 9), (7.5, 6.8)])
R = np.array([(1, 1.5), (2.5, 3), (3.5, 1), (5, 2.5), (6.5, 1.5), (7, 3.5), (1.5, 3.8), (4, 3.5)])
LINES = {  # w, b of w.x + b = 0 (pi1 is the widest-margin line from figs.py)
    "π₂": (np.array([0.3, 1.0]), -6.3, BLUE_C),
    "π₁": (np.array([0.0489, 0.8979]), -4.4853, BLACK),
}


class MarginSearch(Scene):
    def snap(self):
        self.snaps.append(Image.fromarray(self.renderer.get_frame()))

    def caption(self, *lines):
        return VGroup(*[Text(t, font_size=30) for t in lines]).arrange(DOWN, aligned_edge=LEFT, buff=0.18) \
            .move_to(ORIGIN, aligned_edge=UL).shift(RIGHT * 0.2 + UP * 2.5)

    def seg(self, w, b, shift, colour, dashed=False):
        xs = np.array([0.0, 8.5])
        ys = (shift - b - w[0] * xs) / w[1]
        line = Line(self.ax.c2p(xs[0], ys[0]), self.ax.c2p(xs[1], ys[1]), color=colour, stroke_width=5 if not dashed else 3)
        return DashedLine(line.get_start(), line.get_end(), color=GREY_C, stroke_width=3) if dashed else line

    def construct(self):
        self.snaps = []
        self.ax = Axes(x_range=[0, 8.5, 1], y_range=[0, 10, 1], x_length=5.4, y_length=6.4, tips=False,
                       axis_config=dict(color=GREY_C, include_ticks=False)).to_edge(LEFT, buff=0.6)
        dots = VGroup(*[Dot(self.ax.c2p(*p), radius=0.1, color=GREEN_C) for p in G],
                      *[Dot(self.ax.c2p(*p), radius=0.1, color=RED_C) for p in R])
        self.add(self.ax, dots)
        cap = self.caption("Step 1: pick any line π", "that separates the classes")
        w, b, colour = LINES["π₂"]
        pi = self.seg(w, b, 0, colour)
        self.play(Create(pi), FadeIn(cap))
        self.wait(0.5)
        self.snap()

        result = self.measure(w, b, cap, "d′")
        self.snap()

        # Step 4: another line, same procedure
        w1, b1, c1 = LINES["π₁"]
        new_cap = self.caption("Step 4: repeat for other lines", "and keep the one with", "the widest margin")
        self.play(FadeOut(result), Transform(pi, self.seg(w1, b1, 0, c1)), Transform(cap, new_cap))
        result = self.measure(w1, b1, cap, "d", keep_caption=True)
        self.wait(1.5)
        self.snap()

    def measure(self, w, b, cap, name, keep_caption=False):
        top, bottom = (G @ w + b).min(), (R @ w + b).max()
        up, down = ValueTracker(0), ValueTracker(0)
        plus = always_redraw(lambda: self.seg(w, b, up.get_value(), GREY_C, dashed=True))
        minus = always_redraw(lambda: self.seg(w, b, down.get_value(), GREY_C, dashed=True))
        self.add(plus, minus)
        if not keep_caption:
            self.play(Transform(cap, self.caption("Step 2: slide parallel copies out", "until each touches the first",
                                                  "point of its class: π+ and π−")))
        self.play(up.animate.set_value(top), down.animate.set_value(bottom), run_time=2)
        if not keep_caption:
            self.snap()
        touch = [p for p in G if np.isclose(p @ w + b, top, atol=1e-3)] + \
                [p for p in R if np.isclose(p @ w + b, bottom, atol=1e-3)]
        rings = VGroup(*[Circle(radius=0.2, color=BLACK, stroke_width=3).move_to(self.ax.c2p(*p)) for p in touch])
        d = (top - bottom) / np.linalg.norm(w)
        unit = w / np.linalg.norm(w)
        start = np.array([0.9, (bottom - b - w[0] * 0.9) / w[1]])
        arrow = DoubleArrow(self.ax.c2p(*start), self.ax.c2p(*(start + unit * d)), buff=0, color=BLACK,
                            stroke_width=4, tip_length=0.2)
        label = Text(f"{name} = {d:.2f}", font_size=34).move_to(ORIGIN, aligned_edge=UL).shift(RIGHT * 0.2 + UP * 0.2)
        anims = [Create(rings), GrowFromCenter(arrow), FadeIn(label)]
        if not keep_caption:
            anims.append(Transform(cap, self.caption("Step 3: the gap between π+", "and π− is the margin")))
        self.play(*anims)
        self.wait(0.6)
        group = VGroup(rings, arrow, label)
        self.remove(plus, minus)
        dashes = VGroup(self.seg(w, b, top, GREY_C, True), self.seg(w, b, bottom, GREY_C, True))
        self.add(dashes)
        group.add(dashes)
        return group


def key_frames_grid(frames, out, gap=16):
    w, h = frames[0].size
    sheet = Image.new("RGB", (2 * w + gap, 2 * h + gap), "white")
    for i, f in enumerate(frames[:4]):
        sheet.paste(f.convert("RGB"), ((i % 2) * (w + gap), (i // 2) * (h + gap)))
    sheet.save(out)


if __name__ == "__main__":
    media = HERE / ".manim"
    with tempconfig({"quality": "medium_quality", "background_color": WHITE, "media_dir": str(media),
                     "output_file": "margin_search", "disable_caching": True, "verbosity": "WARNING",
                     "progress_bar": "none"}):
        scene = MarginSearch()
        scene.render()
    mp4 = HERE / "margin_search.mp4"
    shutil.copy(next(media.rglob("margin_search.mp4")), mp4)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(mp4), "-vf",
                    "fps=12,scale=720:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "margin_search.gif")], check=True)
    key_frames_grid(scene.snaps, HERE / "margin_search_frames.png")
    shutil.rmtree(media)

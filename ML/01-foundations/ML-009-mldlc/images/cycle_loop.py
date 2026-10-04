"""One pass through the ML development life cycle, a loop back after a failed test, and retraining.
Run: python cycle_loop.py  -> cycle_loop.mp4, cycle_loop.gif, cycle_loop_frames.png"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
from manim import *
from PIL import Image

HERE = Path(__file__).parent
PURPLE_C, BLUE_C, GREEN_C, ORANGE_C, RED_C, TEAL_C, GREY_C = (
    "#B279A2", "#4C78A8", "#54A24B", "#F58518", "#E45756", "#72B7B2", "#6B6B6B")
Text.set_default(color=BLACK, font="Latin Modern Roman")

STAGES = [("1 Frame", PURPLE_C), ("2 Gather data", BLUE_C), ("3 Preprocess", BLUE_C), ("4 EDA", BLUE_C),
          ("5 Features", GREEN_C), ("6 Train, select", ORANGE_C), ("7 Deploy", TEAL_C), ("8 Test", TEAL_C),
          ("9 Optimize", TEAL_C)]


def edge(rect, d):
    """Point where a ray from the rectangle's centre in direction d leaves the rectangle."""
    t = min(rect.width / 2 / max(abs(d[0]), 1e-9), rect.height / 2 / max(abs(d[1]), 1e-9))
    return rect.get_center() + d * t


class CycleLoop(Scene):
    def snap(self):
        self.snaps.append(Image.fromarray(self.renderer.get_frame()))

    def caption(self, text, colour=BLACK):
        new = Text(text, font_size=26, color=colour, line_spacing=0.9).move_to(UP * 0.6)
        anims = [FadeIn(new)] if self.cap is None else [FadeTransform(self.cap, new)]
        self.cap = new
        return anims

    def light(self, i, colour=None):
        box = self.boxes[i][0]
        return box.animate.set_fill(colour or STAGES[i][1], opacity=0.55)

    def construct(self):
        self.snaps, self.cap = [], None
        self.boxes = VGroup()
        for k, (name, colour) in enumerate(STAGES):
            a = np.deg2rad(90 - 40 * k)
            rect = RoundedRectangle(corner_radius=0.12, width=2.9, height=0.8, color=colour, stroke_width=4)
            rect.set_fill(colour, opacity=0.08)
            label = Text(name, font_size=22)
            self.boxes.add(VGroup(rect, label).move_to([5.4 * np.cos(a), 2.8 * np.sin(a), 0]))
        arrows = VGroup()
        for k in range(8):
            a, b = self.boxes[k][0], self.boxes[k + 1][0]
            d = normalize(b.get_center() - a.get_center())
            arrows.add(Arrow(edge(a, d), edge(b, -d), buff=0.08, color=GREY_C,
                             stroke_width=4, max_tip_length_to_length_ratio=0.3))
        self.play(FadeIn(self.boxes, lag_ratio=0.1), Create(arrows), *self.caption("The ML development life cycle"))

        # first pass, stages 1 to 8
        self.play(*self.caption("First pass: stage by stage"))
        for i in range(8):
            self.play(self.light(i), run_time=0.35)
        self.wait(0.5)
        self.snap()

        # testing finds an issue: go back to features
        back = CurvedArrow(self.boxes[7].get_corner(DR) + DR * 0.05, self.boxes[4].get_corner(UL) + UL * 0.05,
                           angle=TAU / 14, color=RED_C, stroke_width=5)
        self.play(self.light(7, RED_C), Create(back),
                  *self.caption("Test finds an issue (e.g. poor features):\ngo back to the stage that caused it", RED_C))
        self.wait(0.8)
        self.snap()

        # redo stages 5 to 8; the test passes
        self.play(FadeOut(back), *[self.boxes[i][0].animate.set_fill(STAGES[i][1], opacity=0.08) for i in range(4, 8)],
                  *self.caption("Redo stages 5 to 8"))
        for i in range(4, 8):
            self.play(self.light(i), run_time=0.35)
        self.play(self.light(7, GREEN_C), self.light(8),
                  *self.caption("Test passes: optimize and\nlaunch for all users", GREEN_C))
        self.wait(0.8)
        self.snap()

        # the model drifts over time: retrain on new data
        loop = CurvedArrow(self.boxes[8].get_right() + RIGHT * 0.05, self.boxes[1].get_left() + LEFT * 0.05,
                           angle=TAU / 8, color=RED_C, stroke_width=5)
        self.play(Create(loop), *self.caption("Data changes and the model drifts:\nretrain on new data", RED_C))
        self.wait(1.2)
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
                     "output_file": "cycle_loop", "disable_caching": True, "verbosity": "WARNING",
                     "progress_bar": "none"}):
        scene = CycleLoop()
        scene.render()
    mp4 = HERE / "cycle_loop.mp4"
    shutil.copy(next(media.rglob("cycle_loop.mp4")), mp4)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(mp4), "-vf",
                    "fps=12,scale=720:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "cycle_loop.gif")], check=True)
    key_frames_grid(scene.snaps, HERE / "cycle_loop_frames.png")
    shutil.rmtree(media)

"""Drawing bootstrap samples: 10 rows, 10 draws with replacement; repeats appear and some rows are never drawn.
Run: python bootstrap_draw.py  -> bootstrap_draw.mp4, bootstrap_draw.gif, bootstrap_draw_frames.png"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
from manim import *
from PIL import Image

HERE = Path(__file__).parent
BLUE_C, ORANGE_C, GREEN_C, RED_C, GREY_C = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#6B6B6B"
Text.set_default(color=BLACK, font="Latin Modern Roman")
N = 10
rng = np.random.default_rng(10)
SAMPLES = [rng.integers(0, N, N) for _ in range(2)]


def card(i, colour):
    box = RoundedRectangle(width=0.9, height=0.9, corner_radius=0.1, color=colour, fill_color=colour,
                           fill_opacity=0.15, stroke_width=3)
    return VGroup(box, Text(str(i + 1), font_size=30)).set_z_index(1)


class BootstrapDraw(Scene):
    def snap(self):
        self.snaps.append(Image.fromarray(self.renderer.get_frame()))

    def construct(self):
        self.snaps = []
        title = Text("Bootstrap sample: draw 10 rows from 10, with replacement", font_size=32).to_edge(UP, buff=0.35)
        data = VGroup(*[card(i, BLUE_C) for i in range(N)]).arrange(RIGHT, buff=0.22).shift(UP * 1.9)
        lab_d = Text("data D", font_size=26).next_to(data, LEFT, buff=0.35)
        self.add(title, data, lab_d)
        y_rows = [0.0, -1.9]
        for s, (sample, y) in enumerate(zip(SAMPLES, y_rows)):
            slots = VGroup(*[RoundedRectangle(width=0.9, height=0.9, corner_radius=0.1, color=GREY_C, stroke_width=2)
                             for _ in range(N)]).arrange(RIGHT, buff=0.22).move_to([data.get_x(), y, 0])
            lab = Text(f"D{s + 1}", font_size=26).next_to(slots, LEFT, buff=0.35)
            self.play(FadeIn(slots), FadeIn(lab), run_time=0.4)
            counts = np.bincount(sample, minlength=N)
            seen = set()
            for k, i in enumerate(sample):
                colour = ORANGE_C if i in seen else GREEN_C           # orange = a repeat
                seen.add(i)
                ring = SurroundingRectangle(data[i], color=BLACK, buff=0.05, stroke_width=4)
                new = card(i, colour).move_to(data[i])
                if s == 0:
                    self.play(Create(ring), run_time=0.2)
                    self.play(new.animate.move_to(slots[k]), FadeOut(ring), run_time=0.45)
                else:
                    self.play(new.animate.move_to(slots[k]), run_time=0.2)
                if (s == 0 and k == 3) or (s == 1 and k == 5):
                    self.snap()
            unused = [i for i in range(N) if counts[i] == 0]
            note = Text(f"{len(seen)} different rows; never drawn: " + ", ".join(str(i + 1) for i in unused),
                        font_size=24, color=RED_C).next_to(slots, DOWN, buff=0.18)
            crosses = VGroup(*[Cross(data[i], stroke_color=RED_C, stroke_width=4, scale_factor=0.6) for i in unused])
            self.play(FadeIn(note), Create(crosses), run_time=0.6)
            self.wait(0.8)
            if s == 0:
                self.snap()
            if s == 0:
                self.play(FadeOut(crosses), run_time=0.3)
        legend = VGroup(card(0, GREEN_C).scale(0.5), Text("first time drawn", font_size=22),
                        card(0, ORANGE_C).scale(0.5), Text("drawn again (repeat)", font_size=22)).arrange(RIGHT, buff=0.2)
        legend.to_edge(DOWN, buff=0.15)
        self.play(FadeIn(legend))
        self.wait(1.5)
        self.snap()


def key_frames_grid(frames, out, gap=16):
    w, hgt = frames[0].size
    sheet = Image.new("RGB", (2 * w + gap, 2 * hgt + gap), "white")
    for i, f in enumerate(frames[:4]):
        sheet.paste(f.convert("RGB"), ((i % 2) * (w + gap), (i // 2) * (hgt + gap)))
    sheet.save(out)


if __name__ == "__main__":
    for s in SAMPLES:
        print("sample", s + 1, "unique", len(set(s)))
    media = HERE / ".manim"
    with tempconfig({"quality": "medium_quality", "background_color": WHITE, "media_dir": str(media),
                     "output_file": "bootstrap_draw", "disable_caching": True, "verbosity": "WARNING",
                     "progress_bar": "none"}):
        scene = BootstrapDraw()
        scene.render()
    mp4 = HERE / "bootstrap_draw.mp4"
    shutil.copy(next(media.rglob("bootstrap_draw.mp4")), mp4)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(mp4), "-vf",
                    "fps=12,scale=720:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "bootstrap_draw.gif")], check=True)
    key_frames_grid(scene.snaps, HERE / "bootstrap_draw_frames.png")
    shutil.rmtree(media)

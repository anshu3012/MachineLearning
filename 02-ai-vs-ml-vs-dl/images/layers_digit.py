"""How DL layers recognise a handwritten 7: pixels -> edges -> shapes -> answer.
Run: python layers_digit.py  -> layers_digit.mp4, layers_digit.gif, layers_digit_frames.png"""
import shutil
import subprocess
from pathlib import Path

from manim import *
from PIL import Image

HERE = Path(__file__).parent
BLUE_C, ORANGE_C, GREEN_C, PURPLE_C, GREY_C = "#4C78A8", "#F58518", "#54A24B", "#B279A2", "#6B6B6B"
Text.set_default(color=BLACK, font="Latin Modern Roman")

# Pixels of a 7 on a 7x7 grid, as (row, col)
TOP_BAR = [(0, c) for c in range(1, 6)]
SLANT = [(1, 5), (2, 4), (3, 4), (4, 3), (5, 3), (6, 2)]
EDGES = [  # (pixels, colour, icon direction) - small pieces layer 1 finds
    ([(0, 1), (0, 2)], ORANGE_C, RIGHT),
    ([(0, 3), (0, 4), (0, 5)], ORANGE_C, RIGHT),
    ([(1, 5), (2, 4)], PURPLE_C, DL),
    ([(3, 4), (4, 3)], PURPLE_C, DL),
    ([(5, 3), (6, 2)], PURPLE_C, DL),
]


class LayersDigit(Scene):
    def snap(self):
        self.snaps.append(Image.fromarray(self.renderer.get_frame()))

    def arrow_to(self, x):
        return Arrow([x - 1.9, 0, 0], [x - 1.35, 0, 0], color=GREY_C, buff=0, stroke_width=6,
                     max_tip_length_to_length_ratio=0.5)

    def column(self, title, x):
        label = Text(title, font_size=26, weight=BOLD).move_to([x, 3.0, 0])
        frame = RoundedRectangle(width=2.6, height=4.6, corner_radius=0.2, color=GREY_C).move_to([x, 0, 0])
        return VGroup(frame, label)

    def construct(self):
        self.snaps = []
        size = 0.42
        cells = {}
        grid = VGroup()
        for r in range(7):
            for c in range(7):
                on = (r, c) in TOP_BAR + SLANT
                sq = Square(size, stroke_color=GREY_C, stroke_width=1,
                            fill_color=BLACK if on else WHITE, fill_opacity=0.85 if on else 1)
                sq.move_to([c * size, -r * size, 0])
                cells[(r, c)] = sq
                grid.add(sq)
        grid.move_to([-5.0, 0, 0])
        g_title = Text("Input: pixels", font_size=26, weight=BOLD).move_to([-5.0, 3.0, 0])
        self.play(FadeIn(grid, lag_ratio=0.02), Write(g_title), run_time=2)
        self.wait(0.5)
        self.snap()

        # Layer 1: tiny edges
        col1 = self.column("Layer 1: edges", -1.4)
        self.play(GrowArrow(self.arrow_to(-1.4)), Create(col1[0]), Write(col1[1]))
        icons1 = VGroup()
        for i, (pix, colour, d) in enumerate(EDGES):
            marks = VGroup(*[cells[p].copy().set_fill(colour, 0.9) for p in pix])
            icon = Line(ORIGIN, d * 0.7, color=colour, stroke_width=10).move_to([-1.4, 1.8 - i * 0.85, 0])
            self.play(FadeIn(marks), run_time=0.4)
            self.play(TransformFromCopy(marks, icon), run_time=0.6)
            icons1.add(icon)
        self.wait(0.5)
        self.snap()

        # Layer 2: edges joined into shapes
        col2 = self.column("Layer 2: shapes", 1.9)
        self.play(GrowArrow(self.arrow_to(1.9)), Create(col2[0]), Write(col2[1]))
        bar = Line(LEFT * 0.9, RIGHT * 0.9, color=ORANGE_C, stroke_width=12).move_to([1.9, 1.0, 0])
        slant = Line(UR * 0.75, DL * 0.75, color=PURPLE_C, stroke_width=12).move_to([1.9, -1.0, 0])
        bar_label = Text("top bar", font_size=20).next_to(bar, DOWN, buff=0.15)
        slant_label = Text("slanted line", font_size=20).next_to(slant, DOWN, buff=0.15)
        self.play(TransformFromCopy(icons1[:2], bar), FadeIn(bar_label), run_time=1.2)
        self.play(TransformFromCopy(icons1[2:], slant), FadeIn(slant_label), run_time=1.2)
        self.wait(0.5)
        self.snap()

        # Output: shapes joined into a digit
        col3 = self.column("Output", 5.2)
        self.play(GrowArrow(self.arrow_to(5.2)), Create(col3[0]), Write(col3[1]))
        seven = Text("7", font_size=150, color=GREEN_C, weight=BOLD).move_to([5.2, 0.3, 0])
        verdict = Text("digit: 7", font_size=30, color=GREEN_C, weight=BOLD).move_to([5.2, -1.6, 0])
        self.play(TransformFromCopy(VGroup(bar, slant), seven), run_time=1.4)
        self.play(Write(verdict))
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
                     "output_file": "layers_digit", "disable_caching": True, "verbosity": "WARNING", "progress_bar": "none"}):
        scene = LayersDigit()
        scene.render()
    mp4 = HERE / "layers_digit.mp4"
    shutil.copy(next(media.rglob("layers_digit.mp4")), mp4)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(mp4), "-vf",
                    "fps=12,scale=720:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "layers_digit.gif")], check=True)
    key_frames_grid(scene.snaps, HERE / "layers_digit_frames.png")
    shutil.rmtree(media)

"""Batch vs online learning: one big block once vs mini-batches streaming in.
Run: python batch_vs_online.py  -> batch_vs_online.mp4, batch_vs_online.gif, batch_vs_online_frames.png"""
import shutil
import subprocess
from pathlib import Path

from manim import *
from PIL import Image

HERE = Path(__file__).parent
BLUE_C, ORANGE_C, GREEN_C, RED_C, GREY_C = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#6B6B6B"
Text.set_default(color=BLACK, font="Latin Modern Roman")


def model_box(y, colour):
    box = RoundedRectangle(width=2.6, height=1.5, corner_radius=0.15, color=colour, fill_color=colour,
                           fill_opacity=0.12, stroke_width=4).move_to([3.6, y, 0])
    label = Text("Model", font_size=30, weight=BOLD).move_to(box).shift(UP * 0.25)
    return box, label


def version(y, n, colour):
    return Text(f"version {n}", font_size=26, color=colour).move_to([3.6, y - 0.3, 0])


class BatchVsOnline(Scene):
    def snap(self):
        self.snaps.append(Image.fromarray(self.renderer.get_frame()))

    def construct(self):
        self.snaps = []
        top, bottom = 1.9, -1.9
        title_b = Text("Batch learning", font_size=32, weight=BOLD, color=BLUE_C).move_to([-5.0, top + 1.25, 0])
        title_o = Text("Online learning", font_size=32, weight=BOLD, color=GREEN_C).move_to([-4.95, bottom + 1.25, 0])
        divider = DashedLine([-7, 0, 0], [7, 0, 0], color=GREY_C, stroke_width=2)
        mb, lb = model_box(top, BLUE_C)
        mo, lo = model_box(bottom, GREEN_C)
        vb, vo = version(top, 0, BLUE_C), version(bottom, 0, GREEN_C)
        big = Rectangle(width=2.8, height=1.4, color=BLUE_C, fill_color=BLUE_C, fill_opacity=0.55).move_to([-3.2, top, 0])
        big_label = Text("all the data", font_size=24, color=WHITE, weight=BOLD).move_to(big)
        stream = VGroup(*[Square(0.45, color=GREEN_C, fill_color=GREEN_C, fill_opacity=0.6) for _ in range(5)])
        stream.arrange(RIGHT, buff=0.18).move_to([-3.6, bottom, 0])
        stream_label = Text("mini-batches", font_size=24, color=GREEN_C).next_to(stream, DOWN, buff=0.25)
        self.play(FadeIn(title_b), FadeIn(title_o), Create(divider), FadeIn(mb), FadeIn(lb), FadeIn(mo), FadeIn(lo),
                  FadeIn(vb), FadeIn(vo), FadeIn(big), FadeIn(big_label), FadeIn(stream), FadeIn(stream_label))
        self.wait(0.4)
        self.snap()

        # Batch: everything goes in once
        self.play(VGroup(big, big_label).animate.move_to(mb).scale(0.3).set_opacity(0), run_time=1.3)
        vb_new = version(top, 1, BLUE_C)
        self.play(Transform(vb, vb_new))
        frozen = Text("then frozen", font_size=24, color=RED_C).next_to(mb, DOWN, buff=0.15)
        self.play(FadeIn(frozen))
        self.snap()

        # Online: one mini-batch at a time, the model updates after each; batch side just waits
        waiting = VGroup()
        for i in range(5):
            square = stream[4 - i]
            pile = Square(0.35, color=BLUE_C, fill_color=BLUE_C, fill_opacity=0.35).move_to([-4.6 + i * 0.45, top - 0.1, 0])
            self.play(square.animate.move_to(mo).scale(0.3).set_opacity(0), FadeIn(pile), run_time=0.6)
            waiting.add(pile)
            self.play(Transform(vo, version(bottom, i + 1, GREEN_C)), run_time=0.3)
            if i == 1:
                self.snap()
        wait_label = Text("new data waits for the next retrain", font_size=22, color=BLUE_C).next_to(waiting, DOWN, buff=0.2)
        keeps = Text("keeps learning", font_size=24, color=GREEN_C).next_to(mo, DOWN, buff=0.15)
        self.play(FadeIn(wait_label), FadeIn(keeps), FadeOut(stream_label))
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
                     "output_file": "batch_vs_online", "disable_caching": True, "verbosity": "WARNING",
                     "progress_bar": "none"}):
        scene = BatchVsOnline()
        scene.render()
    mp4 = HERE / "batch_vs_online.mp4"
    shutil.copy(next(media.rglob("batch_vs_online.mp4")), mp4)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(mp4), "-vf",
                    "fps=12,scale=720:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "batch_vs_online.gif")], check=True)
    key_frames_grid(scene.snaps, HERE / "batch_vs_online_frames.png")
    shutil.rmtree(media)

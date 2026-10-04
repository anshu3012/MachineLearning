"""The story of section 4 read event by event. The short-term lane shows what is happening now; the input gate copies
what matters up to the long-term lane (the cell state) and the forget gate removes what stopped mattering.
Events and memory contents are the rows of the Note's table. Two-path picture after Olah (2015).
Run: python two_memories.py  -> two_memories.gif, two_memories_frames.png (Manim + ffmpeg)"""
import shutil
import subprocess
from pathlib import Path

from manim import *
from PIL import Image

HERE = Path(__file__).parent
BLUE_C, GREEN_C, RED_C, ORANGE_C, GREY_C = "#4C78A8", "#54A24B", "#E45756", "#F58518", "#6B6B6B"
Text.set_default(color=BLACK, font="Latin Modern Roman")
LONG_Y, SHORT_Y = 1.0, -1.9
# (what the story says, "add"/"remove", memory item) -- the table of section 4
EVENTS = [("a thousand-year-old story", "add", "old story"),
          ("in Pratapgarh", "add", "Pratapgarh"),
          ("a great king, Vikram", "add", "Vikram (hero?)"),
          ("XYZ attacks", "add", "XYZ (villain)"),
          ("Vikram dies", "remove", "Vikram (hero?)"),
          ("Vikram Junior becomes king", "add", "Vikram Junior"),
          ("Vikram Junior is killed", "remove", "Vikram Junior"),
          ("Vikram Super Junior kills XYZ", "add", "Vikram Super Junior")]


def chip(label):
    t = Text(label, font_size=30)
    box = RoundedRectangle(corner_radius=0.15, width=t.width + 0.4, height=0.75, stroke_color=GREEN_C,
                           stroke_width=3, fill_color=ManimColor(GREEN_C).interpolate(WHITE, 0.8), fill_opacity=1)
    return VGroup(box, t.move_to(box))


def lane(y, colour, label):
    band = Rectangle(width=13.6, height=1.3, stroke_width=0, fill_color=ManimColor(colour).interpolate(WHITE, 0.88),
                     fill_opacity=1).move_to([0, y, 0])
    line = Arrow([-6.8, y - 0.65, 0], [6.8, y - 0.65, 0], buff=0, color=colour, stroke_width=6)
    name = Text(label, font_size=26, color=colour).next_to(band, UP, buff=0.08).align_to(band, LEFT)
    return VGroup(band, line, name)


class TwoMemories(Scene):
    def snap(self):
        self.snaps.append(Image.fromarray(self.renderer.get_frame()))

    def construct(self):
        self.snaps = []
        self.add(lane(LONG_Y, GREEN_C, "long-term memory (cell state)"),
                 lane(SHORT_Y, RED_C, "short-term memory: what happens now"))
        title = Text("Reading the story, one event at a time", font_size=34).to_edge(UP, buff=0.3)
        self.play(FadeIn(title))
        chips, now = {}, None
        for n, (said, action, item) in enumerate(EVENTS, start=1):
            new_now = Text(f"{n}. {said}", font_size=34, color=RED_C).move_to([0, SHORT_Y, 0])
            self.play(*([FadeOut(now)] if now else []), FadeIn(new_now, shift=LEFT * 0.5), run_time=0.7)
            now = new_now
            if action == "add":
                gate = Text("input gate: add", font_size=28, color=BLUE_C)
                c = chip(item).move_to([0, SHORT_Y, 0])
                target = VGroup(*[m.copy() for m in chips.values()], c.copy()).arrange(RIGHT, buff=0.3).move_to([0, LONG_Y, 0])
                gate.move_to([0, LONG_Y - 1.25, 0])
                self.play(FadeIn(gate), *[m.animate.move_to(t) for m, t in zip(chips.values(), target)],
                          run_time=0.6)
                self.play(c.animate.move_to(target[-1]), run_time=0.9)
                chips[item] = c
            else:
                gate = Text("forget gate: remove", font_size=28, color=RED_C)
                gate.move_to([0, LONG_Y - 1.25, 0])
                c = chips.pop(item)
                cross = Cross(c, stroke_color=RED_C, stroke_width=8)
                self.play(FadeIn(gate), Create(cross), run_time=0.7)
                self.play(FadeOut(c, shift=UP * 0.4), FadeOut(cross), run_time=0.6)
                rest = VGroup(*chips.values())
                self.play(rest.animate.arrange(RIGHT, buff=0.3).move_to([0, LONG_Y, 0]), run_time=0.5)
            self.wait(0.6)
            if n in (4, 5, 8):
                self.snap()
            self.play(FadeOut(gate), run_time=0.3)
        ask = Text("good or bad story?", font_size=34, color=RED_C).move_to([0, SHORT_Y, 0])
        gate = Text("output gate: answer from the long-term memory", font_size=28, color=ORANGE_C)
        gate.move_to([0, LONG_Y - 1.25, 0])
        frame = SurroundingRectangle(VGroup(*chips.values()), color=ORANGE_C, buff=0.2, stroke_width=6)
        self.play(FadeOut(now), FadeIn(ask), run_time=0.6)
        self.play(FadeIn(gate), Create(frame), run_time=0.9)
        self.wait(2.5)
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
                     "output_file": "two_memories", "disable_caching": True, "verbosity": "WARNING",
                     "progress_bar": "none"}):
        scene = TwoMemories()
        scene.render()
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(next(media.rglob("two_memories.mp4"))), "-vf",
                    "fps=10,scale=720:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "two_memories.gif")], check=True)
    key_frames_grid(scene.snaps, HERE / "two_memories_frames.png")
    shutil.rmtree(media)

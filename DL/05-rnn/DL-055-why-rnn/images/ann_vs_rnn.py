"""Section 6, animated, on the Note's reviews. Part 1: an ANN gives each position its own weights, so the word "bad"
meets different weights when the review shifts by one place. Part 2: an RNN reads one word at a time through one
set of weights and passes a memory on; a 5-word and a 3-word review use the same cell, with no padding.
The memory is drawn as the words read so far, older ones fainter: a picture of the idea, not computed numbers.
Run: python ann_vs_rnn.py  -> ann_vs_rnn.gif, ann_vs_rnn_frames.png (Manim)"""
import shutil
import subprocess
from pathlib import Path

from manim import *
from PIL import Image

HERE = Path(__file__).parent
BLUE_C, ORANGE_C, GREEN_C, RED_C, PURPLE_C, GREY_C = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#B279A2", "#6B6B6B"
SLOT_COLOURS = ("#4C78A8", "#F58518", "#54A24B", "#B279A2", "#9D755D")
Text.set_default(color=BLACK, font="Latin Modern Roman")
MarkupText.set_default(color=BLACK, font="Latin Modern Roman")
XS = [-4.8 + 2.4 * i for i in range(5)]


def word_chip(w, colour=BLUE_C):
    t = Text(w, font_size=30, color=colour if w != "pad" else GREY_C)
    box = RoundedRectangle(corner_radius=0.1, width=max(1.6, t.width + 0.3), height=0.7, stroke_color=colour,
                           stroke_width=2, fill_color=WHITE, fill_opacity=1)
    return VGroup(box, t.move_to(box))


class AnnVsRnn(Scene):
    def snap(self):
        self.snaps.append(Image.fromarray(self.renderer.get_frame()))

    def construct(self):
        self.snaps = []
        # Part 1: the ANN, one weight block per position
        title = Text("An ANN: its own weights for every position", font_size=36).to_edge(UP, buff=0.35)
        slots = VGroup()
        for i, (x, c) in enumerate(zip(XS, SLOT_COLOURS)):
            b = Rectangle(width=1.9, height=1.0, stroke_color=c, stroke_width=4,
                          fill_color=ManimColor(c).interpolate(WHITE, 0.8), fill_opacity=1).move_to([x, 0.9, 0])
            slots.add(VGroup(b, MarkupText(f"W<sub>{i + 1}</sub>", font_size=32, color=c).move_to(b)))
        pos = VGroup(*[Text(f"position {i + 1}", font_size=22, color=GREY_C).next_to(s, UP, buff=0.12)
                       for i, s in enumerate(slots)])
        self.play(FadeIn(title), FadeIn(slots), FadeIn(pos))
        words = ["food", "tasted", "bad", "pad", "pad"]
        chips = VGroup(*[word_chip(w).move_to([x, -1.0, 0]) for w, x in zip(words, XS)])
        ups = VGroup(*[Arrow([x, -0.6, 0], [x, 0.35, 0], buff=0.05, color=GREY_C, stroke_width=4) for x in XS])
        self.play(FadeIn(chips, shift=UP * 0.3), GrowFromEdge(ups, DOWN), run_time=1.0)
        hit = SurroundingRectangle(VGroup(chips[2], slots[2]), color=RED_C, buff=0.12, stroke_width=5)
        say = Text('"bad" is read by W3', font_size=30, color=RED_C).to_edge(DOWN, buff=0.5)
        self.play(Create(hit), FadeIn(say))
        self.wait(1.2)
        self.snap()
        shifted = ["pad", "food", "tasted", "bad", "pad"]
        new = VGroup(*[word_chip(w).move_to([x, -1.0, 0]) for w, x in zip(shifted, XS)])
        hit2 = SurroundingRectangle(VGroup(new[3], slots[3]), color=RED_C, buff=0.12, stroke_width=5)
        say2 = Text('shifted one place: now "bad" meets W4, other weights', font_size=30,
                    color=RED_C).to_edge(DOWN, buff=0.5)
        self.play(FadeOut(hit), Transform(chips, new), run_time=1.0)
        self.play(Create(hit2), Transform(say, say2))
        self.wait(1.8)
        self.snap()
        self.play(FadeOut(VGroup(title, slots, pos, chips, ups, hit2, say)))

        # Part 2: the RNN, one cell reused, a memory passed on
        title = Text("An RNN: one set of weights, used at every step", font_size=36).to_edge(UP, buff=0.35)
        cell = RoundedRectangle(corner_radius=0.2, width=2.6, height=1.4, stroke_color=PURPLE_C, stroke_width=4,
                                fill_color=ManimColor(PURPLE_C).interpolate(WHITE, 0.85), fill_opacity=1).move_to([-2.2, 0.6, 0])
        cell_lbl = VGroup(Text("RNN cell", font_size=30), Text("same weights", font_size=22, color=GREY_C)
                          ).arrange(DOWN, buff=0.08).move_to(cell)
        mem = Rectangle(width=2.8, height=3.3, stroke_color=RED_C, stroke_width=4).move_to([2.8, 0.6, 0])
        mem_lbl = Text("memory", font_size=28, color=RED_C).next_to(mem, UP, buff=0.12)
        to_mem = Arrow(cell.get_right(), mem.get_left() + UP * 0.5, buff=0.08, color=RED_C, stroke_width=5)
        back = CurvedArrow(mem.get_left() + DOWN * 0.7, cell.get_right() + DOWN * 0.45, angle=-1.2, color=RED_C,
                           stroke_width=5)
        self.play(FadeIn(title), FadeIn(cell), FadeIn(cell_lbl), Create(mem), FadeIn(mem_lbl),
                  GrowArrow(to_mem), Create(back))
        for review, snap_at in ((["this", "movie", "was", "really", "good"], 2), (["food", "tasted", "bad"], 2)):
            row = VGroup(*[word_chip(w) for w in review]).arrange(RIGHT, buff=0.25).move_to([0, -2.4, 0])
            step = Text(f"{len(review)} words: {len(review)} steps, no padding", font_size=26, color=GREY_C
                        ).next_to(row, DOWN, buff=0.25)
            self.play(FadeIn(row), FadeIn(step))
            held = VGroup()
            for t, chip in enumerate(row):
                moving = chip.copy()
                self.play(chip.animate.set_opacity(0.25), moving.animate.move_to(cell.get_bottom() + DOWN * 0.45),
                          run_time=0.6)
                self.play(FadeOut(moving, shift=UP * 0.5), Indicate(cell, color=PURPLE_C, scale_factor=1.05),
                          run_time=0.5)
                held.add(Text(review[t], font_size=32, color=BLUE_C))
                for age, w in enumerate(reversed(held)):                        # older words fade
                    w.set_opacity(max(1 - 0.22 * age, 0.2))
                n = len(held)                                                   # fixed rows, 0.58 apart
                ys = [mem.get_center()[1] + 0.58 * ((n - 1) / 2 - i) for i in range(n)]
                self.play(*[m.animate.move_to([mem.get_center()[0], y, 0]).set_opacity(m.get_fill_opacity())
                            for m, y in zip(held[:-1], ys[:-1])],
                          FadeIn(held[-1].move_to([mem.get_center()[0], ys[-1], 0]), shift=RIGHT * 0.3),
                          Indicate(back, color=RED_C),
                          run_time=0.6)
                if t == snap_at and len(review) == 5:
                    self.snap()
            self.wait(1.2)
            if len(review) == 5:
                self.play(FadeOut(row), FadeOut(step), FadeOut(held))
        end = Text("same cell for 5 words and for 3; the memory carries what was read", font_size=28,
                   color=PURPLE_C).to_edge(DOWN, buff=0.15)
        self.play(FadeOut(step), FadeIn(end))
        self.wait(2.0)
        self.snap()


def key_frames_grid(frames, out, gap=16):
    w, h = frames[0].size
    sheet = Image.new("RGB", (2 * w + gap, 2 * h + gap), "white")
    for i, f in enumerate(frames[:4]):
        sheet.paste(f.convert("RGB"), ((i % 2) * (w + gap), (i // 2) * (h + gap)))
    sheet.save(out)


if __name__ == "__main__":
    media = HERE / ".manim_ann_vs_rnn"
    with tempconfig({"quality": "medium_quality", "background_color": WHITE, "media_dir": str(media),
                     "output_file": "ann_vs_rnn", "disable_caching": True, "verbosity": "WARNING",
                     "progress_bar": "none"}):
        scene = AnnVsRnn()
        scene.render()
    mp4 = next(media.rglob("ann_vs_rnn.mp4"))
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(mp4), "-vf",
                    "fps=10,scale=720:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "ann_vs_rnn.gif")], check=True)
    key_frames_grid(scene.snaps, HERE / "ann_vs_rnn_frames.png")
    shutil.rmtree(media)

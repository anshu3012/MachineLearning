"""Section 8: each sine-cosine pair of the positional encoding as a clock hand. The point (sin wp, cos wp) starts at
12 o'clock for position 0 and turns clockwise as the position p grows; each pair turns 10 times slower than the
one before (d_model = 8: angle rates 1, 0.1, 0.01, 0.001). Moving k = 10 positions turns every hand by the same
angle w k whether we start at position 10 or at position 30: one fixed rotation, the matrix M_10.
Values straight from the formula of Vaswani et al. (2017, section 3.5). Our own design.
Run: python pe_clocks.py -> pe_clocks.gif, pe_clocks_frames.png (Manim)"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
from manim import *
from PIL import Image
import manimpango

for f in Path("/usr/share/texmf/fonts/opentype/public/lm").glob("lmroman10-*.otf"):   # pango on topgro misses LM
    manimpango.register_font(str(f))

HERE = Path(__file__).parent
BLUE_C, ORANGE_C, GREEN_C, RED_C, PURPLE_C, GREY_C = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#B279A2", "#6B6B6B"
Text.set_default(color=BLACK, font="Latin Modern Roman")
D_MODEL, K = 8, 10
RATES = [1 / 10000 ** (2 * i / D_MODEL) for i in range(D_MODEL // 2)]          # 1, 0.1, 0.01, 0.001
COLS = [BLUE_C, ORANGE_C, GREEN_C, PURPLE_C]
CENTRES = [np.array([x, 0.35, 0]) for x in (-5.1, -1.7, 1.7, 5.1)]
R = 1.25
TURN = ["10 rad: 1.6 turns", "1 rad = 57.3°", "0.1 rad = 5.7°", "0.01 rad = 0.6°"]


def tip(c, w, p, r=R):
    return CENTRES[c] + r * np.array([np.sin(w * p), np.cos(w * p), 0])


def hand(c, w, p, colour, width=7):
    return VGroup(Line(CENTRES[c], tip(c, w, p), color=colour, stroke_width=width),
                  Dot(tip(c, w, p), color=colour, radius=0.09))


class PEClocks(Scene):
    def snap(self):
        self.snaps.append(Image.fromarray(self.renderer.get_frame()))

    def construct(self):
        self.snaps = []
        title = Text("Each sine-cosine pair is a clock hand", font_size=36, weight=BOLD).to_edge(UP, buff=0.25)
        faces = VGroup()
        for c, (w, col) in enumerate(zip(RATES, COLS)):
            circle = Circle(radius=R, color=GREY_C, stroke_width=3).move_to(CENTRES[c])
            noon = Line(CENTRES[c] + UP * R * 0.88, CENTRES[c] + UP * R * 1.08, color=GREY_C, stroke_width=4)
            name = Text(f"dimensions {2 * c}, {2 * c + 1}", font_size=25, color=col)
            rate = Text(f"angle = {w:g} × p", font_size=24, color=GREY_C)
            VGroup(name, rate).arrange(DOWN, buff=0.08).next_to(circle, UP, buff=0.22)
            faces.add(circle, noon, name, rate)
        p = ValueTracker(0)
        hands = VGroup(*[always_redraw(lambda c=c, w=w, col=col: hand(c, w, p.get_value(), col))
                         for c, (w, col) in enumerate(zip(RATES, COLS))])
        counter = always_redraw(lambda: Text(f"position p = {p.get_value():.0f}", font_size=32)
                                .move_to([0, -1.75, 0]))
        caption = Text("the hand's tip is (sin, cos): 12 o'clock at position 0, then clockwise", font_size=26,
                       color=GREY_C).move_to([0, -2.45, 0])
        self.play(FadeIn(title), FadeIn(faces))
        self.add(hands, counter)
        self.play(FadeIn(caption))
        self.wait(0.8)
        self.play(p.animate.set_value(10), run_time=4, rate_func=linear)
        cap2 = Text("each pair turns 10 times slower than the one before", font_size=26, color=GREY_C).move_to(caption)
        self.play(FadeOut(caption), FadeIn(cap2))
        self.wait(1.2)
        self.snap()

        turn_labels = VGroup(*[Text("+ " + t, font_size=24, color=col).next_to(Circle(radius=R).move_to(CENTRES[c]),
                                                                              DOWN, buff=0.15)
                               for c, (t, col) in enumerate(zip(TURN, COLS))])
        counter_y = -2.6
        for n, start in enumerate((10, 30)):
            if n == 1:
                self.play(FadeOut(ghosts), FadeOut(arcs), FadeOut(cap), run_time=0.5)
                self.play(p.animate.set_value(start), run_time=2, rate_func=linear)
            ghosts = VGroup(*[hand(c, w, start, GREY_C, 4) for c, w in enumerate(RATES)])
            cap = Text(f"move k = {K} positions: from {start} to {start + K}", font_size=28).move_to([0, counter_y, 0])
            if n == 0:
                self.play(FadeOut(cap2), counter.animate.shift(UP * 0), FadeIn(ghosts), FadeIn(cap))
                counter.clear_updaters()
                self.remove(counter)
                counter = always_redraw(lambda: Text(f"position p = {p.get_value():.0f}", font_size=30)
                                        .move_to([0, -3.3, 0]))
                self.add(counter)
            else:
                self.play(FadeIn(ghosts), FadeIn(cap))
            self.play(p.animate.set_value(start + K), run_time=3, rate_func=linear)
            arcs = VGroup(*[Arc(radius=R * 0.55, start_angle=PI / 2 - w * start, angle=-w * K, arc_center=CENTRES[c],
                                color=col, stroke_width=6) for c, (w, col) in enumerate(zip(RATES, COLS)) if c in (1, 2)])
            if n == 0:
                self.play(Create(arcs), FadeIn(turn_labels))
            else:
                self.play(Create(arcs), Indicate(turn_labels, color=BLACK, scale_factor=1.08))
            self.wait(1.5)
            self.snap()
        final = Text("the same turn from any start: one fixed rotation", font_size=28, weight=BOLD)
        final.move_to([0, counter_y, 0])
        self.play(FadeOut(cap), FadeIn(final))
        self.wait(3)
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
                     "output_file": "pe_clocks", "disable_caching": True, "verbosity": "WARNING",
                     "progress_bar": "none"}):
        scene = PEClocks()
        scene.render()
    mp4 = next(media.rglob("pe_clocks.mp4"))
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(mp4), "-vf",
                    "fps=12,scale=720:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "pe_clocks.gif")], check=True)
    key_frames_grid(scene.snaps, HERE / "pe_clocks_frames.png")
    shutil.rmtree(media)

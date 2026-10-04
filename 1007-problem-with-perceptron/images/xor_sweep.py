"""XOR's four observations. A line turns through every direction (0 to 340 degrees); at each direction it takes its
best position. The best is always 3 of 4: one corner stays on the wrong side. Then two lines (two hidden nodes,
x1 + x2 = 0.5 and x1 + x2 = 1.5) put the two 1s between them: 4 of 4.
Run: python xor_sweep.py  -> xor_sweep.gif, xor_sweep_frames.png"""
import glob
import shutil
import subprocess
from pathlib import Path

import manimpango
import numpy as np
from manim import *
from PIL import Image

HERE = Path(__file__).parent
# topgro: ~/.fonts links are broken, so register the TeX copy of Latin Modern for Pango
for f in glob.glob("/usr/share/texmf/fonts/opentype/public/lm/lmroman*.otf"):
    manimpango.register_font(f)
BLUE_C, ORANGE_C, GREEN_C, RED_C, PURPLE_C, GREY_C = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#B279A2", "#6B6B6B"
Text.set_default(color=BLACK, font="Latin Modern Roman")
MarkupText.set_default(color=BLACK, font="Latin Modern Roman")

PTS = np.array([[0, 0], [0, 1], [1, 0], [1, 1]], float)
LAB = np.array([0, 1, 1, 0])                       # the XOR column
LO, HI = -0.5, 1.5
BOX = np.array([[LO, LO], [HI, LO], [HI, HI], [LO, HI]])


def best_cut(theta):
    """Best threshold c for the line n.x = c (class 1 where n.x > c); ties -> the one nearest the square's centre."""
    n = np.array([np.cos(theta), np.sin(theta)])
    proj = np.round(PTS @ n, 9)               # exact ties stay ties (e.g. 0 degrees)
    p = np.sort(proj)
    cands = np.r_[p[0] - 0.3, (p[1:] + p[:-1]) / 2, p[-1] + 0.3]
    scores = [((proj > c).astype(int) == LAB).sum() for c in cands]
    best = [c for c, s in zip(cands, scores) if s == max(scores)]
    c = min(best, key=lambda c: abs(c - n @ [0.5, 0.5]))
    return n, c, max(scores), (proj > c).astype(int) != LAB


def clip(poly, n, c):
    """Part of a convex polygon where n.x >= c (Sutherland-Hodgman, one edge)."""
    out = []
    for a, b in zip(poly, np.roll(poly, -1, axis=0)):
        da, db = a @ n - c, b @ n - c
        if da >= 0:
            out.append(a)
        if da * db < 0:
            out.append(a + (b - a) * da / (da - db))
    return np.array(out)


class XORSweep(Scene):
    def snap(self):
        self.snaps.append(Image.fromarray(self.renderer.get_frame()))

    def construct(self):
        self.snaps = []
        ax = Axes(x_range=[LO, HI, 1], y_range=[LO, HI, 1], x_length=5.4, y_length=5.4, tips=False,
                  axis_config={"color": GREY_C, "stroke_width": 2}).move_to([-2.6, -0.35, 0])
        xl = MarkupText("x<sub>1</sub>", font_size=32, color=GREY_C).next_to(ax.c2p(HI, LO), DOWN, buff=0.15)
        yl = MarkupText("x<sub>2</sub>", font_size=32, color=GREY_C).next_to(ax.c2p(LO, HI), LEFT, buff=0.15)
        dots = VGroup(*[Dot(ax.c2p(*p), radius=0.2, color=GREEN_C if l else RED_C) for p, l in zip(PTS, LAB)])
        vals = VGroup(*[Text(str(l), font_size=30, color=WHITE).move_to(d) for d, l in zip(dots, LAB)])
        title = Text("XOR: can one line split the 1s from the 0s?", font_size=36).to_edge(UP, buff=0.25)
        self.play(FadeIn(title), Create(ax), FadeIn(xl), FadeIn(yl), FadeIn(dots), FadeIn(vals), run_time=1.0)

        theta = ValueTracker(0.0)

        def drawing():
            n, c, score, wrong = best_cut(theta.get_value())
            pos = clip(BOX, n, c)
            region = Polygon(*[ax.c2p(*q) for q in pos], stroke_width=0, fill_color=GREEN_C, fill_opacity=0.18)
            rings = VGroup(*[Circle(0.34, color=BLACK, stroke_width=5).move_to(ax.c2p(*PTS[i]))
                             for i in np.where(wrong)[0]])
            return VGroup(region, rings)

        def line_only():
            n, c, _, _ = best_cut(theta.get_value())
            d = np.array([-n[1], n[0]])
            ts = [t for t in np.linspace(-3, 3, 601) if np.all(np.abs(n * c + t * d - 0.5) <= 1)]  # inside the box
            a, b = n * c + ts[0] * d, n * c + ts[-1] * d
            return Line(ax.c2p(*a), ax.c2p(*b), color=BLACK, stroke_width=5)

        region = always_redraw(lambda: drawing()[0])
        rings = always_redraw(lambda: drawing()[1])
        line = always_redraw(line_only)
        score = always_redraw(lambda: Text(f"best position: {best_cut(theta.get_value())[2]} of 4 right",
                                           font_size=34, color=BLUE_C).move_to([3.6, 1.2, 0]))
        angle = always_redraw(lambda: Text(f"angle {np.degrees(theta.get_value()) % 360:.0f}°", font_size=34,
                                           color=GREY_C).move_to([3.6, 0.3, 0]))
        key = VGroup(Text("green side: predict 1", font_size=28, color=GREEN_C),
                     Text("black ring: wrong", font_size=28)).arrange(DOWN, buff=0.15).move_to([3.6, -1.2, 0])
        self.add(region)
        self.bring_to_back(region)
        self.add(line, rings, score, angle)
        self.play(FadeIn(key), run_time=0.5)
        for stop, snap in [(np.radians(20), True), (np.radians(110), True), (np.radians(340), False)]:
            self.play(theta.animate.set_value(stop), run_time=2.5 * (stop - theta.get_value()) / np.radians(90),
                      rate_func=linear)
            if snap:
                self.wait(0.4)
                self.snap()
        never = Text("at best 3 of 4, never 4", font_size=34, color=RED_C).move_to([3.6, -2.5, 0])
        self.play(FadeIn(never))
        self.wait(1.5)
        self.snap()

        # two lines = two hidden nodes
        for m in (region, line, rings, score, angle):
            m.clear_updaters()
        title2 = Text("Two lines (two hidden nodes) split XOR", font_size=36).to_edge(UP, buff=0.25)
        la = Line(ax.c2p(-0.5, 1.0), ax.c2p(1.0, -0.5), color=PURPLE_C, stroke_width=5)
        lb = Line(ax.c2p(0.0, 1.5), ax.c2p(1.5, 0.0), color=ORANGE_C, stroke_width=5)
        band = Polygon(ax.c2p(-0.5, 1.0), ax.c2p(1.0, -0.5), ax.c2p(1.5, -0.5), ax.c2p(1.5, 0.0), ax.c2p(0.0, 1.5),
                       ax.c2p(-0.5, 1.5), stroke_width=0, fill_color=GREEN_C, fill_opacity=0.18)
        lab_a = MarkupText("x<sub>1</sub> + x<sub>2</sub> = 0.5", font_size=30, color=PURPLE_C).move_to([3.6, 1.2, 0])
        lab_b = MarkupText("x<sub>1</sub> + x<sub>2</sub> = 1.5", font_size=30, color=ORANGE_C).move_to([3.6, 0.4, 0])
        rule = Text("1 between the lines", font_size=30, color=GREEN_C).move_to([3.6, -0.6, 0])
        win = Text("4 of 4 right", font_size=34, color=GREEN_C).move_to([3.6, -1.6, 0])
        self.play(FadeOut(region), FadeOut(line), FadeOut(rings), FadeOut(score), FadeOut(angle), FadeOut(key),
                  FadeOut(never), FadeOut(title), FadeIn(title2), run_time=0.8)
        self.play(Create(la), FadeIn(lab_a), run_time=0.8)
        self.play(Create(lb), FadeIn(lab_b), run_time=0.8)
        self.add(band)
        self.bring_to_back(band)
        self.play(FadeIn(band), FadeIn(rule), run_time=0.8)
        self.play(FadeIn(win), Indicate(dots, color=None, scale_factor=1.15), run_time=0.8)
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
                     "output_file": "xor_sweep", "disable_caching": True, "verbosity": "WARNING",
                     "progress_bar": "none"}):
        scene = XORSweep()
        scene.render()
    mp4 = next(media.rglob("xor_sweep.mp4"))
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(mp4), "-vf",
                    "fps=12,scale=720:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "xor_sweep.gif")], check=True)
    key_frames_grid(scene.snaps, HERE / "xor_sweep_frames.png")
    shutil.rmtree(media)

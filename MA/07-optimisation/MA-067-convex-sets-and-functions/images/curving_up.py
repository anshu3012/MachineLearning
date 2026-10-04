"""Curving up means the slope keeps increasing (idea after Khan Academy, "Concavity introduction"; our own code, on the
Note's function q(w) = w^2 (w - 1)^2). Three stacked graphs share one moving cursor: q with its tangent line, the
slope q'(w), and the second derivative q''(w). Green background where q'' >= 0 (q curves up, convex there), red
where q'' < 0 (q curves down). At the end the three flat-tangent points are labelled by the second derivative test.
Run: python curving_up.py  -> curving_up.mp4, .gif, _frames.png"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
from manim import *
from PIL import Image

HERE = Path(__file__).parent
BLUE_C, PURPLE_C, ORANGE_C, GREEN_BG, RED_BG, GREY_C = "#4C78A8", "#B279A2", "#F58518", "#54A24B", "#E45756", "#6B6B6B"
Text.set_default(color=BLACK, font="Latin Modern Roman")
q = lambda w: w ** 2 * (w - 1) ** 2
dq = lambda w: 2 * w * (w - 1) * (2 * w - 1)
d2q = lambda w: 12 * w ** 2 - 12 * w + 2
W0, W1 = -0.3, 1.3
R1, R2 = 0.5 - np.sqrt(1 / 12), 0.5 + np.sqrt(1 / 12)          # where q'' = 0


def boxed(mob, buff=0.08):
    return VGroup(BackgroundRectangle(mob, color=WHITE, fill_opacity=0.92, buff=buff), mob)


class CurvingUp(Scene):
    def snap(self):
        self.snaps.append(Image.fromarray(self.renderer.get_frame()))

    def construct(self):
        self.snaps = []
        cfg = dict(x_range=[W0, W1, 0.5], x_length=7.0, axis_config={"color": GREY_C, "include_ticks": False})
        ax_f = Axes(y_range=[-0.02, 0.16, 0.1], y_length=2.0, **cfg).move_to([-2.0, 2.35, 0])
        ax_d = Axes(y_range=[-1.3, 1.3, 1], y_length=2.0, **cfg).move_to([-2.0, 0.0, 0])
        ax_s = Axes(y_range=[-1.5, 7, 2], y_length=2.0, **cfg).move_to([-2.0, -2.4, 0])
        bands = VGroup()
        for a, b, col in [(W0, R1, GREEN_BG), (R1, R2, RED_BG), (R2, W1, GREEN_BG)]:
            for ax, lo, hi in [(ax_f, -0.02, 0.16), (ax_d, -1.3, 1.3), (ax_s, -1.5, 7)]:
                p0, p1 = ax.c2p(a, lo), ax.c2p(b, hi)
                bands.add(Rectangle(width=p1[0] - p0[0], height=p1[1] - p0[1], stroke_width=0, fill_color=col,
                                    fill_opacity=0.13).move_to((p0 + p1) / 2))
        g_f = ax_f.plot(q, x_range=[W0, W1], color=BLUE_C, stroke_width=5)
        g_d = ax_d.plot(dq, x_range=[W0, W1], color=PURPLE_C, stroke_width=5)
        g_s = ax_s.plot(d2q, x_range=[W0, W1], color=ORANGE_C, stroke_width=5)
        zero = VGroup(DashedLine(ax_d.c2p(W0, 0), ax_d.c2p(W1, 0), color=GREY_C, stroke_width=2),
                      DashedLine(ax_s.c2p(W0, 0), ax_s.c2p(W1, 0), color=GREY_C, stroke_width=2))
        labs = VGroup(Text("q(w)", font_size=32, color=BLUE_C).next_to(ax_f, LEFT, buff=0.15),
                      Text("q′(w)", font_size=32, color=PURPLE_C).next_to(ax_d, LEFT, buff=0.15),
                      Text("q″(w)", font_size=32, color=ORANGE_C).next_to(ax_s, LEFT, buff=0.15))
        self.add(bands, zero, g_f, g_d, g_s, labs)
        w = ValueTracker(W0 + 0.02)

        def moving():
            x = w.get_value()
            out = VGroup()
            for ax, fn in [(ax_f, q), (ax_d, dq), (ax_s, d2q)]:
                out.add(Dot(ax.c2p(x, fn(x)), color=BLACK, radius=0.07))
            out.add(DashedLine(ax_f.c2p(x, -0.02), ax_s.c2p(x, -1.5), color=GREY_C, stroke_width=2))
            p, d = ax_f.c2p(x, q(x)), ax_f.c2p(x + 1, q(x) + dq(x)) - ax_f.c2p(x, q(x))
            d = 0.7 * d / np.linalg.norm(d)                  # the tangent drawn 1.8 screen units long
            out.add(Line(p - d, p + d, color=BLACK, stroke_width=4))
            up = d2q(x) >= 0
            txt = "q′ rising: convex here" if up else "q′ falling: concave here"
            out.add(boxed(VGroup(Text(f"w = {x:.2f}", font_size=30),
                                 Text(f"q′ = {dq(x):+.2f}", font_size=30, color=PURPLE_C),
                                 Text(f"q″ = {d2q(x):+.2f}", font_size=30, color=ORANGE_C),
                                 Text(txt, font_size=26, color=GREEN_BG if up else RED_BG)).arrange(
                DOWN, aligned_edge=LEFT, buff=0.14), 0.1).move_to([4.4, 0.3, 0]))
            return out

        self.add(always_redraw(moving))
        self.wait(0.8)
        self.snap()
        self.play(w.animate.set_value(0.5), run_time=4, rate_func=linear)
        self.wait(0.6)
        self.snap()
        self.play(w.animate.set_value(W1 - 0.02), run_time=4, rate_func=linear)
        self.wait(0.5)
        tests = VGroup()
        for c, word in [(0.0, "min"), (0.5, "max"), (1.0, "min")]:
            tests.add(boxed(Text(f"{word} (q″ = {d2q(c):.0f})", font_size=24), 0.04)
                      .next_to(ax_f.c2p(c, q(c)), UP, buff=0.15))
        self.play(FadeIn(tests))
        self.wait(2.5)
        self.snap()


def key_frames_grid(frames, out, gap=16):
    w, h = frames[0].size
    sheet = Image.new("RGB", (len(frames) * w + (len(frames) - 1) * gap, h), "white")
    for i, fr in enumerate(frames):
        sheet.paste(fr.convert("RGB"), (i * (w + gap), 0))
    sheet.save(out)


if __name__ == "__main__":
    assert abs(q(0.5) - 0.0625) < 1e-12 and d2q(0) == 2 and d2q(0.5) == -1 and d2q(1) == 2
    assert abs(d2q(R1)) < 1e-12 and abs(R1 - 0.211) < 1e-3 and abs(R2 - 0.789) < 1e-3
    name = "curving_up"
    media = HERE / ".manim"
    with tempconfig({"quality": "medium_quality", "background_color": WHITE, "media_dir": str(media),
                     "output_file": name, "disable_caching": True, "verbosity": "WARNING", "progress_bar": "none"}):
        scene = CurvingUp()
        scene.render()
    mp4 = HERE / f"{name}.mp4"
    shutil.copy(next(media.rglob(f"{name}.mp4")), mp4)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(mp4), "-vf",
                    "fps=10,scale=640:-1:flags=lanczos,split[a][b];[a]palettegen=max_colors=64:stats_mode=diff[p];"
                    "[b][p]paletteuse=dither=none", str(HERE / f"{name}.gif")], check=True)
    key_frames_grid([scene.snaps[1], scene.snaps[2]], HERE / f"{name}_frames.png")
    shutil.rmtree(media)

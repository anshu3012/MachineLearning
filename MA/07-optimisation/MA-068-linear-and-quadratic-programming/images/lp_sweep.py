"""The workshop linear program, animated: maximise 3 x1 + 2 x2 subject to x1 + x2 <= L (oven), x1 + 3 x2 <= 9 (flour),
x1 <= 3 (demand), x1, x2 >= 0. The profit line 3 x1 + 2 x2 = p slides outward; its feasible part (thick) shrinks
to one corner, (3, 1) with p = 11. Then one more oven hour (L = 5) moves the best corner to (3, 2), p = 13: the
oven's multiplier is 2.
Run: python lp_sweep.py  -> lp_sweep.mp4, .gif, _frames.png"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
from manim import *
from PIL import Image

HERE = Path(__file__).parent
BLUE_C, ORANGE_C, GREEN_C, RED_C, GREY_C = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#6B6B6B"
Text.set_default(color=BLACK, font="Latin Modern Roman")
C = np.array([3.0, 2.0])                              # profit per batch


def constraints(L):
    """Rows a, limits b of a x <= b."""
    return np.array([[1, 1], [1, 3], [1, 0], [-1, 0], [0, -1]], float), np.array([L, 9, 3, 0, 0], float)


def polygon(L):
    """Feasible polygon by clipping a big square with each half-plane (Sutherland-Hodgman)."""
    pts = [np.array(p, float) for p in ((-10, -10), (10, -10), (10, 10), (-10, 10))]
    for a, b in zip(*constraints(L)):
        out = []
        for i in range(len(pts)):
            p, q = pts[i], pts[(i + 1) % len(pts)]
            fp, fq = a @ p - b, a @ q - b
            if fp <= 0:
                out.append(p)
            if fp * fq < 0:
                out.append(p + (q - p) * fp / (fp - fq))
        pts = out
    return pts


def best(L):
    pts = polygon(L)
    i = int(np.argmax([C @ p for p in pts]))
    return pts[i], C @ pts[i]


def feasible_segment(p, L):
    """Part of the line 3 x1 + 2 x2 = p inside the region, or None."""
    x0, d = np.array([0.0, p / 2]), np.array([2.0, -3.0])
    lo, hi = -np.inf, np.inf
    for a, b in zip(*constraints(L)):
        ad, slack = a @ d, b - a @ x0
        if abs(ad) < 1e-12:
            if slack < -1e-9:
                return None
        elif ad > 0:
            hi = min(hi, slack / ad)
        else:
            lo = max(lo, slack / ad)
    return (x0 + lo * d, x0 + hi * d) if lo <= hi + 1e-9 else None


def boxed(mob, buff=0.08):
    return VGroup(BackgroundRectangle(mob, color=WHITE, fill_opacity=0.92, buff=buff), mob)


class LPSweep(Scene):
    def snap(self):
        self.snaps.append(Image.fromarray(self.renderer.get_frame()))

    def construct(self):
        self.snaps = []
        p, L = ValueTracker(2.0), ValueTracker(4.0)
        ax = Axes(x_range=[-0.3, 5.3, 1], y_range=[-0.3, 4.3, 1], x_length=6.72, y_length=5.52, tips=False,
                  axis_config={"color": GREY_C, "include_numbers": True, "font_size": 26,
                               "decimal_number_config": {"color": BLACK, "num_decimal_places": 0}})
        ax.to_edge(LEFT, buff=0.6).shift(DOWN * 0.2)
        xl = Tex("$x_1$ (A)", color=BLACK, font_size=32).next_to(ax.x_axis, DOWN, buff=0.35).align_to(ax.x_axis, RIGHT)
        yl = Tex("$x_2$ (B)", color=BLACK, font_size=32).next_to(ax.y_axis, UP, buff=0.1)
        region = always_redraw(lambda: Polygon(*[ax.c2p(*q) for q in polygon(L.get_value())], color=BLUE_C,
                                               stroke_width=3, fill_color=BLUE_C, fill_opacity=0.22))

        def profit_line():
            pv = p.get_value()
            # x range where the line stays inside the plot box, y in [-0.3, 4.3]
            x = np.clip(np.array([(pv - 2 * 4.3) / 3, (pv + 2 * 0.3) / 3]), -0.3, 5.3)
            y = (pv - 3 * x) / 2
            g = VGroup(DashedLine(ax.c2p(x[0], y[0]), ax.c2p(x[1], y[1]), color=ORANGE_C, stroke_width=3))
            seg = feasible_segment(pv, L.get_value())
            if seg is not None:
                a, b = seg
                if np.linalg.norm(a - b) > 0.03:
                    g.add(Line(ax.c2p(*a), ax.c2p(*b), color=ORANGE_C, stroke_width=10))
                else:
                    g.add(Dot(ax.c2p(*a), color=GREEN_C, radius=0.13))
            return g

        line = always_redraw(lambda: profit_line())
        readout = always_redraw(lambda: boxed(VGroup(
            MathTex(rf"\text{{profit }} 3x_1 + 2x_2 = {p.get_value():.1f}", color=ORANGE_C, font_size=38),
            MathTex(rf"\text{{oven: }} x_1 + x_2 \le {L.get_value():.0f}", color=BLUE_C, font_size=36),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2), 0.1).move_to([3.9, 2.6, 0]))
        self.add(ax, xl, yl, region, line, readout)
        self.wait(0.8)
        self.play(p.animate.set_value(6.0), run_time=1.5, rate_func=linear)
        self.wait(0.4)
        self.snap()                                   # p = 6: a long feasible segment
        self.play(p.animate.set_value(9.5), run_time=2.0, rate_func=linear)
        self.wait(0.4)
        self.snap()                                   # p = 9.5: the segment shrinks
        self.play(p.animate.set_value(11.0), run_time=1.5, rate_func=linear)
        msg = boxed(VGroup(Text("last touch: a corner", font_size=32, color=GREEN_C),
                           MathTex(r"(3, 1),\ \text{profit } 11", color=GREEN_C, font_size=40)).arrange(DOWN, buff=0.15), 0.1)
        msg.move_to([3.9, 0.6, 0])
        self.play(FadeIn(msg))
        self.wait(1.2)
        self.snap()                                   # p = 11 at (3, 1)
        self.play(FadeOut(msg))
        self.play(L.animate.set_value(5.0), p.animate.set_value(13.0), run_time=2.5)
        msg2 = boxed(VGroup(Text("one more oven hour:", font_size=30, color=BLUE_C),
                            MathTex(r"\text{best corner } (3, 2),\ \text{profit } 13", color=GREEN_C, font_size=36),
                            MathTex(r"13 - 11 = 2 = \lambda_{\text{oven}}", color=BLACK, font_size=38)).arrange(DOWN, buff=0.15), 0.1)
        msg2.move_to([3.9, 0.3, 0])
        self.play(FadeIn(msg2))
        self.wait(2.0)
        self.snap()


def key_frames_grid(frames, out, gap=16):
    w, h = frames[0].size
    sheet = Image.new("RGB", (2 * w + gap, 2 * h + gap), "white")
    for i, f in enumerate(frames[:4]):
        sheet.paste(f.convert("RGB"), ((i % 2) * (w + gap), (i // 2) * (h + gap)))
    sheet.save(out)


if __name__ == "__main__":
    x, v = best(4)                                    # the Note's answer and its oven shadow price
    assert np.allclose(x, [3, 1]) and abs(v - 11) < 1e-9
    x5, v5 = best(5)
    assert np.allclose(x5, [3, 2]) and abs(v5 - 13) < 1e-9
    a, b = feasible_segment(11, 4)
    assert np.allclose(a, b, atol=1e-9)               # the line p = 11 meets the region in one point
    name = "lp_sweep"
    media = HERE / ".manim"
    with tempconfig({"quality": "medium_quality", "background_color": WHITE, "media_dir": str(media),
                     "output_file": name, "disable_caching": True, "verbosity": "WARNING", "progress_bar": "none"}):
        scene = LPSweep()
        scene.render()
    mp4 = HERE / f"{name}.mp4"
    shutil.copy(next(media.rglob(f"{name}.mp4")), mp4)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(mp4), "-vf",
                    "fps=12,scale=720:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / f"{name}.gif")], check=True)
    key_frames_grid(scene.snaps, HERE / f"{name}_frames.png")
    shutil.rmtree(media)

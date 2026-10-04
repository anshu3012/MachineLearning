"""Why the gradient crosses contour lines at right angles (Manim). Zoom in on (1, 1) of f = x1^2 + x1 x2 + 2 x2^2 until
the contour lines f = 4 and f = 4.1 look straight and parallel. Of all steps that raise f by 0.1, the shortest goes
straight across, and that is the direction of the gradient [3, 5].
Idea after Khan Academy, "Gradient and contour maps"; our own function.
Run: python contour_zoom.py -> contour_zoom.mp4, .gif, _frames.png"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
from manim import *
from PIL import Image

HERE = Path(__file__).parent
BLUE_C, ORANGE_C, GREEN_C, GREY_C, PURPLE_C = "#4C78A8", "#F58518", "#54A24B", "#9A9A9A", "#B279A2"
Text.set_default(color=BLACK, font="Latin Modern Roman")
A = np.array([[1.0, 0.5], [0.5, 2.0]])              # f(x) = x^T A x
f = lambda p: float(p @ A @ p)
P = np.array([1.0, 1.0])
GRAD = 2 * A @ P                                    # [3, 5]
G = GRAD / np.linalg.norm(GRAD)
LAM, Q = np.linalg.eigh(A)
TT = np.linspace(0, 2 * np.pi, 9000)
CEN, R = np.array([-3.35, -0.1, 0.0]), 3.3          # screen centre and half-size of the map window
W0, W1 = 2.0, 0.03                                  # half-width of the window before and after the zoom


def to_screen(p, w):
    return CEN + np.array([(p[0] - P[0]) / w * R, (p[1] - P[1]) / w * R, 0.0])


def contour(c, w, colour, width):
    """The part of the contour line f = c inside the window, as line pieces."""
    pts = (Q @ (np.sqrt(c / LAM)[:, None] * np.vstack([np.cos(TT), np.sin(TT)]))).T
    inside = np.all(np.abs(pts - P) <= w, axis=1)
    out, run = VGroup(), []
    for p, ok in zip(pts, inside):
        if ok:
            run.append(to_screen(p, w))
        elif len(run) > 1:
            out.add(VMobject(color=colour, stroke_width=width).set_points_as_corners(run))
            run = []
        else:
            run = []
    if len(run) > 1:
        out.add(VMobject(color=colour, stroke_width=width).set_points_as_corners(run))
    return out


def reach(u):
    """Distance r along the unit vector u from P at which f has risen by 0.1 (exact, f is quadratic)."""
    a, b = float(u @ A @ u), float(GRAD @ u)
    return (-b + np.sqrt(b * b + 0.4 * a)) / (2 * a)


def rot(v, deg):
    t = np.radians(deg)
    return np.array([[np.cos(t), -np.sin(t)], [np.sin(t), np.cos(t)]]) @ v


def say(*lines, colour=BLACK):
    return VGroup(*[Tex(l, font_size=36, color=colour) for l in lines]).arrange(DOWN, aligned_edge=LEFT, buff=0.22)


class ContourZoom(Scene):
    def snap(self):
        self.snaps.append(Image.fromarray(self.renderer.get_frame()))

    def construct(self):
        self.snaps = []
        lw = ValueTracker(np.log(W0))
        w = lambda: float(np.exp(lw.get_value()))
        frame = Square(2 * R, color=GREY_C, stroke_width=2).move_to(CEN)
        levels = [0.5, 1, 2, 3, 5, 6.5, 8, 10]
        lines = always_redraw(lambda: VGroup(*[contour(c, w(), GREY_C, 2) for c in levels],
                                             contour(4.1, w(), PURPLE_C, 5), contour(4.0, w(), BLUE_C, 5)))
        dot = Dot(CEN, color=BLACK, radius=0.1)
        tx = np.array([0.45, 0, 0])
        head = say(r"Contour lines of", r"$f = x_1^2 + x_1 x_2 + 2x_2^2$").move_to(tx + UP * 2.9, aligned_edge=LEFT)
        key = VGroup(say(r"$f = 4$", colour=BLUE_C), say(r"$f = 4.1$", colour=PURPLE_C)).arrange(RIGHT, buff=0.8)
        key.next_to(head, DOWN, buff=0.35, aligned_edge=LEFT)
        width = always_redraw(lambda: Tex(rf"window width: {2 * w():.2f}", font_size=34, color=GREY_C)
                              .next_to(key, DOWN, buff=0.35, aligned_edge=LEFT))
        plab = MathTex("(1, 1)", color=BLACK, font_size=34).next_to(dot, DOWN + LEFT, buff=0.08)
        self.add(frame, lines, dot, plab, head, key, width)
        self.wait(1)
        self.snap()
        self.play(lw.animate.set_value(np.log(0.3)), run_time=2.5, rate_func=linear)
        self.snap()
        self.play(lw.animate.set_value(np.log(W1)), run_time=2.5, rate_func=linear)
        t1 = say(r"Zoomed in, the two lines", r"are straight and parallel.").next_to(width, DOWN, buff=0.45, aligned_edge=LEFT)
        self.play(FadeIn(t1))
        self.wait(1)
        self.snap()
        arrows = VGroup()
        for deg in (-45, -25, 25, 45, 0):
            u = rot(G, deg)
            r = reach(u)
            col = ORANGE_C if deg == 0 else GREY_C
            tip = to_screen(P + r * u, W1)
            arr = Arrow(CEN, tip, buff=0, color=col, stroke_width=7 if deg == 0 else 4,
                        max_tip_length_to_length_ratio=0.1)
            lab = MathTex(f"{r:.3f}", font_size=30, color=col if deg == 0 else BLACK)
            lab.move_to(tip + 0.38 * np.array([u[0], u[1], 0]))
            arrows.add(VGroup(arr, lab))
        t2 = say(r"Every arrow raises $f$ by 0.1.", r"The label is its length.").next_to(t1, DOWN, buff=0.4, aligned_edge=LEFT)
        self.play(FadeIn(t2), *[GrowArrow(a[0]) for a in arrows[:4]], *[FadeIn(a[1]) for a in arrows[:4]], run_time=1.5)
        self.wait(0.8)
        t3 = say(r"The shortest step goes", r"straight across: the direction", r"of the gradient $[3, 5]$.",
                 colour=ORANGE_C).next_to(t2, DOWN, buff=0.4, aligned_edge=LEFT)
        corner = to_screen(P, W1)
        e1, e2 = np.array([G[0], G[1], 0]), np.array([-G[1], G[0], 0])
        sq = VMobject(color=ORANGE_C, stroke_width=3).set_points_as_corners(
            [corner + 0.28 * e2, corner + 0.28 * (e1 + e2), corner + 0.28 * e1])
        self.play(GrowArrow(arrows[4][0]), FadeIn(arrows[4][1]), FadeIn(t3), Create(sq), run_time=1.5)
        self.bring_to_front(dot)
        self.wait(2.5)
        self.snap()


def key_frames_grid(frames, out, gap=16):
    w, hgt = frames[0].size
    sheet = Image.new("RGB", (2 * w + gap, 2 * hgt + gap), "white")
    for i, fr in enumerate(frames[:4]):
        sheet.paste(fr.convert("RGB"), ((i % 2) * (w + gap), (i // 2) * (hgt + gap)))
    sheet.save(out)


if __name__ == "__main__":
    assert f(P) == 4 and list(GRAD) == [3, 5]
    assert abs(f(P + reach(G) * G) - 4.1) < 1e-9 and reach(G) < reach(rot(G, 25)) < reach(rot(G, 45))
    name = "contour_zoom"
    media = HERE / ".manim"
    with tempconfig({"quality": "medium_quality", "background_color": WHITE, "media_dir": str(media),
                     "output_file": name, "disable_caching": True, "verbosity": "WARNING", "progress_bar": "none"}):
        scene = ContourZoom()
        scene.render()
    mp4 = HERE / f"{name}.mp4"
    shutil.copy(next(media.rglob(f"{name}.mp4")), mp4)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(mp4), "-vf",
                    "fps=12,scale=720:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / f"{name}.gif")], check=True)
    key_frames_grid(scene.snaps, HERE / f"{name}_frames.png")
    shutil.rmtree(media)

"""Kernel trick in pictures: two rings in 2D, lifted by z = exp(-(x1^2 + x2^2)), then split by a flat plane.
Run: python lift_3d.py  -> lift_3d.mp4, lift_3d.gif, lift_3d_frames.png"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
from manim import *
from PIL import Image

HERE = Path(__file__).parent
GREEN_C, RED_C, BLUE_C, GREY_C = "#54A24B", "#E45756", "#4C78A8", "#6B6B6B"
Text.set_default(color=BLACK, font="Latin Modern Roman")
rng = np.random.default_rng(0)
ang = rng.uniform(0, 2 * np.pi, 34)
inner = np.c_[np.cos(ang[:14]), np.sin(ang[:14])] * rng.uniform(0.1, 0.7, 14)[:, None]     # centre class
outer = np.c_[np.cos(ang[14:]), np.sin(ang[14:])] * rng.uniform(1.5, 1.9, 20)[:, None]     # ring class
HEIGHT = 2.6                                            # z = HEIGHT * exp(-r^2), stretched so the lift is visible


class Lift3D(ThreeDScene):
    def snap(self):
        self.snaps.append(Image.fromarray(self.renderer.get_frame()))

    def caption(self, *lines):
        cap = VGroup(*[Text(t, font_size=30) for t in lines]).arrange(DOWN, buff=0.15).to_edge(UP, buff=0.3)
        cap.add_background_rectangle(color=WHITE, opacity=1, buff=0.12)
        return cap

    def set_caption(self, *lines):
        new = self.caption(*lines)
        self.add_fixed_in_frame_mobjects(new)
        if self.cap is None:
            self.play(FadeIn(new))
        else:
            self.play(FadeOut(self.cap), FadeIn(new))
        self.cap = new

    def construct(self):
        self.snaps, self.cap = [], None
        axes = ThreeDAxes(x_range=[-2.5, 2.5], y_range=[-2.5, 2.5], z_range=[0, 3.5], x_length=5, y_length=5,
                          z_length=3.5, axis_config=dict(color=GREY_C, include_ticks=False, include_tip=False))
        dots = VGroup(*[Dot3D(axes.c2p(x, y, 0), radius=0.1, color=GREEN_C, resolution=(5, 5)) for x, y in inner],
                      *[Dot3D(axes.c2p(x, y, 0), radius=0.1, color=RED_C, resolution=(5, 5)) for x, y in outer])
        self.set_camera_orientation(phi=0, theta=-90 * DEGREES, zoom=1.25)
        self.add(axes, dots)
        self.set_caption("2D data: no straight line separates the rings")
        self.wait(0.5)
        self.snap()

        self.move_camera(phi=65 * DEGREES, theta=-50 * DEGREES, zoom=1.15, frame_center=axes.c2p(0, 0, 1.4), run_time=2)
        self.set_caption("add a third axis: z = exp(−(x₁² + x₂²))")
        self.snap()

        targets = [axes.c2p(x, y, HEIGHT * np.exp(-(x * x + y * y))) for x, y in np.r_[inner, outer]]
        self.play(*[d.animate.move_to(t) for d, t in zip(dots, targets)], run_time=2.5)
        self.set_caption("points near the centre rise, the ring stays low")
        self.snap()

        level = HEIGHT * np.exp(-1.1 ** 2)                 # between the two classes
        plane = Surface(lambda u, v: axes.c2p(u, v, level), u_range=[-2.2, 2.2], v_range=[-2.2, 2.2],
                        resolution=(2, 2), fill_color=BLUE_C, fill_opacity=0.25, stroke_color=BLUE_C, stroke_width=1)
        self.play(FadeIn(plane))
        self.set_caption("now a flat plane separates the classes")
        self.begin_ambient_camera_rotation(rate=0.25)
        self.wait(2)
        self.stop_ambient_camera_rotation()
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
                     "output_file": "lift_3d", "disable_caching": True, "verbosity": "WARNING",
                     "progress_bar": "none"}):
        scene = Lift3D()
        scene.render()
    mp4 = HERE / "lift_3d.mp4"
    shutil.copy(next(media.rglob("lift_3d.mp4")), mp4)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(mp4), "-vf",
                    "fps=12,scale=720:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "lift_3d.gif")], check=True)
    key_frames_grid(scene.snaps, HERE / "lift_3d_frames.png")
    shutil.rmtree(media)

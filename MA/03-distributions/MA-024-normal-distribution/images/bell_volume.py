"""Why sqrt(pi) is the area under e^(-x^2): lift the bell to the surface e^(-(x^2+y^2)).
Its volume, built from thin cylindrical shells 2*pi*r wide and e^(-r^2) tall, is pi.
Cut into slices parallel to the x axis, every slice is the bell scaled by e^(-y^2), so the volume is C * C = C^2.
So C^2 = pi and C = sqrt(pi).
Run: python bell_volume.py -> bell_volume.mp4, .gif, _frames.png (Manim 3-D; render on topgro)"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
from manim import *
from PIL import Image
from scipy import integrate

HERE = Path(__file__).parent
BLUE_C, ORANGE_C, GREEN_C, GREY_C = "#4C78A8", "#F58518", "#54A24B", "#6B6B6B"
Text.set_default(color=BLACK, font="Latin Modern Roman")
MathTex.set_default(color=BLACK)
R = 0.8                                                            # radius of the highlighted shell
shells = integrate.quad(lambda r: 2 * np.pi * r * np.exp(-r ** 2), 0, np.inf)[0]
C = integrate.quad(lambda x: np.exp(-x ** 2), -np.inf, np.inf)[0]
assert abs(shells - np.pi) < 1e-9 and abs(C - np.sqrt(np.pi)) < 1e-9
print("shell volume", shells, "C", C, "C^2", C ** 2)


class BellVolume(ThreeDScene):
    def snap(self):
        self.snaps.append(Image.fromarray(self.renderer.get_frame()))

    def caption(self, title, formula):
        cap = VGroup(Text(title, font_size=32, weight=BOLD), MathTex(formula, font_size=40)
                     ).arrange(DOWN, buff=0.18).to_edge(UP, buff=0.25)
        bg = BackgroundRectangle(cap, color=WHITE, fill_opacity=0.9, buff=0.1)
        return VGroup(bg, cap)

    def swap(self, old, new):
        self.add_fixed_in_frame_mobjects(new)
        self.play(FadeOut(old), FadeIn(new), run_time=0.8)
        return new

    def construct(self):
        self.snaps = []
        self.set_camera_orientation(phi=62 * DEGREES, theta=-55 * DEGREES, zoom=0.95)
        ax = ThreeDAxes(x_range=[-2.5, 2.5, 1], y_range=[-2.5, 2.5, 1], z_range=[0, 1.2, 0.5],
                        x_length=6, y_length=6, z_length=3, axis_config={"color": GREY_C, "include_tip": False}
                        ).shift(DOWN * 0.6)
        surf = Surface(lambda u, v: ax.c2p(u, v, np.exp(-(u ** 2 + v ** 2))), u_range=[-2.5, 2.5], v_range=[-2.5, 2.5],
                       resolution=(36, 36), fill_opacity=0.45, stroke_width=0.3, stroke_color=WHITE)
        surf.set_fill_by_checkerboard(BLUE_C, "#7EA6CE", opacity=0.45)
        curve = ParametricFunction(lambda t: ax.c2p(t, 0, np.exp(-t ** 2)), t_range=[-2.5, 2.5], color=ORANGE_C,
                                   stroke_width=6)
        cap = self.caption("The bell curve: its area is unknown", r"C = \int_{-\infty}^{\infty} e^{-x^2}\,dx = \ ?")
        self.add_fixed_in_frame_mobjects(cap)
        self.play(Create(ax), Create(curve), FadeIn(cap), run_time=1.5)
        self.wait(0.8)
        self.snap()

        cap = self.swap(cap, self.caption("Lift it to a surface", r"z = e^{-(x^2 + y^2)} = e^{-r^2}"))
        self.play(Create(surf), run_time=2)
        self.begin_ambient_camera_rotation(rate=0.12)
        self.wait(1.5)

        h = np.exp(-R ** 2)
        shell = Surface(lambda u, v: ax.c2p(R * np.cos(u), R * np.sin(u), v * h), u_range=[0, TAU], v_range=[0, 1],
                        resolution=(40, 2), fill_color=ORANGE_C, fill_opacity=0.85, stroke_width=0)
        cap = self.swap(cap, self.caption("Add up thin cylindrical shells",
                                          r"\text{volume} = \int_0^\infty 2\pi r\, e^{-r^2}\,dr = \pi"))
        self.play(FadeIn(shell), FadeOut(curve), surf.animate.set_fill(opacity=0.25), run_time=1.2)
        self.wait(2)
        self.snap()
        self.stop_ambient_camera_rotation()

        slices = VGroup()
        for y0, col in [(0, GREEN_C), (0.8, GREEN_C), (-1.3, GREEN_C)]:
            ts = np.linspace(-2.5, 2.5, 80)
            pts = [ax.c2p(t, y0, np.exp(-t ** 2 - y0 ** 2)) for t in ts] + [ax.c2p(2.5, y0, 0), ax.c2p(-2.5, y0, 0)]
            slices.add(Polygon(*pts, color=col, fill_color=col, fill_opacity=0.55, stroke_width=2))
        cap = self.swap(cap, self.caption("Or add up slices parallel to the x axis",
                                          r"\text{volume} = \int_{-\infty}^{\infty} C\, e^{-y^2}\,dy = C \cdot C = C^2"))
        self.play(FadeOut(shell), FadeIn(slices, lag_ratio=0.3), run_time=1.5)
        self.move_camera(theta=-80 * DEGREES, run_time=1.5)
        self.wait(1.5)
        self.snap()
        cap = self.swap(cap, self.caption("Two ways, one volume", r"C^2 = \pi \quad\Rightarrow\quad C = \sqrt{\pi}"))
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
                     "output_file": "bell_volume", "disable_caching": True, "verbosity": "WARNING",
                     "progress_bar": "none"}):
        scene = BellVolume()
        scene.render()
    mp4 = HERE / "bell_volume.mp4"
    shutil.copy(next(media.rglob("bell_volume.mp4")), mp4)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(mp4), "-vf",
                    "fps=10,scale=720:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "bell_volume.gif")], check=True)
    key_frames_grid([scene.snaps[i] for i in (0, 1, 2, 3)], HERE / "bell_volume_frames.png")
    shutil.rmtree(media)

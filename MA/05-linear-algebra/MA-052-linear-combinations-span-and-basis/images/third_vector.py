"""Linear dependence in 3D. v1 = [2, 0, 1] and v2 = [0, 2, 1] span a plane. Scaling a third vector that lies on the
plane ([2, 2, 2] = v1 + v2) only slides along that plane: the span does not grow (dependent). Scaling a third vector off
the plane ([0, 0, 2.5]) lifts the whole plane up and down, sweeping it through all of 3D (independent).
Run: python third_vector.py  -> third_vector.mp4, .gif, _frames.png"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
from manim import *
from PIL import Image

HERE = Path(__file__).parent
BLUE_C, ORANGE_C, GREEN_C, RED_C, GREY_C = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#6B6B6B"
Text.set_default(color=BLACK, font="Latin Modern Roman")
V1, V2 = np.array([2.0, 0, 1]), np.array([0, 2.0, 1])
ON, OFF = V1 + V2, np.array([0, 0, 2.5])
K = 0.75                                                   # screen units per data unit


def boxed(mob, buff=0.08):
    return VGroup(BackgroundRectangle(mob, color=WHITE, fill_opacity=0.92, buff=buff), mob)


def arrow3(v, colour):
    return Arrow3D(ORIGIN, K * np.asarray(v, float), color=colour, thickness=0.035, height=0.25, base_radius=0.09)


def sheet(shift=np.zeros(3), opacity=0.35, colour=BLUE_C):
    corners = [K * (s * V1 + t * V2 + shift) for s, t in ((-1.3, -1.3), (1.3, -1.3), (1.3, 1.3), (-1.3, 1.3))]
    return Polygon(*corners, color=colour, fill_color=colour, fill_opacity=opacity, stroke_width=1.5)


class ThirdVector(ThreeDScene):
    def snap(self):
        self.snaps.append(Image.fromarray(self.renderer.get_frame()))

    def caption(self, *lines, colour=BLACK):
        group = VGroup(*[Text(t, font_size=30, color=colour, weight=BOLD) for t in lines]).arrange(DOWN, buff=0.12)
        out = boxed(group, 0.12).to_edge(DOWN, buff=0.25)
        self.add_fixed_in_frame_mobjects(out)
        return out

    def construct(self):
        self.snaps = []
        self.set_camera_orientation(phi=65 * DEGREES, theta=-80 * DEGREES, zoom=0.95)
        axes = ThreeDAxes(x_range=[-4, 4], y_range=[-4, 4], z_range=[-3, 3], x_length=8 * K, y_length=8 * K,
                          z_length=6 * K, axis_config={"stroke_color": GREY_C, "stroke_width": 2})
        plane = sheet()
        v1, v2 = arrow3(V1, BLUE_C), arrow3(V2, BLUE_C)
        title = boxed(MathTex(r"\mathbf v_1 = [2, 0, 1],\ \ \mathbf v_2 = [0, 2, 1]", color=BLUE_C, font_size=40), 0.1)
        title.to_corner(UL, buff=0.3)
        self.add_fixed_in_frame_mobjects(title)
        self.add(axes, plane, v1, v2)
        cap = self.caption("v1 and v2 span a plane")
        self.wait(0.8)
        self.snap()
        # 1. a third vector on the plane: scaling it never leaves the sheet
        c = ValueTracker(1.0)
        green = always_redraw(lambda: arrow3(c.get_value() * ON, GREEN_C))
        tag = boxed(MathTex(r"c\,[2, 2, 2] = c\,(\mathbf v_1 + \mathbf v_2)", color=GREEN_C, font_size=40), 0.1)
        tag.next_to(title, DOWN, aligned_edge=LEFT, buff=0.15)
        self.remove(cap)
        cap = self.caption("third vector ON the plane:", "scaling it stays on the sheet", colour=GREEN_C)
        self.add_fixed_in_frame_mobjects(tag)
        self.add(green)
        self.begin_ambient_camera_rotation(rate=-0.04)
        self.play(c.animate.set_value(-1.2), run_time=2)
        self.play(c.animate.set_value(1.3), run_time=2)
        self.wait(0.3)
        self.snap()
        self.remove(cap)
        cap = self.caption("span does not grow: dependent", colour=GREEN_C)
        self.wait(1.2)
        # 2. a third vector off the plane: scaling it lifts the sheet through space
        self.remove(green, tag, cap)
        d = ValueTracker(0.0)
        red = always_redraw(lambda: arrow3(d.get_value() * OFF, RED_C))
        moving = always_redraw(lambda: sheet(d.get_value() * OFF, 0.45, RED_C))
        tag = boxed(MathTex(r"d\,[0, 0, 2.5]", color=RED_C, font_size=40), 0.1)
        tag.next_to(title, DOWN, aligned_edge=LEFT, buff=0.15)
        self.add_fixed_in_frame_mobjects(tag)
        cap = self.caption("third vector OFF the plane:", "scaling it lifts the whole sheet", colour=RED_C)
        self.add(red, moving)
        ghosts = VGroup()
        for target in (0.8, -0.8):
            self.play(d.animate.set_value(target), run_time=1)
            ghost = sheet(target * OFF, 0.07, RED_C)
            ghosts.add(ghost)
            self.add(ghost)
            if target == 0.8:
                self.wait(0.3)
                self.snap()
        self.play(d.animate.set_value(1.0), run_time=1)
        self.remove(cap)
        cap = self.caption("the stacked sheets fill all of 3D: independent", colour=RED_C)
        self.wait(2)
        self.stop_ambient_camera_rotation()
        self.snap()


def key_frames_grid(frames, out, gap=16):
    w, h = frames[0].size
    sheet_img = Image.new("RGB", (2 * w + gap, 2 * h + gap), "white")
    for i, f in enumerate(frames[:4]):
        sheet_img.paste(f.convert("RGB"), ((i % 2) * (w + gap), (i // 2) * (h + gap)))
    sheet_img.save(out)


if __name__ == "__main__":
    assert np.linalg.matrix_rank(np.column_stack([V1, V2, ON])) == 2
    assert np.linalg.matrix_rank(np.column_stack([V1, V2, OFF])) == 3
    name = "third_vector"
    media = HERE / ".manim"
    with tempconfig({"quality": "medium_quality", "background_color": WHITE, "media_dir": str(media),
                     "output_file": name, "disable_caching": True, "verbosity": "WARNING", "progress_bar": "none"}):
        scene = ThirdVector()
        scene.render()
    mp4 = HERE / f"{name}.mp4"
    shutil.copy(next(media.rglob(f"{name}.mp4")), mp4)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(mp4), "-vf",
                    "fps=10,scale=640:-1:flags=lanczos,split[a][b];[a]palettegen=max_colors=48:stats_mode=diff[p];[b][p]paletteuse=dither=none:diff_mode=rectangle",
                    str(HERE / f"{name}.gif")], check=True)
    key_frames_grid(scene.snaps, HERE / f"{name}_frames.png")
    shutil.rmtree(media)

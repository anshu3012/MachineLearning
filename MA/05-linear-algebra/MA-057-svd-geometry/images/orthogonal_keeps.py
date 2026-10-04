"""An orthogonal matrix keeps lengths and angles; a general matrix does not (idea after Khan Academy, "Orthogonal
matrices preserve angles and lengths"; our own code). Two unit arrows 60 degrees apart ride along as the grid moves:
first under the Note's rotation V (45 degrees), then under the Note's matrix A = [[3, 0], [4, 5]].
Run: python orthogonal_keeps.py  -> orthogonal_keeps.mp4, .gif, _frames.png"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
from manim import *
from PIL import Image

HERE = Path(__file__).parent
BLUE_C, ORANGE_C, PURPLE_C, GREY_C = "#4C78A8", "#F58518", "#B279A2", "#C8C8C8"
Text.set_default(color=BLACK, font="Latin Modern Roman")
V = np.array([[1, -1], [1, 1]]) / np.sqrt(2)
A = np.array([[3.0, 0.0], [4.0, 5.0]])
X = np.array([1.0, 0.0])
Y = np.array([0.5, np.sqrt(3) / 2])
KS, ORG = [1.6], np.array([-3.2, -2.4])


def sc(p):
    return np.array([ORG[0] + KS[0] * p[0], ORG[1] + KS[0] * p[1], 0])


def angle(a, b):
    return np.degrees(np.arccos(a @ b / np.linalg.norm(a) / np.linalg.norm(b)))


def boxed(mob, buff=0.08):
    return VGroup(BackgroundRectangle(mob, color=WHITE, fill_opacity=0.92, buff=buff), mob)


class Keeps(Scene):
    def snap(self):
        self.snaps.append(Image.fromarray(self.renderer.get_frame()))

    def construct(self):
        self.snaps = []
        M = [np.eye(2)]

        def picture():
            m = M[0]
            out = VGroup()
            for i in range(-30, 31):
                out.add(Line(sc(m @ [i, -30]), sc(m @ [i, 30]), color=GREY_C, stroke_width=1.5))
                out.add(Line(sc(m @ [-30, i]), sc(m @ [30, i]), color=GREY_C, stroke_width=1.5))
            a, b = m @ X, m @ Y
            out.add(Arrow(sc([0, 0]), sc(a), buff=0, color=ORANGE_C, stroke_width=7, max_tip_length_to_length_ratio=0.2))
            out.add(Arrow(sc([0, 0]), sc(b), buff=0, color=PURPLE_C, stroke_width=7, max_tip_length_to_length_ratio=0.2))
            g = VGroup(Text(f"orange length {np.linalg.norm(a):.2f}", font_size=34, color=ORANGE_C),
                       Text(f"purple length {np.linalg.norm(b):.2f}", font_size=34, color=PURPLE_C),
                       Text(f"angle between {angle(a, b):.1f}°", font_size=34)).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
            out.add(boxed(g, 0.1).move_to([4.2, 0.9, 0]))
            return out

        self.add(always_redraw(picture))
        title = boxed(Text("two unit arrows, 60° apart", font_size=32), 0.08).move_to([3.0, 3.3, 0])
        self.add(title)
        self.wait(1.0)
        self.snap()
        t = ValueTracker(0.0)
        holder = Mobject()
        self.add(holder)
        # part 1: the rotation V, played as a turn through 0..45 degrees
        holder.add_updater(lambda mob: M.__setitem__(0, np.array(
            [[np.cos(t.get_value()), -np.sin(t.get_value())], [np.sin(t.get_value()), np.cos(t.get_value())]])))
        self.play(Transform(title, boxed(Text("orthogonal V: rotate 45°", font_size=32), 0.08).move_to([3.0, 3.3, 0])))
        self.play(t.animate.set_value(np.pi / 4), run_time=2.5)
        self.wait(1.2)
        self.snap()
        holder.clear_updaters()
        M[0] = np.eye(2)
        t.set_value(0.0)
        kt = ValueTracker(KS[0])                          # zoom out so that A's long arrows fit
        zoom = Mobject().add_updater(lambda mob: KS.__setitem__(0, kt.get_value()))
        self.add(zoom)
        self.play(kt.animate.set_value(0.5), run_time=1.5)
        holder.add_updater(lambda mob: M.__setitem__(0, (1 - t.get_value()) * np.eye(2) + t.get_value() * A))
        self.play(Transform(title, boxed(Text("not orthogonal: A stretches and bends", font_size=32), 0.08)
                            .move_to([3.0, 3.3, 0])))
        self.play(t.animate.set_value(1.0), run_time=3.0)
        self.wait(2.0)
        self.snap()


def key_frames_grid(frames, out, gap=16):
    w, h = frames[0].size
    sheet = Image.new("RGB", (len(frames) * w + (len(frames) - 1) * gap, h), "white")
    for i, fr in enumerate(frames):
        sheet.paste(fr.convert("RGB"), (i * (w + gap), 0))
    sheet.save(out)


if __name__ == "__main__":
    assert np.allclose(V.T @ V, np.eye(2))
    assert abs(np.linalg.norm(A @ X) - 5) < 1e-12 and abs(angle(A @ X, A @ Y) - 23.5) < 0.1
    name = "orthogonal_keeps"
    media = HERE / ".manim"
    with tempconfig({"quality": "medium_quality", "background_color": WHITE, "media_dir": str(media),
                     "output_file": name, "disable_caching": True, "verbosity": "WARNING", "progress_bar": "none"}):
        scene = Keeps()
        scene.render()
    mp4 = HERE / f"{name}.mp4"
    shutil.copy(next(media.rglob(f"{name}.mp4")), mp4)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(mp4), "-vf",
                    "fps=10,scale=640:-1:flags=lanczos,split[a][b];[a]palettegen=max_colors=48:stats_mode=diff[p];"
                    "[b][p]paletteuse=dither=none", str(HERE / f"{name}.gif")], check=True)
    key_frames_grid(scene.snaps[1:], HERE / f"{name}_frames.png")
    shutil.rmtree(media)

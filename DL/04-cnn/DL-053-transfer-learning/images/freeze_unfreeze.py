"""Transfer learning on VGG16 in three steps: cut off the ImageNet top and add a new one; freeze the whole
convolutional base (feature extraction); then unfreeze block 5 (fine-tuning). Trainable-parameter counts from the
Notebook (2,097,665 and 9,177,089). Manim: blocks move, padlocks close and open.
Run: python freeze_unfreeze.py -> freeze_unfreeze.gif, freeze_unfreeze_frames.png"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
from manim import *
from PIL import Image
import manimpango

for _f in Path("/usr/share/texmf/fonts/opentype/public/lm").glob("lmroman10-*.otf"):
    manimpango.register_font(str(_f))

HERE = Path(__file__).parent
BLUE_C, ORANGE_C, GREEN_C, RED_C, PURPLE_C, GREY_C = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#B279A2", "#6B6B6B"
Text.set_default(color=BLACK, font="Latin Modern Roman")
MarkupText.set_default(color=BLACK, font="Latin Modern Roman")


class Snap(Scene):
    """A scene that keeps key frames for the PDF grid."""
    def snap(self):
        if not hasattr(self, "snaps"):
            self.snaps = []
        self.snaps.append(Image.fromarray(self.renderer.get_frame()))


def render(scene_cls, name, fps=10, width=760):
    """Render to <name>.gif and a 2 x 2 grid of the scene's first four key frames, <name>_frames.png."""
    media = HERE / ".manim"
    with tempconfig({"quality": "medium_quality", "background_color": WHITE, "media_dir": str(media),
                     "output_file": name, "disable_caching": True, "verbosity": "WARNING", "progress_bar": "none"}):
        scene = scene_cls()
        scene.render()
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(next(media.rglob(f"{name}.mp4"))), "-vf",
                    f"fps={fps},scale={width}:-1:flags=lanczos,split[a][b];[a]palettegen=max_colors=64[p];[b][p]paletteuse",
                    str(HERE / f"{name}.gif")], check=True)
    w, h = scene.snaps[0].size
    sheet = Image.new("RGB", (2 * w + 16, 2 * h + 16), "white")
    for i, f in enumerate(scene.snaps[:4]):
        sheet.paste(f.convert("RGB"), ((i % 2) * (w + 16), (i // 2) * (h + 16)))
    sheet.save(HERE / f"{name}_frames.png")
    shutil.rmtree(media)


def block(label, sub, colour, w=1.45, h=2.2):
    b = VGroup(RoundedRectangle(corner_radius=0.12, width=w, height=h, stroke_color=colour, stroke_width=4,
                                fill_color=colour, fill_opacity=0.18),
               VGroup(Text(label, font_size=26), Text(sub, font_size=20, color=GREY_C)).arrange(DOWN, buff=0.1))
    b[1].move_to(b[0])
    return b


def padlock(closed=True, colour=GREY_C):
    body = RoundedRectangle(corner_radius=0.05, width=0.42, height=0.32, stroke_width=0, fill_color=colour, fill_opacity=1)
    shackle = Arc(radius=0.14, start_angle=0, angle=PI, stroke_color=colour, stroke_width=5).move_to(body.get_top() + UP * 0.07)
    legs = VGroup(Line(shackle.get_start(), shackle.get_start() + DOWN * 0.08, stroke_color=colour, stroke_width=5),
                  Line(shackle.get_end(), shackle.get_end() + DOWN * 0.08, stroke_color=colour, stroke_width=5))
    lock = VGroup(body, shackle, legs)
    if not closed:                       # an open lock: the shackle lifted and swung to the side
        VGroup(shackle, legs[1]).shift(UP * 0.12)
        legs[0].set_opacity(0)
    return lock


class Freeze(Snap):
    def construct(self):
        title = Text("VGG16, trained on ImageNet", font_size=38).to_edge(UP, buff=0.35)
        subs = ["edges,", "colours", "textures", "parts", "objects"]
        base = VGroup(*[block(f"block {i + 1}", ["edges", "colours", "textures", "parts", "objects"][i], BLUE_C)
                        for i in range(5)]).arrange(RIGHT, buff=0.18).move_to([-1.5, 0.3, 0])
        top = block("dense top", "1,000 classes", GREEN_C, w=2.2).next_to(base, RIGHT, buff=0.35)
        brace = VGroup(Line(base.get_corner(DL) + DOWN * 0.25, base.get_corner(DR) + DOWN * 0.25, stroke_color=BLUE_C, stroke_width=3),
                       Text("convolutional base", font_size=26, color=BLUE_C))
        brace[1].next_to(brace[0], DOWN, buff=0.12)
        self.play(FadeIn(title), LaggedStart(*[FadeIn(b, shift=UP * 0.2) for b in base], lag_ratio=0.15), run_time=1.2)
        self.play(FadeIn(top), FadeIn(brace), run_time=0.6)
        self.wait(1.0)
        self.snap()

        # step 1: replace the top
        new_top = block("new top", "cat or dog", ORANGE_C, w=2.2).move_to(top)
        self.play(Transform(title, Text("Step 1: cut off the top, add a new one", font_size=38).to_edge(UP, buff=0.35)),
                  top.animate.shift(UP * 2.2).set_opacity(0), run_time=0.9)
        self.play(FadeIn(new_top, shift=UP * 0.4), run_time=0.7)
        self.wait(0.8)

        # step 2: freeze the base
        locks = VGroup(*[padlock().next_to(b, UP, buff=0.12) for b in base])
        count = Text("trainable: the new top only, 2,097,665 parameters", font_size=30, color=ORANGE_C).to_edge(DOWN, buff=0.45)
        self.play(Transform(title, Text("Step 2, feature extraction: freeze the whole base", font_size=38
                                        ).to_edge(UP, buff=0.35)), run_time=0.6)
        self.play(LaggedStart(*[FadeIn(l, scale=1.6) for l in locks], lag_ratio=0.2),
                  *[b[0].animate.set_fill(GREY_C, opacity=0.18).set_stroke(GREY_C) for b in base], run_time=1.4)
        self.play(FadeIn(count), Indicate(new_top, color=ORANGE_C, scale_factor=1.06), run_time=0.8)
        self.wait(1.4)
        self.snap()

        # step 3: unfreeze block 5
        open5 = padlock(closed=False, colour=ORANGE_C).move_to(locks[4])
        self.play(Transform(title, Text("Step 3, fine-tuning: unfreeze block 5", font_size=38).to_edge(UP, buff=0.35)),
                  run_time=0.6)
        self.play(Transform(locks[4], open5), base[4][0].animate.set_fill(ORANGE_C, opacity=0.18).set_stroke(ORANGE_C),
                  run_time=0.9)
        self.play(Transform(count, Text("trainable: block 5 + the new top, 9,177,089 parameters", font_size=30,
                                        color=ORANGE_C).to_edge(DOWN, buff=0.45)), run_time=0.6)
        self.wait(1.0)
        self.snap()
        lr = Text("with a very low learning rate, so the trained filters change only a little", font_size=28,
                  color=GREY_C).next_to(count, UP, buff=0.2)
        self.play(FadeIn(lr), run_time=0.6)
        self.wait(2.5)
        self.snap()


if __name__ == "__main__":
    render(Freeze, "freeze_unfreeze")

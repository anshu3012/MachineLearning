"""Dropout on the Note's network (5 inputs, two hidden layers of 5, 1 output). Each training step draws a new random
mask: every input and hidden node is switched off with probability p = 0.25 (the Note's worked example); the output
node is never dropped. At prediction every node is back and each weight is scaled by 1 - p (0.8 -> 0.6).
Run: python dropout_anim.py  -> dropout_anim.gif, dropout_anim_frames.png"""
import shutil
import subprocess
from pathlib import Path

import glob

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
P, STEPS = 0.25, 4
LAYERS = [5, 5, 5, 1]
XS = [-4.2, -1.4, 1.4, 4.2]
LAYER_COLOURS = [BLUE_C, PURPLE_C, PURPLE_C, GREEN_C]
rng = np.random.default_rng(0)
# one mask per step; True = node kept; the output layer is never dropped
MASKS = [[rng.random(n) >= P if l < 3 else np.ones(n, bool) for l, n in enumerate(LAYERS)] for _ in range(STEPS)]


def node_pos(l, i):
    n = LAYERS[l]
    return np.array([XS[l], (i - (n - 1) / 2) * -1.05 - 0.2, 0])


class Dropout(Scene):
    def snap(self):
        self.snaps.append(Image.fromarray(self.renderer.get_frame()))

    def construct(self):
        self.snaps = []
        nodes = [[Circle(0.3, stroke_color=LAYER_COLOURS[l], stroke_width=4, fill_color=WHITE, fill_opacity=1)
                  .move_to(node_pos(l, i)) for i in range(n)] for l, n in enumerate(LAYERS)]
        edges = {}
        for l in range(3):
            for i in range(LAYERS[l]):
                for j in range(LAYERS[l + 1]):
                    edges[l, i, j] = Line(node_pos(l, i), node_pos(l + 1, j), buff=0.3, stroke_color=GREY_C,
                                          stroke_width=2, stroke_opacity=0.7)
        heads = VGroup(*[Text(t, font_size=30, color=GREY_C).move_to([x, 2.75, 0])
                         for t, x in zip(["inputs", "hidden 1", "hidden 2", "output"], XS)])
        title = Text("Training: each node is switched off with p = 0.25", font_size=36).to_edge(UP, buff=0.25)
        self.play(FadeIn(title), FadeIn(heads), *[Create(e) for e in edges.values()],
                  *[FadeIn(c) for layer in nodes for c in layer], run_time=1.2)
        self.wait(0.5)

        crosses = VGroup()
        status = VGroup()
        for s, mask in enumerate(MASKS):
            off = [(l, i) for l in range(3) for i in range(LAYERS[l]) if not mask[l][i]]
            anims = []
            for l, layer in enumerate(nodes):
                for i, c in enumerate(layer):
                    kept = mask[l][i]
                    anims.append(c.animate.set_stroke(LAYER_COLOURS[l] if kept else "#C8C8C8")
                                 .set_fill(WHITE if kept else "#EDEDED", 1))
            for (l, i, j), e in edges.items():
                live = mask[l][i] and mask[l + 1][j]
                anims.append(e.animate.set_stroke(BLUE_C if live else "#E2E2E2", 3 if live else 1.5, 1 if live else 0.6))
            new_crosses = VGroup(*[Cross(nodes[l][i], stroke_color=RED_C, stroke_width=4, scale_factor=0.55)
                                   for l, i in off])
            new_status = Text(f"step {s + 1}: {len(off)} of 15 nodes off, a new sub-network",
                              font_size=34, color=BLUE_C).to_edge(DOWN, buff=0.3)
            self.play(*anims, FadeOut(crosses), FadeIn(new_crosses), FadeOut(status), FadeIn(new_status), run_time=1.0)
            crosses, status = new_crosses, new_status
            self.wait(1.0)
            if s in (0, 1, 3):
                self.snap()

        count = Text("2¹⁵ = 32,768 possible sub-networks", font_size=34, color=PURPLE_C
                     ).to_edge(DOWN, buff=0.3)
        self.play(FadeOut(status), FadeIn(count))
        self.wait(1.5)

        # prediction: everything back on, weights scaled by 1 - p
        anims = [c.animate.set_stroke(LAYER_COLOURS[l]).set_fill(WHITE, 1) for l, layer in enumerate(nodes) for c in layer]
        anims += [e.animate.set_stroke(GREEN_C, 2.5, 0.8) for e in edges.values()]
        title2 = Text("Prediction: every node on, each weight × (1 − p)", font_size=36).to_edge(UP, buff=0.25)
        self.play(*anims, FadeOut(crosses), FadeOut(count), FadeOut(title), FadeIn(title2), run_time=1.2)
        e = edges[1, 0, 0]
        self.play(e.animate.set_stroke(ORANGE_C, 7, 1), run_time=0.6)
        ex = Text("w = 0.8  →  0.8 × 0.75 = 0.6", font_size=36, color=ORANGE_C).to_edge(DOWN, buff=0.3)
        self.play(FadeIn(ex))
        self.wait(2.0)
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
                     "output_file": "dropout_anim", "disable_caching": True, "verbosity": "WARNING",
                     "progress_bar": "none"}):
        scene = Dropout()
        scene.render()
    mp4 = next(media.rglob("dropout_anim.mp4"))
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(mp4), "-vf",
                    "fps=10,scale=720:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "dropout_anim.gif")], check=True)
    key_frames_grid(scene.snaps, HERE / "dropout_anim_frames.png")
    shutil.rmtree(media)

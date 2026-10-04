"""The chain rule as linked number lines (Manim). Student 1 of the classification network: nudge the output weight
W2_11 by 0.01 and watch z_f, y_hat and L move in turn. Each ratio of two movements is one chain-rule factor, and the
three ratios multiply to the derivative of the Note, -0.38.
Run: python number_lines.py -> number_lines.mp4, .gif, _frames.png"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
from manim import *
from PIL import Image
import manimpango

for f in Path("/usr/share/texmf/fonts/opentype/public/lm").glob("lmroman10-*.otf"):   # pango on topgro misses LM
    manimpango.register_font(str(f))

HERE = Path(__file__).parent
BLUE_C, ORANGE_C, GREEN_C, RED_C, GREY_C = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#6B6B6B"
Text.set_default(color=BLACK, font="Latin Modern Roman")
sig = lambda z: 1 / (1 + np.exp(-z))
O = sig(1.6)                                             # O11 = O12 = 0.832
DW = 0.01


def forward(w):
    z = w * O + 0.1 * O
    return z, sig(z), -np.log(sig(z))                    # y = 1


(z0, y0, L0), (z1, y1, L1) = forward(0.1), forward(0.1 + DW)
R = [(z1 - z0) / DW, (y1 - y0) / (z1 - z0), (L1 - L0) / (y1 - y0)]
assert round(y0, 4) == 0.5415 and round(L0, 3) == 0.613
assert round(R[0], 3) == 0.832 and round(R[1], 3) == 0.248 and round(R[2], 2) == -1.84
assert round(np.prod(R), 2) == round(-(1 - y0) * O, 2) == -0.38           # the product is the Note's derivative
# name, start, end, window, colour
LINES = [("weight W²₁₁", 0.1, 0.1 + DW, (0.095, 0.115), BLUE_C), ("weighted sum z", z0, z1, (z0 - 0.004, z0 + 0.012), GREY_C),
         ("prediction ŷ", y0, y1, (y0 - 0.001, y0 + 0.003), ORANGE_C), ("loss L", L0, L1, (L0 - 0.005, L0 + 0.002), RED_C)]
RATIO = [f"z moves {R[0]:.3f} times as far as the weight  (the hidden output)",
         f"ŷ moves {R[1]:.3f} times as far as z  (the sigmoid's slope)",
         f"L moves {abs(R[2]):.2f} times as far as ŷ, downwards  (the loss's slope)"]
X0, X1 = -3.2, 2.2


class Lines(Scene):
    def construct(self):
        snaps = []
        title = Text("Nudge one weight and follow the change to the loss", font_size=32, weight=BOLD).to_edge(UP, buff=0.2)
        self.add(title)
        ys = [2.0, 0.75, -0.5, -1.75]
        dots, px = [], []
        for (name, a, b, (lo, hi), col), y in zip(LINES, ys):
            f = lambda v, lo=lo, hi=hi: X0 + (v - lo) / (hi - lo) * (X1 - X0)
            ln = Line([X0, y, 0], [X1, y, 0], color=GREY_C, stroke_width=3)
            ticks = VGroup(*[Line([x, y - 0.1, 0], [x, y + 0.1, 0], color=GREY_C, stroke_width=3) for x in (X0, X1)])
            ends = VGroup(Text(f"{lo:.3f}", font_size=22, color=GREY_C).next_to(ticks[0], DOWN, buff=0.08),
                          Text(f"{hi:.3f}", font_size=22, color=GREY_C).next_to(ticks[1], DOWN, buff=0.08))
            lab = Text(name, font_size=28, color=col).next_to(ln, LEFT, buff=0.35)
            d = Dot([f(a), y, 0], radius=0.14, color=col)
            self.add(ln, ticks, ends, lab, d)
            dots.append(d)
            px.append((f(a), f(b), y, a, b, col))
        self.wait(0.8)
        vals = []
        for i, (xa, xb, y, a, b, col) in enumerate(px):
            ghost = Dot([xa, y, 0], radius=0.14, color=col, fill_opacity=0.25)
            move = Text(f"{a:.4f} → {b:.4f}", font_size=24, color=col).move_to([4.8, y + 0.22, 0])
            self.add(ghost)
            self.play(dots[i].animate.move_to([xb, y, 0]), FadeIn(move), run_time=1.0)
            if i:
                r = Text(RATIO[i - 1], font_size=22, color=BLACK).move_to([0.9, (ys[i - 1] + ys[i]) / 2 + 0.05, 0])
                self.play(FadeIn(r), run_time=0.4)
            self.wait(1.0)
            if i in (1, 3):
                snaps.append(Image.fromarray(self.renderer.get_frame()))
        final = Text(f"change of L per unit change of the weight:  {R[0]:.3f} × {R[1]:.3f} × (−{abs(R[2]):.2f}) = −{abs(np.prod(R)):.2f}",
                     font_size=28, color=RED_C).to_edge(DOWN, buff=0.45)
        self.play(FadeIn(final), run_time=0.6)
        self.wait(2.5)
        snaps.append(Image.fromarray(self.renderer.get_frame()))
        self.snaps = snaps


if __name__ == "__main__":
    print("ratios", np.round(R, 4), "product", round(float(np.prod(R)), 4), "exact derivative", round(-(1 - y0) * O, 4))
    media = HERE / ".manim"
    with tempconfig({"quality": "medium_quality", "frame_rate": 15, "background_color": WHITE, "media_dir": str(media),
                     "output_file": "number_lines", "disable_caching": True, "verbosity": "WARNING", "progress_bar": "none"}):
        scene = Lines()
        scene.render()
    mp4 = HERE / "number_lines.mp4"
    shutil.copy(next(media.rglob("number_lines.mp4")), mp4)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(mp4), "-vf",
                    "fps=8,scale=720:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse", str(HERE / "number_lines.gif")], check=True)
    w, h = scene.snaps[0].size
    sheet = Image.new("RGB", (w, 3 * h + 32), "white")
    for i, f in enumerate(scene.snaps):
        sheet.paste(f.convert("RGB"), (0, i * (h + 16)))
    sheet.save(HERE / "number_lines_frames.png")
    shutil.rmtree(media)

"""One decoder step i in the two designs, run side by side, one operation at a time. Bahdanau: score the previous
state s_(i-1) with a small network, weights, context c_i, then the LSTM step (c_i is one of its inputs), then the
output. Luong: the LSTM step first, then score the new state s_i by a dot product, weights, context c_i, joined with
s_i into h~_i, then the output. Follows the Note's sections 4 and 5 (Bahdanau et al. 2015, §3.1; Luong et al. 2015,
§3.1). Run: python two_orders.py -> two_orders.mp4, two_orders.gif, two_orders_frames.png (Manim)"""
import shutil
import subprocess
from pathlib import Path

from manim import *
from PIL import Image

HERE = Path(__file__).parent
BLUE_C, ORANGE_C, GREEN_C, RED_C, PURPLE_C, GREY_C = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#B279A2", "#6B6B6B"
Text.set_default(color=BLACK, font="Latin Modern Roman")
MarkupText.set_default(color=BLACK, font="Latin Modern Roman")
# (label, colour) from bottom to top
BAHDANAU = [("s<sub>i-1</sub>: previous state", GREY_C), ("score: small network\nv·tanh(W s<sub>i-1</sub> + U h<sub>j</sub>)", PURPLE_C),
            ("softmax → weights α<sub>ij</sub>", PURPLE_C), ("context c<sub>i</sub> = Σ α<sub>ij</sub> h<sub>j</sub>", GREEN_C),
            ("LSTM step (input: y<sub>i-1</sub>, c<sub>i</sub>) → s<sub>i</sub>", BLUE_C), ("softmax → next word", ORANGE_C)]
LUONG = [("s<sub>i-1</sub>: previous state", GREY_C), ("LSTM step (input: y<sub>i-1</sub>) → s<sub>i</sub>", BLUE_C),
         ("score: dot product s<sub>i</sub> · h<sub>j</sub>", PURPLE_C), ("softmax → weights α<sub>ij</sub>", PURPLE_C),
         ("context c<sub>i</sub> = Σ α<sub>ij</sub> h<sub>j</sub>", GREEN_C),
         ("h~<sub>i</sub> = tanh(W<sub>c</sub>[c<sub>i</sub>; s<sub>i</sub>]) → next word", ORANGE_C)]


def column(steps, x):
    boxes, arrows = VGroup(), VGroup()
    for k, (lab, col) in enumerate(steps):
        t = MarkupText(lab, font_size=21)
        b = RoundedRectangle(corner_radius=0.12, width=5.6, height=max(0.62, t.height + 0.25), color=col,
                             fill_color=col, fill_opacity=0.08, stroke_width=3)
        boxes.add(VGroup(b, t.move_to(b)).move_to([x, -2.75 + 1.07 * k, 0]))
    for k in range(len(steps) - 1):
        arrows.add(Arrow(boxes[k].get_top(), boxes[k + 1].get_bottom(), buff=0.03, color=GREY_C, stroke_width=3,
                         max_tip_length_to_length_ratio=0.35))
    return boxes, arrows


class TwoOrders(Scene):
    def snap(self):
        self.snaps.append(Image.fromarray(self.renderer.get_frame()))

    def construct(self):
        self.snaps = []
        title = Text("One decoder step: where the attention happens", font_size=30).to_edge(UP, buff=0.2)
        hb = Text("Bahdanau", font_size=30, color=RED_C).move_to([-3.4, 3.15, 0])
        hl = Text("Luong", font_size=30, color=BLUE_C).move_to([3.4, 3.15, 0])
        bb, ba = column(BAHDANAU, -3.4)
        lb, la = column(LUONG, 3.4)
        self.play(FadeIn(title), FadeIn(hb), FadeIn(hl), run_time=0.6)
        self.play(FadeIn(bb[0]), FadeIn(lb[0]), run_time=0.6)
        for k in range(1, len(BAHDANAU)):
            self.play(GrowArrow(ba[k - 1]), GrowArrow(la[k - 1]), FadeIn(bb[k], shift=UP * 0.2),
                      FadeIn(lb[k], shift=UP * 0.2), run_time=0.9)
            self.wait(0.5)
            if k in (1, 3, 5):
                self.snap()
        for box in (bb[3], lb[4]):
            box[0].set_stroke(width=6)
        note = VGroup(Text("Bahdanau: the context is ready before the LSTM step", font_size=22, color=RED_C),
                      Text("Luong: the LSTM step runs first; the context joins after it", font_size=22, color=BLUE_C)
                      ).arrange(DOWN, buff=0.08).to_edge(DOWN, buff=0.08)
        self.play(Indicate(bb[3], color=GREEN_C), Indicate(lb[4], color=GREEN_C), run_time=1.0)
        self.play(FadeIn(note), run_time=0.8)
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
                     "output_file": "two_orders", "disable_caching": True, "verbosity": "WARNING",
                     "progress_bar": "none"}):
        scene = TwoOrders()
        scene.render()
    mp4 = HERE / "two_orders.mp4"
    shutil.copy(next(media.rglob("two_orders.mp4")), mp4)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(mp4), "-vf",
                    "fps=12,scale=720:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "two_orders.gif")], check=True)
    s = scene.snaps
    key_frames_grid(s, HERE / "two_orders_frames.png")
    shutil.rmtree(media)

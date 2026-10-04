"""One position through a decoder block, in a trained model. The decoder input is "<start> nous sommes" and the
English sentence "we're friends ."; we follow the newest position, "sommes", through the last decoder block:
masked self-attention (it may read only itself and the earlier French words), add and norm, cross-attention (it reads
the English words), add and norm, the feed-forward network (itself only), add and norm, then the linear layer and the
softmax. Line widths are the real attention weights (mean of 4 heads) of the 2 + 2 block transformer trained in the
transformer inference Note. Data: data/decoder_step.json.
Run: python decoder_flow_anim.py -> decoder_flow_anim.mp4, .gif, _frames.png (Manim)"""
import json
import shutil
import subprocess
from pathlib import Path

from manim import *
from PIL import Image

HERE = Path(__file__).parent
BLUE_C, ORANGE_C, GREEN_C, RED_C, PURPLE_C, GREY_C = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#B279A2", "#6B6B6B"
Text.set_default(color=BLACK, font="Latin Modern Roman")
MarkupText.set_default(color=BLACK, font="Latin Modern Roman")
D = json.load(open(HERE.parent / "data" / "decoder_step.json"))
SELF, CROSS = D["self_weights_block2"], D["cross_weights_block2"]


def sub(label, col, y, x=0.9):
    b = RoundedRectangle(corner_radius=0.12, width=4.4, height=0.62, color=col, fill_color=col, fill_opacity=0.1,
                         stroke_width=3).move_to([x, y, 0])
    return VGroup(b, Text(label, font_size=22).move_to(b))


class DecoderFlow(Scene):
    def snap(self):
        self.snaps.append(Image.fromarray(self.renderer.get_frame()))

    def construct(self):
        self.snaps = []
        title = Text("One position through the last decoder block", font_size=30).to_edge(UP, buff=0.2)
        fr = VGroup(*[Text(w.replace("<", "<").replace(">", ">"), font_size=24, color=ORANGE_C) for w in D["decoder_input"]])
        fr.arrange(RIGHT, buff=0.6).move_to([0.9, -3.2, 0])
        en = VGroup(*[Text(w, font_size=24, color=BLUE_C) for w in D["english"]]).arrange(DOWN, buff=0.45).move_to([-5.2, 0.2, 0])
        en_l = Text("English (encoder output)", font_size=20, color=BLUE_C).next_to(en, UP, buff=0.3)
        fr_l = Text("French input so far:", font_size=20, color=ORANGE_C).next_to(fr, LEFT, buff=0.4)
        self.play(FadeIn(title), FadeIn(fr), FadeIn(fr_l), FadeIn(en), FadeIn(en_l), run_time=0.8)
        me = SurroundingRectangle(fr[-1], color=RED_C, buff=0.08)
        self.play(Create(me), run_time=0.5)
        ys = [-2.2, -1.45, -0.7, 0.05, 0.8, 1.55]
        boxes = [sub("masked self-attention", PURPLE_C, ys[0]), sub("add & norm", GREY_C, ys[1]),
                 sub("cross-attention", GREEN_C, ys[2]), sub("add & norm", GREY_C, ys[3]),
                 sub("feed-forward network", BLUE_C, ys[4]), sub("add & norm", GREY_C, ys[5])]
        # 1. masked self-attention: lines from "sommes" to itself and earlier words
        self.play(FadeIn(boxes[0]), run_time=0.5)
        lines = VGroup(*[Line(boxes[0].get_bottom(), fr[k].get_top(), color=PURPLE_C, stroke_width=1 + 14 * w,
                              stroke_opacity=0.3 + 0.7 * w) for k, w in enumerate(SELF)])
        labs = VGroup(*[Text(f"{w:.2f}", font_size=20, color=PURPLE_C).next_to(fr[k], DOWN, buff=0.1)
                        for k, w in enumerate(SELF)])
        self.play(Create(lines), FadeIn(labs), run_time=1.0)
        n1 = Text("itself and earlier\nwords only", font_size=20, color=PURPLE_C).next_to(boxes[0], RIGHT, buff=0.2)
        self.play(FadeIn(n1))
        self.wait(0.8)
        self.snap()
        self.play(FadeIn(boxes[1]), FadeOut(n1), run_time=0.5)
        # 2. cross-attention to the English words
        self.play(FadeIn(boxes[2]), run_time=0.5)
        cl = VGroup(*[Line(boxes[2].get_left(), en[k].get_right(), color=GREEN_C, stroke_width=1 + 14 * w,
                           stroke_opacity=0.3 + 0.7 * w) for k, w in enumerate(CROSS)])
        cw = VGroup(*[Text(f"{w:.2f}", font_size=20, color=GREEN_C).next_to(en[k], LEFT, buff=0.2)
                      for k, w in enumerate(CROSS)])
        self.play(Create(cl), FadeIn(cw), run_time=1.0)
        n2 = Text("reads the English", font_size=20, color=GREEN_C).next_to(boxes[2], RIGHT, buff=0.2)
        self.play(FadeIn(n2))
        self.wait(0.8)
        self.snap()
        self.play(FadeIn(boxes[3]), FadeOut(n2), run_time=0.5)
        # 3. feed-forward network
        self.play(FadeIn(boxes[4]), run_time=0.5)
        n3 = Text("this position only", font_size=20, color=BLUE_C).next_to(boxes[4], RIGHT, buff=0.2)
        self.play(FadeIn(n3), FadeIn(boxes[5]), run_time=0.6)
        # output
        out = VGroup(*[Text(f"{w}  {p:.3f}", font_size=22, color=ORANGE_C if k == 0 else GREY_C)
                       for k, (w, p) in enumerate(D["top"][:3])]).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        lin = Text("linear + softmax: next word", font_size=22).move_to([0.9, 2.35, 0])
        out.next_to(lin, RIGHT, buff=0.4)
        self.play(FadeIn(lin), FadeIn(out), run_time=0.8)
        self.wait(0.6)
        self.snap()
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
                     "output_file": "decoder_flow_anim", "disable_caching": True, "verbosity": "WARNING",
                     "progress_bar": "none"}):
        scene = DecoderFlow()
        scene.render()
    mp4 = HERE / "decoder_flow_anim.mp4"
    shutil.copy(next(media.rglob("decoder_flow_anim.mp4")), mp4)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(mp4), "-vf",
                    "fps=12,scale=720:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "decoder_flow_anim.gif")], check=True)
    key_frames_grid(scene.snaps, HERE / "decoder_flow_anim_frames.png")
    shutil.rmtree(media)

"""Attention as a change added to the word's vector: e_bank + Δe, where Δe is the attention output (the weighted
value vectors, placed tip to tail). First in "money bank", then in "river bank". Numbers from data/vectors.csv.
Intuition after Sanderson (3Blue1Brown), "Attention in transformers, step-by-step", 2024 (13:12-15:44).
Run: python residual_nudge.py -> residual_nudge.mp4, residual_nudge.gif, residual_nudge_frames.png (Manim)"""
import shutil
import subprocess
from pathlib import Path

import numpy as np
import pandas as pd
from manim import *
from PIL import Image

HERE = Path(__file__).parent
BLUE_C, ORANGE_C, GREEN_C, RED_C, PURPLE_C, GREY_C = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#B279A2", "#6B6B6B"
Text.set_default(color=BLACK, font="Latin Modern Roman")
MarkupText.set_default(color=BLACK, font="Latin Modern Roman")
d = pd.read_csv(HERE.parent / "data" / "vectors.csv")


def vec(sentence, word, kind):
    r = d[(d.sentence == sentence) & (d.word == word) & (d.kind == kind)].iloc[0]
    return np.array([r.x, r.y])


def weight(sentence, other):
    return d[(d.sentence == sentence) & (d.word == "bank") & (d.kind == f"weight_{other}")].iloc[0].x


E = vec("money bank", "bank", "e")
CASES = []
for other, colour in (("money", BLUE_C), ("river", ORANGE_C)):
    s = f"{other} bank"
    w_o, w_b = weight(s, other), weight(s, "bank")
    pieces = [(w_o, vec(s, other, "v"), other), (w_b, vec(s, "bank", "v"), "bank")]
    delta = vec(s, "bank", "y")
    assert np.allclose(w_o * pieces[0][1] + w_b * pieces[1][1], delta, atol=1e-3)
    CASES.append(dict(sentence=s, other=other, pieces=pieces, delta=delta, colour=colour,
                      e_other=vec(s, other, "e")))
angle = lambda v: np.degrees(np.arctan2(v[1], v[0]))


class ResidualNudge(Scene):
    def snap(self):
        self.snaps.append(Image.fromarray(self.renderer.get_frame()))

    def construct(self):
        self.snaps = []
        ax = Axes(x_range=[0, 15, 5], y_range=[-3, 9, 3], x_length=7.4, y_length=6.3, tips=False,
                  axis_config=dict(color=GREY_C, stroke_width=2, include_numbers=True, font_size=26,
                                   decimal_number_config=dict(color=GREY_C, num_decimal_places=0)))
        ax.to_edge(LEFT, buff=0.5).shift(DOWN * 0.35)
        P = lambda v: ax.c2p(v[0], v[1])
        arrow = lambda a, b, c, w=6: Arrow(P(a), P(b), buff=0, color=c, stroke_width=w, max_tip_length_to_length_ratio=0.12,
                                           max_stroke_width_to_length_ratio=8)
        title = Text("Attention adds a change to the word's vector", font_size=32).to_edge(UP, buff=0.3)
        panel_x = 1.55
        self.play(FadeIn(title), Create(ax), run_time=1)
        e_arrow = arrow([0, 0], E, GREY_C, 7)
        e_lab = MarkupText("e<sub>bank</sub> = (7, 3)", font_size=26, color=GREY_C).next_to(P(E), DOWN + RIGHT, buff=0.1)
        self.play(GrowArrow(e_arrow), FadeIn(e_lab))
        line1 = MarkupText("the same vector in every sentence", font_size=26, color=GREY_C)
        line1.move_to([panel_x, 2.6, 0], aligned_edge=LEFT)
        self.play(FadeIn(line1))
        self.wait(0.8)
        self.snap()
        kept = []
        for k, c in enumerate(CASES):
            head = MarkupText(f'in "<b>{c["sentence"]}</b>"', font_size=30, color=c["colour"])
            head.move_to([panel_x, 1.8 - 2.3 * k, 0], aligned_edge=LEFT)
            ref = DashedLine(P([0, 0]), P(c["e_other"] * 1.0), color=c["colour"], stroke_width=2, dash_length=0.08)
            ref_lab = MarkupText(f"e<sub>{c['other']}</sub>", font_size=26, color=c["colour"]).next_to(P(c["e_other"]), UP if c["other"] == "money" else DOWN, buff=0.08)
            self.play(FadeIn(head), Create(ref), FadeIn(ref_lab), run_time=0.8)
            start, parts = E, VGroup()
            for w, v, name in c["pieces"]:
                a = arrow(start, start + w * v, RED_C, 5)
                lab = MarkupText(f"{w:.2f} v<sub>{name}</sub>", font_size=24, color=RED_C).next_to(a, LEFT if name == c["other"] else RIGHT, buff=0.25)
                self.play(GrowArrow(a), FadeIn(lab), run_time=0.9)
                parts.add(a, lab)
                start = start + w * v
            delta = arrow(E, E + c["delta"], PURPLE_C, 7)
            d_txt = MarkupText(f"Δe = ({c['delta'][0]:.2f}, {c['delta'][1]:.2f})", font_size=27, color=PURPLE_C)
            d_txt.next_to(head, DOWN, aligned_edge=LEFT, buff=0.15)
            self.play(GrowArrow(delta), FadeIn(d_txt), run_time=0.9)
            self.wait(0.6)
            if k == 0:
                self.snap()
            new = arrow([0, 0], E + c["delta"], c["colour"], 8)
            n_txt = MarkupText(f"e + Δe: {angle(E):.0f}° → {angle(E + c['delta']):.0f}°", font_size=27, color=c["colour"])
            n_txt.next_to(d_txt, DOWN, aligned_edge=LEFT, buff=0.15)
            self.play(GrowArrow(new), FadeIn(n_txt), run_time=1.0)
            self.wait(1.0)
            if k == 0:
                self.snap()
            self.play(FadeOut(parts), FadeOut(delta), FadeOut(ref), FadeOut(ref_lab), run_time=0.6)
            kept.append(new)
        note = VGroup(Text("same word, different context,", font_size=24),
                      Text("different change Δe", font_size=24),
                      Text("the addition is the residual connection", font_size=22, color=GREY_C)
                      ).arrange(DOWN, aligned_edge=LEFT, buff=0.1).move_to([panel_x, -3.0, 0], aligned_edge=LEFT)
        self.play(FadeIn(note), FadeOut(line1))
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
                     "output_file": "residual_nudge", "disable_caching": True, "verbosity": "WARNING",
                     "progress_bar": "none"}):
        scene = ResidualNudge()
        scene.render()
    mp4 = HERE / "residual_nudge.mp4"
    shutil.copy(next(media.rglob("residual_nudge.mp4")), mp4)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(mp4), "-vf",
                    "fps=12,scale=720:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "residual_nudge.gif")], check=True)
    key_frames_grid(scene.snaps, HERE / "residual_nudge_frames.png")
    shutil.rmtree(media)

"""Bayes' theorem as geometry, on the spam example of section 5.2: the square is all emails; a prior strip of
spam (20 percent); inside each strip the share that contains "free" (60 percent of spam, 5 percent of normal);
seeing "free" keeps only those two pieces; their areas 0.12 and 0.04, rescaled to fill the whole, give the
posterior 0.75. Intuition after Sanderson (3Blue1Brown), "Bayes theorem, the geometry of changing beliefs".
Run: python bayes_square.py -> bayes_square.gif, bayes_square_frames.png (Manim)"""
import shutil
import subprocess
from pathlib import Path

from manim import *
from PIL import Image

HERE = Path(__file__).parent
SPAM_C, NORM_C, GREY_C = "#F58518", "#4C78A8", "#6B6B6B"
Text.set_default(color=BLACK, font="Latin Modern Roman")
PRIOR, L_SPAM, L_NORM = 0.20, 0.60, 0.05
EVID = PRIOR * L_SPAM + (1 - PRIOR) * L_NORM
POST = PRIOR * L_SPAM / EVID
assert abs(EVID - 0.16) < 1e-12 and abs(POST - 0.75) < 1e-12      # the numbers of section 5.2
S = 5.6                                                            # side of the square (all emails)


def block(x0, w, h, color, opacity, corner):
    """Rectangle of width w and height h (fractions of S) with its bottom-left at corner + (x0, 0)."""
    r = Rectangle(width=w * S, height=h * S, stroke_color=WHITE, stroke_width=2, fill_color=color,
                  fill_opacity=opacity)
    return r.move_to(corner + RIGHT * (x0 + w / 2) * S + UP * h / 2 * S)


class BayesSquare(Scene):
    def snap(self):
        self.snaps.append(Image.fromarray(self.renderer.get_frame()))

    def title(self, text):
        t = Text(text, font_size=40, weight=BOLD).to_edge(UP, buff=0.3)
        if self.cur is None:
            self.play(FadeIn(t))
        else:
            self.play(ReplacementTransform(self.cur, t))
        self.cur = t

    def construct(self):
        self.snaps, self.cur = [], None
        corner = LEFT * 6.3 + DOWN * 3.3                          # bottom-left of the square
        side = RIGHT * 2.8 + UP * 1.2                             # where the right-hand notes start

        # 1. All emails
        self.title("1. All emails")
        whole = block(0, 1, 1, GREY_C, 0.25, corner)
        self.play(FadeIn(whole))

        # 2. Prior: split into spam and normal
        self.title("2. Prior: 20% are spam")
        spam, norm = block(0, PRIOR, 1, SPAM_C, 0.25, corner), block(PRIOR, 1 - PRIOR, 1, NORM_C, 0.25, corner)
        lab_s = Text("spam 20%", font_size=30, color=SPAM_C, weight=BOLD).next_to(spam, UP, buff=0.15, aligned_edge=LEFT)
        lab_n = Text("normal 80%", font_size=30, color=NORM_C, weight=BOLD).next_to(norm, UP, buff=0.15, aligned_edge=RIGHT)
        self.play(ReplacementTransform(whole, VGroup(spam, norm)), FadeIn(lab_s), FadeIn(lab_n))
        self.wait(0.6)
        self.snap()

        # 3. Likelihood: inside each strip, the share with "free"
        self.title('3. Likelihood: who says "free"?')
        free_s = block(0, PRIOR, L_SPAM, SPAM_C, 0.95, corner)
        free_n = block(PRIOR, 1 - PRIOR, L_NORM, NORM_C, 0.95, corner)
        note_s = Text('60% of spam say "free"', font_size=32, color=SPAM_C).move_to(side)
        note_n = Text('5% of normal say "free"', font_size=32, color=NORM_C).next_to(note_s, DOWN, buff=0.4, aligned_edge=LEFT)
        arr_n = Arrow(note_n.get_left(), free_n.get_right() + UP * 0.1, color=NORM_C, buff=0.15)
        in_s = Text("60%", font_size=30, color=WHITE, weight=BOLD).move_to(free_s)
        self.play(GrowFromEdge(free_s, DOWN), GrowFromEdge(free_n, DOWN), FadeIn(note_s), FadeIn(note_n),
                  GrowArrow(arr_n), run_time=1.5)
        self.play(FadeIn(in_s))
        self.wait(0.6)
        self.snap()

        # 4. Evidence: the email says "free", so everything else is ruled out
        self.title('4. The email says "free"')
        self.play(spam.animate.set_fill(opacity=0.04), norm.animate.set_fill(opacity=0.04),
                  FadeOut(lab_s), FadeOut(lab_n), FadeOut(arr_n), FadeOut(in_s), FadeOut(note_s), FadeOut(note_n))
        area_s = Text("0.2 × 0.6 = 0.12", font_size=34, color=SPAM_C, weight=BOLD).move_to(side)
        area_n = Text("0.8 × 0.05 = 0.04", font_size=34, color=NORM_C, weight=BOLD).next_to(
            area_s, DOWN, buff=0.4, aligned_edge=LEFT)
        total = Text("left: 0.16 of all emails", font_size=32).next_to(area_n, DOWN, buff=0.5, aligned_edge=LEFT)
        self.play(FadeIn(area_s), Indicate(free_s, color=SPAM_C, scale_factor=1.05))
        self.play(FadeIn(area_n), Indicate(free_n, color=NORM_C, scale_factor=1.05))
        self.play(FadeIn(total))
        self.wait(0.8)
        self.snap()

        # 5. Posterior: rescale what is left so it fills the whole
        self.title("5. Posterior: 75% spam")
        bar_w, bar_h = 6.0, 1.3
        bar_c = RIGHT * 0.2 + DOWN * 0.6
        new_s = Rectangle(width=bar_w * POST, height=bar_h, fill_color=SPAM_C, fill_opacity=0.95,
                          stroke_color=WHITE, stroke_width=2).move_to(bar_c + LEFT * bar_w * (1 - POST) / 2)
        new_n = Rectangle(width=bar_w * (1 - POST), height=bar_h, fill_color=NORM_C, fill_opacity=0.95,
                          stroke_color=WHITE, stroke_width=2).move_to(bar_c + RIGHT * bar_w * POST / 2)
        self.play(FadeOut(spam), FadeOut(norm), FadeOut(total), area_s.animate.shift(UP * 0.6),
                  area_n.animate.shift(UP * 0.6))
        self.play(ReplacementTransform(free_s, new_s), ReplacementTransform(free_n, new_n), run_time=2)
        pct_s = Text("75% spam", font_size=40, color=WHITE, weight=BOLD).move_to(new_s)
        pct_n = Text("25%", font_size=34, color=WHITE, weight=BOLD).move_to(new_n)
        frac = Text("0.12 / 0.16 = 0.75", font_size=40, weight=BOLD).next_to(VGroup(new_s, new_n), DOWN, buff=0.6)
        self.play(FadeIn(pct_s), FadeIn(pct_n), FadeIn(frac))
        self.wait(2.5)
        self.snap()


def grid(frames, out, cols=2, gap=16):
    w, h = frames[0].size
    rows = -(-len(frames) // cols)
    sheet = Image.new("RGB", (cols * w + (cols - 1) * gap, rows * h + (rows - 1) * gap), "white")
    for i, f in enumerate(frames):
        sheet.paste(f.convert("RGB"), ((i % cols) * (w + gap), (i // cols) * (h + gap)))
    sheet.save(out)


if __name__ == "__main__":
    media = HERE / ".manim"
    with tempconfig({"quality": "medium_quality", "background_color": WHITE, "media_dir": str(media),
                     "output_file": "bayes_square", "disable_caching": True, "verbosity": "WARNING",
                     "progress_bar": "none"}):
        scene = BayesSquare()
        scene.render()
    mp4 = next(media.rglob("bayes_square.mp4"))
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(mp4), "-vf",
                    "fps=12,scale=720:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "bayes_square.gif")], check=True)
    grid(scene.snaps, HERE / "bayes_square_frames.png")
    shutil.rmtree(media)

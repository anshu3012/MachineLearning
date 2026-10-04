"""The picture to draw for Bayes' theorem (section 5), on the librarian-or-farmer numbers of section 2.
A 1 x 1 square is all people. The librarians are a left strip of width P(H) = 1/21. The description keeps a
piece of height P(E | H) = 0.4 on the left and P(E | not H) = 0.1 on the right. The posterior is the left
piece's share of what is kept: 16.7 percent. Then the right height rises to 0.4: with equal heights the
evidence is irrelevant and the posterior returns to the prior, 4.8 percent.
Idea after Sanderson (3Blue1Brown), "Bayes theorem, the geometry of changing beliefs" (the unit-square diagram).
Run: python steve_square.py -> steve_square.gif, steve_square_frames.png (Manim)"""
import shutil
import subprocess

from bayes_square import *                      # block, grid, S, colours, fonts, HERE

LIB_C, FARM_C = SPAM_C, NORM_C
PRIOR, L_LIB, L_FARM = 1 / 21, 0.4, 0.1


def posterior(h_farm):
    return PRIOR * L_LIB / (PRIOR * L_LIB + (1 - PRIOR) * h_farm)


assert abs(posterior(L_FARM) - 4 / 24) < 1e-12 and abs(posterior(L_LIB) - PRIOR) < 1e-12


class SteveSquare(Scene):
    snap, title = BayesSquare.snap, BayesSquare.title

    def construct(self):
        self.snaps, self.cur = [], None
        corner = LEFT * 6.3 + DOWN * 3.0
        side = RIGHT * 3.2 + UP * 1.6
        h = ValueTracker(L_FARM)                                   # height of the farmers' piece

        self.title("1. Prior: 1 person in 21 is a librarian")
        lib, farm = block(0, PRIOR, 1, LIB_C, 0.25, corner), block(PRIOR, 1 - PRIOR, 1, FARM_C, 0.25, corner)
        lab_l = Text("librarians 1/21", font_size=28, color=LIB_C, weight=BOLD).next_to(lib, DOWN, buff=0.12, aligned_edge=LEFT)
        lab_f = Text("farmers 20/21", font_size=28, color=FARM_C, weight=BOLD).next_to(farm, UP, buff=0.15, aligned_edge=RIGHT)
        self.play(FadeIn(lib), FadeIn(farm), FadeIn(lab_l), FadeIn(lab_f))
        self.wait(0.8)
        self.snap()

        self.title("2. Likelihood: who fits the description?")
        fit_l = block(0, PRIOR, L_LIB, LIB_C, 0.95, corner)
        fit_f = always_redraw(lambda: block(PRIOR, 1 - PRIOR, h.get_value(), FARM_C, 0.95, corner))
        note_l = Text("40% of librarians fit", font_size=30, color=LIB_C).move_to(side)
        note_f = always_redraw(lambda: Text(f"{100 * h.get_value():.0f}% of farmers fit", font_size=30, color=FARM_C)
                               .next_to(note_l, DOWN, buff=0.35, aligned_edge=LEFT))
        self.play(GrowFromEdge(fit_l, DOWN), FadeIn(fit_f), FadeIn(note_l), FadeIn(note_f), run_time=1.5)
        self.wait(0.8)
        self.snap()

        self.title("3. Keep only the people who fit")
        self.play(lib.animate.set_fill(opacity=0.04), farm.animate.set_fill(opacity=0.04))
        self.wait(0.5)

        self.title("4. Posterior: the librarians' share of what is kept")
        bar_w, bar_h, bar_l = 5.2, 0.9, RIGHT * 0.6 + DOWN * 1.4       # bar's left edge

        def bar():
            p = posterior(h.get_value())
            a = Rectangle(width=bar_w * p, height=bar_h, fill_color=LIB_C, fill_opacity=0.95, stroke_color=WHITE,
                          stroke_width=2).move_to(bar_l + RIGHT * bar_w * p / 2)
            b = Rectangle(width=bar_w * (1 - p), height=bar_h, fill_color=FARM_C, fill_opacity=0.95,
                          stroke_color=WHITE, stroke_width=2).move_to(bar_l + RIGHT * bar_w * (p + (1 - p) / 2))
            t = Text(f"librarian: {100 * p:.1f}%", font_size=38, weight=BOLD, color=LIB_C).next_to(
                VGroup(a, b), DOWN, buff=0.3, aligned_edge=LEFT)
            return VGroup(a, b, t)

        share = always_redraw(bar)
        cap = Text("of the people who fit:", font_size=30).move_to(bar_l + UP * 0.95, aligned_edge=LEFT)
        self.play(FadeIn(cap), FadeIn(share))
        self.wait(1.5)
        self.snap()

        self.title("5. Equal heights: the belief does not move")
        self.play(h.animate.set_value(L_LIB), run_time=4)
        same = Text("posterior = prior = 1/21", font_size=32, weight=BOLD).next_to(share, DOWN, buff=0.3, aligned_edge=LEFT)
        self.play(FadeIn(same))
        self.wait(2.5)
        self.snap()


if __name__ == "__main__":
    media = HERE / ".manim"
    with tempconfig({"quality": "medium_quality", "background_color": WHITE, "media_dir": str(media),
                     "output_file": "steve_square", "disable_caching": True, "verbosity": "WARNING",
                     "progress_bar": "none"}):
        scene = SteveSquare()
        scene.render()
    mp4 = next(media.rglob("steve_square.mp4"))
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(mp4), "-vf",
                    "fps=12,scale=720:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "steve_square.gif")], check=True)
    grid(scene.snaps, HERE / "steve_square_frames.png")
    shutil.rmtree(media)

"""Out-of-bag evaluation: 6 rows, 4 trees; each row is predicted only by the trees whose bootstrap sample missed it.
Run: python oob_vote.py  -> oob_vote.mp4, oob_vote.gif, oob_vote_frames.png"""
import shutil
import subprocess
from pathlib import Path

from manim import *
from PIL import Image

HERE = Path(__file__).parent
BLUE_C, ORANGE_C, GREEN_C, RED_C, GREY_C = "#4C78A8", "#F58518", "#54A24B", "#E45756", "#6B6B6B"
Text.set_default(color=BLACK, font="Latin Modern Roman")

TRUE = [1, 0, 1, 0, 1, 0]                      # true class of rows 1..6
SAMPLES = [[1, 1, 2, 4, 5, 5], [2, 3, 3, 4, 6, 6], [1, 3, 4, 4, 5, 6], [1, 2, 2, 3, 6, 6]]   # bootstrap draws
VOTES = {(0, 1): 1, (1, 2): 0, (2, 0): 0, (3, 3): 0, (4, 1): 1, (4, 3): 1, (5, 0): 0}   # (row, tree): OOB vote
CELL = 0.62


class OOBVote(Scene):
    def snap(self):
        self.snaps.append(Image.fromarray(self.renderer.get_frame()))

    def construct(self):
        self.snaps = []
        title = Text("Out-of-bag evaluation: each row is judged only by trees that never saw it", font_size=28)
        title.to_edge(UP, buff=0.3)
        x0, y0 = -2.2, 2.1                                    # top-left cell centre
        pos = lambda r, t: np.array([x0 + t * 1.35, y0 - r * CELL, 0])
        heads = VGroup(*[Text(f"tree {t + 1}", font_size=22).move_to(pos(0, t) + UP * 0.6) for t in range(4)])
        rows = VGroup(*[Text(f"row {r + 1}   y = {TRUE[r]}", font_size=22).move_to(pos(r, 0) + LEFT * 2.3)
                        for r in range(6)])
        self.add(title, heads, rows)

        # 1. the bootstrap samples: blue cells = rows a tree was trained on (with the count), white = out-of-bag
        cells = {}
        for t, s in enumerate(SAMPLES):
            anims = []
            for r in range(6):
                k = s.count(r + 1)
                box = Rectangle(width=1.1, height=CELL * 0.85, stroke_width=2,
                             color=BLUE_C if k else ORANGE_C).set_fill(BLUE_C if k else WHITE, opacity=0.35 if k else 1)
                box.move_to(pos(r, t))
                lab = Text(f"x{k}" if k > 1 else ("seen" if k else "OOB"), font_size=19,
                           color=BLACK if k else ORANGE_C).move_to(box)
                cells[(r, t)] = VGroup(box, lab)
                anims.append(FadeIn(cells[(r, t)]))
            self.play(*anims, run_time=0.5)
            if t == 1:
                self.snap()
        key = Text("blue: in the tree's bootstrap sample    orange: out-of-bag (OOB) for that tree",
                   font_size=20, color=GREY_C).to_edge(DOWN, buff=0.35)
        self.play(FadeIn(key), run_time=0.4)
        self.wait(0.6)
        self.snap()

        # 2. each row: ask only its OOB trees, take the vote, compare with the truth
        pred_head = Text("OOB vote", font_size=22).move_to(pos(0, 4) + UP * 0.6 + RIGHT * 0.5)
        self.play(FadeIn(pred_head), run_time=0.3)
        correct = 0
        for r in range(6):
            band = SurroundingRectangle(VGroup(rows[r], cells[(r, 3)]), color=GREY_C, buff=0.06, stroke_width=2)
            self.play(Create(band), run_time=0.25)
            votes = []
            for t in range(4):
                if (r, t) in VOTES:
                    v = VOTES[(r, t)]
                    votes.append(v)
                    lab = cells[(r, t)][1]
                    self.play(Transform(lab, Text(f"says {v}", font_size=19, color=ORANGE_C).move_to(lab)), run_time=0.3)
            p = max(set(votes), key=votes.count)
            ok = p == TRUE[r]
            correct += ok
            mark = Text(f"{p}  {'right' if ok else 'wrong'}", font_size=22, color=GREEN_C if ok else RED_C)
            self.play(FadeIn(mark.move_to(pos(r, 4) + RIGHT * 0.5)), FadeOut(band), run_time=0.35)
            if r == 2:
                self.snap()
        result = Text(f"OOB score = {correct} right / 6 rows = {correct / 6:.2f}", font_size=28, color=GREEN_C)
        result.next_to(rows, DOWN, buff=0.45).set_x(0)
        self.play(FadeOut(key), FadeIn(result), run_time=0.6)
        self.wait(1.5)
        self.snap()


def key_frames_grid(frames, out, gap=16):
    w, hgt = frames[0].size
    sheet = Image.new("RGB", (2 * w + gap, 2 * hgt + gap), "white")
    for i, f in enumerate(frames[:4]):
        sheet.paste(f.convert("RGB"), ((i % 2) * (w + gap), (i // 2) * (hgt + gap)))
    sheet.save(out)


if __name__ == "__main__":
    media = HERE / ".manim"
    with tempconfig({"quality": "medium_quality", "background_color": WHITE, "media_dir": str(media),
                     "output_file": "oob_vote", "disable_caching": True, "verbosity": "WARNING",
                     "progress_bar": "none"}):
        scene = OOBVote()
        scene.render()
    mp4 = HERE / "oob_vote.mp4"
    shutil.copy(next(media.rglob("oob_vote.mp4")), mp4)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(mp4), "-vf",
                    "fps=12,scale=720:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "oob_vote.gif")], check=True)
    key_frames_grid(scene.snaps, HERE / "oob_vote_frames.png")
    shutil.rmtree(media)

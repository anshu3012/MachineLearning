"""P-value for 100 tosses of a fair coin: the binomial PMF under H0 (p = 0.5), with the bars at or beyond the
observed number of heads in red. Their total height is the p-value. Observed 53 -> 60 -> 65 -> 80 heads.
Run: python coin_p_value.py  -> coin_p_value.mp4, coin_p_value.gif, coin_p_value_frames.png"""
import shutil
import subprocess
from pathlib import Path

from manim import *
from PIL import Image
from scipy import stats

HERE = Path(__file__).parent
BLUE_C, RED_C, GREY_C = "#4C78A8", "#E45756", "#6B6B6B"
Text.set_default(color=BLACK, font="Latin Modern Roman")
KS = range(25, 86)
PMF = {k: stats.binom.pmf(k, 100, 0.5) for k in KS}


def p_text(k):
    p = stats.binom.sf(k - 1, 100, 0.5)
    return f"{p:.3f}" if p >= 0.001 else "0.0000000006"


class CoinPValue(Scene):
    def snap(self):
        self.snaps.append(Image.fromarray(self.renderer.get_frame()))

    def construct(self):
        self.snaps = []
        axes = Axes(x_range=[25, 85, 5], y_range=[0, 0.085, 0.02], x_length=11, y_length=4.6,
                    axis_config={"color": BLACK, "include_tip": False},
                    x_axis_config={"numbers_to_include": range(30, 85, 10), "font_size": 26,
                                   "decimal_number_config": {"num_decimal_places": 0, "color": BLACK}},
                    ).shift(DOWN * 0.3)
        xlab = Text("number of heads in 100 tosses", font_size=26, color=GREY_C).next_to(axes, DOWN, buff=0.3)
        title = Text("If the coin is fair (H₀), how unusual is our result?", font_size=32).to_edge(UP, buff=0.35)
        bars = VGroup()
        for k in KS:
            top = axes.c2p(k, PMF[k])
            base = axes.c2p(k, 0)
            w = (axes.c2p(1, 0)[0] - axes.c2p(0, 0)[0]) * 0.8
            bars.add(Rectangle(width=w, height=max(top[1] - base[1], 0.001), stroke_width=0,
                               fill_color=BLUE_C, fill_opacity=0.85).move_to(base, aligned_edge=DOWN))
        self.play(FadeIn(title), Create(axes), FadeIn(xlab), FadeIn(bars, lag_ratio=0.02), run_time=2)

        label, marker = None, None
        for k in [53, 60, 65, 80]:
            new_marker = DashedLine(axes.c2p(k - 0.5, 0), axes.c2p(k - 0.5, 0.075), color=BLACK, stroke_width=3)
            anims = [b.animate.set_fill(RED_C if kk >= k else BLUE_C) for b, kk in zip(bars, KS)]
            new_label = VGroup(
                Text(f"observed: {k} heads", font_size=30),
                Text(f"p-value = P(X ≥ {k}) = {p_text(k)}", font_size=30, color=RED_C),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_corner(UR, buff=0.4).shift(DOWN * 0.9)
            anims.append(FadeIn(new_label) if label is None else Transform(label, new_label))
            anims.append(Create(new_marker) if marker is None else Transform(marker, new_marker))
            self.play(*anims, run_time=1.2)
            if label is None:
                label, marker = new_label, new_marker
            self.wait(1.0)
            self.snap()
        self.wait(1)


def key_frames_grid(frames, out, gap=16):
    w, h = frames[0].size
    sheet = Image.new("RGB", (2 * w + gap, 2 * h + gap), "white")
    for i, f in enumerate(frames[:4]):
        sheet.paste(f.convert("RGB"), ((i % 2) * (w + gap), (i // 2) * (h + gap)))
    sheet.save(out)


if __name__ == "__main__":
    media = HERE / ".manim"
    with tempconfig({"quality": "medium_quality", "background_color": WHITE, "media_dir": str(media),
                     "output_file": "coin_p_value", "disable_caching": True, "verbosity": "WARNING",
                     "progress_bar": "none"}):
        scene = CoinPValue()
        scene.render()
    mp4 = HERE / "coin_p_value.mp4"
    shutil.copy(next(media.rglob("coin_p_value.mp4")), mp4)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(mp4), "-vf",
                    "fps=12,scale=720:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / "coin_p_value.gif")], check=True)
    key_frames_grid(scene.snaps, HERE / "coin_p_value_frames.png")
    shutil.rmtree(media)

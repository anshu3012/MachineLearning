"""Naive Bayes on word counts (sections 2 and 9), with our own small example: 12 normal messages (20 words)
and 6 spam messages (10 words), over four words.
spam_scores.gif: each likelihood P(word | class) is a bar height divided by the class total; the message
  "hello free" is scored by multiplying the prior with the two likelihoods: 0.045 (normal) against 0.027 (spam).
spam_zero.gif: "meeting prize prize prize" gets spam score 0, because "meeting" never appeared in spam; adding
  1 to every count (alpha = 1) removes the zero and the message is classified as spam.
Idea after StatQuest, "Naive Bayes, Clearly Explained!!!" (word histograms, the added counts); numbers are ours.
Run: python spam_words.py -> spam_scores.gif, spam_zero.gif and their _frames.png (Plotly frames + ffmpeg)"""
import shutil
import subprocess
from pathlib import Path

import plotly.graph_objects as go
from PIL import Image
from plotly.subplots import make_subplots

HERE = Path(__file__).parent
WORDS = ["hello", "meeting", "free", "prize"]
COUNTS = {"normal": [9, 7, 3, 1], "spam": [2, 0, 4, 4]}
MESSAGES = {"normal": 12, "spam": 6}
COLOR = {"normal": "#4C78A8", "spam": "#F58518"}
FONT = dict(family="Latin Modern Roman", size=24, color="black")
PRIOR = {c: MESSAGES[c] / sum(MESSAGES.values()) for c in COUNTS}


def lik(cls, word, alpha=0):
    return (COUNTS[cls][WORDS.index(word)] + alpha) / (sum(COUNTS[cls]) + alpha * len(WORDS))


def score(cls, message, alpha=0):
    s = PRIOR[cls]
    for w in message:
        s *= lik(cls, w, alpha)
    return s


M1, M2 = ["hello", "free"], ["meeting", "prize", "prize", "prize"]
assert round(score("normal", M1), 3) == 0.045 and round(score("spam", M1), 3) == 0.027     # section 2
assert score("spam", M2) == 0 and score("normal", M2) > 0                                  # section 9
assert score("spam", M2, 1) > score("normal", M2, 1)
print({c: (score(c, M1), score(c, M2), score(c, M2, 1)) for c in COUNTS})


def frame(title, labels="count", lit=(), alpha=0, lines=None, verdict=""):
    """labels: 'count' or 'frac'; lit: words of the message to highlight; lines: text under each chart."""
    fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.08, subplot_titles=[
        f"<b>{c}</b>: {MESSAGES[c]} messages, {sum(COUNTS[c]) + alpha * len(WORDS)} words" for c in COUNTS])
    for j, cls in enumerate(COUNTS):
        total = sum(COUNTS[cls]) + alpha * len(WORDS)
        op = [1 if (not lit or w in lit) else 0.25 for w in WORDS]
        text = [str(n) for n in COUNTS[cls]] if labels == "count" else \
               [f"{n + alpha}/{total}<br>= {(n + alpha) / total:.2f}" for n in COUNTS[cls]]
        if alpha:
            fig.add_trace(go.Bar(x=WORDS, y=COUNTS[cls], marker=dict(color=COLOR[cls], opacity=op)), 1, j + 1)
            fig.add_trace(go.Bar(x=WORDS, y=[alpha] * 4, marker=dict(color="black", opacity=op), text=text,
                                 textposition="outside", cliponaxis=False), 1, j + 1)
        else:
            fig.add_trace(go.Bar(x=WORDS, y=COUNTS[cls], marker=dict(color=COLOR[cls], opacity=op), text=text,
                                 textposition="outside", cliponaxis=False), 1, j + 1)
        if lines:
            fig.add_annotation(xref=f"x{j + 1 if j else ''} domain", yref="paper", x=0.5, y=-0.36, showarrow=False,
                               text=lines[cls], font=dict(size=25, color=COLOR[cls]))
    if verdict:
        fig.add_annotation(xref="paper", yref="paper", x=0.5, y=-0.56, showarrow=False, text=f"<b>{verdict}</b>",
                           font=dict(size=28))
    fig.update_yaxes(range=[0, 13], title="times the word appears", title_font_size=22)
    fig.update_yaxes(title="", row=1, col=2)
    fig.update_layout(width=1200, height=720, font=FONT, template="simple_white", showlegend=False, barmode="stack",
                      title=dict(text=f"<b>{title}</b>", x=0.5, y=0.97, font_size=30),
                      margin=dict(l=70, r=20, t=120, b=250))
    fig.update_annotations(selector=lambda a: a.y is not None and a.y > 0.9, font_size=26)
    return fig


def save(name, seq):
    """seq: (figure, seconds to hold). Writes name.gif and a 2-column grid of all frames as name_frames.png."""
    tmp = HERE / f".{name}"
    tmp.mkdir(exist_ok=True)
    keys, n = [], 0
    for fig, hold in seq:
        png = tmp / f"{n:03d}.png"
        fig.write_image(png)
        keys.append(Image.open(png).convert("RGB"))
        for k in range(1, hold):
            shutil.copy(png, tmp / f"{n + k:03d}.png")
        n += hold
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "1", "-i", str(tmp / "%03d.png"), "-vf",
                    "fps=5,scale=900:-1:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse",
                    str(HERE / f"{name}.gif")], check=True)
    w, h = keys[0].size
    rows = -(-len(keys) // 2)
    sheet = Image.new("RGB", (2 * w + 16, rows * h + 16 * (rows - 1)), "white")
    for i, f in enumerate(keys):
        sheet.paste(f, ((i % 2) * (w + 16), (i // 2) * (h + 16)))
    sheet.save(HERE / f"{name}_frames.png")
    shutil.rmtree(tmp)


if __name__ == "__main__":
    pn, ps = PRIOR["normal"], PRIOR["spam"]
    save("spam_scores", [
        (frame("1. Count each word, per class"), 3),
        (frame("2. Likelihood = bar height ÷ total words of the class", "frac"), 4),
        (frame("3. New message “hello free”: start from the prior", "frac", M1,
               lines={"normal": f"prior 12/18 = {pn:.2f}", "spam": f"prior 6/18 = {ps:.2f}"}), 4),
        (frame("4. Multiply by the likelihood of each word", "frac", M1,
               lines={"normal": f"{pn:.2f} × 0.45 × 0.15 = {score('normal', M1):.3f}",
                      "spam": f"{ps:.2f} × 0.20 × 0.40 = {score('spam', M1):.3f}"},
               verdict="0.045 > 0.027: predict normal"), 6)])
    save("spam_zero", [
        (frame("1. New message “meeting prize prize prize”", "frac", M2,
               lines={"normal": f"{pn:.2f} × 0.35 × 0.05³ = {score('normal', M2):.5f}",
                      "spam": f"{ps:.2f} × <b>0</b> × 0.40³ = <b>0</b>"},
               verdict="One zero count: spam can never win"), 6),
        (frame("2. Add 1 to every count (black boxes)", "frac", (), 1), 4),
        (frame("3. Score the message again", "frac", M2, 1,
               lines={"normal": f"{pn:.2f} × 0.33 × 0.08³ = {score('normal', M2, 1):.5f}",
                      "spam": f"{ps:.2f} × 0.07 × 0.36³ = {score('spam', M2, 1):.5f}"},
               verdict="0.00108 > 0.00013: predict spam"), 6)])

"""Shared cricket numbers (no output when run): the 8-match example, query (toss lost, venue Mumbai, outlook sunny).
Win: prior 5/8, P(lost | win) 1/5, P(Mumbai | win) 2/5, P(sunny | win) 4/5. Loss: 3/8, 2/3, 2/3, 1/3."""
FACTORS = {"win": [5 / 8, 1 / 5, 2 / 5, 4 / 5], "loss": [3 / 8, 2 / 3, 2 / 3, 1 / 3]}
NAMES = ["prior P(C)", "× P(toss lost | C)", "× P(Mumbai | C)", "× P(sunny | C)"]
SCORE = {k: v[0] * v[1] * v[2] * v[3] for k, v in FACTORS.items()}
Z = sum(SCORE.values())
POST = {k: s / Z for k, s in SCORE.items()}
assert round(SCORE["win"], 3) == 0.040 and round(SCORE["loss"], 3) == 0.056 and round(POST["loss"], 2) == 0.58

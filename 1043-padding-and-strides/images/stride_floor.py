"""The case where the filter does not fit: a 3x3 filter on an image of 6 rows and 7 columns with stride 2.
It stops at rows 0 and 2 and columns 0, 2, 4 (a 2x3 feature map); the next jump down would need row 6, which
does not exist (dashed red box in the closing frames). Rounding down in the formula drops that position.
Plotly frames (the Note's sliding-window helper) because a window moves step by step. Our own design.
Run: python stride_floor.py -> stride_floor.gif, stride_floor_frames.png"""
from pathlib import Path
import numpy as np
from anim import animate

rng = np.random.default_rng(3)
X = rng.integers(0, 10, size=(6, 7))
K = np.array([[1, 0, -1], [1, 0, -1], [1, 0, -1]])
rows, cols = (6 - 3) // 2 + 1, (7 - 3) // 2 + 1
Z = animate("stride_floor", X, 3, kernel=K, stride=2, here=Path(__file__).parent, keys=(0, 2, 3, 6), height=600,
            ghost=(4, 0, "next jump down: needs rows 4, 5 and 6, but row 6 does not exist, so it is skipped"))
assert Z.shape == (rows, cols) == (2, 3)

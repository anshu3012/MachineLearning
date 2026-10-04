"""2x2 max pooling with stride 2 on a 4x4 feature map: each window keeps its largest value.
Run: python maxpool_slide.py -> maxpool_slide.gif, maxpool_slide_frames.png"""
from pathlib import Path
import numpy as np
from anim import animate

A = np.array([[1, 5, 2, 3], [2, 4, 0, 1], [7, 1, 4, 2], [3, 0, 1, 3]])
P = animate("maxpool_slide", A, 2, op="max", stride=2, here=Path(__file__).parent, keys=(0, 1, 2, 3), fsize=20,
            width=800, height=480, labels=("feature map (after ReLU)", None, "max pooled"))
assert (P == [[5, 3], [7, 4]]).all()

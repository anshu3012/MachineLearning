"""The filter's gradient as a convolution, on the example of section 8.2: the 2x2 gradient dL/dZ1 slides over the
3x3 input X like a filter; each stop fills one cell of dL/dW1. Plotly frames (sliding-window helper anim.py).
Run: python conv_backward_slide.py -> conv_backward_slide.gif, conv_backward_slide_frames.png"""
from pathlib import Path
import numpy as np
from anim import animate

X = np.arange(1, 10).reshape(3, 3)
dZ = np.array([[0.5, -1], [0.25, 2]])
G = animate("conv_backward_slide", X, 2, kernel=dZ, op="conv", here=Path(__file__).parent, keys=(0, 1, 2, 3),
            fsize=24, width=1000, height=470, fps=0.8,
            labels=("input X", "∂L/∂Z<sub>1</sub>", "∂L/∂W<sub>1</sub>"))
assert np.allclose(G, [[9.5, 11.25], [14.75, 16.5]])

"""Three stills of attention_2d.gif, one per section of the Note: the projections (section 4), the query compared
with the keys (section 5), and the weighted value vectors added tip to tail (section 6). Same data and drawing code.
Run: python attention_2d_stills.py -> stills_projections.png, stills_scores.png, stills_sum.png (Plotly)"""
from attention_2d import HERE, frames

for name, k in (("projections", 12), ("scores", 13), ("sum", 40)):
    frames[k].write_image(HERE / f"stills_{name}.png", scale=1.5)

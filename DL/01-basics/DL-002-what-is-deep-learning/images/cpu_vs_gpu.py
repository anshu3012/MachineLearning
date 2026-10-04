"""CPU vs GPU on matrix multiplication, from data/cpu_vs_gpu.json (made by experiments/cpu_vs_gpu.py on one laptop:
Intel Core i9-13900HK CPU, NVIDIA RTX 4060 Laptop GPU). Plotly."""
import json
from pathlib import Path

import plotly.graph_objects as go

HERE = Path(__file__).parent
R = json.load(open(HERE.parent / "data" / "cpu_vs_gpu.json"))
N = sorted(int(n) for n in R["CPU"]["seconds"])
cpu = [1000 * R["CPU"]["seconds"][str(n)] for n in N]
gpu = [1000 * R["GPU"]["seconds"][str(n)] for n in N]
speed = [c / g for c, g in zip(cpu, gpu)]
assert speed[-1] > 10 and speed[-1] > 3 * speed[0], speed

import math  # noqa: E402

fig = go.Figure()
X = list(range(len(N)))                                 # one evenly spaced position per size (each doubles)
fig.add_scatter(x=X, y=cpu, mode="lines+markers", name="CPU (Intel i9-13900HK)", line=dict(color="#F58518", width=4),
                marker=dict(size=12))
fig.add_scatter(x=X, y=gpu, mode="lines+markers", name="GPU (NVIDIA RTX 4060 Laptop)",
                line=dict(color="#54A24B", width=4), marker=dict(size=12))
for i, c, sp in zip(X, cpu, speed):
    fig.add_annotation(x=i, y=math.log10(c), text=f"<b>{sp:.1f}×</b>", showarrow=False, yshift=26, font=dict(size=20))
fig.update_layout(template="simple_white", width=1050, height=640, font=dict(family="Latin Modern Roman", size=21),
                  title=dict(text="Time to multiply two n × n matrices (labels: how many times faster the GPU is)",
                             x=0.5, font=dict(size=21)),
                  xaxis=dict(title="matrix size n", tickvals=X, ticktext=[f"{n:,}" for n in N], range=[-0.4, len(N) - 0.6]),
                  yaxis=dict(type="log", title="time (milliseconds, log scale)", tickvals=[0.1, 1, 10, 100, 1000],
                             ticktext=["0.1", "1", "10", "100", "1,000"], range=[-1.1, 3.6]),
                  legend=dict(x=0.02, y=0.98), margin=dict(l=90, r=30, t=70, b=80))
fig.write_image(HERE / "cpu_vs_gpu.png", scale=2)
print([round(v, 1) for v in speed])

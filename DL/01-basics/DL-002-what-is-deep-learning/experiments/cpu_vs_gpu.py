"""CPU vs GPU, measured on the operation a network spends its time on: multiplying two square matrices of float32
numbers (n = 256 to 8192), with TensorFlow. Each size is timed as the best of 5 runs after a warm-up, in a child
process that sees either no GPU or the GPU. Writes data/cpu_vs_gpu.json.
Run on a machine with an NVIDIA GPU: python experiments/cpu_vs_gpu.py"""
import json
import os
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
SIZES = [256, 512, 1024, 2048, 4096, 8192]


def child():
    os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "3")
    import tensorflow as tf
    res = {}
    for n in SIZES:
        a = tf.random.normal((n, n), seed=0)
        b = tf.random.normal((n, n), seed=1)
        (a @ b).numpy()                                   # warm-up
        best = []
        for _ in range(5):
            t = time.perf_counter()
            (a @ b).numpy()                               # .numpy() waits for the result
            best.append(time.perf_counter() - t)
        res[n] = min(best)
    gpus = tf.config.list_physical_devices("GPU")
    name = tf.config.experimental.get_device_details(gpus[0]).get("device_name", "GPU") if gpus else "CPU"
    print(json.dumps({"seconds": res, "device": name}))


if __name__ == "__main__":
    if len(sys.argv) > 1:
        child()
        sys.exit()
    out = {}
    for name, env in (("CPU", {"CUDA_VISIBLE_DEVICES": ""}), ("GPU", {})):
        r = subprocess.run([sys.executable, __file__, "child"], env={**os.environ, **env}, capture_output=True, text=True)
        out[name] = json.loads(r.stdout.strip().splitlines()[-1])
        print(name, out[name])
    out["cpu_name"] = next((l.split(":", 1)[1].strip() for l in open("/proc/cpuinfo") if l.startswith("model name")), "")
    json.dump(out, open(HERE / "data" / "cpu_vs_gpu.json", "w"), indent=1)

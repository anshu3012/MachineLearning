"""Transcribe audio/NNN.m4a with faster-whisper (large-v3, GPU) into NNN.whisper-en.txt (English translation, one segment per line).
Used for Videos whose YouTube captions are missing or unusable."""
import subprocess
import sys
import time
from pathlib import Path

import numpy as np

from faster_whisper import WhisperModel

here = Path(__file__).parent
model = WhisperModel("large-v3", device="cuda", compute_type="int8_float16")
for n in sys.argv[1:]:
    out = here / f"{n}.whisper-en.txt"
    if out.exists():
        continue
    t0 = time.time()
    raw = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", str(here / "audio" / f"{n}.m4a"), "-f", "s16le",
                          "-ac", "1", "-ar", "16000", "-"], capture_output=True, check=True).stdout
    audio = np.frombuffer(raw, np.int16).astype(np.float32) / 32768.0      # ffmpeg decode: avoids the PyAV version clash
    segments, info = model.transcribe(audio, task="translate", language="hi",
                                      beam_size=5, vad_filter=True)
    lines = [s.text.strip() for s in segments]
    out.write_text("\n".join(lines) + "\n")
    print(n, f"{info.duration / 60:.1f} min audio", f"{(time.time() - t0) / 60:.1f} min", len(" ".join(lines).split()), "words", flush=True)

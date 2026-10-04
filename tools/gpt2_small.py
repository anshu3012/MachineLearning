"""GPT-2 small (124M) in plain NumPy: weights, tokenizer and a forward pass that keeps every intermediate.

No torch / transformers. Weights come from Hugging Face `openai-community/gpt2/model.safetensors` by HTTP byte
ranges (one request per tensor, the way the 1077 Notebook reads BERT), cached as .npy files in
~/.cache/campusx/gpt2/ (override with $GPT2_CACHE). The first full load downloads about 500 MB; loading only the
embedding table (`load_wte`) downloads about 155 MB.

API
---
    import sys; sys.path.insert(0, "<repo>/tools"); import gpt2_small as g

    tok = g.tokenizer()                      # `tokenizers.Tokenizer` with GPT-2's BPE (tokenizer.json, cached)
    ids = g.encode("The capital of France is")   # list[int]
    g.decode(ids), g.tokens(ids)             # text, list of token strings ("Ġ" = leading space)

    W = g.load()                             # dict name -> np.float32 array, HF names: "wte.weight",
                                             # "h.0.attn.c_attn.weight" (in, out), ... ; mask buffers skipped
    g.load_wte()                             # just the 50,257 x 768 token-embedding (= unembedding) table
    g.n_params(W)                            # 124,439,808
    g.CONFIG                                 # n_layer 12, n_head 12, d 768, n_ctx 1024, vocab 50257

    out = g.forward(ids, W, hook=None)       # one sequence, T <= 1024 tokens
      out["resid"]     (13, T, 768)  residual stream entering block 0..11, and after block 11 (before ln_f)
      out["resid_mid"] (12, T, 768)  residual after the attention sub-block of each layer
      out["attn"]      (12, 12, T, T) attention pattern [layer, head, query, key]; rows sum to 1, causal
      out["attn_out"]  (12, T, 768)  what each attention sub-block adds to the stream (after c_proj)
      out["mlp_pre"]   (12, T, 3072) MLP hidden values before GELU
      out["mlp_act"]   (12, T, 3072) after GELU ("neurons")
      out["mlp_out"]   (12, T, 768)  what each MLP sub-block adds to the stream
      out["final"]     (T, 768)      ln_f(resid[-1])
      out["logits"]    (T, 50257)    final @ wte.T  (tied unembedding; see `unembed`)

    hook(name, layer, x) -> x  is called on "attn_out", "mlp_act" and "mlp_out" before use, so an ablation is
    e.g.  lambda n, l, x: 0 * x if (n, l) == ("mlp_out", 5) else x .

    g.logit_lens(out, W)                     # (13, T, 50257) logits read from every residual stream position
    g.softmax(z, T=1.0)                      # temperature softmax over the last axis
    g.generate(ids, W, n=20, T=0.0, seed=0)  # T=0: greedy; T>0: sample from softmax(logits / T)

Run `python gpt2_small.py` for the self-check (parameter count; " Paris" in the top-5 after
"The capital of France is"; greedy text equal to the Hugging Face "How to generate text" blog's).
Set OMP_NUM_THREADS to a small number on a busy machine: BLAS threads fighting for cores slow it 5-10x.
"""
import json
import os
import struct
import urllib.request
from pathlib import Path

import numpy as np

URL = "https://huggingface.co/openai-community/gpt2/resolve/main/"
CACHE = Path(os.environ.get("GPT2_CACHE", Path.home() / ".cache" / "campusx" / "gpt2"))
CONFIG = dict(n_layer=12, n_head=12, d=768, n_ctx=1024, vocab=50257, d_ff=3072, eps=1e-5)
_tok = None


def _get(url, a=None, b=None):
    headers = {"Range": f"bytes={a}-{b}"} if a is not None else {}
    return urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=120).read()


def _header():
    f = CACHE / "header.json"
    if not f.exists():
        CACHE.mkdir(parents=True, exist_ok=True)
        n = struct.unpack("<Q", _get(URL + "model.safetensors", 0, 7))[0]
        h = json.loads(_get(URL + "model.safetensors", 8, 8 + n - 1))
        h["__hlen__"] = n
        f.write_text(json.dumps(h))
    return json.loads(f.read_text())


def tensor(name):
    """One weight tensor by name (float32), downloaded once by byte range and cached."""
    f = CACHE / f"{name}.npy"
    if not f.exists():
        h = _header()
        s, e = h[name]["data_offsets"]
        off = 8 + h["__hlen__"]
        raw = _get(URL + "model.safetensors", off + s, off + e - 1)
        assert len(raw) == e - s, name
        np.save(f, np.frombuffer(raw, "<f4").reshape(h[name]["shape"]))
    return np.load(f)


def load():
    """All parameters (the 12 causal-mask buffers `h.N.attn.bias` are skipped: they are not learned)."""
    names = [k for k in _header() if not k.startswith("__") and not k.endswith(".attn.bias")]
    return {k: tensor(k) for k in names}


def load_wte():
    return tensor("wte.weight")


def n_params(W):
    return int(sum(v.size for v in W.values()))


def tokenizer():
    global _tok
    if _tok is None:
        from tokenizers import Tokenizer
        f = CACHE / "tokenizer.json"
        if not f.exists():
            CACHE.mkdir(parents=True, exist_ok=True)
            f.write_bytes(_get(URL + "tokenizer.json"))
        _tok = Tokenizer.from_file(str(f))
    return _tok


def encode(text):
    return tokenizer().encode(text).ids


def decode(ids):
    return tokenizer().decode(list(map(int, ids)))


def tokens(ids):
    return [tokenizer().id_to_token(int(i)) for i in ids]


def layer_norm(x, g, b, eps=CONFIG["eps"]):
    m = x.mean(-1, keepdims=True)
    v = ((x - m) ** 2).mean(-1, keepdims=True)
    return (x - m) / np.sqrt(v + eps) * g + b


def gelu(x):
    """GPT-2's `gelu_new` (tanh approximation of GELU, Hendrycks & Gimpel 2016)."""
    return 0.5 * x * (1 + np.tanh(np.sqrt(2 / np.pi) * (x + 0.044715 * x ** 3)))


def softmax(z, T=1.0):
    z = np.asarray(z, dtype=np.float64) / T
    z = z - z.max(-1, keepdims=True)
    e = np.exp(z)
    return e / e.sum(-1, keepdims=True)


def forward(ids, W, hook=None):
    hook = hook or (lambda name, layer, x: x)
    C = CONFIG
    T, H, d = len(ids), C["n_head"], C["d"]
    dh = d // H
    assert T <= C["n_ctx"]
    x = W["wte.weight"][ids] + W["wpe.weight"][:T]
    mask = np.triu(np.full((T, T), -np.inf, dtype=np.float32), 1)        # key after query -> -inf
    keep = {k: [] for k in ("resid", "resid_mid", "attn", "attn_out", "mlp_pre", "mlp_act", "mlp_out")}
    for l in range(C["n_layer"]):
        p = f"h.{l}."
        keep["resid"].append(x)
        a = layer_norm(x, W[p + "ln_1.weight"], W[p + "ln_1.bias"])
        q, k, v = np.split(a @ W[p + "attn.c_attn.weight"] + W[p + "attn.c_attn.bias"], 3, axis=-1)
        q, k, v = (m.reshape(T, H, dh).transpose(1, 0, 2) for m in (q, k, v))     # (H, T, dh)
        A = softmax(q @ k.transpose(0, 2, 1) / np.sqrt(dh) + mask).astype(np.float32)
        z = (A @ v).transpose(1, 0, 2).reshape(T, d)
        attn_out = hook("attn_out", l, z @ W[p + "attn.c_proj.weight"] + W[p + "attn.c_proj.bias"])
        x = x + attn_out
        keep["resid_mid"].append(x)
        m = layer_norm(x, W[p + "ln_2.weight"], W[p + "ln_2.bias"])
        pre = m @ W[p + "mlp.c_fc.weight"] + W[p + "mlp.c_fc.bias"]
        act = hook("mlp_act", l, gelu(pre))
        mlp_out = hook("mlp_out", l, act @ W[p + "mlp.c_proj.weight"] + W[p + "mlp.c_proj.bias"])
        x = x + mlp_out
        for key, val in (("attn", A), ("attn_out", attn_out), ("mlp_pre", pre), ("mlp_act", act), ("mlp_out", mlp_out)):
            keep[key].append(val)
    keep["resid"].append(x)
    out = {k: np.stack(v) for k, v in keep.items()}
    out["final"] = layer_norm(x, W["ln_f.weight"], W["ln_f.bias"])
    out["logits"] = unembed(out["final"], W)
    return out


def unembed(x, W):
    """x (..., 768) -> logits (..., 50257) = x . every row of wte (written as wte @ x.T: no 154 MB transpose copy)."""
    x = np.asarray(x, dtype=np.float32)
    return np.moveaxis(W["wte.weight"] @ x.reshape(-1, x.shape[-1]).T, 0, -1).reshape(*x.shape[:-1], -1)


def logit_lens(out, W):
    """Unembed every residual stream state with the final layer norm (nostalgebraist 2020): (13, T, vocab)."""
    return unembed(layer_norm(out["resid"], W["ln_f.weight"], W["ln_f.bias"]), W)


def generate(ids, W, n=20, T=0.0, seed=0):
    """Extend `ids` by n tokens. T = 0 takes the top token; otherwise samples from softmax(logits / T)."""
    rng, ids = np.random.default_rng(seed), list(ids)
    for _ in range(n):
        z = forward(ids[-CONFIG["n_ctx"]:], W)["logits"][-1]
        ids.append(int(z.argmax()) if T == 0 else int(rng.choice(len(z), p=softmax(z, T))))
    return ids


if __name__ == "__main__":
    W = load()
    assert n_params(W) == 124_439_808, n_params(W)
    assert W["wte.weight"].shape == (50257, 768) and "lm_head.weight" not in W     # tied unembedding
    ids = encode("The capital of France is")
    out = forward(ids, W)
    assert np.allclose(out["attn"].sum(-1), 1, atol=1e-5) and out["attn"][0, 0, 0, 1] == 0  # rows sum to 1, causal
    top = np.argsort(-out["logits"][-1])[:5]
    print("params:", n_params(W))
    print("top-5 after 'The capital of France is':", tokens(top), softmax(out["logits"][-1])[top].round(3))
    assert encode(" Paris")[0] in top
    lens = logit_lens(out, W)
    assert np.allclose(lens[-1], out["logits"], atol=1e-3)
    # greedy output published in the Hugging Face blog "How to generate text" (von Platen 2020, GPT-2 small)
    blog = ", but I'm not sure if I'll ever be able to walk with my dog. I'm not sure if I'll ever be able to walk"
    text = decode(generate(encode("I enjoy walking with my cute dog"), W, n=30))
    assert text.endswith(blog), text
    print("greedy matches the HF blog:", repr(text))

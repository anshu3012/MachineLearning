from check_pdf import missing

md = "## 1. Intro\n\nThe quick brown fox jumps over.\n\n> **Key point:** Lazy dogs sleep all day long.\n"
assert missing(md, "1. Intro The quick brown fox jumps over. Key point: Lazy dogs sleep all day long.") == []
assert missing(md, "1. Intro The quick brown fox jumps over.") == ["key point lazy dogs sleep"]
assert missing("A first fine finding here today.", "A \ufb01rst \ufb01ne \ufb01nding here today.") == []
print("ok")

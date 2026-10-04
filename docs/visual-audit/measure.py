import re, json, pathlib
root = pathlib.Path('/home/anshu/campusx')
SKIP = re.compile(r'summary|prerequisites|sources|key terms|references|further reading', re.I)
IMG = re.compile(r'!\[.*?\]\(([^)\s]+\.(?:png|gif|svg|jpe?g|webp))\)')
rows = []
for d in sorted(root.glob('[0-9]*-*/note.md'), key=lambda p: int(p.parent.name.split('-')[0])):
    t = d.read_text()
    title = re.search(r'^title:\s*"?(.*?)"?$', t, re.M); title = title.group(1) if title else d.parent.name
    t = re.sub(r'<!-- where-this-fits.*?<!-- /where-this-fits -->', '', t, flags=re.S)
    t = re.sub(r'^---.*?---', '', t, count=1, flags=re.S)
    # split into top-level sections
    parts = re.split(r'^## ', t, flags=re.M)[1:]
    secs = []; figs = gifs = words = 0; code = 0
    for p in parts:
        head = p.split('\n', 1)[0].strip()
        body = p.split('\n', 1)[1] if '\n' in p else ''
        if SKIP.search(head): continue
        imgs = [i for i in IMG.findall(body) if 'where_this_fits' not in i]
        g = sum(i.lower().endswith('.gif') for i in imgs)
        figs += len(imgs) - g; gifs += g
        code += len(re.findall(r'^```', body, re.M)) // 2
        prose = re.sub(r'```.*?```', '', body, flags=re.S)
        prose = re.sub(r'\$\$.*?\$\$', '', prose, flags=re.S)
        prose = IMG.sub('', prose)
        w = len(re.findall(r'[A-Za-z]{2,}', prose))
        words += w
        secs.append((head, len(imgs), w))
    numbered = [s for s in secs if re.match(r'\d+\.', s[0])]
    kp = re.search(r'\*\*Key point:\*\*\s*(.*)', t); kp = kp.group(1)[:220] if kp else ''
    imgdir = d.parent / 'images'
    files = sorted(x.name for x in imgdir.iterdir()) if imgdir.exists() else []
    gifn=[i for i in IMG.findall(t) if i.lower().endswith('.gif')]
    rows.append(dict(gifn=gifn, note=d.parent.name, title=title, figs=figs, gifs=gifs, code=code, words=words,
        nsec=len(numbered), secfig=sum(1 for s in numbered if s[1]), wpv=round(words / max(1, figs + gifs)),
        sections=[s[0] for s in numbered], kp=kp,
        scripts=[f for f in files if f.endswith(('.py', '.tex'))],
        unref_gif=[f for f in files if f.endswith('.gif') and f not in t]))
json.dump(rows, open(root/'docs/visual-audit/metrics.json', 'w'), indent=1)
for r in rows:
    print(f"{r['note'][:42]:42} f{r['figs']:2} g{r['gifs']} s{r['secfig']}/{r['nsec']} w{r['words']:5} wpv{r['wpv']:5} c{r['code']}")

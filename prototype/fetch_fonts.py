import re, base64, urllib.request, sys
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
url = ("https://fonts.googleapis.com/css2?family=Noto+Sans+Lao:wght@400;600;700"
       "&family=Noto+Serif+Lao:wght@600;700&family=Fraunces:wght@600;800&display=swap")
css = urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA})).read().decode()
groups = {}
for m in re.finditer(r"/\*\s*([\w-]+)\s*\*/\s*(@font-face\s*\{.*?\})", css, re.S):
    subset, block = m.group(1), m.group(2)
    fam = re.search(r"font-family:\s*'([^']+)'", block).group(1)
    if subset not in (("lao", "latin") if "Lao" in fam else ("latin",)):
        continue
    src = re.search(r"url\((https://[^)]+)\)", block).group(1)
    w = int(re.search(r"font-weight:\s*(\d+)", block).group(1))
    rng = re.search(r"unicode-range:\s*([^;]+);", block).group(1)
    g = groups.setdefault((fam, subset, src), {"w": [], "rng": rng})
    g["w"].append(w)
out = []
for (fam, subset, src), g in groups.items():
    data = urllib.request.urlopen(urllib.request.Request(src, headers={"User-Agent": UA})).read()
    b64 = base64.b64encode(data).decode()
    out.append(f"@font-face{{font-family:'{fam}';font-style:normal;font-weight:{min(g['w'])} {max(g['w'])};font-display:swap;"
               f"src:url(data:font/woff2;base64,{b64}) format('woff2');unicode-range:{g['rng']};}}")
    print(fam, subset, g["w"], len(data), file=sys.stderr)
open("fonts/fonts.css", "w").write("\n".join(out))

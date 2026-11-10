import re
from pathlib import Path

p = Path(r"c:\antigravity\影片\逆向研究\claude3d_工法\scene.html")
text = p.read_text(encoding="utf-8")

count = text.count('"NTC"')
print(f"Found {count} occurrences of \"NTC\"")

# Replace "NTC" with "Microsoft JhengHei", "Noto Sans TC", sans-serif
text = text.replace('"NTC"', '"Microsoft JhengHei", "Noto Sans TC", sans-serif')
p.write_text(text, encoding="utf-8")
print("Replaced all with Microsoft JhengHei fallback!")

import sys
from pathlib import Path

p = Path(r"c:\antigravity\影片\逆向研究\claude3d_工法\scene.html")
text = p.read_text(encoding="utf-8")

old_expose = "window.__letters = letters;"
new_expose = """window.__THREE = THREE;
window.__letters = letters;"""

if old_expose in text and "window.__THREE" not in text:
    text = text.replace(old_expose, new_expose)
    print("Exposed window.__THREE")

p.write_text(text, encoding="utf-8")

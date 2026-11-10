import sys
from pathlib import Path

p = Path(r"c:\antigravity\影片\逆向研究\claude3d_工法\scene.html")
text = p.read_text(encoding="utf-8")

old_expose = "window.__seekTo = (t) => renderAt(Math.max(0, Math.min(TOTAL - 1e-3, t)));"
new_expose = """window.__letters = letters;
window.__seekTo = (t) => renderAt(Math.max(0, Math.min(TOTAL - 1e-3, t)));"""

if old_expose in text:
    text = text.replace(old_expose, new_expose)
    print("Exposed window.__letters")

p.write_text(text, encoding="utf-8")

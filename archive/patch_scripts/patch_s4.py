import sys
from pathlib import Path

p = Path(r"c:\antigravity\影片\逆向研究\claude3d_工法\scene.html")
text = p.read_text(encoding="utf-8")

# 1. 頒獎台置中並稍微靠近，間距設為 [-1.22, 0.0, 1.22]
old_pod = "const podiums = [-1.45, 0.0, 1.45].map((x, i) => {"
new_pod = "const podiums = [-1.22, 0.0, 1.22].map((x, i) => {"
if old_pod in text:
    text = text.replace(old_pod, new_pod)
    print("1. Podiums spacing set to [-1.22, 0.0, 1.22]")

# 2. 小橘塊站位設在 x = -1.95, z = 0.55，身體微面向右上方領獎台
old_s4_hero = "hx = -2.35; hy = 0.0; hz = 0.70;"
new_s4_hero = "hx = -1.95; hy = 0.0; hz = 0.55;"
if old_s4_hero in text:
    text = text.replace(old_s4_hero, new_s4_hero)
    print("2. S4 Hero positioned at x = -1.95, z = 0.55 (golden left)")

# 3. 第 4 幕鏡頭後移並稍微拉高，確保三座台座與小橘塊完全收在視野黃金分割線內
old_cam_s4 = """  // Scene 4: 47.5 ~ 62.3s (頒獎台盛典)
  [48.0, [0.0, 2.5, 8.2],    [0.0, 1.1, 0]],
  [53.0, [0.0, 2.2, 7.6],    [0.0, 0.85, 0]],
  [57.0, [-0.2, 1.85, 6.2],  [0.0, 0.8, 0]],
  [TOTAL,[-0.3, 1.75, 5.8],  [0.0, 0.78, 0]],"""

new_cam_s4 = """  // Scene 4: 47.5 ~ 62.3s (頒獎台盛典：廣角寬敞構圖，三台與小人完美入鏡)
  [48.0, [-0.2, 2.4, 8.4],   [-0.1, 0.95, 0]],
  [53.0, [-0.2, 2.2, 7.8],   [-0.1, 0.85, 0]],
  [57.0, [-0.3, 2.0, 7.2],   [-0.1, 0.82, 0]],
  [TOTAL,[-0.3, 1.9, 6.8],   [-0.1, 0.80, 0]],"""

if old_cam_s4 in text:
    text = text.replace(old_cam_s4, new_cam_s4)
    print("3. S4 Camera widened to fit all 3 podiums and hero.")

p.write_text(text, encoding="utf-8")
print("S4 staging patched successfully!")

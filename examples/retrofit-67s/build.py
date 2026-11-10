# -*- coding: utf-8 -*-
"""把「既有 2D 簡報長片」與「3D 黏土角色引擎」組裝成一支自包含 composition。

來源（一律只讀，不要改它們）：
  SRC_DECK  既有長片：版面 markup、字幕、翻頁 GSAP、配音 <audio>
  SRC_CLAY  3D 黏土引擎：角色建構、材質、表情零件、特效
  ctrl.js   本範例的控制層（固定攝影機、螢幕像素走位、七通道情緒）

輸出：OUT（自包含，可直接 render）

用法：
  python build.py                 # 用下面的預設路徑
  python build.py <deck> <clay>   # 指定來源
"""
import pathlib
import re
import sys

# ---------------- 路徑設定（改版時只要改這裡） ----------------
HERE = pathlib.Path(__file__).resolve().parent
BASE = HERE.parents[2] if len(HERE.parents) > 2 else HERE

if len(sys.argv) >= 3:
    DECK = pathlib.Path(sys.argv[1]).resolve()
    CLAY = pathlib.Path(sys.argv[2]).resolve()
else:
    # 原始專案佈局：<專案>/mimo/index.html  +  <專案>/clay3d/index.html
    DECK = BASE / "mimo" / "index.html"
    CLAY = BASE / "clay3d" / "index.html"

CTRL = HERE / "ctrl.js"
OUT = HERE / "index.html"
# --------------------------------------------------------------


def between(text, start, end, label):
    i = text.find(start)
    if i < 0:
        raise SystemExit(f"找不到起點：{label}")
    i += len(start)
    j = text.find(end, i)
    if j < 0:
        raise SystemExit(f"找不到終點：{label}")
    return text[i:j], i, j


def strip_mascots(block):
    """移除 .mascot 區塊（多行 div）"""
    lines = block.split("\n")
    out, i, removed = [], 0, 0
    while i < len(lines):
        if 'class="mascot' in lines[i]:
            removed += 1
            i += 1
            while i < len(lines) and lines[i].strip() != "</div>":
                i += 1
            i += 1
            continue
        out.append(lines[i])
        i += 1
    return "\n".join(out), removed


deck = DECK.read_text(encoding="utf-8")
engine = CLAY.read_text(encoding="utf-8")
ctrl = CTRL.read_text(encoding="utf-8").rstrip() + "\n"

# ---------- 1. 既有長片的 CSS ----------
style, _, _ = between(deck, "    <style>\n", "\n    </style>", "deck style")

# 對比度：三個被 check 標記的橘字在奶油底上太淡，統一壓深（仍是品牌橙系）
for a, b in [
    ("#s0h2 b { color: #d96b44; font-size: 54px; }", "#s0h2 b { color: #b4502c; font-size: 54px; }"),
    ("#s6a .lb { color: #d96b44; font-weight: 800; }", "#s6a .lb { color: #b4502c; font-weight: 800; }"),
    ("#s7l2 { top: 412px; color: #c2552e; }", "#s7l2 { top: 412px; color: #b4502c; }"),
]:
    if a not in style:
        raise SystemExit("找不到樣式：" + a)
    style = style.replace(a, b, 1)

# ---------- 2. 既有長片的 #root markup ----------
markup, _, _ = between(deck, '      data-height="720"\n    >\n', "\n    </div>\n    <script>", "deck markup")
markup, n_mascot = strip_mascots(markup)

# 3D 畫布插在背景與地板之後、場景之前（z-index 5，永遠在文字與卡片之下）
needle = '      <div class="floor"></div>\n'
if needle not in markup:
    raise SystemExit("找不到 .floor")
markup = markup.replace(needle, needle + '      <canvas id="stage" class="clip" data-start="0" data-duration="67"></canvas>\n', 1)

# ---------- 3. 既有長片的 GSAP -------------
gsap, _, _ = between(deck, "    <script>\n", "\n    </script>", "deck gsap")
gsap_src = gsap.split("\n")
gsap_lines = []
n_tween = 0
i = 0
while i < len(gsap_src):
    ln = gsap_src[i]
    if re.search(r'"#s[0-7]m"', ln):
        n_tween += 1
        # tween 可能跨行：一路吃到分號為止
        while not ln.rstrip().endswith(";") and i + 1 < len(gsap_src):
            i += 1
            ln = gsap_src[i]
        i += 1
        continue
    gsap_lines.append(ln)
    i += 1
gsap = "\n".join(gsap_lines)

# ---------- 4. 黏土引擎的 3D 區塊 ----------
block, _, _ = between(engine, "      // ---------- 3D 黏土舞台（Three.js） ----------", "\n    </script>\n  </body>", "clay stage")
block = "      // ---------- 3D 黏土舞台（Three.js） ----------" + block

# 特效改掛在 hero 底下（跟著角色縮放與位移）
for a, b in [
    ("        scene.add(smokeGroup);", "        hero.add(smokeGroup);"),
    ("          scene.add(m);", "          hero.add(m);"),
    ("        scene.add(cloudGroup);", "        hero.add(cloudGroup);"),
    ("        scene.add(rainGroup);", "        hero.add(rainGroup);"),
    ("        cloudGroup.position.set(1.25, 2.0, 0);", "        cloudGroup.position.set(0, 1.88, 0.12);"),
    ("        rainGroup.position.set(1.25, 0, 0.05);", "        rainGroup.position.set(0, 0, 0.05);"),
    # 嘴巴：「哇」的圓嘴加厚，小尺寸時才不會看起來像甜甜圈
    ("new THREE.TorusGeometry(0.079, 0.031, 10, 22)", "new THREE.TorusGeometry(0.085, 0.048, 10, 24)"),
    # 冒煙：全部往角色右側（螢幕右邊）飄，避開左上方的「陣風 8 級」膠囊
    ("side: (i % 2 === 0 ? 1 : -1) * (0.12 + (i % 4) * 0.13)", "side: 0.18 + (i % 4) * 0.10"),
]:
    if a not in block:
        raise SystemExit("替換失敗：" + a)
    block = block.replace(a, b, 1)

# 控制層：從「鏡頭」到 window.__dbg 之後的 renderAt(0) 之前，整段換掉
start = block.find("        // ---- 鏡頭 ----")
if start < 0:
    raise SystemExit("找不到控制層起點")
dbg = block.find("        window.__dbg", start)
if dbg < 0:
    raise SystemExit("找不到 __dbg")
tail = block.find("        renderAt(0);", dbg)
if tail < 0:
    raise SystemExit("找不到 renderAt(0)")
block = block[:start] + ctrl + "\n" + block[tail:]

HTML = """<!doctype html>
<html lang="zh-Hant">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1280, height=720" />
    <title>Puti-AI · 天氣小學堂｜3D 黏土小吉 67 秒</title>
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
    <style>
{style}

      /* ---------- 3D 舞台（在文字與卡片之下、背景之上） ---------- */
      #stage {{
        position: absolute; inset: 0; width: 1280px; height: 720px;
        display: block; z-index: 5;
      }}
    </style>
    <script type="importmap">
      {{ "imports": {{ "three": "./assets/vendor/three/three.module.js" }} }}
    </script>
  </head>
  <body>
    <div
      id="root"
      data-composition-id="main"
      data-start="0"
      data-duration="67"
      data-width="1280"
      data-height="720"
    >
{markup}
    </div>
    <script>
{gsap}
    </script>
    <script>
{block}
    </script>
  </body>
</html>
"""

html = HTML.format(style=style, markup=markup, gsap=gsap, block=block)
OUT.write_text(html, encoding="utf-8")

print("index.html 已產生：%d 行 / %.1f KB" % (html.count("\n") + 1, len(html.encode()) / 1024))
print("移除平面小吉：%d 個，移除小吉 tween：%d 行" % (n_mascot, n_tween))
print("canvas:", '<canvas id="stage"' in html)
print("audio :", 'src="assets/audio/mix.wav"' in html)
print("3D    :", 'buildReady.clay' in html, '/ ctrl:', '67 秒版：固定攝影機' in html)

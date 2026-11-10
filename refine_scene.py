from pathlib import Path

html_p = Path(r"c:\antigravity\影片\逆向研究\claude3d_工法\scene.html")
code = html_p.read_text(encoding="utf-8")

# 1. 第一幕：小包裹排斥邏輯微調（避開胸前正中，讓小人全身露出來）
old_s1_slots = """// 嚴格避開小人本體 [-1.9, -1.1] x [-0.25, 0.55]，小箱子全部散落在四周環繞，絕不穿模！
for (let k = 0; k < N; k++) {
  const a = k * 2.39996;
  const r = 0.95 + Math.sqrt((k + 0.5) / N) * 1.85; // 離小人中心至少 0.95 米！
  const sx = -1.5 + Math.cos(a) * r * 1.25;
  const sz = 0.15 + Math.sin(a) * r * 0.95;
  slots.push({ x: sx, z: sz, y: 0.08 + (k % 4) * 0.14 });
}"""

new_s1_slots = """// 嚴格避開小人本體與正前胸視角，箱子散落在兩側與後方，主角清晰可見！
for (let k = 0; k < N; k++) {
  const a = k * 2.39996;
  const r = 1.05 + Math.sqrt((k + 0.5) / N) * 1.95;
  let sx = -1.5 + Math.cos(a) * r * 1.35;
  let sz = 0.15 + Math.sin(a) * r * 1.05;
  // 避開身前正下方錐形區域
  if (Math.abs(sx - (-1.5)) < 0.65 && sz > 0.0 && sz < 0.8) {
    sx += (sx >= -1.5 ? 0.6 : -0.6);
  }
  slots.push({ x: sx, z: sz, y: 0.08 + (k % 4) * 0.14 });
}"""
assert old_s1_slots in code, "old_s1_slots not found!"
code = code.replace(old_s1_slots, new_s1_slots)

# 2. 第二幕：小人站位 x = -0.85，收納盒 x = 0.75，小人微傾斜看標籤
code = code.replace("hx = lerp(-1.5, -0.75, eio(jumpU));", "hx = lerp(-1.5, -0.85, eio(jumpU));")
code = code.replace("hx = -0.75; hy = 0.0; rz = 0;", "hx = -0.85; hy = 0.0; rz = 0;")
code = code.replace("gazeTgt.set(0.85, 0.85, 0.25);\n          ry = 0.42;", "gazeTgt.set(0.85, 0.85, 0.25);\n          ry = 0.45; rx = 0.06;")

# 3. 第四幕：小人站位 x = -1.88, z = 0.85，完全不擋住第一個頒獎台！
old_s4_hero = """      // 站位在左側黃金點 x = -1.55, z = 0.55，整尊完完整整站在地面上，下半身絕不被切掉！
      hx = -1.55; hy = 0.0; hz = 0.55;
      ry = 0.42; // 側身 24 度朝向右上方中間冠軍台
      if (t < 52.0) {
        gazeTgt.set(0, 2.5, 0); // 看漏斗
      } else if (t < 56.5) {
        gazeTgt.set(0.0, 1.45, 0.0); // 專注仰望中間「首選推薦 B」！
        smiling = true;
      } else {
        gazeTgt.set(-0.2, 1.4, 5.0); // 轉向鏡頭與觀眾互動
        smiling = true;
        wink = t > 57.8 && t < 59.2; // 自信眨眼
        scaleY = 1.05 + Math.sin(t * 3.2) * 0.03;
        scaleX = 0.96;
      }"""

new_s4_hero = """      // 站位在左前方外側 x = -1.88, z = 0.85，完全不擋住第一個台子，黃金引薦身姿！
      hx = -1.88; hy = 0.0; hz = 0.85;
      ry = 0.52; // 側身 30 度指向中間冠軍台
      if (t < 52.0) {
        gazeTgt.set(0, 2.5, 0);
      } else if (t < 56.5) {
        gazeTgt.set(0.0, 1.5, 0.0); // 專注仰望中間冠軍卡片
        smiling = true;
        rx = -0.05; // 稍微抬頭仰望
      } else {
        gazeTgt.set(-0.3, 1.4, 5.5);
        smiling = true;
        rx = 0;
        wink = t > 57.8 && t < 59.2;
        scaleY = 1.05 + Math.sin(t * 3.2) * 0.03;
        scaleX = 0.96;
      }"""

assert old_s4_hero in code, "old_s4_hero not found!"
code = code.replace(old_s4_hero, new_s4_hero)

# 4. 彩帶避開小人新位置 (-1.88, 0.85)
code = code.replace("Math.hypot(cx - (-1.55), cz - 0.55) < 0.65", "Math.hypot(cx - (-1.88), cz - 0.85) < 0.75")

html_p.write_text(code, encoding="utf-8")
print("SUCCESS: Refined staging and clear-lines!")

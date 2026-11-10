from pathlib import Path

html_p = Path(r"c:\antigravity\影片\逆向研究\claude3d_工法\scene.html")
code = html_p.read_text(encoding="utf-8")

# 1. 第 2 幕分頁卡片繞行中心移至右側收納盒上方 (x = 0.85, z = 0.2)，小人在左側完全不被擋！
old_orbit = """    // 8 個分頁繞行半徑加大至 3.0m，絕不插小人臉！
    tabCards.forEach((c, idx) => {
      const spawnT = 17.5 + idx * 0.32;
      if (t < spawnT) { c.visible = false; return; }
      c.visible = true;

      const angle = (idx / 8) * Math.PI * 2 + orbitT * 0.38 + 0.45;
      const radius = 3.0;
      const wave = Math.sin(orbitT * 2.5 + idx * 0.8);
      const orbitPos = new THREE.Vector3(Math.cos(angle) * radius, 1.35 + wave * 0.15, Math.sin(angle) * radius);
      const targetPos = new THREE.Vector3(0.95, 0.85, 0.25 - idx * 0.015);

      c.position.lerpVectors(orbitPos, targetPos, collectE);
      c.rotation.set(wave * 0.08, -angle + Math.PI / 2, Math.cos(orbitT * 2 + idx) * 0.06);
      c.scale.setScalar(lerp(1, 0.40, collectE));
      if (collectU >= 1) c.visible = false;
    });"""

new_orbit = """    // 8 個分頁繞行中心設在右側 (x = 0.85, z = 0.2)，半徑 1.6m 盤旋，左側小人視野 100% 乾淨！
    tabCards.forEach((c, idx) => {
      const spawnT = 17.5 + idx * 0.32;
      if (t < spawnT) { c.visible = false; return; }
      c.visible = true;

      const angle = (idx / 8) * Math.PI * 2 + orbitT * 0.45 + 0.3;
      const radius = 1.65;
      const wave = Math.sin(orbitT * 2.5 + idx * 0.8);
      const orbitPos = new THREE.Vector3(0.85 + Math.cos(angle) * radius, 1.35 + wave * 0.18, 0.2 + Math.sin(angle) * 0.95);
      const targetPos = new THREE.Vector3(0.95, 0.85, 0.25 - idx * 0.015);

      c.position.lerpVectors(orbitPos, targetPos, collectE);
      c.rotation.set(wave * 0.08, -angle + Math.PI / 2, Math.cos(orbitT * 2 + idx) * 0.06);
      c.scale.setScalar(lerp(1, 0.40, collectE));
      if (collectU >= 1) c.visible = false;
    });"""

assert old_orbit in code, "old_orbit not found!"
code = code.replace(old_orbit, new_orbit)

# 2. 第 4 幕小人站位：從 -2.25 挪到 -1.75, z = 0.85，完整全身在畫面內！
old_s4_hero_pos = """      // 站位在最左側外邊 x = -2.25, z = 0.85，完全不擋任何展台！
      hx = -2.25; hy = 0.0; hz = 0.85;
      ry = 0.55; // 側身 32 度引薦中間推薦卡"""

new_s4_hero_pos = """      // 站位在左側黃金引薦位 x = -1.75, z = 0.85，全身完整露出，不被左邊緣切斷！
      hx = -1.75; hy = 0.0; hz = 0.85;
      ry = 0.48;"""

assert old_s4_hero_pos in code, "old_s4_hero_pos not found!"
code = code.replace(old_s4_hero_pos, new_s4_hero_pos)

# 3. 彩帶生成禁區：卡片前方徹底禁生彩帶，絕不遮擋任何卡片文字！
old_conf_rule = """    // 嚴格避開中央卡片與左側小人
    if (Math.abs(cx) < 1.1 && cz > -0.2 && cz < 0.6) continue;
    if (Math.hypot(cx - (-2.25), cz - 0.85) < 0.75) continue;"""

new_conf_rule = """    // 嚴格避開所有 3 張卡片正面 (cx 在 [-2.0, 2.0] 且 cz 在 [-0.3, 0.7]) 與小人身邊！
    if (Math.abs(cx) < 2.1 && cz > -0.3 && cz < 0.7) continue;
    if (Math.hypot(cx - (-1.75), cz - 0.85) < 0.75) continue;"""

assert old_conf_rule in code, "old_conf_rule not found!"
code = code.replace(old_conf_rule, new_conf_rule)

html_p.write_text(code, encoding="utf-8")
print("SUCCESS: Zero-clipping tabs & refined podium layout applied!")

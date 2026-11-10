import sys
from pathlib import Path

p = Path(r"c:\antigravity\影片\逆向研究\claude3d_工法\scene.html")
text = p.read_text(encoding="utf-8")

# 1. 調整材料粗糙度與金屬度，徹底排除拋光反光塑膠感
target_mat_start = "const M = {\n  orange:    new THREE.MeshStandardMaterial({ color: 0xc85624"
if target_mat_start in text:
    old_mat_block = """const M = {
  orange:    new THREE.MeshStandardMaterial({ color: 0xc85624, roughness: 0.65, metalness: 0.04 }), // 焦糖橘
  navy:      new THREE.MeshStandardMaterial({ color: 0x16223e, roughness: 0.55, metalness: 0.08 }), // 深海軍藍
  navyText:  new THREE.MeshStandardMaterial({ color: 0x182442, roughness: 0.45, metalness: 0.10 }),
  card:      new THREE.MeshStandardMaterial({ color: 0xbf8e54, roughness: 0.75, metalness: 0.02 }), // 牛皮紙箱卡片
  paper:     new THREE.MeshStandardMaterial({ color: 0xfbf8f2, roughness: 0.60, metalness: 0.0 }),  // 象牙米白紙卡
  metalGate: new THREE.MeshStandardMaterial({ color: 0x1c273e, roughness: 0.35, metalness: 0.65 }), // 緞面金屬
  yellow:    new THREE.MeshStandardMaterial({ color: 0xf59e0b, roughness: 0.50, metalness: 0.05 }), // 鉻黃
  red:       new THREE.MeshStandardMaterial({ color: 0xd93829, roughness: 0.55, metalness: 0.05 }), // 赤紅
  green:     new THREE.MeshStandardMaterial({ color: 0x059669, roughness: 0.50, metalness: 0.05 }), // 翡翠綠
  cheek:     new THREE.MeshBasicMaterial({ color: 0xf29179, transparent: true, opacity: 0.65 }),
  tape:      new THREE.MeshStandardMaterial({ color: 0xf3eee3, roughness: 0.5, transparent: true, opacity: 0.88 }),
  funnel:    new THREE.MeshStandardMaterial({ color: 0xf59e0b, roughness: 0.45, metalness: 0.15 }),
};"""
    new_mat_block = """const M = {
  orange:    new THREE.MeshStandardMaterial({ color: 0xc65322, roughness: 0.82, metalness: 0.0 }),  // 原片同款啞光熟成焦糖黏土
  navy:      new THREE.MeshStandardMaterial({ color: 0x152038, roughness: 0.75, metalness: 0.02 }), // 啞光深海軍藍
  navyText:  new THREE.MeshStandardMaterial({ color: 0x16223c, roughness: 0.65, metalness: 0.02 }),
  card:      new THREE.MeshStandardMaterial({ color: 0xb8884c, roughness: 0.88, metalness: 0.0 }),  // 啞光厚牛皮紙板
  paper:     new THREE.MeshStandardMaterial({ color: 0xfcfaf5, roughness: 0.85, metalness: 0.0 }),  // 啞光象牙純棉紙卡
  metalGate: new THREE.MeshStandardMaterial({ color: 0x182236, roughness: 0.55, metalness: 0.35 }), // 厚重啞光深鐵門
  yellow:    new THREE.MeshStandardMaterial({ color: 0xf29b05, roughness: 0.70, metalness: 0.0 }),  // 暖鉻黃黏土
  red:       new THREE.MeshStandardMaterial({ color: 0xd73525, roughness: 0.75, metalness: 0.0 }),  // 啞光赤紅
  green:     new THREE.MeshStandardMaterial({ color: 0x048a60, roughness: 0.75, metalness: 0.0 }),  // 啞光深翡翠綠
  cheek:     new THREE.MeshBasicMaterial({ color: 0xf28b72, transparent: true, opacity: 0.60 }),
  tape:      new THREE.MeshStandardMaterial({ color: 0xf4efe5, roughness: 0.80, transparent: true, opacity: 0.88 }),
  funnel:    new THREE.MeshStandardMaterial({ color: 0xf29b05, roughness: 0.70, metalness: 0.05 }),
};"""
    text = text.replace(old_mat_block, new_mat_block)
    print("1. Materials updated to matte clay.")

# 2. 地面接觸陰影強化 (Contact AO)
old_ao = """  grad.addColorStop(0, "rgba(22, 18, 14, 0.52)");
  grad.addColorStop(0.35, "rgba(32, 25, 20, 0.32)");
  grad.addColorStop(0.70, "rgba(45, 36, 28, 0.12)");
  grad.addColorStop(1, "rgba(0, 0, 0, 0)");"""
new_ao = """  grad.addColorStop(0, "rgba(16, 12, 8, 0.78)");
  grad.addColorStop(0.25, "rgba(24, 18, 12, 0.52)");
  grad.addColorStop(0.55, "rgba(38, 28, 20, 0.22)");
  grad.addColorStop(0.85, "rgba(48, 38, 28, 0.06)");
  grad.addColorStop(1, "rgba(0, 0, 0, 0)");"""
if old_ao in text:
    text = text.replace(old_ao, new_ao)
    print("2. Contact shadow AO deepened.")

# 3. 第 1 幕小橘塊受震波：只震動不變扁！直到 3.8s 箱子砸到它才開始被壓扁
target_s1_start = "} else if (t < 3.7) {"
if target_s1_start in text:
    old_s1 = """      } else if (t < 3.7) {
        // 2.05 ~ 3.7s: 大箱砸地震波！騰空壓扁回彈
        const dtLand = t - 2.05;
        rx = 0.0; rz = 0.0;
        if (dtLand < 0.6) {
          hy = Math.sin((dtLand / 0.6) * Math.PI) * 0.22;
          scaleY = 0.70 + Math.sin(dtLand * 14) * 0.25;
          scaleX = 1.22 - Math.sin(dtLand * 14) * 0.18;
          eyeScaleX = 1.35; eyeScaleY = 1.35;
          mouthType = "o"; mouthScale = 1.3;
        } else {
          gazeTgt.set(1.45, 0.8, -0.35);
          ry = 0.35; rz = -0.15; // 呆萌微縮
          mouthType = "straight";
        }
      } else if (t < 7.6) {
        // 3.7 ~ 7.6s: 漫天紙箱堆疊成山
        const dtSwarm = t - 3.7;
        gazeTgt.set(-1.5 + Math.sin(t * 15) * 0.8, 1.8, 0.5);
        hx += Math.sin(t * 28) * 0.02;
        const crushU = clamp(dtSwarm / 2.2);
        hy = 0.0;
        scaleY = lerp(1.0, 0.74, crushU);
        scaleX = lerp(1.0, 1.22, crushU);"""

    new_s1 = """      } else if (t < 3.8) {
        // 2.05 ~ 3.8s: 大箱落地地震波！小人被震起微跳，身體保持飽滿不扁！
        const dtLand = t - 2.05;
        rx = 0.0; rz = 0.0;
        if (dtLand < 0.55) {
          hy = Math.sin((dtLand / 0.55) * Math.PI) * 0.16;
          scaleY = 1.0; scaleX = 1.0; scaleZ = 1.0; // 絕不提前扁塌！
          eyeScaleX = 1.35; eyeScaleY = 1.35;
          mouthType = "o"; mouthScale = 1.15;
          gazeTgt.set(1.45, 0.8, -0.35);
        } else {
          hy = 0.0;
          scaleY = 1.0; scaleX = 1.0; scaleZ = 1.0;
          gazeTgt.set(1.45, 1.2, -0.35);
          ry = 0.32; rz = -0.12; // 側身歪頭，困惑看著大箱子
          mouthType = "straight";
        }
      } else if (t < 7.6) {
        // 3.8 ~ 7.6s: 漫天紙箱堆疊成山，砸在小橘塊頭頂並堆疊！
        const dtSwarm = t - 3.8;
        gazeTgt.set(-1.5 + Math.sin(t * 12) * 0.5, 1.5, 0.5);
        hx += Math.sin(t * 26) * 0.015;
        const crushU = clamp(dtSwarm / 2.0);
        hy = 0.0;
        scaleY = lerp(1.0, 0.68, crushU);
        scaleX = lerp(1.0, 1.28, crushU);"""
    text = text.replace(old_s1, new_s1)
    print("3. S1 Hero squash timing fixed (squash only when boxes hit).")

# 4. 第 2 幕卡片繞行路徑與高度，避開小橘塊
old_orbit = """      const angle = (idx / 8) * Math.PI * 2 + orbitT * 0.45 + 0.3;
      const radius = 1.65;
      const wave = Math.sin(orbitT * 2.5 + idx * 0.8);
      const orbitPos = new THREE.Vector3(0.85 + Math.cos(angle) * radius, 1.35 + wave * 0.18, 0.2 + Math.sin(angle) * 0.95);
      const targetPos = new THREE.Vector3(0.95, 0.85, 0.25 - idx * 0.015);"""

new_orbit = """      const angle = (idx / 8) * Math.PI * 2 + orbitT * 0.42 + 0.3;
      // 繞行中心往右推到 x = 1.05，半徑收緊為 1.35，高度提高到 y = 1.82，在小橘塊上方與右側環繞，視線 100% 乾淨！
      const radius = 1.35;
      const wave = Math.sin(orbitT * 2.2 + idx * 0.8);
      const orbitPos = new THREE.Vector3(1.05 + Math.cos(angle) * radius, 1.82 + wave * 0.14, 0.25 + Math.sin(angle) * 0.85);
      const targetPos = new THREE.Vector3(0.95, 0.85, 0.25 - idx * 0.015);"""

if old_orbit in text:
    text = text.replace(old_orbit, new_orbit)
    print("4. S2 tab orbit lifted and shifted right (no face clipping).")

# 5. 第 4 幕站位與左右頒獎台
old_s4_podium = "const podiums = [-1.35, 0.0, 1.35].map((x, i) => {"
new_s4_podium = "const podiums = [-1.45, 0.0, 1.45].map((x, i) => {"
if old_s4_podium in text:
    text = text.replace(old_s4_podium, new_s4_podium)
    print("5. S4 podiums widened.")

old_s4_hero = "      hx = -1.75; hy = 0.0; hz = 0.85;"
new_s4_hero = "      hx = -2.35; hy = 0.0; hz = 0.70;"
if old_s4_hero in text:
    text = text.replace(old_s4_hero, new_s4_hero)
    print("6. S4 Hero positioned clearly to the left.")

p.write_text(text, encoding="utf-8")
print("scene.html patched successfully!")

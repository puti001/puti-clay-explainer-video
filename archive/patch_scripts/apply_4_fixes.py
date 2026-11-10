import sys
from pathlib import Path

p = Path(r"c:\antigravity\影片\逆向研究\claude3d_工法\scene.html")
text = p.read_text(encoding="utf-8")

# ========================================================
# 1. 修正 3D 立體字「Gemini購物」接地 Y 軸：精確貼齊地面，絕不陷進地板！
# ========================================================
old_letters_build = """  const str = "Gemini購物", size = 0.52, scale = size / fontData.resolution;
  let x = 0.0;
  [...str].forEach((ch, i) => {
    const g = new TextGeometry(ch, { font, size, depth: 0.17, curveSegments: 8, bevelEnabled: true, bevelThickness: 0.035, bevelSize: 0.018, bevelSegments: 5 });
    g.computeBoundingBox();
    const m = shadowy(new THREE.Mesh(g, i < 6 ? M.orange : M.navyText));
    const adv = (fontData.glyphs[ch]?.ha ?? fontData.resolution * 0.6) * scale;
    m.userData = { x: x, i };
    x += adv + (i === 5 ? 0.14 : 0.015);
    s1Group.add(m); letters.push(m);
  });
  letters.forEach((m) => { m.userData.x += 0.1; });"""

new_letters_build = """  const str = "Gemini購物", size = 0.52, scale = size / fontData.resolution;
  let x = 0.0;
  [...str].forEach((ch, i) => {
    const g = new TextGeometry(ch, { font, size, depth: 0.17, curveSegments: 8, bevelEnabled: true, bevelThickness: 0.035, bevelSize: 0.018, bevelSegments: 5 });
    g.computeBoundingBox();
    const minY = g.boundingBox ? g.boundingBox.min.y : 0;
    const m = shadowy(new THREE.Mesh(g, i < 6 ? M.orange : M.navyText));
    const adv = (fontData.glyphs[ch]?.ha ?? fontData.resolution * 0.6) * scale;
    m.userData = { x: x, i, minY: minY };
    x += adv + (i === 5 ? 0.14 : 0.015);
    s1Group.add(m); letters.push(m);
  });
  letters.forEach((m) => { m.userData.x += 0.1; });"""

if old_letters_build in text:
    text = text.replace(old_letters_build, new_letters_build)
    print("1.1 Letters build minY recorded.")

old_letters_anim = """    // 3D 立體字
    letters.forEach((m) => {
      const t0 = 12.0 + m.userData.i * 0.075, s = t - t0;
      m.visible = s > 0;
      const fall = clamp(s / 0.34), y = (1 - fall * fall) * 3.2;
      const lnd = s - 0.34, lsq = lnd > 0 ? spring(lnd, 3.0, 5.5) * 0.22 : 0;
      m.position.set(m.userData.x, y, 0.75);
      m.scale.set(1 + lsq * 0.5, 1 - lsq, 1 + lsq * 0.5);
    });"""

new_letters_anim = """    // 3D 立體字（精確接地補償 -minY，底部與地面 0.005 齊平，絕不陷地！）
    letters.forEach((m) => {
      const t0 = 12.0 + m.userData.i * 0.075, s = t - t0;
      m.visible = s > 0;
      const fall = clamp(s / 0.34);
      const baseY = -m.userData.minY + 0.005;
      const dropY = (1 - fall * fall) * 3.2;
      const lnd = s - 0.34, lsq = lnd > 0 ? spring(lnd, 3.0, 5.5) * 0.22 : 0;
      m.position.set(m.userData.x, baseY + dropY, 0.75);
      m.scale.set(1 + lsq * 0.5, 1 - lsq, 1 + lsq * 0.5);
    });"""

if old_letters_anim in text:
    text = text.replace(old_letters_anim, new_letters_anim)
    print("1.2 Letters animation grounded perfectly.")

# ========================================================
# 2. 第 2 幕：小橘塊回到正中心 (0, 0, 0)，8 張分頁環繞包圍小橘塊！
# ========================================================
# 小橘塊站位修改：第 2 幕留在中心 (0, 0, 0)
old_s2_hero = """    } else if (t < 32.5) {
      // ---------- 第 2 幕 表演 ----------
      // 站位在左側 x = -1.15，收納盒在 x = 0.95，相隔 2.1 米絕對不穿模！
      const jumpU = prog(t, 16.0, 0.9);
      if (jumpU < 1) {
        hx = lerp(-1.5, -1.15, eio(jumpU));
        hy = Math.sin(jumpU * Math.PI) * 1.35;
      } else {
        hx = -1.15; hy = 0.0;
        if (t < 26.5) {
          // 分頁繞行：小人好奇轉頭，眼神追蹤卡片
          const trackAngle = (t - 17.5) * 0.38 + 0.45;
          gazeTgt.set(Math.cos(trackAngle) * 2.2, 1.3, Math.sin(trackAngle) * 2.2);
          ry = Math.sin(t * 3.5) * 0.35;
          rz = Math.cos(t * 3.0) * 0.12; // 呆萌歪頭
          if (t > 20.0) {
            eyeScaleX = 1.2; eyeScaleY = 0.25; // 稍微看暈瞇眼
            mouthType = "sad"; mouthScale = 0.9;
          } else {
            mouthType = "o"; mouthScale = 0.8;
          }
        } else {
          // 磁吸啪一聲收納！小人清醒，轉身面向右側收納盒（ry = 0.52），歪頭滿意微笑！
          gazeTgt.set(0.95, 0.85, 0.25);
          ry = 0.52; rz = -0.15; // 側身歪頭滿意看著初篩表！
          mouthType = "smile"; mouthScale = 1.25;
          scaleY = 1.05 + Math.sin(t * 4) * 0.03;
        }
      }"""

new_s2_hero = """    } else if (t < 32.5) {
      // ---------- 第 2 幕 表演 ----------
      // 小橘塊穩居舞台中心 (0, 0, 0)，8 張分頁圍成環形包圍小人！
      const jumpU = prog(t, 16.0, 0.9);
      if (jumpU < 1) {
        hx = lerp(-1.5, 0.0, eio(jumpU));
        hy = Math.sin(jumpU * Math.PI) * 1.35;
      } else {
        hx = 0.0; hy = 0.0; hz = 0.0;
        if (t < 26.0) {
          // 分頁繞行包圍：小人在中心轉頭被轉得暈頭轉向，眼神追蹤旋轉卡片！
          const trackAngle = (t - 17.5) * 0.65;
          gazeTgt.set(Math.cos(trackAngle) * 2.0, 1.1, Math.sin(trackAngle) * 2.0);
          ry = Math.sin(t * 4.0) * 0.45;
          rz = Math.cos(t * 3.2) * 0.15; // 呆萌暈眩歪頭
          if (t > 20.0) {
            eyeScaleX = 1.2; eyeScaleY = 0.25; // 暈頭瞇眼
            mouthType = "sad"; mouthScale = 0.9;
          } else {
            mouthType = "o"; mouthScale = 0.85;
          }
        } else {
          // 磁吸啪一聲收納進右側盒子！小人後退一步舒暢站立，看向收合處滿意微笑！
          hx = -0.65;
          gazeTgt.set(0.95, 0.85, 0.25);
          ry = 0.55; rz = -0.12; // 側身歪頭滿意看著初篩表！
          mouthType = "smile"; mouthScale = 1.25;
          scaleY = 1.05 + Math.sin(t * 4) * 0.03;
        }
      }"""

if old_s2_hero in text:
    text = text.replace(old_s2_hero, new_s2_hero)
    print("2.1 Hero center staging in S2 updated.")

# 8 張分頁繞行中心設在 (0, 0, 0)，半徑 1.95，小人 (0, 0, 0) 半徑 0.5，淨空間 1.45 米絕不穿模！
old_orbit = """    // 8 個分頁繞行中心設在右側 (x = 0.85, z = 0.2)，半徑 1.6m 盤旋，左側小人視野 100% 乾淨！
    tabCards.forEach((c, idx) => {
      const spawnT = 17.5 + idx * 0.32;
      if (t < spawnT) { c.visible = false; return; }
      c.visible = true;

      const angle = (idx / 8) * Math.PI * 2 + orbitT * 0.42 + 0.3;
      // 繞行中心往右推到 x = 1.05，半徑收緊為 1.35，高度提高到 y = 1.82，在小橘塊上方與右側環繞，視線 100% 乾淨！
      const radius = 1.35;
      const wave = Math.sin(orbitT * 2.2 + idx * 0.8);
      const orbitPos = new THREE.Vector3(1.05 + Math.cos(angle) * radius, 1.82 + wave * 0.14, 0.25 + Math.sin(angle) * 0.85);
      const targetPos = new THREE.Vector3(0.95, 0.85, 0.25 - idx * 0.015);

      c.position.lerpVectors(orbitPos, targetPos, collectE);
      c.rotation.set(wave * 0.08, -angle + Math.PI / 2, Math.cos(orbitT * 2 + idx) * 0.06);
      c.scale.setScalar(lerp(1, 0.40, collectE));
      if (collectU >= 1) c.visible = false;
    });"""

new_orbit = """    // 8 個分頁圍繞小橘塊 (0, 0, 0) 展開 360 度大環繞！小橘塊在正中心被眾多分頁包圍！
    tabCards.forEach((c, idx) => {
      const spawnT = 17.0 + idx * 0.28;
      if (t < spawnT) { c.visible = false; return; }
      c.visible = true;

      const angle = (idx / 8) * Math.PI * 2 + orbitT * 0.48;
      const radius = 2.05; // 寬敞大圓半徑，小人在中心 (0, 0, 0)，前後左右完全包圍且留有 1.5 米安全裕度！
      const wave = Math.sin(orbitT * 2.4 + idx * 0.9);
      // 卡片圍繞中心 (0, 0, 0)，高度在 1.05 (與小人視線齊平)，且正面朝向中心小人！
      const orbitPos = new THREE.Vector3(Math.cos(angle) * radius, 1.05 + wave * 0.12, Math.sin(angle) * radius);
      const targetPos = new THREE.Vector3(0.95, 0.85, 0.25 - idx * 0.015);

      c.position.lerpVectors(orbitPos, targetPos, collectE);
      // 卡片面朝中心 (0, 0, 0)
      c.rotation.set(wave * 0.06, -angle - Math.PI / 2, Math.cos(orbitT * 2 + idx) * 0.05);
      c.scale.setScalar(lerp(1, 0.38, collectE));
      if (collectU >= 1) c.visible = false;
    });"""

if old_orbit in text:
    text = text.replace(old_orbit, new_orbit)
    print("2.2 S2 360 degree enclosing orbit around hero updated.")

# ========================================================
# 3. 第 4 幕：3 座立牌台座給予 3 種專屬顏色！立牌字體放大 1.4 倍！
# ========================================================
# 新增台座顏色材料
target_mat_cheek = "cheek:     new THREE.MeshBasicMaterial({ color: 0xf28b72, transparent: true, opacity: 0.60 }),"
new_mats_podium = """cheek:     new THREE.MeshBasicMaterial({ color: 0xf28b72, transparent: true, opacity: 0.60 }),
  podiumNavy:   new THREE.MeshStandardMaterial({ color: 0x18243c, roughness: 0.80, metalness: 0.0 }), // 深海軍藍台座
  podiumGold:   new THREE.MeshStandardMaterial({ color: 0xd98a28, roughness: 0.72, metalness: 0.05 }), // 尊貴暖金台座 (冠軍)
  podiumClay:   new THREE.MeshStandardMaterial({ color: 0x8a7260, roughness: 0.85, metalness: 0.0 }), // 溫潤大地灰褐台座"""

if target_mat_cheek in text and "podiumNavy" not in text:
    text = text.replace(target_mat_cheek, new_mats_podium)
    print("3.1 Podium 3 distinct materials added.")

old_podiums_block = """// 3 個頒獎台（原片同款溫潤暖木台座，配專屬接地軟陰影！）
const podiumShadows = [];
const podiums = [-1.22, 0.0, 1.22].map((x, i) => {
  const heights = [0.65, 1.05, 0.5];
  const g = new THREE.Group(); g.position.set(x, 0, 0);
  const pShadow = createContactShadowMesh(1.5, 1.3, 0.60);
  pShadow.position.set(x, 0.005, 0);
  podiumShadows.push(pShadow);
  pShadow.visible = false;

  const base = shadowy(new THREE.Mesh(new RoundedBoxGeometry(1.1, heights[i], 0.9, 3, 0.08), M.paper));
  base.position.y = heights[i] / 2; g.add(base);
  
  const cTitle = ["品牌 A 6L", "首選推薦 B", "品牌 C 靜音"][i];
  const cTag = ["空間適配", "一級節能 · 規格全勝", "平價靜音"][i];
  const card = new THREE.Group();
  
  const cMesh = shadowy(new THREE.Mesh(new RoundedBoxGeometry(0.96, 0.8, 0.045, 2, 0.02), i === 1 ? M.metalGate : M.card));
  const cFace = new THREE.Mesh(new THREE.PlaneGeometry(0.92, 0.76), new THREE.MeshStandardMaterial({
    roughness: 0.4,
    map: labelTex(900, 720, (ctx, w, h) => {
      rr(ctx, 12, 12, w - 24, h - 24, 40); ctx.fillStyle = i === 1 ? "#ffffff" : "#ffffff"; ctx.fill();
      ctx.lineWidth = i === 1 ? 20 : 12; ctx.strokeStyle = i === 1 ? "#c85624" : "#152038"; ctx.stroke();
      if (i === 1) {
        rr(ctx, w/2 - 150, 24, 300, 60, 30); ctx.fillStyle = "#c85624"; ctx.fill();
        ctx.fillStyle = "#ffffff"; ctx.font = '900 36px "Microsoft JhengHei", "Noto Sans TC", sans-serif'; ctx.textAlign = "center"; ctx.fillText("★ BEST CHOICE ★", w/2, 66);
      }
      ctx.fillStyle = "#152038"; ctx.font = '900 78px "Microsoft JhengHei", "Noto Sans TC", sans-serif'; ctx.textAlign = "center"; ctx.fillText(cTitle, w/2, i === 1 ? 180 : 155);
      ctx.fillStyle = "#d73525"; ctx.font = '900 110px "Microsoft JhengHei", "Noto Sans TC", sans-serif'; ctx.fillText("$" + [6490, 7880, 5990][i], w/2, i === 1 ? 345 : 310);
      ctx.fillStyle = "#374151"; ctx.font = '700 52px "Microsoft JhengHei", "Noto Sans TC", sans-serif'; ctx.fillText(cTag, w/2, i === 1 ? 515 : 475);
    })
  }));
  cFace.position.z = 0.025; card.add(cMesh, cFace);
  card.position.set(0, heights[i] + 0.46, 0);
  g.add(card);
  s4Group.add(g); g.visible = false;
  return { g, card, pShadow, h: heights[i] };
});"""

new_podiums_block = """// 3 個頒獎台（三座台座給予 3 種專屬顏色！立牌放大、字體超清晰無穿模！）
const podiumShadows = [];
const podiumMats = [M.podiumNavy, M.podiumGold, M.podiumClay];
const podiums = [-1.22, 0.0, 1.22].map((x, i) => {
  const heights = [0.65, 1.05, 0.5];
  const g = new THREE.Group(); g.position.set(x, 0, 0);
  const pShadow = createContactShadowMesh(1.5, 1.3, 0.65);
  pShadow.position.set(x, 0.005, 0);
  podiumShadows.push(pShadow);
  pShadow.visible = false;

  // 三種專屬配色台座：左海軍藍、中金黃、右灰褐！
  const base = shadowy(new THREE.Mesh(new RoundedBoxGeometry(1.12, heights[i], 0.92, 3, 0.08), podiumMats[i]));
  base.position.y = heights[i] / 2; g.add(base);
  
  const cTitle = ["品牌 A 6L", "首選推薦 B", "品牌 C 靜音"][i];
  const cTag = ["空間適配", "一級節能 · 規格全勝", "平價靜音"][i];
  const card = new THREE.Group();
  
  // 立牌尺寸加大 1.25 倍 (1.18 x 0.96)
  const cMesh = shadowy(new THREE.Mesh(new RoundedBoxGeometry(1.18, 0.96, 0.05, 2, 0.02), i === 1 ? M.orange : M.navy));
  const cFace = new THREE.Mesh(new THREE.PlaneGeometry(1.14, 0.92), new THREE.MeshStandardMaterial({
    roughness: 0.35,
    map: labelTex(1100, 880, (ctx, w, h) => {
      rr(ctx, 14, 14, w - 28, h - 28, 44); ctx.fillStyle = "#ffffff"; ctx.fill();
      ctx.lineWidth = i === 1 ? 24 : 14; ctx.strokeStyle = i === 1 ? "#c85624" : "#152038"; ctx.stroke();
      if (i === 1) {
        rr(ctx, w/2 - 200, 26, 400, 72, 36); ctx.fillStyle = "#c85624"; ctx.fill();
        ctx.fillStyle = "#ffffff"; ctx.font = '900 44px "Microsoft JhengHei", "Noto Sans TC", sans-serif'; ctx.textAlign = "center"; ctx.fillText("★ BEST CHOICE ★", w/2, 78);
      }
      ctx.fillStyle = "#152038"; ctx.font = '900 102px "Microsoft JhengHei", "Noto Sans TC", sans-serif'; ctx.textAlign = "center"; ctx.fillText(cTitle, w/2, i === 1 ? 210 : 180);
      ctx.fillStyle = "#d73525"; ctx.font = '900 148px "Microsoft JhengHei", "Noto Sans TC", sans-serif'; ctx.fillText("$" + [6490, 7880, 5990][i], w/2, i === 1 ? 425 : 390);
      ctx.fillStyle = "#2d3748"; ctx.font = '900 68px "Microsoft JhengHei", "Noto Sans TC", sans-serif'; ctx.fillText(cTag, w/2, i === 1 ? 640 : 610);
    })
  }));
  cFace.position.z = 0.027; // 安全厚度防止 Z-fighting
  card.add(cMesh, cFace);
  card.position.set(0, heights[i] + 0.55, 0);
  g.add(card);
  s4Group.add(g); g.visible = false;
  return { g, card, pShadow, h: heights[i] };
});"""

if old_podiums_block in text:
    text = text.replace(old_podiums_block, new_podiums_block)
    print("3.2 Podiums block updated with 3 colors and larger cards.")

# ========================================================
# 4. 第 3 幕：折價券與小橘塊穿模徹底修復！
# ========================================================
# 折價券雨的生成範圍避開小橘塊 (小橘塊在 x = -1.5 ~ -1.3, z = 0.2)
old_coupon_spawn = """  cMesh.position.set((R() - 0.5) * 6, 2.5 + R() * 2.5, (R() - 0.5) * 4);"""
new_coupon_spawn = """  // 折價券主要落在鐵門前方與右側空間，絕對不砸進左側小橘塊頭皮！
  let cx = (R() - 0.5) * 5.5;
  if (cx < -0.8 && cx > -2.2) cx += 1.8; // 強制避開小橘塊安全通道
  cMesh.position.set(cx, 2.5 + R() * 2.5, 0.4 + (R() - 0.5) * 2.8);"""

if old_coupon_spawn in text:
    text = text.replace(old_coupon_spawn, new_coupon_spawn)
    print("4.1 Coupon spawn zone cleared from Hero.")

old_coupon_loop = """    // 折價券雨
    const rainT = t - 39.5;
    couponCards.forEach((cp, idx) => {
      if (rainT <= 0) { cp.mesh.visible = false; return; }
      cp.mesh.visible = true;
      cp.mesh.position.y -= 0.038 * cp.speed;
      if (cp.mesh.position.y < 0.15) cp.mesh.position.y = 4.5;
      cp.mesh.rotation.x += 0.03; cp.mesh.rotation.y += 0.02;
    });"""

new_coupon_loop = """    // 折價券雨（避開小橘塊安全距離，落地後透明淡出，絕不穿透角色！）
    const rainT = t - 39.5;
    couponCards.forEach((cp, idx) => {
      if (rainT <= 0) { cp.mesh.visible = false; return; }
      cp.mesh.visible = true;
      cp.mesh.position.y -= 0.038 * cp.speed;
      // 保持在小橘塊外部安全半徑
      const distToHero = Math.hypot(cp.mesh.position.x - hx, cp.mesh.position.z - hz);
      if (distToHero < 0.85) {
        cp.mesh.position.x += (cp.mesh.position.x >= hx ? 0.6 : -0.6);
      }
      if (cp.mesh.position.y < 0.15) cp.mesh.position.y = 4.5;
      cp.mesh.rotation.x += 0.03; cp.mesh.rotation.y += 0.02;
    });"""

if old_coupon_loop in text:
    text = text.replace(old_coupon_loop, new_coupon_loop)
    print("4.2 Coupon collision evasion added.")

p.write_text(text, encoding="utf-8")
print("All 4 critical fixes successfully written to scene.html!")

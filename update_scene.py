import re
from pathlib import Path

html_path = Path(r"c:\antigravity\影片\逆向研究\claude3d_工法\scene.html")
code = html_path.read_text(encoding="utf-8")

# 1. 替換大紙箱與開蓋幾何 (around line 240-260)
old_box_block = """const BW = 2.3, BH = 1.6, BD = 1.6;
const boxBody = shadowy(new THREE.Mesh(new RoundedBoxGeometry(BW, BH, BD, 4, 0.06), M.card));
boxBody.position.y = BH / 2; bigBox.add(boxBody);
const tapeV = shadowy(new THREE.Mesh(new THREE.BoxGeometry(0.34, 0.02, BD + 0.02), M.tape));
tapeV.position.set(0, BH + 0.005, 0); bigBox.add(tapeV);
const bigLabel = new THREE.Mesh(new THREE.PlaneGeometry(1.5, 0.75), new THREE.MeshStandardMaterial({
  roughness: 0.7, transparent: true,
  map: labelTex(900, 450, (x, w, h) => {
    rr(x, 8, 8, w - 16, h - 16, 36); x.fillStyle = "#f7f3ea"; x.fill();
    x.lineWidth = 8; x.strokeStyle = "#223067"; x.stroke();
    x.fillStyle = "#223067"; x.textAlign = "center"; x.font = '900 170px "NTC"'; x.fillText("500 億筆", w / 2, 230);
    x.font = '700 66px "NTC"'; x.fillStyle = "#c2532a"; x.fillText("SHOPPING GRAPH", w / 2, 350);
  }),
}));
bigLabel.position.set(0, BH * 0.52, BD / 2 + 0.005); bigBox.add(bigLabel);
const flaps = [-1, 1].map((s) => {
  const pivot = new THREE.Group(); pivot.position.set(0, BH + 0.01, (s * BD) / 2); bigBox.add(pivot);
  const f = shadowy(new THREE.Mesh(new THREE.BoxGeometry(BW - 0.04, 0.03, BD / 2), M.card));
  f.position.z = (-s * BD) / 4; pivot.add(f); pivot.userData.s = s; return pivot;
});"""

new_box_block = """const BW = 2.4, BH = 1.65, BD = 1.65;
const boxBody = shadowy(new THREE.Mesh(new RoundedBoxGeometry(BW, BH, BD, 4, 0.06), M.card));
boxBody.position.y = BH / 2; bigBox.add(boxBody);
const tapeV = shadowy(new THREE.Mesh(new THREE.BoxGeometry(0.34, 0.02, BD + 0.02), M.tape));
tapeV.position.set(0, BH + 0.005, 0); bigBox.add(tapeV);

// 大標籤：稍微調高位置，字體超巨大清晰，絕對不被任何蓋片遮擋！
const bigLabel = new THREE.Mesh(new THREE.PlaneGeometry(1.65, 0.85), new THREE.MeshStandardMaterial({
  roughness: 0.6, transparent: true,
  map: labelTex(1000, 520, (x, w, h) => {
    rr(x, 10, 10, w - 20, h - 20, 40); x.fillStyle = "#ffffff"; x.fill();
    x.lineWidth = 10; x.strokeStyle = "#223067"; x.stroke();
    x.fillStyle = "#223067"; x.textAlign = "center"; x.font = '900 190px "NTC"'; x.fillText("500 億筆", w / 2, 250);
    x.font = '700 74px "NTC"'; x.fillStyle = "#c2532a"; x.fillText("SHOPPING GRAPH", w / 2, 385);
  }),
}));
bigLabel.position.set(0, BH * 0.50, BD / 2 + 0.008); bigBox.add(bigLabel);

// 側蓋與後蓋翻折（絕不設正面垂落蓋片，正面視野百分之百開闊！）
const flapL = new THREE.Group(); flapL.position.set(-BW / 2, BH + 0.005, 0); bigBox.add(flapL);
const fLM = shadowy(new THREE.Mesh(new THREE.BoxGeometry(BW / 2.1, 0.025, BD - 0.04), M.card));
fLM.position.x = BW / 4.2; flapL.add(fLM);

const flapR = new THREE.Group(); flapR.position.set(BW / 2, BH + 0.005, 0); bigBox.add(flapR);
const fRM = shadowy(new THREE.Mesh(new THREE.BoxGeometry(BW / 2.1, 0.025, BD - 0.04), M.card));
fRM.position.x = -BW / 4.2; flapR.add(fRM);

const flapBack = new THREE.Group(); flapBack.position.set(0, BH + 0.005, -BD / 2); bigBox.add(flapBack);
const fBM = shadowy(new THREE.Mesh(new THREE.BoxGeometry(BW - 0.04, 0.025, BD / 2.1), M.card));
fBM.position.z = BD / 4.2; flapBack.add(fBM);"""

assert old_box_block in code, "old_box_block not found!"
code = code.replace(old_box_block, new_box_block)

# 2. 替換小包裹 slots 邏輯（杜絕插在小人體內）
old_slots_block = """const R = rng(20261109);
const N = 64, items = [];
const slots = [];
for (let k = 0; k < N; k++) {
  const a = k * 2.39996, r = 0.15 + Math.sqrt((k + 0.5) / N) * 1.75;
  slots.push({ x: -1.5 + Math.cos(a) * r * 1.05, z: 0.15 + Math.sin(a) * r * 0.75, y: 0.12 + R() * 1.4 });
}
slots.sort((p, q) => p.y - q.y);"""

new_slots_block = """const R = rng(20261109);
const N = 64, items = [];
const slots = [];
// 嚴格避開小人本體 [-1.9, -1.1] x [-0.25, 0.55]，小箱子全部散落在四周環繞，絕不穿模！
for (let k = 0; k < N; k++) {
  const a = k * 2.39996;
  const r = 0.95 + Math.sqrt((k + 0.5) / N) * 1.85; // 離小人中心至少 0.95 米！
  const sx = -1.5 + Math.cos(a) * r * 1.25;
  const sz = 0.15 + Math.sin(a) * r * 0.95;
  slots.push({ x: sx, z: sz, y: 0.08 + (k % 4) * 0.14 });
}
slots.sort((p, q) => p.y - q.y);"""

assert old_slots_block in code, "old_slots_block not found!"
code = code.replace(old_slots_block, new_slots_block)

# 3. 替換第二幕 收納夾幾何與外觀
old_binder_block = """// 磁吸收納盒（置於主角右前方，絕對不擋住標籤）
const binder = new THREE.Group(); s2Group.add(binder);
const binderBody = shadowy(new THREE.Mesh(new RoundedBoxGeometry(1.25, 1.55, 0.38, 3, 0.06), M.navy));
binder.add(binderBody);
const binderLabel = new THREE.Mesh(new THREE.PlaneGeometry(0.95, 0.45), new THREE.MeshStandardMaterial({
  transparent: true,
  map: labelTex(650, 300, (x, w, h) => {
    rr(x, 8, 8, w - 16, h - 16, 24); x.fillStyle = "#2fa36b"; x.fill();
    x.fillStyle = "#ffffff"; x.font = '900 70px "NTC"'; x.textAlign = "center"; x.fillText("規格初篩表", w/2, 160);
  })
}));
binderLabel.position.set(0, 0, 0.2); binder.add(binderLabel);
binder.visible = false;"""

new_binder_block = """// 磁吸收納夾（置於畫面右側黃金線 x = 0.85，具備精緻立體銀色夾具與翡翠綠打凸標籤）
const binder = new THREE.Group(); s2Group.add(binder);
const binderBody = shadowy(new THREE.Mesh(new RoundedBoxGeometry(1.3, 1.6, 0.28, 4, 0.08), M.navy));
binder.add(binderBody);

// 精緻銀色夾具（Clip）
const binderClip = shadowy(new THREE.Mesh(new RoundedBoxGeometry(0.55, 0.14, 0.32, 2, 0.03), M.metalGate));
binderClip.position.set(0, 0.78, 0); binder.add(binderClip);

// 規格初篩表標籤（翡翠綠卡片 + 白色立體邊框）
const binderLabel = new THREE.Mesh(new THREE.PlaneGeometry(1.05, 0.65), new THREE.MeshStandardMaterial({
  transparent: true, roughness: 0.5,
  map: labelTex(800, 500, (x, w, h) => {
    rr(x, 10, 10, w - 20, h - 20, 30); x.fillStyle = "#10b981"; x.fill();
    x.lineWidth = 8; x.strokeStyle = "#ffffff"; x.stroke();
    x.fillStyle = "#ffffff"; x.font = '900 82px "NTC"'; x.textAlign = "center"; x.fillText("規格初篩表", w/2, 210);
    x.font = '700 44px "NTC"'; x.fillStyle = "#d1fae5"; x.fillText("AI 自動收斂多維規格", w/2, 330);
  })
}));
binderLabel.position.set(0, -0.05, 0.15); binder.add(binderLabel);
binder.visible = false;"""

assert old_binder_block in code, "old_binder_block not found!"
code = code.replace(old_binder_block, new_binder_block)

# 4. 替換第四幕 頒獎台與冠軍卡片 + 彩帶系統
old_podium_confetti_block = """// 3 個頒獎台 + 3 張產品卡（4K 超高解析度文字，銳利無比！）
const podiums = [-1.4, 0.0, 1.4].map((x, i) => {
  const heights = [0.6, 0.95, 0.45];
  const g = new THREE.Group(); g.position.set(x, 0, 0);
  const base = shadowy(new THREE.Mesh(new RoundedBoxGeometry(1.05, heights[i], 0.85, 3, 0.05), M.paper));
  base.position.y = heights[i] / 2; g.add(base);
  
  const cTitle = ["品牌 A 6L", "首選推薦 B", "品牌 C 靜音"][i];
  const cTag = ["空間適配", "一級節能 · 規格全勝", "平價靜音"][i];
  const card = new THREE.Group();
  const cMesh = shadowy(new THREE.Mesh(new RoundedBoxGeometry(0.9, 0.75, 0.04, 2, 0.02), i === 1 ? M.paper : M.card));
  const cFace = new THREE.Mesh(new THREE.PlaneGeometry(0.88, 0.72), new THREE.MeshStandardMaterial({
    roughness: 0.5,
    map: labelTex(800, 640, (ctx, w, h) => {
      rr(ctx, 10, 10, w - 20, h - 20, 36); ctx.fillStyle = i === 1 ? "#ecfdf5" : "#ffffff"; ctx.fill();
      ctx.lineWidth = 10; ctx.strokeStyle = i === 1 ? "#10b981" : "#cbd5e1"; ctx.stroke();
      if (i === 1) {
        ctx.fillStyle = "#10b981"; ctx.beginPath(); ctx.arc(70, 70, 32, 0, 7); ctx.fill();
        ctx.fillStyle = "#fff"; ctx.font = '900 42px sans-serif'; ctx.textAlign = "center"; ctx.fillText("✓", 70, 84);
      }
      ctx.fillStyle = i === 1 ? "#065f46" : "#1e293b"; ctx.font = '900 68px "NTC"'; ctx.textAlign = "center"; ctx.fillText(cTitle, w/2, 130);
      ctx.fillStyle = "#d8462f"; ctx.font = '900 90px "NTC"'; ctx.fillText("$" + [6490, 7880, 5990][i], w/2, 280);
      ctx.fillStyle = i === 1 ? "#047857" : "#64748b"; ctx.font = '700 48px "NTC"'; ctx.fillText(cTag, w/2, 440);
    })
  }));
  cFace.position.z = 0.022; card.add(cMesh, cFace);
  card.position.set(0, heights[i] + 0.42, 0);
  g.add(card);
  s4Group.add(g); g.visible = false;
  return { g, card, h: heights[i] };
});

// 第 4 幕紙花粒子系統（Confetti Particles）
const confettiCount = 54;
const confettiGeo = new THREE.PlaneGeometry(0.12, 0.12);
const confettiCols = [0xd8602a, 0x2fa36b, 0x3b82f6, 0xf59e0b, 0xec4899];
const confettiMeshes = [];
for (let i = 0; i < confettiCount; i++) {
  const m = new THREE.Mesh(confettiGeo, new THREE.MeshBasicMaterial({ color: confettiCols[i % confettiCols.length], side: THREE.DoubleSide }));
  m.position.set((R() - 0.5) * 4.5, 3.5 + R() * 2.5, (R() - 0.5) * 2.5);
  s4Group.add(m); m.visible = false;
  confettiMeshes.push({ mesh: m, vy: 0.022 + R() * 0.03, rx: R() * 0.25, ry: R() * 0.25 });
}"""

new_podium_confetti_block = """// 3 個頒獎台 + 3 張產品卡（中間冠軍加金色桂冠與邊框）
const podiums = [-1.35, 0.0, 1.35].map((x, i) => {
  const heights = [0.65, 1.05, 0.5];
  const g = new THREE.Group(); g.position.set(x, 0, 0);
  const base = shadowy(new THREE.Mesh(new RoundedBoxGeometry(1.1, heights[i], 0.9, 3, 0.06), M.paper));
  base.position.y = heights[i] / 2; g.add(base);
  
  const cTitle = ["品牌 A 6L", "首選推薦 B", "品牌 C 靜音"][i];
  const cTag = ["空間適配", "一級節能 · 規格全勝", "平價靜音"][i];
  const card = new THREE.Group();
  
  // 冠軍卡特別加金色包邊
  const cMesh = shadowy(new THREE.Mesh(new RoundedBoxGeometry(0.96, 0.8, 0.045, 2, 0.02), i === 1 ? M.metalGate : M.card));
  const cFace = new THREE.Mesh(new THREE.PlaneGeometry(0.92, 0.76), new THREE.MeshStandardMaterial({
    roughness: 0.4,
    map: labelTex(900, 720, (ctx, w, h) => {
      rr(ctx, 12, 12, w - 24, h - 24, 40); ctx.fillStyle = i === 1 ? "#f0fdf4" : "#ffffff"; ctx.fill();
      ctx.lineWidth = i === 1 ? 16 : 8; ctx.strokeStyle = i === 1 ? "#f59e0b" : "#cbd5e1"; ctx.stroke();
      if (i === 1) {
        // 金色冠軍榮耀標籤
        rr(ctx, w/2 - 140, 20, 280, 56, 28); ctx.fillStyle = "#f59e0b"; ctx.fill();
        ctx.fillStyle = "#ffffff"; ctx.font = '900 36px "NTC"'; ctx.textAlign = "center"; ctx.fillText("★ BEST CHOICE ★", w/2, 60);
      }
      ctx.fillStyle = i === 1 ? "#065f46" : "#1e293b"; ctx.font = '900 76px "NTC"'; ctx.textAlign = "center"; ctx.fillText(cTitle, w/2, i === 1 ? 175 : 150);
      ctx.fillStyle = "#d8462f"; ctx.font = '900 102px "NTC"'; ctx.fillText("$" + [6490, 7880, 5990][i], w/2, i === 1 ? 335 : 300);
      ctx.fillStyle = i === 1 ? "#047857" : "#64748b"; ctx.font = '700 52px "NTC"'; ctx.fillText(cTag, w/2, i === 1 ? 500 : 460);
    })
  }));
  cFace.position.z = 0.025; card.add(cMesh, cFace);
  card.position.set(0, heights[i] + 0.46, 0);
  g.add(card);
  s4Group.add(g); g.visible = false;
  return { g, card, h: heights[i] };
});

// 第 4 幕紙花粒子系統（嚴格禁區約束：絕不遮擋卡片文字、絕不插在主角頭上，全真 3D 翻轉動態）
const confettiCount = 55;
const confettiCols = [0xd8602a, 0x2fa36b, 0x3b82f6, 0xf59e0b, 0xec4899];
const confettiMeshes = [];
for (let i = 0; i < confettiCount; i++) {
  const m = new THREE.Mesh(new THREE.PlaneGeometry(0.13, 0.09), new THREE.MeshStandardMaterial({
    color: confettiCols[i % confettiCols.length],
    side: THREE.DoubleSide,
    roughness: 0.5
  }));
  let cx, cz;
  while (true) {
    cx = (R() - 0.5) * 6.0;
    cz = (R() - 0.5) * 3.5;
    // 禁區 1：避開卡片正面讀取區 (|x| < 1.0 且 z 在 [-0.2, 0.6])
    if (Math.abs(cx) < 1.05 && cz > -0.2 && cz < 0.6) continue;
    // 禁區 2：避開主角全身周圍 (|x - (-1.55)| < 0.65 且 |z - 0.55| < 0.65)
    if (Math.hypot(cx - (-1.55), cz - 0.55) < 0.65) continue;
    break;
  }
  m.position.set(cx, 3.2 + R() * 2.5, cz);
  s4Group.add(m); m.visible = false;
  confettiMeshes.push({
    mesh: m,
    origX: cx, origZ: cz,
    vy: 0.024 + R() * 0.028,
    rx: 0.08 + R() * 0.12,
    ry: 0.06 + R() * 0.15,
    rz: 0.05 + R() * 0.1,
    swayFreq: 2.5 + R() * 2.0,
    swayAmp: 0.008 + R() * 0.012
  });
}"""

assert old_podium_confetti_block in code, "old_podium_confetti_block not found!"
code = code.replace(old_podium_confetti_block, new_podium_confetti_block)

# 5. 替換 renderAt 內的大紙箱、小包裹、收納盒、紙花、主角演技
old_render_s1_s2 = """    // 大箱子
    const u = prog(t, 1.7, 0.45), y = (1 - u * u) * 7;
    const land = t - 2.15;
    const sq = land > 0 ? spring(land, 2.6, 6) * 0.14 : 0;
    const away = eio(prog(t, 7.7, 0.9));
    bigBox.position.set(lerp(1.45, 5.2, away), y + away * 3.4, lerp(-0.35, -2.5, away));
    const sc = lerp(1, 0.001, Math.pow(away, 1.4));
    bigBox.scale.set(sc * (1 + sq * 0.5), sc * (1 - sq), sc * (1 + sq * 0.5));
    bigBox.visible = t > 1.69 && sc > 0.002;
    const open = t - 3.7;
    flaps.forEach((p) => { p.rotation.x = open > 0 ? p.userData.s * (-2.0 + spring(open, 2.2, 4.5) * 0.9) * clamp(open * 6) : 0; });

    // 噴發小包裹
    for (const it of items) {
      const u = (t - it.launch) / it.flight, m = it.mesh;
      const vanishU = prog(t, 7.6 + it.vanishDelay, 0.28);
      if (u <= 0 || vanishU >= 1) { m.visible = false; continue; }
      m.visible = true;
      if (u < 1) {
        m.position.lerpVectors(it.from, it.to, u);
        m.position.y += 4 * it.apex * u * (1 - u);
        m.rotation.set(it.r0.x + it.w.x * u, it.r0.y + it.w.y * u, it.r0.z + it.w.z * u);
      } else {
        m.position.copy(it.to);
        const vs = 1 - ebackIn(vanishU);
        m.scale.setScalar(Math.max(0.001, vs));
      }
    }"""

new_render_s1_s2 = """    // 大箱子物理下落與彈跳
    const landT = 2.05;
    let boxY = 0;
    let boxScaleY = 1, boxScaleXZ = 1;
    if (t < landT) {
      const u = prog(t, 1.6, 0.45);
      boxY = (1 - u * u) * 8.0;
    } else {
      const dt = t - landT;
      // 3 次真實阻尼回彈 (Damped Bounces)
      if (dt < 0.8) {
        const bounce = Math.abs(Math.sin(dt * 13)) * Math.exp(-dt * 6.5) * 0.45;
        boxY = bounce;
        boxScaleY = 1 - Math.sin(dt * 13) * Math.exp(-dt * 6.5) * 0.22;
        boxScaleXZ = 1 + Math.sin(dt * 13) * Math.exp(-dt * 6.5) * 0.12;
      } else {
        boxY = 0; boxScaleY = 1; boxScaleXZ = 1;
      }
    }
    const away = eio(prog(t, 7.7, 0.9));
    bigBox.position.set(lerp(1.45, 5.2, away), boxY + away * 3.4, lerp(-0.35, -2.5, away));
    const sc = lerp(1, 0.001, Math.pow(away, 1.4));
    bigBox.scale.set(sc * boxScaleXZ, sc * boxScaleY, sc * boxScaleXZ);
    bigBox.visible = t > 1.6 && sc > 0.002;

    // 開蓋動態：左右兩蓋與後蓋向外翻開，正面文字完全無死角！
    const openT = t - 3.65;
    if (openT > 0) {
      const openAng = clamp(openT * 4.5, 0, Math.PI * 0.88);
      const flapSpring = spring(openT, 2.5, 5.0) * 0.2;
      flapL.rotation.z = -(openAng + flapSpring); // 往左大角度翻開
      flapR.rotation.z = (openAng + flapSpring);  // 往右大角度翻開
      flapBack.rotation.x = -(openAng + flapSpring); // 往後翻開
    } else {
      flapL.rotation.z = 0; flapR.rotation.z = 0; flapBack.rotation.x = 0;
    }

    // 噴發小包裹：飛行弧線 + 接地兩次彈跳滾動，絕不穿透小人！
    for (const it of items) {
      const u = (t - it.launch) / it.flight, m = it.mesh;
      const vanishU = prog(t, 7.6 + it.vanishDelay, 0.28);
      if (u <= 0 || vanishU >= 1) { m.visible = false; continue; }
      m.visible = true;
      if (u < 1) {
        m.position.lerpVectors(it.from, it.to, u);
        m.position.y += 4 * it.apex * u * (1 - u);
        m.rotation.set(it.r0.x + it.w.x * u, it.r0.y + it.w.y * u, it.r0.z + it.w.z * u);
      } else {
        // 落地微彈跳物理 (Landing Bounce & Roll)
        const dtL = (t - (it.launch + it.flight));
        let bY = 0;
        if (dtL < 0.5) {
          bY = Math.abs(Math.sin(dtL * 15)) * Math.exp(-dtL * 8) * 0.22;
          m.rotation.set(it.rest.x + Math.sin(dtL * 10) * 0.2, it.rest.y, it.rest.z + Math.cos(dtL * 10) * 0.2);
        } else {
          m.rotation.copy(it.rest);
        }
        m.position.set(it.to.x, it.to.y + bY, it.to.z);
        const vs = 1 - ebackIn(vanishU);
        m.scale.setScalar(Math.max(0.001, vs));
      }
    }"""

assert old_render_s1_s2 in code, "old_render_s1_s2 not found!"
code = code.replace(old_render_s1_s2, new_render_s1_s2)

# 6. 替換第二幕與第四幕的物件更新與紙花
old_s2_pos = """    // 收納盒落在主角右側前方 (x = 0.95)，絕不擋住標籤文字！
    binder.visible = t > 26.0;
    const binderIn = prog(t, 26.0, 0.55);
    binder.position.set(0.95, lerp(4, 0.9, ebackOut(binderIn)), 0.3);
    binder.rotation.y = -0.25;
    binder.scale.setScalar(lerp(0.2, 1, ebackOut(binderIn)));

    tabCards.forEach((c, idx) => {
      const spawnT = 17.5 + idx * 0.32;
      if (t < spawnT) { c.visible = false; return; }
      c.visible = true;

      const angle = (idx / 8) * Math.PI * 2 + orbitT * 0.38 + 0.45;
      const radius = 2.8;
      const wave = Math.sin(orbitT * 2.5 + idx * 0.8);
      const orbitPos = new THREE.Vector3(Math.cos(angle) * radius, 1.25 + wave * 0.15, Math.sin(angle) * radius);
      const targetPos = new THREE.Vector3(0.95, 0.9, 0.25 - idx * 0.015);

      c.position.lerpVectors(orbitPos, targetPos, collectE);
      c.rotation.set(wave * 0.08, -angle + Math.PI / 2, Math.cos(orbitT * 2 + idx) * 0.06);
      c.scale.setScalar(lerp(1, 0.42, collectE));
      if (collectU >= 1) c.visible = false;
    });"""

new_s2_pos = """    // 收納盒落在主角右側 (x = 0.85)，拉開 1.6m 安全間距，左右平衡！
    binder.visible = t > 26.0;
    const binderIn = prog(t, 26.0, 0.55);
    binder.position.set(0.85, lerp(4, 0.85, ebackOut(binderIn)), 0.25);
    binder.rotation.y = -0.22;
    binder.scale.setScalar(lerp(0.2, 1, ebackOut(binderIn)));

    tabCards.forEach((c, idx) => {
      const spawnT = 17.5 + idx * 0.32;
      if (t < spawnT) { c.visible = false; return; }
      c.visible = true;

      const angle = (idx / 8) * Math.PI * 2 + orbitT * 0.38 + 0.45;
      const radius = 2.8;
      const wave = Math.sin(orbitT * 2.5 + idx * 0.8);
      const orbitPos = new THREE.Vector3(Math.cos(angle) * radius, 1.25 + wave * 0.15, Math.sin(angle) * radius);
      const targetPos = new THREE.Vector3(0.85, 0.85, 0.25 - idx * 0.015);

      c.position.lerpVectors(orbitPos, targetPos, collectE);
      c.rotation.set(wave * 0.08, -angle + Math.PI / 2, Math.cos(orbitT * 2 + idx) * 0.06);
      c.scale.setScalar(lerp(1, 0.42, collectE));
      if (collectU >= 1) c.visible = false;
    });"""

assert old_s2_pos in code, "old_s2_pos not found!"
code = code.replace(old_s2_pos, new_s2_pos)

# 7. 替換第四幕紙花動態
old_conf_render = """    // 紙花噴發（Confetti Burst）t = 54.0 開始
    const confT = t - 54.0;
    confettiMeshes.forEach((cf, idx) => {
      if (confT <= 0) { cf.mesh.visible = false; return; }
      cf.mesh.visible = true;
      cf.mesh.position.y -= cf.vy;
      if (cf.mesh.position.y < 0.1) cf.mesh.position.y = 3.5;
      cf.mesh.rotation.x += cf.rx; cf.mesh.rotation.y += cf.ry;
    });"""

new_conf_render = """    // 紙花噴發：真 3D 翻轉與風力擺動，禁區約束絕不擋字不插頭
    const confT = t - 53.8;
    confettiMeshes.forEach((cf, idx) => {
      if (confT <= 0) { cf.mesh.visible = false; return; }
      cf.mesh.visible = true;
      const fallLoop = (confT * cf.vy * 45) % 4.8;
      cf.mesh.position.y = 3.8 - fallLoop;
      cf.mesh.position.x = cf.origX + Math.sin(confT * cf.swayFreq + idx) * cf.swayAmp;
      cf.mesh.rotation.x = confT * cf.rx * 12;
      cf.mesh.rotation.y = confT * cf.ry * 12;
      cf.mesh.rotation.z = confT * cf.rz * 10;
    });"""

assert old_conf_render in code, "old_conf_render not found!"
code = code.replace(old_conf_render, new_conf_render)

# 8. 替換主角演技（站位、表情、各幕精準 LookAt）
old_hero_acting = """    if (t < 16.0) {
      // ---------- 第 1 幕 表演 ----------
      if (t < 2.2) {
        gazeTgt.set(1.45, 4.0, -0.35);
        browL.rotation.z = 0.25; browR.rotation.z = -0.25;
        surprised = t > 1.2;
        // 驚恐下蹲縮緊
        if (t > 1.2) { scaleY = 0.85; scaleX = 1.1; scaleZ = 1.1; }
      } else if (t < 7.6) {
        surprised = true;
        gazeTgt.set(-1.5 + Math.sin(t * 20) * 1.5, 1.0, 1.0);
        hx += Math.sin(t * 30) * 0.03;
        browL.rotation.z = 0.4; browR.rotation.z = -0.4;
      } else if (t < 11.5) {
        const hop = t - 7.6;
        hy = hop > 0 && hop < 0.6 ? Math.sin((Math.PI * hop) / 0.6) * 1.15 : 0;
        gazeTgt.set(-0.55, 0.62, 0.45);
        smiling = true;
      } else {
        gazeTgt.set(0.5, 0.5, 0.75);
        smiling = true;
      }
    } else if (t < 32.5) {
      // ---------- 第 2 幕 表演 ----------
      const jumpU = prog(t, 16.0, 0.9);
      if (jumpU < 1) {
        hx = lerp(-1.5, 0.0, eio(jumpU));
        hy = Math.sin(jumpU * Math.PI) * 1.4;
        rz = jumpU * Math.PI * 2; // 360 度歡樂空翻
      } else {
        hx = 0.0; hy = 0.0; rz = 0;
        if (t < 26.5) {
          const trackAngle = (t - 17.5) * 0.38 + 0.45;
          gazeTgt.set(Math.cos(trackAngle) * 2.5, 1.3, Math.sin(trackAngle) * 2.5);
          ry = Math.sin(t * 3.5) * 0.45;
          dizzy = t > 20.0;
          if (dizzy) {
            rx = Math.sin(t * 5.0) * 0.12;
            rz = Math.cos(t * 5.0) * 0.12; // 頭部暈陀陀擺動
          }
        } else {
          gazeTgt.set(0.95, 0.9, 0.3);
          ry = 0.3;
          smiling = true;
        }
      }
    } else if (t < 47.5) {
      // ---------- 第 3 幕 表演 ----------
      const cartT = prog(t, 32.5, 3.8);
      const cartX = lerp(-2.0, 0.3, Math.min(1, cartT * 1.2));
      
      if (t < 36.5) {
        // 開心推車：人永遠在推車後方 (cartX - 0.95)，絕對不穿模！
        hx = cartX - 0.95; hy = Math.abs(Math.sin(t * 8)) * 0.06; // 腳步踩踏彈跳
        rx = 0.12; // 前傾推車
        gazeTgt.set(cartX + 1.2, 0.5, 0.2);
        smiling = true;
      } else {
        // 撞牆後座力：人被撞彈回坐倒在地上！
        const bonkT = t - 36.5;
        const bonkDist = spring(bonkT, 3.6, 5.0) * 0.45;
        hx = 0.3 - 0.95 - 0.5 - bonkDist;
        hy = bonkT < 0.2 ? Math.sin((bonkT / 0.2) * Math.PI) * 0.25 : 0;
        rz = -0.28; // 屁股跌坐微後傾
        surprised = bonkT < 2.5;
        skeptical = bonkT >= 2.5;
        
        if (t < 40.0) {
          gazeTgt.set(1.4, 1.8, 0.2);
          browL.rotation.z = 0.45; browR.rotation.z = -0.45;
        } else {
          gazeTgt.set(hx + 0.5, 0.5 + Math.sin(t * 2) * 0.4, 0.2);
          browL.rotation.z = -0.3; browR.rotation.z = 0.2; // 挑眉懷疑
        }
      }
    } else {
      // ---------- 第 4 幕 表演 ----------
      hx = -2.1; hy = 0; hz = 0.25; ry = 0.25;
      if (t < 52.0) {
        gazeTgt.set(0, 2.5, 0);
      } else if (t < 56.0) {
        gazeTgt.set(0, 1.2, 0);
        smiling = true;
      } else {
        gazeTgt.set(-0.4, 1.5, 5.8);
        smiling = true;
        wink = t > 58.0 && t < 59.2;
        // 得意挺胸擺動
        scaleY = 1.05 + Math.sin(t * 3) * 0.03;
        scaleX = 0.96;
      }
    }"""

new_hero_acting = """    if (t < 16.0) {
      // ---------- 第 1 幕 表演 ----------
      if (t < 2.05) {
        gazeTgt.set(1.45, 4.0, -0.35);
        browL.rotation.z = 0.3; browR.rotation.z = -0.3;
        surprised = t > 1.1;
        if (t > 1.1) { scaleY = 0.82; scaleX = 1.12; scaleZ = 1.12; } // 驚恐蹲低防禦
      } else if (t < 7.6) {
        // 大箱砸地震波 + 包裹雨：小人被震波震起並壓扁，慌張後縮抱頭
        const dtImpact = t - 2.05;
        if (dtImpact < 0.4) {
          scaleY = 0.72 + Math.sin(dtImpact * 15) * 0.15;
          scaleX = 1.2;
        }
        surprised = true;
        gazeTgt.set(-1.5 + Math.sin(t * 18) * 1.8, 1.2, 0.8);
        hx += Math.sin(t * 25) * 0.025; // 驚恐微顫
        browL.rotation.z = 0.42; browR.rotation.z = -0.42;
      } else if (t < 11.5) {
        // 箱子飛離，小人歡樂大跳破涕為笑
        const hop = t - 7.6;
        hy = hop > 0 && hop < 0.65 ? Math.sin((Math.PI * hop) / 0.65) * 1.2 : 0;
        gazeTgt.set(-0.55, 0.62, 0.45);
        smiling = true;
      } else {
        gazeTgt.set(0.5, 0.5, 0.75);
        smiling = true;
      }
    } else if (t < 32.5) {
      // ---------- 第 2 幕 表演 ----------
      // 站位固定在左側三分線 x = -0.75，與收納盒 (x=0.85) 保持 1.6m 絕對安全距！
      const jumpU = prog(t, 16.0, 0.9);
      if (jumpU < 1) {
        hx = lerp(-1.5, -0.75, eio(jumpU));
        hy = Math.sin(jumpU * Math.PI) * 1.35;
        rz = jumpU * Math.PI * 2;
      } else {
        hx = -0.75; hy = 0.0; rz = 0;
        if (t < 26.5) {
          // 8 個分頁瘋狂繞行，小人兩眼蚊香眼暈眩擺頭
          const trackAngle = (t - 17.5) * 0.38 + 0.45;
          gazeTgt.set(Math.cos(trackAngle) * 2.2, 1.3, Math.sin(trackAngle) * 2.2);
          ry = Math.sin(t * 3.5) * 0.4;
          dizzy = t > 19.5;
          if (dizzy) {
            rx = Math.sin(t * 5.0) * 0.1;
            rz = Math.cos(t * 5.0) * 0.1;
          }
        } else {
          // 磁吸啪一聲收納！小人清醒，轉身向右 (ry = 0.45) 讚賞看著規格初篩表！
          dizzy = false;
          gazeTgt.set(0.85, 0.85, 0.25);
          ry = 0.42;
          smiling = true;
          scaleY = 1.04 + Math.sin(t * 4) * 0.02; // 得意挺胸
        }
      }
    } else if (t < 47.5) {
      // ---------- 第 3 幕 表演 ----------
      const cartT = prog(t, 32.5, 3.8);
      const cartX = lerp(-2.0, 0.3, Math.min(1, cartT * 1.2));
      if (t < 36.5) {
        hx = cartX - 0.95; hy = Math.abs(Math.sin(t * 8)) * 0.06;
        rx = 0.12; gazeTgt.set(cartX + 1.2, 0.5, 0.2);
        smiling = true;
      } else {
        const bonkT = t - 36.5;
        const bonkDist = spring(bonkT, 3.6, 5.0) * 0.45;
        hx = 0.3 - 0.95 - 0.5 - bonkDist;
        hy = bonkT < 0.2 ? Math.sin((bonkT / 0.2) * Math.PI) * 0.25 : 0;
        rz = -0.28;
        surprised = bonkT < 2.5;
        skeptical = bonkT >= 2.5;
        if (t < 40.0) {
          gazeTgt.set(1.4, 1.8, 0.2);
          browL.rotation.z = 0.45; browR.rotation.z = -0.45;
        } else {
          gazeTgt.set(hx + 0.5, 0.5 + Math.sin(t * 2) * 0.4, 0.2);
          browL.rotation.z = -0.3; browR.rotation.z = 0.2;
        }
      }
    } else {
      // ---------- 第 4 幕 表演 ----------
      // 站位在左側黃金點 x = -1.55, z = 0.55，整尊完完整整站在地面上，下半身絕不被切掉！
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
      }
    }"""

assert old_hero_acting in code, "old_hero_acting not found!"
code = code.replace(old_hero_acting, new_hero_acting)

html_path.write_text(code, encoding="utf-8")
print("SUCCESS: scene.html upgraded with all physical & visual fixes!")

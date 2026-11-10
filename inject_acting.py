import re
from pathlib import Path

html_p = Path(r"c:\antigravity\影片\逆向研究\claude3d_工法\scene.html")
code = html_p.read_text(encoding="utf-8")

# 1. 重構角色臉部幾何與材質
old_face_block = """// 臉部群組
const face = new THREE.Group(); face.position.set(0, 0.5, 0.465); heroBody.add(face);

// 兩顆純粹可愛的黑豆眼 + 視線追蹤
const eyeLGroup = new THREE.Group(); eyeLGroup.position.set(-0.17, 0.06, 0);
const eyeRGroup = new THREE.Group(); eyeRGroup.position.set(0.17, 0.06, 0);
face.add(eyeLGroup, eyeRGroup);

const eyeSocketGeo = new THREE.CapsuleGeometry(0.052, 0.085, 6, 12);
const socketL = new THREE.Mesh(eyeSocketGeo, M.navy); socketL.scale.z = 0.5;
const socketR = new THREE.Mesh(eyeSocketGeo, M.navy); socketR.scale.z = 0.5;
eyeLGroup.add(socketL); eyeRGroup.add(socketR);

// 眉毛（傾斜表達恐懼、懷疑、驚訝）
const browGeo = new THREE.BoxGeometry(0.14, 0.032, 0.02);
const browL = new THREE.Mesh(browGeo, M.navy); browL.position.set(-0.17, 0.165, 0.01);
const browR = new THREE.Mesh(browGeo, M.navy); browR.position.set(0.17, 0.165, 0.01);
face.add(browL, browR);

// 臉頰紅暈
[-0.29, 0.29].forEach((x) => {
  const c = new THREE.Mesh(new THREE.CircleGeometry(0.065, 24), M.cheek);
  c.position.set(x, -0.06, 0.006); face.add(c);
});

// 嘴型
const smile = new THREE.Mesh(new THREE.TorusGeometry(0.075, 0.017, 10, 24, Math.PI), M.navy);
smile.rotation.z = Math.PI; smile.position.set(0, -0.06, 0.01); face.add(smile);
const oMouth = new THREE.Mesh(new THREE.TorusGeometry(0.045, 0.018, 10, 24), M.navy);
oMouth.position.set(0, -0.09, 0.01); face.add(oMouth);
const straightMouth = new THREE.Mesh(new THREE.BoxGeometry(0.13, 0.025, 0.02), M.navy);
straightMouth.position.set(0, -0.08, 0.01); face.add(straightMouth); straightMouth.visible = false;

// 眩暈蚊香眼（第2幕）
const dizzyEyes = new THREE.Group(); dizzyEyes.position.set(0, 0.06, 0.01); face.add(dizzyEyes);
[-0.17, 0.17].forEach((x) => {
  const de = new THREE.Mesh(new THREE.TorusGeometry(0.055, 0.016, 8, 20), M.navy);
  de.position.x = x; dizzyEyes.add(de);
});
dizzyEyes.visible = false;"""

new_face_block = """// 臉部群組：具備超立體皮克斯靈魂的高表現力臉部系統
const face = new THREE.Group(); face.position.set(0, 0.5, 0.47); heroBody.add(face);

// 兩顆大黑豆眼（支援瞪大、瞇眼、眨眼、視線追蹤）
const eyeLGroup = new THREE.Group(); eyeLGroup.position.set(-0.18, 0.07, 0);
const eyeRGroup = new THREE.Group(); eyeRGroup.position.set(0.18, 0.07, 0);
face.add(eyeLGroup, eyeRGroup);

const eyeSocketGeo = new THREE.CapsuleGeometry(0.062, 0.095, 8, 16);
const socketL = new THREE.Mesh(eyeSocketGeo, M.navy); socketL.scale.z = 0.5;
const socketR = new THREE.Mesh(eyeSocketGeo, M.navy); socketR.scale.z = 0.5;
eyeLGroup.add(socketL); eyeRGroup.add(socketR);

// 立體加粗圓角眉毛（大幅增強戲劇表現力）
const browGeo = new RoundedBoxGeometry(0.22, 0.065, 0.035, 2, 0.015);
const browL = new THREE.Mesh(browGeo, M.navy); browL.position.set(-0.18, 0.20, 0.015);
const browR = new THREE.Mesh(browGeo, M.navy); browR.position.set(0.18, 0.20, 0.015);
face.add(browL, browR);

// 臉頰紅暈
[-0.30, 0.30].forEach((x) => {
  const c = new THREE.Mesh(new THREE.CircleGeometry(0.075, 24), M.cheek);
  c.position.set(x, -0.06, 0.006); face.add(c);
});

// 嘴型集合（加粗、大弧度、生動立體）
// 1. 燦爛微笑嘴
const smileMouth = new THREE.Mesh(new THREE.TorusGeometry(0.10, 0.026, 12, 32, Math.PI), M.navy);
smileMouth.rotation.z = Math.PI; smileMouth.position.set(0, -0.06, 0.015); face.add(smileMouth);

// 2. 驚恐大張 O 嘴（立體大開口）
const oMouth = new THREE.Mesh(new THREE.TorusGeometry(0.08, 0.032, 12, 32), M.navy);
oMouth.position.set(0, -0.09, 0.015); face.add(oMouth);

// 3. 委屈撇嘴 / 哀號苦瓜嘴（倒扣下垂）
const sadMouth = new THREE.Mesh(new THREE.TorusGeometry(0.095, 0.026, 12, 32, Math.PI), M.navy);
sadMouth.position.set(0, -0.11, 0.015); face.add(sadMouth);

// 4. 緊繃一字嘴（咬牙切齒）
const straightMouth = new THREE.Mesh(new RoundedBoxGeometry(0.20, 0.045, 0.03, 2, 0.01), M.navy);
straightMouth.position.set(0, -0.08, 0.015); face.add(straightMouth);

// 眩暈蚊香眼（第2幕）
const dizzyEyes = new THREE.Group(); dizzyEyes.position.set(0, 0.07, 0.015); face.add(dizzyEyes);
[-0.18, 0.18].forEach((x) => {
  const de = new THREE.Mesh(new THREE.TorusGeometry(0.065, 0.020, 8, 24), M.navy);
  de.position.x = x; dizzyEyes.add(de);
});
dizzyEyes.visible = false;"""

assert old_face_block in code, "old_face_block not found!"
code = code.replace(old_face_block, new_face_block)

# 2. 重構第一幕小包裹生成：全部朝小橘塊那邊掉落堆疊，形成紙箱山！
old_slots_block = """const R = rng(20261109);
const N = 64, items = [];
const slots = [];
// 嚴格避開小人本體與正前胸視角，箱子散落在兩側與後方，主角清晰可見！
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
}
slots.sort((p, q) => p.y - q.y);
for (let k = 0; k < N; k++) {
  const isTag = R() < 0.28, s = 0.2 + R() * 0.17;
  let mesh;
  if (isTag) {
    mesh = new THREE.Group();
    const base = shadowy(new THREE.Mesh(new RoundedBoxGeometry(0.42, 0.26, 0.025, 2, 0.01), M.paper));
    const lab = new THREE.Mesh(new THREE.PlaneGeometry(0.4, 0.25), new THREE.MeshStandardMaterial({ map: tagTexs[k % 5], transparent: true, roughness: 0.7 }));
    lab.position.z = 0.014; mesh.add(base, lab);
  } else {
    mesh = new THREE.Group();
    const b = shadowy(new THREE.Mesh(new RoundedBoxGeometry(s * 1.25, s, s, 2, 0.025), M.card));
    const tp = new THREE.Mesh(new THREE.BoxGeometry(s * 0.28, 0.006, s + 0.004), M.tape);
    tp.position.y = s / 2 + 0.002; mesh.add(b, tp);
  }
  s1Group.add(mesh);
  const slot = slots[k];
  items.push({
    mesh, isTag,
    launch: 3.8 + (k / N) * 1.2,
    flight: 0.55 + R() * 0.3,
    apex: 1.3 + R() * 1.3,
    from: new THREE.Vector3(1.45 + (R() - 0.5) * 1.2, 1.75, -0.35 + (R() - 0.5) * 0.8),
    to: new THREE.Vector3(slot.x, slot.y + (isTag ? 0.03 : s / 2), slot.z),
    r0: new THREE.Euler(R() * 6, R() * 6, R() * 6),
    w: new THREE.Vector3((R() - 0.5) * 16, (R() - 0.5) * 16, (R() - 0.5) * 16),
    rest: new THREE.Euler(isTag ? -Math.PI / 2 + (R() - 0.5) * 0.5 : (R() - 0.5) * 0.4, R() * 6, (R() - 0.5) * 0.4),
    vanishDelay: Math.hypot(slot.x - (-1.5), slot.z - 0.15) * 0.22,
  });
}"""

new_slots_block = """const R = rng(20261109);
// 84 個大大小小的紙箱與標籤，形成鋪天蓋地砸向小橘塊並堆疊掩埋的震撼奇景！
const N = 84, items = [];
const slots = [];

for (let k = 0; k < N; k++) {
  // 分層堆疊演算法：
  // 0~25: 堆在小橘塊四周貼身下層 (r = 0.35~0.8, y = 0.1~0.3)
  // 26~55: 堆在小橘塊身上與兩側中層 (r = 0.18~0.65, y = 0.35~0.65)
  // 56~83: 直接砸向小橘塊頭頂身側高處 (r = 0.05~0.45, y = 0.7~1.15)
  let r, y;
  if (k < 26) {
    r = 0.45 + Math.sqrt(k / 26) * 0.65;
    y = 0.10 + (k % 3) * 0.10;
  } else if (k < 56) {
    r = 0.22 + Math.sqrt((k - 26) / 30) * 0.45;
    y = 0.35 + ((k - 26) % 3) * 0.12;
  } else {
    r = 0.08 + Math.sqrt((k - 56) / 28) * 0.35;
    y = 0.65 + ((k - 56) % 4) * 0.13;
  }
  const a = k * 2.39996;
  const sx = -1.5 + Math.cos(a) * r * 1.15;
  const sz = 0.15 + Math.sin(a) * r * 0.85;
  slots.push({ x: sx, z: sz, y: y });
}

for (let k = 0; k < N; k++) {
  const isTag = R() < 0.22;
  const s = 0.18 + R() * 0.22; // 大小豐富：0.18 ~ 0.40m
  let mesh;
  if (isTag) {
    mesh = new THREE.Group();
    const base = shadowy(new THREE.Mesh(new RoundedBoxGeometry(0.38, 0.24, 0.02, 2, 0.01), M.paper));
    const lab = new THREE.Mesh(new THREE.PlaneGeometry(0.36, 0.22), new THREE.MeshStandardMaterial({ map: tagTexs[k % 5], transparent: true, roughness: 0.7 }));
    lab.position.z = 0.012; mesh.add(base, lab);
  } else {
    mesh = new THREE.Group();
    const b = shadowy(new THREE.Mesh(new RoundedBoxGeometry(s * 1.25, s, s, 2, 0.02), M.card));
    const tp = new THREE.Mesh(new THREE.BoxGeometry(s * 0.28, 0.006, s + 0.004), M.tape);
    tp.position.y = s / 2 + 0.002; mesh.add(b, tp);
  }
  s1Group.add(mesh);
  const slot = slots[k];
  // 爆發飛散目標：t = 7.6 破土大爆發時向四周炸飛的向量
  const burstDir = new THREE.Vector3(slot.x - (-1.5), slot.y * 1.5 + 0.4, slot.z - 0.15).normalize().multiplyScalar(4.5 + R() * 3.0);
  
  items.push({
    mesh, isTag, s,
    launch: 3.75 + (k / N) * 1.4, // 3.75s ~ 5.15s 連續傾瀉砸落
    flight: 0.48 + R() * 0.25,
    apex: 1.4 + R() * 1.2,
    from: new THREE.Vector3(1.45 + (R() - 0.5) * 1.2, 1.75, -0.35 + (R() - 0.5) * 0.8),
    to: new THREE.Vector3(slot.x, slot.y, slot.z),
    burstDir,
    r0: new THREE.Euler(R() * 6, R() * 6, R() * 6),
    w: new THREE.Vector3((R() - 0.5) * 18, (R() - 0.5) * 18, (R() - 0.5) * 18),
    rest: new THREE.Euler(isTag ? -Math.PI / 2 + (R() - 0.5) * 0.4 : (R() - 0.5) * 0.35, R() * 6, (R() - 0.5) * 0.35),
    vanishDelay: Math.hypot(slot.x - (-1.5), slot.z - 0.15) * 0.15,
  });
}"""

assert old_slots_block in code, "old_slots_block not found!"
code = code.replace(old_slots_block, new_slots_block)

# 3. 重構包裹渲染：被淹沒堆疊 + t=7.6 破土大爆破炸飛！
old_render_items = """    // 噴發小包裹：飛行弧線 + 接地兩次彈跳滾動，絕不穿透小人！
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

new_render_items = """    // 噴發小包裹：傾瀉砸向小橘塊堆疊成山 + t=7.6 破土破山大炸飛！
    for (const it of items) {
      const u = (t - it.launch) / it.flight, m = it.mesh;
      if (u <= 0) { m.visible = false; continue; }
      m.visible = true;

      if (t < 7.6) {
        // 飛行與堆疊掩埋階段
        if (u < 1) {
          m.position.lerpVectors(it.from, it.to, u);
          m.position.y += 4 * it.apex * u * (1 - u);
          m.rotation.set(it.r0.x + it.w.x * u, it.r0.y + it.w.y * u, it.r0.z + it.w.z * u);
        } else {
          const dtL = t - (it.launch + it.flight);
          let bY = 0;
          if (dtL < 0.35) {
            bY = Math.abs(Math.sin(dtL * 18)) * Math.exp(-dtL * 9) * 0.18;
          }
          m.position.set(it.to.x, it.to.y + bY, it.to.z);
          m.rotation.copy(it.rest);
        }
        m.scale.setScalar(1.0);
      } else {
        // t >= 7.6：小橘塊衝天破土！所有箱子受衝擊力向四周爆炸震飛散開！
        const burstT = t - 7.6;
        const bU = clamp(burstT / 0.65);
        m.position.set(
          it.to.x + it.burstDir.x * bU,
          it.to.y + it.burstDir.y * bU - 4.9 * bU * bU,
          it.to.z + it.burstDir.z * bU
        );
        m.rotation.x += 0.25; m.rotation.y += 0.2;
        const fade = clamp(1.0 - (burstT - 0.25) / 0.45);
        m.scale.setScalar(Math.max(0.001, fade));
        if (fade <= 0.002) m.visible = false;
      }
    }"""

assert old_render_items in code, "old_render_items not found!"
code = code.replace(old_render_items, new_render_items)

# 4. 重構主角表演與表情系統（眉毛、嘴型、眼睛連動，徹底杜絕未被砸到就莫名變扁！）
old_hero_acting = """    // 視線目標
    let gazeTgt = new THREE.Vector3(0, 1.5, 8.0);

    if (t < 16.0) {
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
    } else if (t < 32.5) {"""

new_hero_acting = """    // 視線目標與五官動態變數
    let gazeTgt = new THREE.Vector3(0, 1.5, 8.0);
    let eyeScaleX = 1.0, eyeScaleY = 1.0;
    let browY = 0.20, browRotL = 0.0, browRotR = 0.0;
    let mouthType = "smile"; // smile, o, sad, straight
    let mouthScale = 1.0;

    if (t < 16.0) {
      // ---------- 第 1 幕 表演（皮克斯級戲劇靈魂） ----------
      if (t < 1.3) {
        // 0.0 ~ 1.3s: 挺直身體，天真可愛微笑，身體完全不扁！
        scaleX = scaleY = scaleZ = 1.0;
        smiling = true; mouthType = "smile";
        gazeTgt.set(-1.5, 1.2, 5.0);
        browY = 0.20; browRotL = 0.05; browRotR = -0.05;
      } else if (t < 2.05) {
        // 1.3 ~ 2.05s: 聽到頭頂轟隆巨響，抬頭仰望天空（身體完全不扁！挺拔向上看）
        scaleX = scaleY = scaleZ = 1.0;
        rx = -0.32; // 大幅仰頭看天！
        gazeTgt.set(1.45, 6.5, -0.35); // 仰望天上急速掉落的大箱子
        eyeScaleX = 1.35; eyeScaleY = 1.35; // 兩眼瞪大圓滾滾！
        browY = 0.25; browRotL = 0.45; browRotR = -0.45; // 雙眉高挑成倒八字（大驚）
        mouthType = "o"; mouthScale = 0.85; // 嘴巴微張成驚訝小 O 型
      } else if (t < 3.7) {
        // 2.05 ~ 3.7s: 大箱「轟！」砸地！強烈地面衝擊波席捲小人！
        const dtLand = t - 2.05;
        rx = 0.0;
        if (dtLand < 0.6) {
          // 震波傳來：先被震得騰空離地，再重重壓扁回彈！
          hy = Math.sin((dtLand / 0.6) * Math.PI) * 0.22;
          scaleY = 0.70 + Math.sin(dtLand * 14) * 0.25;
          scaleX = 1.22 - Math.sin(dtLand * 14) * 0.18;
          scaleZ = 1.15;
          eyeScaleX = 1.4; eyeScaleY = 1.4; // 驚呆瞪圓
          browY = 0.26; browRotL = 0.55; browRotR = -0.55;
          mouthType = "o"; mouthScale = 1.35; // 嘴巴大張！
        } else {
          // 震波過後稍稍回正，驚恐未定望向右邊的大箱子
          gazeTgt.set(1.45, 0.8, -0.35);
          ry = 0.35;
          eyeScaleX = 1.2; eyeScaleY = 1.2;
          browY = 0.22; browRotL = 0.35; browRotR = -0.35;
          mouthType = "straight"; // 緊咬牙關
        }
      } else if (t < 7.6) {
        // 3.7 ~ 7.6s: 漫天大大小小紙箱如瀑布般砸向小橘塊！
        const dtSwarm = t - 3.7;
        gazeTgt.set(-1.5 + Math.sin(t * 15) * 0.8, 1.8, 0.5); // 慌亂看著四周漫天落下的箱子
        hx += Math.sin(t * 30) * 0.025; // 驚恐顫抖

        // 隨著越來越多箱子堆在頭上身邊，小橘塊被真正「砸扁下沉淹沒」！
        const crushU = clamp(dtSwarm / 2.2); // 0 ~ 1 逐漸被壓扁
        hy = -crushU * 0.22; // 身體下沉進箱子堆
        scaleY = lerp(1.0, 0.60, crushU); // 被壓成扁扁的果凍！
        scaleX = lerp(1.0, 1.30, crushU);
        scaleZ = lerp(1.0, 1.25, crushU);

        // 表情：從驚恐大 O 嘴，到被壓得痛苦瞇眼（><）、嘴角下撇苦瓜臉！
        if (crushU < 0.4) {
          eyeScaleX = 1.4; eyeScaleY = 1.4;
          browY = 0.25; browRotL = 0.6; browRotR = -0.6;
          mouthType = "o"; mouthScale = 1.4;
        } else {
          // 被箱子壓扁淹沒中：兩眼緊閉成一字痛苦瞇眼！眉毛緊皺！
          eyeScaleX = 1.3; eyeScaleY = 0.10; // 瞇瞇眼！
          browY = 0.14; browRotL = 0.70; browRotR = -0.70; // 眉頭深鎖
          mouthType = "sad"; mouthScale = 1.1; // 嘴角下垂苦不堪言
        }
      } else if (t < 11.5) {
        // 7.6 ~ 11.5s: 破土大爆發！把身上的箱子全震飛，衝天大跳開懷大笑！
        const hopT = t - 7.6;
        if (hopT < 0.75) {
          const hopU = hopT / 0.75;
          hy = Math.sin(hopU * Math.PI) * 1.5; // 衝上 1.5 米高空！
          scaleY = 1.35; scaleX = 0.82; scaleZ = 0.82; // 向上延展拉伸 Stretch！
          rz = hopU * Math.PI * 2; // 空中 360 度歡樂空翻！
          eyeScaleX = 1.3; eyeScaleY = 1.3;
          browY = 0.24; browRotL = -0.2; browRotR = 0.2;
          mouthType = "smile"; mouthScale = 1.4; // 燦爛大笑！
          gazeTgt.set(-0.55, 0.62, 5.0);
        } else {
          // 落地平穩站好，開心看著飛來的比較表
          const settleT = hopT - 0.75;
          hy = 0; rz = 0;
          scaleY = 1 + spring(settleT, 3.5, 6.0) * 0.15;
          scaleX = 1 - spring(settleT, 3.5, 6.0) * 0.1;
          eyeScaleX = 1.0; eyeScaleY = 1.0;
          browY = 0.20; browRotL = 0; browRotR = 0;
          mouthType = "smile";
          gazeTgt.set(-0.55, 0.62, 0.45);
        }
      } else {
        gazeTgt.set(0.5, 0.5, 0.75);
        mouthType = "smile";
      }
    } else if (t < 32.5) {"""

assert old_hero_acting in code, "old_hero_acting not found!"
code = code.replace(old_hero_acting, new_hero_acting)

# 5. 更新第 2、3、4 幕的表情參數
old_s2_acting = """        if (t < 26.5) {
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
          ry = 0.45; rx = 0.06;
          smiling = true;
          scaleY = 1.04 + Math.sin(t * 4) * 0.02; // 得意挺胸
        }"""

new_s2_acting = """        if (t < 26.5) {
          const trackAngle = (t - 17.5) * 0.38 + 0.45;
          gazeTgt.set(Math.cos(trackAngle) * 2.2, 1.3, Math.sin(trackAngle) * 2.2);
          ry = Math.sin(t * 3.5) * 0.4;
          dizzy = t > 19.5;
          if (dizzy) {
            rx = Math.sin(t * 5.0) * 0.1;
            rz = Math.cos(t * 5.0) * 0.1;
            mouthType = "sad"; mouthScale = 0.9; // 暈得撇嘴
            browY = 0.15; browRotL = 0.3; browRotR = -0.3;
          } else {
            mouthType = "o"; mouthScale = 0.8;
            browY = 0.22; browRotL = 0.2; browRotR = -0.2;
          }
        } else {
          dizzy = false;
          gazeTgt.set(0.85, 0.85, 0.25);
          ry = 0.45; rx = 0.06;
          mouthType = "smile"; mouthScale = 1.25; // 得意大微笑
          browY = 0.22; browRotL = -0.15; browRotR = 0.15; // 自信揚眉
          scaleY = 1.05 + Math.sin(t * 4) * 0.03;
        }"""

assert old_s2_acting in code, "old_s2_acting not found!"
code = code.replace(old_s2_acting, new_s2_acting)

# 6. 更新第 3 幕表情
old_s3_acting = """      if (t < 36.5) {
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
      }"""

new_s3_acting = """      if (t < 36.5) {
        hx = cartX - 0.95; hy = Math.abs(Math.sin(t * 8)) * 0.06;
        rx = 0.12; gazeTgt.set(cartX + 1.2, 0.5, 0.2);
        mouthType = "smile"; browY = 0.20;
      } else {
        const bonkT = t - 36.5;
        const bonkDist = spring(bonkT, 3.6, 5.0) * 0.45;
        hx = 0.3 - 0.95 - 0.5 - bonkDist;
        hy = bonkT < 0.2 ? Math.sin((bonkT / 0.2) * Math.PI) * 0.25 : 0;
        rz = -0.28;
        if (bonkT < 2.5) {
          // 猛然撞門：大驚呆跌坐！
          gazeTgt.set(1.4, 1.8, 0.2);
          eyeScaleX = 1.35; eyeScaleY = 1.35;
          browY = 0.25; browRotL = 0.55; browRotR = -0.55;
          mouthType = "o"; mouthScale = 1.2;
        } else {
          // 挑眉懷疑思考（一眉高一眉低）
          gazeTgt.set(hx + 0.5, 0.5 + Math.sin(t * 2) * 0.4, 0.2);
          browY = 0.20; browRotL = -0.45; browRotR = 0.35; // 挑眉懷疑！
          mouthType = "straight"; mouthScale = 1.1; // 撇平嘴思考
        }
      }"""

assert old_s3_acting in code, "old_s3_acting not found!"
code = code.replace(old_s3_acting, new_s3_acting)

# 7. 更新第 4 幕表情
old_s4_acting = """      if (t < 52.0) {
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

new_s4_acting = """      if (t < 52.0) {
        gazeTgt.set(0, 2.5, 0);
        mouthType = "o"; mouthScale = 0.7; browY = 0.22;
      } else if (t < 56.5) {
        gazeTgt.set(0.0, 1.5, 0.0);
        rx = -0.08; // 抬頭仰望
        mouthType = "smile"; mouthScale = 1.2;
        browY = 0.22; browRotL = -0.15; browRotR = 0.15;
      } else {
        gazeTgt.set(-0.3, 1.4, 5.5);
        rx = 0;
        wink = t > 57.8 && t < 59.2;
        mouthType = "smile"; mouthScale = 1.35; // 自信燦笑
        browY = 0.24; browRotL = -0.2; browRotR = 0.2;
        scaleY = 1.06 + Math.sin(t * 3.2) * 0.03;
        scaleX = 0.95;
      }"""

assert old_s4_acting in code, "old_s4_acting not found!"
code = code.replace(old_s4_acting, new_s4_acting)

# 8. 替換臉部最終渲染邏輯：完全掌控眉毛、眼睛、嘴型
old_face_apply = """    // 表情切換
    dizzyEyes.visible = dizzy;
    socketL.visible = !dizzy; socketR.visible = !dizzy;
    if (wink) { socketL.scale.y = 0.15; socketR.scale.y = 1.0; }
    else if (!dizzy) { socketL.scale.y = socketR.scale.y = (Math.sin(t * 4.5) > 0.96 ? 0.2 : 1.0); }

    oMouth.visible = surprised && !dizzy;
    smile.visible = smiling && !surprised && !dizzy;
    straightMouth.visible = skeptical || dizzy;"""

new_face_apply = """    // 表情與五官連動渲染
    dizzyEyes.visible = dizzy;
    socketL.visible = !dizzy; socketR.visible = !dizzy;

    // 眼睛縮放與眨眼
    if (dizzy) {
      dizzyEyes.rotation.z = t * 6.0;
    } else if (wink) {
      socketL.scale.set(eyeScaleX, 0.12, 0.5);
      socketR.scale.set(eyeScaleX, eyeScaleY, 0.5);
    } else {
      const isBlink = Math.sin(t * 4.2) > 0.97;
      const curEyeY = isBlink ? 0.15 : eyeScaleY;
      socketL.scale.set(eyeScaleX, curEyeY, 0.5);
      socketR.scale.set(eyeScaleX, curEyeY, 0.5);
    }

    // 眉毛動態控制（高挑、鎖緊、傾斜角度）
    browL.position.y = browY; browR.position.y = browY;
    browL.rotation.z = browRotL; browR.rotation.z = browRotR;

    // 嘴型切換與縮放
    smileMouth.visible = mouthType === "smile" && !dizzy;
    oMouth.visible = mouthType === "o" && !dizzy;
    sadMouth.visible = mouthType === "sad" || dizzy;
    straightMouth.visible = mouthType === "straight" && !dizzy;

    if (smileMouth.visible) smileMouth.scale.setScalar(mouthScale);
    if (oMouth.visible) oMouth.scale.setScalar(mouthScale);
    if (sadMouth.visible) sadMouth.scale.setScalar(mouthScale);
    if (straightMouth.visible) straightMouth.scale.setScalar(mouthScale);"""

assert old_face_apply in code, "old_face_apply not found!"
code = code.replace(old_face_apply, new_face_apply)

html_p.write_text(code, encoding="utf-8")
print("SUCCESS: Full Facial Rigging & Avalanche Staging injected into scene.html!")

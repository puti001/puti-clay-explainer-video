import re
from pathlib import Path

html_p = Path(r"c:\antigravity\影片\逆向研究\claude3d_工法\scene.html")
code = html_p.read_text(encoding="utf-8")

# 我們寫一個完整的重構版本，將極簡黏土小人、原片色彩、接觸陰影、零穿模佈局一次性注入！
rebuilt_code = """<!DOCTYPE html>
<html lang="zh-TW">
<head>
<meta charset="utf-8">
<title>Puti-AI | 3D 知識點影片</title>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  html, body { width: 100%; height: 100%; overflow: hidden; background: #eae5db; font-family: "HunInn", "Noto Sans TC", sans-serif; }
  #canvas-container { position: absolute; inset: 0; width: 100%; height: 100%; }
  canvas { display: block; width: 100% !important; height: 100% !important; }
  
  #chapter {
    position: absolute; top: 48px; left: 56px;
    background: rgba(255, 255, 255, 0.94);
    border: 1.5px solid rgba(0,0,0,0.06);
    color: #1a233a; font-size: 26px; font-weight: 900;
    padding: 14px 28px; border-radius: 999px;
    box-shadow: 0 12px 32px rgba(26,35,58,0.08);
    display: flex; align-items: center; gap: 14px;
    letter-spacing: 0.5px;
    backdrop-filter: blur(12px);
  }
  #chapter .num {
    background: #c85624; color: #fff; width: 34px; height: 34px;
    border-radius: 50%; display: flex; align-items: center; justify-content: center;
    font-size: 20px; font-weight: 900;
  }
  
  #sub {
    position: absolute; bottom: 84px; left: 50%; transform: translateX(-50%);
    background: rgba(24, 34, 60, 0.92); color: #fff;
    font-size: 38px; font-weight: 800; letter-spacing: 1.2px;
    padding: 16px 42px; border-radius: 20px;
    box-shadow: 0 16px 40px rgba(0,0,0,0.22);
    text-align: center; max-width: 85%;
    line-height: 1.35; white-space: nowrap;
    transition: opacity 0.15s ease-out;
    backdrop-filter: blur(10px);
  }

  #puti-footer {
    position: absolute; bottom: 18px; left: 50%; transform: translateX(-50%);
    font-size: 14px; font-weight: 600; color: rgba(26, 35, 58, 0.52);
    letter-spacing: 0.5px; white-space: nowrap;
  }
  #puti-footer a { color: #c85624; text-decoration: underline; font-weight: 700; margin-left: 4px; }
</style>

<script type="importmap">
{
  "imports": {
    "three": "./node_modules/three/build/three.module.js",
    "three/addons/": "./node_modules/three/examples/jsm/"
  }
}
</script>
</head>
<body>
<div id="canvas-container"></div>
<div id="chapter"><span class="num">1</span> 破題：五百億筆商品</div>
<div id="sub">你丟給 AI 五百億筆商品，</div>
<div id="puti-footer">屏東縣後庄國小黃朝榮老師作品，免費分享，歡迎擴散推廣，嚴禁商用與任何侵權、不尊重著作權的行為，更多 Puti-AI 教學工具 <a href="https://padlet.com/clongwh/puti_ai_tools" target="_blank">點此前往</a></div>

<script type="module">
import * as THREE from "three";
import { RoundedBoxGeometry } from "three/addons/geometries/RoundedBoxGeometry.js";
import { TTFLoader } from "three/addons/loaders/TTFLoader.js";
import { Font } from "three/addons/loaders/FontLoader.js";
import { TextGeometry } from "three/addons/geometries/TextGeometry.js";

const cuesReq = await fetch("cues.json");
const cuesData = await cuesReq.json();
const C = cuesData.cues;
const TOTAL = cuesData.total;

// ==========================================
// 數學與緩動輔助函式
// ==========================================
const clamp = (v, min = 0, max = 1) => Math.max(min, Math.min(max, v));
const lerp = (a, b, t) => a + (b - a) * t;
const prog = (t, s, d) => clamp((t - s) / d);
const eout = (t) => 1 - Math.pow(1 - t, 3);
const eio = (t) => t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;
const ebackOut = (t, s = 1.70158) => { const u = t - 1; return u * u * ((s + 1) * u + s) + 1; };
const ebackIn = (t, s = 1.70158) => t * t * ((s + 1) * t - s);
const spring = (t, freq = 3.5, decay = 5.5) => Math.exp(-decay * t) * Math.cos(freq * Math.PI * 2 * t);

function rng(seed) {
  let s = seed % 2147483647;
  if (s <= 0) s += 2147483646;
  return () => { s = (s * 16807) % 2147483647; return (s - 1) / 2147483646; };
}

// ==========================================
// 渲染器與攝影機（電影級棚拍設定）
// ==========================================
const W = 1920, H = 1080;
const scene = new THREE.Scene();
scene.background = new THREE.Color(0xeae5db); // 原片同款溫潤象牙米灰

const camera = new THREE.PerspectiveCamera(28, W / H, 0.1, 100);
const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: false, powerPreference: "high-performance" });
renderer.setSize(W, H);
renderer.setPixelRatio(1);
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;

// ACESFilmic 色調映射：壓住死白、高光平滑滾降、釋放深層色彩飽和度
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.05;
document.getElementById("canvas-container").appendChild(renderer.domElement);

// ==========================================
// 雙色溫棚拍燈光系統（暖金主光 + 冷天光漫反射）
// ==========================================
const hemi = new THREE.HemisphereLight(0xfffaed, 0xd2c8b8, 1.0);
scene.add(hemi);

const dir1 = new THREE.DirectionalLight(0xfff5e4, 1.85); // 暖金主光
dir1.position.set(5.5, 9.5, 7.5);
dir1.castShadow = true;
dir1.shadow.mapSize.width = 2048;
dir1.shadow.mapSize.height = 2048;
dir1.shadow.camera.near = 1;
dir1.shadow.camera.far = 25;
dir1.shadow.camera.left = -6;
dir1.shadow.camera.right = 6;
dir1.shadow.camera.top = 6;
dir1.shadow.camera.bottom = -6;
dir1.shadow.bias = -0.0003;
dir1.shadow.radius = 3.5;
scene.add(dir1);

const dir2 = new THREE.DirectionalLight(0x9db8eb, 0.85); // 冷藍天光（暗部補光）
dir2.position.set(-6, 7, -4);
scene.add(dir2);

// ==========================================
// 接觸陰影生成器（Contact Shadow & Ground AO）
// ==========================================
function createContactShadowTexture(radius = 256) {
  const c = document.createElement("canvas");
  c.width = c.height = radius;
  const ctx = c.getContext("2d");
  const grad = ctx.createRadialGradient(radius/2, radius/2, 0, radius/2, radius/2, radius/2);
  grad.addColorStop(0, "rgba(22, 18, 14, 0.52)");
  grad.addColorStop(0.35, "rgba(32, 25, 20, 0.32)");
  grad.addColorStop(0.70, "rgba(45, 36, 28, 0.12)");
  grad.addColorStop(1, "rgba(0, 0, 0, 0)");
  ctx.fillStyle = grad;
  ctx.fillRect(0, 0, radius, radius);
  const tex = new THREE.CanvasTexture(c);
  tex.minFilter = THREE.LinearFilter;
  return tex;
}
const contactTex = createContactShadowTexture();

function createContactShadowMesh(w, h, opacity = 0.8) {
  const geo = new THREE.PlaneGeometry(w, h);
  const mat = new THREE.MeshBasicMaterial({
    map: contactTex, transparent: true, opacity: opacity, depthWrite: false
  });
  const m = new THREE.Mesh(geo, mat);
  m.rotation.x = -Math.PI / 2;
  m.position.y = 0.005;
  scene.add(m);
  return m;
}

// 攝影棚無縫底板
const cyclorama = new THREE.Mesh(
  new THREE.PlaneGeometry(80, 80),
  new THREE.MeshStandardMaterial({ color: 0xeae5db, roughness: 0.95, metalness: 0.0 })
);
cyclorama.rotation.x = -Math.PI / 2;
cyclorama.receiveShadow = true;
scene.add(cyclorama);

// ==========================================
// 原片同款包浩斯深邃色票（M）
// ==========================================
const M = {
  orange:    new THREE.MeshStandardMaterial({ color: 0xc85624, roughness: 0.65, metalness: 0.04 }), // 原片赤陶焦糖土
  navy:      new THREE.MeshStandardMaterial({ color: 0x16223e, roughness: 0.55, metalness: 0.08 }), // 深海群青藍
  navyText:  new THREE.MeshStandardMaterial({ color: 0x182442, roughness: 0.45, metalness: 0.10 }),
  card:      new THREE.MeshStandardMaterial({ color: 0xbf8e54, roughness: 0.75, metalness: 0.02 }), // 復古牛皮紙褐
  paper:     new THREE.MeshStandardMaterial({ color: 0xfbf8f2, roughness: 0.60, metalness: 0.0 }),  // 溫潤暖白紙質
  metalGate: new THREE.MeshStandardMaterial({ color: 0x1c273e, roughness: 0.35, metalness: 0.65 }), // 消光金屬深藍
  yellow:    new THREE.MeshStandardMaterial({ color: 0xf59e0b, roughness: 0.50, metalness: 0.05 }), // 原片鉻黃
  red:       new THREE.MeshStandardMaterial({ color: 0xd93829, roughness: 0.55, metalness: 0.05 }), // 原片朱紅
  green:     new THREE.MeshStandardMaterial({ color: 0x059669, roughness: 0.50, metalness: 0.05 }), // 翡翠薄荷綠
  cheek:     new THREE.MeshBasicMaterial({ color: 0xf29179, transparent: true, opacity: 0.65 }),
  tape:      new THREE.MeshStandardMaterial({ color: 0xf3eee3, roughness: 0.5, transparent: true, opacity: 0.88 }),
  funnel:    new THREE.MeshStandardMaterial({ color: 0xf59e0b, roughness: 0.45, metalness: 0.15 }),
};
const shadowy = (m) => { m.castShadow = true; m.receiveShadow = true; return m; };

// 2.5x 超取樣標籤文字紋理
function labelTex(w, h, draw) {
  const S = 2.5;
  const c = document.createElement("canvas");
  c.width = Math.round(w * S); c.height = Math.round(h * S);
  const x = c.getContext("2d");
  x.scale(S, S);
  draw(x, w, h);
  const t = new THREE.CanvasTexture(c);
  t.anisotropy = 16;
  t.minFilter = THREE.LinearFilter;
  t.generateMipmaps = false;
  return t;
}
function rr(x, px, py, pw, ph, r) {
  x.beginPath(); x.moveTo(px + r, py);
  x.arcTo(px + pw, py, px + pw, py + ph, r);
  x.arcTo(px + pw, py + ph, px, py + ph, r);
  x.arcTo(px, py + ph, px, py, r);
  x.arcTo(px, py, px + pw, py, r); x.closePath();
}

// ==========================================
// 角色：原片同款・極簡黏土小人（零眉毛・純淨黑豆眼・微弧線嘴）
// ==========================================
const hero = new THREE.Group(); scene.add(hero);
const heroBody = new THREE.Group(); hero.add(heroBody);
const heroShadow = createContactShadowMesh(1.35, 1.35, 0.75);

const bodyMesh = shadowy(new THREE.Mesh(new RoundedBoxGeometry(1.0, 0.95, 0.92, 7, 0.3), M.orange));
bodyMesh.position.y = 0.475; heroBody.add(bodyMesh);

const face = new THREE.Group(); face.position.set(0, 0.5, 0.465); heroBody.add(face);

// 兩顆純粹可愛的黑豆眼
const eyeLGroup = new THREE.Group(); eyeLGroup.position.set(-0.18, 0.08, 0);
const eyeRGroup = new THREE.Group(); eyeRGroup.position.set(0.18, 0.08, 0);
face.add(eyeLGroup, eyeRGroup);

const eyeSocketGeo = new THREE.CapsuleGeometry(0.058, 0.090, 8, 16);
const socketL = new THREE.Mesh(eyeSocketGeo, M.navy); socketL.scale.z = 0.5;
const socketR = new THREE.Mesh(eyeSocketGeo, M.navy); socketR.scale.z = 0.5;
eyeLGroup.add(socketL); eyeRGroup.add(socketR);

// 臉頰紅暈
[-0.29, 0.29].forEach((x) => {
  const c = new THREE.Mesh(new THREE.CircleGeometry(0.068, 24), M.cheek);
  c.position.set(x, -0.05, 0.006); face.add(c);
});

// 極簡微弧線嘴型
// 1. 溫柔微笑（細緻微彎）
const smileMouth = new THREE.Mesh(new THREE.TorusGeometry(0.065, 0.016, 10, 28, Math.PI), M.navy);
smileMouth.rotation.z = Math.PI; smileMouth.position.set(0, -0.10, 0.012); face.add(smileMouth);

// 2. 驚訝小圓嘴
const oMouth = new THREE.Mesh(new THREE.TorusGeometry(0.050, 0.018, 10, 28), M.navy);
oMouth.position.set(0, -0.11, 0.012); face.add(oMouth);

// 3. 委屈下垂微撇嘴（苦瓜臉）
const sadMouth = new THREE.Mesh(new THREE.TorusGeometry(0.065, 0.016, 10, 28, Math.PI), M.navy);
sadMouth.position.set(0, -0.13, 0.012); face.add(sadMouth);

// 4. 閉嘴微縫線
const straightMouth = new THREE.Mesh(new THREE.BoxGeometry(0.12, 0.022, 0.02), M.navy);
straightMouth.position.set(0, -0.10, 0.012); face.add(straightMouth);

// 視線追蹤
const gazeWorld = new THREE.Vector3();
function setGaze(targetVec3) {
  gazeWorld.copy(targetVec3);
  const localTarget = face.worldToLocal(gazeWorld.clone());
  const lookX = clamp(localTarget.x * 0.12, -0.040, 0.040);
  const lookY = clamp(localTarget.y * 0.12, -0.040, 0.040);
  socketL.position.set(lookX, lookY, 0);
  socketR.position.set(lookX, lookY, 0);
}

// ==========================================
// 第 1 幕：500億大紙箱 + 雙側開蓋 + 散落包裹 + 3D文字
// ==========================================
const s1Group = new THREE.Group(); scene.add(s1Group);
const bigBox = new THREE.Group(); s1Group.add(bigBox);
const bigBoxShadow = createContactShadowMesh(3.2, 2.4, 0.65);

const BW = 2.4, BH = 1.65, BD = 1.65;
const boxBody = shadowy(new THREE.Mesh(new RoundedBoxGeometry(BW, BH, BD, 4, 0.06), M.card));
boxBody.position.y = BH / 2; bigBox.add(boxBody);
const tapeV = shadowy(new THREE.Mesh(new THREE.BoxGeometry(0.34, 0.02, BD + 0.02), M.tape));
tapeV.position.set(0, BH + 0.005, 0); bigBox.add(tapeV);

// 大標籤：大字無遮擋
const bigLabel = new THREE.Mesh(new THREE.PlaneGeometry(1.65, 0.85), new THREE.MeshStandardMaterial({
  roughness: 0.6, transparent: true,
  map: labelTex(1000, 520, (x, w, h) => {
    rr(x, 10, 10, w - 20, h - 20, 40); x.fillStyle = "#ffffff"; x.fill();
    x.lineWidth = 10; x.strokeStyle = "#16223e"; x.stroke();
    x.fillStyle = "#16223e"; x.textAlign = "center"; x.font = '900 190px "NTC"'; x.fillText("500 億筆", w / 2, 250);
    x.font = '700 74px "NTC"'; x.fillStyle = "#c85624"; x.fillText("SHOPPING GRAPH", w / 2, 385);
  }),
}));
bigLabel.position.set(0, BH * 0.50, BD / 2 + 0.008); bigBox.add(bigLabel);

// 側蓋與後蓋翻折（絕不設正面垂落蓋片，正面視野 100% 開闊！）
const flapL = new THREE.Group(); flapL.position.set(-BW / 2, BH + 0.005, 0); bigBox.add(flapL);
const fLM = shadowy(new THREE.Mesh(new THREE.BoxGeometry(BW / 2.1, 0.025, BD - 0.04), M.card));
fLM.position.x = BW / 4.2; flapL.add(fLM);

const flapR = new THREE.Group(); flapR.position.set(BW / 2, BH + 0.005, 0); bigBox.add(flapR);
const fRM = shadowy(new THREE.Mesh(new THREE.BoxGeometry(BW / 2.1, 0.025, BD - 0.04), M.card));
fRM.position.x = -BW / 4.2; flapR.add(fRM);

const flapBack = new THREE.Group(); flapBack.position.set(0, BH + 0.005, -BD / 2); bigBox.add(flapBack);
const fBM = shadowy(new THREE.Mesh(new THREE.BoxGeometry(BW - 0.04, 0.025, BD / 2.1), M.card));
fBM.position.z = BD / 4.2; flapBack.add(fBM);

const tagTexs = ["$8,990", "$6,490", "$7,880", "$12,900", "$5,990"].map((p) => labelTex(400, 240, (x, w, h) => {
  rr(x, 6, 6, w - 12, h - 12, 30); x.fillStyle = "#fbf8f2"; x.fill();
  x.fillStyle = "#c85624"; x.font = '900 96px "NTC"'; x.textAlign = "center"; x.fillText(p, w / 2, 150);
  x.beginPath(); x.arc(44, 44, 15, 0, 7); x.fillStyle = "#c9c1b2"; x.fill();
}));

const R = rng(20261109);
const N = 72, items = [];
const slots = [];

for (let k = 0; k < N; k++) {
  const a = k * 2.39996;
  let r, y, sx, sz;
  if (k < 24) {
    r = 0.55 + Math.sqrt(k / 24) * 0.65; y = 0.10 + (k % 3) * 0.10;
  } else if (k < 52) {
    r = 0.32 + Math.sqrt((k - 24) / 28) * 0.38; y = 0.30 + ((k - 24) % 4) * 0.12;
  } else {
    r = 0.18 + Math.sqrt((k - 52) / 20) * 0.30; y = 0.65 + ((k - 52) % 3) * 0.12;
  }
  sx = -1.5 + Math.cos(a) * r * 1.25;
  sz = 0.15 + Math.sin(a) * r * 0.95;
  // 正面窗口防擋：小人正面視線內壓低高度，整張受壓臉部清清楚楚露在正前方！
  if (Math.abs(sx - (-1.5)) < 0.52 && sz > 0.15) {
    y = Math.min(y, 0.14);
  }
  slots.push({ x: sx, z: sz, y: y });
}

for (let k = 0; k < N; k++) {
  const isTag = R() < 0.22, s = 0.18 + R() * 0.20;
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
  const burstDir = new THREE.Vector3(slot.x - (-1.5), slot.y * 1.5 + 0.4, slot.z - 0.15).normalize().multiplyScalar(4.5 + R() * 2.8);
  items.push({
    mesh, isTag, s,
    launch: 3.75 + (k / N) * 1.4, flight: 0.48 + R() * 0.25, apex: 1.35 + R() * 1.1,
    from: new THREE.Vector3(1.45 + (R() - 0.5) * 1.2, 1.75, -0.35 + (R() - 0.5) * 0.8),
    to: new THREE.Vector3(slot.x, slot.y, slot.z), burstDir,
    r0: new THREE.Euler(R() * 6, R() * 6, R() * 6),
    w: new THREE.Vector3((R() - 0.5) * 16, (R() - 0.5) * 16, (R() - 0.5) * 16),
    rest: new THREE.Euler(isTag ? -Math.PI / 2 + (R() - 0.5) * 0.4 : (R() - 0.5) * 0.35, R() * 6, (R() - 0.5) * 0.35),
    vanishDelay: Math.hypot(slot.x - (-1.5), slot.z - 0.15) * 0.15,
  });
}

// 比較表卡片
const card = new THREE.Group(); s1Group.add(card);
const cardShadow = createContactShadowMesh(1.2, 0.8, 0.55);
const cardBase = shadowy(new THREE.Mesh(new RoundedBoxGeometry(0.95, 1.2, 0.04, 2, 0.02), M.paper));
const cardFace = new THREE.Mesh(new THREE.PlaneGeometry(0.93, 1.18), new THREE.MeshStandardMaterial({
  roughness: 0.7, transparent: true,
  map: labelTex(700, 880, (x, w, h) => {
    x.fillStyle = "#16223e"; x.font = '900 80px "NTC"'; x.textAlign = "left"; x.fillText("比較表", 50, 115);
    x.fillStyle = "#c85624"; x.fillRect(50, 145, 180, 12);
    const rows = [["A 款", 0.55, "#9aa6c4"], ["B 款", 0.9, "#059669"], ["C 款", 0.7, "#9aa6c4"]];
    rows.forEach(([n, v, col], i) => {
      const y = 250 + i * 180;
      x.fillStyle = "#2d3748"; x.font = '700 60px "NTC"'; x.fillText(n, 50, y + 20);
      rr(x, 220, y - 26, 400, 52, 26); x.fillStyle = "#e9e4da"; x.fill();
      rr(x, 220, y - 26, 400 * v, 52, 26); x.fillStyle = col; x.fill();
    });
    x.strokeStyle = "#059669"; x.lineWidth = 24; x.lineCap = "round"; x.beginPath();
    x.moveTo(450, 770); x.lineTo(510, 830); x.lineTo(630, 710); x.stroke();
  }),
}));
cardFace.position.z = 0.022; card.add(cardBase, cardFace);

// 3D 立體字「Gemini購物」
const fontData = await new Promise((ok, no) => new TTFLoader().load("fonts/huninn_sub.ttf", ok, undefined, no));
const font = new Font(fontData);
const letters = [];
{
  const str = "Gemini購物", size = 0.52, scale = size / fontData.resolution;
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
  letters.forEach((m) => { m.userData.x += 0.1; });
}

// ==========================================
// 第 2 幕：環繞分頁 + 磁吸收納盒（絕不穿模・左右黃金平衡）
// ==========================================
const s2Group = new THREE.Group(); scene.add(s2Group);
const tabTitles = ["momo 購物網", "PChome 24h", "蝦皮商城", "Yahoo 購物", "Mobile01 開箱", "PTT 家電板", "燦坤線上", "全國電子"];
const tabColors = ["#ec1c24", "#0076cb", "#ee4d2d", "#7b1fa2", "#059669", "#1a264a", "#f59e0b", "#c85624"];
const tabCards = [];

tabTitles.forEach((name, i) => {
  const g = new THREE.Group();
  // 正面
  const base = shadowy(new THREE.Mesh(new RoundedBoxGeometry(0.85, 0.6, 0.025, 2, 0.02), M.paper));
  const faceMesh = new THREE.Mesh(new THREE.PlaneGeometry(0.83, 0.58), new THREE.MeshStandardMaterial({
    roughness: 0.6, transparent: true,
    map: labelTex(600, 420, (x, w, h) => {
      rr(x, 6, 6, w - 12, h - 12, 28); x.fillStyle = "#ffffff"; x.fill();
      x.fillStyle = tabColors[i]; x.fillRect(6, 6, w - 12, 75);
      x.fillStyle = "#ffffff"; x.font = '700 40px "NTC"'; x.textAlign = "left"; x.fillText(name, 35, 56);
      x.fillStyle = "#e5e7eb"; x.fillRect(35, 120, 230, 28);
      x.fillStyle = "#9ca3af"; x.fillRect(35, 170, 400, 22);
      x.fillRect(35, 210, 310, 22);
      x.fillStyle = "#c85624"; x.font = '900 60px "NTC"'; x.fillText("$" + (6000 + i * 400), 35, 330);
    })
  }));
  faceMesh.position.z = 0.014;
  // 背面（雙面貼圖，絕不死白薄片！）
  const backMesh = new THREE.Mesh(new THREE.PlaneGeometry(0.83, 0.58), new THREE.MeshStandardMaterial({
    color: 0xf0ece1, roughness: 0.7
  }));
  backMesh.rotation.y = Math.PI; backMesh.position.z = -0.014;
  g.add(base, faceMesh, backMesh);
  g.visible = false;
  s2Group.add(g); tabCards.push(g);
});

// 磁吸收納盒（置於右側黃金線 x = 0.95，絕不穿模！）
const binder = new THREE.Group(); s2Group.add(binder);
const binderShadow = createContactShadowMesh(1.8, 1.0, 0.70);
const binderBody = shadowy(new THREE.Mesh(new RoundedBoxGeometry(1.3, 1.6, 0.32, 4, 0.08), M.navy));
binder.add(binderBody);

// 金屬鉻黃夾具
const binderClip = shadowy(new THREE.Mesh(new RoundedBoxGeometry(0.55, 0.14, 0.36, 2, 0.03), M.yellow));
binderClip.position.set(0, 0.78, 0); binder.add(binderClip);

// 規格初篩表標籤（翡翠綠卡片 + 白色立體邊框）
const binderLabel = new THREE.Mesh(new THREE.PlaneGeometry(1.05, 0.65), new THREE.MeshStandardMaterial({
  transparent: true, roughness: 0.5,
  map: labelTex(800, 500, (x, w, h) => {
    rr(x, 10, 10, w - 20, h - 20, 30); x.fillStyle = "#059669"; x.fill();
    x.lineWidth = 8; x.strokeStyle = "#ffffff"; x.stroke();
    x.fillStyle = "#ffffff"; x.font = '900 82px "NTC"'; x.textAlign = "center"; x.fillText("規格初篩表", w/2, 210);
    x.font = '700 44px "NTC"'; x.fillStyle = "#d1fae5"; x.fillText("AI 自動收斂多維規格", w/2, 330);
  })
}));
binderLabel.position.set(0, -0.05, 0.17); binder.add(binderLabel);
binder.visible = false;

// ==========================================
// 第 3 幕：購物車 + 會員登入大金屬牆（相隔 2 米・零穿模）
// ==========================================
const s3Group = new THREE.Group(); scene.add(s3Group);

// 小購物車
const cart = new THREE.Group(); s3Group.add(cart);
const cartShadow = createContactShadowMesh(1.2, 0.85, 0.60);
const cartBasket = shadowy(new THREE.Mesh(new RoundedBoxGeometry(0.85, 0.48, 0.62, 2, 0.04), M.orange));
cartBasket.position.y = 0.42; cart.add(cartBasket);
[-0.26, 0.26].forEach((z) => {
  [-0.32, 0.32].forEach((x) => {
    const wheel = new THREE.Mesh(new THREE.CylinderGeometry(0.08, 0.08, 0.05, 16), M.navy);
    wheel.rotation.z = Math.PI / 2; wheel.position.set(x, 0.08, z); cart.add(wheel);
  });
});
const handleBar = new THREE.Mesh(new THREE.BoxGeometry(0.04, 0.35, 0.55), M.navy);
handleBar.position.set(-0.46, 0.55, 0); cart.add(handleBar);

const cartItem = shadowy(new THREE.Mesh(new RoundedBoxGeometry(0.5, 0.4, 0.4, 2, 0.03), M.card));
cartItem.position.set(0, 0.68, 0); cart.add(cartItem);

// 會員登入大金屬牆（置於右側 x = 1.35，消光金屬深藍，非死黑！）
const gate = new THREE.Group(); s3Group.add(gate);
const gateShadow = createContactShadowMesh(4.2, 0.9, 0.75);
const gateMesh = shadowy(new THREE.Mesh(new RoundedBoxGeometry(3.6, 2.7, 0.24, 3, 0.08), M.metalGate));
gate.position.y = 1.35; gate.add(gateMesh);
const gateSign = new THREE.Mesh(new THREE.PlaneGeometry(3.2, 1.4), new THREE.MeshStandardMaterial({
  transparent: true, roughness: 0.4,
  map: labelTex(1200, 520, (x, w, h) => {
    rr(x, 15, 15, w - 30, h - 30, 36); x.fillStyle = "#151d2f"; x.fill();
    x.lineWidth = 12; x.strokeStyle = "#dc2626"; x.stroke();
    x.fillStyle = "#f59e0b"; x.font = '900 102px "NTC"'; x.textAlign = "center"; x.fillText("🔒 會員專屬登入牆", w/2, 165);
    x.fillStyle = "#ffffff"; x.font = '700 60px "NTC"'; x.fillText("登入後才顯示券後底價", w/2, 300);
    x.fillStyle = "#9ca3af"; x.font = '500 45px "NTC"'; x.fillText("AI 爬蟲無權限存取真實優惠", w/2, 400);
  })
}));
gateSign.position.z = 0.13; gate.add(gateSign);
gate.visible = false;

// 漫天折價券
const couponCards = [];
const couponTexts = ["折 $500", "滿萬折千", "會員神券", "限時 88 折", "免運券"];
for (let i = 0; i < 28; i++) {
  const cMesh = new THREE.Mesh(new THREE.PlaneGeometry(0.48, 0.28), new THREE.MeshStandardMaterial({
    side: THREE.DoubleSide, roughness: 0.6,
    map: labelTex(360, 210, (x, w, h) => {
      rr(x, 6, 6, w - 12, h - 12, 24); x.fillStyle = "#fee2e2"; x.fill();
      x.lineWidth = 6; x.strokeStyle = "#ef4444"; x.stroke();
      x.fillStyle = "#dc2626"; x.font = '900 58px "NTC"'; x.textAlign = "center"; x.fillText(couponTexts[i % 5], w/2, 125);
    })
  }));
  cMesh.position.set((R() - 0.5) * 6, 2.5 + R() * 2.5, (R() - 0.5) * 4);
  cMesh.rotation.set(R() * 6, R() * 6, R() * 6);
  s3Group.add(cMesh);
  couponCards.push({ mesh: cMesh, speed: 0.8 + R() * 0.8 });
  cMesh.visible = false;
}

// 思考問號（第3幕）
const qMark = new THREE.Group(); qMark.position.set(0.35, 1.3, 0); hero.add(qMark);
const qPlane = new THREE.Mesh(new THREE.PlaneGeometry(0.55, 0.55), new THREE.MeshBasicMaterial({
  transparent: true,
  map: labelTex(240, 240, (x, w, h) => {
    x.fillStyle = "#c85624"; x.font = '900 150px "NTC"'; x.textAlign = "center"; x.fillText("?", w/2, 170);
  })
}));
qMark.add(qPlane); qMark.visible = false;

// ==========================================
// 第 4 幕：漏斗 + 頒獎台 + 原片高飽和度彩帶
// ==========================================
const s4Group = new THREE.Group(); scene.add(s4Group);

// 3D 漏斗
const funnel = new THREE.Group(); s4Group.add(funnel);
const funnelTop = shadowy(new THREE.Mesh(new THREE.CylinderGeometry(1.4, 0.45, 1.2, 32, 1, true), M.funnel));
funnelTop.position.y = 2.4; funnel.add(funnelTop);
const funnelSpout = shadowy(new THREE.Mesh(new THREE.CylinderGeometry(0.45, 0.45, 0.6, 32), M.funnel));
funnelSpout.position.y = 1.5; funnel.add(funnelSpout);
funnel.visible = false;

const filterPills = ["台北套房", "安靜省電", "預算 8,000"].map((text, i) => {
  const p = new THREE.Group();
  const b = shadowy(new THREE.Mesh(new RoundedBoxGeometry(0.9, 0.35, 0.25, 3, 0.08), M.paper));
  const lab = new THREE.Mesh(new THREE.PlaneGeometry(0.85, 0.3), new THREE.MeshBasicMaterial({
    map: labelTex(450, 160, (x, w, h) => {
      rr(x, 6, 6, w - 12, h - 12, 24); x.fillStyle = "#1e40af"; x.fill();
      x.fillStyle = "#ffffff"; x.font = '900 54px "NTC"'; x.textAlign = "center"; x.fillText(text, w/2, 100);
    })
  }));
  lab.position.z = 0.13; p.add(b, lab);
  s4Group.add(p); p.visible = false; return p;
});

// 3 個頒獎台（原片同款溫潤暖木台座，配專屬接地軟陰影！）
const podiumShadows = [];
const podiums = [-1.35, 0.0, 1.35].map((x, i) => {
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
      rr(ctx, 12, 12, w - 24, h - 24, 40); ctx.fillStyle = i === 1 ? "#f0fdf4" : "#ffffff"; ctx.fill();
      ctx.lineWidth = i === 1 ? 16 : 8; ctx.strokeStyle = i === 1 ? "#f59e0b" : "#cbd5e1"; ctx.stroke();
      if (i === 1) {
        rr(ctx, w/2 - 140, 20, 280, 56, 28); ctx.fillStyle = "#f59e0b"; ctx.fill();
        ctx.fillStyle = "#ffffff"; ctx.font = '900 36px "NTC"'; ctx.textAlign = "center"; ctx.fillText("★ BEST CHOICE ★", w/2, 60);
      }
      ctx.fillStyle = i === 1 ? "#065f46" : "#1a264a"; ctx.font = '900 76px "NTC"'; ctx.textAlign = "center"; ctx.fillText(cTitle, w/2, i === 1 ? 175 : 150);
      ctx.fillStyle = "#c85624"; ctx.font = '900 102px "NTC"'; ctx.fillText("$" + [6490, 7880, 5990][i], w/2, i === 1 ? 335 : 300);
      ctx.fillStyle = i === 1 ? "#047857" : "#64748b"; ctx.font = '700 52px "NTC"'; ctx.fillText(cTag, w/2, i === 1 ? 500 : 460);
    })
  }));
  cFace.position.z = 0.025; card.add(cMesh, cFace);
  card.position.set(0, heights[i] + 0.46, 0);
  g.add(card);
  s4Group.add(g); g.visible = false;
  return { g, card, pShadow, h: heights[i] };
});

// 原片同款高飽和度小長方形紙花（金、紅、深藍、翡翠綠）
const confettiCount = 50;
const confettiCols = [0xf59e0b, 0xd93829, 0x16223e, 0x059669, 0xc85624];
const confettiMeshes = [];
for (let i = 0; i < confettiCount; i++) {
  const m = new THREE.Mesh(new THREE.PlaneGeometry(0.12, 0.08), new THREE.MeshStandardMaterial({
    color: confettiCols[i % confettiCols.length], side: THREE.DoubleSide, roughness: 0.5
  }));
  let cx, cz;
  while (true) {
    cx = (R() - 0.5) * 6.5; cz = (R() - 0.5) * 3.5;
    // 嚴格避開中央卡片與左側小人
    if (Math.abs(cx) < 1.1 && cz > -0.2 && cz < 0.6) continue;
    if (Math.hypot(cx - (-2.25), cz - 0.85) < 0.75) continue;
    break;
  }
  m.position.set(cx, 3.5 + R() * 2.5, cz);
  s4Group.add(m); m.visible = false;
  confettiMeshes.push({
    mesh: m, origX: cx, origZ: cz,
    vy: 0.022 + R() * 0.025,
    rx: 0.08 + R() * 0.12, ry: 0.06 + R() * 0.15, rz: 0.05 + R() * 0.1,
    swayFreq: 2.5 + R() * 2.0, swayAmp: 0.008 + R() * 0.012
  });
}

// 衝擊波環
const shockwaveGeo = new THREE.RingGeometry(0.05, 0.15, 32);
const shockwaveMat = new THREE.MeshBasicMaterial({ color: 0x9a8e80, side: THREE.DoubleSide, transparent: true, opacity: 0 });
const shockwaveMesh = new THREE.Mesh(shockwaveGeo, shockwaveMat);
shockwaveMesh.rotation.x = -Math.PI / 2; shockwaveMesh.position.y = 0.01;
scene.add(shockwaveMesh);

function triggerShockwave(t, impactT, dur, maxRad, originX, originZ) {
  const u = prog(t, impactT, dur);
  if (u <= 0 || u >= 1) { shockwaveMesh.material.opacity = 0; return; }
  shockwaveMesh.position.set(originX, 0.012, originZ);
  const rad = lerp(0.3, maxRad, eout(u));
  shockwaveMesh.scale.set(rad, rad, 1);
  shockwaveMesh.material.opacity = (1 - u) * 0.70;
}

// ==========================================
// 攝影機關鍵路徑
// ==========================================
const K = [
  // Scene 1: 0.0 ~ 16.0s
  [0.0,  [-1.5, 0.82, 2.55], [-1.5, 0.5, 0]],
  [1.0,  [-1.5, 0.82, 2.55], [-1.5, 0.5, 0]],
  [2.9,  [0.0, 2.3, 8.2],    [0.0, 0.75, 0]],
  [5.5,  [-0.7, 2.0, 6.9],   [-0.9, 0.65, 0]],
  [8.0,  [-0.8, 1.65, 6.1],  [-1.0, 0.62, 0]],
  [11.5, [-1.0, 1.35, 5.0],  [-1.0, 0.62, 0]],
  [14.0, [0.35, 2.05, 8.5],  [0.35, 0.62, 0]],
  [15.8, [0.45, 1.95, 8.2],  [0.45, 0.62, 0]],
  
  // Scene 2: 16.5 ~ 32.5s (從中間環視，小人在左，盒子在右)
  [16.8, [0.0, 2.2, 7.8],    [0.0, 0.7, 0]],
  [22.0, [0.1, 2.3, 7.6],    [0.0, 0.75, 0]],
  [27.0, [0.1, 1.95, 6.8],   [0.1, 0.75, 0]],
  [31.8, [0.1, 1.85, 6.4],   [0.1, 0.7, 0]],
  
  // Scene 3: 32.5 ~ 47.5s (平移鏡頭，跟隨推車，鐵門在右)
  [33.0, [-0.5, 1.8, 6.8],   [-0.2, 0.8, 0]],
  [36.5, [0.2, 2.2, 8.2],    [0.3, 1.1, 0]],
  [41.0, [0.0, 2.0, 7.5],    [0.1, 0.9, 0]],
  [46.5, [0.0, 1.9, 7.0],    [0.0, 0.85, 0]],
  
  // Scene 4: 47.5 ~ 62.3s (頒獎台盛典)
  [48.0, [0.0, 2.5, 8.2],    [0.0, 1.1, 0]],
  [53.0, [0.0, 2.2, 7.6],    [0.0, 0.85, 0]],
  [57.0, [-0.2, 1.85, 6.2],  [0.0, 0.8, 0]],
  [TOTAL,[-0.3, 1.75, 5.8],  [0.0, 0.78, 0]],
];
const v3 = (a) => new THREE.Vector3(...a);
function camAt(t) {
  let i = 0; while (i < K.length - 2 && t > K[i + 1][0]) i++;
  const [t0, p0, l0] = K[i], [t1, p1, l1] = K[i + 1];
  const u = eio(prog(t, t0, t1 - t0));
  const p = v3(p0).lerp(v3(p1), u), l = v3(l0).lerp(v3(l1), u);
  camera.position.copy(p); camera.lookAt(l);
}

// ==========================================
// 每一幀渲染
// ==========================================
function renderAt(t) {
  camAt(t);

  // 震波
  if (t >= 2.05 && t < 3.0) {
    triggerShockwave(t, 2.05, 0.85, 2.8, 1.45, -0.35);
  } else if (t >= 36.5 && t < 37.5) {
    triggerShockwave(t, 36.5, 0.75, 3.5, 1.35, 0.2);
  } else if (t >= 26.8 && t < 27.6) {
    triggerShockwave(t, 26.8, 0.65, 1.8, 0.95, 0.25);
  } else {
    shockwaveMesh.material.opacity = 0;
  }

  // -------------------------
  // 第 1 幕（0 ~ 16.0s）
  // -------------------------
  const s1FadeOut = prog(t, 15.6, 0.8);
  const s1Active = t < 16.5;
  s1Group.visible = s1Active;
  if (s1Active) {
    s1Group.position.y = -s1FadeOut * 4.0;

    // 大箱子
    const landT = 2.05;
    let boxY = 0, boxScaleY = 1, boxScaleXZ = 1;
    if (t < landT) {
      const u = prog(t, 1.6, 0.45); boxY = (1 - u * u) * 8.0;
    } else {
      const dt = t - landT;
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
    const curBoxX = lerp(1.45, 5.2, away);
    const curBoxZ = lerp(-0.35, -2.5, away);
    bigBox.position.set(curBoxX, boxY + away * 3.4, curBoxZ);
    const sc = lerp(1, 0.001, Math.pow(away, 1.4));
    bigBox.scale.set(sc * boxScaleXZ, sc * boxScaleY, sc * boxScaleXZ);
    bigBox.visible = t > 1.6 && sc > 0.002;

    // 接觸陰影
    bigBoxShadow.position.set(curBoxX, 0.005, curBoxZ);
    bigBoxShadow.scale.setScalar(sc * (1 + boxY * 0.2));
    bigBoxShadow.material.opacity = 0.65 * sc * Math.exp(-boxY * 0.8);
    bigBoxShadow.visible = bigBox.visible;

    // 雙側開蓋
    const openT = t - 3.65;
    if (openT > 0) {
      const openAng = clamp(openT * 4.5, 0, Math.PI * 0.88);
      const flapSpring = spring(openT, 2.5, 5.0) * 0.2;
      flapL.rotation.z = -(openAng + flapSpring);
      flapR.rotation.z = (openAng + flapSpring);
      flapBack.rotation.x = -(openAng + flapSpring);
    } else {
      flapL.rotation.z = 0; flapR.rotation.z = 0; flapBack.rotation.x = 0;
    }

    // 小包裹
    for (const it of items) {
      const u = (t - it.launch) / it.flight, m = it.mesh;
      if (u <= 0) { m.visible = false; continue; }
      m.visible = true;

      if (t < 7.6) {
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
    }

    // 比較表卡片
    const cu = prog(t, 9.0, 0.65), ce = eout(cu);
    card.visible = t > 9.0;
    card.position.lerpVectors(new THREE.Vector3(3.2, 4.2, 1.2), new THREE.Vector3(-0.55, 0.62, 0.45), ce);
    card.position.y += Math.sin(Math.PI * cu) * 0.7;
    cardShadow.position.set(card.position.x, 0.005, card.position.z);
    cardShadow.visible = card.visible;
    cardShadow.material.opacity = 0.55 * ce;

    // 3D 立體字
    letters.forEach((m) => {
      const t0 = 12.0 + m.userData.i * 0.075, s = t - t0;
      m.visible = s > 0;
      const fall = clamp(s / 0.34), y = (1 - fall * fall) * 3.2;
      const lnd = s - 0.34, lsq = lnd > 0 ? spring(lnd, 3.0, 5.5) * 0.22 : 0;
      m.position.set(m.userData.x, y, 0.75);
      m.scale.set(1 + lsq * 0.5, 1 - lsq, 1 + lsq * 0.5);
    });
  } else {
    bigBoxShadow.visible = false; cardShadow.visible = false;
  }

  // -------------------------
  // 第 2 幕（16.0 ~ 32.5s）
  // -------------------------
  const s2FadeOut = prog(t, 32.0, 0.6);
  const s2Active = t >= 16.0 && t < 32.8;
  s2Group.visible = s2Active;
  if (s2Active) {
    s2Group.position.x = -s2FadeOut * 5.0;

    const orbitT = t - 17.5;
    const collectU = prog(t, 26.5, 0.85);
    const collectE = eio(collectU);

    // 收納盒落在右側黃金線 x = 0.95，絕不穿模！
    binder.visible = t > 26.0;
    const binderIn = prog(t, 26.0, 0.55);
    const bY = lerp(4, 0.85, ebackOut(binderIn));
    binder.position.set(0.95, bY, 0.25);
    binder.rotation.y = -0.22;
    binder.scale.setScalar(lerp(0.2, 1, ebackOut(binderIn)));

    binderShadow.position.set(0.95, 0.005, 0.25);
    binderShadow.visible = binder.visible;
    binderShadow.material.opacity = 0.65 * clamp((4 - bY) / 3.15);

    // 8 個分頁繞行半徑加大至 3.0m，絕不插小人臉！
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
    });
  } else {
    binderShadow.visible = false;
  }

  // -------------------------
  // 第 3 幕（32.5 ~ 47.5s）
  // -------------------------
  const s3FadeOut = prog(t, 46.8, 0.7);
  const s3Active = t >= 32.5 && t < 47.5;
  s3Group.visible = s3Active;
  if (s3Active) {
    s3Group.position.y = -s3FadeOut * 4.5;

    const cartT = prog(t, 32.5, 3.8);
    let cartX = lerp(-2.2, -0.2, Math.min(1, cartT * 1.2)); // 停在 -0.2，絕不碰右側 1.35 的鐵門！
    if (t >= 36.5) {
      const cartBounce = spring(t - 36.5, 4.2, 6.0) * 0.12;
      cartX = -0.2 - cartBounce;
      const impT = t - 36.5;
      const inertiaY = impT < 0.35 ? Math.sin((impT / 0.35) * Math.PI) * 0.25 : 0;
      cartItem.position.set(cartBounce * 0.8, 0.68 + inertiaY, 0);
      cartItem.rotation.z = -cartBounce * 1.5;
    }
    cart.position.set(cartX, 0, 0.2);
    cartShadow.position.set(cartX, 0.005, 0.2);
    cartShadow.visible = true;

    // 鐵門落在右側 x = 1.35，與推車保持 1.55 米安全間距！
    gate.visible = t > 36.0;
    const gateDrop = prog(t, 36.1, 0.35);
    const gateBounce = t > 36.5 ? spring(t - 36.5, 4.0, 6.0) * 0.2 : 0;
    const gY = lerp(6.5, 1.35, gateDrop) + gateBounce;
    gate.position.set(1.35, gY, 0.2);
    gateShadow.position.set(1.35, 0.005, 0.2);
    gateShadow.visible = gate.visible;
    gateShadow.material.opacity = 0.75 * clamp((6.5 - gY) / 5.15);

    // 折價券雨
    const rainT = t - 39.5;
    couponCards.forEach((cp, idx) => {
      if (rainT <= 0) { cp.mesh.visible = false; return; }
      cp.mesh.visible = true;
      cp.mesh.position.y -= 0.038 * cp.speed;
      if (cp.mesh.position.y < 0.15) cp.mesh.position.y = 4.5;
      cp.mesh.rotation.x += 0.03; cp.mesh.rotation.y += 0.02;
    });

    qMark.visible = t > 38.0 && t < 46.5;
    if (qMark.visible) {
      qMark.position.set(-0.85, 1.25, 0.2);
      qMark.scale.setScalar(1 + Math.sin(t * 8) * 0.15);
      qMark.lookAt(camera.position);
    }
  } else {
    cartShadow.visible = false; gateShadow.visible = false; qMark.visible = false;
  }

  // -------------------------
  // 第 4 幕（47.5 ~ 62.3s）
  // -------------------------
  const s4Active = t >= 47.2;
  s4Group.visible = s4Active;
  if (s4Active) {
    funnel.visible = t < 53.5;
    const fIn = prog(t, 47.5, 0.6);
    const fOut = prog(t, 51.8, 0.7);
    const fy = lerp(lerp(6, 0.4, ebackOut(fIn)), 6.5, eio(fOut));
    funnel.position.set(0, fy, 0);

    filterPills.forEach((p, idx) => {
      const dropT = 49.2 + idx * 0.6;
      if (t < dropT) { p.visible = false; return; }
      p.visible = true;
      const u = prog(t, dropT, 0.65);
      const swirlAng = u * Math.PI * 4 + idx * 2.1;
      const swirlRad = (1 - u) * 0.8;
      p.position.set(Math.cos(swirlAng) * swirlRad, lerp(4.5, 1.6, u), Math.sin(swirlAng) * swirlRad);
      p.scale.setScalar(lerp(1, 0.2, u));
      if (u >= 1) p.visible = false;
    });

    podiums.forEach((pd, idx) => {
      const riseT = 52.5 + idx * 0.4;
      if (t < riseT) { pd.g.visible = false; pd.pShadow.visible = false; return; }
      pd.g.visible = true; pd.pShadow.visible = true;
      const ru = prog(t, riseT, 0.55);
      pd.g.position.y = lerp(-2.5, 0, ebackOut(ru));
      pd.card.scale.setScalar(lerp(0.1, 1, ebackOut(ru)));
      pd.pShadow.material.opacity = 0.60 * eout(ru);
    });

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
    });
  } else {
    podiumShadows.forEach((ps) => { ps.visible = false; });
  }

  // ==========================================
  // 主角極簡黏土演技（原片靈魂：頭部傾斜、視線聚焦、自然呼吸）
  // ==========================================
  {
    const breathe = 1 + Math.sin(t * 2.8) * 0.015;
    let hx = -1.5, hy = 0, hz = 0.15, ry = 0.15, rx = 0, rz = 0;
    let scaleX = 1, scaleY = 1, scaleZ = 1;
    let eyeScaleX = 1.0, eyeScaleY = 1.0;
    let mouthType = "smile", mouthScale = 1.0;
    let gazeTgt = new THREE.Vector3(0, 1.5, 8.0);
    let wink = false;

    if (t < 16.0) {
      // ---------- 第 1 幕 表演 ----------
      if (t < 1.3) {
        // 0.0 ~ 1.3s: 挺拔身形，呆萌微笑
        scaleX = scaleY = scaleZ = 1.0;
        mouthType = "smile"; gazeTgt.set(-1.5, 1.2, 5.0);
      } else if (t < 2.05) {
        // 1.3 ~ 2.05s: 抬頭看天，好奇困惑（原片同款歪頭好奇！）
        scaleX = scaleY = scaleZ = 1.0;
        rx = -0.32; rz = 0.18; // 歪頭仰望！
        gazeTgt.set(1.45, 6.5, -0.35);
        eyeScaleX = 1.35; eyeScaleY = 1.35;
        mouthType = "o"; mouthScale = 0.85;
      } else if (t < 3.7) {
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
        scaleX = lerp(1.0, 1.22, crushU);

        if (crushU < 0.35) {
          eyeScaleX = 1.35; eyeScaleY = 1.35; mouthType = "o"; mouthScale = 1.3;
        } else {
          eyeScaleX = 1.35; eyeScaleY = 0.12; // 痛苦瞇眼 (><)
          mouthType = "sad"; mouthScale = 1.25; // 苦瓜嘴角下撇
          rz = Math.sin(t * 8) * 0.08; // 微微掙扎
        }
      } else if (t < 11.5) {
        // 7.6 ~ 11.5s: 破土大爆發！直立騰空大跳開懷大笑！
        const hopT = t - 7.6;
        if (hopT < 0.75) {
          const hopU = hopT / 0.75;
          hy = Math.sin(hopU * Math.PI) * 0.95;
          scaleY = 1.25; scaleX = 0.88; scaleZ = 0.88;
          rz = Math.sin(hopU * Math.PI * 2) * 0.12;
          eyeScaleX = 1.35; eyeScaleY = 1.35;
          mouthType = "smile"; mouthScale = 1.35;
          gazeTgt.set(-1.5, 2.0, 6.0);
        } else {
          const settleT = hopT - 0.75;
          hy = 0; rz = 0;
          scaleY = 1 + spring(settleT, 3.5, 6.0) * 0.15;
          scaleX = 1 - spring(settleT, 3.5, 6.0) * 0.1;
          mouthType = "smile";
          gazeTgt.set(-0.55, 0.62, 0.45);
        }
      } else {
        gazeTgt.set(0.5, 0.5, 0.75);
        mouthType = "smile";
      }
    } else if (t < 32.5) {
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
      }
    } else if (t < 47.5) {
      // ---------- 第 3 幕 表演 ----------
      const cartT = prog(t, 32.5, 3.8);
      const cartX = lerp(-2.2, -0.2, Math.min(1, cartT * 1.2));
      if (t < 36.5) {
        // 小人推車：人永遠在推車後方 (cartX - 0.85)，推車在 -0.2，相隔鐵門 (1.35) 超過 1.5 米！
        hx = cartX - 0.85; hy = Math.abs(Math.sin(t * 8)) * 0.06;
        rx = 0.12; gazeTgt.set(cartX + 1.2, 0.5, 0.2);
        mouthType = "smile";
      } else {
        // 鐵門砸下氣流震退：小人彈坐至 x = -1.65，鐵門在 1.35，間距 3 米，絕不穿模！
        const bonkT = t - 36.5;
        const bonkDist = spring(bonkT, 3.6, 5.0) * 0.45;
        hx = -0.2 - 0.85 - 0.4 - bonkDist;
        hy = bonkT < 0.2 ? Math.sin((bonkT / 0.2) * Math.PI) * 0.25 : 0;
        rz = -0.25; // 跌坐後傾
        if (bonkT < 2.5) {
          gazeTgt.set(1.35, 1.8, 0.2); // 驚訝看著高聳大門
          eyeScaleX = 1.35; eyeScaleY = 1.35;
          mouthType = "o"; mouthScale = 1.2;
        } else {
          gazeTgt.set(hx + 0.5, 0.5 + Math.sin(t * 2) * 0.4, 0.2);
          mouthType = "straight"; mouthScale = 1.0;
          rz = -0.18; // 歪頭困惑思考
        }
      }
    } else {
      // ---------- 第 4 幕 表演 ----------
      // 站位在最左側外邊 x = -2.25, z = 0.85，完全不擋任何展台！
      hx = -2.25; hy = 0.0; hz = 0.85;
      ry = 0.55; // 側身 32 度引薦中間推薦卡
      if (t < 52.0) {
        gazeTgt.set(0, 2.5, 0); mouthType = "o"; mouthScale = 0.7;
      } else if (t < 56.5) {
        gazeTgt.set(0.0, 1.5, 0.0); // 專注仰望中間冠軍卡片！
        rx = -0.08; rz = -0.12; // 側身歪頭崇拜仰望
        mouthType = "smile"; mouthScale = 1.2;
      } else {
        gazeTgt.set(-0.2, 1.4, 5.5); // 轉向鏡頭互動
        rx = 0; rz = 0.10;
        wink = t > 57.8 && t < 59.2;
        mouthType = "smile"; mouthScale = 1.35;
        scaleY = 1.06 + Math.sin(t * 3.2) * 0.03;
        scaleX = 0.95;
      }
    }

    hero.position.set(hx, hy, hz);
    hero.rotation.set(rx, ry, rz);
    heroBody.scale.set(breathe * scaleX, breathe * scaleY, breathe * scaleZ);

    // 接觸陰影跟隨小人平移與跳躍
    heroShadow.position.set(hx, 0.005, hz);
    const shadowSc = (1 + hy * 0.25) * scaleX;
    heroShadow.scale.set(shadowSc, shadowSc, 1);
    heroShadow.material.opacity = 0.75 * Math.exp(-hy * 1.5);

    setGaze(gazeTgt);

    // 眨眼與瞇眼
    if (wink) {
      socketL.scale.set(eyeScaleX, 0.12, 0.5);
      socketR.scale.set(eyeScaleX, eyeScaleY, 0.5);
    } else {
      const isBlink = Math.sin(t * 4.2) > 0.97;
      const curEyeY = isBlink ? 0.15 : eyeScaleY;
      socketL.scale.set(eyeScaleX, curEyeY, 0.5);
      socketR.scale.set(eyeScaleX, curEyeY, 0.5);
    }

    // 嘴型切換
    smileMouth.visible = mouthType === "smile";
    oMouth.visible = mouthType === "o";
    sadMouth.visible = mouthType === "sad";
    straightMouth.visible = mouthType === "straight";

    if (smileMouth.visible) smileMouth.scale.setScalar(mouthScale);
    if (oMouth.visible) oMouth.scale.setScalar(mouthScale);
    if (sadMouth.visible) sadMouth.scale.setScalar(mouthScale);
    if (straightMouth.visible) straightMouth.scale.setScalar(mouthScale);
  }

  renderer.render(scene, camera);

  // UI
  const chap = document.getElementById("chapter");
  if (t < 16.0) {
    chap.innerHTML = '<span class="num">1</span> 破題：五百億筆商品';
  } else if (t < 32.5) {
    chap.innerHTML = '<span class="num">2</span> 痛點：十個分頁 vs 磁吸收合';
  } else if (t < 47.5) {
    chap.innerHTML = '<span class="num">3</span> 盲區：登入牆與折價券黑箱';
  } else {
    chap.innerHTML = '<span class="num">4</span> 定位：規格初篩特助';
  }

  const sub = document.getElementById("sub");
  const cue = C.find((c) => t >= c.start - 0.05 && t <= c.end + 0.25);
  sub.style.opacity = cue ? 1 : 0;
  if (cue && sub.textContent !== cue.text) sub.textContent = cue.text;
}

window.__total = TOTAL;
window.__seekTo = (t) => renderAt(Math.max(0, Math.min(TOTAL - 1e-3, t)));
renderAt(0);
window.__ready = true;
</script>
</body>
</html>
"""

html_p.write_text(rebuilt_code, encoding="utf-8")
print("SUCCESS: Full Rebuilt scene.html written!")

from pathlib import Path

html_p = Path(r"c:\antigravity\影片\逆向研究\claude3d_工法\scene.html")
code = html_p.read_text(encoding="utf-8")

# 1. 調整五官垂直佈局：拉開眉毛、眼睛、嘴巴的縱向間距，絕不重疊！
old_face_coords = """// 兩顆大黑豆眼（支援瞪大、瞇眼、眨眼、視線追蹤）
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
straightMouth.position.set(0, -0.08, 0.015); face.add(straightMouth);"""

new_face_coords = """// 五官佈局升級：拉開層次，眉眼嘴比例完美協調，絕不穿插！
// 眉毛：y = 0.26
const browGeo = new RoundedBoxGeometry(0.20, 0.055, 0.035, 2, 0.015);
const browL = new THREE.Mesh(browGeo, M.navy); browL.position.set(-0.18, 0.26, 0.015);
const browR = new THREE.Mesh(browGeo, M.navy); browR.position.set(0.18, 0.26, 0.015);
face.add(browL, browR);

// 眼睛：y = 0.10
const eyeLGroup = new THREE.Group(); eyeLGroup.position.set(-0.18, 0.10, 0);
const eyeRGroup = new THREE.Group(); eyeRGroup.position.set(0.18, 0.10, 0);
face.add(eyeLGroup, eyeRGroup);

const eyeSocketGeo = new THREE.CapsuleGeometry(0.058, 0.085, 8, 16);
const socketL = new THREE.Mesh(eyeSocketGeo, M.navy); socketL.scale.z = 0.5;
const socketR = new THREE.Mesh(eyeSocketGeo, M.navy); socketR.scale.z = 0.5;
eyeLGroup.add(socketL); eyeRGroup.add(socketR);

// 臉頰紅暈：y = -0.04
[-0.30, 0.30].forEach((x) => {
  const c = new THREE.Mesh(new THREE.CircleGeometry(0.068, 24), M.cheek);
  c.position.set(x, -0.04, 0.006); face.add(c);
});

// 嘴型集合：基準 y = -0.16，與眼睛 (y=0.10) 保持 0.26m 完美間距！
// 1. 燦爛微笑嘴（U 型上揚弧線）
const smileMouth = new THREE.Mesh(new THREE.TorusGeometry(0.075, 0.022, 12, 32, Math.PI), M.navy);
smileMouth.rotation.z = Math.PI; smileMouth.position.set(0, -0.16, 0.015); face.add(smileMouth);

// 2. 驚恐大張 O 嘴（圓形開口）
const oMouth = new THREE.Mesh(new THREE.TorusGeometry(0.065, 0.026, 12, 32), M.navy);
oMouth.position.set(0, -0.16, 0.015); face.add(oMouth);

// 3. 委屈下垂撇嘴（倒 U 型苦瓜臉）
const sadMouth = new THREE.Mesh(new THREE.TorusGeometry(0.075, 0.022, 12, 32, Math.PI), M.navy);
sadMouth.position.set(0, -0.19, 0.015); face.add(sadMouth);

// 4. 咬牙緊繃一字嘴
const straightMouth = new THREE.Mesh(new RoundedBoxGeometry(0.18, 0.040, 0.03, 2, 0.01), M.navy);
straightMouth.position.set(0, -0.16, 0.015); face.add(straightMouth);"""

assert old_face_coords in code, "old_face_coords not found!"
code = code.replace(old_face_coords, new_face_coords)

# 2. 修正蚊香眼位置
code = code.replace("dizzyEyes.position.set(0, 0.07, 0.015);", "dizzyEyes.position.set(0, 0.10, 0.015);")

# 3. 修正紙箱山的堆疊分佈：確保小橘塊正臉在箱山中「清晰露出呼救」！
old_mountain_slots = """for (let k = 0; k < N; k++) {
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
}"""

new_mountain_slots = """for (let k = 0; k < N; k++) {
  // 戲劇包裹山演算法：
  // 箱子集中在小橘塊的後方、左右兩側與頭頂後上方，正面留出視窗露出受壓痛苦正臉！
  const a = k * 2.39996;
  let r, y, sx, sz;
  if (k < 28) {
    // 外圍裙樓 (r = 0.55 ~ 1.15m)
    r = 0.55 + Math.sqrt(k / 28) * 0.60;
    y = 0.10 + (k % 3) * 0.11;
  } else if (k < 62) {
    // 兩側與後方主堆體 (r = 0.30 ~ 0.65m)
    r = 0.32 + Math.sqrt((k - 28) / 34) * 0.35;
    y = 0.32 + ((k - 28) % 4) * 0.14;
  } else {
    // 頂部斜壓層 (堆在後腦勺與頭頂兩側，y = 0.75 ~ 1.10)
    r = 0.20 + Math.sqrt((k - 62) / 22) * 0.28;
    y = 0.72 + ((k - 62) % 3) * 0.13;
  }
  sx = -1.5 + Math.cos(a) * r * 1.25;
  sz = 0.15 + Math.sin(a) * r * 0.95;
  // 視角窗口約束：如果箱子落在正臉正前方視線中 (x 接近 -1.5 且 z > 0.35 且 y > 0.2)，往兩側推開！
  if (Math.abs(sx - (-1.5)) < 0.45 && sz > 0.25 && y > 0.25) {
    sx += (sx >= -1.5 ? 0.42 : -0.42);
  }
  slots.push({ x: sx, z: sz, y: y });
}"""

assert old_mountain_slots in code, "old_mountain_slots not found!"
code = code.replace(old_mountain_slots, new_mountain_slots)

# 4. 調整眉毛基礎高度
code = code.replace("let browY = 0.20", "let browY = 0.26")
code = code.replace("browY = 0.20; browRotL = 0.05;", "browY = 0.26; browRotL = 0.05;")
code = code.replace("browY = 0.25; browRotL = 0.45;", "browY = 0.31; browRotL = 0.48;")
code = code.replace("browY = 0.26; browRotL = 0.55;", "browY = 0.32; browRotL = 0.55;")
code = code.replace("browY = 0.22; browRotL = 0.35;", "browY = 0.28; browRotL = 0.35;")
code = code.replace("browY = 0.25; browRotL = 0.6;", "browY = 0.32; browRotL = 0.6;")
code = code.replace("browY = 0.14; browRotL = 0.70;", "browY = 0.19; browRotL = 0.65;")
code = code.replace("browY = 0.24; browRotL = -0.2;", "browY = 0.28; browRotL = -0.2;")
code = code.replace("browY = 0.20; browRotL = 0;", "browY = 0.26; browRotL = 0;")
code = code.replace("browY = 0.22;", "browY = 0.27;")

html_p.write_text(code, encoding="utf-8")
print("SUCCESS: Adjusted facial hierarchy and box mountain staging window!")

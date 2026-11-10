import sys
from pathlib import Path

p = Path(r"c:\antigravity\影片\逆向研究\claude3d_工法\scene.html")
text = p.read_text(encoding="utf-8")

old_m = """const M = {
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
};"""

new_m = """const M = {
  orange:       new THREE.MeshStandardMaterial({ color: 0xc65322, roughness: 0.82, metalness: 0.0 }),  // 啞光熟成焦糖黏土
  navy:         new THREE.MeshStandardMaterial({ color: 0x152038, roughness: 0.75, metalness: 0.02 }), // 啞光深海軍藍
  navyText:     new THREE.MeshStandardMaterial({ color: 0x16223c, roughness: 0.65, metalness: 0.02 }),
  card:         new THREE.MeshStandardMaterial({ color: 0xb8884c, roughness: 0.88, metalness: 0.0 }),  // 啞光厚牛皮紙板
  paper:        new THREE.MeshStandardMaterial({ color: 0xfcfaf5, roughness: 0.85, metalness: 0.0 }),  // 啞光象牙純棉紙卡
  metalGate:    new THREE.MeshStandardMaterial({ color: 0x182236, roughness: 0.55, metalness: 0.35 }), // 厚重啞光深鐵門
  yellow:       new THREE.MeshStandardMaterial({ color: 0xf29b05, roughness: 0.70, metalness: 0.0 }),  // 暖鉻黃黏土
  red:          new THREE.MeshStandardMaterial({ color: 0xd73525, roughness: 0.75, metalness: 0.0 }),  // 啞光赤紅
  green:        new THREE.MeshStandardMaterial({ color: 0x048a60, roughness: 0.75, metalness: 0.0 }),  // 啞光深翡翠綠
  cheek:        new THREE.MeshBasicMaterial({ color: 0xf28b72, transparent: true, opacity: 0.60 }),
  tape:         new THREE.MeshStandardMaterial({ color: 0xf4efe5, roughness: 0.80, transparent: true, opacity: 0.88 }),
  funnel:       new THREE.MeshStandardMaterial({ color: 0xf29b05, roughness: 0.70, metalness: 0.05 }),
  podiumNavy:   new THREE.MeshStandardMaterial({ color: 0x18243c, roughness: 0.82, metalness: 0.0 }), // 深海軍藍台座
  podiumGold:   new THREE.MeshStandardMaterial({ color: 0xd98a28, roughness: 0.75, metalness: 0.04 }), // 尊貴暖金台座 (冠軍)
  podiumClay:   new THREE.MeshStandardMaterial({ color: 0x8a7260, roughness: 0.85, metalness: 0.0 }), // 溫潤大地灰褐台座
};"""

if old_m in text:
    text = text.replace(old_m, new_m)
    print("M object updated with matte clay and 3 podium materials!")
else:
    print("old_m not matched, searching...")

p.write_text(text, encoding="utf-8")

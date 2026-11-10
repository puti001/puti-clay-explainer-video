import sys
from pathlib import Path

p = Path(r"c:\antigravity\影片\逆向研究\claude3d_工法\scene.html")
text = p.read_text(encoding="utf-8")

# 1. 替換 3D 字體位置：居中對齊 (0.15, y, 0.45)
old_letters_x = """    x += adv + (i === 5 ? 0.14 : 0.015);
    s1Group.add(m); letters.push(m);
  });
  letters.forEach((m) => { m.userData.x += 0.1; });"""

new_letters_x = """    x += adv + (i === 5 ? 0.14 : 0.015);
    s1Group.add(m); letters.push(m);
  });
  // 總寬度約 3.0，中心化偏移：起始 x 設在 -0.45，購物字 (i=6,7) 落在 x ≈ 1.8，整行落在 [-0.45, 2.3]
  letters.forEach((m) => { m.userData.x -= 0.45; });"""

if old_letters_x in text:
    text = text.replace(old_letters_x, new_letters_x)
    print("1. Letters shifted left by 0.55m so '購物' is fully inside frame.")

# 2. 為每個 3D 字母加上原片同款專屬接地接觸陰影 (Contact AO)！
old_letters_shadow_build = """// 3D 立體字「Gemini購物」"""
new_letters_shadow_build = """// 3D 立體字專屬接地接觸陰影
const letterShadows = [];"""

if old_letters_shadow_build in text and "letterShadows" not in text:
    text = text.replace(old_letters_shadow_build, new_letters_shadow_build + "\n" + old_letters_shadow_build)
    print("2.1 letterShadows array declared.")

old_letter_push = """    s1Group.add(m); letters.push(m);"""
new_letter_push = """    const lShadow = createContactShadowMesh(0.55, 0.45, 0.70);
    lShadow.position.set(x, 0.005, 0.75);
    lShadow.visible = false;
    s1Group.add(m); letters.push(m); letterShadows.push(lShadow);"""

if old_letter_push in text:
    text = text.replace(old_letter_push, new_letter_push)
    print("2.2 Letter contact shadows created.")

old_letters_anim_loop = """    // 3D 立體字（精確接地補償 -minY，底部與地面 0.005 齊平，絕不陷地！）
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

new_letters_anim_loop = """    // 3D 立體字（精確接地補償 -minY，底部與地面 0.005 齊平，絕不陷地！帶有扎實接觸陰影！）
    letters.forEach((m, idx) => {
      const t0 = 12.0 + m.userData.i * 0.075, s = t - t0;
      m.visible = s > 0;
      const fall = clamp(s / 0.34);
      const baseY = -m.userData.minY + 0.005;
      const dropY = (1 - fall * fall) * 3.2;
      const lnd = s - 0.34, lsq = lnd > 0 ? spring(lnd, 3.0, 5.5) * 0.22 : 0;
      m.position.set(m.userData.x, baseY + dropY, 0.75);
      m.scale.set(1 + lsq * 0.5, 1 - lsq, 1 + lsq * 0.5);

      if (letterShadows[idx]) {
        letterShadows[idx].visible = m.visible;
        letterShadows[idx].position.set(m.userData.x + 0.15, 0.005, 0.75);
        letterShadows[idx].material.opacity = 0.70 * (1 - Math.min(1, dropY / 1.5));
      }
    });"""

if old_letters_anim_loop in text:
    text = text.replace(old_letters_anim_loop, new_letters_anim_loop)
    print("2.3 Letters animation with shadows updated.")

# 3. 調整 14.0s ~ 15.8s 鏡頭：拉廣且中心微調，保證左小人、比較表、整行 Gemini 購物完美入鏡！
old_cam_s1_end = """  [14.0, [0.35, 2.05, 8.5],  [0.35, 0.62, 0]],
  [15.8, [0.45, 1.95, 8.2],  [0.45, 0.62, 0]],"""

new_cam_s1_end = """  [14.0, [0.30, 2.35, 9.2],  [0.30, 0.55, 0]],
  [15.8, [0.35, 2.25, 9.0],  [0.35, 0.55, 0]],"""

if old_cam_s1_end in text:
    text = text.replace(old_cam_s1_end, new_cam_s1_end)
    print("3. Camera K for S1 end widened and elevated.")

p.write_text(text, encoding="utf-8")
print("Letters framing & shadow patched successfully!")

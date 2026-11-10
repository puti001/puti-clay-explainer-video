import sys
from pathlib import Path

p = Path(r"c:\antigravity\影片\逆向研究\claude3d_工法\scene.html")
text = p.read_text(encoding="utf-8")

old_coupon_calc = """      // 保持在小橘塊外部安全半徑
      const distToHero = Math.hypot(cp.mesh.position.x - hx, cp.mesh.position.z - hz);
      if (distToHero < 0.85) {
        cp.mesh.position.x += (cp.mesh.position.x >= hx ? 0.6 : -0.6);
      }"""

new_coupon_calc = """      // 保持在小橘塊外部安全半徑（第3幕小橘塊在 x = -1.5, z = 0.2）
      const heroX3 = -1.5, heroZ3 = 0.2;
      const distToHero = Math.hypot(cp.mesh.position.x - heroX3, cp.mesh.position.z - heroZ3);
      if (distToHero < 0.95) {
        cp.mesh.position.x += (cp.mesh.position.x >= heroX3 ? 0.7 : -0.7);
      }"""

if old_coupon_calc in text:
    text = text.replace(old_coupon_calc, new_coupon_calc)
    print("Fixed heroX3 variable in couponCards!")
else:
    print("old_coupon_calc not found!")

p.write_text(text, encoding="utf-8")

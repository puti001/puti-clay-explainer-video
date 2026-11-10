import sys
from pathlib import Path

p = Path(r"c:\antigravity\影片\逆向研究\claude3d_工法\scene.html")
text = p.read_text(encoding="utf-8")

old_draw = """      rr(ctx, 12, 12, w - 24, h - 24, 40); ctx.fillStyle = i === 1 ? "#f0fdf4" : "#ffffff"; ctx.fill();
      ctx.lineWidth = i === 1 ? 16 : 8; ctx.strokeStyle = i === 1 ? "#f59e0b" : "#cbd5e1"; ctx.stroke();
      if (i === 1) {
        rr(ctx, w/2 - 140, 20, 280, 56, 28); ctx.fillStyle = "#f59e0b"; ctx.fill();
        ctx.fillStyle = "#ffffff"; ctx.font = '900 36px "NTC"'; ctx.textAlign = "center"; ctx.fillText("★ BEST CHOICE ★", w/2, 60);
      }
      ctx.fillStyle = i === 1 ? "#065f46" : "#1a264a"; ctx.font = '900 76px "NTC"'; ctx.textAlign = "center"; ctx.fillText(cTitle, w/2, i === 1 ? 175 : 150);
      ctx.fillStyle = "#c85624"; ctx.font = '900 102px "NTC"'; ctx.fillText("$" + [6490, 7880, 5990][i], w/2, i === 1 ? 335 : 300);
      ctx.fillStyle = i === 1 ? "#047857" : "#64748b"; ctx.font = '700 52px "NTC"'; ctx.fillText(cTag, w/2, i === 1 ? 500 : 460);"""

new_draw = """      rr(ctx, 12, 12, w - 24, h - 24, 40); ctx.fillStyle = i === 1 ? "#ffffff" : "#ffffff"; ctx.fill();
      ctx.lineWidth = i === 1 ? 20 : 12; ctx.strokeStyle = i === 1 ? "#c85624" : "#152038"; ctx.stroke();
      if (i === 1) {
        rr(ctx, w/2 - 150, 24, 300, 60, 30); ctx.fillStyle = "#c85624"; ctx.fill();
        ctx.fillStyle = "#ffffff"; ctx.font = '900 36px "NTC"'; ctx.textAlign = "center"; ctx.fillText("★ BEST CHOICE ★", w/2, 66);
      }
      ctx.fillStyle = "#152038"; ctx.font = '900 78px "NTC"'; ctx.textAlign = "center"; ctx.fillText(cTitle, w/2, i === 1 ? 180 : 155);
      ctx.fillStyle = "#d73525"; ctx.font = '900 110px "NTC"'; ctx.fillText("$" + [6490, 7880, 5990][i], w/2, i === 1 ? 345 : 310);
      ctx.fillStyle = "#374151"; ctx.font = '700 52px "NTC"'; ctx.fillText(cTag, w/2, i === 1 ? 515 : 475);"""

if old_draw in text:
    text = text.replace(old_draw, new_draw)
    print("Podium card text contrast and border upgraded!")
else:
    print("old_draw not found!")

p.write_text(text, encoding="utf-8")

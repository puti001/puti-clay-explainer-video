from pathlib import Path

html_p = Path(r"c:\antigravity\影片\逆向研究\claude3d_工法\scene.html")
code = html_p.read_text(encoding="utf-8")

# 1. 調整第一幕小人受壓與跳躍動態
old_burst_hop = """      } else if (t < 7.6) {
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
          browY = 0.32; browRotL = 0.6; browRotR = -0.6;
          mouthType = "o"; mouthScale = 1.4;
        } else {
          // 被箱子壓扁淹沒中：兩眼緊閉成一字痛苦瞇眼！眉毛緊皺！
          eyeScaleX = 1.3; eyeScaleY = 0.10; // 瞇瞇眼！
          browY = 0.19; browRotL = 0.65; browRotR = -0.65; // 眉頭深鎖
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
          browY = 0.28; browRotL = -0.2; browRotR = 0.2;
          mouthType = "smile"; mouthScale = 1.4; // 燦爛大笑！
          gazeTgt.set(-0.55, 0.62, 5.0);
        } else {"""

new_burst_hop = """      } else if (t < 7.6) {
        // 3.7 ~ 7.6s: 漫天大大小小紙箱如瀑布般砸向小橘塊堆成大山！
        const dtSwarm = t - 3.7;
        gazeTgt.set(-1.5 + Math.sin(t * 15) * 0.8, 1.8, 0.5);
        hx += Math.sin(t * 28) * 0.02; // 驚恐顫抖

        // 隨箱子堆疊，小橘塊原地被壓扁成 Q 彈果凍（hy 保持 0，臉部完好露在箱山正中央！）
        const crushU = clamp(dtSwarm / 2.2);
        hy = 0.0;
        scaleY = lerp(1.0, 0.72, crushU); // 壓扁至 0.72
        scaleX = lerp(1.0, 1.25, crushU); // 橫向外擴
        scaleZ = lerp(1.0, 1.20, crushU);

        if (crushU < 0.35) {
          eyeScaleX = 1.4; eyeScaleY = 1.4;
          browY = 0.32; browRotL = 0.6; browRotR = -0.6;
          mouthType = "o"; mouthScale = 1.35;
        } else {
          // 被大堆箱子壓住：痛苦瞇瞇眼 (><)、深鎖倒八字眉、嘴角下垂苦瓜臉！
          eyeScaleX = 1.35; eyeScaleY = 0.12; // 痛苦瞇眼
          browY = 0.22; browRotL = 0.68; browRotR = -0.68; // 眉毛鎖緊
          mouthType = "sad"; mouthScale = 1.2; // 嘴角徹底下撇哀號
        }
      } else if (t < 11.5) {
        // 7.6 ~ 11.5s: 破土大爆發！直立衝天彈跳（直立面向鏡頭，大眼大笑歡呼！）
        const hopT = t - 7.6;
        if (hopT < 0.75) {
          const hopU = hopT / 0.75;
          hy = Math.sin(hopU * Math.PI) * 1.35; // 騰空跳躍
          scaleY = 1.28; scaleX = 0.88; scaleZ = 0.88; // 彈性拉長
          rz = Math.sin(hopU * Math.PI * 2) * 0.12; // 興奮左右微擺，絕不倒立！
          eyeScaleX = 1.35; eyeScaleY = 1.35; // 雙眼圓睜發亮
          browY = 0.30; browRotL = -0.25; browRotR = 0.25; // 揚眉開朗
          mouthType = "smile"; mouthScale = 1.35; // 超大燦爛笑嘴！
          gazeTgt.set(-1.5, 2.0, 6.0); // 直視觀眾鏡頭
        } else {"""

assert old_burst_hop in code, "old_burst_hop not found!"
code = code.replace(old_burst_hop, new_burst_hop)

# 2. 正前方箱子壓低高度，絕不擋臉
code = code.replace(
    "if (Math.abs(sx - (-1.5)) < 0.45 && sz > 0.25 && y > 0.25) {\n    sx += (sx >= -1.5 ? 0.42 : -0.42);\n  }",
    "if (Math.abs(sx - (-1.5)) < 0.55 && sz > 0.15) {\n    y = Math.min(y, 0.18);\n  }"
)

html_p.write_text(code, encoding="utf-8")
print("SUCCESS: Refined burried facial window and upright leap cheering!")

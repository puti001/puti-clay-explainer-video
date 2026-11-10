from pathlib import Path

html_p = Path(r"c:\antigravity\影片\逆向研究\claude3d_工法\scene.html")
code = html_p.read_text(encoding="utf-8")

# 1. 壓低小人身前箱子的高度
target1 = """  // 視角窗口約束：如果箱子落在正臉正前方視線中 (x 接近 -1.5 且 z > 0.35 且 y > 0.2)，往兩側推開！
  if (Math.abs(sx - (-1.5)) < 0.45 && sz > 0.25 && y > 0.25) {
    sx += (sx >= -1.5 ? 0.42 : -0.42);
  }"""
rep1 = """  // 視角窗口約束：小人正前方胸前不堆高，保證痛苦受壓臉部 100% 露出來！
  if (Math.abs(sx - (-1.5)) < 0.55 && sz > 0.15) {
    y = Math.min(y, 0.15);
  }"""

if target1 in code:
    code = code.replace(target1, rep1)
    print("Replaced target1 successfully!")
else:
    print("Warning: target1 not found directly, checking normalized...")
    code = code.replace(target1.replace("\r\n", "\n"), rep1)

# 2. 修正小人被箱子淹沒時的 hy 與跳躍時直立衝天（取消翻滾倒立）
target2 = """      } else if (t < 7.6) {
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
          browY = 0.19; browRotL = 0.65; browRotR = -0.70; // 眉頭深鎖
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

rep2 = """      } else if (t < 7.6) {
        // 3.7 ~ 7.6s: 漫天大大小小紙箱如瀑布般砸向小橘塊堆成大山！
        const dtSwarm = t - 3.7;
        gazeTgt.set(-1.5 + Math.sin(t * 15) * 0.8, 1.8, 0.5);
        hx += Math.sin(t * 28) * 0.02;

        // 小橘塊原地被壓扁成 Q 彈果凍（hy 保持 0，五官清晰露在正面！）
        const crushU = clamp(dtSwarm / 2.2);
        hy = 0.0;
        scaleY = lerp(1.0, 0.74, crushU); // 壓扁至 0.74
        scaleX = lerp(1.0, 1.22, crushU);
        scaleZ = lerp(1.0, 1.18, crushU);

        if (crushU < 0.35) {
          eyeScaleX = 1.4; eyeScaleY = 1.4;
          browY = 0.32; browRotL = 0.6; browRotR = -0.6;
          mouthType = "o"; mouthScale = 1.35;
        } else {
          // 被箱山壓迫：痛苦瞇瞇眼 (><)、深鎖倒八字眉、嘴角下垂苦瓜臉！
          eyeScaleX = 1.35; eyeScaleY = 0.12;
          browY = 0.22; browRotL = 0.68; browRotR = -0.68;
          mouthType = "sad"; mouthScale = 1.25;
        }
      } else if (t < 11.5) {
        // 7.6 ~ 11.5s: 破土大爆發！直立衝天彈跳（直立面向鏡頭，大眼大笑歡呼！）
        const hopT = t - 7.6;
        if (hopT < 0.75) {
          const hopU = hopT / 0.75;
          hy = Math.sin(hopU * Math.PI) * 1.35; // 騰空跳躍
          scaleY = 1.28; scaleX = 0.88; scaleZ = 0.88;
          rz = Math.sin(hopU * Math.PI * 2) * 0.12; // 興奮左右微擺，絕不倒立！
          eyeScaleX = 1.35; eyeScaleY = 1.35; // 雙眼圓睜發亮
          browY = 0.30; browRotL = -0.25; browRotR = 0.25;
          mouthType = "smile"; mouthScale = 1.35; // 超大燦爛笑嘴！
          gazeTgt.set(-1.5, 2.0, 6.0); // 直視觀眾鏡頭
        } else {"""

if target2 in code:
    code = code.replace(target2, rep2)
    print("Replaced target2 successfully!")
else:
    print("Warning: target2 not found directly, checking normalized...")
    code = code.replace(target2.replace("\r\n", "\n"), rep2)

html_p.write_text(code, encoding="utf-8")
print("SUCCESS: Fixes saved to scene.html!")

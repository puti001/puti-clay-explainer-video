# Puti-AI | 3D 極簡黏土定格動畫解說影片生成引擎
> **對標 Jerry_AI Claude 3D 小黃人定格動畫工法・純代碼 Three.js 程式化場景・Playwright 1080p 逐幀無損渲染管線**

本專案完整復刻並工程化落地了爆款 3D 黏土小人知識點解說動畫管線。告別傳統 AI 影片生成模型（如 Runway/Luma/Sora/H3）的「時間膨脹特徵漂移、角色突變、文字穿幫」痛點，採用**100% 程式化決定論架構**，讓每一幀畫面都精準對齊旁白時間碼與物理演技。

---

## 🌟 核心工程亮點

1. **原汁原味 3D 啞光黏土風格 (Matte Clay Shader)**
   - 採用低粗糙度 `MeshStandardMaterial` 結合微噪點凹凸貼圖（Procedural Noise Bump Map）。
   - 攝影棚雙向柔光設定（主光、側補光、邊緣光、環境環境遮擋 AO）。
   - 主角專屬地面接觸軟陰影（Contact AO），跳躍時動態縮小淡化，落地時重壓形變。

2. **時間決定論求值架構 (`__seekTo(timeSec)`)**
   - 畫面狀態是時間 $t$ 的**純函數**，完全杜絕幀相依（Frame-dependent）狀態累積。
   - 支援離線跳幀、倒播、任意倍速渲染，渲染過程無人值守零崩潰。

3. **靈動演技控制器 (Acting & Physics System)**
   - **視線追蹤 (Gaze Tracking)**：頭部與眼球隨時間動態聚焦當前說話字卡，內建視線保護限制（防止翻白眼）。
   - **誇張擠壓拉伸 (Squash & Stretch)**：跳躍起飛拉長、著地受壓扁平，完全符合皮克斯動畫 12 原則。
   - **恐慌／慶祝／驚疑三態表演**：含眨眼、歪頭、雙手舉起、旋轉飛躍等情緒動態。

4. **雙層無鋸齒立體卡片架構**
   - 象牙白厚實倒角底板（`RoundedBoxGeometry`）＋ 獨立前置平面字卡貼圖（前置 0.003）。
   - 徹底解決倒角處 UV 拉伸產生黑線鋸齒的產業痛點。

5. **Playwright 1080p 60/30fps 逐格無損壓製**
   - 內建非同步管線調用本機 Headless Chrome 逐幀截圖，直接管線輸入 FFmpeg。
   - 實測每秒渲染 21~25 fps，60 秒全片僅需約 80 秒即產出 1080p 廣播級 MP4。

---

## 📁 目錄結構

```text
├── index.html                   # 核心 Three.js 3D 舞台、黏土材質與時間函數
├── update_scene.py              # 場景編修與幾何參數即時更新器
├── apply_final_acting.py        # 角色演技、動態物理與視線追蹤控制器
├── synth_sfx.py                 # 程式化環境音效與點對點動態音效合成
├── tts.py                       # 旁白語音生成與時間碼對齊
├── 3D黏土動畫實戰踩坑與最佳實踐.md  # 逆向工程踩坑全記錄與解決方案
├── audio/                       # 旁白音軌、音效與 BGM
├── fonts/                       # 開源思源黑體與日系圓體字型
└── Gemini購物_完整4幕3D知識點影片_1080p.mp4  # 完整成品展示
```

---

## 🚀 快速上手

### 1. 安裝環境需求
```bash
pip install playwright soundfile numpy edge-tts
playwright install chromium
```

### 2. 本地預覽 3D 舞台
啟動本地伺服器並在瀏覽器查看：
```bash
python -m http.server 8000
# 瀏覽器打開 http://localhost:8000
```

### 3. 逐幀離線渲染 1080p 影片
```bash
python test_render.py
```

---

## 📚 實戰踩坑手冊
完整踩坑手冊請詳閱 [3D黏土動畫實戰踩坑與最佳實踐.md](3D黏土動畫實戰踩坑與最佳實踐.md)，涵蓋：
- RoundedBox 倒角黑邊徹底解法
- 接觸陰影 (Contact AO) 換幕洩漏排錯
- Three.js 旋轉正負號與時間軸求值對齊
- FFmpeg `amix` 多軌衰減與末端爆音解決方案

---

## 📜 版權與授權
屏東縣後庄國小黃朝榮老師作品，免費分享，歡迎擴散推廣，嚴禁商用與任何侵權、不尊重著作權的行為。
更多 Puti-AI 教學工具請前往：[https://padlet.com/clongwh/puti_ai_tools](https://padlet.com/clongwh/puti_ai_tools)

# Puti-AI | 3D 黏土定格動畫解說影片生成引擎 (3D Clay Explainer Video)

> **對標 Jerry_AI Claude 3D 極簡小橘人解說片工法 ╳ 純代碼 Three.js 程式化動效 ╳ Playwright 1080p 逐幀無損渲染管線**

本專案是一套專為製作高品質 **3D 黏土定格風格知識點解說短片** 的開源程式碼引擎。徹底擺脫黑盒 AI 影片生成模型（如 Runway / Luma / Sora / MiniMax H3）的「文字亂碼、角色五官崩壞、物件幻覺變形、秒數配額限制」痛點，採用 **100% 程式碼確定性渲染技術**，確保每一格畫面皆由嚴謹的 3D 著色器與物理參數控制。

---

## 🌟 核心技術與特色亮點

1. **啞光黏土微噪點材質 (Matte Clay Shader)**
   - 使用低粗糙度 `MeshStandardMaterial` 結合程序化微噪點凹凸（Procedural Noise Bump Map）。
   - 燈光配置仿定格動畫微距攝影棚：雙側冷暖補光 + 柔和接觸陰影（Contact AO），落地時壓扁回彈帶有真實重量感。

2. **時間純函數跳轉機制 (`__seekTo(timeSec)`)**
   - 畫面狀態是時間 $t$ 的 *純函數*，不存在依賴播放幀率的累積誤差。
   - 支援任意秒數瞬移、倒帶、非線性調度，精準對齊旁白每一句語音波形與音效重擊點。

3. **物理演技系統 (Acting & Physics System)**
   - **視線追蹤 (Gaze Tracking)**：頭部與眼球自然朝向空中懸浮的知識卡片與視角焦點。
   - **擠壓與拉伸 (Squash & Stretch)**：起跳拉伸、著地衝擊壓扁，還原傳統定格迪士尼 12 原則。
   - **階梯式定格步進**：支援 12fps 定格動畫階梯采樣，呈現逼真的黏土定格頓挫感。

4. **100% 程序化安全音效與配樂 (Procedural Audio & BGM)**
   - 內建純數學正弦泛音合成器 (`synth_sfx.py`)，自動產生水晶叮、木質咚、金牌揭曉鏘、卡通彈跳蹦。
   - 所有音效時間軸與音量由 [`sfx.json`](sfx.json) 完全資料驅動，消滅程式碼魔法數字。
   - 內建溫潤的 **卡林巴琴 (Kalimba) C 大調五度進行背景音樂**，零版權風險、免外部依賴。

5. **自動字幕與雙比例響應式輸出**
   - 支援從 `cues.json` 一鍵匯出符合工業標準的 `subtitles.srt` 與 `subtitles.vtt`。
   - 支援 16:9 橫式（1920x1080）與 9:16 直式（1080x1920）動態攝影機視角與 UI 自動重排。

6. **Playwright 1080p 逐幀管道離線渲染**
   - 透過 Playwright 啟動 Headless Chrome 逐格繪製 Canvas，直通管道餵給 FFmpeg 進行 H.264 編碼。
   - 預設 30fps 廣播級渲染（可選 `--fps 60`），60 秒全片約 75 秒即可無損壓制出 1080p 高清 MP4。

---

## 📂 專案目錄結構

```text
puti-clay-explainer-video/
├── build.py                  # 統一參數化主構建管線 (--check, --style, --audio, --subtitles, --render)
├── compile_style.py          # 將 style.yaml 編譯為 scene.html 讀取的 style.js
├── render_video.py           # Playwright 逐幀管道流渲染腳本
├── synth_sfx.py              # 100% 程序化數學音效與 Kalimba BGM 合成器
├── mix_audio.py              # 讀取 sfx.json 與 cues.json 進行 EBU R128 (-14 LUFS) 多軌混音
├── tts.py                    # 旁白語音生成與時間軸校正
├── export_subtitles.py       # 自動產生 SRT / VTT 字幕檔
├── scene.html                # 核心 Three.js 3D 黏土定格動畫互動舞台 (支援 16:9 / 9:16)
├── index.html                # 進入點與導覽頁
├── cues.json                 # 旁白時間軸分鏡與文案資料
├── sfx.json                  # 音效對位與音量資料契約
├── style.yaml                # 黏土風格視覺規格契約 (Single Source of Truth)
├── style.js                  # 編譯後的風格設定 (供 scene.html 載入)
├── requirements.txt          # Python 依賴清單
├── package.json              # Playwright / Three.js 依賴定義
├── audio/                    # 自動合成的旁白、音效與 BGM
├── fonts/                    # 開源可商用字型 (jf-openhuninn, NotoSansTC)
└── archive/                  # 歷史修補腳本與除錯截圖歸檔
```

---

## 🚀 快速上手

### 1. 安裝環境依賴

```bash
# 1. 安裝 Python 依賴
pip install -r requirements.txt

# 2. 安裝 Playwright 瀏覽器核心
playwright install chromium
```

> **注意**：系統須已安裝 `ffmpeg` 與 `ffprobe` 並加入 PATH。

### 2. 環境健康檢查

```bash
python build.py --check
```

### 3. 一鍵完整構建與渲染

```bash
# 執行完整管線：編譯風格 -> 合成音訊 -> 匯出字幕 -> Playwright 離線渲染 1080p MP4
python build.py --all

# 或分步執行：
python build.py --style      # 編譯 style.yaml -> style.js
python build.py --audio      # 由 sfx.json 與 cues.json 合成音效與 BGM 混音
python build.py --subtitles  # 產生 subtitles.srt 與 subtitles.vtt
python build.py --render     # 渲染橫式 16:9 (1920x1080, 預設 30fps)
python build.py --render --aspect 9:16  # 渲染直式 9:16 (1080x1920)
```

### 4. 本地即時預覽 3D 場景

直接在瀏覽器打開 `scene.html` 或啟動本地靜態伺服器：

```bash
python -m http.server 8000
```
瀏覽器訪問：
- 橫式：`http://localhost:8000/scene.html`
- 直式：`http://localhost:8000/scene.html?aspect=9:16`

- 拖曳滑鼠：360 度環視 3D 黏土角色與場景。
- 空白鍵：播放 / 暫停。
- 鍵盤左右方向鍵：逐秒快轉或倒退。

---

## 🎨 視覺規格契約 (`style.yaml`)

本專案將黏土材質的所有核心物理與視覺參數固化於 `style.yaml`，作為全專案的單一真相來源：
- **小橘人主色**：`#c65322`（啞光熟成焦糖黏土，陰影修邊 `#963810`）
- **地面與背景**：`#eae5db`（原片同款溫潤象牙米灰）
- **材質粗糙度 (Roughness)**：角色 `0.82`、地面 `0.95`
- **相機視角 (FOV)**：16:9 電影長焦為 `28`；9:16 直式適配為 `56`
- **雙色溫棚拍燈光**：暖金主光（1.85 / `#fff5e4`）+ 冷藍天光（0.85 / `#9db8eb`）
- **標準字型**：標題使用粉圓體 (`huninn.ttf`)、內文使用思源黑體 (`NotoSansTC-VF.ttf`)。
- **標準字型**：標題使用粉圓體 (`huninn.ttf`)、內文使用思源黑體 (`NotoSansTC-VF.ttf`)。

---

## 📜 版權與宣告

屏東縣後庄國小黃朝榮老師作品，免費分享，歡迎擴散推廣，嚴禁商用與任何侵權、不尊重著作權的行為。
更多教學工具請參考：[Puti-AI 教學工具庫](https://padlet.com/clongwh/puti_ai_tools)

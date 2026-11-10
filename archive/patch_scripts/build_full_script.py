import asyncio
import json
import subprocess
from pathlib import Path
import edge_tts

BASE = Path(r"c:\antigravity\影片\逆向研究\claude3d_工法")
AUDIO_DIR = BASE / "audio"
AUDIO_DIR.mkdir(parents=True, exist_ok=True)

# 完整 4 幕劇本設計（緊湊、有力、每句皆有強烈視覺對應）
SCRIPT = [
    # Scene 1: 破題（500 億筆資訊過載）- 0 ~ 16.5s
    {"id": "vo_00", "text": "你丟給 AI 五百億筆商品，"},
    {"id": "vo_01", "text": "它不會變聰明，只會把你淹沒。"},
    {"id": "vo_02", "text": "聰明人要的，是一張剛剛好的比較表。"},
    {"id": "vo_03", "text": "這才是 Gemini 購物，真正好用的地方。"},
    # Scene 2: 痛點（開 10 個分頁 vs 磁吸收合）- 16.5s ~ 28s
    {"id": "vo_04", "text": "過去想買台套房除濕機，你得猜關鍵字、爬開箱文，"},
    {"id": "vo_05", "text": "開十幾個分頁，在各家電商之間眼花撩亂。"},
    {"id": "vo_06", "text": "Gemini 真正改變的，是把混亂的視窗一鍵收合成規格表。"},
    # Scene 3: 盲區（台灣電商登入牆與折價券）- 28s ~ 41s
    {"id": "vo_07", "text": "但搬到台灣電商，它會立刻撞上兩道大牆："},
    {"id": "vo_08", "text": "會員專屬的登入牆，以及滿天飛的隱藏折價券。"},
    {"id": "vo_09", "text": "AI 抓得到公開標價，卻穿不透登入後的真實底價。"},
    # Scene 4: 結論（規格初篩特助）- 41s ~ 54s
    {"id": "vo_10", "text": "所以，別把它當成一鍵搶便宜的神器，"},
    {"id": "vo_11", "text": "把它當成幫你精準過濾規格的選品特助。"},
    {"id": "vo_12", "text": "懂這層邊界，你才算真正用懂了 AI 購物。"},
]

VOICE = "zh-TW-HsiaoChenNeural"

async def gen_all():
    cues = []
    current_time = 0.5 # 0.5s pre-roll

    for i, item in enumerate(SCRIPT):
        fn = f"{item['id']}.mp3"
        fp = AUDIO_DIR / fn
        comm = edge_tts.Communicate(item["text"], VOICE, rate="+6%")
        await comm.save(str(fp))
        
        # probe duration
        res = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", str(fp)],
            capture_output=True, text=True
        )
        dur = float(res.stdout.strip())
        
        start = round(current_time, 3)
        end = round(start + dur, 3)
        cues.append({
            "i": i,
            "id": item["id"],
            "text": item["text"],
            "start": start,
            "end": end,
            "dur": dur,
            "file": fn
        })
        # Add pause between sentences
        # If transitioning between major scenes, add slightly longer pause (0.6s), else 0.35s
        gap = 0.6 if i in [3, 6, 9] else 0.35
        current_time = end + gap

    total = round(current_time + 1.2, 3)
    out_data = {
        "total": total,
        "cues": cues
    }
    with open(BASE / "cues.json", "w", encoding="utf-8") as f:
        json.dump(out_data, f, ensure_ascii=False, indent=2)
    
    print(f"Generated {len(cues)} voiceover tracks. Total duration: {total}s")

if __name__ == "__main__":
    asyncio.run(gen_all())

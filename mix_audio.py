import json
import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
AUDIO_DIR = BASE_DIR / "audio"
CUES_PATH = BASE_DIR / "cues.json"
SFX_PATH = BASE_DIR / "sfx.json"
BGM_PATH = AUDIO_DIR / "bgm_kalimba.wav"
OUTPUT_PATH = AUDIO_DIR / "master_norm.mp3"

def mix():
    if not CUES_PATH.exists():
        print(f"Error: {CUES_PATH} not found.", file=sys.stderr)
        sys.exit(1)
        
    with open(CUES_PATH, "r", encoding="utf-8") as f:
        cues_data = json.load(f)

    cues = cues_data["cues"]
    total_dur = cues_data["total"]

    sfx_list = []
    if SFX_PATH.exists():
        with open(SFX_PATH, "r", encoding="utf-8") as f:
            sfx_list = json.load(f)

    # 1. 嚴格驗證 sfx.json 合法性
    for idx, item in enumerate(sfx_list):
        item_id = item.get("id", f"sfx_{idx}")
        filename = item.get("file")
        if not filename:
            raise ValueError(f"[sfx.json 錯誤] 缺少 'file' 欄位: 項目 {item_id}")
            
        sfx_file = AUDIO_DIR / filename
        if not sfx_file.exists():
            raise FileNotFoundError(f"[sfx.json 錯誤] 音效檔案不存在: {sfx_file} (項目: {item_id})")
            
        t = item.get("time", -1)
        if not (0.0 <= t <= total_dur):
            raise ValueError(f"[sfx.json 錯誤] 音效時間點 {t}s 超出影片總長度 {total_dur}s (項目: {item_id})")

    # 2. 建立輸入列表
    # 旁白軌道 (0..len(cues)-1)
    inputs = [AUDIO_DIR / f"{c['id']}.mp3" for c in cues]
    
    # SFX 軌道
    sfx_start_idx = len(inputs)
    for item in sfx_list:
        inputs.append(AUDIO_DIR / item["file"])
        
    # BGM 軌道 (最後一個輸入)
    bgm_idx = len(inputs)
    inputs.append(BGM_PATH)

    filter_complex = []

    # 旁白延遲與對齊 (adelay)
    vo_outputs = []
    for i, c in enumerate(cues):
        ms = int(round(c["start"] * 1000))
        out_lbl = f"v{i}"
        filter_complex.append(f"[{i}:a]adelay={ms}|{ms},volume=1.35[{out_lbl}];")
        vo_outputs.append(f"[{out_lbl}]")

    # 音效延遲與音量 (由 sfx.json 資料驅動)
    sfx_outputs = []
    for idx, item in enumerate(sfx_list):
        in_idx = sfx_start_idx + idx
        ms = int(round(item["time"] * 1000))
        vol = item.get("vol", 1.0)
        out_lbl = f"sfx_{idx}"
        filter_complex.append(f"[{in_idx}:a]adelay={ms}|{ms},volume={vol:.2f}[{out_lbl}];")
        sfx_outputs.append(f"[{out_lbl}]")

    # BGM 淡入淡出與音量平衡
    filter_complex.append(
        f"[{bgm_idx}:a]volume=0.22,afade=t=in:st=0:d=1.5,afade=t=out:st={total_dur-2.5:.2f}:d=2.5[bgm];"
    )

    # 總混音：依據實戰規範加入 normalize=0:dropout_transition=0 防止動態抽吸與各軌衰減
    all_tracks = vo_outputs + sfx_outputs + ["[bgm]"]
    total_tracks_count = len(all_tracks)
    inputs_concat = "".join(all_tracks)
    filter_complex.append(
        f"{inputs_concat}amix=inputs={total_tracks_count}:normalize=0:dropout_transition=0[mixed];"
    )
    # 廣播級 EBU R128 (-14 LUFS) 響度正規化
    filter_complex.append("[mixed]loudnorm=I=-14:TP=-1.5:LRA=11[out]")

    cmd = ["ffmpeg", "-y"]
    for inp in inputs:
        cmd.extend(["-i", str(inp)])

    cmd.extend([
        "-filter_complex", "".join(filter_complex),
        "-map", "[out]",
        "-c:a", "libmp3lame",
        "-b:a", "192k",
        "-t", str(total_dur + 0.5),
        str(OUTPUT_PATH)
    ])

    print(f"Mixing {len(cues)} VO tracks, {len(sfx_list)} validated SFX tracks, and 1 BGM track (normalize=0)...")
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if res.returncode == 0:
        print(f"Master Audio successfully generated: {OUTPUT_PATH}")
    else:
        print("FFmpeg error:", res.stderr.decode('utf-8', errors='ignore'), file=sys.stderr)
        sys.exit(res.returncode)

if __name__ == "__main__":
    mix()

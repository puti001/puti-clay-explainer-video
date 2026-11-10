import json
import subprocess
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
AUDIO_DIR = BASE_DIR / "audio"
CUES_PATH = BASE_DIR / "cues.json"
BGM_PATH = AUDIO_DIR / "bgm_kalimba.wav"
OUTPUT_PATH = AUDIO_DIR / "master_norm.mp3"

with open(CUES_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

cues = data["cues"]
total_dur = data["total"]

# 1. 旁白軌道 (0..12)
inputs = [AUDIO_DIR / f"{c['id']}.mp3" for c in cues]

# 2. 程序化 SFX (13..16)
inputs += [
    AUDIO_DIR / "sfx_boing.wav",   # 13: 卡通彈跳
    AUDIO_DIR / "sfx_ding.wav",    # 14: 水晶叮
    AUDIO_DIR / "sfx_dong.wav",    # 15: 溫潤咚
    AUDIO_DIR / "sfx_chiang.wav",  # 16: 璀璨金牌鏘
    BGM_PATH                       # 17: 程序化 Kalimba BGM
]

filter_complex = []

# 旁白延遲與對齊
for i, c in enumerate(cues):
    ms = int(c["start"] * 1000)
    filter_complex.append(f"[{i}:a]adelay={ms}|{ms},volume=1.35[v{i}];")

# 音效精準對位
# 彈跳 boing (2.4s, 14.5s)
filter_complex.append("[13:a]asplit=2[boing1][boing2];")
filter_complex.append("[boing1]adelay=2400|2400,volume=1.2[s_boing1];")
filter_complex.append("[boing2]adelay=14500|14500,volume=1.2[s_boing2];")

# 叮 ding (8.5s, 31.8s)
filter_complex.append("[14:a]asplit=2[ding1][ding2];")
filter_complex.append("[ding1]adelay=8500|8500,volume=1.1[s_ding1];")
filter_complex.append("[ding2]adelay=31800|31800,volume=1.1[s_ding2];")

# 咚 dong (10.2s, 34.0s)
filter_complex.append("[15:a]asplit=2[dong1][dong2];")
filter_complex.append("[dong1]adelay=10200|10200,volume=1.0[s_dong1];")
filter_complex.append("[dong2]adelay=34000|34000,volume=1.0[s_dong2];")

# 鏘 chiang (50.5s - 第一名卡片高潮揭曉)
filter_complex.append("[16:a]adelay=50500|50500,volume=1.3[s_chiang];")

# BGM 側鏈避讓 (Ducking) 與淡入淡出
filter_complex.append(f"[17:a]volume=0.22,afade=t=in:st=0:d=1.5,afade=t=out:st={total_dur-2.5}:d=2.5[bgm];")

# 總混音 (13 軌旁白 + 7 處音效 + 1 軌 BGM)
mix_inputs = "".join([f"[v{i}]" for i in range(len(cues))]) + "[s_boing1][s_boing2][s_ding1][s_ding2][s_dong1][s_dong2][s_chiang][bgm]"
total_tracks = len(cues) + 7 + 1
filter_complex.append(f"{mix_inputs}amix=inputs={total_tracks}:duration=longest:dropout_transition=2[mixed];")
# 響度正規化 (EBU R128 -14 LUFS)
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

print("Running pure local mix...")
res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
if res.returncode == 0:
    print(f"Master Audio successfully generated: {OUTPUT_PATH}")
else:
    print("FFmpeg error:", res.stderr.decode('utf-8', errors='ignore'))

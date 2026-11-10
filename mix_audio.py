import json
import subprocess
from pathlib import Path

BASE = Path(r"c:\antigravity\影片\逆向研究\claude3d_工法")
AUDIO_DIR = BASE / "audio"
SFX_DIR = Path(r"C:\antigravity\影片\shanshiba-workflow-colab\sfx")
BGM_PATH = Path(r"C:\antigravity\影片\minimax_task\bgm.mp3")

with open(BASE / "cues.json", "r", encoding="utf-8") as f:
    data = json.load(f)

cues = data["cues"]
total_dur = data["total"]

# Voiceovers: 0..12
inputs = [AUDIO_DIR / f"{c['id']}.mp3" for c in cues]

# Real SFX + Synthesized Musical Foley (叮、咚、鏘、蹦)
inputs += [
    SFX_DIR / "球" / "thud_body_hit_276600.mp3",          # 13: 箱子落地重擊
    SFX_DIR / "球" / "ball_rubber_bounce_423778.mp3",     # 14: 箱子彈跳二次撞擊
    SFX_DIR / "膠帶" / "tape_rip_467721.mp3",             # 15: 膠帶撕開
    SFX_DIR / "砝碼" / "coins_change_table_243517.mp3",    # 16: 小包裹散落滾動聲
    AUDIO_DIR / "sfx_boing.wav",                           # 17: 卡通彈跳蹦
    SFX_DIR / "翻頁" / "page_flip_683706.mp3",             # 18: 卡片飛入滑音
    AUDIO_DIR / "sfx_ding.wav",                            # 19: 水晶「叮」
    AUDIO_DIR / "sfx_dong.wav",                            # 20: 溫潤「咚」
    AUDIO_DIR / "sfx_chiang.wav",                          # 21: 金牌揭曉璀璨「鏘」
    SFX_DIR / "門" / "door_close_classroom_204178.mp3",    # 22: 防護巨門轟然落地
    SFX_DIR / "紙" / "paper_folding_398896.mp3",           # 23: 折價券沙沙飄落
    SFX_DIR / "歡呼" / "clap_kids_short_529455.mp3",       # 24: 兒童短促喝采
    BGM_PATH,                                              # 25: 輕快背景配樂
]

filter_complex = []

# 13 軌旁白
for i, c in enumerate(cues):
    ms = int(c["start"] * 1000)
    filter_complex.append(f"[{i}:a]adelay={ms}|{ms},volume=1.35[v{i}];")

# SFX 精密對位
# 第 1 幕：大箱落地連環彈跳 + 膠帶撕開 + 包裹散落滾動 + 小橘人彈出 + 叮咚
filter_complex.append("[13:a]adelay=2050|2050,volume=1.3[s_box_hit1];")     # 第一次重擊
filter_complex.append("[14:a]asplit=2[b1][b2];")
filter_complex.append("[b1]adelay=2450|2450,volume=0.9[s_box_hit2];")       # 第二次彈跳撞擊
filter_complex.append("[15:a]adelay=3650|3650,volume=1.1[s_tape_rip];")      # 膠帶撕開
filter_complex.append("[16:a]adelay=4200|4200,volume=0.85[s_boxes_roll];")  # 小包裹滾動散落
filter_complex.append("[17:a]asplit=2[boing1][boing2];")
filter_complex.append("[boing1]adelay=7600|7600,volume=1.0[s_pop_boing];")   # 主角破土彈出蹦！
filter_complex.append("[18:a]adelay=9000|9000,volume=0.9[s_card_in];")      # 比較表飛入
filter_complex.append("[19:a]asplit=3[ding1][ding2][ding3];")
filter_complex.append("[ding1]adelay=9350|9350,volume=0.85[s_card_ding];")   # 比較表定格清脆「叮！」
filter_complex.append("[20:a]asplit=4[dong1][dong2][dong3][dong4];")
filter_complex.append("[dong1]adelay=12300|12300,volume=0.75[s_txt1];")     # 3D 文字落下「咚」
filter_complex.append("[dong2]adelay=12600|12600,volume=0.75[s_txt2];")

# 第 2 幕：分頁撲克牌切牌收合 + 磁吸收納扣合
filter_complex.append("[18:a]adelay=26800|26800,volume=1.0[s_tabs_shuffle];") # 分頁洗牌
filter_complex.append("[ding2]adelay=27300|27300,volume=1.1[s_binder_ding];") # 收納盒扣合「叮！」

# 第 3 幕：鐵門狂砸落地 + 主角後仰撞跌 + 折價券飄落 + 疑惑問號
filter_complex.append("[22:a]adelay=36500|36500,volume=1.4[s_gate_slam];")    # 鐵門落地重響
filter_complex.append("[b2]adelay=36900|36900,volume=1.0[s_hero_fall];")      # 主角跌坐地面
filter_complex.append("[boing2]adelay=38200|38200,volume=0.85[s_q_boing];")   # 頭頂冒出問號蹦
filter_complex.append("[23:a]adelay=39500|39500,volume=0.75[s_coupon_fall];")

# 第 4 幕：頒獎台升起 + 金牌首選揭曉璀璨「鏘！」+ 歡呼 + 眨眼叮
filter_complex.append("[dong3]adelay=52800|52800,volume=0.9[s_podium1];")
filter_complex.append("[dong4]adelay=53400|53400,volume=0.9[s_podium2];")
filter_complex.append("[21:a]adelay=54000|54000,volume=1.3[s_winner_chiang];") # 首選推薦金牌「鏘！」
filter_complex.append("[24:a]adelay=54500|54500,volume=0.85[s_kids_clap];")    # 歡呼喝采
filter_complex.append("[ding3]adelay=58600|58600,volume=0.9[s_wink_ding];")     # 帥氣眨眼「叮！」

# BGM
filter_complex.append(f"[25:a]aloop=loop=-1:size=2e+09,volume=0.12,afade=t=in:st=0:d=1.5,afade=t=out:st={total_dur-2.0}:d=2.0,atrim=0:{total_dur}[bgm];")

all_labels = [f"[v{i}]" for i in range(len(cues))]
all_labels += [
    "[s_box_hit1]", "[s_box_hit2]", "[s_tape_rip]", "[s_boxes_roll]", "[s_pop_boing]",
    "[s_card_in]", "[s_card_ding]", "[s_txt1]", "[s_txt2]",
    "[s_tabs_shuffle]", "[s_binder_ding]",
    "[s_gate_slam]", "[s_hero_fall]", "[s_q_boing]", "[s_coupon_fall]",
    "[s_podium1]", "[s_podium2]", "[s_winner_chiang]", "[s_kids_clap]", "[s_wink_ding]",
    "[bgm]"
]

n_inputs = len(all_labels)
filter_complex.append(
    f"{''.join(all_labels)}amix=inputs={n_inputs}:duration=longest:normalize=0[mix_raw];"
    f"[mix_raw]loudnorm=I=-14:TP=-1.5:LRA=11[outa]"
)

cmd = ["ffmpeg", "-y"]
for inp in inputs:
    cmd.extend(["-i", str(inp)])

cmd.extend([
    "-filter_complex", "".join(filter_complex),
    "-map", "[outa]",
    "-t", str(total_dur),
    str(AUDIO_DIR / "master_norm.mp3")
])

print("Mixing rich Foley & Musical Audio track with FFmpeg...")
res = subprocess.run(cmd, capture_output=True)
if res.returncode != 0:
    print("FFmpeg error:", res.stderr.decode("utf-8", errors="ignore"))
else:
    print("Success: audio/master_norm.mp3 generated with rich Foley actors (叮、咚、鏘、蹦)!")

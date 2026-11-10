"""旁白 → cues.json（每句起訖秒數），場景與混音都吃這份時間軸。"""
import asyncio, json, pathlib, subprocess
import edge_tts

ROOT = pathlib.Path(__file__).parent
VOICE, RATE = "zh-TW-HsiaoChenNeural", "+6%"
LINES = [
    "你丟給 AI 五百億筆商品，",
    "它不會變聰明，只會把你淹沒。",
    "聰明人要的，是一張剛剛好的比較表。",
    "這才是 Gemini 購物，真正好用的地方。",
]
START, GAP, TAIL = 0.5, 0.35, 0.9


def dur(p):
    return float(subprocess.check_output(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "csv=p=0", str(p)], text=True).strip())


async def main():
    out = ROOT / "audio"
    out.mkdir(exist_ok=True)
    cues, t = [], START
    for i, line in enumerate(LINES):
        f = out / f"vo_{i:02d}.mp3"
        if not f.exists():
            await edge_tts.Communicate(line, VOICE, rate=RATE).save(str(f))
        d = dur(f)
        cues.append({"i": i, "text": line.rstrip("，。"), "start": round(t, 3),
                     "end": round(t + d, 3), "file": f.name})
        t += d + GAP
    total = round(cues[-1]["end"] + TAIL, 3)
    (ROOT / "cues.json").write_text(json.dumps({"total": total, "cues": cues},
                                               ensure_ascii=False, indent=2), "utf-8")
    print(json.dumps({"total": total, "cues": cues}, ensure_ascii=False, indent=2))


asyncio.run(main())

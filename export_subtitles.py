import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
CUES_FILE = BASE_DIR / "cues.json"

def format_timestamp_srt(seconds: float) -> str:
    millis = int(round(seconds * 1000))
    hours = millis // 3600000
    millis %= 3600000
    minutes = millis // 60000
    millis %= 60000
    secs = millis // 1000
    millis %= 1000
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"

def format_timestamp_vtt(seconds: float) -> str:
    millis = int(round(seconds * 1000))
    hours = millis // 3600000
    millis %= 3600000
    minutes = millis // 60000
    millis %= 60000
    secs = millis // 1000
    millis %= 1000
    return f"{hours:02d}:{minutes:02d}:{secs:02d}.{millis:03d}"

def generate_subtitles():
    with open(CUES_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    cues = data.get("cues", [])
    
    # SRT Output
    srt_lines = []
    for idx, cue in enumerate(cues, start=1):
        start_ts = format_timestamp_srt(cue["start"])
        end_ts = format_timestamp_srt(cue["end"])
        text = cue["text"].strip()
        srt_lines.append(f"{idx}\n{start_ts} --> {end_ts}\n{text}\n")
    
    srt_path = BASE_DIR / "subtitles.srt"
    srt_path.write_text("\n".join(srt_lines), encoding="utf-8")
    print(f"Generated SRT: {srt_path}")

    # VTT Output
    vtt_lines = ["WEBVTT\n"]
    for idx, cue in enumerate(cues, start=1):
        start_ts = format_timestamp_vtt(cue["start"])
        end_ts = format_timestamp_vtt(cue["end"])
        text = cue["text"].strip()
        vtt_lines.append(f"{idx}\n{start_ts} --> {end_ts}\n{text}\n")
        
    vtt_path = BASE_DIR / "subtitles.vtt"
    vtt_path.write_text("\n".join(vtt_lines), encoding="utf-8")
    print(f"Generated VTT: {vtt_path}")

if __name__ == "__main__":
    generate_subtitles()

import http.server
import json
import socketserver
import subprocess
import sys
import threading
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

BASE_DIR = Path(r"c:\antigravity\影片\逆向研究\claude3d_工法")
PORT = 8785
OUTPUT_MP4 = BASE_DIR / "Gemini購物_完整4幕3D知識點影片_1080p.mp4"
AUDIO_MASTER = BASE_DIR / "audio" / "master_norm.mp3"

with open(BASE_DIR / "cues.json", "r", encoding="utf-8") as f:
    cues_data = json.load(f)

TOTAL_DURATION = cues_data["total"]
FPS = 30
TOTAL_FRAMES = int(TOTAL_DURATION * FPS)

print(f"1080p Full HD Render | Total: {TOTAL_DURATION}s, FPS: {FPS}, Frames: {TOTAL_FRAMES}", flush=True)

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(BASE_DIR), **kwargs)

    def log_message(self, format, *args):
        pass

socketserver.TCPServer.allow_reuse_address = True
server = socketserver.TCPServer(("127.0.0.1", PORT), Handler)
threading.Thread(target=server.serve_forever, daemon=True).start()

ffmpeg_cmd = [
    "ffmpeg", "-y",
    "-f", "image2pipe",
    "-vcodec", "mjpeg",
    "-r", str(FPS),
    "-s", "1920x1080",
    "-i", "-",
    "-i", str(AUDIO_MASTER),
    "-c:v", "libx264",
    "-pix_fmt", "yuv420p",
    "-preset", "veryfast",
    "-crf", "17",
    "-c:a", "aac",
    "-b:a", "192k",
    "-shortest",
    str(OUTPUT_MP4)
]

ffmpeg_proc = subprocess.Popen(
    ffmpeg_cmd,
    stdin=subprocess.PIPE,
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL
)

t0 = time.time()
with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=True,
        args=[
            "--use-gl=angle",
            "--use-angle=gl",
            "--enable-webgl",
            "--ignore-gpu-blocklist"
        ]
    )
    page = browser.new_page(viewport={"width": 1920, "height": 1080})
    page.goto(f"http://127.0.0.1:{PORT}/scene.html?render=1")
    page.wait_for_function("() => window.__ready === true", timeout=15000)
    print("Page ready! Starting 1080p full render...", flush=True)

    for i in range(TOTAL_FRAMES):
        t = i / FPS
        page.evaluate(f"window.__seekTo({t:.5f})")
        img_bytes = page.screenshot(type="jpeg", quality=98)
        ffmpeg_proc.stdin.write(img_bytes)

        if (i + 1) % 100 == 0 or i == TOTAL_FRAMES - 1:
            elapsed = time.time() - t0
            speed = (i + 1) / elapsed if elapsed > 0 else 0
            eta = (TOTAL_FRAMES - i - 1) / speed if speed > 0 else 0
            print(f"Rendered [{i+1:4d}/{TOTAL_FRAMES}] ({((i+1)/TOTAL_FRAMES)*100:.1f}%) | {speed:.1f} fps | ETA: {eta:.1f}s", flush=True)

    browser.close()

ffmpeg_proc.stdin.close()
ffmpeg_proc.wait()
server.shutdown()

elapsed = time.time() - t0
print(f"1080p Render finished in {elapsed:.1f}s! Saved to: {OUTPUT_MP4}", flush=True)

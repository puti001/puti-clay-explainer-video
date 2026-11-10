import argparse
import http.server
import json
import socketserver
import subprocess
import sys
import threading
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

BASE_DIR = Path(__file__).resolve().parent
AUDIO_MASTER = BASE_DIR / "audio" / "master_norm.mp3"
CUES_FILE = BASE_DIR / "cues.json"

def get_free_port():
    import socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('127.0.0.1', 0))
        return s.getsockname()[1]

def render(aspect="16:9", fps=30, output_name=None):
    if not CUES_FILE.exists():
        print(f"Error: {CUES_FILE} not found. Please run tts.py first.", file=sys.stderr)
        sys.exit(1)

    with open(CUES_FILE, "r", encoding="utf-8") as f:
        cues_data = json.load(f)

    total_duration = cues_data.get("total", 62.0)
    total_frames = int(total_duration * fps)

    if aspect == "9:16":
        width, height = 1080, 1920
        default_out = "output_vertical_1080x1920.mp4"
    else:
        width, height = 1920, 1080
        default_out = "output_horizontal_1920x1080.mp4"

    output_path = BASE_DIR / (output_name or default_out)
    port = get_free_port()

    print(f"=== Starting 3D Clay Stop-Motion Offline Render ===")
    print(f"Resolution : {width}x{height} ({aspect})")
    print(f"FPS        : {fps}")
    print(f"Total Time : {total_duration}s ({total_frames} frames)")
    print(f"Output     : {output_path}")

    # Local Web Server
    class Handler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=str(BASE_DIR), **kwargs)

        def log_message(self, format, *args):
            pass

    socketserver.TCPServer.allow_reuse_address = True
    server = socketserver.TCPServer(("127.0.0.1", port), Handler)
    server_thread = threading.Thread(target=server.serve_forever, daemon=True)
    server_thread.start()

    # Build FFmpeg command
    ffmpeg_cmd = [
        "ffmpeg", "-y",
        "-f", "image2pipe",
        "-vcodec", "mjpeg",
        "-r", str(fps),
        "-s", f"{width}x{height}",
        "-i", "-"
    ]

    has_audio = AUDIO_MASTER.exists()
    if has_audio:
        ffmpeg_cmd.extend(["-i", str(AUDIO_MASTER)])

    ffmpeg_cmd.extend([
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-preset", "veryfast",
        "-crf", "18"
    ])

    if has_audio:
        ffmpeg_cmd.extend([
            "-c:a", "aac",
            "-b:a", "192k",
            "-shortest"
        ])

    ffmpeg_cmd.append(str(output_path))

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
        page = browser.new_page(viewport={"width": width, "height": height})
        target_url = f"http://127.0.0.1:{port}/scene.html?render=1&aspect={aspect}"
        page.goto(target_url)
        page.wait_for_function("() => window.__ready === true", timeout=20000)
        print("WebGL Canvas ready! Pipe streaming to FFmpeg...", flush=True)

        for i in range(total_frames):
            t = i / fps
            page.evaluate(f"window.__seekTo({t:.5f})")
            img_bytes = page.screenshot(type="jpeg", quality=98)
            ffmpeg_proc.stdin.write(img_bytes)

            if (i + 1) % 150 == 0 or i == total_frames - 1:
                elapsed = time.time() - t0
                speed = (i + 1) / elapsed if elapsed > 0 else 0
                eta = (total_frames - i - 1) / speed if speed > 0 else 0
                print(f"Rendered [{i+1:4d}/{total_frames}] ({((i+1)/total_frames)*100:.1f}%) | {speed:.1f} fps | ETA: {eta:.1f}s", flush=True)

        browser.close()

    ffmpeg_proc.stdin.close()
    ffmpeg_proc.wait()
    server.shutdown()

    elapsed = time.time() - t0
    print(f"Render finished in {elapsed:.1f}s! Saved to: {output_path}", flush=True)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Puti-AI 3D Clay Stop-Motion Offline Renderer")
    parser.add_argument("--aspect", choices=["16:9", "9:16"], default="16:9", help="Video aspect ratio")
    parser.add_argument("--fps", type=int, default=30, help="Framerate (default: 30)")
    parser.add_argument("--out", type=str, default=None, help="Output MP4 filename")
    args = parser.parse_args()

    render(aspect=args.aspect, fps=args.fps, output_name=args.out)

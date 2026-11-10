import argparse
import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

def run_step(script_name, description, extra_args=None):
    print(f"\n==========================================")
    print(f"  [RUN] {description} ({script_name})")
    print(f"==========================================")
    cmd = [sys.executable, str(BASE_DIR / script_name)]
    if extra_args:
        cmd.extend(extra_args)
    res = subprocess.run(cmd)
    if res.returncode != 0:
        print(f"[ERROR] Step {script_name} failed with code {res.returncode}", file=sys.stderr)
        sys.exit(res.returncode)

def run_check():
    print("\n=== Puti-AI 3D Clay Environment Health Check ===")
    has_error = False

    # 1. 檢查必要字型
    font_huninn = BASE_DIR / "fonts" / "huninn.ttf"
    font_noto = BASE_DIR / "fonts" / "NotoSansTC-VF.ttf"
    if font_huninn.exists():
        print(f"  [OK] Headline Font  : {font_huninn.name}")
    else:
        print(f"  [MISSING] Headline Font: {font_huninn}")
        has_error = True

    if font_noto.exists():
        print(f"  [OK] Body Font      : {font_noto.name}")
    else:
        print(f"  [MISSING] Body Font: {font_noto}")
        has_error = True

    # 2. 檢查核心場景與資料
    scene_html = BASE_DIR / "scene.html"
    cues_json = BASE_DIR / "cues.json"
    style_yaml = BASE_DIR / "style.yaml"
    for item in [scene_html, cues_json, style_yaml]:
        if item.exists():
            print(f"  [OK] Core File      : {item.name}")
        else:
            print(f"  [MISSING] Core File : {item.name}")
            has_error = True

    # 3. 檢查系統工具 (FFmpeg, Node, Playwright)
    for tool in ["ffmpeg", "ffprobe"]:
        try:
            ver = subprocess.check_output([tool, "-version"], stderr=subprocess.DEVNULL).decode('utf-8').split('\n')[0]
            print(f"  [OK] Tool           : {tool} ({ver.split()[2]})")
        except Exception:
            print(f"  [MISSING] CLI Tool  : {tool} not found in PATH!")
            has_error = True

    if not has_error:
        print("\nAll checks passed! Project is healthy and ready to build.")
    else:
        print("\nSome dependencies are missing. Please inspect above messages.", file=sys.stderr)

def main():
    parser = argparse.ArgumentParser(description="Puti-AI 3D Clay Explainer Video Master Build Pipeline")
    parser.add_argument("--check", action="store_true", help="Run health and environment check")
    parser.add_argument("--audio", action="store_true", help="Build procedural SFX, BGM, and master mix")
    parser.add_argument("--subtitles", action="store_true", help="Generate SRT and VTT subtitles from cues.json")
    parser.add_argument("--render", action="store_true", help="Run Playwright offline 1080p render")
    parser.add_argument("--aspect", choices=["16:9", "9:16"], default="16:9", help="Video aspect ratio")
    parser.add_argument("--fps", type=int, default=30, help="Framerate")
    parser.add_argument("--all", action="store_true", help="Execute full build: audio -> subtitles -> render")

    args = parser.parse_args()

    # If no flags passed, default to help or full build
    if not (args.check or args.audio or args.subtitles or args.render or args.all):
        parser.print_help()
        return

    if args.check:
        run_check()

    if args.audio or args.all:
        run_step("synth_sfx.py", "Synthesizing Procedural Audio & BGM")
        run_step("mix_audio.py", "Mixing Audio Master with Loudnorm")

    if args.subtitles or args.all:
        run_step("export_subtitles.py", "Exporting Subtitles (SRT / VTT)")

    if args.render or args.all:
        render_args = ["--aspect", args.aspect, "--fps", str(args.fps)]
        run_step("render_video.py", "Rendering 1080p 3D Clay Stop-Motion Video", extra_args=render_args)

if __name__ == "__main__":
    main()

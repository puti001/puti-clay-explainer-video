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

    # 1. 檢查 Python 依賴包
    python_packages = [
        ("playwright", "playwright"),
        ("edge_tts", "edge-tts"),
        ("yaml", "PyYAML"),
        ("soundfile", "soundfile"),
        ("numpy", "numpy")
    ]
    for mod_name, pkg_name in python_packages:
        try:
            __import__(mod_name)
            print(f"  [OK] Python Package : {pkg_name}")
        except ImportError:
            print(f"  [MISSING] Python Pkg: {pkg_name} (run: pip install {pkg_name})")
            has_error = True

    # 2. 檢查字型資產
    font_huninn = BASE_DIR / "fonts" / "huninn.ttf"
    font_noto = BASE_DIR / "fonts" / "NotoSansTC-VF.ttf"
    for f in [font_huninn, font_noto]:
        if f.exists():
            print(f"  [OK] Font Asset     : {f.name}")
        else:
            print(f"  [MISSING] Font Asset: {f}")
            has_error = True

    # 3. 檢查核心契約與資料檔
    core_files = [
        BASE_DIR / "scene.html",
        BASE_DIR / "style.yaml",
        BASE_DIR / "cues.json",
        BASE_DIR / "sfx.json"
    ]
    for item in core_files:
        if item.exists():
            print(f"  [OK] Core Contract  : {item.name}")
        else:
            print(f"  [MISSING] Core File : {item.name}")
            has_error = True

    # 4. 檢查系統工具 (FFmpeg, FFprobe)
    for tool in ["ffmpeg", "ffprobe"]:
        try:
            ver = subprocess.check_output([tool, "-version"], stderr=subprocess.DEVNULL).decode('utf-8').split('\n')[0]
            print(f"  [OK] System Tool    : {tool} ({ver.split()[2]})")
        except Exception:
            print(f"  [MISSING] CLI Tool  : {tool} not found in PATH!")
            has_error = True

    if not has_error:
        print("\nAll checks passed! Project is fully healthy, verified, and ready to render.")
    else:
        print("\nSome dependencies or assets are missing. Please inspect above messages.", file=sys.stderr)

def main():
    parser = argparse.ArgumentParser(description="Puti-AI 3D Clay Explainer Video Master Build Pipeline")
    parser.add_argument("--check", action="store_true", help="Run comprehensive health and environment check")
    parser.add_argument("--style", action="store_true", help="Compile style.yaml to style.js")
    parser.add_argument("--audio", action="store_true", help="Build procedural SFX, BGM, and master mix")
    parser.add_argument("--subtitles", action="store_true", help="Generate SRT and VTT subtitles from cues.json")
    parser.add_argument("--render", action="store_true", help="Run Playwright offline 1080p render")
    parser.add_argument("--aspect", choices=["16:9", "9:16"], default="16:9", help="Video aspect ratio (default: 16:9)")
    parser.add_argument("--fps", type=int, default=30, help="Framerate (default: 30)")
    parser.add_argument("--all", action="store_true", help="Execute full build: style -> audio -> subtitles -> render")

    args = parser.parse_args()

    if not (args.check or args.style or args.audio or args.subtitles or args.render or args.all):
        parser.print_help()
        return

    if args.check:
        run_check()

    if args.style or args.all:
        run_step("compile_style.py", "Compiling style.yaml -> style.js")

    if args.audio or args.all:
        run_step("synth_sfx.py", "Synthesizing Procedural Audio & BGM")
        run_step("mix_audio.py", "Mixing Audio Master from sfx.json & cues.json")

    if args.subtitles or args.all:
        run_step("export_subtitles.py", "Exporting Subtitles (SRT / VTT)")

    if args.render or args.all:
        render_args = ["--aspect", args.aspect, "--fps", str(args.fps)]
        run_step("render_video.py", f"Rendering 1080p 3D Clay Stop-Motion ({args.aspect})", extra_args=render_args)

if __name__ == "__main__":
    main()

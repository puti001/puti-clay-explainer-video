import http.server
import socketserver
import threading
from pathlib import Path
from playwright.sync_api import sync_playwright

BASE_DIR = Path(r"c:\antigravity\影片\逆向研究\claude3d_工法")
PORT = 8770

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(BASE_DIR), **kwargs)
    def log_message(self, format, *args):
        pass

socketserver.TCPServer.allow_reuse_address = True
server = socketserver.TCPServer(("127.0.0.1", PORT), Handler)
threading.Thread(target=server.serve_forever, daemon=True).start()

with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=True,
        args=["--use-gl=angle", "--use-angle=gl", "--enable-webgl", "--ignore-gpu-blocklist"]
    )
    page = browser.new_page(viewport={"width": 1280, "height": 720})
    page.goto(f"http://127.0.0.1:{PORT}/scene.html?render=1")
    page.wait_for_function("() => window.__ready === true", timeout=15000)

    # Test frames across the 4 scenes
    test_points = [
        (4.5, "check_scene1.jpg"),
        (22.0, "check_scene2.jpg"),
        (37.5, "check_scene3.jpg"),
        (55.0, "check_scene4.jpg"),
    ]
    for t, fn in test_points:
        page.evaluate(f"window.__seekTo({t})")
        page.screenshot(path=str(BASE_DIR / fn), type="jpeg", quality=95)
        print(f"Saved {fn} at t={t}s")

    browser.close()
server.shutdown()
print("Done checking all 4 scenes!")

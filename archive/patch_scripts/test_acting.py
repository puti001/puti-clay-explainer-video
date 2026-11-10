import http.server
import socketserver
import threading
from pathlib import Path
from playwright.sync_api import sync_playwright

BASE_DIR = Path(r"c:\antigravity\影片\逆向研究\claude3d_工法")
PORT = 8775

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

    checks = [
        (2.0, "acting_01_panic_look_up.jpg"),
        (16.5, "acting_02_jump_transition.jpg"),
        (22.0, "acting_03_dizzy_tabs.jpg"),
        (30.0, "acting_04_point_binder.jpg"),
        (35.0, "acting_05_push_cart.jpg"),
        (38.0, "acting_06_tumble_back.jpg"),
        (43.0, "acting_07_skeptical_coupon.jpg"),
        (55.0, "acting_08_confetti_podium.jpg"),
        (59.0, "acting_09_wink_cheer.jpg"),
    ]
    for t, fn in checks:
        page.evaluate(f"window.__seekTo({t})")
        page.screenshot(path=str(BASE_DIR / fn), type="jpeg", quality=95)
        print(f"Saved {fn} at t={t}s")

    browser.close()
server.shutdown()
print("All acting check frames saved!")

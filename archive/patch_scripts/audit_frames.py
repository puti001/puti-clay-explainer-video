import http.server
import socketserver
import threading
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

BASE_DIR = Path(r"c:\antigravity\影片\逆向研究\claude3d_工法")
PORT = 8802

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
        args=["--enable-webgl", "--ignore-gpu-blocklist", "--use-gl=angle", "--use-angle=d3d11"]
    )
    page = browser.new_page(viewport={"width": 1920, "height": 1080})
    page.goto(f"http://127.0.0.1:{PORT}/scene.html")
    page.wait_for_function("window.__ready === true", timeout=30000)

    targets = [
        (4.5, "verify_curr_s1_crush.jpg"),
        (21.0, "verify_curr_s2_orbit.jpg"),
        (28.0, "verify_curr_s2_binder.jpg"),
        (37.5, "verify_curr_s3_gate.jpg"),
        (56.5, "verify_curr_s4_podium.jpg"),
    ]

    for t, name in targets:
        page.evaluate(f"window.__seekTo({t})")
        time.sleep(0.08)
        out_p = BASE_DIR / name
        page.screenshot(path=str(out_p), quality=95, type="jpeg")
        print(f"Captured: {name} at {t}s")

    browser.close()

server.shutdown()
print("All frames captured!")

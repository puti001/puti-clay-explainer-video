import http.server
import socketserver
import threading
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

BASE_DIR = Path(r"c:\antigravity\影片\逆向研究\claude3d_工法")
PORT = 8806

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

    page.evaluate("window.__seekTo(14.5)")
    res = page.evaluate("window.__letters.map(m => ({ i: m.userData.i, minY: m.userData.minY, y: m.position.y }))")
    for r in res:
        print(r)

    browser.close()

server.shutdown()

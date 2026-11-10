import http.server
import socketserver
import threading
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

BASE_DIR = Path(r"c:\antigravity\影片\逆向研究\claude3d_工法")
PORT = 8807

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

    # 針對使用者點出的 4 個時間點精確截圖：
    targets = [
        (14.5, "verify_fix1_letters_ground.jpg"), # 1. 購物字體落定貼齊地面
        (19.0, "verify_fix2_cards_orbit_hero.jpg"), # 2. 卡片 360 度包圍中間小橘
        (44.0, "verify_fix3_s3_no_clipping.jpg"), # 3. 第 3 幕折價券避開小橘不穿模
        (56.5, "verify_fix4_podiums_3colors.jpg"), # 4. 第 4 幕三座台座 3 種顏色 + 立牌大字
    ]

    for t, name in targets:
        page.evaluate(f"window.__seekTo({t})")
        time.sleep(0.08)
        out_p = BASE_DIR / name
        page.screenshot(path=str(out_p), quality=95, type="jpeg")
        print(f"Captured: {name} at {t}s")

    browser.close()

server.shutdown()
print("All 4 verification frames captured!")

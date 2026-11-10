import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

BASE = Path(r"c:\antigravity\影片\逆向研究\claude3d_工法")
HTML_URL = f"file:///{BASE.as_posix()}/scene.html"

async def check_console():
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=["--enable-webgl", "--ignore-gpu-blocklist", "--use-gl=angle", "--use-angle=d3d11"]
        )
        page = await browser.new_page()
        page.on("console", lambda msg: print(f"BROWSER CONSOLE [{msg.type}]: {msg.text}"))
        page.on("pageerror", lambda exc: print(f"BROWSER PAGEERROR: {exc}"))
        await page.goto(HTML_URL)
        await asyncio.sleep(3)
        await browser.close()

if __name__ == "__main__":
    asyncio.run(check_console())

"""Capture frames of the three.js hero.

Usage: python3 -I capture.py <base_url> <out_dir> <frames> [query] [cam_json]
frames=1 -> single still at t=0.25 (for pose tuning)
"""
import json
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

base, out, n = sys.argv[1], Path(sys.argv[2]), int(sys.argv[3])
query = sys.argv[4] if len(sys.argv) > 4 else ""
cam = json.loads(sys.argv[5]) if len(sys.argv) > 5 else {}
out.mkdir(parents=True, exist_ok=True)

with sync_playwright() as p:
    b = p.chromium.launch(args=["--use-angle=swiftshader", "--enable-unsafe-swiftshader",
                                "--ignore-gpu-blocklist"])
    pg = b.new_page(viewport={"width": 1280, "height": 480}, device_scale_factor=1)
    logs = []
    pg.on("console", lambda m: logs.append(m.text))
    pg.on("pageerror", lambda e: logs.append(f"ERR {e}"))
    pg.goto(f"{base}/index.html?{query}")
    pg.wait_for_function("window.ready !== undefined", timeout=60000)
    pg.evaluate("window.ready")
    pg.evaluate("document.fonts.ready")
    pg.evaluate(f"window.setupCamera({json.dumps(cam)})")
    hero = pg.locator("#hero")
    times = [0.25] if n == 1 else [i / n for i in range(n)]
    for i, t in enumerate(times):
        pg.evaluate(f"window.renderAt({t})")
        hero.screenshot(path=str(out / f"f{i:03d}.png"))
    for line in logs[:20]:
        print(line)
    b.close()
print("captured", len(times))

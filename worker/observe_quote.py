"""Observe the actual quote page and its own requests, without clicking purchase controls."""
import argparse
import json
import time
from pathlib import Path
from urllib.parse import urlsplit

from playwright.sync_api import sync_playwright


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("run", type=Path)
    ap.add_argument("--headed", action="store_true")
    ap.add_argument("--seconds", type=int, default=35)
    args = ap.parse_args()
    state = json.loads((args.run / "state.private.json").read_text(encoding="utf-8"))
    url = state["data"]["history"][-1]["payload"]["redirectTo"].strip('"')
    parsed = urlsplit(url)
    if parsed.scheme != "https" or parsed.hostname != "chat.lemonade.com" or parsed.path != "/gb/home/quote/view":
        raise ValueError("Unexpected quote destination; navigation refused")
    capture = args.run / "browser"
    capture.mkdir(exist_ok=True)
    network = []
    errors = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=not args.headed)
        context = browser.new_context(viewport={"width": 1365, "height": 1000})
        cookies = []
        for c in state["cookies"]:
            cookie = {k: c[k] for k in ("name", "value", "domain", "path", "secure")}
            if c.get("expires") and c["expires"] > time.time():
                cookie["expires"] = c["expires"]
            cookies.append(cookie)
        context.add_cookies(cookies)
        page = context.new_page()
        page.on("pageerror", lambda e: errors.append(str(e)))

        def received(response):
            request = response.request
            parts = urlsplit(response.url)
            if not (parts.hostname == "lemonade.com" or (parts.hostname or "").endswith(".lemonade.com")):
                return
            record = {"url": response.url, "status": response.status,
                      "method": request.method, "type": request.resource_type,
                      "content_type": response.headers.get("content-type", "")}
            if request.resource_type in ("fetch", "xhr", "document"):
                record["request_headers"] = request.all_headers()
                record["request_body"] = request.post_data
                try:
                    body = response.body()
                    suffix = ".json" if "json" in record["content_type"] else ".txt"
                    name = f"response-{len(network):03d}.private{suffix}"
                    (capture / name).write_bytes(body)
                    record["body_file"] = name
                    print(response.status, request.method, parts.hostname, parts.path, record["content_type"], flush=True)
                except Exception as exc:
                    record["capture_error"] = str(exc)
            network.append(record)

        page.on("response", received)
        try:
            page.goto(url, wait_until="domcontentloaded", timeout=45000)
            deadline = time.monotonic() + min(max(args.seconds, 1), 90)
            while time.monotonic() < deadline:
                page.wait_for_timeout(1000)
            (capture / "page.private.txt").write_text(page.locator("body").inner_text(), encoding="utf-8")
            (capture / "page.private.html").write_text(page.content(), encoding="utf-8")
            page.screenshot(path=str(capture / "page.private.png"), full_page=True)
            context.storage_state(path=str(capture / "storage.private.json"))
            print("Page title:", page.title(), flush=True)
        except Exception as exc:
            errors.append(str(exc))
            print("Browser observation error:", type(exc).__name__, flush=True)
        finally:
            (capture / "network.private.json").write_text(json.dumps(network, indent=2), encoding="utf-8")
            (capture / "errors.private.json").write_text(json.dumps(errors, indent=2), encoding="utf-8")
            browser.close()
    print("Captured", len(network), "responses;", len(errors), "page errors")


if __name__ == "__main__":
    main()

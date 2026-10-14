"""Điểm khởi động ứng dụng desktop DCS PCCC Takeoff."""
import os
import sys

import webview

from . import APP_NAME, __version__
from .api import Api
from .core.paths import ui_dir


def main():
    api = Api()
    window = webview.create_window(
        f"{APP_NAME} – DC Software",
        url=str(ui_dir() / "index.html"),
        js_api=api,
        width=1440,
        height=900,
        min_size=(1180, 720),
        background_color="#F6F7FB",
        text_select=True,
    )
    api._window = window
    debug = "--debug" in sys.argv
    if "--selftest" in sys.argv:
        out = sys.argv[sys.argv.index("--selftest") + 1]
        webview.start(_selftest, (window, out), gui="edgechromium", private_mode=False)
        return
    webview.start(gui="edgechromium", debug=debug, private_mode=False)


def _selftest(window, out):
    """Kiểm tra bản đóng gói: giao diện khởi động được và gọi được phần xử lý."""
    import json
    import time
    res = {"ok": False}
    try:
        for _ in range(80):
            time.sleep(0.25)
            if window.evaluate_js("typeof S!=='undefined' && !!S.info"):
                break
        time.sleep(1.0)
        res = {"ok": bool(window.evaluate_js("!!S.info")),
               "version": window.evaluate_js("S.info && S.info.version"),
               "catalog": window.evaluate_js("S.info ? S.info.catalog.length : 0"),
               "projects": window.evaluate_js("S.projects ? S.projects.length : -1"),
               "errors": window.evaluate_js("window.__errs")}
        src = os.environ.get("PCCC_SELFTEST_INPUT")
        if src:
            from .core import compute as C
            from .core import project as P
            t0 = time.time()
            prj = P.process(P.create("Selftest", [src])["id"], lambda *a: None)
            r = C.compute(prj)
            res["process"] = {"seconds": round(time.time() - t0, 1), "pages": len(prj["pages"]),
                              "engines": sorted({f.get("convert", {}).get("engine", "") for f in prj["files"]}),
                              "stats": r["stats"]}
            P.delete(prj["id"])
    except Exception as ex:
        res["exception"] = repr(ex)
    with open(out, "w", encoding="utf-8") as fh:
        json.dump(res, fh, ensure_ascii=False)
    window.destroy()


if __name__ == "__main__":
    main()

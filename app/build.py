"""Đóng gói ứng dụng thành thư mục chạy được (dist/DCS PCCC Takeoff/).

Chạy:  .venv\Scripts\python app\build.py
"""
import os
import shutil
import subprocess
import sys
from pathlib import Path

from PIL import Image

APP = Path(__file__).resolve().parent
ROOT = APP.parent
NAME = "DCS PCCC Takeoff"


def make_icon() -> Path:
    src = APP / "pccc_takeoff" / "ui" / "assets" / "logo-dark.png"
    ico = APP / "build" / "app.ico"
    ico.parent.mkdir(parents=True, exist_ok=True)
    im = Image.open(src).convert("RGBA")
    h = im.height
    sq = im.crop((0, 0, h, h))  # phần biểu tượng bên trái logo
    canvas = Image.new("RGBA", (256, 256), (0, 0, 0, 0))
    sq = sq.resize((232, 232), Image.LANCZOS)
    canvas.paste(sq, (12, 12), sq)
    canvas.save(ico, sizes=[(16, 16), (24, 24), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)])
    return ico


def sync_ui_version():
    """Ghi số phiên bản (__version__) vào giao diện: nhãn, hằng UI_VERSION, ?v= của css/js."""
    import re
    ver = re.search(r'__version__ = "([^"]+)"', (APP / "pccc_takeoff" / "__init__.py").read_text(encoding="utf-8")).group(1)
    ui = APP / "pccc_takeoff" / "ui"
    html = (ui / "index.html").read_text(encoding="utf-8")
    html = re.sub(r"\?v=[0-9.]+", f"?v={ver}", html)
    html = re.sub(r"Phiên bản [0-9.]+", f"Phiên bản {ver}", html)
    (ui / "index.html").write_text(html, encoding="utf-8")
    js = (ui / "js" / "app.js").read_text(encoding="utf-8")
    js = re.sub(r'const UI_VERSION = "[^"]+"', f'const UI_VERSION = "{ver}"', js)
    (ui / "js" / "app.js").write_text(js, encoding="utf-8")
    return ver


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    print("Phiên bản:", sync_ui_version())
    # --dist <thư mục>: đóng gói ra chỗ khác (dùng khi bản cũ đang mở, Windows khoá file)
    dist = Path(sys.argv[sys.argv.index("--dist") + 1]) if "--dist" in sys.argv else ROOT / "dist"
    ico = make_icon()
    sep = ";"
    args = [
        sys.executable, "-m", "PyInstaller", "--noconfirm", "--clean", "--windowed",
        "--name", NAME, "--icon", str(ico),
        "--distpath", str(dist), "--workpath", str(APP / "build" / "work"), "--specpath", str(APP / "build"),
        "--add-data", f"{APP / 'pccc_takeoff' / 'ui'}{sep}ui",
        "--add-data", f"{APP / 'vendor' / 'libredwg'}{sep}vendor/libredwg",
        "--collect-submodules", "ezdxf",
        "--exclude-module", "PySide6", "--exclude-module", "PyQt5", "--exclude-module", "PyQt6",
        "--exclude-module", "matplotlib", "--exclude-module", "tkinter",
        "--hidden-import", "webview.platforms.edgechromium",
        "--hidden-import", "webview.platforms.winforms",
        "--paths", str(APP),
        str(APP / "run_app.py"),
    ]
    env = dict(os.environ, PYTHONUTF8="1", PYTHONIOENCODING="utf-8")
    subprocess.check_call(args, env=env)
    out = dist / NAME
    shutil.copy(APP / "vendor" / "libredwg" / "COPYING", out / "LICENSE-LibreDWG-GPLv3.txt")
    (out / "README.txt").write_text(
        "DCS PCCC Takeoff – DC Software (dcsoftware.vn)\r\n\r\n"
        f"Chạy file \"{NAME}.exe\".\r\n"
        "Yêu cầu: Windows 10/11 có Microsoft Edge WebView2 Runtime (mặc định có sẵn trên Windows 10/11 cập nhật).\r\n\r\n"
        "Phần mềm dùng LibreDWG (GNU GPL v3) như một chương trình riêng để chuyển DWG sang DXF.\r\n"
        "Mã nguồn LibreDWG: https://github.com/LibreDWG/libredwg (phiên bản 0.14).\r\n",
        encoding="utf-8")
    print("OK ->", out)


if __name__ == "__main__":
    main()

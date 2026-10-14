"""Đường dẫn tài nguyên và dữ liệu người dùng."""
import os
import sys
from pathlib import Path


def resource_dir() -> Path:
    """Thư mục chứa ui/ và vendor/ (khi chạy từ source hoặc bản đóng gói)."""
    if getattr(sys, "frozen", False):
        return Path(getattr(sys, "_MEIPASS", Path(sys.executable).parent))
    return Path(__file__).resolve().parent.parent


def ui_dir() -> Path:
    return resource_dir() / "ui"


def libredwg_exe() -> Path:
    base = resource_dir()
    for cand in (base / "vendor" / "libredwg" / "dwg2dxf.exe",
                 base.parent / "vendor" / "libredwg" / "dwg2dxf.exe"):
        if cand.exists():
            return cand
    return base / "vendor" / "libredwg" / "dwg2dxf.exe"


def data_dir() -> Path:
    root = os.environ.get("APPDATA") or str(Path.home())
    p = Path(root) / "DCSoftware" / "PCCC Takeoff"
    p.mkdir(parents=True, exist_ok=True)
    return p


def projects_dir() -> Path:
    p = data_dir() / "projects"
    p.mkdir(parents=True, exist_ok=True)
    return p

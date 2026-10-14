"""Thư viện ký hiệu đã "dạy": lưu lại để dự án sau tự nhận ra."""
import json
import threading

from .paths import data_dir

_LOCK = threading.Lock()


def _path():
    return data_dir() / "library.json"


def load() -> dict:
    p = _path()
    if p.exists():
        try:
            d = json.loads(p.read_text(encoding="utf-8"))
            d.setdefault("symbols", {})
            d.setdefault("layers", {})
            return d
        except Exception:
            pass
    return {"symbols": {}, "layers": {}}


def save(lib: dict):
    with _LOCK:
        tmp = _path().with_suffix(".tmp")
        tmp.write_text(json.dumps(lib, ensure_ascii=False, indent=1), encoding="utf-8")
        tmp.replace(_path())


def remember(kind: str, key: str, mapping: dict | None):
    lib = load()
    if mapping is None:
        lib[kind].pop(key, None)
    else:
        lib[kind][key] = {k: v for k, v in mapping.items() if k in ("material", "unit", "ignore", "factor")}
    save(lib)

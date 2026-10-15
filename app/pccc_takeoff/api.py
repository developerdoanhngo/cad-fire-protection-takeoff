"""Cầu nối giữa giao diện (JavaScript) và phần xử lý (Python)."""
import os
import subprocess
import threading
import time
import traceback
from pathlib import Path

import webview

from . import APP_NAME, __version__
from .core import catalog as CAT
from .core import compute as C
from .core import export_xlsx as X
from .core import library as L
from .core import project as P


def _dialog(name):
    fd = getattr(webview, "FileDialog", None)
    if fd is not None:
        return getattr(fd, name)
    return getattr(webview, f"{name}_DIALOG")


class Api:
    def __init__(self):
        self._window = None
        self._jobs = {}
        self._cache = {}
        self._lock = threading.RLock()

    # ------------------------------------------------------------ nội bộ
    def _prj(self, pid):
        with self._lock:
            if pid not in self._cache:
                self._cache[pid] = P.load(pid)
            return self._cache[pid]

    def _save(self, prj):
        with self._lock:
            P.save(prj)

    # ------------------------------------------------------------ chung
    def app_info(self):
        return {"name": APP_NAME, "version": __version__, "catalog": CAT.catalog_list(),
                "rules": len(CAT.RULES),
                "systems": [{"code": c, "name": n} for c, n in CAT.SYSTEMS]}

    def list_projects(self):
        return P.list_projects()

    def pick_folder(self):
        r = self._window.create_file_dialog(_dialog("FOLDER"))
        return r[0] if r else None

    def pick_files(self):
        r = self._window.create_file_dialog(_dialog("OPEN"), allow_multiple=True,
                                            file_types=("Bản vẽ CAD (*.dwg;*.dxf)", "Tất cả file (*.*)"))
        return list(r) if r else []

    def scan(self, paths):
        try:
            files = P.scan_inputs(paths)
        except Exception as ex:
            return {"error": str(ex), "files": []}
        for f in files:
            f["system_name"] = CAT.SYSTEM_NAME.get(f["system"], "")
        name = ""
        if paths:
            p = Path(paths[0])
            name = p.name if p.is_dir() else p.parent.name
        return {"files": files, "suggested_name": name}

    def create_project(self, name, paths):
        try:
            prj = P.create(name, paths or [])
        except Exception as ex:
            return {"error": str(ex)}
        if prj["files"]:
            self.start_processing(prj["id"])
        return {"id": prj["id"], "processing": bool(prj["files"])}

    def set_drawings(self, pid, paths):
        """Thêm / thay bộ bản vẽ cho dự án rồi xử lý lại."""
        try:
            prj = P.set_drawings(pid, paths or [])
        except Exception as ex:
            return {"error": str(ex)}
        with self._lock:
            self._cache[pid] = prj
        self.start_processing(pid)
        return {"id": pid, "processing": True}

    def start_processing(self, pid):
        job = {"stage": "start", "pct": 0.0, "msg": "Chuẩn bị…", "done": False, "error": None,
               "started": time.time(), "log": []}
        self._jobs[pid] = job
        weights = {"convert": (0.02, 0.23), "read": (0.25, 0.68), "pages": (0.25, 0.68), "symbols": (0.95, 0.0), "done": (1.0, 0.0)}

        def cb(stage, pct, msg):
            a, b = weights.get(stage, (0, 0))
            job["stage"] = stage
            job["pct"] = min(1.0, a + b * pct)
            if msg != job["msg"]:
                job["log"].append(msg)
                job["log"] = job["log"][-40:]
            job["msg"] = msg

        def run():
            try:
                prj = P.process(pid, cb)
                with self._lock:
                    self._cache[pid] = prj
                job["done"] = True
                job["pct"] = 1.0
            except Exception as ex:
                job["error"] = str(ex) or ex.__class__.__name__
                job["trace"] = traceback.format_exc()
                job["done"] = True
                with self._lock:
                    self._cache.pop(pid, None)

        threading.Thread(target=run, daemon=True).start()
        return True

    def progress(self, pid):
        j = self._jobs.get(pid)
        if not j:
            return {"stage": "idle", "done": True}
        out = {k: v for k, v in j.items() if k != "trace"}
        out["elapsed"] = round(time.time() - j["started"], 1)
        return out

    # ------------------------------------------------------------ dự án
    def get_project(self, pid):
        prj = self._prj(pid)
        counts = P.symbol_counts(prj)
        lens = P.layer_lengths(prj)
        pages = []
        for p in prj["pages"]:
            top = sorted(p["counts"].items(), key=lambda kv: -kv[1])[:8]
            pages.append({k: p[k] for k in ("id", "file", "file_name", "system", "index", "title", "building", "floors",
                                            "floor_label", "multiplier", "include", "auto_reason", "warnings", "scale")}
                         | {"n_symbols": sum(p["counts"].values()), "n_legend": sum(p["legend"].values()),
                            "top": top, "lengths": p["lengths"]})
        syms = []
        for key, s in prj["symbols"].items():
            syms.append({"key": key, "eff": s["eff"], "label": s["label"], "svg": s.get("svg", ""),
                         "map": s.get("map"), "source": s.get("source"), "files": s.get("files", []),
                         "count": round(counts["included"].get(key, 0)), "count_all": counts["all"].get(key, 0)})
        syms.sort(key=lambda s: (-s["count"], -s["count_all"], s["key"]))
        layers = []
        for layer, l in prj["layers"].items():
            layers.append({"layer": layer, "map": l.get("map"), "source": l.get("source"), "files": l.get("files", []),
                           "length": round(lens.get(layer, 0.0), 1), "length_all": round(l.get("total_m", 0.0), 1)})
        layers.sort(key=lambda l: (l["map"] is None, -l["length"]))
        files = [{k: f.get(k) for k in ("id", "name", "role", "system", "size", "frames", "status")} |
                 {"system_name": CAT.SYSTEM_NAME.get(f.get("system"), "")} for f in prj["files"]]
        return {"id": prj["id"], "name": prj["name"], "status": prj.get("status"), "error": prj.get("error"),
                "created": prj.get("created"), "updated": prj.get("updated"),
                "process_seconds": prj.get("process_seconds"), "files": files, "pages": pages,
                "symbols": syms, "layers": layers, "settings": prj.get("settings", {})}

    def page_geometry(self, pid, page_id):
        return P.page_geometry(pid, page_id)

    def update_page(self, pid, page_id, changes):
        prj = self._prj(pid)
        for p in prj["pages"]:
            if p["id"] == page_id:
                for k in ("include", "multiplier", "building", "floor_label"):
                    if k in changes:
                        v = changes[k]
                        if k == "multiplier":
                            try:
                                v = max(0.0, float(v))
                            except Exception:
                                v = 1
                        p[k] = v
                self._save(prj)
                return True
        return False

    def bulk_include(self, pid, page_ids, include):
        prj = self._prj(pid)
        ids = set(page_ids)
        for p in prj["pages"]:
            if p["id"] in ids:
                p["include"] = bool(include)
        self._save(prj)
        return True

    def set_symbol(self, pid, key, mapping, remember=True):
        prj = self._prj(pid)
        s = prj["symbols"].get(key)
        if s is None:
            return False
        if mapping is None:
            s["map"], s["source"] = None, None
        else:
            s["map"] = {"material": (mapping.get("material") or "").strip(), "unit": mapping.get("unit") or "cái",
                        "ignore": bool(mapping.get("ignore"))}
            s["source"] = "user"
        self._save(prj)
        if remember:
            L.remember("symbols", key, s["map"])
        return True

    def accept_suggestions(self, pid):
        prj = self._prj(pid)
        n = 0
        for key, s in prj["symbols"].items():
            if s.get("source") == "suggest" and s.get("map"):
                s["source"] = "user"
                L.remember("symbols", key, s["map"])
                n += 1
        for layer, l in prj["layers"].items():
            if l.get("source") == "suggest" and l.get("map"):
                l["source"] = "user"
                L.remember("layers", layer, l["map"])
        self._save(prj)
        return n

    def set_layer(self, pid, layer, mapping, remember=True):
        prj = self._prj(pid)
        l = prj["layers"].get(layer)
        if l is None:
            return False
        if mapping is None:
            l["map"], l["source"] = None, None
        else:
            try:
                factor = float(mapping.get("factor", 1) or 1)
            except Exception:
                factor = 1.0
            l["map"] = {"material": (mapping.get("material") or "").strip(), "unit": mapping.get("unit") or "m",
                        "factor": factor, "ignore": bool(mapping.get("ignore"))}
            l["source"] = "user"
        self._save(prj)
        if remember:
            L.remember("layers", layer, l["map"])
        return True

    def update_settings(self, pid, settings):
        prj = self._prj(pid)
        prj.setdefault("settings", {}).update(settings or {})
        self._save(prj)
        return prj["settings"]

    def rename_project(self, pid, name):
        prj = self._prj(pid)
        prj["name"] = (name or "").strip() or prj["name"]
        self._save(prj)
        return prj["name"]

    def compute(self, pid):
        return C.compute(self._prj(pid))

    def export_excel(self, pid):
        prj = self._prj(pid)
        res = C.compute(prj)
        safe = "".join(ch for ch in prj["name"] if ch not in '\\/:*?"<>|').strip() or "Khoi luong"
        r = self._window.create_file_dialog(_dialog("SAVE"), save_filename=f"{safe} - Khối lượng.xlsx",
                                            file_types=("Excel (*.xlsx)",))
        if not r:
            return None
        path = r if isinstance(r, str) else r[0]
        try:
            return {"path": X.export(prj, res, path)}
        except PermissionError:
            return {"error": "Không ghi được file. Có thể file đang mở trong Excel – hãy đóng file rồi thử lại."}
        except Exception as ex:
            return {"error": str(ex)}

    def open_path(self, path):
        try:
            os.startfile(path)
            return True
        except Exception:
            return False

    def reveal(self, path):
        try:
            subprocess.Popen(["explorer", "/select,", str(Path(path))])
            return True
        except Exception:
            return False

    def delete_project(self, pid):
        with self._lock:
            self._cache.pop(pid, None)
        P.delete(pid)
        return True

    def open_website(self):
        import webbrowser
        webbrowser.open("https://dcsoftware.vn")
        return True

    # ------------------------------------------------------------ thư viện ký hiệu
    def library(self):
        lib = L.load()
        # dự án còn ký hiệu "Gợi ý" / "Chưa xác định" -> gợi ý người dùng vào xác nhận
        pending = []
        for meta in P.list_projects():
            if meta.get("status") != "ready":
                continue
            try:
                prj = self._prj(meta["id"])
            except Exception:
                continue
            counts = P.symbol_counts(prj)["included"]
            sug = sum(1 for k, s in prj["symbols"].items() if s.get("source") == "suggest" and counts.get(k, 0) > 0)
            unk = sum(1 for k, s in prj["symbols"].items() if not s.get("map") and counts.get(k, 0) > 0)
            if sug or unk:
                pending.append({"id": meta["id"], "name": meta["name"], "suggest": sug, "unknown": unk,
                                "updated": meta.get("updated")})
        return {"symbols": [{"key": k} | v for k, v in sorted(lib["symbols"].items())],
                "layers": [{"key": k} | v for k, v in sorted(lib["layers"].items())],
                "pending": pending}

    def library_remove(self, kind, key):
        L.remember(kind, key, None)
        return True

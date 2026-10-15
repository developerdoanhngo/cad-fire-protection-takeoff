"""Quản lý dự án: tạo, xử lý bản vẽ, lưu / mở lại."""
import gzip
import json
import shutil
import time
import traceback
import uuid
from collections import defaultdict
from datetime import datetime
from pathlib import Path

from . import library
from .catalog import detect_system, suggest_layer, suggest_symbol
from .convert import convert_dwg
from .extract import dec, extract_file
from .pages import build_pages
from .paths import projects_dir

DEFAULT_SETTINGS = {"waste_pipe": 0, "waste_cable": 0, "waste_duct": 0, "round_pipe_6m": False}


def _now():
    return datetime.now().isoformat(timespec="seconds")


def project_dir(pid: str) -> Path:
    return projects_dir() / pid


def save(project: dict):
    project["updated"] = _now()
    d = project_dir(project["id"])
    d.mkdir(parents=True, exist_ok=True)
    tmp = d / "project.tmp"
    tmp.write_text(json.dumps(project, ensure_ascii=False), encoding="utf-8")
    tmp.replace(d / "project.json")


def load(pid: str) -> dict:
    p = json.loads((project_dir(pid) / "project.json").read_text(encoding="utf-8"))
    p.setdefault("settings", dict(DEFAULT_SETTINGS))
    return p


def list_projects() -> list:
    out = []
    for d in projects_dir().iterdir():
        f = d / "project.json"
        if not f.exists():
            continue
        try:
            p = json.loads(f.read_text(encoding="utf-8"))
        except Exception:
            continue
        pages = p.get("pages", [])
        out.append({
            "id": p["id"], "name": p["name"], "created": p.get("created"), "updated": p.get("updated"),
            "status": p.get("status"), "files": len([x for x in p.get("files", []) if x.get("role") == "main"]),
            "pages": len(pages), "pages_used": sum(1 for x in pages if x.get("include")),
            "symbols": len(p.get("symbols", {})),
            "systems": sorted({x.get("system") for x in p.get("files", []) if x.get("role") == "main"}),
        })
    out.sort(key=lambda x: x.get("updated") or "", reverse=True)
    return out


def scan_inputs(paths: list) -> list:
    files = []
    seen = set()
    for raw in paths:
        p = Path(raw)
        cands = []
        if p.is_dir():
            cands = [q for q in p.rglob("*") if q.suffix.lower() in (".dwg", ".dxf")]
        elif p.suffix.lower() in (".dwg", ".dxf"):
            cands = [p]
            # tự lấy thêm thư mục Xref đi kèm
            for sub in p.parent.iterdir():
                if sub.is_dir() and "xref" in sub.name.lower():
                    cands += [q for q in sub.rglob("*") if q.suffix.lower() in (".dwg", ".dxf")]
        for q in cands:
            k = str(q.resolve()).lower()
            if k in seen:
                continue
            seen.add(k)
            is_xref = any("xref" in part.lower() for part in q.parent.parts[-2:]) or q.stem.lower().startswith("xref")
            files.append({"path": str(q), "name": q.name, "role": "xref" if is_xref else "main",
                          "size": q.stat().st_size})
    files.sort(key=lambda f: (f["role"] != "main", f["name"].lower()))
    for i, f in enumerate(files):
        f["id"] = f"F{i + 1:02d}"
        f["system"] = detect_system(f["name"]) if f["role"] == "main" else ""
        f["status"] = "pending"
    return files


def create(name: str, inputs: list) -> dict:
    """Tạo dự án. `inputs` rỗng = dự án trống, thêm bản vẽ sau bằng set_drawings()."""
    files = scan_inputs(inputs) if inputs else []
    if inputs and not any(f["role"] == "main" for f in files):
        raise ValueError("Không tìm thấy file bản vẽ .dwg/.dxf nào trong lựa chọn.")
    pid = datetime.now().strftime("%Y%m%d-%H%M%S-") + uuid.uuid4().hex[:4]
    project = {
        "id": pid, "name": name.strip() or "Dự án mới", "created": _now(), "updated": _now(),
        "status": "new" if files else "empty", "error": None, "inputs": inputs or [], "files": files,
        "pages": [], "symbols": {}, "layers": {}, "settings": dict(DEFAULT_SETTINGS),
    }
    save(project)
    return project


def set_drawings(pid: str, inputs: list) -> dict:
    """Gắn (hoặc thay) bộ bản vẽ của dự án. Ký hiệu đã xác nhận vẫn giữ nhờ thư viện."""
    files = scan_inputs(inputs)
    if not any(f["role"] == "main" for f in files):
        raise ValueError("Không tìm thấy file bản vẽ .dwg/.dxf nào trong lựa chọn.")
    project = load(pid)
    project.update({"inputs": inputs, "files": files, "pages": [], "symbols": {}, "layers": {},
                    "status": "new", "error": None})
    save(project)
    return project


def _apply_mapping(project):
    lib = library.load()
    for key, s in project["symbols"].items():
        if s.get("map") and s.get("source") == "user":
            continue
        if key in lib["symbols"]:
            s["map"], s["source"] = dict(lib["symbols"][key]), "library"
        else:
            sug = suggest_symbol(s["eff"], s["label"])
            s["map"], s["source"] = (sug, "suggest") if sug else (None, None)
    for layer, l in project["layers"].items():
        if l.get("map") and l.get("source") == "user":
            continue
        if layer in lib["layers"]:
            l["map"], l["source"] = dict(lib["layers"][layer]), "library"
        else:
            sug = suggest_layer(layer)
            l["map"], l["source"] = (sug, "suggest") if sug else (None, None)


def process(pid: str, progress):
    """Chạy toàn bộ: chuyển file -> đọc -> chia trang -> gợi ý ký hiệu. `progress(stage, pct, msg)`."""
    project = load(pid)
    if not any(f["role"] == "main" for f in project["files"]):
        raise ValueError("Dự án chưa có bản vẽ. Hãy thêm bản vẽ trước.")
    project["status"] = "processing"
    save(project)
    d = project_dir(pid)
    work = d / "work"
    cache = d / "pages"
    shutil.rmtree(work, ignore_errors=True)
    shutil.rmtree(cache, ignore_errors=True)
    work.mkdir(parents=True)
    cache.mkdir(parents=True)
    t0 = time.time()
    try:
        files = project["files"]
        n = len(files)
        dxf_of = {}
        for i, f in enumerate(files):
            progress("convert", i / n, f"Chuyển đổi {f['name']}")
            out, info = convert_dwg(Path(f["path"]), work, f["id"])
            dxf_of[f["id"]] = str(out)
            f["convert"] = info
            f["status"] = "converted"
        lookup = {dec(Path(f["name"]).stem).lower(): dxf_of[f["id"]] for f in files}
        xref_cache = {}
        mains = [f for f in files if f["role"] == "main"]
        pages_all, symbols, layers = [], {}, {}
        for j, f in enumerate(mains):
            base = j / len(mains)

            def cb(x, f=f, base=base):
                progress("read", base + x / len(mains), f"Đọc bản vẽ {f['name']}")

            cb(0)
            fd = extract_file(dxf_of[f["id"]], lookup, xref_cache, cb)
            progress("pages", base + 0.95 / len(mains), f"Chia trang {f['name']}")
            pages, geoms = build_pages(fd, f["id"], f["system"], f["name"])
            for pg in pages:
                with gzip.open(cache / f"{pg['id']}.json.gz", "wt", encoding="utf-8") as fh:
                    json.dump(geoms[pg["id"]], fh, separators=(",", ":"))
            pages_all += pages
            f["frames"] = len(fd["frames"])
            f["status"] = "done"
            for key, k in fd["keys"].items():
                s = symbols.setdefault(key, {"eff": k["eff"], "label": k["label"], "svg": k["svg"], "files": []})
                if f["id"] not in s["files"]:
                    s["files"].append(f["id"])
                if not s["svg"] and k["svg"]:
                    s["svg"] = k["svg"]
            for pg in pages:
                for layer, L in pg["lengths"].items():
                    l = layers.setdefault(layer, {"files": [], "total_m": 0.0})
                    l["total_m"] += L
                    if f["id"] not in l["files"]:
                        l["files"].append(f["id"])
            del fd
        progress("symbols", 0.98, "Nhận diện ký hiệu")
        project["pages"] = pages_all
        project["symbols"] = symbols
        project["layers"] = layers
        _apply_mapping(project)
        project["status"] = "ready"
        project["error"] = None
        project["process_seconds"] = round(time.time() - t0, 1)
        save(project)
        progress("done", 1.0, "Hoàn tất")
    except Exception as ex:
        project["status"] = "error"
        project["error"] = f"{ex}"
        project["traceback"] = traceback.format_exc()
        save(project)
        raise
    finally:
        shutil.rmtree(work, ignore_errors=True)
    return project


def page_geometry(pid: str, page_id: str) -> dict:
    f = project_dir(pid) / "pages" / f"{page_id}.json.gz"
    with gzip.open(f, "rt", encoding="utf-8") as fh:
        return json.load(fh)


def symbol_counts(project: dict) -> dict:
    """Số lượng mỗi ký hiệu: trên các trang được tính (đã nhân hệ số tầng) và trên toàn bộ."""
    inc = defaultdict(float)
    allc = defaultdict(int)
    for p in project["pages"]:
        for k, n in p["counts"].items():
            allc[k] += n
            if p["include"]:
                inc[k] += n * float(p.get("multiplier") or 1)
    return {"included": inc, "all": allc}


def layer_lengths(project: dict) -> dict:
    inc = defaultdict(float)
    for p in project["pages"]:
        if p["include"]:
            for l, L in p["lengths"].items():
                inc[l] += L * float(p.get("multiplier") or 1)
    return inc


def delete(pid: str):
    shutil.rmtree(project_dir(pid), ignore_errors=True)

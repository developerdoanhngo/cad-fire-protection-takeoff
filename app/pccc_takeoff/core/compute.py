"""Tính khối lượng từ các trang được chọn và bảng ký hiệu -> vật tư."""
import math
from collections import defaultdict

from .catalog import SYSTEM_NAME, SYSTEM_ORDER

ROMAN = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X"]
BUILDING_ORDER = ["Ngoài nhà", "Trạm bơm", "Nhà xưởng", "Nhà kho", "Nhà văn phòng", "Nhà để xe",
                  "Nhà điều hành XLNT", "Nhà bảo vệ", "Chung"]


def _waste(settings, material):
    m = material.lower()
    if m.startswith("ống thép"):
        return float(settings.get("waste_pipe", 0) or 0)
    if m.startswith("dây") or m.startswith("cáp"):
        return float(settings.get("waste_cable", 0) or 0)
    if m.startswith("ống gió"):
        return float(settings.get("waste_duct", 0) or 0)
    return 0.0


def _bkey(b):
    first = b.split(" + ")[0]
    return (BUILDING_ORDER.index(first) if first in BUILDING_ORDER else 50, b)


def compute(project: dict) -> dict:
    st = project.get("settings", {})
    syms = project.get("symbols", {})
    lays = project.get("layers", {})
    items = {}
    detail = []
    unmapped = defaultdict(float)
    pages_used = 0
    seen_len = defaultdict(list)  # (hệ, nhà, tầng, lớp) -> [(chiều dài, trang)]
    dups = []
    for p in project.get("pages", []):
        if not p.get("include"):
            continue
        pages_used += 1
        mult = max(float(p.get("multiplier") or 1), 0.0)
        per = defaultdict(lambda: [0.0, 0.0, "", ""])
        for key, n in p.get("counts", {}).items():
            m = (syms.get(key) or {}).get("map")
            if not m or (not m.get("ignore") and not m.get("material")):
                unmapped[key] += n * mult
                continue
            if m.get("ignore"):
                continue
            r = per[(m["material"], m.get("unit") or "cái")]
            r[0] += n
            r[1] += n * mult
            r[2] = "Đếm"
        for layer, L in p.get("lengths", {}).items():
            m = (lays.get(layer) or {}).get("map")
            if not m or m.get("ignore") or not m.get("material"):
                continue
            # cùng một đường ống vẽ lặp lại ở nhiều trang của cùng tầng -> chỉ tính 1 lần
            gk = (p["system"], p["building"], tuple(p.get("floors") or ()), p.get("file"), layer)
            twin = next((pg for L0, pg in seen_len[gk] if abs(L - L0) <= max(0.01 * max(L, L0), 0.5)), None)
            if twin is not None:
                dups.append({"page_id": p["id"], "page": p["index"], "file": p.get("file_name", ""),
                             "title": p["title"], "layer": layer, "twin": twin, "length": L})
                continue
            seen_len[gk].append((L, p["index"]))
            base = L * float(m.get("factor", 1) or 1)
            q = base * mult * (1 + _waste(st, m["material"]) / 100.0)
            r = per[(m["material"], m.get("unit") or "m")]
            r[0] += base
            r[1] += q
            r[2] = "Đo"
        for (mat, unit), (base, q, src, _x) in per.items():
            key = (p["system"], p["building"], mat, unit)
            it = items.setdefault(key, {"material": mat, "unit": unit, "qty": 0.0, "source": src, "pages": []})
            it["qty"] += q
            it["pages"].append(p["index"])
            detail.append({
                "system": p["system"], "page": p["index"], "page_id": p["id"], "file": p.get("file_name", ""),
                "title": p["title"], "building": p["building"], "floor": p.get("floor_label", ""),
                "multiplier": mult, "material": mat, "unit": unit, "base": round(base, 2), "qty": round(q, 2),
                "source": src,
            })

    if st.get("round_pipe_6m"):
        for it in items.values():
            if it["material"].lower().startswith("ống thép") and it["qty"] > 0:
                it["qty"] = math.ceil(it["qty"] / 6.0) * 6.0

    systems = defaultdict(lambda: defaultdict(list))
    for (sysc, bld, _m, _u), it in items.items():
        it["qty"] = round(it["qty"], 2 if it["unit"] == "m" else 0)
        systems[sysc][bld].append(it)
    groups = []
    for n, sysc in enumerate(sorted(systems, key=lambda s: SYSTEM_ORDER.get(s, 99))):
        blds = []
        for bld in sorted(systems[sysc], key=_bkey):
            its = sorted(systems[sysc][bld], key=lambda i: (i["source"] != "Đếm", i["material"]))
            blds.append({"name": bld, "items": its})
        groups.append({"code": sysc, "roman": ROMAN[n] if n < len(ROMAN) else str(n + 1),
                       "name": SYSTEM_NAME.get(sysc, sysc), "buildings": blds})

    warnings = []
    for p in project.get("pages", []):
        if p.get("include"):
            for w in p.get("warnings", []):
                warnings.append({"type": "page", "page_id": p["id"], "where": f"{p.get('file_name', '')} · Trang {p['index']}: {p['title'][:70]}", "text": w})
    for d in dups:
        warnings.append({"type": "dup", "page_id": d["page_id"], "where": f"{d['file']} · Trang {d['page']}: {d['title'][:70]}",
                         "text": f"Đường nét lớp “{d['layer']}” ({d['length']:,.1f} m) trùng với trang {d['twin']} cùng tầng – chỉ tính 1 lần"})
    for key, n in sorted(unmapped.items(), key=lambda kv: -kv[1]):
        warnings.append({"type": "symbol", "key": key, "where": f"Ký hiệu “{key}”", "text": f"Chưa xác định là vật tư gì – {int(n)} cái đang chưa được tính"})

    detail.sort(key=lambda d: (SYSTEM_ORDER.get(d["system"], 99), d["file"], d["page"], d["material"]))
    return {
        "groups": groups,
        "detail": detail,
        "warnings": warnings,
        "stats": {
            "pages_used": pages_used,
            "pages_total": len(project.get("pages", [])),
            "items": len(items),
            "unmapped": len(unmapped),
            "warnings": len(warnings),
        },
    }

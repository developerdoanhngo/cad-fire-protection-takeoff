"""Chia bản vẽ thành từng trang theo khung tên, đọc tiêu đề, gợi ý trang nào tính / bỏ."""
import math
import re
from collections import Counter, defaultdict

from .catalog import norm

TITLE_KW = re.compile(r"MẶT BẰNG|SƠ ĐỒ|CHI TIẾT|MẶT CẮT|K[ÍÝ] HIỆU|THUYẾT MINH|DANH MỤC|THỐNG KÊ|TỔNG MẶT")

EXCLUDE_RULES = [
    (re.compile(r"SO VỚI KẾT CẤU"), "Trang đối chiếu kết cấu – trùng với mặt bằng chính"),
    (re.compile(r"KHÔNG GIAN|ISOMETRIC|\b3D\b"), "Sơ đồ không gian (3D) – trùng với mặt bằng"),
    (re.compile(r"CHỈ DẪN THOÁT NẠN"), "Sơ đồ chỉ dẫn thoát nạn – dùng lại thiết bị của mặt bằng"),
    (re.compile(r"NGUYÊN LÝ|THỦY LỰC|THUỶ LỰC|BIỂU ĐỒ"), "Sơ đồ nguyên lý / tính toán"),
    (re.compile(r"K[ÍÝ] HIỆU|GHI CHÚ CHUNG|THUYẾT MINH|DANH MỤC|THỐNG KÊ"), "Trang ký hiệu / ghi chú"),
    (re.compile(r"^CHI TIẾT|^MẶT CẮT"), "Trang chi tiết"),
]

BUILDINGS = [
    (re.compile(r"XỬ LÝ NƯỚC THẢI|XLNT"), "Nhà điều hành XLNT"),
    (re.compile(r"TRẠM BƠM|NHÀ BƠM|PHÒNG BƠM"), "Trạm bơm"),
    (re.compile(r"NHÀ BẢO VỆ"), "Nhà bảo vệ"),
    (re.compile(r"NHÀ (ĐỂ )?XE"), "Nhà để xe"),
    (re.compile(r"NHÀ XƯỞNG"), "Nhà xưởng"),
    (re.compile(r"NHÀ KHO"), "Nhà kho"),
    (re.compile(r"NHÀ VĂN PHÒNG"), "Nhà văn phòng"),
    (re.compile(r"TỔNG MẶT BẰNG|NGOÀI NHÀ"), "Ngoài nhà"),
]

FLOOR_RE = re.compile(r"TẦNG\s*(\d+|MÁI|HẦM|LỬNG|TUM)((?:\s*(?:,|&|VÀ|-|ĐẾN|\+)\s*(?:TẦNG\s*)?(?:\d+|MÁI|TUM))*)")
LEGEND_LAYER = re.compile(r"LEGEND|GHICHU|GHI CHU|CHUTHICH|CHU THICH")
HEAD_RE = re.compile(r"K[ÍÝI]\s*HI[ỆEÖ]U|CHÚ THÍCH|LEGEND")


def _inside(b, x, y):
    return b[0] <= x <= b[2] and b[1] <= y <= b[3]


def _title_of(texts):
    cands = [(h, s) for _x, _y, s, h in texts if TITLE_KW.search(s.upper()) and 8 <= len(s) <= 160]
    if not cands:
        big = sorted(((h, s) for _x, _y, s, h in texts if 10 <= len(s) <= 120), reverse=True)
        return big[0][1] if big else ""
    hmax = max(h for h, _s in cands)
    picked = []
    for h, s in sorted(cands, key=lambda c: -c[0]):
        if h >= 0.6 * hmax:
            s1 = re.sub(r"\s+", " ", s.replace("\n", " ")).strip()
            if s1.upper() not in (p.upper() for p in picked):
                picked.append(s1)
    return " + ".join(picked[:3])


def _buildings(title_u):
    found = []
    for rx, name in BUILDINGS:
        if rx.search(title_u) and name not in found:
            found.append(name)
    return " + ".join(found) if found else "Chung"


def _floors(title_u):
    out = []
    for m in FLOOR_RE.finditer(title_u):
        for tok in re.findall(r"\d+|MÁI|HẦM|LỬNG|TUM", m.group(0)):
            if tok not in out:
                out.append(tok)
    return out


def _floor_label(floors):
    if not floors:
        return ""
    return "Tầng " + ", ".join(f.capitalize() if not f.isdigit() else f for f in floors)


def _legend_flags(syms, texts, bbox):
    """Đánh dấu ký hiệu nằm trong bảng chú thích (legend) của trang."""
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]
    flags = [False] * len(syms)
    counts = Counter(k for k, *_ in syms)
    for i, (_k, _x, _y, layer) in enumerate(syms):
        if LEGEND_LAYER.search(norm(layer).upper()):
            flags[i] = True
    tol = w * 0.004
    # tiêu đề "KÝ HIỆU" (cả bảng mã Unicode lẫn TCVN3 cũ: 'kÝ hiÖu')
    heads = [(x, y) for x, y, s, _h in texts if HEAD_RE.search(s.upper()) and len(s) <= 40]
    rare = sorted((i for i, s in enumerate(syms) if counts[s[0]] <= 3 and not flags[i]), key=lambda i: syms[i][1])
    groups, cur = [], []
    for i in rare:
        if cur and syms[i][1] - syms[cur[-1]][1] > tol:
            groups.append(cur)
            cur = []
        cur.append(i)
    if cur:
        groups.append(cur)
    for g in groups:
        distinct = len({syms[i][0] for i in g})
        if len(g) < 3 or distinct < 3:
            continue
        xs = [syms[i][1] for i in g]
        ys = [syms[i][2] for i in g]
        xm = sum(xs) / len(xs)
        if max(ys) - min(ys) > 0.45 * h:
            continue
        head_y = [hy for hx, hy in heads if abs(hx - xm) <= 0.06 * w and 0 <= hy - max(ys) <= 0.10 * h]
        # cột ký hiệu "hiếm" thẳng hàng: có tiêu đề KÝ HIỆU phía trên, hoặc đủ nhiều loại khác nhau
        if not head_y and not (len(g) >= 4 and distinct >= 3):
            continue
        step = (max(ys) - min(ys)) / max(len(g) - 1, 1)
        y0, y1 = min(ys) - 1.5 * step, max(ys) + 2.5 * step
        if head_y:
            y1 = max(y1, max(head_y))
        for j, (_k, x, y, _l) in enumerate(syms):
            if abs(x - xm) <= tol and y0 <= y <= y1:
                flags[j] = True
    return flags


def build_pages(fd: dict, file_id: str, system: str, file_name: str):
    """Chia dữ liệu của 1 file thành các trang. Trả về (pages, geoms)."""
    frames = fd["frames"]
    if not frames:
        pts = [(x, y) for _k, x, y, _l in fd["inserts"]] + [(x, y) for _l, x, y, _L, _p in fd["linear"]]
        if not pts:
            return [], {}
        xs = [p[0] for p in pts]
        ys = [p[1] for p in pts]
        frames = [{"bbox": [min(xs), min(ys), max(xs), max(ys)], "scale": 1.0}]
    # thứ tự trang: từ trên xuống, trái sang phải
    hs = sorted(f["bbox"][3] - f["bbox"][1] for f in frames)
    hmed = hs[len(hs) // 2] or 1.0
    order = sorted(range(len(frames)), key=lambda i: (-round(((frames[i]["bbox"][1] + frames[i]["bbox"][3]) / 2) / hmed),
                                                         frames[i]["bbox"][0]))
    frames = [frames[i] for i in order]
    by_area = sorted(range(len(frames)), key=lambda i: (frames[i]["bbox"][2] - frames[i]["bbox"][0]) * (frames[i]["bbox"][3] - frames[i]["bbox"][1]))

    def which(x, y):
        for i in by_area:
            if _inside(frames[i]["bbox"], x, y):
                return i
        return -1

    p_syms = defaultdict(list)
    p_texts = defaultdict(list)
    p_lin = defaultdict(list)
    for k, x, y, layer in fd["inserts"]:
        i = which(x, y)
        if i >= 0:
            p_syms[i].append((k, x, y, layer))
    for x, y, s, h in fd["texts"]:
        i = which(x, y)
        if i >= 0:
            p_texts[i].append((x, y, s, h))
    for layer, x, y, L, pts in fd["linear"]:
        i = which(x, y)
        if i >= 0:
            p_lin[i].append((layer, L, pts))

    scales = Counter(f["scale"] for f in frames)
    main_scale = scales.most_common(1)[0][0] if scales else 1.0
    to_m = fd["to_m"]
    pages, geoms = [], {}
    for i, fr in enumerate(frames):
        pid = f"{file_id}-{i + 1:03d}"
        bb = fr["bbox"]
        title = _title_of(p_texts[i]) or f"Trang {i + 1}"
        tu = title.upper()
        syms = p_syms[i]
        flags = _legend_flags(syms, p_texts[i], bb)
        counts, legend = Counter(), Counter()
        for (k, *_r), f in zip(syms, flags):
            (legend if f else counts)[k] += 1
        lengths = defaultdict(float)
        for layer, L, _pts in p_lin[i]:
            lengths[layer] += L * to_m
        floors = _floors(tu)
        reason = None
        for rx, why in EXCLUDE_RULES:
            if rx.search(tu):
                reason = why
                break
        if reason is None and fr["scale"] and main_scale and fr["scale"] < 0.35 * main_scale and "MẶT BẰNG" not in tu:
            reason = "Trang chi tiết (vẽ phóng to)"
        if reason is None and not counts and not any(v > 0 for v in lengths.values()):
            reason = "Không có thiết bị"
        warnings = []
        if len(floors) > 1:
            warnings.append(f"Trang ghi nhiều tầng ({_floor_label(floors)}) – kiểm tra hệ số tầng")
        total = sum(counts.values())
        spr = sum(n for k, n in counts.items() if "phun" in norm(k))
        if re.search(r"VÁCH TƯỜNG|BÌNH CHỮA CHÁY|HỌNG", tu) and total >= 10 and spr >= 0.9 * total:
            warnings.append("Tiêu đề nói về vòi/bình chữa cháy nhưng trang chỉ có đầu phun – có thể tiêu đề ghi sai")
        pages.append({
            "id": pid, "file": file_id, "file_name": file_name, "system": system, "index": i + 1,
            "title": title, "building": _buildings(tu), "floors": floors, "floor_label": _floor_label(floors),
            "multiplier": 1, "include": reason is None, "auto_reason": reason, "warnings": warnings,
            "scale": fr["scale"], "counts": dict(counts), "legend": dict(legend),
            "lengths": {k: round(v, 3) for k, v in lengths.items() if v > 0},
        })
        # dữ liệu để vẽ trang (toạ độ tương đối, làm tròn)
        ox, oy = bb[0], bb[1]
        layers = sorted({layer for layer, _L, _p in p_lin[i]})
        li = {l: n for n, l in enumerate(layers)}
        polys = []
        for layer, _L, pts in p_lin[i]:
            flat = [li[layer]]
            for x, y in pts:
                flat.append(round(x - ox))
                flat.append(round(y - oy))
            polys.append(flat)
        geoms[pid] = {
            "w": round(bb[2] - bb[0]), "h": round(bb[3] - bb[1]), "layers": layers, "polys": polys,
            "syms": [[k, round(x - ox), round(y - oy), 1 if f else 0] for (k, x, y, _l), f in zip(syms, flags)],
        }

    _mark_duplicates(pages)
    return pages, geoms


def _mark_duplicates(pages):
    """Cảnh báo 2 trang cùng tầng có nội dung gần như giống hệt nhau."""
    inc = [p for p in pages if p["include"] and sum(p["counts"].values()) >= 30]
    for a_i, a in enumerate(inc):
        for b in inc[a_i + 1:]:
            if a["building"] != b["building"] or a["floors"] != b["floors"]:
                continue
            keys = set(a["counts"]) | set(b["counts"])
            dot = sum(a["counts"].get(k, 0) * b["counts"].get(k, 0) for k in keys)
            na = math.sqrt(sum(v * v for v in a["counts"].values()))
            nb = math.sqrt(sum(v * v for v in b["counts"].values()))
            if na and nb and dot / (na * nb) >= 0.98:
                b["warnings"].append(f"Nội dung gần giống trang {a['index']} ({a['title'][:50]}) – kiểm tra có phải trang trùng không")

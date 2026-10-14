"""Đọc file DXF: khung trang, chữ, ký hiệu (block) và các đường nét để đo chiều dài."""
import math
import re
from collections import Counter
from pathlib import Path

import ezdxf
from ezdxf import bbox as ezbbox
from ezdxf import path as ezpath
from ezdxf.lldxf.encoding import decode_dxf_unicode
from ezdxf.math import Vec3

FRAME_RE = re.compile(r"khung|title|frame|border|khungten", re.I)
LINEAR_TYPES = {"LINE", "LWPOLYLINE", "POLYLINE", "ARC", "SPLINE", "ELLIPSE"}
_CTRL = re.compile(r"%%[a-zA-Z]")
UNIT_TO_M = {0: 0.001, 1: 0.0254, 2: 0.3048, 4: 0.001, 5: 0.01, 6: 1.0}
FLAT_TOL = 25.0  # độ mịn khi xấp xỉ cung tròn (đơn vị bản vẽ)


def dec(s) -> str:
    if not s:
        return ""
    try:
        s = decode_dxf_unicode(s)
    except Exception:
        pass
    return _CTRL.sub("", s).strip()


def read_doc(path):
    try:
        return ezdxf.readfile(str(path))
    except Exception:
        from ezdxf import recover
        doc, _aud = recover.readfile(str(path))
        return doc


class BlockInfo:
    """Tra tên gốc của dynamic block và nhãn chữ hiển thị bên trong block."""

    def __init__(self, doc):
        self.doc = doc
        self._eff: dict[str, str] = {}
        self._lab: dict[str, str] = {}

    def eff(self, name: str) -> str:
        if name in self._eff:
            return self._eff[name]
        res = name
        if name.upper().startswith("*U"):
            try:
                br = self.doc.blocks.get(name).block_record
                xd = br.get_xdata("AcDbBlockRepBTag")
                h = [v for c, v in xd if c == 1005][0]
                res = self.doc.entitydb[h].dxf.name
            except Exception:
                pass
        res = dec(res) or name
        self._eff[name] = res
        return res

    def label(self, name: str) -> str:
        if name in self._lab:
            return self._lab[name]
        lab = ""
        blk = self.doc.blocks.get(name)
        if blk is not None:
            for e in blk:
                t = e.dxftype()
                if t == "MTEXT":
                    s = e.plain_text()
                elif t == "TEXT":
                    s = e.dxf.text
                else:
                    continue
                s = dec(s)
                if 0 < len(s) <= 12:
                    lab = s
                    break
        self._lab[name] = lab
        return lab


def _points(e):
    t = e.dxftype()
    if t == "LINE":
        s, en = e.dxf.start, e.dxf.end
        return [(s.x, s.y), (en.x, en.y)]
    if t == "LWPOLYLINE":
        ext = e.dxf.get("extrusion", (0, 0, 1))
        pts = list(e.get_points("xyb"))
        if tuple(ext) == (0, 0, 1) and not any(abs(p[2]) > 1e-9 for p in pts):
            out = [(p[0], p[1]) for p in pts]
            if e.closed and out:
                out.append(out[0])
            return out
    p = ezpath.make_path(e)
    return [(v.x, v.y) for v in p.flattening(FLAT_TOL)]


def _length(pts):
    return sum(math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in zip(pts, pts[1:]))


def _block_extents(doc, name, xref_lookup, xref_cache):
    blk = doc.blocks.get(name)
    if blk is None:
        return None
    be = blk.block
    if be is not None and be.is_xref:
        xp = (be.dxf.get("xref_path", "") or "").replace("\\", "/")
        stem = dec(Path(xp).stem).lower()
        dxf = xref_lookup.get(stem)
        if not dxf:
            return None
        if dxf not in xref_cache:
            try:
                xd = read_doc(dxf)
                xref_cache[dxf] = ezbbox.extents(xd.modelspace(), fast=True)
            except Exception:
                xref_cache[dxf] = None
        ext = xref_cache[dxf]
    else:
        ext = ezbbox.extents(blk, fast=True)
    if ext is None or not ext.has_data:
        return None
    return ext.extmin, ext.extmax


def find_frames(doc, msp, xref_lookup, xref_cache):
    counts = Counter(e.dxf.name for e in msp.query("INSERT"))
    cands = sorted((n for n in counts if FRAME_RE.search(dec(n))), key=lambda n: -counts[n])
    for name in cands:
        ext = _block_extents(doc, name, xref_lookup, xref_cache)
        if not ext:
            continue
        mn, mx = ext
        frames = []
        for e in msp.query("INSERT"):
            if e.dxf.name != name:
                continue
            m = e.matrix44()
            pts = [m.transform(Vec3(x, y, 0)) for x in (mn.x, mx.x) for y in (mn.y, mx.y)]
            xs = [p.x for p in pts]
            ys = [p.y for p in pts]
            frames.append({"bbox": [min(xs), min(ys), max(xs), max(ys)],
                           "scale": round(abs(e.dxf.get("xscale", 1.0)), 4)})
        if frames:
            return name, frames
    return None, []


def block_svg(doc, name: str) -> str:
    """Vẽ thử hình ký hiệu ra SVG nhỏ để người dùng nhận diện."""
    blk = doc.blocks.get(name)
    if blk is None:
        return ""
    strokes, fills, texts = [], [], []

    def walk(entities, depth):
        for e in entities:
            t = e.dxftype()
            try:
                if t == "INSERT":
                    if depth < 3:
                        walk(e.virtual_entities(), depth + 1)
                elif t == "HATCH":
                    for p in ezpath.from_hatch(e):
                        fills.append([(v.x, v.y) for v in p.flattening(0.5)])
                elif t in ("TEXT", "MTEXT"):
                    s = dec(e.plain_text() if t == "MTEXT" else e.dxf.text)
                    if s:
                        h = e.dxf.get("char_height", 0) if t == "MTEXT" else e.dxf.get("height", 0)
                        ins = e.dxf.insert
                        anchor = "start"
                        if t == "MTEXT":
                            ap = e.dxf.get("attachment_point", 1)
                            anchor = {1: "start", 2: "middle", 3: "end"}[(ap - 1) % 3 + 1]
                        texts.append((ins.x, ins.y, s[:16], h or 1.0, anchor, t == "MTEXT" and e.dxf.get("attachment_point", 1) in (4, 5, 6)))
                elif t in ("ATTDEF", "ATTRIB", "POINT", "DIMENSION"):
                    continue
                else:
                    p = ezpath.make_path(e)
                    pts = [(v.x, v.y) for v in p.flattening(0.5)]
                    if len(pts) >= 2:
                        strokes.append(pts)
            except Exception:
                continue

    walk(blk, 0)
    allp = [pt for poly in strokes + fills for pt in poly] + [(x, y) for x, y, *_ in texts]
    if not allp:
        return ""
    xs = [p[0] for p in allp]
    ys = [p[1] for p in allp]
    x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
    w = max(x1 - x0, 1e-6)
    h = max(y1 - y0, 1e-6)
    size = max(w, h)
    pad = size * 0.12
    vb = f"{x0 - pad - (size - w) / 2:.3f} {-(y1 + pad + (size - h) / 2):.3f} {size + 2 * pad:.3f} {size + 2 * pad:.3f}"

    def d(poly):
        return "M" + " L".join(f"{x:.2f},{-y:.2f}" for x, y in poly)

    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}">']
    for poly in fills[:60]:
        parts.append(f'<path d="{d(poly)}Z" fill="currentColor" fill-opacity=".85" stroke="none"/>')
    for poly in strokes[:400]:
        parts.append(f'<path d="{d(poly)}" fill="none" stroke="currentColor" stroke-width="1.6" vector-effect="non-scaling-stroke" stroke-linecap="round" stroke-linejoin="round"/>')
    for x, y, s, hgt, anchor, middle in texts[:6]:
        s = s.replace("&", "&amp;").replace("<", "&lt;")
        base = ' dominant-baseline="central"' if middle else ""
        parts.append(f'<text x="{x:.2f}" y="{-y:.2f}" font-size="{hgt:.2f}" text-anchor="{anchor}"{base} fill="#ed1844" font-weight="700" font-family="IBM Plex Sans,Segoe UI,sans-serif">{s}</text>')
    parts.append("</svg>")
    return "".join(parts)


def extract_file(dxf_path, xref_lookup, xref_cache, progress=None) -> dict:
    """Đọc 1 file DXF đã chuyển đổi. Trả về dữ liệu thô (chưa chia trang)."""
    doc = read_doc(dxf_path)
    msp = doc.modelspace()
    units = int(doc.header.get("$INSUNITS", 0) or 0)
    to_m = UNIT_TO_M.get(units, 0.001)
    info = BlockInfo(doc)
    frame_block, frames = find_frames(doc, msp, xref_lookup, xref_cache)
    xref_names = {b.name for b in doc.blocks if b.block is not None and b.block.is_xref}

    inserts, texts, linear = [], [], []
    keys: dict[str, dict] = {}
    entities = list(msp)
    total = max(len(entities), 1)
    for i, e in enumerate(entities):
        if progress and i % 4000 == 0:
            progress(i / total)
        t = e.dxftype()
        try:
            if t == "INSERT":
                name = e.dxf.name
                if name in xref_names or name == frame_block:
                    continue
                eff = info.eff(name)
                lab = info.label(name)
                key = f"{eff} | {lab}" if lab else eff
                p = e.dxf.insert
                inserts.append((key, p.x, p.y, e.dxf.layer))
                if key not in keys:
                    keys[key] = {"eff": eff, "label": lab, "raw": name}
            elif t in ("TEXT", "MTEXT"):
                s = dec(e.plain_text() if t == "MTEXT" else e.dxf.text)
                if s:
                    p = e.dxf.insert
                    h = e.dxf.get("char_height", 0) if t == "MTEXT" else e.dxf.get("height", 0)
                    texts.append((p.x, p.y, s, float(h or 0)))
            elif t in LINEAR_TYPES:
                pts = _points(e)
                if len(pts) < 2:
                    continue
                m = pts[len(pts) // 2]
                linear.append((e.dxf.layer, m[0], m[1], _length(pts), pts))
        except Exception:
            continue

    for k, v in keys.items():
        v["svg"] = block_svg(doc, v["raw"])

    return {
        "to_m": to_m,
        "frame_block": frame_block,
        "frames": frames,
        "inserts": inserts,
        "texts": texts,
        "linear": linear,
        "keys": keys,
    }

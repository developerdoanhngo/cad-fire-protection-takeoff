"""Chuyển DWG -> DXF bằng LibreDWG (miễn phí), kèm bước sửa lỗi định dạng."""
import glob
import os
import re
import shutil
import subprocess
from pathlib import Path

from .paths import libredwg_exe

_INT = re.compile(rb"^\s*-?\d+\s*$")
CREATE_NO_WINDOW = 0x08000000


class ConvertError(Exception):
    pass


def _find_oda() -> str | None:
    """ODA File Converter nếu người dùng tự cài (chỉ dùng làm phương án dự phòng)."""
    for base in (r"C:\Program Files\ODA", r"C:\Program Files (x86)\ODA"):
        hits = sorted(glob.glob(os.path.join(base, "*", "ODAFileConverter.exe")))
        if hits:
            return hits[-1]
    return None


def sanitize_dxf(src: Path, dst: Path) -> dict:
    """Sửa 2 lỗi đã gặp ở DXF do LibreDWG ghi ra:
    - giá trị MTEXT dài bị xuống dòng thô -> gộp lại vào giá trị trước;
    - nhóm '101 Embedded Object' của MTEXT -> bỏ (ezdxf không đọc được)."""
    data = src.read_bytes()
    lines = data.split(b"\n")
    pairs = []
    merged = 0
    i = 0
    n = len(lines)
    while i < n:
        code = lines[i].rstrip(b"\r")
        if not _INT.match(code):
            if pairs and code.strip():
                pairs[-1][1] += b"\\P" + code
                merged += 1
            i += 1
            continue
        if i + 1 >= n:
            break
        pairs.append([code, lines[i + 1].rstrip(b"\r")])
        i += 2
    out = []
    skip = False
    removed = 0
    for code, val in pairs:
        c = code.strip()
        if skip and c == b"0":
            skip = False
        if not skip and c == b"101" and val.strip() == b"Embedded Object":
            skip = True
            removed += 1
        if not skip:
            out.append(code)
            out.append(val)
    dst.write_bytes(b"\r\n".join(out) + b"\r\n")
    return {"merged_lines": merged, "removed_embedded": removed}


def convert_dwg(src: Path, work_dir: Path, tag: str) -> tuple[Path, dict]:
    """Trả về (đường dẫn DXF, thông tin). `tag` là tên ASCII an toàn."""
    work_dir.mkdir(parents=True, exist_ok=True)
    if src.suffix.lower() == ".dxf":
        return src, {"engine": "dxf"}
    # LibreDWG không mở được đường dẫn có dấu tiếng Việt -> chép sang tên ASCII
    tmp_in = work_dir / f"{tag}.dwg"
    raw = work_dir / f"{tag}.raw.dxf"
    out = work_dir / f"{tag}.dxf"
    shutil.copyfile(src, tmp_in)
    exe = libredwg_exe()
    info = {"engine": "libredwg"}
    ok = False
    if exe.exists():
        try:
            p = subprocess.run([str(exe), "-y", "-o", str(raw), str(tmp_in)],
                               capture_output=True, timeout=1800,
                               creationflags=CREATE_NO_WINDOW)
            log = (p.stdout + p.stderr).decode("utf-8", "replace")
            info["warnings"] = sum(1 for ln in log.splitlines() if "ERROR" in ln.upper())
            ok = p.returncode == 0 and raw.exists() and raw.stat().st_size > 1000
        except subprocess.TimeoutExpired:
            ok = False
    if ok:
        info.update(sanitize_dxf(raw, out))
        raw.unlink(missing_ok=True)
    else:
        oda = _find_oda()
        if not oda:
            raise ConvertError(f"Không chuyển được file {src.name} sang DXF.")
        oda_in = work_dir / f"{tag}_oda_in"
        oda_out = work_dir / f"{tag}_oda_out"
        oda_in.mkdir(exist_ok=True)
        oda_out.mkdir(exist_ok=True)
        shutil.copyfile(src, oda_in / f"{tag}.dwg")
        subprocess.run([oda, str(oda_in), str(oda_out), "ACAD2018", "DXF", "0", "1", "*.DWG"],
                       capture_output=True, timeout=1800, creationflags=CREATE_NO_WINDOW)
        res = oda_out / f"{tag}.dxf"
        if not res.exists():
            raise ConvertError(f"Không chuyển được file {src.name} sang DXF.")
        shutil.move(str(res), out)
        info["engine"] = "oda"
    tmp_in.unlink(missing_ok=True)
    return out, info

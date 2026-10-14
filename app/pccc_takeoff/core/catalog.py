"""Danh mục hệ thống, vật tư và quy tắc gợi ý ký hiệu -> vật tư (không dùng AI)."""
import re
import unicodedata

SYSTEMS = [
    ("CC", "Hệ thống chữa cháy"),
    ("BC", "Hệ thống báo cháy"),
    ("EX", "Hệ thống đèn sự cố và chỉ dẫn thoát nạn"),
    ("LOA", "Hệ thống loa thông báo"),
    ("HK", "Hệ thống hút khói"),
    ("TMB", "Tổng mặt bằng PCCC"),
    ("KHAC", "Hạng mục khác"),
]
SYSTEM_NAME = dict(SYSTEMS)
SYSTEM_ORDER = {code: i for i, (code, _n) in enumerate(SYSTEMS)}


def norm(s: str) -> str:
    """Bỏ dấu tiếng Việt, chữ thường."""
    s = (s or "").replace("đ", "d").replace("Đ", "D")
    s = unicodedata.normalize("NFD", s)
    s = "".join(ch for ch in s if unicodedata.category(ch) != "Mn")
    return s.lower()


def detect_system(filename: str) -> str:
    n = norm(filename).upper()
    tokens = set(re.split(r"[^A-Z0-9]+", n))
    flat = re.sub(r"[^A-Z0-9]", "", n)
    if "CC" in tokens or "CHUACHAY" in flat or "SPRINKLER" in flat:
        return "CC"
    if "BC" in tokens or "BAOCHAY" in flat or "FA" in tokens:
        return "BC"
    if "EX" in tokens or "EXIT" in tokens or "THOATNAN" in flat or "CHIEUSANG" in flat:
        return "EX"
    if "LOA" in tokens or "PA" in tokens:
        return "LOA"
    if "HK" in tokens or "HUTKHOI" in flat or "SMOKE" in flat:
        return "HK"
    if "TMB" in tokens or "BDX" in tokens or "TONGMATBANG" in flat:
        return "TMB"
    return "KHAC"


# Danh mục gợi ý cho ô chọn vật tư (người dùng vẫn gõ tên khác được)
CATALOG = {
    "CC": [
        ("Đầu phun sprinkler K8.0 quay lên", "cái"), ("Đầu phun sprinkler K8.0 quay xuống", "cái"),
        ("Đầu phun sprinkler K11.2 quay lên", "cái"), ("Đầu phun sprinkler K11.2 quay xuống", "cái"),
        ("Đầu phun sprinkler K5.6 quay lên", "cái"), ("Đầu phun sprinkler K5.6 quay xuống", "cái"),
        ("Van cổng OS&Y", "cái"), ("Van báo động (alarm valve)", "bộ"), ("Van một chiều", "cái"),
        ("Van xả khí", "cái"), ("Đồng hồ đo áp lực", "cái"), ("Công tắc dòng chảy", "cái"),
        ("Van góc chữa cháy", "cái"), ("Tủ / hộp chữa cháy", "hộp"), ("Bình chữa cháy xách tay", "bình"),
        ("Trụ chữa cháy", "trụ"), ("Họng tiếp nước", "cái"),
        ("Ống thép DN25", "m"), ("Ống thép DN32", "m"), ("Ống thép DN40", "m"), ("Ống thép DN50", "m"),
        ("Ống thép DN65", "m"), ("Ống thép DN80", "m"), ("Ống thép DN100", "m"), ("Ống thép DN150", "m"),
        ("Ống thép DN200", "m"), ("Ống thép DN250", "m"),
    ],
    "BC": [
        ("Đầu báo khói thường", "cái"), ("Đầu báo khói địa chỉ", "cái"), ("Đầu báo nhiệt thường", "cái"),
        ("Đầu báo nhiệt địa chỉ", "cái"), ("Nút ấn báo cháy", "cái"), ("Chuông báo cháy", "cái"),
        ("Đèn báo cháy", "cái"), ("Tổ hợp chuông, đèn, nút ấn", "bộ"), ("Đèn chỉ thị báo cháy (báo phòng)", "cái"),
        ("Module giám sát", "cái"), ("Module điều khiển", "cái"), ("Module đầu báo thường", "cái"),
        ("Điện trở cuối kênh", "cái"), ("Hộp kỹ thuật / hộp đấu nối", "hộp"), ("Tủ trung tâm báo cháy", "tủ"),
    ],
    "EX": [
        ("Đèn EXIT chỉ dẫn thoát nạn", "cái"), ("Đèn chiếu sáng sự cố", "cái"),
        ("Sơ đồ chỉ dẫn thoát nạn", "cái"), ("Biển / mũi tên chỉ hướng thoát nạn", "cái"),
        ("Aptomat", "cái"), ('Đèn "Trạm bơm chữa cháy"', "cái"),
    ],
    "LOA": [
        ("Loa thông báo", "cái"), ("Tủ điều khiển loa", "tủ"), ("Micro điều khiển từ xa", "bộ"),
    ],
    "HK": [
        ("Quạt hút khói", "cái"), ("Quạt cấp bù khí", "cái"), ("Van chặn lửa", "cái"),
        ("Van chặn lửa điều khiển bằng motor", "cái"), ("Miệng gió / cửa gió", "cái"),
        ("Cửa thu khói", "cái"), ("Tủ điện điều khiển quạt", "tủ"), ("Công tắc chọn chế độ", "cái"),
        ("Ống gió", "m"),
    ],
    "TMB": [
        ("Biển báo lối vào trên cao", "cái"), ("Bãi đỗ xe chữa cháy", "vị trí"), ("Biển bãi đỗ xe chữa cháy", "cái"),
    ],
}


def catalog_list():
    out = []
    for code, items in CATALOG.items():
        for name, unit in items:
            out.append({"system": code, "name": name, "unit": unit})
    return out


def _k(label: str, eff: str) -> str:
    m = re.search(r"(\d+[.,]\d+)", label or "")
    if not m:
        m = re.search(r"k\s*=?\s*(\d+[.,]\d+)", norm(eff))
    return f" K{m.group(1).replace(',', '.')}" if m else ""


IGNORE_RE = re.compile(
    r"^\d+$|archtick|ky ?hieu ?so|huong ?truc|mat ?cat|truc ?thong ?tang|_iso$|chi ?tiet|"
    r"^cot$|^nut$|bolt|^matcat|^xref|khung|title|^.{1,2}$|^qqq|^mbkc|^nha ?cu|sdcz$"
)

# (biểu thức trên tên đã bỏ dấu, tên vật tư, đơn vị) – thứ tự quan trọng
RULES = [
    (r"cut ?han ?d ?(\d+)|weld-?elb\d*-?dn ?(\d+)", "Cút thép hàn DN{1}", "cái"),
    (r"cut ?ren ?d ?(\d+)|screw-?elb\d*-?dn ?(\d+)", "Cút thép ren DN{1}", "cái"),
    (r"te ?han ?d ?(\d+)|weld-?tee-?dn ?(\d+)", "Tê thép hàn DN{1}", "cái"),
    (r"te ?ren ?d ?(\d+)|screw-?tee-?dn ?(\d+)", "Tê thép ren DN{1}", "cái"),
    (r"con ?thu ?han ?d ?(\d+) ?x ?(\d+)", "Côn thép hàn DN{1}/{2}", "cái"),
    (r"con ?ren ?d ?(\d+) ?x ?(\d+)", "Côn thép ren DN{1}/{2}", "cái"),
    (r"bich ?\w* ?d ?(\d+)", "Bích thép DN{1}", "cái"),
    (r"^gv-? ?(\d+)", "Van cổng DN{1}", "cái"),
    (r"^ch-? ?(\d+)", "Van một chiều DN{1}", "cái"),
    (r"^fjp-? ?(\d+)", "Khớp nối mềm DN{1}", "cái"),
    (r"bom ?truc ?dung|vertical ?pump", "Máy bơm chữa cháy trục đứng", "máy"),
    (r"bom ?bu ?ap|jockey", "Máy bơm bù áp", "máy"),
    (r"cong ?tac ?ap ?luc|pressure ?switch", "Công tắc áp lực", "cái"),
    (r"cam ?bien ?muc ?nuoc", "Cảm biến mực nước", "cái"),
    (r"pressure ?tank|binh ?tich ?ap", "Bình tích áp", "bình"),
    (r"nguon ?phu|power ?supply", "Bộ nguồn phụ 24V", "bộ"),
    (r"man ?hinh ?hien ?thi", "Màn hình hiển thị phụ báo cháy", "bộ"),
    (r"dung ?cu ?pha ?do", "Hộp dụng cụ phá dỡ thô sơ", "hộp"),
    (r"^support$|gia ?do ?ong", "Giá đỡ ống", "bộ"),
    (r"^co ?90|cut ?gio", "Phụ kiện ống gió – co 90°", "cái"),
    (r"con ?giam|con ?thu ?gio", "Phụ kiện ống gió – côn thu", "cái"),
    (r"con ?chuyen ?vuong ?tron", "Phụ kiện ống gió – côn chuyển vuông tròn", "cái"),
    (r"ong ?gio ?nep", "Phụ kiện ống gió – nẹp TDC", "cái"),
    (r"^duct", "Phụ kiện ống gió", "cái"),
    (r"dauphun.*quaylen|sprinkler.*(up|len)", "Đầu phun sprinkler{K} quay lên", "cái"),
    (r"dauphun.*quayxuong|sprinkler.*(pendent|down|xuong)", "Đầu phun sprinkler{K} quay xuống", "cái"),
    (r"dauphun|sprinkler", "Đầu phun sprinkler{K}", "cái"),
    (r"daubaokhoi.*diachi", "Đầu báo khói địa chỉ", "cái"),
    (r"daubaokhoi|smoke ?det", "Đầu báo khói thường", "cái"),
    (r"daubaonhiet.*diachi", "Đầu báo nhiệt địa chỉ", "cái"),
    (r"daubaonhiet|heat ?det", "Đầu báo nhiệt thường", "cái"),
    (r"chuong ?den ?nut ?an", "Tổ hợp chuông, đèn, nút ấn", "bộ"),
    (r"nut ?bam|nut ?an|manual ?call", "Nút ấn báo cháy", "cái"),
    (r"chuong ?bao ?chay|bell", "Chuông báo cháy", "cái"),
    (r"den ?bao ?phong", "Đèn chỉ thị báo cháy (báo phòng)", "cái"),
    (r"den ?bao ?chay", "Đèn báo cháy", "cái"),
    (r"module.*giam ?sat", "Module giám sát", "cái"),
    (r"module.*dieu ?khien", "Module điều khiển", "cái"),
    (r"module", "Module đầu báo thường", "cái"),
    (r"dien ?tro ?cuoi", "Điện trở cuối kênh", "cái"),
    (r"hop ?ky ?thuat|hop ?dau ?noi", "Hộp kỹ thuật / hộp đấu nối", "hộp"),
    (r"trung ?tam ?bao ?chay|fire ?alarm ?panel", "Tủ trung tâm báo cháy", "tủ"),
    (r"den ?exit|exit", "Đèn EXIT chỉ dẫn thoát nạn", "cái"),
    (r"den ?su ?co|emergency", "Đèn chiếu sáng sự cố", "cái"),
    (r"den ?tram ?bom", 'Đèn "Trạm bơm chữa cháy"', "cái"),
    (r"so ?do ?thoat ?nan|^sdtn", "Sơ đồ chỉ dẫn thoát nạn", "cái"),
    (r"mui ?ten.*thoat ?nan|mui ?ten ?chi ?huong", "Biển / mũi tên chỉ hướng thoát nạn", "cái"),
    (r"atomat|aptomat|mcb", "Aptomat", "cái"),
    (r"tu ?dieu ?khien ?loa|tu ?loa", "Tủ điều khiển loa", "tủ"),
    (r"remote ?micro|micro", "Micro điều khiển từ xa", "bộ"),
    (r"loa|speaker", "Loa thông báo", "cái"),
    (r"binh ?chua ?chay|extinguisher", "Bình chữa cháy xách tay", "bình"),
    (r"tu ?chua ?chay|hop ?chua ?chay|hose ?cabinet", "Tủ / hộp chữa cháy", "hộp"),
    (r"van ?xa ?khi", "Van xả khí", "cái"),
    (r"os&y|os ?y|van ?khoa ?os", "Van cổng OS&Y", "cái"),
    (r"van ?mot ?chieu|check ?valve", "Van một chiều", "cái"),
    (r"alarm ?van|van ?bao ?dong|alarm ?valve", "Van báo động (alarm valve)", "bộ"),
    (r"dong ?ho ?do ?ap|pressure ?gauge", "Đồng hồ đo áp lực", "cái"),
    (r"cong ?tac ?dong ?chay|flow ?switch", "Công tắc dòng chảy", "cái"),
    (r"van ?goc", "Van góc chữa cháy", "cái"),
    (r"tru ?chua ?chay|tru ?cc|hydrant", "Trụ chữa cháy", "trụ"),
    (r"hong ?tiep ?nuoc", "Họng tiếp nước", "cái"),
    (r"van ?chan ?lua ?dieu ?khien|motor ?damper", "Van chặn lửa điều khiển bằng motor", "cái"),
    (r"van ?chan ?lua|fire ?damper", "Van chặn lửa", "cái"),
    (r"cua ?thu ?khoi", "Cửa thu khói", "cái"),
    (r"mieng ?gio|cua ?gio|grille|louver|diffuser", "Miệng gió / cửa gió", "cái"),
    (r"(fan|quat).*(cap|supply|bu)", "Quạt cấp bù khí", "cái"),
    (r"fan|quat", "Quạt hút khói", "cái"),
    (r"selector|idec", "Công tắc chọn chế độ", "cái"),
    (r"tudien|tu ?dien", "Tủ điện điều khiển quạt", "tủ"),
    (r"loi ?vao ?tren ?cao", "Biển báo lối vào trên cao", "cái"),
    (r"bien ?bai ?do ?xe", "Biển bãi đỗ xe chữa cháy", "cái"),
    (r"bai ?do ?xe", "Bãi đỗ xe chữa cháy", "vị trí"),
]
_RULES = [(re.compile(p), name, unit) for p, name, unit in RULES]


def suggest_symbol(eff: str, label: str) -> dict | None:
    n = norm(eff)
    spaced = re.sub(r"(?<=[a-z])(?=[A-Z])", " ", eff or "")  # DauPhunQuayLen -> Dau Phun Quay Len
    n2 = norm(spaced)
    if IGNORE_RE.search(n.strip()):
        return {"material": "", "unit": "", "ignore": True}
    for rx, name, unit in _RULES:
        m = rx.search(n) or rx.search(n2)
        if m:
            nums = [g for g in m.groups() if g]
            out = name.replace("{K}", _k(label, eff))
            for i, g in enumerate(nums, start=1):
                out = out.replace("{%d}" % i, str(int(g)))
            return {"material": out, "unit": unit, "ignore": False}
    return None


def suggest_layer(layer: str) -> dict | None:
    n = norm(layer).upper()
    m = re.fullmatch(r"\s*DN\s*-?\s*(\d{2,3})\s*", n)
    if m:
        return {"material": f"Ống thép DN{int(m.group(1))}", "unit": "m", "factor": 1.0, "ignore": False}
    if re.search(r"DAY ?DIEN|DAYDIEN|CAP ?DIEN|CABLE|WIRE|DAY ?CAP|DAY ?TIN ?HIEU|DAY ?NGUON", n):
        tail = re.split(r"DAY ?DIEN[-_ ]*|DAYDIEN[-_ ]*", layer, flags=re.I)[-1] if re.search(r"DAY ?DIEN", n) else layer
        tail = tail.strip(" -_") or layer
        return {"material": f"Dây / cáp: {tail}", "unit": "m", "factor": 1.0, "ignore": False}
    if re.search(r"DUCT|ONG ?GIO|HVAC|CDFF", n):
        return {"material": "Ống gió", "unit": "m", "factor": 0.5, "ignore": False}
    return None

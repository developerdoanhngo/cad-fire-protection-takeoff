# Phần mềm bóc tách khối lượng PCCC từ bản vẽ CAD: đánh giá và kế hoạch

## Context
Khách hàng là nhà thầu PCCC (Sao Vàng Đại Việt), hiện bóc khối lượng thủ công từ bản vẽ để lập báo giá. Họ muốn có phần mềm đọc bản vẽ CAD, tự bóc khối lượng và ra báo giá. Input mẫu là dự án Youngone Bắc Giang: hồ sơ PCCC dạng DWG và PDF, cùng báo giá Excel ~42,08 tỷ (chưa VAT). Tài liệu này trả lời 3 câu hỏi: dự án có khả thi và hiệu quả không, triển khai theo flow nào, và input còn thiếu gì.

---

## 1. Input đã có: đã phân tích được gì

| File | Nội dung | Ghi chú |
|---|---|---|
| `1. HS PCCC_YOBG_20260907.rar` (197 MB) | 6 DWG theo hệ: `0.TMB+BDX` (tổng mặt bằng), `2.CC` (chữa cháy), `3.BC` (báo cháy), `4.EX` (đèn thoát nạn), `5.LOA` (loa), `6.HK` (hút khói). 9 file Xref: kiến trúc từng nhà (NX, NhaXe, NhaBom, NhaBaoVe, XLNT…), khung tên, dây chuyền công nghệ. Kèm PDF của từng hệ và 1 file `.bak` | **Đây là input chính.** Môi trường hiện tại chưa có `unrar` nên chưa xem được bên trong DWG (layer, block, attribute). Việc này làm đầu tiên ở Giai đoạn 0 |
| `1. Hồ sơ PCCC.pdf` (120 trang) | Bộ hồ sơ đầy đủ gồm mặt bằng, sơ đồ nguyên lý, chi tiết, ký hiệu và thuyết minh tính toán. Phân bổ: CC tr.2–49, BC tr.51–75, EX tr.77–98, Loa tr.100–108, HK tr.114–120 | PDF dạng vector, không phải scan. Tuy vậy nhãn DN và ký hiệu đã bị chuyển thành nét vẽ nên **gần như không trích được chữ**. Vì vậy PDF chỉ dùng để tham chiếu, không dùng làm nguồn tự động |
| `Báo giá youngone 05.10.xlsx` | 2 sheet: `Summary` và `Điều chỉnh theo KL lớn`. Khoảng 336 dòng, chia 6 hệ, mỗi hệ chia theo từng nhà (trạm bơm / ngoài nhà / nhà xưởng / nhà xe + phụ trợ / XLNT + bảo vệ) | Có link ngoài tới **`File ban đầu.xlsx` (sheet Detail)**, file này chưa được cung cấp |

**Quan sát quan trọng**
- **Bản vẽ được vẽ có chuẩn, rất thuận lợi cho tự động hoá.** Ống phân màu theo DN (DN25 đỏ, DN32 vàng, DN40 xanh lá, DN50 xanh dương, DN150 cam đậm) và có nhãn DN. Sprinkler là ký hiệu lặp lại, kèm nhãn hệ số K (`8.0` / `11.2`). Có trang "Kí hiệu chung" (legend) cho từng hệ.
- **Có rủi ro đếm trùng.** Trang 10–12 ("so với kết cấu") lặp lại trang 3–5. Trang 22–25 trùng tiêu đề với trang 15–18. Nếu đếm cả modelspace, kết quả sẽ bị nhân đôi, nên phần mềm phải có bước **chọn vùng tính**.
- **Cách lập báo giá hiện tại:**
  - Đơn giá = `giá gốc × hệ số (1,2–2,5) + nhân công`, ví dụ `=6800000*1.5+2000000`.
  - Chiều dài ống = `số cây × 6 m`, ví dụ `=844*6`.
  - Nhiều khối lượng cáp/ống luồn là số tròn (10.000 m, 20.000 m), tức là **ước lượng chứ không đo**.
  - Đã có sẵn các quy tắc định mức trong công thức, ví dụ cuộn vòi = số van góc × 2, lăng phun = số tủ.
- **Tỷ trọng giá trị báo giá theo loại khối lượng:**

  | Loại khối lượng | Tỷ trọng |
  |---|---|
  | Chiều dài (m): ống, cáp, ống gió | **63,7%** |
  | Đếm (cái/bộ) | 28,7% |
  | Trọn gói (lot) | 5,6% |
  | Diện tích (m²) | 1,4% |

  20 dòng lớn nhất chiếm ~55% giá trị, chủ yếu là ống DN150, ống gió, cáp chống cháy. **Đo chiều dài chính xác là tính năng mang lại giá trị lớn nhất.**

**Đối chiếu thử: số đếm từ chữ trong PDF so với báo giá**

| Hạng mục | Từ bản vẽ | Báo giá | Nhận xét |
|---|---|---|---|
| Đèn EXIT, nhà xưởng (tr.77–83) | 120 | 120 | Khớp tuyệt đối |
| Đèn EXIT, nhà xe/phụ trợ (tr.91–96) | 29 | 29 | Khớp tuyệt đối |
| Sprinkler K8.0, nhà xưởng (tr.3, 9, 20) | ~1.625 | 1.622 | Khớp (sai lệch ~0,2%) |
| Sprinkler K11.2, nhà xưởng (tr.4–8, 21) | ~3.199 | 3.480 | Báo giá cao hơn ~9%, cần giải thích |
| Sprinkler, nhà xe (tr.36–37) | ~894 | 1.040 | Báo giá cao hơn ~16%, cần giải thích |

Kết luận từ phép thử: khối lượng **suy ra được trực tiếp từ bản vẽ**, và phần mềm còn có giá trị **kiểm soát chênh lệch** giữa bản vẽ và báo giá. Với dự án này, sai 1% khối lượng tương đương ~420 triệu VNĐ.

---

## 2. Đánh giá khả thi và hiệu quả

**Kết luận: KHẢ THI CAO** cho mô hình *bóc tách bán tự động*. Phần mềm làm ~80–90% khối lượng, chuyên viên dự toán rà soát và bổ sung phần còn lại. Đây không phải mô hình "bấm một nút ra báo giá". Điều kiện để đạt mức này là bản vẽ theo chuẩn layer/block nhất quán, như bộ bản vẽ mẫu.

| Nhóm hạng mục | Cách phần mềm xử lý | Mức khả thi |
|---|---|---|
| Thiết bị dạng ký hiệu: sprinkler, đầu báo, nút ấn, chuông/đèn, đèn EXIT/sự cố, loa, bình chữa cháy, tủ chữa cháy, van, module | Đếm block (theo tên/attribute) trong từng vùng tầng/nhà | **Cao** (95–100%) |
| Ống thép theo DN trên mặt bằng | Đo tổng chiều dài polyline/line, gán DN theo layer, màu hoặc nhãn DN gần nhất | **Cao** (±3–5%) |
| Ống gió theo kích thước | Đo tuyến và gán kích thước theo nhãn (1000x400…) | Trung bình – Cao |
| Phụ kiện: tê, cút, côn, măng sông, bích | Dựng mạng ống (graph): tê ở chỗ rẽ nhánh, cút ở chỗ đổi hướng, côn ở chỗ đổi DN, cộng thêm quy tắc theo từng đầu phun | Trung bình, cần hiệu chỉnh theo dự án thật |
| Giá treo, ty ren, nở/kẹp, sơn ống (m²) | Quy tắc định mức: khoảng cách treo theo DN; diện tích sơn = π·D·L | Trung bình, cần bộ định mức của công ty |
| Ống đứng, ống nhánh lên/xuống đầu phun | Theo cao độ tầng/trần cộng chiều dài chuẩn mỗi đầu phun (chi tiết tr.49) | Trung bình |
| Cáp tín hiệu/động lực, ống luồn | Đo tuyến nếu có vẽ, cộng đoạn lên xuống và hệ số hao hụt (1,2–1,3) | Trung bình – Thấp, tuỳ mức độ vẽ |
| Thiết bị trạm bơm, tủ điện, máy phát, FM-200 | Lấy từ sơ đồ nguyên lý hoặc nhập tay theo mẫu | Thấp, giữ nhập tay |
| Vật tư phụ, an toàn lao động, vận chuyển, kiểm định | Nhập tay hoặc tính theo % | Không cần tự động |

**Hiệu quả kỳ vọng** (ước tính, cần đo lại khi pilot)
- **Thời gian:** bóc tách một dự án cỡ này (120 bản vẽ, ~5.000 đầu phun) thủ công mất khoảng vài ngày đến 1–2 tuần công. Với phần mềm, đếm và đo xong trong vài phút, rà soát mất 0,5–1,5 ngày, tức **giảm 60–80% thời gian**.
- **Độ chính xác:** loại bỏ lỗi đếm sót, đếm trùng và cộng nhầm. Mọi con số đều truy vết được về đối tượng trên bản vẽ (có bảng diễn giải theo tầng).
- **Tốc độ đấu thầu:** khi bản vẽ sửa đổi, chạy lại và có ngay danh sách chênh lệch giữa hai phiên bản.
- **Chuẩn hoá tri thức:** định mức và đơn giá nằm trong hệ thống, không còn phụ thuộc vào cá nhân.

**Rủi ro chính và cách giảm**
1. **Bản vẽ do đơn vị khác vẽ, sai chuẩn, hoặc ký hiệu đã bị explode thành nét rời.** Giảm bằng màn hình mapping lưu thành profile. Giai đoạn sau bổ sung nhận dạng hình học cho ký hiệu đã explode.
2. **Đếm trùng do có nhiều bản sao cùng một tầng.** Giảm bằng bước chọn vùng tính theo khung bản vẽ.
3. **Đọc DWG.** Giảm bằng cách dùng ODA File Converter (miễn phí) để chuyển DWG sang DXF. Nếu thương mại hoá rộng thì cân nhắc ODA Drawings SDK (có phí membership).
4. **Quy tắc phụ kiện và định mức là riêng của từng công ty.** Thiết kế rule engine cấu hình được, không hard-code.

---

## 3. Phần mềm hoạt động như thế nào (flow người dùng)

```
 [DWG + Xref]
   │ 1. Upload và chuyển đổi: DWG → DXF, ghép Xref, đọc layout/khung tên
   ▼
 2. Phân vùng: nhận khung bản vẽ và tiêu đề → gán Nhà/Tầng/Hệ
   │   Người dùng tick vùng cần tính, bỏ vùng trùng ("so với kết cấu"…)
   ▼
 3. Trích xuất: block (thiết bị) · polyline/line (ống, cáp, ống gió) · text (DN, K, kích thước)
   ▼
 4. Mapping: layer/block/màu → mã vật tư chuẩn (gợi ý tự động, lưu profile dùng lại)
   ▼
 5. Tính khối lượng
   │   đếm · đo dài (gán DN) · mạng ống → tê/cút/côn
   │   quy tắc định mức → giá treo, ty ren, sơn, vòi + lăng theo tủ, ống đứng theo cao độ, hao hụt
   ▼
 6. Rà soát: viewer tô màu đối tượng đã tính / chưa map, sửa tay, ghi chú
   ▼
 7. Áp giá: kho đơn giá (giá gốc × hệ số + nhân công, xuất xứ, quy cách)
   ▼
 8. Xuất: Excel báo giá theo mẫu công ty (song ngữ, giữ công thức)
          + bảng diễn giải khối lượng theo tầng
          + DXF có đánh dấu để kiểm tra trên AutoCAD
          + so sánh phiên bản bản vẽ
```

**Kiến trúc đề xuất**
- **Engine:** Python, gồm `ezdxf` để đọc DXF, `shapely` cho hình học và phân vùng, `networkx` để dựng mạng ống và suy ra phụ kiện.
- **Chuyển đổi DWG:** ODA File Converter chạy phía server.
- **Ứng dụng:** web app với backend FastAPI và PostgreSQL (dự án, mapping profile, kho giá, định mức). Frontend React kèm viewer 2D (dxf-viewer/three.js hoặc SVG) để tô sáng đối tượng.
- **Xuất Excel:** `openpyxl`, giữ công thức để khách vẫn chỉnh được như hiện nay.
- **Phương án thay thế:** plugin AutoCAD (.NET), chạy và tô sáng ngay trong AutoCAD. Phù hợp nếu khách chỉ dùng nội bộ, nhưng phụ thuộc phiên bản AutoCAD và khó làm thành sản phẩm.

---

## 4. Kế hoạch triển khai theo giai đoạn

| Giai đoạn | Nội dung | Thời gian | Đầu ra và tiêu chí nghiệm thu |
|---|---|---|---|
| **0. Khảo sát và chuẩn hoá** | Giải nén RAR, phân tích DWG (layer, block, attribute, text, xref, layout). Phỏng vấn chuyên viên dự toán về quy trình và định mức. Chốt danh mục vật tư chuẩn (mã, tên song ngữ, đơn vị). Chốt chuẩn CAD | 1–2 tuần | Báo cáo cấu trúc DWG; danh mục vật tư; bộ quy tắc định mức v1 |
| **1. PoC** | Script đọc DXF dự án Youngone: đếm thiết bị theo nhà/tầng, đo ống theo DN, rồi đối chiếu với báo giá và file gốc | 2–3 tuần | Đếm đúng ≥98% so với đếm lại thủ công; chiều dài ống sai ≤5%; danh sách chênh lệch có giải thích |
| **2. MVP bóc tách** | Web app chạy bước 1→6 và xuất Excel khối lượng. Gồm rule engine (phụ kiện, giá treo, sơn, hao hụt), mapping profile, viewer rà soát | 8–10 tuần | Chạy trọn dự án Youngone và thêm 2 dự án khác, chuyên viên dự toán xác nhận |
| **3. Báo giá** | Kho đơn giá (giá gốc, hệ số, nhân công, xuất xứ), mẫu báo giá công ty, sheet Summary, quản lý phiên bản | 3–4 tuần | Xuất được báo giá đúng định dạng file hiện tại |
| **4. Pilot** | Dùng thật song song với cách làm cũ trên 3–5 dự án mới, đo thời gian và sai lệch | 4–6 tuần (chạy song song) | Số liệu tiết kiệm thời gian thật; danh sách lỗi và yêu cầu |
| **5. Nâng cao** (tuỳ chọn) | So sánh phiên bản bản vẽ, nhận dạng ký hiệu đã explode, ống đứng từ mặt cắt/3D, AI gợi ý mapping, plugin AutoCAD, đa người dùng/phân quyền | Theo nhu cầu | |

**Nhân sự:** 1 BA/chuyên gia PCCC (nên là chuyên viên dự toán của khách), 1–2 dev Python mảng hình học CAD, 1 dev frontend, QA bán thời gian. **Thời gian đến bản dùng được (hết giai đoạn 3):** khoảng 4–5 tháng.

---

## 5. Input còn thiếu

| # | Input cần thêm | Vì sao cần | Mức độ |
|---|---|---|---|
| 1 | **`File ban đầu.xlsx`** (sheet Detail mà báo giá đang link tới) và bảng diễn giải khối lượng gốc, nếu có | Làm "đáp án chuẩn" cho PoC. Giải thích vì sao sheet tên "Điều chỉnh theo KL lớn" lệch so với bản vẽ | **Bắt buộc** |
| 2 | **Bộ quy tắc và định mức bóc tách của công ty**: hao hụt (1,2 / 1,3), khoảng cách giá treo theo DN, quy tắc phụ kiện cho mỗi đầu phun hoặc nhánh, chiều dài ống nhánh xuống đầu phun, cao độ tầng/trần, cách tính cáp, cách tính vật tư phụ | Không có thì phần mềm chỉ đếm và đo được, không ra đủ được ~40% số dòng còn lại | **Bắt buộc** |
| 3 | **Danh mục vật tư và kho đơn giá**: giá gốc, ý nghĩa hệ số ×1,5 / ×1,2 / ×2,5, đơn giá nhân công, xuất xứ | Cho giai đoạn báo giá | **Bắt buộc** (từ giai đoạn 3) |
| 4 | **Ai vẽ bản vẽ** (công ty tự vẽ hay nhận từ tư vấn ngoài) và **chuẩn layer/block** đang dùng | Quyết định mức tự động hoá cho các dự án khác ngoài dự án mẫu | **Bắt buộc** |
| 5 | **2–4 dự án mẫu khác** (DWG kèm báo giá/quyết toán cuối), khác loại công trình (xưởng, văn phòng, kho…), lý tưởng là có cả bản vẽ của đơn vị khác | Kiểm chứng phần mềm không chỉ chạy đúng với một dự án | **Cao** |
| 6 | Phiên bản AutoCAD/DWG đang dùng; ai là người dùng (chuyên viên dự toán hay kỹ sư thiết kế); muốn web, desktop hay plugin AutoCAD; số người dùng | Chốt kiến trúc và chi phí license | **Cao** |
| 7 | Quy trình và baseline hiện tại: bao lâu cho một dự án, mấy người, bao nhiêu dự án mỗi tháng | Đo ROI và đặt mục tiêu | Trung bình |
| 8 | Mẫu báo giá chuẩn (bản trống) và quy tắc nhóm hạng mục (Hệ → Nhà → Hạng mục) | File hiện có đã đáp ứng phần lớn, chỉ cần xác nhận | Trung bình |
| 9 | Có cần xuất sang phần mềm dự toán theo định mức nhà nước (mã hiệu công tác, ví dụ G8/Eta/F1) không | Phạm vi tính năng xuất | Trung bình |
| 10 | Bản vẽ thi công và hoàn công/quyết toán thực tế của dự án cũ | Hiệu chỉnh quy tắc phụ kiện và hao hụt cho sát thực tế | Thấp (có thì tốt) |
| 11 | Báo giá nhà cung cấp, lịch sử giá | Cập nhật kho giá | Thấp |

---

## 6. Việc làm ngay khi plan được duyệt (bước đầu của Giai đoạn 0 và 1)

1. **Cài công cụ giải nén** (`unrar` hoặc `7z`) và giải nén RAR vào thư mục riêng `data/raw/` (không chạy file nào bên trong).
2. **Chuyển DWG sang DXF** bằng ODA File Converter, hoặc nhờ khách "Save As DXF" từ AutoCAD.
3. **Viết script phân tích** `tools/inspect_dxf.py`, dùng `ezdxf` liệt kê:
   - layer và số đối tượng trên từng layer;
   - block và số lần chèn;
   - attribute;
   - text chứa "DN", "K=", kích thước ống gió;
   - xref và layout/khung tên.
4. **Viết script PoC** `tools/poc_takeoff.py`:
   - xác định vùng theo khung tên;
   - đếm block theo vùng;
   - đo chiều dài ống theo DN;
   - xuất Excel đối chiếu với `Báo giá youngone 05.10.xlsx`.
5. **Viết báo cáo PoC:** bảng khớp/lệch theo từng dòng báo giá, danh sách quy tắc còn thiếu và câu hỏi gửi khách.

**Cách kiểm chứng**
- So số đếm của script với số đếm từ PDF đã làm ở trên (EXIT 120/29, K8.0 ~1.625, K11.2 ~3.199).
- Đếm tay ngẫu nhiên 2–3 tầng trên AutoCAD.
- So chiều dài ống DN với báo giá (`844*6`…) và giải thích từng chênh lệch lớn hơn 5%.

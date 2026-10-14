# Phần mềm bóc tách khối lượng PCCC từ bản vẽ CAD: đánh giá và kế hoạch

> **Phiên bản 2, ngày 13/10/2026.** Bản này thay cho bản đầu (12/10).
> Khác biệt chính: bản đầu chỉ dựa trên file PDF (như xem ảnh chụp bản vẽ). Bản này đã mở được **file bản vẽ gốc (DWG)** và chạy thử, nên các con số là số đo thật.

## Bối cảnh

- **Có 3 bên:**
  - Chúng ta: làm phần mềm.
  - Khách hàng: công ty lắp đặt hệ thống phòng cháy chữa cháy (PCCC).
  - Khách của họ: chủ đầu tư, ví dụ Youngone.
- **"Bóc khối lượng"** là việc nhìn bản vẽ rồi đếm, đo xem công trình cần bao nhiêu thứ: bao nhiêu đầu phun nước, bao nhiêu mét ống, bao nhiêu mét dây điện… Hiện khách làm việc này bằng tay để lập báo giá.
- **Phần mềm** sẽ đọc file bản vẽ CAD, tự đếm và tự đo, rồi ra bảng khối lượng (có thể ra luôn báo giá, xem mục B3).
- **Input mẫu** là bộ hồ sơ dự án Youngone Bắc Giang:
  - 6 file bản vẽ, mỗi file một hệ: tổng mặt bằng, chữa cháy, báo cháy, đèn thoát nạn, loa, hút khói.
  - 9 file bản vẽ nền (thư mục Xref): kiến trúc từng nhà và khung tên.
  - Bản PDF của các bản vẽ trên.
- **File Excel `Báo giá youngone 05.10.xlsx`** là báo giá công ty PCCC gửi cho Youngone, tức là **kết quả bóc tay của một dự án đã làm xong**. Ta chỉ dùng file này vào 2 việc:
  - làm "đáp án" để chấm xem phần mềm đếm đúng không;
  - làm mẫu hình thức cho file đầu ra.

  Ta **không đánh giá báo giá đó đúng hay sai**, vì đó là việc giữa họ và khách của họ.

## Kết luận nhanh

| Câu hỏi | Trả lời |
|---|---|
| Làm được không? | **Được**, theo kiểu **bán tự động**: máy làm phần nặng (đếm, đo), người chọn trang cần tính và xem lại |
| Được phần nào? | Khoảng **2/3 khối lượng công việc**. Phần còn lại là thiết bị lớn và chi phí trọn gói, người nhập tay nhưng nhanh |
| Chính xác bao nhiêu? | Đếm thiết bị: **98–100%** (đã thử). Đo ống: **~95%** (ước tính, chưa thử) |
| Giúp khách bao nhiêu? | Giảm khoảng **60–80% thời gian** bóc khối lượng (ước tính, cần đo khi dùng thử) |
| Một lần bóc mất bao lâu? | Máy chạy vài phút; tính cả người xem lại khoảng **1 ngày** cho dự án cỡ Youngone |
| Làm phần mềm bao lâu (AI viết code)? | Bản chạy thử **~1 tuần**, bản dùng thật **~2–3 tháng** |
| Có mất tiền không? | Chuyển file và các thư viện lập trình đều **miễn phí**. Chi phí chính là thuê máy chủ (vài trăm nghìn đến ~1 triệu/tháng) |
| Đủ input chưa? | **Đủ** để làm và test bản chạy thử. **Chưa đủ** để làm bản dùng thật (xem mục A12) |

---

# PHẦN A. KỸ THUẬT

## A1. Kết quả chạy thử trên bộ Youngone

**Đã làm:**
- chuyển 15 file bản vẽ sang dạng đọc được;
- chia bản vẽ thành từng trang theo khung tên;
- đọc tiêu đề từng trang (ví dụ "MẶT BẰNG … TẦNG 2 – NHÀ XƯỞNG");
- đếm ký hiệu thiết bị theo từng trang.

**So số máy đếm với số người đếm tay** (lấy từ file Excel):

| Hạng mục (nhà xưởng) | Máy đếm | Người đếm | Chênh lệch |
|---|---|---|---|
| Đầu phun K8.0 quay lên | 1.206 | 1.205 | ~0% |
| Đầu phun K11.2 quay lên | 2.778 | 2.773 | 0,2% |
| Đầu phun K8.0 quay xuống | 420 | 417 | 0,7% |
| Đầu phun K11.2 quay xuống | 715 | 707 | 1,1% |
| **Cộng đầu phun** | **5.119** | **5.102** | **0,3%** |
| Loa | 61 | 60 | 1 cái (nhiều khả năng là ký hiệu trong bảng chú thích) |
| Đèn EXIT | 144–158 | 120 | **Chưa rõ lý do, cần tìm hiểu** |
| Chiều dài ống | chưa thử | | Phải lọc các trang vẽ trùng trước |

*K8.0 và K11.2 là 2 loại đầu phun, khác nhau ở lưu lượng nước. Số máy đếm vẫn còn lẫn vài ký hiệu nằm trong bảng chú thích ở góc mỗi trang, chưa được loại ra.*

## A2. Phần mềm làm được phần nào, chính xác bao nhiêu

Tỷ trọng giá trị dưới đây tính theo cơ cấu một dự án mẫu (Youngone):

| Nhóm việc | Ví dụ | Độ chính xác | Tỷ trọng giá trị |
|---|---|---|---|
| **1. Máy tự đếm, tự đo** | Đầu phun, đầu báo khói, đèn, loa, bình và tủ chữa cháy, van; chiều dài ống nước | Đếm 98–100%; ống ~95% | ~44% |
| **2. Máy đo, người xem lại** | Dây điện của hệ báo cháy, đèn, loa; ống gió; quạt hút khói | ~90% | ~14% |
| **3. Máy tính theo quy tắc** | Khớp nối ống (co, tê), giá treo, sơn ống, cuộn vòi | 80–90%, tùy quy tắc khách đưa | ~8% |
| **4. Người nhập tay** | Máy bơm, máy phát, tủ điện, dây điện hệ hút khói, phí vận chuyển và kiểm định | Máy không làm | ~34% |

**Máy làm được bao nhiêu, theo từng hệ thống:**

| Hệ | Máy làm được | Ghi chú |
|---|---|---|
| Chữa cháy (hệ lớn nhất) | ~85% | |
| Báo cháy | ~90% | Dây điện được vẽ đủ và tách riêng theo loại dây, nên đo được |
| Đèn thoát nạn | ~90% | Như trên |
| Loa | ~60% | |
| **Hút khói** | **~30%** | Yếu nhất: phần lớn là tủ điện, máy phát và dây điện, vốn không có trên bản vẽ |

## A3. Những "bẫy" trong bản vẽ mà phần mềm phải xử lý

1. **Một thiết bị được vẽ lặp lại ở nhiều trang:**
   - trang mặt bằng chính;
   - trang "so với kết cấu";
   - sơ đồ 3D (sơ đồ không gian);
   - bảng chú thích ký hiệu ở góc mỗi trang;
   - sơ đồ chỉ dẫn thoát nạn.

   Nếu cộng hết thì **ra gấp đôi**. Ví dụ ống DN150 (đường kính 150 mm): cộng hết được 23,9 km, trong khi người bóc tay ra khoảng 11,2 km.
2. **Tên ký hiệu khác với chữ hiện ra trên bản vẽ.** Ký hiệu đặt tên "K11.2" nhưng chữ hiện ra là "8.0", và người bóc tay đếm theo chữ hiện ra. → Không được tin tên gọi, phải đọc cả chữ hiện ra.
3. **Tiêu đề trang có khi ghi sai.** 4 trang có tiêu đề "VÁCH TƯỜNG + BÌNH CHỮA CHÁY TẦNG 3–6" nhưng thực ra chỉ chứa đầu phun nằm dưới ống gió. → Không chỉ dựa vào tiêu đề, phải xem cả nội dung trang.
4. **Một trang vẽ dùng chung cho nhiều tầng.** Ví dụ trang "TẦNG 1, 2 NHÀ XE". → Cần cho người dùng nhập số tầng áp dụng.
5. **Ký hiệu "động" và ký hiệu tên vô nghĩa.**
   - Ký hiệu "động": một ký hiệu có nhiều biến thể. Ví dụ ký hiệu đèn EXIT có khoảng 15 biến thể.
   - Ký hiệu tên vô nghĩa do máy tự sinh, như `A$C6DE14615`.
6. **Các trang chi tiết được phóng to**, tức là vẽ theo tỷ lệ khác. → Không đo chiều dài ở những trang này.
7. **Hệ hút khói vẽ kém chuẩn nhất:**
   - có vẻ nhiều đơn vị khác nhau cùng vẽ, cách đặt tên lộn xộn;
   - ống gió vẽ bằng 2 nét viền, máy phải tự tìm đường giữa để đo;
   - dây điện gần như không được vẽ.

**Cách xử lý chung** (đây là lý do phần mềm là bán tự động):
- Người dùng tick chọn trang cần tính. Máy gợi ý sẵn những trang nên bỏ.
- Người dùng xác nhận ký hiệu trong lần đầu tiên.
- Máy cảnh báo khi nội dung trang không khớp với tiêu đề.

## A4. Giải pháp kỹ thuật

1. **Tải lên:** người dùng tải cả thư mục bản vẽ (file `.dwg` kèm thư mục Xref), hoặc 1 file zip.
2. **Chuyển file:** máy chủ tự chuyển DWG sang DXF bằng công cụ miễn phí LibreDWG (xem A6).
3. **Chia trang:** máy chia bản vẽ theo khung tên, đọc tiêu đề, gợi ý trang nào tính và trang nào bỏ. Người dùng tick xác nhận.
4. **Xác nhận ký hiệu:** máy liệt kê các loại ký hiệu tìm thấy, kèm hình, số lượng, chữ hiện ra và vật tư gợi ý. Người dùng xác nhận.
5. **Tính khối lượng:**
   - đếm thiết bị;
   - đo ống và dây theo từng loại;
   - tính phụ kiện, giá treo, hao hụt theo quy tắc của công ty.
6. **Xem lại:** bản vẽ được tô màu ở những chỗ đã tính. Người dùng có thể sửa tay.
7. **Xuất kết quả:** file Excel (xem A9).

**Máy "nhớ" bằng cách nào? Không cần AI.**
- Máy lưu một **bảng tra cứu** trong cơ sở dữ liệu, giống danh bạ điện thoại. Ví dụ: "ký hiệu `DauPhunQuayLen`, chữ hiện ra 11.2 = Đầu phun K11.2 quay lên".
- Lần sau gặp lại đúng ký hiệu đó, máy tự điền. Người dùng chỉ phải xác nhận những ký hiệu mới.
- Máy tra theo **cả tên lẫn chữ hiện ra**. Nếu cùng một tên mà chữ hiện ra khác đi, máy hỏi lại chứ không tự đoán.
- Lớp vẽ (ví dụ `DN150` = ống DN150) và quy tắc chọn trang (ví dụ bỏ trang "SƠ ĐỒ KHÔNG GIAN") cũng được nhớ theo cách tương tự.

**AI là tùy chọn, có thể thêm sau:**
- Nhận dạng ký hiệu theo hình dáng, khi bản vẽ của đơn vị khác đặt tên vô nghĩa hoặc ký hiệu đã bị phá thành nét rời.
- Đọc bản vẽ PDF hoặc bản scan.

Bản đầu tiên không cần AI. Không dùng AI còn có lợi là không tốn phí theo lượt dùng, và kết quả luôn giống nhau mỗi lần chạy.

## A5. Bộ công nghệ

| Phần | Công nghệ | Ghi chú |
|---|---|---|
| Máy chủ | **Linux (Ubuntu)**, thuê VPS hoặc cloud | Rẻ hơn Windows, phổ biến nhất cho web |
| Đóng gói | **Docker** | Chạy giống hệt nhau ở mọi nơi: máy chủ thuê, máy chủ của khách, máy lập trình |
| Chuyển DWG sang DXF | **LibreDWG** | Miễn phí. Vốn là phần mềm làm cho Linux |
| Xử lý bản vẽ | **Python** + ezdxf, shapely, networkx | Đây là phần đã chạy thử |
| Phần nhận yêu cầu từ trình duyệt | **FastAPI** (Python) | |
| Cơ sở dữ liệu | **PostgreSQL** | Lưu dự án, bảng ký hiệu đã "dạy", quy tắc tính |
| Giao diện | **React** + dxf-viewer | Chạy trong trình duyệt, người dùng dùng Windows hay Mac đều được |
| Xuất Excel | **openpyxl** | Giữ công thức để khách vẫn sửa tay được |

- **Không cần Windows ở bất kỳ chỗ nào.** Người dùng cũng không cần cài AutoCAD để dùng phần mềm.
- Trường hợp duy nhất buộc phải dùng Windows là làm plugin chạy bên trong AutoCAD. **Không chọn phương án này**, vì nó phụ thuộc phiên bản AutoCAD và khó bán rộng.
- Tất cả thành phần đều miễn phí và được dùng thương mại. Riêng LibreDWG có lưu ý về giấy phép, xem A6.

## A6. Tự động chuyển DWG sang DXF bằng giải pháp miễn phí

File AutoCAD (`.dwg`) là định dạng đóng của hãng Autodesk, nên phải đổi sang định dạng mở (`.dxf`) thì phần mềm mới đọc được. Việc này **chạy tự động trên máy chủ**, người dùng không phải làm gì.

| Giải pháp | Miễn phí? | Dùng trong sản phẩm bán được không? | Kết quả chạy thử |
|---|---|---|---|
| ODA File Converter | Tải về miễn phí | **Không.** Người không phải thành viên ODA chỉ được dùng cho mục đích phi thương mại. Gói thương mại: $3.000 năm đầu, $2.250 các năm sau (dưới 100 bản/năm). Gói cho web: $7.500 năm đầu, $4.500 các năm sau | Tốt cả 15 file (dùng làm chuẩn để so) |
| **LibreDWG** (dự án GNU, mã nguồn mở) | **Có** | **Được**, khi chạy trên máy chủ của mình (giấy phép GPLv3) | Chuyển được cả 15 file, **số liệu giống hệt ODA** |
| Thư viện Python | — | — | Không có thư viện miễn phí nào đọc thẳng được DWG |

**Kết quả thử LibreDWG (bản 0.14):**
- **Tốc độ:** chuyển cả 15 file mất ~15 giây; file lớn nhất (13,6 MB) mất 8 giây.
- **So với ODA trên 6 bản vẽ chính:** số ký hiệu, chiều dài ống, chiều dài dây, số dòng chữ, tiêu đề tiếng Việt và nhãn "8.0 / 11.2" trong ký hiệu đều **giống 100%**.
- **Gặp 2 lỗi, cả 2 đã xử lý được:**
  1. **Không mở được file nằm trong thư mục có dấu tiếng Việt.** Cách xử lý: máy chủ đổi tên file sang không dấu khi nhận.
  2. **Ở bản vẽ báo cháy, 17 dòng ghi chú dài bị ghi sai định dạng**, làm bước đọc file bị lỗi. Cách xử lý: thêm một bước tự sửa file (khoảng 25 dòng code). Sau bước đó, kết quả giống hệt ODA.

**Rủi ro:**
- **Mới thử 1 bộ bản vẽ.** Bộ khác có thể gặp lỗi khác.
- **LibreDWG báo nhiều cảnh báo** về các thành phần phụ khi đọc. Với bộ này thì không ảnh hưởng số liệu. Dự án được cập nhật gần như hằng ngày, tức là đang được bảo trì tích cực nhưng vẫn còn đang hoàn thiện.
- **Giấy phép GPLv3:**
  - Chạy trên máy chủ của mình thì không phải công bố mã nguồn phần mềm của mình.
  - Nếu đóng gói thành phần mềm cài vào máy khách thì phải kèm mã nguồn của LibreDWG.
  - **Nên hỏi luật sư trước khi bán rộng.**

**Đề xuất:**
- Dùng LibreDWG làm mặc định.
- Thiết kế để có thể thay bằng ODA khi cần.
- Sau mỗi lần chuyển đổi, phần mềm tự kiểm tra. Nếu có dấu hiệu lỗi nặng thì cảnh báo người dùng, không âm thầm cho ra số sai.

**Còn phải thử:** chạy LibreDWG trong môi trường Linux (dùng Docker) để xác nhận kết quả vẫn giống ODA. Phần thử ở trên mới làm trên Windows.

## A7. Dung lượng file DWG và việc tải lên

**Dung lượng file DWG thường gặp** (ước lượng theo kinh nghiệm chung, không phải số thống kê):

| Mức | Mỗi file | Ví dụ |
|---|---|---|
| Nhẹ | Dưới 5 MB | Nhà xưởng nhỏ, văn phòng vài tầng |
| Trung bình | 5–30 MB | **Youngone** (file lớn nhất 13,6 MB, cả bộ 30 MB) |
| Nặng | 30–100 MB | Cao ốc, trung tâm thương mại, bệnh viện, nhiều tòa trong một file |
| Rất nặng | 100–300 MB trở lên | File chèn ảnh/PDF, có mô hình 3D, bản đồ địa hình |

File thường nặng vì chèn ảnh, có mô hình 3D, gộp luôn bản vẽ nền vào file, có nhiều bản sao của cùng một mặt bằng, hoặc còn nhiều rác chưa dọn.

**Chỉ cần tải lên file bản vẽ, không cần cả bộ hồ sơ:**
- Cần tải: 15 file `.dwg`, gồm cả thư mục Xref (30 MB, nén zip còn 24 MB). Mất khoảng 5–20 giây.
- **Bắt buộc phải có thư mục Xref**, vì khung tên của từng trang nằm trong đó.
- Không cần tải: PDF (228 MB), file RAR gốc (197 MB), file `.bak`.

**Bộ nhớ máy chủ cần dùng** (đo thật trên file 13,6 MB):

| Cách đọc | RAM | Thời gian | File 100 MB (ước tính) |
|---|---|---|---|
| Đọc thường (nạp cả file vào bộ nhớ) | 720 MB | ~15 giây | ~5 GB RAM ⚠️ |
| **Đọc cuốn chiếu** (đọc lần lượt từng phần) | **170 MB** | 12,5 giây | Vài trăm MB đến ~1 GB |

Đọc cuốn chiếu cho kết quả đếm **giống hệt** đọc thường. → Thiết kế đọc cuốn chiếu ngay từ đầu thì **máy chủ 8 GB RAM xử lý được file vài trăm MB**.

**Những việc cần làm thêm:**
- Cho phép tải lên tới khoảng 500 MB mỗi dự án.
- Cho phép tải tiếp khi rớt mạng.
- File trung gian (khoảng 8 lần file gốc, ~235 MB với bộ Youngone) xóa ngay sau khi xử lý, chỉ giữ lại kết quả.

**Rủi ro đáng lo hơn dung lượng là file xuất từ Revit** (phần mềm thiết kế 3D). Loại file này thường có tên ký hiệu tự sinh, dài, có khi mỗi ký hiệu một tên khác nhau, nên khó "nhớ" theo tên. Bộ Youngone đã có một dấu vết kiểu này: `Pressure tank 200 lit - …-2474845-NỀN NHÀ XE`. → Cần xin khách ít nhất 1 bộ bản vẽ xuất từ Revit để thử.

## A8. Triển khai: máy chủ thuê hay cài tại công ty khách

Nhờ đóng gói bằng Docker, cùng một phần mềm chạy được theo cả 2 cách:

| Cách | Bản vẽ nằm ở đâu | Ưu điểm | Nhược điểm |
|---|---|---|---|
| Máy chủ thuê (cloud) | Máy chủ của mình | Cập nhật một lần là mọi khách đều có; dễ bán cho nhiều khách | Khách phải chấp nhận gửi bản vẽ ra ngoài |
| Cài trong công ty khách | Máy chủ hoặc máy tính của họ (máy Windows có Docker Desktop cũng được) | Bản vẽ không ra khỏi công ty | Mỗi lần cập nhật phải cài lại ở từng nơi |

→ Cần hỏi khách: **họ có chấp nhận tải bản vẽ lên máy chủ bên ngoài không?**

## A9. Đầu ra (output)

**1. File Excel khối lượng, gồm 5 sheet:**
- **Tổng hợp:** chia theo Hệ → Tòa nhà → Hạng mục, ghi đơn vị, khối lượng và cách ra số (máy đếm / máy đo / quy tắc / nhập tay).
- **Chi tiết theo tầng:** mỗi con số lấy từ trang nào, tầng nào.
- **Diễn giải cách tính.** Ví dụ: "Ống DN150 tầng 1 = 1.120 m đo được × 1,05 hao hụt"; "Cuộn vòi = 76 van góc × 2".
- **Cần kiểm tra:** những chỗ máy không chắc, ví dụ tiêu đề trang có thể ghi sai, ký hiệu chưa biết là gì, trang dùng chung cho nhiều tầng.
- **Nhập tay:** danh sách hạng mục máy không làm, để sẵn ô trống cho người điền.

**2. Bản vẽ tô màu**, xem trên web và tải về được dạng PDF:
- xanh: đã tính;
- đỏ: máy chưa biết là gì;
- xám: trang bị bỏ qua.

Bấm vào một con số trong bảng thì bản vẽ nhảy tới đúng vị trí đó.

**3. So sánh khi bản vẽ được sửa**, ví dụ: "Tầng 3: đầu phun K11.2 +12 cái, ống DN50 −35 m".

**4. File báo giá theo mẫu của khách**, nếu khách chọn Mức 2 (xem B3).

## A10. Một lần bóc tách mất bao lâu

| Việc | Thời gian |
|---|---|
| Tải lên, chuyển file, đếm, đo | Vài phút |
| Tick chọn trang (bộ Youngone khoảng 127 trang; máy gợi ý sẵn những trang nên bỏ) | 15–30 phút |
| Xác nhận ký hiệu (chỉ lần đầu với một kiểu bản vẽ mới) | 30–60 phút |
| Xem lại kết quả và nhập tay nhóm 4 | Nửa ngày đến 1 ngày |
| **Tổng** | **Khoảng 1 ngày** |

Làm tay ước tính mất vài ngày đến 1–2 tuần, **cần hỏi khách con số thật**.

## A11. Thời gian làm phần mềm (AI viết code)

| Giai đoạn | Thời gian | Kết quả |
|---|---|---|
| Bản chạy thử | ~1 tuần | Chạy trên bộ Youngone, xuất Excel khối lượng theo tầng, so với số người đếm |
| Bản dùng được | Thêm 3–4 tuần | Giao diện web đầy đủ các bước ở A4, có quy tắc tính phụ kiện |
| Thử với bản vẽ khác, sửa lỗi | Thêm 2–3 tuần | Chạy đúng với 2–4 bộ bản vẽ khác |
| Khách dùng thử thật | Thêm 2–4 tuần | Đo được thời gian tiết kiệm thật |
| **Tổng** | **~2–3 tháng** | Bản đầu của plan tính cho đội người viết code là 4–5 tháng |
| *(Tùy chọn)* Mức 2: ra báo giá | Thêm 3–4 tuần | Bảng giá, xuất file báo giá theo mẫu |

- AI viết code nhanh. Thứ làm chậm tiến độ là **chờ khách gửi tài liệu và kiểm tra kết quả**.
- Vẫn cần một người điều khiển AI, kiểm tra kết quả và làm việc với khách.

## A12. Input: đã đủ chưa

- **Để làm và test bản chạy thử: ĐỦ.** Đã có bộ bản vẽ đầy đủ 6 hệ, file gốc mở được, và có số người đếm để so.
- **Để làm bản dùng thật: CHƯA.** Cần xin thêm:

| # | Cần thêm | Để làm gì | Khi nào cần |
|---|---|---|---|
| 1 | Chốt phạm vi: chỉ đếm và đo (Mức 1), hay ra luôn báo giá (Mức 2) | Quyết định có làm phần tính tiền không | Ngay |
| 2 | Bảng bóc tay chi tiết theo tầng của 1–2 dự án | Làm "đáp án" để chấm phần mềm, nhất là chiều dài ống. Hiện chỉ có số tổng theo tòa nhà | Ngay |
| 3 | Có chấp nhận tải bản vẽ lên máy chủ bên ngoài không | Chọn cách triển khai (A8) | Ngay |
| 4 | 2–4 bộ bản vẽ dự án khác: có bộ do đơn vị khác vẽ, có ít nhất 1 bộ xuất từ Revit | Chắc chắn phần mềm không chỉ chạy đúng với 1 bộ | Trước khi làm bản dùng thật |
| 5 | Quy tắc tính phụ kiện (tê, cút), giá treo, hao hụt, dây điện hệ hút khói | Để máy làm được nhóm 3 (một số quy tắc đã lấy được từ file Excel, xem B4) | Tuần 2–3 |
| 6 | Hiện tại bóc tay 1 dự án mất bao lâu, cần mấy người, mỗi tháng làm bao nhiêu dự án | Đo hiệu quả thật | Trước khi dùng thử |
| 7 | Nếu chọn Mức 2: bảng đơn giá vật tư, nhân công, hệ số; mẫu báo giá trống | Làm phần báo giá | Khi làm Mức 2 |
| 8 | Một chuyên viên bóc khối lượng của khách dành thời gian kiểm tra kết quả | Xác nhận phần mềm đúng | Khi dùng thử |

---

# PHẦN B. NGHIỆP VỤ VÀ KINH DOANH

## B1. Phần mềm thay đổi quy trình của khách thế nào

File Excel báo giá của khách có sẵn vì dự án Youngone **đã bóc tay xong**. Với mỗi dự án mới, khách nhận bản vẽ và phải nộp báo giá trong vài ngày. Lúc đó **chưa có file Excel nào cả**, và việc bóc tách tốn nhiều ngày chính là thứ phần mềm làm thay.

| Bước | Hiện tại | Có phần mềm |
|---|---|---|
| 1 | Nhận bản vẽ | Nhận bản vẽ |
| 2 | Đếm tay hàng nghìn ký hiệu, đo tay từng đoạn ống và dây (**vài ngày đến 1–2 tuần**) | Tải bản vẽ lên, máy đếm và đo, người xem lại (**khoảng 1 ngày**) |
| 3 | Gõ số vào cột "Khối lượng" của file báo giá | Mức 1: chép số sang. Mức 2: phần mềm xuất ra luôn file báo giá |
| 4 | Điền đơn giá, ra thành tiền | (như trên) |

Ngay trong file Excel đã thấy dấu vết làm tay. Ví dụ khối lượng dây điện trạm bơm là `=(18+26+2+2)*1.2*2`: người làm đo tay từng đoạn 18 m, 26 m, 2 m, 2 m rồi nhân hệ số.

## B2. Giúp khách được bao nhiêu

- **Thời gian giảm khoảng 60–80%.** Phần tốn công nhất là đếm hàng nghìn ký hiệu và đo hàng km ống, đó đúng là phần máy làm. Nhóm 4 chiếm 1/3 giá trị nhưng chỉ là vài chục thiết bị lớn, nhập nhanh.
- **Bớt sai sót.** Không còn đếm sót, đếm trùng hay cộng nhầm. Con số nào cũng chỉ ra được nằm ở đâu trên bản vẽ.
- **Khi bản vẽ được sửa,** chỉ cần chạy lại vài phút, có ngay danh sách thay đổi.
- **Quy mô tiền:** với dự án cỡ 40 tỷ, sai 1% khối lượng tương đương khoảng 400 triệu.
- **Hạn chế:** với hệ hút khói, phần mềm chỉ giúp được khoảng 30%.

## B3. Phạm vi: cần khách chốt

| Mức | Phần mềm làm gì | Thêm thời gian | Cần khách đưa |
|---|---|---|---|
| **Mức 1: bảng khối lượng** | Điền cột "Khối lượng". Khách tự nhân với đơn giá như hiện nay | — | — |
| **Mức 2: ra luôn báo giá** | Xuất nguyên file báo giá theo mẫu, có đơn giá và thành tiền | 3–4 tuần | Bảng giá vật tư, nhân công, hệ số; mẫu báo giá. Sau này khách tự cập nhật giá |

**Đề xuất làm Mức 1 trước** để khách thấy hiệu quả nhanh. Mức 2 tính sau.

## B4. Dùng lại file báo giá Excel làm mẫu đầu ra

**Dùng lại được hình thức trình bày:** các cột, mô tả song ngữ, cách nhóm Hệ → Tòa nhà → Hạng mục.

**Nhưng không dùng nguyên file làm khuôn rồi điền số vào được**, vì 5 vấn đề sau. Đây là vấn đề cấu trúc file, không phải nhận xét về số liệu:

1. **File gắn chặt với dự án Youngone.** Các nhóm tòa nhà và số dòng là riêng của dự án này. Dự án sau sẽ khác, nên phần mềm phải tự tạo dòng.
2. **Đơn giá của dòng này lấy từ dòng khác.** 68 ô đơn giá trỏ sang dòng khác, trong đó 12 dòng thuộc các hệ khác lấy giá từ mục "Trạm bơm". Dự án nào không có trạm bơm, hoặc chỉ cần thêm bớt dòng, là các ô này báo lỗi hoặc lấy nhầm giá.
3. **Giá nằm rải rác trong công thức.** 122 ô đơn giá gõ số trực tiếp, ví dụ `=183000000*1.5+3500000`. Không có bảng giá chung.
4. **Có liên kết tới file "File ban đầu.xlsx"**, file này không có ở đây. Đó là ô tổng mục VI ở sheet Summary. Mở trên máy khác, Excel sẽ hỏi cập nhật liên kết hoặc báo lỗi.
5. **23 công thức cộng tổng dùng vùng cố định**, kiểu `=SUM(G7:G60)`. Khi số dòng thay đổi, phần mềm phải tự viết lại.

**Tin tốt: file có sẵn một số quy tắc tính của khách**, nằm trong công thức, lấy ra dùng được ngay:

| Quy tắc | Công thức trong file |
|---|---|
| Cuộn vòi = số van góc × 2 | `=E103*2` |
| Lăng phun = số hộp chữa cháy | `=E102` |
| Nối mềm chống rung = 2 × số quạt | `=2*SUM(...)` |
| Lò xo giảm chấn = 4 × số quạt (riêng 1 loại quạt ly tâm là 6) | `=4*SUM(...)+6*E284` |
| Ống luồn dây = 0,9 × chiều dài dây | `=E17*0.9` |
| Chiều dài ống = số cây × 6 m | `=844*6` |

Số lượng tê, cút, giá treo trong file là số gõ tay, không có công thức, nên quy tắc cho các phần này vẫn phải hỏi khách.

**Đề xuất:** dựng một **mẫu mới** giữ nguyên hình thức file của khách, gồm:
- sheet danh mục vật tư và bảng giá, mỗi vật tư một mã riêng;
- sheet chi tiết do phần mềm tự tạo dòng, đơn giá tra theo mã vật tư;
- vẫn giữ công thức Excel để khách sửa tay được;
- không có liên kết sang file khác.

## B5. Thương mại hóa được không

- **Có tiềm năng.** Công ty PCCC nào cũng phải bóc khối lượng khi đấu thầu. Các công cụ nước ngoài chủ yếu bắt người tự bấm chọn trên PDF, và không theo cách gọi tên vật tư cũng như mẫu biểu của Việt Nam.
- **Nhưng chưa chứng minh được.** Mới thử 1 bộ bản vẽ, và bộ này vẽ khá gọn gàng. Mỗi công ty vẽ một kiểu, tính phụ kiện một kiểu, nên phần mềm phải có chức năng "dạy ký hiệu" và "cài quy tắc" cho từng công ty.
- **Đề xuất các bước:**
  1. Làm cho khách này trước.
  2. Thử thêm 2–4 bộ bản vẽ của đơn vị khác, có cả file xuất từ Revit.
  3. Nếu máy vẫn làm được khoảng 2/3 công việc thì mới tính chuyện bán rộng.

## B6. Chi phí

| Khoản | Chi phí |
|---|---|
| Các thư viện lập trình (đọc bản vẽ, tính hình học, xuất Excel, web) | Miễn phí, được phép dùng thương mại |
| Chuyển DWG sang DXF bằng LibreDWG | **Miễn phí** |
| *(Chỉ khi LibreDWG không đáp ứng)* Gói ODA | $3.000 năm đầu, $2.250/năm sau (phần mềm cài máy). $7.500 năm đầu, $4.500/năm sau (web) |
| Máy chủ thuê để chạy web | Vài trăm nghìn đến ~1 triệu đồng/tháng |
| AI viết code | Phí thuê bao AI hằng tháng trong thời gian làm |
| Tư vấn luật về giấy phép GPLv3 | Một lần, trước khi bán rộng |

---

## Việc làm tiếp theo

1. **Thử LibreDWG trên Linux** (Docker), xác nhận kết quả vẫn giống ODA.
2. **Gửi khách các câu hỏi ở mục A12**, ưu tiên mục 1–3.
3. **Viết bản chạy thử:**
   - chuyển file;
   - chia trang và lọc trang trùng;
   - xác nhận ký hiệu;
   - đếm, đo ống theo cỡ;
   - xuất Excel khối lượng theo tầng;
   - so với số người đếm.
4. **Tìm nguyên nhân chênh lệch đèn EXIT** (máy 144–158, người đếm 120).

---

## Phụ lục: ghi chú kỹ thuật cho người lập trình

**Bộ file Youngone:**
- 6 DWG chính: `0.TMB+BDX`, `2.CC`, `3.BC`, `4.EX`, `5.LOA`, `6.HK`.
- 9 Xref: `NX`, `NhaXe`, `NhaBom`, `NhaBaoVe`, `NhaXuLyNuocThai`, `TMB`, `HKSC`, `Day chuyen cong nghe`, `khung ten`.
- Định dạng: AC1032 (2018), AC1021 (2007); riêng `2.CC` là AC1018 (2004). File `.bak` có nội dung giống hệt `.dwg`.
- PDF trong RAR: 127 trang = 3 TMB + 49 CC + 27 BC + 24 EX + 11 Loa + 13 HK. File `1. Hồ sơ PCCC.pdf` ở thư mục gốc là bản 120 trang.

**Chia trang:**
- Khung bản vẽ là các insert của xref `Xref_khung ten` đặt trong modelspace. Bao khung = extents của `Xref_khung ten.dxf` × ma trận insert.
- Tiêu đề là TEXT/MTEXT nằm trong khung.
- Tỷ lệ khung khác nhau (0,527 / 1,492 / 0,048…): các khung tỷ lệ nhỏ là trang chi tiết.

**Ký hiệu:**
- Thiết bị là block có tên, nằm trên các layer `F_ChuaChay_*`, `F-BAO CHAY-*`, `F_DenThoatNan_*`, `F_ThietBi_LoaThongBao`.
- Ống nằm trên các layer `DN25`…`DN250`.
- Dây báo cháy nằm trên layer đặt theo quy cách dây, ví dụ `F-BAOCHAY-DAYDIEN-TINHIEU-2X0.75MM`.
- Dynamic block (`*U###`): lấy tên gốc qua xdata `AcDbBlockRepBTag` (mã 1005 → handle của block record gốc).
- Nhãn K nằm trong MTEXT bên trong định nghĩa block, và mâu thuẫn với tên block: `DauPhunQuayLenK11.2` hiển thị "8.0", `DauPhunQuayLen` hiển thị "11.2".

**Nguồn trùng cần loại:**
- trang "SO VỚI KẾT CẤU";
- "SƠ ĐỒ KHÔNG GIAN" (block có hậu tố `_ISO`, ống vẽ theo hình chiếu iso);
- "SƠ ĐỒ CHỈ DẪN THOÁT NẠN (ĐIỂN HÌNH)";
- ký hiệu chú thích (legend) trong từng khung;
- các khung "CHI TIẾT", "SƠ ĐỒ NGUYÊN LÝ".

**LibreDWG 0.14 (`dwg2dxf`) trên Windows:**
- Không mở được đường dẫn non-ASCII.
- Với `3.BC`, một số MTEXT dài bị xuống dòng thô trong giá trị, cùng nhóm `101 Embedded Object`, khiến ezdxf báo lỗi. Cách sửa: gộp dòng lẻ vào giá trị trước đó và bỏ khối `101 Embedded Object`. Sau đó kết quả trùng ODA.
- Chữ tiếng Việt được ghi dạng `\U+XXXX`. Giải mã bằng `ezdxf.lldxf.encoding.decode_dxf_unicode`.

**Hiệu năng** (file `2.CC`: 13,6 MB DWG → 132–143 MB DXF, 64.455 entity trong modelspace):

| Bước | Thời gian | RAM |
|---|---|---|
| Chuyển đổi (LibreDWG) | 8,2 giây | |
| `ezdxf.readfile` | 13–15 giây | 720 MB |
| `ezdxf.addons.iterdxf` (đọc cuốn chiếu) | 12,5 giây | 170 MB |

**Nguồn tham khảo:**
- [ODA File Converter: điều kiện sử dụng](https://www.opendesign.com/node/3218)
- [Bảng giá thành viên ODA](https://www.opendesign.com/pricing.md)
- [LibreDWG (GPLv3)](https://github.com/LibreDWG/libredwg)
- [LibreDWG 0.14](https://github.com/LibreDWG/libredwg/releases/tag/0.14)

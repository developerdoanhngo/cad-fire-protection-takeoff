# Hướng dẫn sử dụng DCS PCCC Takeoff (phiên bản 1.0.3)

Phần mềm desktop đọc bộ bản vẽ CAD (DWG) của hệ thống phòng cháy chữa cháy, tự đếm thiết bị, đo chiều dài ống và dây, rồi xuất bảng khối lượng ra Excel.

## 1. Cài đặt và mở phần mềm
- Chép thư mục `DCS PCCC Takeoff` (hoặc giải nén file `DCS-PCCC-Takeoff-1.0.3-win64.zip`) vào máy.
- Chạy file **`DCS PCCC Takeoff.exe`**.
- Yêu cầu máy: Windows 10/11 có Microsoft Edge WebView2. Các máy Windows 10/11 được cập nhật đều có sẵn thành phần này.
- Không cần cài AutoCAD. Bản vẽ được xử lý ngay trên máy, không gửi đi đâu.

## 2. Bố cục màn hình
- **Menu trái** là phần chung của phần mềm, gồm:
  - nút **Tạo dự án mới**;
  - **Dự án**: danh sách tất cả dự án;
  - **Thư viện ký hiệu**;
  - **Giới thiệu**.
- **Màn hình dự án** là phần riêng của từng dự án:
  - Thanh trên cùng ghi **← Dự án › Tên dự án**. Bấm "← Dự án" để quay về danh sách.
  - Bên dưới là **3 bước của dự án**: Trang bản vẽ → Ký hiệu & vật tư → Kết quả.
- **Quản lý nhiều dự án:** mỗi dự án là một thẻ trong mục **Dự án**, dự án sửa gần nhất xếp lên đầu. Bấm thẻ để mở; rê chuột lên thẻ sẽ hiện nút xoá. Dự án đang mở có nhãn **"Đang mở"**.

## 3. Tạo dự án
1. Bấm **Tạo dự án mới** và nhập tên dự án.
2. Chọn bộ bản vẽ:
   - Bấm **Chọn thư mục**, rồi chọn thư mục chứa các file `.dwg`.
   - Nên chọn cả thư mục để phần mềm lấy luôn thư mục **Xref** (khung tên, bản vẽ nền). Thiếu Xref thì phần mềm không chia được trang.
   - **Chưa có bản vẽ?** Có thể bấm **Tạo dự án, thêm bản vẽ sau**. Khi mở dự án, phần mềm sẽ hiện nút **Chọn thư mục bản vẽ** để thêm sau.
3. Kiểm tra danh sách file. Phần mềm tự nhận ra hệ thống của từng file (chữa cháy, báo cháy, đèn thoát nạn, loa, hút khói…) theo tên file.
4. Bấm **Bắt đầu xử lý**. Bộ bản vẽ cỡ trung bình mất khoảng 1–2 phút.
5. **Khi có bản vẽ sửa đổi:** trong dự án, bấm **Cập nhật bản vẽ** để chọn bộ bản vẽ mới.
   - Phần mềm sẽ xử lý lại toàn bộ.
   - Ký hiệu đã xác nhận vẫn được giữ, vì đã lưu trong thư viện.
   - Việc chọn trang và hệ số tầng sẽ được tính lại từ đầu.

## 4. Bước 1: Trang bản vẽ
- Danh sách bên trái là các trang bản vẽ, chia theo khung tên. Công tắc bật nghĩa là trang đó **được tính**.
- Phần mềm tự **bỏ** những trang sẽ gây đếm trùng, kèm lý do:
  - trang "so với kết cấu";
  - sơ đồ không gian (3D);
  - sơ đồ chỉ dẫn thoát nạn;
  - sơ đồ nguyên lý;
  - trang ký hiệu, ghi chú, chi tiết.
- Bấm vào một trang để xem bản vẽ tô màu:
  - 🟢 **xanh**: ký hiệu được tính;
  - 🔴 **đỏ**: ký hiệu chưa biết là vật tư gì;
  - ⚪ **xám**: ký hiệu bỏ qua;
  - **vòng tròn rỗng**: ký hiệu nằm trong bảng chú thích, đã được loại ra.
- Thao tác với khung xem: lăn chuột để phóng to / thu nhỏ, kéo chuột để di chuyển, nhấp đúp để xem vừa khung.
- **Tòa nhà / Tầng / Hệ số tầng**: sửa được nếu phần mềm đọc sai tiêu đề. Nếu một trang vẽ chung cho nhiều tầng (ví dụ "Tầng 1, 2"), nhập hệ số tầng = số tầng thật.
- Các trang có biểu tượng ⚠ là chỗ cần xem lại, ví dụ tiêu đề có thể ghi sai, hoặc trang ghi nhiều tầng.

## 5. Bước 2: Ký hiệu & vật tư
- **Ký hiệu thiết bị**: mỗi dòng là một loại ký hiệu, kèm hình vẽ, chữ hiện trên bản vẽ (nhãn đỏ, ví dụ "8.0") và số lượng trên các trang được tính.
  - Cột **Là vật tư gì?** đã được gợi ý sẵn. Sửa nếu chưa đúng: gõ tên hoặc chọn trong danh sách.
  - ✓ để **xác nhận**, 👁 để **không tính** ký hiệu đó, ◎ để xem ký hiệu nằm ở đâu trên bản vẽ.
  - **Xác nhận tất cả gợi ý**: chấp nhận mọi gợi ý một lần.
  - Ký hiệu đã xác nhận được **ghi nhớ vào Thư viện ký hiệu**. Dự án sau có cùng ký hiệu sẽ tự điền.
- **Đường ống & dây (đo dài)**: gán mỗi lớp vẽ (layer) là loại ống / dây gì.
  - Ví dụ lớp `DN50` là ống thép DN50.
  - Ống gió vẽ bằng 2 nét viền thì để hệ số 0,5.

## 6. Bước 3: Kết quả & xuất Excel
- Bảng **Tổng hợp** chia theo Hệ → Tòa nhà → Hạng mục. "Đếm" nghĩa là phần mềm đếm ký hiệu, "Đo" nghĩa là phần mềm đo chiều dài.
- **Chi tiết theo trang**: mỗi con số lấy từ trang nào, tầng nào.
- **Cần kiểm tra**: danh sách cảnh báo, kèm nút "Xem trang".
- **Cài đặt tính toán**: hao hụt (%) cho ống, dây, ống gió; làm tròn ống thép theo cây 6 m.
- Bấm **Xuất Excel** để lưu file. File gồm 5 sheet:

| Sheet | Nội dung |
|---|---|
| Tổng hợp | Bảng khối lượng theo hệ, tòa nhà, hạng mục |
| Chi tiết theo trang | Mỗi con số lấy từ trang nào, tầng nào |
| Cần kiểm tra | Các cảnh báo cần người xem lại |
| Nhập tay | Hạng mục không có trên bản vẽ, để trống cho người điền |
| Bảng ký hiệu | Ký hiệu nào đã được gán là vật tư gì |

## 7. Những điều cần biết
- **Khối lượng là số đọc được từ bản vẽ.** Những thứ bản vẽ không thể hiện thì nhập ở sheet "Nhập tay", ví dụ:
  - máy bơm, tủ điện, máy phát;
  - phụ kiện, giá treo;
  - đoạn ống nhánh xuống đầu phun.
- **Đường ống vẽ lặp lại** ở nhiều trang của cùng một tầng (trang đầu phun, trang vòi + bình, trang dưới ống gió) **chỉ được tính 1 lần**. Mỗi lần như vậy được ghi ở mục "Cần kiểm tra".
- **Dữ liệu dự án và thư viện ký hiệu** lưu tại `%APPDATA%\DCSoftware\PCCC Takeoff`.

## 8. Kết quả chạy thử trên bộ bản vẽ Youngone Bắc Giang

| Hạng mục (nhà xưởng) | Phần mềm | Bóc tay |
|---|---|---|
| Đầu phun K8.0 quay lên | 1.206 | 1.205 |
| Đầu phun K11.2 quay lên | 2.776 | 2.773 |
| Đầu phun K8.0 quay xuống | 422 | 417 |
| Đầu phun K11.2 quay xuống | 716 | 707 |
| Loa thông báo | 60 | 60 |
| Ống thép DN40 | 3.455 m | 3.504 m |

Thời gian xử lý cả bộ (15 file, 127 trang) khoảng 1 phút.

# DCS PCCC Takeoff: mã nguồn ứng dụng desktop

Ứng dụng Windows gồm 2 phần:
- **Giao diện:** HTML/CSS/JS chạy trong cửa sổ WebView2 (thư viện pywebview).
- **Phần xử lý:** Python, gồm LibreDWG để chuyển DWG sang DXF, ezdxf để đọc bản vẽ và openpyxl để xuất Excel.

## Chạy từ mã nguồn
```powershell
python -m venv .venv
.venv\Scripts\pip install ezdxf pywebview openpyxl pillow pyinstaller
.venv\Scripts\python app\run_app.py          # thêm --debug để mở DevTools
```

## Đóng gói
```powershell
.venv\Scripts\python app\build.py           # -> dist\DCS PCCC Takeoff\DCS PCCC Takeoff.exe
```

Kiểm tra bản đóng gói, gồm cả xử lý một bộ bản vẽ thật:
```powershell
$env:PCCC_SELFTEST_INPUT="D:\duong\dan\bo-ban-ve"
& "dist\DCS PCCC Takeoff\DCS PCCC Takeoff.exe" --selftest selftest.json
```

## Cấu trúc
| Đường dẫn | Vai trò |
|---|---|
| `pccc_takeoff/main.py` | Mở cửa sổ ứng dụng, chế độ `--selftest` |
| `pccc_takeoff/api.py` | Các hàm giao diện gọi xuống Python |
| `pccc_takeoff/core/convert.py` | DWG → DXF bằng LibreDWG, sửa 2 lỗi định dạng của LibreDWG. Dùng ODA làm dự phòng nếu máy có cài sẵn |
| `pccc_takeoff/core/extract.py` | Đọc DXF: khung tên (xref), chữ, block (tên gốc dynamic block + nhãn chữ trong block), đường nét; vẽ hình ký hiệu ra SVG |
| `pccc_takeoff/core/pages.py` | Chia trang, đọc tiêu đề → tòa nhà / tầng, quy tắc bỏ trang trùng, loại ký hiệu bảng chú thích, cảnh báo |
| `pccc_takeoff/core/catalog.py` | Danh mục vật tư, quy tắc gợi ý ký hiệu / lớp → vật tư (không dùng AI) |
| `pccc_takeoff/core/compute.py` | Tính khối lượng; đường nét trùng chiều dài cùng tầng, cùng lớp chỉ tính 1 lần |
| `pccc_takeoff/core/export_xlsx.py` | Xuất Excel 5 sheet theo nhận diện DC Software |
| `pccc_takeoff/core/project.py` | Lưu dự án tại `%APPDATA%\DCSoftware\PCCC Takeoff\projects` |
| `pccc_takeoff/ui/` | Giao diện: `index.html`, `css/app.css`, `js/app.js`, logo, font IBM Plex Sans |
| `vendor/libredwg/` | `dwg2dxf.exe` 0.14 và các DLL (GNU GPL v3, xem `COPYING`) |

## Giấy phép bên thứ ba
| Thành phần | Giấy phép |
|---|---|
| LibreDWG | GPLv3. Gọi như một chương trình riêng; mã nguồn tại https://github.com/LibreDWG/libredwg |
| ezdxf | MIT |
| pywebview | BSD |
| openpyxl | MIT |
| IBM Plex Sans | SIL OFL 1.1 |

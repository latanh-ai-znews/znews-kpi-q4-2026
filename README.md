# Cổng Thông Tin Giao Chỉ Tiêu & Báo Cáo KPI Quý 4/2026
### Tạp chí điện tử Tri thức - Znews

---

## 1. Địa chỉ truy cập trực tiếp (Live URLs)

- 🎯 **Trang 1 — Công cụ tính toán & đề xuất KPI từ tháng 9 (Trang chính mới):**  
  [https://latanh-ai-znews.github.io/znews-kpi-q4-2026/](https://latanh-ai-znews.github.io/znews-kpi-q4-2026/)
- 📋 **Trang 2 — Bảng giao chỉ tiêu đã phê duyệt (Phương án TB T8–T9):**  
  [https://latanh-ai-znews.github.io/znews-kpi-q4-2026/kpi_phe_duyet.html](https://latanh-ai-znews.github.io/znews-kpi-q4-2026/kpi_phe_duyet.html)
- 📑 **Trang 3 — Báo cáo giải thích chi tiết & Bối cảnh dữ liệu:**  
  [https://latanh-ai-znews.github.io/znews-kpi-q4-2026/detail.html](https://latanh-ai-znews.github.io/znews-kpi-q4-2026/detail.html)

---

## 2. Bối cảnh & Mục tiêu xây dựng

Sau biến động kỹ thuật về tên miền vào đầu tháng 8/2026, lưu lượng truy cập toàn trang sụt giảm trung bình **58,1%** so với cùng kỳ năm 2025. Để phục vụ công tác điều hành linh hoạt và giao chỉ tiêu chính xác, hệ thống được cấu trúc thành **3 trang chuyên trách** tích hợp thanh điều hướng trực tiếp:

1. **Công cụ tính toán KPI từ tháng 9 (`index.html`):**  
   - Dựa trên dữ liệu thực tế tháng 9/2026 (29 ngày thực tế quy đổi đủ 30 ngày).
   - Tích hợp bộ điều khiển tương tác theo thời gian thực (Zero-latency reactivity).
   - **Tùy chọn loại bỏ ảnh hưởng Zalo:** 3 kịch bản gồm *Trừ Zalo thực tế (2,1%)*, *Trừ Zalo giả định (5,0%)*, và *Không trừ Zalo (Số gốc T9 quy đổi)*.
   - **Chế độ phân bổ tỷ lệ:** *Áp tỷ lệ tăng toàn bộ ban* hoặc *Tùy chỉnh riêng cho từng ban*.
   - **Tỷ lệ tăng trưởng linh hoạt:** Chọn nhanh các mốc đặt sẵn (+10%, +15%, +20%, +50%) hoặc gõ con số bất kỳ vào ô nhập.
   - Tự động tính toán KPI Ngày (lượt/ngày), KPI Tháng (M), KPI Cả Quý 4 (92 ngày) và Dự báo Cả năm 2026 (% so với 2025).

2. **Phương án KPI đã phê duyệt (`kpi_phe_duyet.html`):**  
   - Bảng giao chỉ tiêu chính thức theo phương án Ban biên tập đã chốt dựa trên mức nền trung bình 2 tháng sau biến động (TB T8–T9: 28,28M/tháng): Khối Uy tín +15%, Khối Kinh doanh +15%, Khối Lifestyle +15% (riêng Lifestyle +10%), Khối Truy cập: Giải trí +15%, Thể thao +20%. Toàn trang đạt **98,73M** trong Quý 4 (tương ứng **1.073.185 lượt/ngày**).

3. **Báo cáo giải thích chi tiết (`detail.html`):**  
   - Phân tích toàn cảnh dữ liệu 9 tháng đầu năm 2026, bảng tiến độ 19 đơn vị qua các mốc 7T, 8T, 9T, đối chiếu 4 kịch bản mục tiêu và phân tích cơ sở tăng trưởng từ 2 đòn bẩy: **Zalo OA** và **Độ uy tín tên miền Google (Domain warm-up)**.

---

## 3. Kiến trúc hệ thống & Danh mục file

```text
Tính KPI Znews Q4 2026/
├── generate_full_dashboard.py      # Kịch bản Python tự động tạo cả 3 trang HTML
├── brief_data.json                 # CSDL gốc trích xuất từ bảng số liệu tòa soạn
├── KPI thang 9.xlsx                # File dữ liệu tháng 9 gốc tòa soạn cung cấp
├── index.html                      # Trang 1: Công cụ tính toán KPI tương tác từ T9
├── kpi_phe_duyet.html              # Trang 2: Bảng giao chỉ tiêu TB T8–T9 đã phê duyệt
├── detail.html                     # Trang 3: Báo cáo giải thích chi tiết & bối cảnh dữ liệu
├── Brief web.md.rtf                # Bản brief yêu cầu & phân tích ban đầu
├── Tien do KPI.rtf                 # Bảng dữ liệu tiến độ KPI 9 tháng đầu năm
├── README.md                       # Tài liệu tổng quan dự án (file này)
├── CHANGELOG.md                    # Nhật ký ghi lại chi tiết từng lần cập nhật của hệ thống
└── HUONG_DAN_TAO_WEBSITE_KPI.md   # Hướng dẫn kỹ thuật & đặc tả chi tiết để tái lập website
```

---

## 4. Công thức tính toán KPI chuẩn từ tháng 9

```
1. Cơ sở tháng 9 (quy đổi 30 ngày):
   - Mức gốc T9 = (Số lượt thực tế 29 ngày / 29) × 30
   - Sau trừ Zalo thực tế (2,13%) = Mức gốc T9 × (1 - 0,0213159)
   - Sau trừ Zalo giả định (5,0%) = Mức gốc T9 × (1 - 0,05)

2. Chỉ tiêu Quý 4/2026:
   - Cơ sở ngày = Cơ sở tháng / 30
   - KPI ngày = Cơ sở ngày × (1 + Tỷ lệ tăng trưởng / 100)
   - KPI Quý 4 (92 ngày) = KPI ngày × 92
   - KPI trung bình tháng = KPI Quý 4 / 3

3. Dự báo cả năm 2026:
   - Cả năm 2026 = Lũy kế 9 tháng thực tế + KPI Quý 4
   - % Tăng trưởng vs 2025 = ((Cả năm 2026 - Cả năm 2025) / Cả năm 2025) × 100%
```

---

## 5. Quy chuẩn kỹ thuật Znews CMS (6 quy tắc vàng)

Mọi trang HTML sinh ra bắt buộc phải vượt qua bộ kiểm thử tự động 6 tiêu chuẩn:
1. **0 inline style (`style=""`):** 100% định dạng nằm trong thẻ `<style>` ở `<head>`, bao gói dưới namespace `.container_AI`.
2. **0 thẻ `<span>`:** Sử dụng các thẻ ngữ nghĩa thay thế: `<strong>`, `<em>`, `<div>`, `<small>`.
3. **0 thẻ `<button>`:** Thay thế bằng `<div class="chip">` hoặc thẻ liên kết `<a class="chip">`.
4. **0 hình ảnh base64 hoặc raster:** 100% biểu đồ (line chart, dumbbell chart, bar chart, mini progress bars) được vẽ trực tiếp bằng vector **inline SVG**, sắc nét ở mọi độ phân giải và tải tức thì.
5. **Đúng chuẩn chính tả tiếng Việt (Sentence case):** Chỉ viết hoa chữ cái đầu câu và danh từ riêng; tuyệt đối không dùng Title Case kiểu tiếng Anh (viết hoa từng từ).
6. **Chuẩn định dạng số tiếng Việt:** Dùng dấu chấm (`.`) phân cách hàng nghìn, dấu phẩy (`,`) phân cách số thập phân.

---

## 6. Lệnh tạo trang & Quy trình triển khai

### Tái tạo mã nguồn:
Chạy script Python để sinh tự động cả 3 file `index.html`, `kpi_phe_duyet.html` và `detail.html`:
```bash
python3 generate_full_dashboard.py
```
*Script sẽ tự động chạy bộ kiểm tra hợp quy (Built-in CMS Validator) trên cả 3 file trước khi ghi file ra đĩa.*

### Đẩy lên GitHub Pages:
```bash
# 1. Cập nhật nhánh main
git add generate_full_dashboard.py index.html kpi_phe_duyet.html detail.html README.md HUONG_DAN_TAO_WEBSITE_KPI.md "KPI thang 9.xlsx"
git commit -m "feat: add interactive September KPI calculator and 3-page portal"
git push origin main

# 2. Xuất bản lên nhánh gh-pages
git checkout gh-pages
git checkout main -- index.html kpi_phe_duyet.html detail.html
git commit -m "deploy: publish 3-page KPI portal to gh-pages"
git push origin gh-pages
git checkout main
```
Sau khoảng 30–60 giây, GitHub Pages sẽ tự động kích hoạt build và cập nhật giao diện mới nhất.

---

## 7. Lịch sử cập nhật hệ thống (Changelog)

Toàn bộ các lần thay đổi, tinh chỉnh số liệu, sửa đổi giao diện và cập nhật tính năng được ghi chép đầy đủ tại tài liệu riêng:
👉 **[Xem chi tiết toàn bộ lịch sử cập nhật tại CHANGELOG.md](CHANGELOG.md)**

### Tóm tắt các mốc phiên bản gần nhất:
- **v2.5 (30/09 22:46):** Đặt mặc định trừ Zalo 5,0%; bổ sung ô và nút tùy chỉnh % ảnh hưởng Zalo linh hoạt theo thời gian thực (`Tùy chỉnh: [ 5 ] %`).
- **v2.4 (30/09 22:34):** Chuẩn hóa tiêu đề "Đề xuất KPI từng ban (14 ban)"; đưa khối 4 thẻ chỉ số tổng quan xuống cuối trang.
- **v2.3 (30/09 22:26):** Tái cấu trúc layout: Thẻ 14 ban lên đầu $\rightarrow$ Bảng tổng hợp $\rightarrow$ Bảng điều khiển $\rightarrow$ 4 thẻ chỉ số.
- **v2.2 (30/09 22:16):** Lược bỏ bảng so sánh 4 kịch bản tĩnh ở trang chủ để tối ưu chiều dài trang.
- **v2.1 (30/09 22:09):** Khắc phục sai số ngày lịch (92 ngày vs 90 ngày) khi tính tỷ lệ tăng trưởng khối/toàn trang.
- **v2.0 (30/09 22:03):** Tích hợp dữ liệu `KPI thang 9.xlsx`, kiến trúc 3 trang chuyên trách với công cụ tính toán thời gian thực.

# Cổng Thông Tin Giao Chỉ Tiêu & Báo Cáo KPI Quý 4/2026
### Tạp chí điện tử Tri thức - Znews

---

## 1. Địa chỉ truy cập trực tiếp (Live URLs)

- 🔗 **Trang chính (Bảng giao chỉ tiêu KPI Quý 4/2026):**  
  [https://latanh-ai-znews.github.io/znews-kpi-q4-2026/](https://latanh-ai-znews.github.io/znews-kpi-q4-2026/)
- 📑 **Trang giải thích chi tiết & Bối cảnh dữ liệu:**  
  [https://latanh-ai-znews.github.io/znews-kpi-q4-2026/detail.html](https://latanh-ai-znews.github.io/znews-kpi-q4-2026/detail.html)

---

## 2. Bối cảnh & Mục tiêu xây dựng

Sau biến động kỹ thuật về tên miền vào đầu tháng 8/2026, lưu lượng truy cập toàn trang sụt giảm trung bình **58,1%** so với cùng kỳ năm 2025. Để vừa đảm bảo tính khả thi thực tiễn, vừa tạo động lực tái thiết lập lưu lượng truy cập cho tòa soạn trong giai đoạn cao điểm cuối năm, Ban biên tập Tạp chí điện tử Tri thức - Znews đã phê duyệt phương án KPI Quý 4/2026.

Hệ thống website này được xây dựng theo mô hình **Portal 2 tầng (2-page architecture)**:
1. **Trang chính (`index.html`):** Executive Dashboard tinh gọn, tập trung 100% vào số liệu giao chỉ tiêu chính thức theo Ngày (lượt xem/ngày), Tháng (M) và Cả Quý 4 (M), không chứa văn bản rườm rà.
2. **Trang báo cáo chi tiết (`detail.html`):** Nghiên cứu chuyên sâu phân tích toàn cảnh dữ liệu 9 tháng đầu năm 2026, bảng tiến độ 19 đơn vị, 4 kịch bản mục tiêu và cơ sở tăng trưởng từ 2 đòn bẩy cốt lõi: **Kênh Zalo OA** và **Độ uy tín tên miền Google (Domain warm-up)**.

---

## 3. Kiến trúc hệ thống & Danh mục file

```text
Tính KPI Znews Q4 2026/
├── generate_full_dashboard.py      # Kịch bản Python tự động tạo toàn bộ index.html và detail.html
├── brief_data.json                 # CSDL gốc trích xuất từ bảng số liệu tòa soạn
├── index.html                      # Trang 1: Bảng giao chỉ tiêu điều hành chính thức
├── detail.html                     # Trang 2: Báo cáo giải thích chi tiết & bối cảnh dữ liệu
├── Brief web.md.rtf                # Bản brief yêu cầu & phân tích ban đầu
├── Tien do KPI.rtf                 # Bảng dữ liệu tiến độ KPI 9 tháng đầu năm
├── README.md                       # Tài liệu tổng quan dự án (file này)
└── HUONG_DAN_TAO_WEBSITE_KPI.md   # Hướng dẫn kỹ thuật & đặc tả chi tiết để tái lập website
```

---

## 4. Bảng giao chỉ tiêu KPI Quý 4/2026 chính thức

> **Cơ sở tính toán:**  
> - Quý 4/2026 có tổng cộng **92 ngày** (Tháng 10: 31 ngày; Tháng 11: 30 ngày; Tháng 12: 31 ngày).  
> - Chỉ tiêu ngày: `round((Chỉ tiêu Quý 4 / 92) * 1.000.000)`.  
> - Đơn vị tính: Triệu lượt hiển thị là **M** (ví dụ `98,73M`). Số ngày hiển thị số nguyên có dấu chấm phân cách hàng nghìn (ví dụ `1.073.185`).

| Đơn vị / ban | KPI ngày (lượt) | KPI tháng (M) | KPI quý 4 (M) | Mức tăng chốt | TB T8–T9 nền (M) | Dự kiến cả năm 2026 (M) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Toàn Znews** | **1.073.185** | **32,91M** | **98,73M** | **+16.4%** | **28,28M** | **595,2M (-25,6%)** |
| **Khối Uy tín** | **205.663** | **6,31M** | **18,92M** | **+15.0%** | **5,48M** | **123,2M (-32,6%)** |
| ↳ Xã hội | 69.489 | 2,13M | 6,39M | +15% | 1,85M | 33,8M (-54,2%) |
| ↳ Pháp luật | 57.326 | 1,76M | 5,27M | +15% | 1,53M | 29,9M (-45,2%) |
| ↳ Thế giới | 35.902 | 1,10M | 3,30M | +15% | 0,96M | 45,6M (+12,9%) |
| ↳ Xuất bản | 42.946 | 1,32M | 3,95M | +15% | 1,15M | 13,8M (-0,4%) |
| **Khối Kinh doanh** | **226.272** | **6,94M** | **20,82M** | **+15.0%** | **6,03M** | **95,7M (-24,4%)** |
| ↳ Kinh doanh | 136.435 | 4,18M | 12,55M | +15% | 3,64M | 55,1M (-26,1%) |
| ↳ Công nghệ | 58.826 | 1,80M | 5,41M | +15% | 1,57M | 26,3M (-24,3%) |
| ↳ Xe | 31.011 | 0,95M | 2,85M | +15% | 0,83M | 14,2M (-17,1%) |
| **Khối Lifestyle** | **215.087** | **6,60M** | **19,79M** | **+14.5%** | **5,76M** | **132,5M (-26,6%)** |
| ↳ Đời sống | 69.065 | 2,12M | 6,35M | +15% | 1,84M | 53,1M (-19,9%) |
| ↳ Sức khỏe | 70.467 | 2,16M | 6,48M | +15% | 1,88M | 34,1M (-37,0%) |
| ↳ Du lịch | 36.326 | 1,11M | 3,34M | +15% | 0,97M | 20,4M (-17,8%) |
| ↳ Giáo dục | 20.283 | 0,62M | 1,87M | +15% | 0,54M | 12,8M (-30,5%) |
| ↳ Lifestyle *(Đặc thù)* | **18.946** | **0,58M** | **1,74M** | **+10%** | **0,53M** | **12,1M (-28,0%)** |
| **Khối Truy cập** | **426.163** | **13,07M** | **39,21M** | **+18.8%** | **11,01M** | **243,8M (-21,3%)** |
| ↳ Thể thao *(Mũi nhọn)* | **323.152** | **9,91M** | **29,73M** | **+20%** | **8,26M** | **180,1M (-15,5%)** |
| ↳ Giải trí | 103.011 | 3,16M | 9,48M | +15% | 2,75M | 63,7M (-34,2%) |

---

## 5. Quy chuẩn kỹ thuật Znews CMS (6 quy tắc vàng)

Để mã HTML có thể nhúng trực tiếp vào CMS nội bộ hoặc chạy tĩnh độc lập với độ tương thích tuyệt đối, hệ thống tuân thủ nghiêm ngặt 6 tiêu chuẩn:
1. **0 inline style (`style=""`):** 100% định dạng nằm trong thẻ `<style>` ở `<head>`, bao gói dưới namespace `.container_AI`.
2. **0 thẻ `<span>`:** Sử dụng các thẻ ngữ nghĩa thay thế: `<strong>`, `<em>`, `<div>`, `<small>`.
3. **0 thẻ `<button>`:** Thay thế bằng `<div class="chip">` hoặc thẻ liên kết `<a class="chip">`.
4. **0 hình ảnh base64 hoặc raster:** 100% biểu đồ (line chart, dumbbell chart, bar chart, mini progress bars) được vẽ trực tiếp bằng vector **inline SVG**, sắc nét ở mọi độ phân giải và tải tức thì.
5. **Đúng chuẩn chính tả tiếng Việt (Sentence case):** Chỉ viết hoa chữ cái đầu câu và danh từ riêng; tuyệt đối không dùng Title Case kiểu tiếng Anh (viết hoa từng từ).
6. **Chuẩn định dạng số tiếng Việt:** Dùng dấu chấm (`.`) phân cách hàng nghìn, dấu phẩy (`,`) phân cách số thập phân.

---

## 6. Lệnh tạo trang & Quy trình triển khai

### Tái tạo mã nguồn:
Chạy script Python để sinh tự động cả 2 file `index.html` và `detail.html`:
```bash
python3 generate_full_dashboard.py
```
*Script sẽ tự động chạy bộ kiểm tra hợp quy (Built-in CMS Validator) trước khi ghi file ra đĩa.*

### Đẩy lên GitHub Pages:
```bash
# 1. Cập nhật nhánh main
git add generate_full_dashboard.py index.html detail.html
git commit -m "feat: update dashboard files"
git push origin main

# 2. Xuất bản lên nhánh gh-pages
git checkout gh-pages
git checkout main -- index.html detail.html
git commit -m "deploy: publish latest build to gh-pages"
git push origin gh-pages
git checkout main
```
Sau khoảng 30–60 giây, GitHub Pages sẽ tự động kích hoạt build và cập nhật giao diện mới nhất.

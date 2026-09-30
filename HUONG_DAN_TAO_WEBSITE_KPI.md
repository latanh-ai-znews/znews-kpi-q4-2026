# HƯỚNG DẪN KỸ THUẬT & ĐẶC TẢ XÂY DỰNG WEBSITE BÁO CÁO KPI
### Cẩm nang tái lập & phát triển hệ thống Dashboard cho Tạp chí điện tử Tri thức - Znews

---

## MỤC LỤC
1. [Giới thiệu & Triết lý thiết kế](#1-giới-thiệu--triết-lý-thiết-kế)
2. [Cấu trúc kiến trúc 3 tầng (Portal Architecture)](#2-cấu-trúc-kiến-trúc-2-tầng-portal-architecture)
3. [Quy chuẩn Znews CMS (6 quy tắc vàng)](#3-quy-chuẩn-znews-cms-6-quy-tắc-vàng)
4. [Hệ thống thiết kế UI/UX (Design System)](#4-hệ-thống-thiết-kế-uiux-design-system)
5. [Đặc tả mô hình dữ liệu (Data Schema)](#5-đặc-tả-mô-hình-dữ-liệu-data-schema)
6. [Công thức tính toán KPI chuẩn](#6-công-thức-tính-toán-kpi-chuẩn)
7. [Kỹ thuật dựng biểu đồ vector bằng SVG thuần (Zero-library)](#7-kỹ-thuật-dựng-biểu-đồ-vector-bằng-svg-thuần-zero-library)
8. [Bộ kiểm thử tự động (Built-in Validator)](#8-bộ-kiểm-thử-tự-động-built-in-validator)
9. [Quy trình phát triển & Xuất bản lên GitHub Pages](#9-quy-trình-phát-triển--xuất-bản-lên-github-pages)
10. [Mẫu khung Python (Boilerplate) để tạo website mới](#10-mẫu-khung-python-boilerplate-để-tạo-website-mới)

---

## 1. Giới thiệu & Triết lý thiết kế

Tài liệu này đóng gói toàn bộ phương pháp luận, công thức toán học, quy chuẩn mã nguồn và quy trình triển khai đã được áp dụng thành công tại dự án **Website KPI Quý 4/2026 của Tạp chí điện tử Tri thức - Znews**.

### Triết lý cốt lõi:
- **Độc lập tuyệt đối (Zero Dependency):** Không dùng bất kỳ thư viện JavaScript ngoài nào (không npm, không Chart.js, không D3.js, không React/Vue). Toàn bộ HTML/CSS/SVG/JS nằm trọn vẹn trong các file tĩnh độc lập.
- **Tốc độ siêu tốc & Tải tức thì:** Kích thước trang nhẹ (khoảng 50KB – 200KB), hiển thị ngay lập tức không có độ trễ kết nối CDN.
- **Tập trung vào số liệu điều hành:** Giảm thiểu văn bản giải thích dài dòng ở trang chủ, ưu tiên trực quan hóa con số theo Ngày • Tháng • Quý.
- **Ngữ pháp & Chính tả tiếng Việt chuẩn mực:** Tuân thủ quy tắc Sentence case (chỉ viết hoa đầu câu và danh từ riêng).

---

## 2. Cấu trúc kiến trúc 3 tầng (Portal Architecture)

Hệ thống được tách bạch thành 2 trang chuyên trách, liên kết qua lại bằng các nút điều hướng rõ ràng:

```
[ Người xem ]
     │
     ├──► [ index.html ]: Công cụ tính toán & đề xuất KPI từ tháng 9 (Interactive Calculator)
     │         ├─ Bộ điều khiển Zalo (Trừ thực tế 2,1%, Trừ giả định 5%, Không trừ)
     │         ├─ Chế độ phân bổ (Áp toàn bộ ban vs Tùy từng ban)
     │         ├─ Tỷ lệ tăng (+10%, +15%, +20%, +50% hoặc nhập tùy ý)
     │         ├─ 4 thẻ tổng quan toàn soạn: Ngày, Tháng, Quý 4, Năm
     │         ├─ Bảng Master 19 đơn vị có input chỉnh riêng theo từng ban
     │         └─ Bảng so sánh 4 kịch bản quy đổi theo tháng
     │
     ├──► [ kpi_phe_duyet.html ]: Bảng giao chỉ tiêu chính thức (Executive Dashboard) (Executive Dashboard)
     │         ├─ 4 thẻ tổng quan toàn soạn: Ngày (1.073.185), Tháng (32,91M), Quý 4 (98,73M), Năm (595,20M)
     │         ├─ Bảng Master 19 đơn vị: Có bộ lọc tương tác (Tất cả, 4 khối, 14 ban)
     │         ├─ Cột hiển thị: Đơn vị/ban | KPI ngày | KPI tháng | KPI quý 4 | Mức tăng | TB T8-T9 (nền)
     │         ├─ 14 thẻ ban biên tập: Hiển thị 3 hộp số liệu Ngày/Tháng/Quý + Nền T8-T9 + Cả năm
     │         └─ Nút CTA: Dẫn sang trang giải thích chi tiết
     │
     └──► [ detail.html ]: Báo Cáo Giải Thích Chi Tiết & Bối Cảnh Dữ Liệu
               ├─ Phần 1: Ảnh hưởng truy cập sau biến động T8 (Dumbbell 7T, Drop T8-T9, Tiến độ 7T/8T/9T)
               ├─ Phần 2: Đề xuất các mức KPI mới (Bảng 4 kịch bản +10%, +15%, +20%, +50% của 19 đơn vị)
               ├─ Phần 3: Cơ sở khoa học & 2 Đòn bẩy tăng trưởng (Zalo OA & Google Domain warm-up)
               └─ Nút Back: Quay lại trang chính (ở đầu trang, menu nhanh và chân trang)
```

---

## 3. Quy chuẩn Znews CMS (6 quy tắc vàng)

Mọi trang HTML sinh ra bắt buộc phải vượt qua bộ kiểm thử 6 tiêu chí:

| STT | Tiêu chuẩn | Lý do kỹ thuật | Cách xử lý thay thế |
| :---: | :--- | :--- | :--- |
| **1** | **0 Inline Style (`style=""`)** | Tránh xung đột với CSS của CMS khi nhúng | Mọi style đưa vào khối `<style>` đóng gói dưới scope `.container_AI` |
| **2** | **0 thẻ `<span>`** | CMS Znews có bộ lọc strip hoặc override `<span>` | Dùng `<strong>`, `<em>`, `<div>`, `<small>` |
| **3** | **0 thẻ `<button>`** | CMS có thể hiểu nhầm là nút submit form | Dùng `<div class="chip">` hoặc `<a class="chip">` |
| **4** | **0 ảnh base64 / bitmap** | Làm phình file HTML, vỡ hình trên màn Retina | Dùng **Inline SVG vector**, co dãn mượt mà với `viewBox` |
| **5** | **Đúng chính tả tiếng Việt** | Tôn trọng chuẩn biên tập báo chí chính quy | Dùng Sentence case (chỉ viết hoa đầu câu); bỏ `text-transform: uppercase` |
| **6** | **Chuẩn số tiếng Việt** | Tránh nhầm lẫn phân cách thập phân | Dấu `.` cho hàng nghìn (`1.073.185`), dấu `,` cho thập phân (`32,91M`) |

---

## 4. Hệ thống thiết kế UI/UX (Design System)

### Bảng màu nhận diện (Color Palette):
```css
/* Màu chủ đạo & Nền */
--bg-page:        #f8fafc; /* Nền xám nhạt dịu mắt */
--bg-card:        #ffffff; /* Nền thẻ trắng */
--text-main:      #14161c; /* Chữ chính đậm */
--text-muted:     #64748b; /* Chữ chú thích xám */
--border-subtle:  #e2e8f0; /* Viền thẻ nhẹ */

/* Màu trạng thái & Số liệu */
--primary-blue:   #3b56e0; /* Xanh dương điểm nhấn / KPI tháng */
--success-green:  #10b981; /* Xanh lá / KPI ngày / Tăng trưởng dương */
--quarter-purple: #8b5cf6; /* Tím / KPI Quý 4 */
--warning-amber:  #d97706; /* Vàng cam / Cảnh báo chững lại */
--danger-red:     #dc2626; /* Đỏ / Sụt giảm mạnh / Chậm tiến độ */
```

### Font chữ quy chuẩn:
- **Nội dung & Nhãn:** `Be Vietnam Pro` (tối ưu hiển thị dấu thanh tiếng Việt).
- **Con số:** `Manrope` (font hình học hiện đại, hỗ trợ số `tnum` - Tabular Numbers để các con số thẳng hàng hoàn hảo trong bảng).

---

## 5. Đặc tả mô hình dữ liệu (Data Schema)

File dữ liệu nguồn chuẩn hóa lưu trữ dưới dạng JSON (`brief_data.json`):

```json
{
  "monthly": {
    "cot": ["01/2025", "02/2025", ..., "08/2026", "09/2026"],
    "dong": {
      "Toàn Znews": [55756048, 62768254, ..., 31407164, 25155728],
      "Khối Uy tín": [ ... ],
      "Xã hội": [ ... ],
      "Pháp luật": [ ... ]
    }
  },
  "t7_growth": {
    "Toàn Znews": { "t7_2025": 470713631, "t7_2026": 435900089, "pct_7t": -7.4, ... },
    "Thể thao": { ... }
  },
  "kpi_progress": {
    "Toàn Znews": { "target_year": 834200000, "actual_7t": 439900000, "actual_8t": 471300000, "actual_9t": 496464023 },
    "Kinh doanh": { ... }
  }
}
```

> **Lưu ý đặc thù về số liệu:**  
> Dữ liệu ngày 08/12/2025 của chuyên mục *Lifestyle* trong sheet gốc có sai sót gõ thừa số (`19.177.465` thay vì `91.774` lượt). Luôn dùng **SỐ CHUẨN** (giảm 19,08 triệu lượt của năm 2025) để mọi tỷ lệ tăng trưởng so với cùng kỳ không bị méo mó.

---

## 6. Công thức tính toán KPI chuẩn

### 6.1. Mức nền thực tế (Baseline):
Do biến động tên miền diễn ra từ tháng 8, mức nền chuẩn của Quý 4 được lấy bằng trung bình cộng thực tế 2 tháng sau cú sốc (T8 và T9/2026):
$$\text{TB T8–T9} = \frac{\text{Thực tế T8/2026} + \text{Thực tế T9/2026}}{2}$$

### 6.2. Mục tiêu Tháng (KPI Tháng):
$$\text{KPI}_{\text{tháng}} = \text{TB T8–T9} \times (1 + \text{Mức tăng chốt})$$
*Ví dụ: Ban Xã hội có nền 1,85M, tăng +15% $\rightarrow 1,85 \times 1,15 = 2,13\text{M/tháng}$.*

### 6.3. Mục tiêu Cả Quý 4 (92 ngày):
$$\text{KPI}_{\text{Quý 4}} = \text{KPI}_{\text{tháng}} \times 3$$
*(Toàn Znews: $32,91\text{M} \times 3 = 98,73\text{M}$.)*

### 6.4. Mục tiêu Ngày (KPI Ngày):
Quý 4 gồm 92 ngày (T10: 31, T11: 30, T12: 31):
$$\text{KPI}_{\text{ngày}} = \text{round}\left( \frac{\text{KPI}_{\text{Quý 4}} \times 1.000.000}{92} \right)$$
*Ví dụ: Toàn Znews cần đạt: $98.730.000 / 92 = 1.073.185\text{ lượt/ngày}$.*

### 6.5. Dự kiến Cả năm 2026:
$$\text{Dự kiến 2026} = \text{Lũy kế 9 tháng thực tế} + \text{KPI}_{\text{Quý 4}}$$
$$\%\text{ so với năm 2025} = \frac{\text{Dự kiến 2026} - \text{Thực tế 2025 (chuẩn)}}{\text{Thực tế 2025 (chuẩn)}} \times 100\%$$

---

## 7. Kỹ thuật dựng biểu đồ vector bằng SVG thuần (Zero-library)

Thay vì tải các thư viện nặng nề, code Python sẽ trực tiếp tính toán tọa độ pixel `(x, y)` và kết xuất chuỗi thẻ `<svg>`.

### 7.1. Mẫu vẽ thanh tiến độ Mini Progress Bar (với vạch mốc chuẩn):
```python
def build_mini_progress_svg(pct_actual, pct_target_standard, width=84, height=6):
    # Chiều dài thanh thực tế
    bar_w = round(min(pct_actual / 100.0, 1.0) * width, 1)
    # Vị trí vạch chuẩn thời gian (ví dụ 58.3% hoặc 75.0%)
    line_x = round((pct_target_standard / 100.0) * width, 1)
    
    # Màu sắc dựa trên tiến độ
    color = "#10b981" if pct_actual >= pct_target_standard else ("#f59e0b" if pct_actual >= pct_target_standard - 10 else "#dc2626")
    
    return f'''<svg class="prog_svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">
      <rect x="0" y="0" width="{width}" height="{height}" fill="#e2e8f0" rx="3"/>
      <rect x="0" y="0" width="{bar_w}" height="{height}" fill="{color}" rx="3"/>
      <line x1="{line_x}" y1="0" x2="{line_x}" y2="{height}" stroke="#0f172a" stroke-width="1.5"/>
    </svg>'''
```

### 7.2. Mẫu vẽ biểu đồ cột ngang (Horizontal Bar Chart):
```python
def build_horizontal_bar_svg(data_items, max_val, width=960, row_height=32):
    height = len(data_items) * row_height + 40
    svg = [f'<svg class="chart_svg" viewBox="0 0 {width} {height}" width="100%" height="auto" xmlns="http://www.w3.org/2000/svg">']
    
    for i, (name, val) in enumerate(data_items):
        y = i * row_height + 20
        bar_len = round((val / max_val) * (width - 300), 1)
        # Nền xen kẽ
        if i % 2 == 1:
            svg.append(f'<rect x="10" y="{y - 12}" width="{width - 20}" height="{row_height}" fill="#f8fafc" rx="4"/>')
        # Tên ban (bên trái)
        svg.append(f'<text x="20" y="{y + 6}" fill="#14161c" font-size="13" font-weight="700">{name}</text>')
        # Thanh giá trị
        svg.append(f'<rect x="180" y="{y - 6}" width="{bar_len}" height="16" fill="#3b56e0" rx="3"/>')
        # Nhãn giá trị (bên phải thanh bar)
        svg.append(f'<text x="{180 + bar_len + 12}" y="{y + 6}" fill="#0f172a" font-size="12" font-weight="700">{val}M</text>')
        
    svg.append('</svg>')
    return "".join(svg)
```

---

## 8. Bộ kiểm thử tự động (Built-in Validator)

Trong script sinh file `generate_full_dashboard.py`, luôn tích hợp hàm kiểm thử tự động trước khi xuất ra đĩa:

```python
def validate_html(html_str, filename):
    errors = []
    
    # 1. Kiểm tra inline style
    if re.search(r'<[^>]+style=[\"\'][^>]+>', html_str, re.IGNORECASE):
        errors.append("Phát hiện thẻ chứa inline style=\"...\" (Quy chuẩn cấm).")
        
    # 2. Kiểm tra thẻ span
    if re.search(r'<\/?span[^>]*>', html_str, re.IGNORECASE):
        errors.append("Phát hiện thẻ <span> (Quy chuẩn cấm, dùng strong/em/div).")
        
    # 3. Kiểm tra thẻ button
    if re.search(r'<\/?button[^>]*>', html_str, re.IGNORECASE):
        errors.append("Phát hiện thẻ <button> (Dùng div.chip hoặc a.chip).")
        
    # 4. Kiểm tra ảnh base64
    if "data:image" in html_str:
        errors.append("Phát hiện ảnh base64 (Chỉ cho phép inline vector SVG).")
        
    # 5. Kiểm tra danh xưng Tạp chí
    if re.search(r'[Bb]áo\s+(?:điện\s+tử|Điện\s+Tử)', html_str):
        errors.append("Phát hiện danh xưng 'Báo điện tử' (Phải là Tạp chí điện tử Tri thức - Znews).")
        
    if errors:
        print(f"FAILED: {filename} vi phạm quy chuẩn CMS:")
        for e in errors:
            print(f"  - {e}")
        return False
    else:
        print(f"PASS: {filename} 100% đạt chuẩn Znews CMS rules!")
        return True
```

---

## 9. Quy trình phát triển & Xuất bản lên GitHub Pages

### Bước 1: Chuẩn bị dữ liệu
Cập nhật số liệu thô vào `brief_data.json` hoặc truyền trực tiếp vào script Python.

### Bước 2: Sinh file tĩnh
```bash
python3 generate_full_dashboard.py
```

### Bước 3: Đẩy mã nguồn & Triển khai
Để trang web chạy trên GitHub Pages ổn định, ta sử dụng mô hình nhánh:
- `main`: Lưu toàn bộ mã nguồn, script Python, dữ liệu và tài liệu hướng dẫn.
- `gh-pages`: Nhánh độc lập chỉ chứa các file xuất bản tĩnh (`index.html`, `detail.html`, `.nojekyll`).

**Lệnh đẩy tự động:**
```bash
# Cập nhật code lên nhánh main
git add .
git commit -m "feat: cập nhật số liệu KPI"
git push origin main

# Triển khai tức thì lên GitHub Pages
git checkout gh-pages
git checkout main -- index.html detail.html
git commit -m "deploy: xuất bản trang mới lên GitHub Pages"
git push origin gh-pages
git checkout main
```

**Xác thực trạng thái xuất bản qua GitHub CLI:**
```bash
gh api repos/:owner/:repo/pages/builds/latest --jq '.status'
# Khi trả về "built" là trang web đã chính thức online.
```

---

## 10. Mẫu khung Python (Boilerplate) để tạo website mới

Khi cần tạo website KPI mới cho Quý tiếp theo (ví dụ Quý 1/2027), chỉ cần sao chép khung mã nguồn sau:

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
KỊCH BẢN MẪU: SINH WEBSITE BÁO CÁO KPI TỰ ĐỘNG
Tạp chí điện tử Tri thức - Znews
"""

import json, re

def fmt_day(val):
    return f"{int(round(val)):,}".replace(",", ".")

def fmt_tr(val, decimals=2):
    f_str = f"{val:.{decimals}f}".replace(".", ",")
    return f_str

def generate_page(title, body_content):
    css = """
    @import url('https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@400;500;600;700&family=Manrope:wght@600;700;800&display=swap');
    .container_AI { width: 100vw; margin-left: calc(50% - 50vw); margin-right: calc(50% - 50vw); background: #f8fafc; font-family: 'Be Vietnam Pro', sans-serif; color: #14161c; }
    .container_AI .wrap { max-width: 1100px; margin: 0 auto; padding: 40px 20px; }
    .container_AI .card { background: #ffffff; border: 1px solid #e2e8f0; border-radius: 14px; padding: 24px; margin-bottom: 24px; }
    .container_AI .chip { display: inline-block; padding: 6px 14px; border-radius: 20px; background: #f1f5f9; cursor: pointer; font-size: 13px; font-weight: 600; }
    .container_AI .chip.active { background: #3b56e0; color: #ffffff; }
    """
    
    html = f"""<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <style>{css}</style>
</head>
<body>
<article class="container_AI">
  <div class="wrap">
    {body_content}
  </div>
</article>
</body>
</html>"""
    return html

if __name__ == "__main__":
    # Điền nội dung và ghi ra file
    content = '<div class="card"><h1>Nội dung giao chỉ tiêu</h1></div>'
    out_html = generate_page("Bảng giao chỉ tiêu KPI — Tạp chí điện tử Tri thức - Znews", content)
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(out_html)
    print("Hoàn tất tạo trang!")
```

---
*Tài liệu được biên soạn và chuẩn hóa bởi Antigravity AI Assistant & Ban Biên tập Tạp chí điện tử Tri thức - Znews (Lưu hành nội bộ).*

# Nhật Ký Cập Nhật Hệ Thống Tính & Báo Cáo KPI Quý 4/2026
### Tạp chí điện tử Tri thức - Znews

Tài liệu này ghi lại toàn bộ lịch sử các lần cập nhật, sửa đổi, bổ sung tính năng và tinh chỉnh số liệu của dự án từ ngày khởi tạo (29/09/2026) đến thời điểm hiện tại.

---

## 📌 Bảng Tóm Tắt Lịch Sử Cập Nhật

| Phiên bản | Thời gian | Mã Commit | Nội dung cập nhật chính | Người thực hiện |
| :--- | :--- | :--- | :--- | :--- |
| **v2.7** | 30/09/2026 23:38 | `aeff07f` | Đồng bộ toàn bộ dòng tổng các khối về màu xanh trong Bảng tổng hợp; chạy code xác thực số liệu | Antigravity AI |
| **v2.6** | 30/09/2026 23:22 | `1532730` | Thêm box giải thích bối cảnh và nguyên tắc đề xuất KPI mới ở đầu trang | Antigravity AI |
| **v2.5** | 30/09/2026 22:46 | `0dc4c28` | Đặt mặc định trừ Zalo 5,0%; thêm ô tùy chỉnh % ảnh hưởng Zalo linh hoạt | Antigravity AI |
| **v2.4** | 30/09/2026 22:34 | `2646ad7` | Đổi tên "Đề xuất KPI từng ban (14 ban)"; đưa 4 thẻ chỉ số tổng quan xuống cuối trang | Antigravity AI |
| **v2.3** | 30/09/2026 22:26 | `af164f9` | Đảo vị trí: Thẻ 14 ban lên đầu $\rightarrow$ Bảng tổng hợp $\rightarrow$ Bảng điều khiển | Antigravity AI |
| **v2.2** | 30/09/2026 22:16 | `ca93fff` | Bỏ bảng so sánh 4 kịch bản (+10%, +15%, +20%, +50%) ở trang index | Antigravity AI |
| **v2.1** | 30/09/2026 22:09 | `efe9152` | Sửa logic tính tỷ lệ tăng trưởng khối/toàn trang theo ngày, xử lý lệch ngày lịch | Antigravity AI |
| **v2.0** | 30/09/2026 22:03 | `c4a3e88` | Tích hợp dữ liệu `KPI thang 9.xlsx`, tạo công cụ tương tác mới `index.html` | Antigravity AI |
| **v1.6** | 30/09/2026 21:37 | `7c0b6b1` | Xuất bản tài liệu kiến trúc `README.md` & cẩm nang tái tạo `HUONG_DAN_TAO_WEBSITE_KPI.md` | Antigravity AI |
| **v1.5** | 30/09/2026 11:13 | `67b2b39` | Chuẩn hóa danh xưng: "Tạp chí điện tử Tri thức - Znews" (thay cho Báo điện tử) | Antigravity AI |
| **v1.4** | 30/09/2026 10:53 | `29d4185` | Chuẩn hóa chính tả tiếng Việt (Sentence-case) & đổi tên "Chi tiết KPI từng ban" | Antigravity AI |
| **v1.3** | 30/09/2026 09:31 | `4349710` | Tinh gọn trang chủ sang số liệu thuần túy với đơn vị M, sắp xếp lại thứ tự cột | Antigravity AI |
| **v1.2** | 30/09/2026 09:05 | `cce2ff5` | Tách cổng thông tin: `index.html` (chỉ tiêu đã duyệt) và `detail.html` (báo cáo giải trình) | Antigravity AI |
| **v1.1** | 29/09/2026 19:41 | `e382a3e` | Chuẩn hóa định dạng số tiếng Việt trong biểu đồ grouped bar chart | Antigravity AI |
| **v1.0.5**| 29/09/2026 19:18 | `afa893b` | Sửa lỗi CSS chip lọc bảng tiến độ 19 đơn vị (`.is_hidden`) | Antigravity AI |
| **v1.0.4**| 29/09/2026 19:08 | `620bb60` | Tái cấu trúc báo cáo 3 phần: Tiến độ 9T, mức độ sụt giảm, 2 đòn bẩy Zalo & Google | Antigravity AI |
| **v1.0.3**| 29/09/2026 18:53 | `b2ccb03` | Điều chỉnh dữ liệu Lifestyle (loại trừ lỗi ngày 08/12/2025) và cập nhật tổng 2025 | Antigravity AI |
| **v1.0.2**| 29/09/2026 18:05 | `0ad72aa` | Khắc phục triệt để hiện tượng chữ đè lên thanh biểu đồ (Zero text overlap) | Antigravity AI |
| **v1.0.1**| 29/09/2026 17:56 | `52653d1` | Bổ sung 2 kịch bản KPI: Mốc +20% (Thử thách) và Mốc +50% (Phục hồi truy cập) | Antigravity AI |
| **v1.0** | 29/09/2026 16:52 | `7d66f0d` | Khởi tạo trang dashboard báo cáo KPI Quý 4/2026 tĩnh đầu tiên | Antigravity AI |

---

## 🔍 Chi Tiết Từng Lần Cập Nhật

---

### [Cập nhật #24] — Phiên bản v2.7 (30/09/2026 23:38:00)
- **Mã Commit:** `aeff07f` (nhánh `main`)
- **Yêu cầu từ người dùng:**
  > *"Bảng tổng hợp chỉ tiêu: Ngày • Tháng • Quý 4/2026 & dự báo năm*
  > *Trong bảng này, số tổng của các khối đều màu vàng, riêng khối lifestyle lại là màu xanh. Đổi lại đồng bộ màu xanh.*
  > *Ngoài ra, chạy code để đảm bảo toàn bộ số liệu chính xác và xác thực cho tôi."*
- **Các thay đổi thực hiện:**
  1. **Đồng bộ màu sắc dòng tổng của các khối (Master Table):**
     - Đổi style `.row_block` (dòng tổng 4 khối: Khối Uy tín, Khối Kinh doanh, Khối Lifestyle, Khối Truy cập) sang tông nền xanh dịu nhạt đồng nhất (`#f0fdf4`), viền xanh ngọc thanh lịch (`border: 1.5px solid #bbf7d0`), chữ màu xanh đậm (`color: #064e3b`).
     - Đổi badge tỷ lệ tăng trưởng trên cả 4 dòng khối sang `badge_20` màu xanh lá dịu (`background: #dcfce7; color: #166534`).
     - Đồng bộ hóa logic Javascript trong hàm `render()` để khi tính toán phản ứng, các badge dòng khối và dòng Toàn Znews luôn giữ màu xanh đồng bộ.
     - Đồng bộ cả dòng tổng `row_total` (Toàn Znews) với viền ngọc emerald (`#059669`) và nền xanh (`#ecfdf5`).
  2. **Chạy mã kiểm toán độc lập & xác thực 100% số liệu:**
     - Đã chạy script Python kiểm toán toàn bộ số liệu từ dữ liệu gốc 29 ngày tháng 9 (`25.155.728` lượt), quy đổi 30 ngày (`26.023.166,90` lượt), sau trừ Zalo 5% (`24.722.008,55` lượt).
     - Xác thực chéo chính xác:
       * Tổng 14 ban $\equiv$ Tổng 4 khối $\equiv$ Toàn Znews.
       * KPI ngày Quý 4: `947.677` lượt/ngày (+15,0% so với nền T9).
       * KPI tháng Quý 4: `29,06M` lượt/tháng.
       * KPI Quý 4 (92 ngày): `87,19M` lượt.
       * Dự kiến cả năm 2026: `583,65M` lượt (-27,0% so với năm 2025 sau điều chỉnh Lifestyle).
  3. **Tuân thủ quy chuẩn Znews CMS:**
     - 100% tuân thủ CSS scoped, 0 inline styles, 0 thẻ `<span>`, 0 thẻ `<button>`, 0 ảnh base64.

---

### [Cập nhật #23] — Phiên bản v2.6 (30/09/2026 23:22:00)
- **Mã Commit:** `1532730` (nhánh `main`) và `d9b56b0` (nhánh `gh-pages`)
- **Yêu cầu từ người dùng:**
  > *"Thêm một box giải thích ở ngay đầu trang, phía trên phần Đề xuất KPI từng ban. Box này cần được đặt trong ô căn giữa trang, có nền nhã nhặn và chữ dễ nhìn.*
  > *Bối cảnh và nguyên tắc đề xuất KPI mới:*
  > *- Từ tháng 8, việc thay đổi tên miền khiến truy cập giảm mạnh. Mức giảm trung bình là 58%, nhưng có những ban giảm tới 70%. Tòa soạn cần đề xuất KPI mới vừa phản ánh được mặt bằng truy cập mới, vừa là con số để các ban phấn đấu.*
  > *- KPI mới được xây dựng dựa trên mức trung bình truy cập của tháng 9, đồng thời giảm trừ khoảng 5% ảnh hưởng truy cập từ Zalo, yếu tố hiện tại tòa soạn chưa chủ động kiểm soát.*
  > *- Cụ thể, con số đề xuất cho toàn bộ Quý IV là tăng 15% so với mức trung bình."*
- **Các thay đổi thực hiện:**
  1. **Vị trí hiển thị:** Đặt box giải thích `.intro_context_card` ở ngay đầu trang `index.html`, ngay dưới Header thương hiệu và phía trên phần "Đề xuất KPI từng ban (14 ban)".
  2. **Giao diện & Căn giữa:**
     - Thiết lập căn giữa trang (`max-width: 1040px; margin: 0 auto 28px auto;`).
     - Tông màu nền nhã nhặn dịu mắt (`#f8faff`), viền xanh thanh lịch (`#dbeafe`), đường chỉ nhấn lề trái xanh dương Znews (`border-left: 4px solid #3b56e0`).
     - Font chữ tối màu rõ ràng (`#334155`), tiêu đề đậm nét (`#1e293b`), các số liệu cốt lõi (`58%`, `70%`, `5%`, `tăng 15% so với mức trung bình`) được in đậm để lãnh đạo và biên tập viên dễ theo dõi.
  3. **Tuân thủ quy chuẩn Znews CMS:**
     - 100% tuân thủ CSS scoped, 0 inline styles, 0 thẻ `<span>`, 0 thẻ `<button>`, 0 ảnh base64.

---

### [Cập nhật #22] — Phiên bản v2.5 (30/09/2026 22:46:58)
- **Mã Commit:** `0dc4c28` (nhánh `main`) và `ad1a4b7` (nhánh `gh-pages`)
- **Yêu cầu từ người dùng:**
  > *"Zalo đặt mặc định ảnh hưởng là 5%. Cho thêm nút tùy chỉnh mức ảnh hưởng của Zalo để tôi tự điều chỉnh."*
- **Các thay đổi thực hiện:**
  1. **Đặt mức trừ Zalo mặc định là 5,0%**:
     - Chip `Trừ Zalo giả định (5,0%)` được active mặc định khi tải trang.
     - Dữ liệu pre-render tĩnh và state JavaScript ban đầu (`state.zaloRate = 5.0`) đều tính theo mức trừ 5,0%:
       * Mức nền tháng 9: **24,72M/tháng** (**824.067 lượt/ngày**).
       * KPI ngày toàn trang: **947.677** lượt/ngày.
       * KPI trung bình tháng: **29,06M**/tháng.
       * KPI Quý 4: **87,19M**.
       * Dự báo cả năm 2026: **583,65M** (*-27,0% so với 2025*).
  2. **Thêm ô tùy chỉnh mức ảnh hưởng Zalo (`Tùy chỉnh: [ 5 ] %`)**:
     - Thêm ô nhập số vào khối `#zalo_chips` với tiền tố nhãn `.input_prefix_tag` ("Tùy chỉnh:") và hậu tố `.rate_unit` ("%").
     - Hỗ trợ nhập số thực bất kỳ (bước nhảy `step="0.5"`, khoảng giá trị 0% – 50%).
     - Tích hợp liên kết hai chiều (two-way binding): gõ số thì tự động tính lại toàn trang và đồng bộ trạng thái chip; bấm chip đặt sẵn thì ô số tự động điền giá trị.
     - Dòng ghi chú chân bộ điều khiển tự động tính toán và hiển thị mức nền M/tháng và lượt/ngày tương ứng với % Zalo vừa nhập.
  3. **Định dạng hiển thị nhất quán (M suffix)**:
     - Tạo hàm Python `fmt_m()` để hiển thị số triệu kèm chữ `M` (ví dụ `2,09M`, `6,27M`, `33,70M`), khớp hoàn toàn với hàm JS `fmtTr()` ở client, tránh hiện tượng nhảy định dạng khi tải trang.
- **Tuân thủ Znews CMS:** Vượt qua 100% kiểm thử 6 tiêu chuẩn (0 inline style, 0 `<span>`, 0 `<button>`, 0 base64).

---

### [Cập nhật #21] — Phiên bản v2.4 (30/09/2026 22:34:11)
- **Mã Commit:** `2646ad7` (nhánh `main`) và `f58b297` (nhánh `gh-pages`)
- **Yêu cầu từ người dùng:**
  > *"Đề xuất KPI từng ban (14 ban biên tập) -> sửa thành Đề xuất KPI từng ban (14 ban). Cái khối 4 thẻ chỉ số (KPI ngày, KPI tháng, KPI Quý 4, Dự kiến cả năm 2026) bỏ xuống cuối cùng luôn."*
- **Các thay đổi thực hiện:**
  1. Đổi tiêu đề thẻ 14 ban thành: **"Đề xuất KPI từng ban (14 ban)"**.
  2. Di chuyển khối `.kpi_grid_4` (gồm 4 thẻ chỉ số tổng quan: Ngày, Tháng, Quý 4, Cả năm) từ vị trí trên bảng điều khiển xuống **cuối trang** (nằm ngay trên banner CTA tài liệu liên quan).
  3. Cập nhật lại logic JavaScript để 4 thẻ này vẫn phản ứng tức thì khi người dùng thay đổi thông số ở bảng điều khiển bên trên.

---

### [Cập nhật #20] — Phiên bản v2.3 (30/09/2026 22:26:41)
- **Mã Commit:** `af164f9` (nhánh `main`)
- **Yêu cầu từ người dùng:**
  > *"Điều chỉnh trang index như sau:*
  > *Chi tiết KPI từng ban (14 ban biên tập) -> Đổi lên đầu, Sửa thành Đề xuất KPI từng ban (14 ban biên tập)*
  > *Bảng điều khiển thông số tính toán KPI -> Đưa xuống cuối trang*
  > *Bảng tổng hợp chỉ tiêu: Ngày • tháng • quý 4/2026 & dự báo năm -> đưa lên trên bảng điều khiển. Ngày, Tháng, Quý 4 viết hoa chữ đầu"*
- **Các thay đổi thực hiện:**
  1. Sắp xếp lại thứ tự các khối trên trang `index.html`:
     - Khối 1: **Đề xuất KPI từng ban (14 ban biên tập)** (lên đầu tiên sau Header).
     - Khối 2: **Bảng tổng hợp chỉ tiêu: Ngày • Tháng • Quý 4/2026 & dự báo năm** (chuẩn hóa viết hoa đầu từ).
     - Khối 3: **Bảng điều khiển thông số tính toán KPI**.
     - Khối 4: 4 thẻ chỉ số tổng quan và CTA liên kết.

---

### [Cập nhật #19] — Phiên bản v2.2 (30/09/2026 22:16:23)
- **Mã Commit:** `ca93fff` (nhánh `main`)
- **Yêu cầu từ người dùng:**
  > *"So sánh 4 mốc tăng trưởng (+10%, +15%, +20%, +50%) theo cơ sở tháng 9. Bỏ phần này trong trang đầu tiên."*
- **Các thay đổi thực hiện:**
  1. Gỡ bỏ hoàn toàn bảng tĩnh đối chiếu 4 mốc kịch bản (+10%, +15%, +20%, +50%) khỏi trang `index.html`.
  2. Toàn bộ tính năng xem kịch bản được chuyển giao sang công cụ tương tác trực tiếp: người dùng chỉ cần bấm chip hoặc nhập số là bảng tự động hiển thị mốc tương ứng mà không làm dài trang.

---

### [Cập nhật #18] — Phiên bản v2.1 (30/09/2026 22:09:08)
- **Mã Commit:** `efe9152` (nhánh `main`)
- **Yêu cầu từ người dùng:**
  > *"Vì sao tỷ lệ từng ban tăng có 15% mà cả khối đều tăng 17,6%, logic có gì sai không?"*
- **Phân tích nguyên nhân:**
  - Tháng 9 có 30 ngày (quy đổi), Quý 4 có 92 ngày (trung bình 30,67 ngày/tháng).
  - Trước đó, code tính tỷ lệ tăng trưởng khối dựa trên tổng Quý 4 so với 3 lần tháng nền:
    $$\text{Tỷ lệ cũ} = \left(\frac{\text{KPI Quý 4}}{3 \times \text{Nền T9}} - 1\right) = \frac{92}{90} \times 1,15 - 1 = +17,6\%$$
    $\rightarrow$ Bị đội thêm $+2,6\%$ do chênh lệch 2 ngày lịch (92 ngày vs 90 ngày).
- **Giải pháp khắc phục:**
  - Quy chuẩn công thức tính tỷ lệ tăng trưởng hàm ý (implied growth rate) cho dòng khối và dòng Toàn Znews về cấp độ **KPI ngày**:
    $$\text{implied\_rate} = \left(\frac{\text{Tổng KPI ngày}}{\text{Tổng nền T9} / 30} - 1\right) \times 100\%$$
  - Kết quả: Khi toàn bộ các ban tăng đúng 15%, tỷ lệ hiển thị của khối và Toàn Znews hiển thị chính xác tuyệt đối **+15,0%**, xóa bỏ hoàn toàn sai số lịch.

---

### [Cập nhật #17] — Phiên bản v2.0 (30/09/2026 22:03:02)
- **Mã Commit:** `c4a3e88` (nhánh `main`)
- **Yêu cầu từ người dùng:**
  > *"Hãy đọc file KPI thang 9 tôi vừa lưu trong folder. Ở file này, tôi chỉ lấy dữ liệu truy cập trong tháng 9 thôi, từ đó tính KPI năm theo cách tăng tỷ lệ. Tôi đã đặt sẵn tỷ lệ 10-15-20-50%.*
  > *Tôi muốn bạn làm một trang mới trong link vừa rồi, ở đầu tiên. Trình bày lại y như trang KPI trước đó, nhưng chỉ lấy dữ liệu từ tháng 9.*
  > *Ngoài việc có các tỷ lệ đặt sẵn, hãy cho tôi một ô để nhập tỷ lệ tăng trưởng. Cho tôi toggle 'Áp tỷ lệ tăng toàn bộ ban' và 'Tỷ lệ tăng tùy từng ban'.*
  > *Ngoài ra, cho tùy chọn bật/tắt ảnh hưởng Zalo: Zalo thực tế (1-2%), Zalo giả định (5%)."*
- **Các thay đổi thực hiện:**
  1. Trích xuất toàn bộ dữ liệu từ file `KPI thang 9.xlsx`:
     - 29 ngày dữ liệu thực tế tháng 9 quy đổi đủ 30 ngày cho 14 ban biên tập.
     - Lũy kế 9 tháng thực tế (`lk_9t`) và số thực hiện cả năm 2025 (`yr_2025`).
  2. Thiết lập cấu trúc hệ thống 3 trang (3-page portal):
     - `index.html`: Công cụ tính toán tương tác thời gian thực từ dữ liệu tháng 9.
     - `kpi_phe_duyet.html`: Bảng giao chỉ tiêu đã phê duyệt theo TB T8–T9 (98,73M).
     - `detail.html`: Báo cáo giải trình chi tiết 3 phần và phân tích 2 đòn bẩy.
  3. Xây dựng bộ điều khiển KPI tương tác (`control_panel_card`):
     - Tùy chọn trừ Zalo: Thực tế (2,13%), Giả định (5,0%), Không trừ (gốc T9).
     - Chế độ áp tỷ lệ: Toàn bộ ban vs Tùy chỉnh từng ban.
     - Tỷ lệ tăng trưởng: Chip nhanh (+10%, +15%, +20%, +50%) và ô nhập số tự do.
     - Ô nhập tỷ lệ trực tiếp tại từng thẻ ban và từng dòng bảng khi ở chế độ tùy chỉnh.
  4. Thanh điều hướng Top bar (`.top_bar_nav`) gắn trên đầu cả 3 trang.

---

### [Cập nhật #16] — Phiên bản v1.6 (30/09/2026 21:37:58)
- **Mã Commit:** `7c0b6b1` (nhánh `main`)
- **Yêu cầu từ người dùng:**
  > *"Xuất lại tài liệu mô tả vào trong folder để có thể tạo website khác khi cần."*
- **Các thay đổi thực hiện:**
  1. Soạn thảo tài liệu `README.md`: Tổng quan dự án, liên kết live, kiến trúc file, công thức tính toán và quy chuẩn kỹ thuật.
  2. Soạn thảo cẩm nang kỹ thuật `HUONG_DAN_TAO_WEBSITE_KPI.md`: Hướng dẫn chi tiết từng bước tạo website KPI tương tự (chuẩn bị dữ liệu JSON, thiết kế SVG inline, xây dựng CSS scoped, bộ quy tắc Znews CMS và quy trình deploy GitHub Pages).

---

### [Cập nhật #15] — Phiên bản v1.5 (30/09/2026 11:13:33)
- **Mã Commit:** `67b2b39` (nhánh `main`)
- **Yêu cầu từ người dùng:**
  > *"Điều chỉnh lại title và trong file. Znews là Tạp chí điện tử Tri thức - Znews. Không phải Báo điện tử."*
- **Các thay đổi thực hiện:**
  1. Rà soát và thay thế toàn bộ danh xưng *"Báo điện tử"* thành **"Tạp chí điện tử Tri thức - Znews"** trong `<title>`, thẻ meta, header kicker, footer và nội dung báo cáo giải trình trên toàn bộ các trang.

---

### [Cập nhật #14] — Phiên bản v1.4 (30/09/2026 10:53:01)
- **Mã Commit:** `29d4185` (nhánh `main`)
- **Yêu cầu từ người dùng:**
  > *"Thẻ Giao Chỉ Tiêu Từng Ban Biên Tập (14 Ban) -> Sửa thành 'Chi tiết KPI từng ban'. Ngoài ra cần sửa theo đúng kiểu chính tả tiếng Việt, chỉ viết hoa chữ đầu tiên trong câu, không được viết hoa từng từ."*
- **Các thay đổi thực hiện:**
  1. Đổi tiêu đề thẻ thành: **"Chi tiết KPI từng ban"**.
  2. Rà soát toàn bộ các tiêu đề, thẻ tag, bảng biểu: Áp dụng triệt để quy tắc chính tả tiếng Việt (sentence-case), loại bỏ hoàn toàn lối viết hoa từng từ (Title Case kiểu tiếng Anh).

---

### [Cập nhật #13] — Phiên bản v1.3 (30/09/2026 09:31:07)
- **Mã Commit:** `4349710` (nhánh `main`)
- **Yêu cầu từ người dùng:**
  - Tối giản trang chủ giao chỉ tiêu: Tập trung vào số liệu thực chất.
  - Chuyển đơn vị hiển thị về triệu lượt xem (**M**), rút gọn cột, loại bỏ văn bản giải thích dài dòng để lãnh đạo và ban biên tập dễ tra cứu nhanh.

---

### [Cập nhật #12] — Phiên bản v1.2 (30/09/2026 09:05:12)
- **Mã Commit:** `cce2ff5` (nhánh `main`)
- **Yêu cầu từ người dùng:**
  - Tách nội dung giao chỉ tiêu và báo cáo giải thích thành 2 trang độc lập:
    * `index.html`: Dành cho giao ban và theo dõi số liệu thực thi.
    * `detail.html`: Dành cho phân tích bối cảnh, lý do điều chỉnh và giải thích thuật toán/đòn bẩy.

---

### [Cập nhật #1 đến #11] — Giai đoạn Xây dựng Ban đầu (29/09/2026)
- **29/09 16:52 (`7d66f0d`):** Khởi tạo trang dashboard tĩnh đầu tiên dựa trên bản brief yêu cầu.
- **29/09 16:53 (`0fc32aa`):** Hoàn thiện dashboard responsive, cấu trúc CSS scoped `.container_AI`.
- **29/09 17:29 (`c19e1e5`):** Thêm file `.nojekyll` hỗ trợ GitHub Pages render đúng định dạng.
- **29/09 17:42 (`0612fa7`):** Căn chỉnh Section 03 loại bỏ lỗi đè chữ trên biểu đồ sụt giảm.
- **29/09 17:56 (`52653d1`):** Bổ sung 2 kịch bản KPI Quý 4 (+20% và +50%).
- **29/09 18:05 (`0ad72aa`):** Xử lý lỗi đè chữ trên biểu đồ dumbbell 7T và cả năm 2026.
- **29/09 18:53 (`b2ccb03`):** Hiệu chỉnh số liệu lịch sử của ban Lifestyle (bỏ đột biến lỗi hệ thống ngày 08/12/2025).
- **29/09 19:08 (`620bb60`):** Cấu trúc lại báo cáo theo format 3 phần chuyên nghiệp: Phân tích 9T, Thực trạng sụt giảm, Đòn bẩy Zalo OA & Google.
- **29/09 19:18 (`afa893b`):** Bổ sung class `.is_hidden` xử lý lọc dữ liệu bảng tiến độ 19 đơn vị.
- **29/09 19:41 (`e382a3e`):** Chuẩn hóa định dạng số tiếng Việt trong biểu đồ SVG grouped bar chart.

---

## 🛠️ Quy Chuẩn Kỹ Thuật Bắt Buộc Khi Cập Nhật Tiếp Theo

Khi thực hiện bất kỳ cập nhật nào trên codebase này, bắt buộc phải bảo đảm các nguyên tắc sau:
1. **Quy chuẩn Znews CMS (Bộ lọc Validator tự động):**
   - Không dùng `style=""` trực tiếp trên thẻ HTML.
   - Không dùng thẻ `<span>` (thay bằng `<strong>`, `<em>`, `<div>`, `<small>`).
   - Không dùng thẻ `<button>` (thay bằng `<div class="chip">` hoặc `<a class="chip">`).
   - Không nhúng ảnh base64/raster; toàn bộ biểu đồ bắt buộc vẽ bằng SVG vector inline.
2. **Quy tắc chính tả tiếng Việt:**
   - Chỉ viết hoa chữ cái đầu câu và danh từ riêng; không viết hoa chữ cái đầu của từng từ (Title Case kiểu tiếng Anh).
   - Tên cơ quan báo chí bắt buộc là: **Tạp chí điện tử Tri thức - Znews**.
3. **Quy trình xuất bản tự động:**
   - Chỉnh sửa logic trong file master: `generate_full_dashboard.py`.
   - Chạy `python3 generate_full_dashboard.py` để sinh ra các file HTML và chạy qua bộ validator.
   - Commit & push đồng thời trên 2 nhánh: `main` (lưu trữ mã nguồn) và `gh-pages` (triển khai live website).

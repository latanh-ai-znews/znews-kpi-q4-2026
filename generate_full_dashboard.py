# -*- coding: utf-8 -*-
"""
Production-grade generator for Znews Q4 2026 Static Dashboard:
- 3-Part Architecture with Sticky Navigation Tabs (#part1, #part2, #part3)
- Section 01: Diễn biến truy cập theo tháng (2025–2026)
- Section 02: Tăng trưởng 7 tháng đầu năm (Giai đoạn trước biến động)
- Section 03: Mức độ sụt giảm T8–T9/2026 sau biến động
- Section 04: Tiến độ thực hiện KPI năm 2026 theo ban & Cú sốc tháng 8 (MỚI)
- Section 05: Đề xuất 4 mức KPI Quý 4/2026 (Cơ sở, Phấn đấu, Thử thách, Lấy lại truy cập)
- Section 06: Kịch bản cả năm 2026 so với 2025 (4 Mức KPI)
- Section 07: Cơ sở & Lý do đề xuất KPI mới (Thực trạng hụt hơi, Đòn bẩy Zalo OA, Tín hiệu hồi phục Google)

100% compliance with Znews CMS:
- No inline style="" anywhere in HTML or JS
- No <span> tags anywhere (div/em/strong/b/small used instead)
- No <button> tags anywhere (div.chip / a.chip / a.nav_tab used instead)
- No base64 images (pure inline SVG)
- Fully responsive, mobile font size increased ~15%
- Full-bleed 100vw layout scoped in .container_AI
- Numbers formatted in Vietnamese locale (1.000,00)
- Section 03, Section 02, Section 06: zero text-bar overlap
"""
import json
import re

# 1. Load data
with open("brief_data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

meta = data["meta"]
kpi_c = data["kpi_phuong_an_C"]
t7_growth = data["tang_truong_7_thang_dau_nam"]
monthly = data["truy_cap_theo_thang"]
tien_do_kpi = data.get("tien_do_kpi_2026", [])
benchmarks = meta.get("tien_do_chuan", {"7t": 58.3, "8t": 66.7, "9t": 75.0})

def fmt_tr(val_k, dec=2):
    v = val_k / 1000.0
    return f"{v:,.{dec}f}".replace(",", "X").replace(".", ",").replace("X", ".")

def fmt_pct(p, dec=1):
    sign = "+" if p > 0 else ""
    return f"{sign}{p:.{dec}f}".replace(".", ",") + "%"

def fmt_pct_nosign(p, dec=1):
    return f"{p:.{dec}f}".replace(".", ",") + "%"

kpi_dict = {item["ten"]: item for item in kpi_c}
growth_dict = {item["ten"]: item for item in t7_growth}
tien_do_dict = {item["ten"]: item for item in tien_do_kpi}

deps_by_block = {
    "Khối Uy tín": ["Xã hội", "Pháp luật", "Thế giới", "Xuất bản"],
    "Khối Kinh doanh": ["Kinh doanh", "Công nghệ", "Xe"],
    "Khối Lifestyle": ["Đời sống", "Lifestyle", "Sức khỏe", "Giáo dục", "Du lịch"],
    "Khối Truy cập": ["Thể thao", "Giải trí"]
}

dep_block_map = {}
for blk, deps in deps_by_block.items():
    for d in deps:
        dep_block_map[d] = blk

all_deps = [
    "Xã hội", "Pháp luật", "Thế giới", "Xuất bản",
    "Kinh doanh", "Công nghệ", "Xe",
    "Đời sống", "Lifestyle", "Sức khỏe", "Giáo dục", "Du lịch",
    "Thể thao", "Giải trí"
]

all_blocks = ["Khối Uy tín", "Khối Kinh doanh", "Khối Lifestyle", "Khối Truy cập"]

# Compute 4 Tiers (+10%, +15%, +20%, +50%)
kpi_4tiers = {}
for dep in all_deps:
    raw = kpi_dict[dep]
    tb = raw["tb_thang_T8T9_2026"]
    luyke = raw["luy_ke_2026_den_29_09"]
    q4_25 = raw["q4_2025_thuc_te"]
    yr_25 = raw["ca_nam_2025"]
    
    # 10%
    m10_th = raw["muc_10"]["kpi_moi_thang"]
    m10_q4 = raw["muc_10"]["tong_q4"]
    m10_yr = raw["muc_10"]["ca_nam_2026"]
    m10_pct_q4 = raw["muc_10"]["pct_q4_vs_q4_2025"]
    m10_pct_yr = raw["muc_10"]["pct_ca_nam_vs_2025"]
    
    # 15%
    m15_th = raw["muc_15"]["kpi_moi_thang"]
    m15_q4 = raw["muc_15"]["tong_q4"]
    m15_yr = raw["muc_15"]["ca_nam_2026"]
    m15_pct_q4 = raw["muc_15"]["pct_q4_vs_q4_2025"]
    m15_pct_yr = raw["muc_15"]["pct_ca_nam_vs_2025"]

    # 20% Thử thách
    m20_th = round(tb * 1.20)
    m20_q4 = m20_th * 3
    m20_yr = luyke + m20_q4
    m20_pct_q4 = (m20_q4 / q4_25 - 1.0) * 100.0 if q4_25 else 0.0
    m20_pct_yr = (m20_yr / yr_25 - 1.0) * 100.0 if yr_25 else 0.0

    # 50% Lấy lại truy cập
    m50_th = round(tb * 1.50)
    m50_q4 = m50_th * 3
    m50_yr = luyke + m50_q4
    m50_pct_q4 = (m50_q4 / q4_25 - 1.0) * 100.0 if q4_25 else 0.0
    m50_pct_yr = (m50_yr / yr_25 - 1.0) * 100.0 if yr_25 else 0.0

    kpi_4tiers[dep] = {
        "ten": dep, "tb": tb, "luyke": luyke, "q4_25": q4_25, "yr_25": yr_25,
        "m10": {"th": m10_th, "q4": m10_q4, "yr": m10_yr, "pct_q4": m10_pct_q4, "pct_yr": m10_pct_yr},
        "m15": {"th": m15_th, "q4": m15_q4, "yr": m15_yr, "pct_q4": m15_pct_q4, "pct_yr": m15_pct_yr},
        "m20": {"th": m20_th, "q4": m20_q4, "yr": m20_yr, "pct_q4": m20_pct_q4, "pct_yr": m20_pct_yr},
        "m50": {"th": m50_th, "q4": m50_q4, "yr": m50_yr, "pct_q4": m50_pct_q4, "pct_yr": m50_pct_yr},
    }

# Compute Blocks
for blk in all_blocks:
    deps = deps_by_block[blk]
    raw = kpi_dict[blk]
    tb = raw["tb_thang_T8T9_2026"]
    luyke = raw["luy_ke_2026_den_29_09"]
    q4_25 = raw["q4_2025_thuc_te"]
    yr_25 = raw["ca_nam_2025"]
    
    m10_th = sum(kpi_4tiers[d]["m10"]["th"] for d in deps)
    m10_q4 = m10_th * 3
    m10_yr = luyke + m10_q4
    m10_pct_q4 = (m10_q4 / q4_25 - 1.0) * 100.0
    m10_pct_yr = (m10_yr / yr_25 - 1.0) * 100.0

    m15_th = sum(kpi_4tiers[d]["m15"]["th"] for d in deps)
    m15_q4 = m15_th * 3
    m15_yr = luyke + m15_q4
    m15_pct_q4 = (m15_q4 / q4_25 - 1.0) * 100.0
    m15_pct_yr = (m15_yr / yr_25 - 1.0) * 100.0

    m20_th = sum(kpi_4tiers[d]["m20"]["th"] for d in deps)
    m20_q4 = m20_th * 3
    m20_yr = luyke + m20_q4
    m20_pct_q4 = (m20_q4 / q4_25 - 1.0) * 100.0
    m20_pct_yr = (m20_yr / yr_25 - 1.0) * 100.0

    m50_th = sum(kpi_4tiers[d]["m50"]["th"] for d in deps)
    m50_q4 = m50_th * 3
    m50_yr = luyke + m50_q4
    m50_pct_q4 = (m50_q4 / q4_25 - 1.0) * 100.0
    m50_pct_yr = (m50_yr / yr_25 - 1.0) * 100.0

    kpi_4tiers[blk] = {
        "ten": blk, "tb": tb, "luyke": luyke, "q4_25": q4_25, "yr_25": yr_25,
        "m10": {"th": m10_th, "q4": m10_q4, "yr": m10_yr, "pct_q4": m10_pct_q4, "pct_yr": m10_pct_yr},
        "m15": {"th": m15_th, "q4": m15_q4, "yr": m15_yr, "pct_q4": m15_pct_q4, "pct_yr": m15_pct_yr},
        "m20": {"th": m20_th, "q4": m20_q4, "yr": m20_yr, "pct_q4": m20_pct_q4, "pct_yr": m20_pct_yr},
        "m50": {"th": m50_th, "q4": m50_q4, "yr": m50_yr, "pct_q4": m50_pct_q4, "pct_yr": m50_pct_yr},
    }

# Compute Toàn Znews
raw_toan = kpi_dict["Toàn Znews"]
toan_tb = raw_toan["tb_thang_T8T9_2026"]
toan_luyke = raw_toan["luy_ke_2026_den_29_09"]
toan_q4_25 = raw_toan["q4_2025_thuc_te"]
toan_yr_25 = raw_toan["ca_nam_2025"]

toan_m10_th = sum(kpi_4tiers[b]["m10"]["th"] for b in all_blocks)
toan_m10_q4 = toan_m10_th * 3
toan_m10_yr = toan_luyke + toan_m10_q4
toan_m10_pct_q4 = (toan_m10_q4 / toan_q4_25 - 1.0) * 100.0
toan_m10_pct_yr = (toan_m10_yr / toan_yr_25 - 1.0) * 100.0

toan_m15_th = sum(kpi_4tiers[b]["m15"]["th"] for b in all_blocks)
toan_m15_q4 = toan_m15_th * 3
toan_m15_yr = toan_luyke + toan_m15_q4
toan_m15_pct_q4 = (toan_m15_q4 / toan_q4_25 - 1.0) * 100.0
toan_m15_pct_yr = (toan_m15_yr / toan_yr_25 - 1.0) * 100.0

toan_m20_th = sum(kpi_4tiers[b]["m20"]["th"] for b in all_blocks)
toan_m20_q4 = toan_m20_th * 3
toan_m20_yr = toan_luyke + toan_m20_q4
toan_m20_pct_q4 = (toan_m20_q4 / toan_q4_25 - 1.0) * 100.0
toan_m20_pct_yr = (toan_m20_yr / toan_yr_25 - 1.0) * 100.0

toan_m50_th = sum(kpi_4tiers[b]["m50"]["th"] for b in all_blocks)
toan_m50_q4 = toan_m50_th * 3
toan_m50_yr = toan_luyke + toan_m50_q4
toan_m50_pct_q4 = (toan_m50_q4 / toan_q4_25 - 1.0) * 100.0
toan_m50_pct_yr = (toan_m50_yr / toan_yr_25 - 1.0) * 100.0

kpi_4tiers["Toàn Znews"] = {
    "ten": "Toàn Znews", "tb": toan_tb, "luyke": toan_luyke, "q4_25": toan_q4_25, "yr_25": toan_yr_25,
    "m10": {"th": toan_m10_th, "q4": toan_m10_q4, "yr": toan_m10_yr, "pct_q4": toan_m10_pct_q4, "pct_yr": toan_m10_pct_yr},
    "m15": {"th": toan_m15_th, "q4": toan_m15_q4, "yr": toan_m15_yr, "pct_q4": toan_m15_pct_q4, "pct_yr": toan_m15_pct_yr},
    "m20": {"th": toan_m20_th, "q4": toan_m20_q4, "yr": toan_m20_yr, "pct_q4": toan_m20_pct_q4, "pct_yr": toan_m20_pct_yr},
    "m50": {"th": toan_m50_th, "q4": toan_m50_q4, "yr": toan_m50_yr, "pct_q4": toan_m50_pct_q4, "pct_yr": toan_m50_pct_yr},
}

toan_t7 = growth_dict["Toàn Znews"]

col_indices = {col: i for i, col in enumerate(monthly["cot"])}
monthly_series = {}
for name in monthly["cot"][1:]:
    idx = col_indices[name]
    vals_2025 = [monthly["dong"][m][idx] for m in range(12)]
    vals_2026 = [monthly["dong"][m][idx] for m in range(12, 21)]
    monthly_series[name] = {
        "vals_2025": vals_2025,
        "vals_2026": vals_2026
    }

# ==========================================
# MINI PROGRESS BAR SVG (ZERO INLINE STYLES)
# ==========================================
def build_mini_progress_svg(pct, bench):
    W, H = 84, 6
    pct_w = max(0.0, min(float(W), (pct / 100.0) * W))
    bench_x = min(float(W), (bench / 100.0) * W)
    
    if pct >= bench:
        fill_col = "#16a34a"  # green: on track
    elif pct >= bench - 8.0:
        fill_col = "#ca8a04"  # amber: slight lag
    else:
        fill_col = "#dc2626"  # red: heavy lag
        
    return f'<svg class="prog_svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}"><rect x="0" y="0" width="{W}" height="{H}" fill="#e2e8f0" rx="3"/><rect x="0" y="0" width="{pct_w:.1f}" height="{H}" fill="{fill_col}" rx="3"/><line x1="{bench_x:.1f}" y1="0" x2="{bench_x:.1f}" y2="{H}" stroke="#0f172a" stroke-width="1.5"/></svg>'


# ==========================================
# SVG CHARTS BUILDERS (4 TIERS AWARE)
# ==========================================

def build_monthly_chart_svg():
    W, H = 960, 440
    L, R, T, B = 65, 45, 45, 60
    PW, PH = W - L - R, H - T - B
    xs = [L + i * (PW / 11.0) for i in range(12)]
    
    s25 = monthly_series["Toàn Znews"]["vals_2025"]
    s26 = monthly_series["Toàn Znews"]["vals_2026"]
    
    m10_val = kpi_4tiers["Toàn Znews"]["m10"]["th"]
    m15_val = kpi_4tiers["Toàn Znews"]["m15"]["th"]
    m20_val = kpi_4tiers["Toàn Znews"]["m20"]["th"]
    m50_val = kpi_4tiers["Toàn Znews"]["m50"]["th"]
    
    y_max = 90000.0
    def get_y(val):
        return T + PH - (val / y_max) * PH

    svg = []
    svg.append(f'<svg id="monthly_svg" class="chart_svg" viewBox="0 0 {W} {H}" width="100%" height="auto" xmlns="http://www.w3.org/2000/svg">')
    svg.append('<defs>')
    svg.append('  <linearGradient id="bandGrad" x1="0" y1="0" x2="0" y2="1">')
    svg.append('    <stop offset="0%" stop-color="#fff1f2" stop-opacity="0.9"/>')
    svg.append('    <stop offset="100%" stop-color="#fff1f2" stop-opacity="0.3"/>')
    svg.append('  </linearGradient>')
    svg.append('  <linearGradient id="targetGrad" x1="0" y1="0" x2="0" y2="1">')
    svg.append('    <stop offset="0%" stop-color="#e0e7ff" stop-opacity="0.7"/>')
    svg.append('    <stop offset="100%" stop-color="#e0e7ff" stop-opacity="0.1"/>')
    svg.append('  </linearGradient>')
    svg.append('</defs>')

    y_ticks = [0, 20000, 40000, 60000, 80000]
    for yt in y_ticks:
        y_pos = get_y(yt)
        svg.append(f'<line class="grid_line" x1="{L}" y1="{y_pos:.1f}" x2="{W-R}" y2="{y_pos:.1f}" stroke="#e9ebf1" stroke-width="1" stroke-dasharray="3,3"/>')
        label_text = f"{int(yt/1000)} tr"
        svg.append(f'<text class="axis_label_y" x="{L-12}" y="{y_pos+4:.1f}" text-anchor="end" fill="#6c7280" font-size="12" font-family="Manrope">{label_text}</text>')

    band_x1 = xs[7] - (PW / 22.0)
    band_w = (PW / 11.0) * 2.0
    svg.append(f'<rect class="event_band" x="{band_x1:.1f}" y="{T}" width="{band_w:.1f}" height="{PH}" fill="url(#bandGrad)" stroke="#fecdd3" stroke-width="1" rx="6"/>')
    svg.append(f'<text class="event_label" x="{xs[7] + (PW/22.0):.1f}" y="{T+22}" text-anchor="middle" fill="#c2410c" font-size="12" font-weight="700" font-family="Be Vietnam Pro">⚡ Biến động từ T8/2026</text>')

    for i in range(12):
        svg.append(f'<text class="axis_label_x" x="{xs[i]:.1f}" y="{H-22}" text-anchor="middle" fill="#14161c" font-size="12" font-weight="600" font-family="Be Vietnam Pro">T{i+1}</text>')

    pts_25 = " ".join([f"{xs[i]:.1f},{get_y(s25[i]):.1f}" for i in range(12)])
    svg.append(f'<path id="path_2025" d="M {pts_25.replace(" ", " L ")}" fill="none" stroke="#94a3b8" stroke-width="2.5" stroke-dasharray="5,4" stroke-linecap="round"/>')

    pts_26 = " ".join([f"{xs[i]:.1f},{get_y(s26[i]):.1f}" for i in range(9)])
    svg.append(f'<path id="path_2026" d="M {pts_26.replace(" ", " L ")}" fill="none" stroke="#3b56e0" stroke-width="3.5" stroke-linecap="round"/>')

    y_t9 = get_y(s26[8])
    y_m10 = get_y(m10_val)
    y_m20 = get_y(m20_val)
    y_m50 = get_y(m50_val)

    pts_poly = f"{xs[8]:.1f},{y_t9:.1f} {xs[9]:.1f},{y_m50:.1f} {xs[10]:.1f},{y_m50:.1f} {xs[11]:.1f},{y_m50:.1f} {xs[11]:.1f},{y_m10:.1f} {xs[10]:.1f},{y_m10:.1f} {xs[9]:.1f},{y_m10:.1f} {xs[8]:.1f},{y_t9:.1f}"
    svg.append(f'<polygon id="poly_target" points="{pts_poly}" fill="url(#targetGrad)"/>')

    path_target_m10 = f"M {xs[8]:.1f},{y_t9:.1f} L {xs[9]:.1f},{y_m10:.1f} L {xs[10]:.1f},{y_m10:.1f} L {xs[11]:.1f},{y_m10:.1f}"
    svg.append(f'<path id="path_target_m10" d="{path_target_m10}" fill="none" stroke="#3b56e0" stroke-width="2" stroke-dasharray="4,4" stroke-linecap="round"/>')

    path_target_m20 = f"M {xs[8]:.1f},{y_t9:.1f} L {xs[9]:.1f},{y_m20:.1f} L {xs[10]:.1f},{y_m20:.1f} L {xs[11]:.1f},{y_m20:.1f}"
    svg.append(f'<path id="path_target_m20" d="{path_target_m20}" fill="none" stroke="#6366f1" stroke-width="1.5" stroke-dasharray="3,3" stroke-linecap="round"/>')

    path_target_m50 = f"M {xs[8]:.1f},{y_t9:.1f} L {xs[9]:.1f},{y_m50:.1f} L {xs[10]:.1f},{y_m50:.1f} L {xs[11]:.1f},{y_m50:.1f}"
    svg.append(f'<path id="path_target_m50" d="{path_target_m50}" fill="none" stroke="#1e1b4b" stroke-width="2.5" stroke-dasharray="5,4" stroke-linecap="round"/>')

    for i in range(12):
        svg.append(f'<circle class="dot_2025" cx="{xs[i]:.1f}" cy="{get_y(s25[i]):.1f}" r="4" fill="#94a3b8" stroke="#ffffff" stroke-width="1.5"/>')

    for i in range(9):
        col = "#c2410c" if i >= 7 else "#3b56e0"
        r_size = 5.5 if i >= 7 else 4.5
        svg.append(f'<circle class="dot_2026" cx="{xs[i]:.1f}" cy="{get_y(s26[i]):.1f}" r="{r_size}" fill="{col}" stroke="#ffffff" stroke-width="2"/>')

    for i in range(9, 12):
        svg.append(f'<circle class="dot_target_10" cx="{xs[i]:.1f}" cy="{y_m10:.1f}" r="4" fill="#3b56e0" stroke="#ffffff" stroke-width="1.5"/>')
        svg.append(f'<circle class="dot_target_20" cx="{xs[i]:.1f}" cy="{y_m20:.1f}" r="3.5" fill="#6366f1" stroke="#ffffff" stroke-width="1.5"/>')
        svg.append(f'<circle class="dot_target_50" cx="{xs[i]:.1f}" cy="{y_m50:.1f}" r="4.5" fill="#1e1b4b" stroke="#ffffff" stroke-width="2"/>')

    svg.append(f'<text id="lbl_t1" class="chart_val_lbl" x="{xs[0]:.1f}" y="{get_y(s26[0])-12:.1f}" text-anchor="middle" fill="#3b56e0" font-size="12" font-weight="700" font-family="Manrope">{fmt_tr(s26[0], 1)} tr</text>')
    svg.append(f'<text id="lbl_t8" class="chart_val_lbl" x="{xs[7]:.1f}" y="{get_y(s26[7])-12:.1f}" text-anchor="middle" fill="#c2410c" font-size="12" font-weight="700" font-family="Manrope">{fmt_tr(s26[7], 1)} tr</text>')
    svg.append(f'<text id="lbl_t9" class="chart_val_lbl" x="{xs[8]:.1f}" y="{y_t9+18:.1f}" text-anchor="middle" fill="#c2410c" font-size="12" font-weight="700" font-family="Manrope">{fmt_tr(s26[8], 1)} tr</text>')
    svg.append(f'<text id="lbl_target" class="chart_val_lbl" x="{xs[11]:.1f}" y="{y_m50-12:.1f}" text-anchor="end" fill="#1e1b4b" font-size="12" font-weight="800" font-family="Manrope">Dải mục tiêu Q4: {fmt_tr(m10_val, 1)}–{fmt_tr(m50_val, 1)} tr/tháng</text>')

    svg.append('</svg>')
    return "\n".join(svg)


def build_t7_growth_bar_svg():
    sorted_deps = sorted(all_deps, key=lambda d: growth_dict[d]["pct_7t"], reverse=True)
    W, H = 560, 530
    row_h = 32
    top_offset = 48
    x_zero = 315
    scale = 1.9
    
    svg = []
    svg.append(f'<svg class="chart_svg" viewBox="0 0 {W} {H}" width="100%" height="auto" xmlns="http://www.w3.org/2000/svg">')
    
    # Headers
    svg.append(f'<text x="16" y="24" fill="#64748b" font-size="11" font-weight="700" font-family="Be Vietnam Pro">ĐƠN VỊ</text>')
    svg.append(f'<text x="145" y="24" text-anchor="end" fill="#64748b" font-size="11" font-weight="700" font-family="Be Vietnam Pro">% 7T</text>')
    svg.append(f'<text x="505" y="24" text-anchor="middle" fill="#64748b" font-size="11" font-weight="700" font-family="Be Vietnam Pro">ĐÁNH GIÁ</text>')

    for ref_pct in [-40, -20, 20, 40, 60]:
        rx = x_zero + ref_pct * scale
        svg.append(f'<line x1="{rx:.1f}" y1="36" x2="{rx:.1f}" y2="{top_offset + 14 * row_h}" stroke="#f1f5f9" stroke-width="1" stroke-dasharray="2,2"/>')
        ref_txt = f"+{ref_pct}%" if ref_pct > 0 else f"{ref_pct}%"
        svg.append(f'<text x="{rx:.1f}" y="24" text-anchor="middle" fill="#94a3b8" font-size="10" font-weight="600" font-family="Manrope">{ref_txt}</text>')

    svg.append(f'<line x1="{x_zero}" y1="34" x2="{x_zero}" y2="{top_offset + 14 * row_h}" stroke="#94a3b8" stroke-width="1.5"/>')
    svg.append(f'<text x="{x_zero}" y="24" text-anchor="middle" fill="#14161c" font-size="11" font-weight="800" font-family="Manrope">0%</text>')

    for i, name in enumerate(sorted_deps):
        y = top_offset + i * row_h
        item = growth_dict[name]
        pct = item["pct_7t"]
        danh_gia = item["danh_gia"]
        bar_len = abs(pct) * scale
        
        # Row zebra background
        if i % 2 == 1:
            svg.append(f'<rect x="8" y="{y-14}" width="{W-16}" height="{row_h}" fill="#f8fafc" rx="4"/>')
            
        # 1. Department name (Column 1: x=16..90)
        weight = "700" if pct > 0 else "600"
        svg.append(f'<text x="16" y="{y+4}" fill="#14161c" font-size="12.5" font-weight="{weight}" font-family="Be Vietnam Pro">{name}</text>')
        
        # 2. Percentage text (Column 2: x=100..145)
        val_col = "#15803d" if pct > 10 else ("#3b56e0" if pct > 0 else "#c2410c")
        svg.append(f'<text x="145" y="{y+4}" text-anchor="end" fill="{val_col}" font-size="11.5" font-weight="700" font-family="Manrope">{fmt_pct(pct)}</text>')

        # 3. Bar in dedicated region (Column 3: x=219..436)
        if pct >= 0:
            fill_col = "#16a34a" if pct > 10 else "#3b56e0"
            bx = x_zero
        else:
            fill_col = "#c2410c" if pct < -20 else "#ea580c"
            bx = x_zero - bar_len
        svg.append(f'<rect x="{bx:.1f}" y="{y-7}" width="{bar_len:.1f}" height="14" fill="{fill_col}" rx="3"/>')

        # 4. Badge in dedicated column (Column 4: x=460..550)
        badge_bg = "#ecfdf5" if "Vượt" in danh_gia else ("#eff6ff" if "Đạt" in danh_gia else ("#fffbeb" if "dưới" in danh_gia else "#fef2f2"))
        badge_fg = "#15803d" if "Vượt" in danh_gia else ("#1d4ed8" if "Đạt" in danh_gia else ("#b45309" if "dưới" in danh_gia else "#991b1b"))
        svg.append(f'<rect x="460" y="{y-10}" width="90" height="20" fill="{badge_bg}" rx="10"/>')
        svg.append(f'<text x="505" y="{y+4}" text-anchor="middle" fill="{badge_fg}" font-size="10.5" font-weight="700" font-family="Be Vietnam Pro">{danh_gia}</text>')

    svg.append('</svg>')
    return "\n".join(svg)


def build_t7_dumbbell_svg():
    W, H = 510, 480
    top_offset = 60
    row_h = 75
    
    rows = [
        {"name": "Khối Truy cập", "t7_25": 178267, "t7_26": 182595, "pct": 2.4},
        {"name": "Khối Lifestyle", "t7_25": 102010, "t7_26": 101203, "pct": -0.8},
        {"name": "Khối Kinh doanh", "t7_25": 74972, "t7_26": 62797, "pct": -16.2},
        {"name": "Khối Uy tín", "t7_25": 115465, "t7_26": 93306, "pct": -19.2},
        {"name": "Toàn Znews", "t7_25": 470714, "t7_26": 439901, "pct": -6.5}
    ]
    
    max_val = 500000
    scale = (W - 170) / max_val
    
    svg = []
    svg.append(f'<svg class="chart_svg" viewBox="0 0 {W} {H}" width="100%" height="auto" xmlns="http://www.w3.org/2000/svg">')
    svg.append('<circle cx="150" cy="22" r="5" fill="#94a3b8"/>')
    svg.append('<text x="162" y="26" fill="#6c7280" font-size="12" font-family="Be Vietnam Pro">7T/2025</text>')
    svg.append('<circle cx="250" cy="22" r="5" fill="#3b56e0"/>')
    svg.append('<text x="262" y="26" fill="#3b56e0" font-size="12" font-weight="700" font-family="Be Vietnam Pro">7T/2026</text>')

    for i, r in enumerate(rows):
        y = top_offset + i * row_h
        is_total = (r["name"] == "Toàn Znews")
        bg_col = "#eef2ff" if is_total else ("#f8fafc" if i % 2 == 1 else "#ffffff")
        stroke_col = "#c7d2fe" if is_total else "#e9ebf1"
        svg.append(f'<rect x="10" y="{y-18}" width="{W-20}" height="{row_h-8}" fill="{bg_col}" stroke="{stroke_col}" stroke-width="1" rx="10"/>')
        
        font_weight = "800" if is_total else "700"
        title_fill = "#3b56e0" if is_total else "#14161c"
        title_size = "14" if is_total else "13"
        svg.append(f'<text x="24" y="{y+6}" fill="{title_fill}" font-size="{title_size}" font-weight="{font_weight}" font-family="Be Vietnam Pro">{r["name"]}</text>')
        
        x25 = 140 + r["t7_25"] * scale
        x26 = 140 + r["t7_26"] * scale
        line_col = "#22c55e" if r["pct"] > 0 else "#f87171"
        svg.append(f'<line x1="{x25:.1f}" y1="{y+6}" x2="{x26:.1f}" y2="{y+6}" stroke="{line_col}" stroke-width="4" stroke-linecap="round"/>')
        svg.append(f'<circle cx="{x25:.1f}" cy="{y+6}" r="6.5" fill="#94a3b8" stroke="#ffffff" stroke-width="1.5"/>')
        svg.append(f'<circle cx="{x26:.1f}" cy="{y+6}" r="7.5" fill="#3b56e0" stroke="#ffffff" stroke-width="2"/>')
        
        svg.append(f'<text x="{x25:.1f}" y="{y+26}" text-anchor="middle" fill="#64748b" font-size="11" font-weight="600" font-family="Manrope">{fmt_tr(r["t7_25"], 1)} tr</text>')
        svg.append(f'<text x="{x26:.1f}" y="{y-6}" text-anchor="middle" fill="#3b56e0" font-size="12" font-weight="800" font-family="Manrope">{fmt_tr(r["t7_26"], 1)} tr</text>')

        badge_bg = "#ecfdf5" if r["pct"] > 0 else "#fef2f2"
        badge_fg = "#15803d" if r["pct"] > 0 else "#c2410c"
        svg.append(f'<rect x="425" y="{y-7}" width="65" height="24" fill="{badge_bg}" rx="12"/>')
        svg.append(f'<text x="457" y="{y+9}" text-anchor="middle" fill="{badge_fg}" font-size="12" font-weight="800" font-family="Manrope">{fmt_pct(r["pct"])}</text>')

    svg.append('</svg>')
    return "\n".join(svg)


# =========================================================================
# SECTION 03: MỨC ĐỘ SỤT GIẢM T8-T9/2026 (ZERO TEXT OVERLAP)
# =========================================================================
def build_drop_t8t9_svg():
    sorted_by_drop = sorted(all_deps, key=lambda d: growth_dict[d]["pct_T8T9_2026_vs_cung_ky"])
    
    W, H = 960, 520
    top_offset = 55
    row_h = 31
    x_zero = 240
    scale = 7.5
    
    svg = []
    svg.append(f'<svg class="chart_svg" viewBox="0 0 {W} {H}" width="100%" height="auto" xmlns="http://www.w3.org/2000/svg">')
    svg.append(f'<line x1="{x_zero}" y1="{top_offset-20}" x2="{x_zero}" y2="{top_offset + 14 * row_h}" stroke="#14161c" stroke-width="1.5"/>')
    svg.append(f'<text x="{x_zero}" y="{top_offset-28}" text-anchor="middle" fill="#14161c" font-size="12" font-weight="700" font-family="Manrope">0%</text>')

    for ref_pct in [-20, -40, -60, -80]:
        rx = x_zero + abs(ref_pct) * scale
        svg.append(f'<line x1="{rx:.1f}" y1="{top_offset-15}" x2="{rx:.1f}" y2="{top_offset + 14 * row_h}" stroke="#e2e8f0" stroke-width="1" stroke-dasharray="3,3"/>')
        svg.append(f'<text x="{rx:.1f}" y="{top_offset-28}" text-anchor="middle" fill="#94a3b8" font-size="11" font-weight="600" font-family="Manrope">{ref_pct}%</text>')

    site_avg_pct = 58.1
    rx_avg = x_zero + site_avg_pct * scale
    svg.append(f'<line x1="{rx_avg:.1f}" y1="{top_offset-15}" x2="{rx_avg:.1f}" y2="{top_offset + 14 * row_h}" stroke="#c2410c" stroke-width="1.5" stroke-dasharray="4,3"/>')
    svg.append(f'<rect x="{rx_avg-65:.1f}" y="{top_offset-48}" width="130" height="20" fill="#fff1f2" stroke="#fecdd3" stroke-width="1" rx="4"/>')
    svg.append(f'<text x="{rx_avg:.1f}" y="{top_offset-34}" text-anchor="middle" fill="#c2410c" font-size="10.5" font-weight="700" font-family="Be Vietnam Pro">TB Toàn trang: -58,1%</text>')

    for i, name in enumerate(sorted_by_drop):
        y = top_offset + i * row_h
        item = growth_dict[name]
        pct = item["pct_T8T9_2026_vs_cung_ky"]
        blk = dep_block_map[name]
        blk_short = blk.replace("Khối ", "")
        
        if i % 2 == 1:
            svg.append(f'<rect x="10" y="{y-14}" width="{W-20}" height="{row_h}" fill="#f8fafc" rx="4"/>')
            
        svg.append(f'<text x="20" y="{y+4}" fill="#14161c" font-size="13" font-weight="700" font-family="Be Vietnam Pro">{name}</text>')
        svg.append(f'<rect x="135" y="{y-9}" width="85" height="19" fill="#eef2f6" rx="5"/>')
        svg.append(f'<text x="177" y="{y+4}" text-anchor="middle" fill="#64748b" font-size="11" font-weight="600" font-family="Be Vietnam Pro">{blk_short}</text>')
        
        bar_len = abs(pct) * scale
        fill_col = "#fb923c" if pct > -45 else ("#ea580c" if pct > -60 else "#c2410c")
        svg.append(f'<rect x="{x_zero}" y="{y-8}" width="{bar_len:.1f}" height="16" fill="{fill_col}" rx="3"/>')
        
        val_x = x_zero + bar_len + 8
        svg.append(f'<text x="{val_x:.1f}" y="{y+4}" text-anchor="start" fill="{fill_col}" font-size="12" font-weight="800" font-family="Manrope">{fmt_pct(pct)}</text>')

    svg.append('</svg>')
    return "\n".join(svg)


# =========================================================================
# SECTION 05 (OLD 04): GROUPED BAR CHART (TB vs +10% vs +20% vs +50%)
# =========================================================================
def build_kpi_comparison_svg():
    W, H = 960, 520
    top_offset = 40
    row_h = 32
    scale = 32.0
    bx = 180
    
    svg = []
    svg.append(f'<svg class="chart_svg" viewBox="0 0 {W} {H}" width="100%" height="auto" xmlns="http://www.w3.org/2000/svg">')
    
    svg.append('<rect x="180" y="10" width="12" height="12" fill="#cbd5e1" rx="2"/>')
    svg.append('<text x="198" y="21" fill="#64748b" font-size="11.5" font-weight="600" font-family="Be Vietnam Pro">TB T8–T9</text>')

    svg.append('<rect x="290" y="10" width="12" height="12" fill="#818cf8" rx="2"/>')
    svg.append('<text x="308" y="21" fill="#4338ca" font-size="11.5" font-weight="600" font-family="Be Vietnam Pro">+10% Cơ sở</text>')
    
    svg.append('<rect x="420" y="10" width="12" height="12" fill="#3b56e0" rx="2"/>')
    svg.append('<text x="438" y="21" fill="#1e293b" font-size="11.5" font-weight="600" font-family="Be Vietnam Pro">+20% Thử thách</text>')

    svg.append('<rect x="570" y="10" width="12" height="12" fill="#1e1b4b" rx="2"/>')
    svg.append('<text x="588" y="21" fill="#1e1b4b" font-size="11.5" font-weight="800" font-family="Be Vietnam Pro">+50% Lấy lại truy cập</text>')

    for i, name in enumerate(all_deps):
        y = top_offset + i * row_h
        item = kpi_4tiers[name]
        tb = item["tb"] / 1000.0
        m10 = item["m10"]["th"] / 1000.0
        m20 = item["m20"]["th"] / 1000.0
        m50 = item["m50"]["th"] / 1000.0
        
        w_tb = tb * scale
        w_m10 = m10 * scale
        w_m20 = m20 * scale
        w_m50 = m50 * scale
        
        if i % 2 == 1:
            svg.append(f'<rect x="10" y="{y-14}" width="{W-20}" height="{row_h}" fill="#f8fafc" rx="4"/>')
            
        svg.append(f'<text x="20" y="{y+4}" fill="#14161c" font-size="13" font-weight="700" font-family="Be Vietnam Pro">{name}</text>')
        
        svg.append(f'<rect x="{bx}" y="{y-8}" width="{w_m50:.1f}" height="17" fill="#1e1b4b" rx="3"/>')
        svg.append(f'<rect x="{bx}" y="{y-8}" width="{w_m20:.1f}" height="17" fill="#3b56e0" rx="3"/>')
        svg.append(f'<rect x="{bx}" y="{y-8}" width="{w_m10:.1f}" height="17" fill="#818cf8" rx="3"/>')
        svg.append(f'<rect x="{bx}" y="{y-8}" width="{w_tb:.1f}" height="17" fill="#cbd5e1" rx="3"/>')
        
        val_txt = f"{fmt_tr(item['tb'], 2)} → {fmt_tr(item['m10']['th'], 2)} | {fmt_tr(item['m20']['th'], 2)} | {fmt_tr(item['m50']['th'], 2)} tr"
        svg.append(f'<text x="{bx + w_m50 + 10:.1f}" y="{y+5}" fill="#14161c" font-size="11" font-weight="700" font-family="Manrope">{val_txt}</text>')

    svg.append('</svg>')
    return "\n".join(svg)


# =========================================================================
# SECTION 06 (OLD 05): YEAR DUMBBELL & GROWTH
# =========================================================================
def build_year_dumbbell_svg():
    W, H = 510, 480
    top_offset = 60
    row_h = 75
    
    rows = [
        {"name": "Khối Truy cập", "y25": kpi_4tiers["Khối Truy cập"]["yr_25"], "y26_10": kpi_4tiers["Khối Truy cập"]["m10"]["yr"], "y26_50": kpi_4tiers["Khối Truy cập"]["m50"]["yr"], "pct_10": kpi_4tiers["Khối Truy cập"]["m10"]["pct_yr"], "pct_50": kpi_4tiers["Khối Truy cập"]["m50"]["pct_yr"]},
        {"name": "Khối Lifestyle", "y25": kpi_4tiers["Khối Lifestyle"]["yr_25"], "y26_10": kpi_4tiers["Khối Lifestyle"]["m10"]["yr"], "y26_50": kpi_4tiers["Khối Lifestyle"]["m50"]["yr"], "pct_10": kpi_4tiers["Khối Lifestyle"]["m10"]["pct_yr"], "pct_50": kpi_4tiers["Khối Lifestyle"]["m50"]["pct_yr"]},
        {"name": "Khối Uy tín", "y25": kpi_4tiers["Khối Uy tín"]["yr_25"], "y26_10": kpi_4tiers["Khối Uy tín"]["m10"]["yr"], "y26_50": kpi_4tiers["Khối Uy tín"]["m50"]["yr"], "pct_10": kpi_4tiers["Khối Uy tín"]["m10"]["pct_yr"], "pct_50": kpi_4tiers["Khối Uy tín"]["m50"]["pct_yr"]},
        {"name": "Khối Kinh doanh", "y25": kpi_4tiers["Khối Kinh doanh"]["yr_25"], "y26_10": kpi_4tiers["Khối Kinh doanh"]["m10"]["yr"], "y26_50": kpi_4tiers["Khối Kinh doanh"]["m50"]["yr"], "pct_10": kpi_4tiers["Khối Kinh doanh"]["m10"]["pct_yr"], "pct_50": kpi_4tiers["Khối Kinh doanh"]["m50"]["pct_yr"]},
        {"name": "Toàn Znews", "y25": kpi_4tiers["Toàn Znews"]["yr_25"], "y26_10": kpi_4tiers["Toàn Znews"]["m10"]["yr"], "y26_50": kpi_4tiers["Toàn Znews"]["m50"]["yr"], "pct_10": kpi_4tiers["Toàn Znews"]["m10"]["pct_yr"], "pct_50": kpi_4tiers["Toàn Znews"]["m50"]["pct_yr"]}
    ]
    
    max_val = 850000
    scale = (W - 180) / max_val
    
    svg = []
    svg.append(f'<svg class="chart_svg" viewBox="0 0 {W} {H}" width="100%" height="auto" xmlns="http://www.w3.org/2000/svg">')
    svg.append('<circle cx="120" cy="22" r="5" fill="#94a3b8"/>')
    svg.append('<text x="132" y="26" fill="#6c7280" font-size="12" font-family="Be Vietnam Pro">Cả năm 2025</text>')
    svg.append('<circle cx="230" cy="22" r="5" fill="#3b56e0"/>')
    svg.append('<text x="242" y="26" fill="#14161c" font-size="12" font-weight="600" font-family="Be Vietnam Pro">Mức +10%</text>')
    svg.append('<circle cx="340" cy="22" r="5" fill="#1e1b4b"/>')
    svg.append('<text x="352" y="26" fill="#1e1b4b" font-size="12" font-weight="800" font-family="Be Vietnam Pro">Mức +50% (Phục hồi)</text>')

    for i, r in enumerate(rows):
        y = top_offset + i * row_h
        is_total = (r["name"] == "Toàn Znews")
        bg_col = "#eef2ff" if is_total else ("#f8fafc" if i % 2 == 1 else "#ffffff")
        stroke_col = "#c7d2fe" if is_total else "#e9ebf1"
        svg.append(f'<rect x="10" y="{y-18}" width="{W-20}" height="{row_h-8}" fill="{bg_col}" stroke="{stroke_col}" stroke-width="1" rx="10"/>')
        
        font_weight = "800" if is_total else "700"
        title_fill = "#3b56e0" if is_total else "#14161c"
        title_size = "14" if is_total else "13"
        svg.append(f'<text x="24" y="{y+6}" fill="{title_fill}" font-size="{title_size}" font-weight="{font_weight}" font-family="Be Vietnam Pro">{r["name"]}</text>')
        
        x25 = 140 + r["y25"] * scale
        x26_10 = 140 + r["y26_10"] * scale
        x26_50 = 140 + r["y26_50"] * scale

        svg.append(f'<line x1="{x25:.1f}" y1="{y+6}" x2="{x26_10:.1f}" y2="{y+6}" stroke="#f87171" stroke-width="4" stroke-linecap="round"/>')
        svg.append(f'<line x1="{x26_10:.1f}" y1="{y+6}" x2="{x26_50:.1f}" y2="{y+6}" stroke="#10b981" stroke-width="4" stroke-linecap="round"/>')

        svg.append(f'<circle cx="{x25:.1f}" cy="{y+6}" r="6.5" fill="#94a3b8" stroke="#ffffff" stroke-width="1.5"/>')
        svg.append(f'<circle cx="{x26_10:.1f}" cy="{y+6}" r="6.5" fill="#3b56e0" stroke="#ffffff" stroke-width="1.5"/>')
        svg.append(f'<circle cx="{x26_50:.1f}" cy="{y+6}" r="7.5" fill="#1e1b4b" stroke="#ffffff" stroke-width="2"/>')
        
        svg.append(f'<text x="{x25:.1f}" y="{y+26}" text-anchor="middle" fill="#64748b" font-size="11" font-weight="600" font-family="Manrope">{fmt_tr(r["y25"], 1)} tr</text>')
        svg.append(f'<text x="{x26_50:.1f}" y="{y-6}" text-anchor="middle" fill="#1e1b4b" font-size="12" font-weight="800" font-family="Manrope">{fmt_tr(r["y26_50"], 1)} tr</text>')

        pct_lbl = f"{fmt_pct(r['pct_10'])} → {fmt_pct(r['pct_50'])}"
        svg.append(f'<rect x="415" y="{y-7}" width="85" height="24" fill="#fef2f2" rx="12"/>')
        svg.append(f'<text x="457" y="{y+9}" text-anchor="middle" fill="#c2410c" font-size="11" font-weight="800" font-family="Manrope">{pct_lbl}</text>')

    svg.append('</svg>')
    return "\n".join(svg)


def build_year_growth_bar_svg():
    sorted_deps_yr = sorted(all_deps, key=lambda d: kpi_4tiers[d]["m10"]["pct_yr"], reverse=True)
    W, H = 560, 530
    row_h = 32
    top_offset = 48
    x_zero = 485
    scale = 3.5
    
    svg = []
    svg.append(f'<svg class="chart_svg" viewBox="0 0 {W} {H}" width="100%" height="auto" xmlns="http://www.w3.org/2000/svg">')
    
    # Headers and Legends
    svg.append(f'<text x="16" y="24" fill="#64748b" font-size="11" font-weight="700" font-family="Be Vietnam Pro">ĐƠN VỊ</text>')
    svg.append(f'<text x="156" y="24" text-anchor="middle" fill="#64748b" font-size="11" font-weight="700" font-family="Be Vietnam Pro">MỐC +10% → +50%</text>')

    # Grid lines
    for ref_pct in [-60, -40, -20, 15]:
        rx = x_zero + ref_pct * scale
        svg.append(f'<line x1="{rx:.1f}" y1="36" x2="{rx:.1f}" y2="{top_offset + 14 * row_h}" stroke="#f1f5f9" stroke-width="1" stroke-dasharray="2,2"/>')
        ref_txt = f"+{ref_pct}%" if ref_pct > 0 else f"{ref_pct}%"
        svg.append(f'<text x="{rx:.1f}" y="24" text-anchor="middle" fill="#94a3b8" font-size="10" font-weight="600" font-family="Manrope">{ref_txt}</text>')

    svg.append(f'<line x1="{x_zero}" y1="34" x2="{x_zero}" y2="{top_offset + 14 * row_h}" stroke="#94a3b8" stroke-width="1.5"/>')
    svg.append(f'<text x="{x_zero}" y="24" text-anchor="middle" fill="#14161c" font-size="11" font-weight="800" font-family="Manrope">0%</text>')

    # Legend indicator for bars
    svg.append(f'<rect x="250" y="15" width="9" height="9" fill="#fca5a5" rx="2"/>')
    svg.append(f'<text x="263" y="23" fill="#64748b" font-size="10" font-weight="600" font-family="Be Vietnam Pro">Mức giảm</text>')
    svg.append(f'<rect x="340" y="15" width="9" height="9" fill="#10b981" rx="2"/>')
    svg.append(f'<text x="353" y="23" fill="#047857" font-size="10" font-weight="700" font-family="Be Vietnam Pro">Thu hẹp nhờ +50%</text>')

    for i, name in enumerate(sorted_deps_yr):
        y = top_offset + i * row_h
        item = kpi_4tiers[name]
        pct10 = item["m10"]["pct_yr"]
        pct50 = item["m50"]["pct_yr"]
        is_the_gioi = (name == "Thế giới")
        is_xuat_ban = (name == "Xuất bản")
        
        row_bg = "#ecfdf5" if is_the_gioi else ("#fefce8" if is_xuat_ban else ("#f8fafc" if i % 2 == 1 else "#ffffff"))
        svg.append(f'<rect x="8" y="{y-14}" width="{W-16}" height="{row_h}" fill="{row_bg}" rx="4"/>')

        # 1. Department name (Column 1: x=16..88)
        weight = "800" if (is_the_gioi or is_xuat_ban) else "600"
        svg.append(f'<text x="16" y="{y+4}" fill="#14161c" font-size="12.5" font-weight="{weight}" font-family="Be Vietnam Pro">{name}</text>')

        # 2. Percentage range pill (Column 2: x=96..216)
        pill_bg = "#dcfce7" if is_the_gioi else ("#fef08a" if is_xuat_ban else "#f1f5f9")
        pill_fg = "#15803d" if is_the_gioi else ("#854d0e" if is_xuat_ban else "#c2410c")
        svg.append(f'<rect x="96" y="{y-9}" width="120" height="19" fill="{pill_bg}" rx="5"/>')
        val_txt = f"{fmt_pct(pct10)} → {fmt_pct(pct50)}"
        svg.append(f'<text x="156" y="{y+4}" text-anchor="middle" fill="{pill_fg}" font-size="11" font-weight="700" font-family="Manrope">{val_txt}</text>')

        # 3. Bar in Column 3 (x=230..545)
        x10 = x_zero + pct10 * scale
        x50 = x_zero + pct50 * scale

        if is_the_gioi:
            # Positive: base bar + extra
            svg.append(f'<rect x="{x_zero}" y="{y-7}" width="{x10 - x_zero:.1f}" height="14" fill="#16a34a" rx="3"/>')
            svg.append(f'<rect x="{x10:.1f}" y="{y-7}" width="{x50 - x10:.1f}" height="14" fill="#059669" rx="3"/>')
        elif is_xuat_ban:
            # Crosses zero: pct10 is -1.7%, pct50 is +8.3%
            svg.append(f'<rect x="{x10:.1f}" y="{y-7}" width="{x_zero - x10:.1f}" height="14" fill="#fed7aa" rx="3"/>')
            svg.append(f'<rect x="{x_zero}" y="{y-7}" width="{x50 - x_zero:.1f}" height="14" fill="#16a34a" rx="3"/>')
        else:
            # Negative:
            # Residual deficit bar (+50% level to 0):
            svg.append(f'<rect x="{x50:.1f}" y="{y-7}" width="{x_zero - x50:.1f}" height="14" fill="#fca5a5" rx="3"/>')
            # Recovery gain bar (+10% to +50%):
            svg.append(f'<rect x="{x10:.1f}" y="{y-7}" width="{x50 - x10:.1f}" height="14" fill="#10b981" rx="3"/>')

    svg.append('</svg>')
    return "\n".join(svg)


# ==========================================
# ASSEMBLE FULL HTML (ZERO STYLE ATTRIBUTES)
# ==========================================



# =========================================================================
# APPROVED POLICY DATA (CHỐT KPI QUÝ 4/2026)
# =========================================================================
def fmt_day(day_val):
    return f"{day_val:,.0f}".replace(",", ".")

approved_pct = {
    "Xã hội": 15, "Pháp luật": 15, "Thế giới": 15, "Xuất bản": 15,
    "Kinh doanh": 15, "Công nghệ": 15, "Xe": 15,
    "Đời sống": 15, "Lifestyle": 10, "Sức khỏe": 15, "Giáo dục": 15, "Du lịch": 15,
    "Thể thao": 20, "Giải trí": 15,
}

dep_focus = {
    "Xã hội": "Khai thác sâu dòng sự kiện chính sách, an sinh; kết nối bắn tin Zalo OA các chủ đề thiết thực với đời sống.",
    "Pháp luật": "Tập trung các vụ án dư luận quan tâm, chuyên đề phổ biến kiến thức pháp luật và phòng ngừa lừa đảo.",
    "Thế giới": "Bám sát các điểm nóng xung đột, bầu cử toàn cầu; tối ưu SEO nhanh cho các bản tin thời sự quốc tế nóng.",
    "Xuất bản": "Đẩy mạnh bình luận sách, chân dung tác giả, giải thưởng văn học và nội dung văn hóa tư tưởng.",
    "Kinh doanh": "Tận dụng mùa cao điểm báo cáo tài chính Q4, bất động sản, thị trường vàng và chính sách tiền tệ cuối năm.",
    "Công nghệ": "Tâm điểm mùa ra mắt sản phẩm công nghệ cuối năm, xu hướng AI thực chiến và bảo mật thông tin.",
    "Xe": "Khai thác triển lãm ô tô, mùa kích cầu mua sắm xe cuối năm, đánh giá trải nghiệm thực tế xe điện.",
    "Đời sống": "Chuyên đề gia đình, người trẻ đô thị, mùa lễ hội cuối năm và xu hướng tiêu dùng thông minh.",
    "Lifestyle": "Tăng 10% do mất động lực đẩy bên ngoài; tập trung nội dung thời trang, làm đẹp chọn lọc, củng cố SEO tự nhiên.",
    "Sức khỏe": "Mùa dịch bệnh thời tiết cuối năm, dinh dưỡng, tư vấn bác sĩ và chuyên đề sống lành mạnh.",
    "Giáo dục": "Chính sách giáo dục, du học, kỳ thi tốt nghiệp và các vấn đề phụ huynh - học sinh thời đại số.",
    "Du lịch": "Mùa du lịch lễ tết cuối năm, ẩm thực vùng miền, trải nghiệm khám phá và cẩm nang dịch chuyển.",
    "Thể thao": "Mũi nhọn kéo traffic (+20%): Tường thuật trực tiếp AFF Cup, Ngoại hạng Anh, Champions League và bắn Zalo giờ vàng.",
    "Giải trí": "Mùa giải trí cuối năm, sự kiện âm nhạc, điện ảnh và chân dung nhân vật nghệ thuật tạo sóng dư luận.",
}

approved_deps = {}
for dep in all_deps:
    raw = kpi_dict[dep]
    tb = raw["tb_thang_T8T9_2026"]
    pct = approved_pct[dep]
    th = round(tb * (1.0 + pct / 100.0))
    q4 = th * 3
    day = round((q4 * 1000) / 92)  # Q4 has 92 days (31+30+31)
    luyke = raw["luy_ke_2026_den_29_09"]
    yr_25 = raw["ca_nam_2025"]
    yr_26 = luyke + q4
    pct_yr = (yr_26 / yr_25 - 1.0) * 100.0
    approved_deps[dep] = {
        "ten": dep, "khoi": dep_block_map[dep], "pct": pct,
        "tb": tb, "day": day, "th": th, "q4": q4,
        "luyke": luyke, "yr_25": yr_25, "yr_26": yr_26, "pct_yr": pct_yr,
        "focus": dep_focus[dep]
    }

approved_blocks = {}
for blk in all_blocks:
    deps = deps_by_block[blk]
    b_tb = sum(approved_deps[d]["tb"] for d in deps)
    b_th = sum(approved_deps[d]["th"] for d in deps)
    b_q4 = sum(approved_deps[d]["q4"] for d in deps)
    b_day = sum(approved_deps[d]["day"] for d in deps)
    b_luyke = sum(approved_deps[d]["luyke"] for d in deps)
    b_yr_25 = sum(approved_deps[d]["yr_25"] for d in deps)
    b_yr_26 = b_luyke + b_q4
    b_pct_yr = (b_yr_26 / b_yr_25 - 1.0) * 100.0
    b_pct = (b_th / b_tb - 1.0) * 100.0
    approved_blocks[blk] = {
        "ten": blk, "pct": b_pct,
        "tb": b_tb, "day": b_day, "th": b_th, "q4": b_q4,
        "luyke": b_luyke, "yr_25": b_yr_25, "yr_26": b_yr_26, "pct_yr": b_pct_yr
    }

toan_tb_app = sum(approved_blocks[b]["tb"] for b in all_blocks)
toan_th_app = sum(approved_blocks[b]["th"] for b in all_blocks)
toan_q4_app = sum(approved_blocks[b]["q4"] for b in all_blocks)
toan_day_app = sum(approved_blocks[b]["day"] for b in all_blocks)
toan_yr_25_app = sum(approved_blocks[b]["yr_25"] for b in all_blocks)
toan_luyke_app = sum(approved_blocks[b]["luyke"] for b in all_blocks)
toan_yr_26_app = toan_luyke_app + toan_q4_app
toan_pct_yr_app = (toan_yr_26_app / toan_yr_25_app - 1.0) * 100.0
toan_pct_tang_app = (toan_th_app / toan_tb_app - 1.0) * 100.0

approved_total = {
    "ten": "Toàn Znews", "pct": toan_pct_tang_app,
    "tb": toan_tb_app, "day": toan_day_app, "th": toan_th_app, "q4": toan_q4_app,
    "yr_25": toan_yr_25_app, "yr_26": toan_yr_26_app, "pct_yr": toan_pct_yr_app
}

def build_approved_kpi_bar_svg():
    W, H = 960, 520
    top_offset = 45
    row_h = 32
    scale = 32.0
    bx = 180
    
    svg = []
    svg.append(f'<svg class="chart_svg" viewBox="0 0 {W} {H}" width="100%" height="auto" xmlns="http://www.w3.org/2000/svg">')
    
    svg.append('<rect x="180" y="10" width="12" height="12" fill="#cbd5e1" rx="2"/>')
    svg.append('<text x="198" y="21" fill="#64748b" font-size="11.5" font-weight="600" font-family="Be Vietnam Pro">Mức nền TB T8–T9</text>')

    svg.append('<rect x="340" y="10" width="12" height="12" fill="#3b56e0" rx="2"/>')
    svg.append('<text x="358" y="21" fill="#1e293b" font-size="11.5" font-weight="700" font-family="Be Vietnam Pro">Chỉ tiêu Quý 4 đã chốt (+15%, Thể thao +20%, Lifestyle +10%)</text>')

    for i, name in enumerate(all_deps):
        y = top_offset + i * row_h
        item = approved_deps[name]
        tb = item["tb"] / 1000.0
        th = item["th"] / 1000.0
        pct = item["pct"]
        day = item["day"]
        
        w_tb = tb * scale
        w_th = th * scale
        
        if i % 2 == 1:
            svg.append(f'<rect x="10" y="{y-14}" width="{W-20}" height="{row_h}" fill="#f8fafc" rx="4"/>')
            
        svg.append(f'<text x="20" y="{y+4}" fill="#14161c" font-size="13" font-weight="700" font-family="Be Vietnam Pro">{name}</text>')
        
        fill_col = "#16a34a" if pct == 20 else ("#d97706" if pct == 10 else "#3b56e0")
        svg.append(f'<rect x="{bx}" y="{y-8}" width="{w_th:.1f}" height="17" fill="{fill_col}" rx="3"/>')
        svg.append(f'<rect x="{bx}" y="{y-8}" width="{w_tb:.1f}" height="17" fill="#cbd5e1" rx="3"/>')
        
        val_txt = f"{fmt_day(day)} lượt/ngày • {fmt_tr(item['th'], 2)} tr/tháng (+{pct}%)"
        svg.append(f'<text x="{bx + w_th + 10:.1f}" y="{y+5}" fill="#14161c" font-size="11" font-weight="700" font-family="Manrope">{val_txt}</text>')

    svg.append('</svg>')
    return "\n".join(svg)

css_scoped = """
@import url('https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:ital,wght@0,400;0,500;0,600;0,700;1,400&family=Manrope:wght@500;600;700;800&display=swap');

html {
  scroll-behavior: smooth;
}

.container_AI {
  width: 100vw;
  margin-left: calc(50% - 50vw);
  margin-right: calc(50% - 50vw);
  background-color: #f8fafc;
  color: #14161c;
  font-family: 'Be Vietnam Pro', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  font-size: 15px;
  line-height: 1.6;
  -webkit-font-smoothing: antialiased;
}

.container_AI * {
  box-sizing: border-box;
}

.container_AI .wrap {
  max-width: 1100px;
  margin: 0 auto;
  padding: 40px 20px 80px 20px;
}

.container_AI .num {
  font-family: 'Manrope', sans-serif;
  font-feature-settings: 'tnum' 1;
  font-weight: 700;
}

.container_AI h1, .container_AI h2, .container_AI h3, .container_AI h4, .container_AI p {
  margin: 0;
}

.container_AI h1 {
  font-size: 32px;
  font-weight: 800;
  line-height: 1.25;
  color: #14161c;
  letter-spacing: -0.02em;
}

.container_AI h2 {
  font-size: 20px;
  font-weight: 700;
  color: #14161c;
}

.container_AI h3 {
  font-size: 16px;
  font-weight: 700;
  color: #14161c;
}

.container_AI .page_header {
  margin-bottom: 24px;
}

.container_AI .badge_bar {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 12px;
  flex-wrap: wrap;
}

.container_AI .meta_badge {
  display: inline-block;
  background-color: #eef2ff;
  color: #3b56e0;
  font-size: 12px;
  font-weight: 700;
  padding: 4px 10px;
  border-radius: 6px;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.container_AI .meta_subtext {
  color: #64748b;
  font-size: 13px;
}

.container_AI .page_desc {
  margin-top: 10px;
  color: #475569;
  font-size: 15px;
  max-width: 900px;
}

/* =======================================================
   STICKY 3-PART NAVIGATION BAR
   ======================================================= */
.container_AI .main_nav_tabs {
  position: sticky;
  top: 0;
  z-index: 999;
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
  padding: 14px 20px;
  background: rgba(248, 250, 252, 0.96);
  backdrop-filter: blur(12px);
  border-bottom: 1.5px solid #e2e8f0;
  margin: 24px -20px 36px -20px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.04);
}

.container_AI .nav_tab {
  display: flex;
  flex-direction: column;
  padding: 12px 16px;
  background: #ffffff;
  border: 1.5px solid #e2e8f0;
  border-radius: 12px;
  text-decoration: none;
  color: #1e293b;
  transition: all 0.2s ease;
  cursor: pointer;
}

.container_AI .nav_tab:hover {
  border-color: #94a3b8;
  background: #f8fafc;
  transform: translateY(-1px);
}

.container_AI .nav_tab.active {
  background: #eff6ff;
  border-color: #3b56e0;
  box-shadow: 0 4px 14px rgba(59, 86, 224, 0.12);
}

.container_AI .nav_tab_badge {
  font-size: 11px;
  font-weight: 800;
  color: #3b56e0;
  letter-spacing: 0.05em;
  text-transform: uppercase;
  margin-bottom: 3px;
}

.container_AI .nav_tab_title {
  font-size: 14px;
  font-weight: 700;
  color: #0f172a;
  margin-bottom: 2px;
  line-height: 1.3;
}

.container_AI .nav_tab_desc {
  font-size: 11px;
  color: #64748b;
  line-height: 1.3;
}

/* =======================================================
   DASHBOARD PARTS & BANNERS
   ======================================================= */
.container_AI .dashboard_part {
  scroll-margin-top: 130px;
  margin-bottom: 56px;
}

.container_AI .part_banner {
  background: #ffffff;
  border: 1.5px solid #e2e8f0;
  border-left: 6px solid #3b56e0;
  border-radius: 14px;
  padding: 22px 28px;
  margin-bottom: 24px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.02);
}

.container_AI .part_banner.part2_banner {
  border-left-color: #4f46e5;
}

.container_AI .part_banner.part3_banner {
  border-left-color: #059669;
}

.container_AI .part_badge {
  display: inline-block;
  font-size: 11px;
  font-weight: 800;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  padding: 3px 10px;
  border-radius: 6px;
  background: #eff6ff;
  color: #3b56e0;
  margin-bottom: 8px;
}

.container_AI .part2_banner .part_badge {
  background: #eef2ff;
  color: #4f46e5;
}

.container_AI .part3_banner .part_badge {
  background: #ecfdf5;
  color: #059669;
}

.container_AI .part_title {
  font-size: 22px;
  font-weight: 800;
  color: #0f172a;
  margin-bottom: 6px;
  line-height: 1.3;
}

.container_AI .part_desc {
  font-size: 14px;
  color: #64748b;
  line-height: 1.5;
}

/* =======================================================
   GRIDS & CARDS
   ======================================================= */
.container_AI .grid_4col {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
  margin-bottom: 24px;
}

.container_AI .grid_2col {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  margin-bottom: 24px;
}

.container_AI .kpi_card_head {
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  padding: 18px 20px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.02);
}

.container_AI .kpi_card_head.highlight {
  background: #eff6ff;
  border-color: #bfdbfe;
  border-width: 2px;
}

.container_AI .kpi_card_head.warn_card {
  background: #fffbeb;
  border-color: #fde68a;
}

.container_AI .kpi_card_head.alert_card {
  background: #fef2f2;
  border-color: #fecdd3;
}

.container_AI .kpi_label {
  font-size: 12px;
  font-weight: 700;
  color: #64748b;
  text-transform: uppercase;
  letter-spacing: 0.04em;
  margin-bottom: 8px;
}

.container_AI .kpi_value_huge {
  font-family: 'Manrope', sans-serif;
  font-size: 24px;
  font-weight: 800;
  color: #0f172a;
  letter-spacing: -0.02em;
  line-height: 1.2;
}

.container_AI .kpi_value_huge.accent {
  color: #3b56e0;
}

.container_AI .kpi_value_huge.negative {
  color: #c2410c;
}

.container_AI .kpi_value_huge.warning_val {
  color: #b45309;
}

.container_AI .kpi_sub {
  margin-top: 8px;
  font-size: 13px;
  color: #64748b;
}

.container_AI .card {
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 14px;
  padding: 24px;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.02);
  margin-bottom: 24px;
}

.container_AI .card h3 {
  margin-bottom: 4px;
}

.container_AI .card p {
  color: #64748b;
  font-size: 13.5px;
  margin-bottom: 16px;
}

/* =======================================================
   SECTION HEADERS & CONTROLS
   ======================================================= */
.container_AI .section_block {
  margin-bottom: 28px;
}

.container_AI .section_header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 16px;
  flex-wrap: wrap;
  gap: 12px;
}

.container_AI .section_title_wrap {
  display: flex;
  align-items: center;
  gap: 12px;
}

.container_AI .section_num {
  font-family: 'Manrope', sans-serif;
  font-size: 14px;
  font-weight: 800;
  color: #ffffff;
  background-color: #3b56e0;
  width: 28px;
  height: 28px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.container_AI .section_title {
  font-size: 18px;
  font-weight: 800;
  color: #0f172a;
}

.container_AI .section_sub {
  color: #64748b;
  font-size: 13px;
}

.container_AI .controls_bar {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
  align-items: center;
  margin-bottom: 16px;
}

.container_AI .chip {
  display: inline-block;
  font-size: 12.5px;
  font-weight: 600;
  padding: 6px 14px;
  border-radius: 20px;
  background: #f1f5f9;
  color: #475569;
  border: 1px solid #e2e8f0;
  cursor: pointer;
  transition: all 0.15s ease;
  user-select: none;
}

.container_AI .chip:hover {
  background: #e2e8f0;
  color: #0f172a;
}

.container_AI .chip.active {
  background: #3b56e0;
  color: #ffffff;
  border-color: #3b56e0;
}

.container_AI .chip_sm {
  font-size: 11.5px;
  padding: 4px 10px;
}

/* =======================================================
   TABLE STYLES & KPI PROGRESS SECTION
   ======================================================= */
.container_AI .table_responsive {
  width: 100%;
  overflow-x: auto;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
}

.container_AI .kpi_table {
  width: 100%;
  border-collapse: collapse;
  font-size: 13.5px;
  text-align: left;
}

.container_AI .kpi_table th {
  background: #f8fafc;
  color: #475569;
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 0.02em;
  padding: 12px 14px;
  border-bottom: 2px solid #e2e8f0;
  white-space: nowrap;
}

.container_AI .kpi_table td {
  padding: 12px 14px;
  border-bottom: 1px solid #f1f5f9;
  color: #1e293b;
}

.container_AI .kpi_table tbody tr:hover {
  background-color: #f8fafc;
}

.container_AI .kpi_table .row_block {
  background-color: #f1f5f9;
  font-weight: 700;
  border-top: 1.5px solid #e2e8f0;
  border-bottom: 1.5px solid #e2e8f0;
}

.container_AI .kpi_table .row_total {
  background-color: #eff6ff;
  font-weight: 800;
  border-top: 2px solid #3b56e0;
  border-bottom: 2px solid #3b56e0;
}

.container_AI tr.hidden_element,
.container_AI .hidden_element {
  display: none !important;
}

.container_AI .cell_num {
  text-align: right;
  font-family: 'Manrope', sans-serif;
  font-feature-settings: 'tnum' 1;
}

.container_AI .cell_center {
  text-align: center;
}

.container_AI .cell_primary {
  color: #3b56e0;
  font-weight: 700;
}

.container_AI .cell_challenge {
  color: #4338ca;
  font-weight: 700;
}

.container_AI .cell_recover {
  color: #065f46;
  font-weight: 800;
  background: #ecfdf5;
}

.container_AI .cell_bold {
  font-weight: 700;
}

.container_AI .cell_neg {
  color: #c2410c;
  font-weight: 700;
}

/* Progress Table Cells */
.container_AI .prog_cell {
  display: flex;
  flex-direction: column;
  gap: 4px;
  align-items: flex-end;
}

.container_AI .prog_val_line {
  display: flex;
  justify-content: flex-end;
  align-items: baseline;
  gap: 6px;
}

.container_AI .prog_pct {
  font-size: 11px;
  font-weight: 700;
  font-family: 'Manrope', sans-serif;
}

.container_AI .pct_good {
  color: #15803d;
}

.container_AI .pct_warn {
  color: #b45309;
}

.container_AI .pct_bad {
  color: #b91c1c;
}

.container_AI .badge_critical {
  display: inline-block;
  background: #fef2f2;
  color: #991b1b;
  border: 1px solid #fecdd3;
  padding: 3px 8px;
  border-radius: 6px;
  font-weight: 800;
  font-size: 11.5px;
  font-family: 'Manrope', sans-serif;
  white-space: nowrap;
}

.container_AI .badge_warning {
  display: inline-block;
  background: #fffbeb;
  color: #b45309;
  border: 1px solid #fde68a;
  padding: 3px 8px;
  border-radius: 6px;
  font-weight: 700;
  font-size: 11.5px;
  font-family: 'Manrope', sans-serif;
  white-space: nowrap;
}

.container_AI .badge_success {
  display: inline-block;
  background: #ecfdf5;
  color: #15803d;
  border: 1px solid #a7f3d0;
  padding: 3px 8px;
  border-radius: 6px;
  font-weight: 700;
  font-size: 11.5px;
  font-family: 'Manrope', sans-serif;
  white-space: nowrap;
}

.container_AI .table_col_highlight {
  background-color: #f0f7ff;
}

.container_AI .table_col_highlight_gold {
  background-color: #fefce8;
}

.container_AI .tier_focus {
  background-color: #eff6ff !important;
  font-weight: 800;
}

.container_AI .tier_focus_50 {
  background-color: #ecfdf5 !important;
  font-weight: 800;
}

/* =======================================================
   REASON & STRATEGY SECTION (PART 3)
   ======================================================= */
.container_AI .reason_grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  margin-top: 16px;
}

.container_AI .reason_card {
  background: #ffffff;
  border: 1.5px solid #e2e8f0;
  border-radius: 14px;
  padding: 24px;
  display: flex;
  flex-direction: column;
  gap: 12px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.02);
}

.container_AI .reason_header {
  display: flex;
  align-items: center;
  gap: 14px;
}

.container_AI .reason_icon {
  width: 44px;
  height: 44px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 22px;
  font-weight: 800;
  flex-shrink: 0;
}

.container_AI .icon_shock {
  background: #fef2f2;
  color: #dc2626;
}

.container_AI .icon_zalo {
  background: #e0f2fe;
  color: #0284c7;
}

.container_AI .icon_google {
  background: #ecfdf5;
  color: #059669;
}

.container_AI .reason_title {
  font-size: 16px;
  font-weight: 800;
  color: #0f172a;
  line-height: 1.35;
}

.container_AI .reason_body {
  font-size: 14px;
  color: #475569;
  line-height: 1.6;
}

.container_AI .reason_bullets {
  margin: 8px 0 0 0;
  padding-left: 18px;
}

.container_AI .reason_bullets li {
  margin-bottom: 8px;
}

.container_AI .matrix_grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
  margin-top: 16px;
}

.container_AI .matrix_card {
  background: #f8fafc;
  border: 1.5px solid #e2e8f0;
  border-radius: 12px;
  padding: 18px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.container_AI .matrix_title {
  font-size: 14px;
  font-weight: 800;
  color: #1e293b;
}

.container_AI .matrix_sub {
  font-size: 12.5px;
  color: #64748b;
  line-height: 1.5;
}

.container_AI .callout_banner {
  background: #eff6ff;
  border: 1.5px solid #bfdbfe;
  border-radius: 14px;
  padding: 20px 24px;
  margin-top: 20px;
}

.container_AI .callout_title {
  font-size: 15px;
  font-weight: 800;
  color: #1e40af;
  margin-bottom: 6px;
}

.container_AI .callout_text {
  font-size: 13.5px;
  color: #1e3a8a;
  line-height: 1.55;
}

/* =======================================================
   DEP CARDS & CHARTS
   ======================================================= */
.container_AI .dep_grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
  margin-top: 24px;
}

.container_AI .dep_card {
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  padding: 20px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.container_AI .dep_card_header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 14px;
  flex-wrap: wrap;
  gap: 12px;
}

.container_AI .dep_name {
  font-size: 17px;
  font-weight: 800;
  color: #0f172a;
}

.container_AI .dep_block_tag {
  font-size: 11px;
  font-weight: 700;
  padding: 3px 8px;
  border-radius: 4px;
  background: #f1f5f9;
  color: #475569;
}

.container_AI .dep_stat_row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 10px;
  margin-bottom: 12px;
}

.container_AI .stat_box {
  background: #f8fafc;
  border: 1px solid #f1f5f9;
  border-radius: 8px;
  padding: 10px 12px;
}

.container_AI .stat_box_label {
  font-size: 11px;
  color: #64748b;
  margin-bottom: 4px;
  font-weight: 600;
}

.container_AI .stat_box_val {
  font-family: 'Manrope', sans-serif;
  font-size: 15px;
  font-weight: 800;
  color: #0f172a;
}

.container_AI .target_row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 8px;
  background: #f1f5f9;
  border-radius: 8px;
  padding: 10px 12px;
  margin-bottom: 8px;
}

.container_AI .target_row.gold {
  background: #fefce8;
  border: 1px solid #fef08a;
}

.container_AI .target_tier {
  font-size: 12px;
  font-weight: 700;
  color: #1e293b;
}

.container_AI .target_val {
  font-family: 'Manrope', sans-serif;
  font-size: 13.5px;
  font-weight: 800;
  color: #3b56e0;
  text-align: right;
}

.container_AI .target_val.gold {
  color: #854d0e;
}

.container_AI .dep_footer_row {
  margin-top: 8px;
  padding-top: 10px;
  border-top: 1px dashed #e2e8f0;
  display: flex;
  justify-content: space-between;
  font-size: 12px;
  color: #64748b;
}

.container_AI .chart_svg {
  display: block;
  overflow: visible;
}

.container_AI .page_footer {
  margin-top: 48px;
  padding-top: 24px;
  border-top: 1px solid #e2e8f0;
  display: flex;
  justify-content: space-between;
  color: #64748b;
  font-size: 13px;
  flex-wrap: wrap;
  gap: 12px;
}

/* =======================================================
   RESPONSIVE DESIGN (MOBILE FONT +15%)
   ======================================================= */
@media (max-width: 900px) {
  .container_AI .main_nav_tabs {
    grid-template-columns: 1fr;
    gap: 8px;
    padding: 12px 14px;
    position: relative;
    margin: 20px 0 28px 0;
  }
  .container_AI .grid_4col {
    grid-template-columns: 1fr 1fr;
  }
  .container_AI .grid_2col {
    grid-template-columns: 1fr;
  }
  .container_AI .dep_grid {
    grid-template-columns: 1fr;
  }
  .container_AI .reason_grid {
    grid-template-columns: 1fr;
  }
  .container_AI .matrix_grid {
    grid-template-columns: 1fr 1fr;
  }
}

@media (max-width: 640px) {
  .container_AI {
    font-size: 16.5px;
  }
  .container_AI .wrap {
    padding: 20px 14px 60px 14px;
  }
  .container_AI h1 {
    font-size: 24px;
  }
  .container_AI .grid_4col {
    grid-template-columns: 1fr;
  }
  .container_AI .matrix_grid {
    grid-template-columns: 1fr;
  }
  .container_AI .part_title {
    font-size: 19px;
  }
  .container_AI .part_banner {
    padding: 16px 18px;
  }
}


/* NEW PORTAL CLASSES (NO INLINE STYLES) */
.container_AI .top_header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 0 28px 0;
  border-bottom: 2px solid #e2e8f0;
  margin-bottom: 28px;
  flex-wrap: wrap;
  gap: 16px;
}

.container_AI .brand_area {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.container_AI .brand_kicker {
  font-size: 12.5px;
  font-weight: 700;
  letter-spacing: 0.04em;
  color: #3b56e0;
}

.container_AI .brand_title {
  font-size: 28px;
  font-weight: 900;
  color: #0f172a;
  letter-spacing: -0.02em;
  line-height: 1.25;
}

.container_AI .brand_sub {
  font-size: 14.5px;
  color: #64748b;
  font-weight: 500;
}

.container_AI .nav_btn_main {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background: #3b56e0;
  color: #ffffff;
  padding: 12px 22px;
  border-radius: 10px;
  font-size: 14px;
  font-weight: 700;
  text-decoration: none;
  transition: all 0.2s ease;
  box-shadow: 0 4px 14px rgba(59, 86, 224, 0.25);
}

.container_AI .nav_btn_main:hover {
  background: #2740c4;
  transform: translateY(-1px);
  box-shadow: 0 6px 20px rgba(59, 86, 224, 0.35);
}

.container_AI .nav_btn_back {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background: #0f172a;
  color: #ffffff;
  padding: 12px 20px;
  border-radius: 10px;
  font-size: 13.5px;
  font-weight: 700;
  text-decoration: none;
  transition: all 0.2s ease;
}

.container_AI .nav_btn_back:hover {
  background: #334155;
  transform: translateY(-1px);
}

.container_AI .top_nav_back_bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 0;
  margin-bottom: 24px;
  border-bottom: 1px solid #e2e8f0;
  flex-wrap: wrap;
  gap: 12px;
}

.container_AI .kpi_grid_4 {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 18px;
  margin-bottom: 28px;
}

.container_AI .kpi_metric_card {
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 14px;
  padding: 22px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  box-shadow: 0 2px 6px rgba(0,0,0,0.02);
  position: relative;
  overflow: hidden;
}

.container_AI .kpi_metric_card.highlight_day {
  background: linear-gradient(135deg, #ecfdf5 0%, #ffffff 100%);
  border: 1.5px solid #10b981;
}

.container_AI .kpi_metric_card.highlight_month {
  background: linear-gradient(135deg, #eff6ff 0%, #ffffff 100%);
  border: 1.5px solid #3b56e0;
}

.container_AI .kpi_metric_card.highlight_quarter {
  background: linear-gradient(135deg, #faf5ff 0%, #ffffff 100%);
  border: 1.5px solid #8b5cf6;
}

.container_AI .kpi_metric_label {
  font-size: 13px;
  font-weight: 700;
  color: #64748b;
  margin-bottom: 6px;
}

.container_AI .kpi_metric_val {
  font-family: 'Manrope', sans-serif;
  font-size: 32px;
  font-weight: 800;
  line-height: 1.15;
  color: #0f172a;
  margin-bottom: 6px;
  letter-spacing: -0.02em;
}

.container_AI .kpi_metric_val.val_green {
  color: #059669;
}

.container_AI .kpi_metric_val.val_blue {
  color: #3b56e0;
}

.container_AI .kpi_metric_val.val_purple {
  color: #7c3aed;
}

.container_AI .kpi_metric_sub {
  font-size: 13px;
  color: #475569;
  line-height: 1.4;
}

.container_AI .policy_banner {
  background: #ffffff;
  border-left: 5px solid #3b56e0;
  border: 1px solid #e2e8f0;
  border-left-width: 5px;
  border-left-color: #3b56e0;
  border-radius: 12px;
  padding: 24px;
  margin-bottom: 28px;
}

.container_AI .policy_header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 14px;
  flex-wrap: wrap;
  gap: 12px;
}

.container_AI .policy_title {
  font-size: 18px;
  font-weight: 800;
  color: #0f172a;
}

.container_AI .policy_sub {
  font-size: 13.5px;
  color: #64748b;
}

.container_AI .policy_grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 12px;
  margin-top: 14px;
}

.container_AI .policy_item {
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  padding: 12px 14px;
}

.container_AI .policy_item_title {
  font-size: 13px;
  font-weight: 800;
  color: #0f172a;
  margin-bottom: 4px;
}

.container_AI .policy_item_desc {
  font-size: 12px;
  color: #64748b;
  line-height: 1.4;
}

.container_AI .cell_day_hl {
  background-color: #ecfdf5;
  color: #065f46;
  font-weight: 800;
  font-size: 14px;
  border-left: 1px solid #d1fae5;
  border-right: 1px solid #d1fae5;
}

.container_AI .row_block .cell_day_hl {
  background-color: #d1fae5;
}

.container_AI .row_total .cell_day_hl {
  background-color: #a7f3d0;
  color: #064e3b;
  font-size: 15px;
}

.container_AI .badge_kpi {
  display: inline-block;
  padding: 3px 8px;
  border-radius: 6px;
  font-size: 11.5px;
  font-weight: 800;
  font-family: 'Manrope', sans-serif;
}

.container_AI .badge_15 {
  background: #dbeafe;
  color: #1e40af;
}

.container_AI .badge_20 {
  background: #dcfce7;
  color: #166534;
}

.container_AI .badge_10 {
  background: #fef3c7;
  color: #92400e;
}

.container_AI .dep_target_boxes {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 10px;
  margin-bottom: 14px;
}

.container_AI .target_box {
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  padding: 10px;
  text-align: center;
}

.container_AI .target_box.box_day {
  background: #ecfdf5;
  border-color: #a7f3d0;
}

.container_AI .target_box_label {
  font-size: 11.5px;
  font-weight: 700;
  color: #64748b;
  margin-bottom: 3px;
}

.container_AI .target_box_val {
  font-family: 'Manrope', sans-serif;
  font-size: 17px;
  font-weight: 800;
  color: #0f172a;
}

.container_AI .target_box.box_day .target_box_val {
  color: #047857;
}

.container_AI .dep_focus_note {
  font-size: 12.5px;
  color: #475569;
  line-height: 1.45;
  background: #f8fafc;
  padding: 10px 12px;
  border-radius: 6px;
  border-left: 3px solid #cbd5e1;
}

.container_AI .cta_footer_card {
  background: linear-gradient(135deg, #1e1b4b 0%, #0f172a 100%);
  color: #ffffff;
  border-radius: 16px;
  padding: 36px 32px;
  margin-top: 36px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 20px;
  box-shadow: 0 10px 25px rgba(15, 23, 42, 0.2);
}

.container_AI .cta_footer_content {
  max-width: 720px;
}

.container_AI .cta_footer_title {
  font-size: 22px;
  font-weight: 800;
  color: #ffffff;
  margin-bottom: 8px;
}

.container_AI .cta_footer_desc {
  font-size: 14.5px;
  color: #cbd5e1;
  line-height: 1.5;
}

.container_AI .btn_cta_large {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  background: #3b56e0;
  color: #ffffff;
  padding: 14px 28px;
  border-radius: 10px;
  font-size: 15px;
  font-weight: 800;
  text-decoration: none;
  transition: all 0.2s ease;
  white-space: nowrap;
}

.container_AI .btn_cta_large:hover {
  background: #4f6cf6;
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(59, 86, 224, 0.4);
}

@media (max-width: 992px) {
  .container_AI .kpi_grid_4 { grid-template-columns: repeat(2, 1fr); }
  .container_AI .policy_grid { grid-template-columns: repeat(2, 1fr); }
}

@media (max-width: 640px) {
  .container_AI .kpi_grid_4 { grid-template-columns: 1fr; }
  .container_AI .policy_grid { grid-template-columns: 1fr; }
  .container_AI .top_header { flex-direction: column; align-items: flex-start; }
  .container_AI .brand_title { font-size: 24px; }
  .container_AI .kpi_metric_val { font-size: 28px; }
  .container_AI .cta_footer_card { flex-direction: column; align-items: flex-start; }
}

/* =========================================================================
   TOP NAV TABS & INTERACTIVE CONTROLS (T9 CALCULATOR)
   ========================================================================= */
.container_AI .top_bar_nav {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-wrap: wrap;
  margin-bottom: 24px;
  padding-bottom: 16px;
  border-bottom: 1px solid #e2e8f0;
}

.container_AI .top_nav_link {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  border-radius: 999px;
  font-size: 14px;
  font-weight: 700;
  text-decoration: none;
  background: #f1f5f9;
  color: #475569;
  border: 1px solid #cbd5e1;
  transition: all 0.2s ease;
}

.container_AI .top_nav_link:hover {
  background: #e2e8f0;
  color: #0f172a;
  transform: translateY(-1px);
}

.container_AI .top_nav_link.active {
  background: #3b56e0;
  color: #ffffff;
  border-color: #3b56e0;
  box-shadow: 0 2px 8px rgba(59, 86, 224, 0.25);
}

.container_AI .control_panel_card {
  background: #ffffff;
  border: 1.5px solid #e2e8f0;
  border-radius: 16px;
  padding: 24px;
  margin-bottom: 28px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.04);
}

.container_AI .control_panel_header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 12px;
  margin-bottom: 16px;
  padding-bottom: 14px;
  border-bottom: 1px solid #f1f5f9;
}

.container_AI .control_panel_title {
  font-size: 18px;
  font-weight: 800;
  color: #0f172a;
}

.container_AI .control_grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
}

.container_AI .control_section {
  display: flex;
  flex-direction: column;
  gap: 10px;
  background: #f8fafc;
  padding: 16px;
  border-radius: 12px;
  border: 1px solid #e2e8f0;
}

.container_AI .control_section_full {
  grid-column: 1 / -1;
  background: #f0f7ff;
  border-color: #bfdbfe;
}

.container_AI .control_label {
  font-size: 13px;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  color: #334155;
}

.container_AI .control_desc {
  font-size: 13px;
  color: #64748b;
  line-height: 1.4;
}

.container_AI .chip_group {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  align-items: center;
}

.container_AI .chip {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 7px 14px;
  background: #ffffff;
  border: 1.5px solid #cbd5e1;
  border-radius: 8px;
  font-size: 13.5px;
  font-weight: 600;
  color: #334155;
  cursor: pointer;
  user-select: none;
  transition: all 0.15s ease;
}

.container_AI .chip:hover {
  background: #f1f5f9;
  border-color: #94a3b8;
  color: #0f172a;
}

.container_AI .chip.active {
  background: #3b56e0;
  border-color: #3b56e0;
  color: #ffffff;
  box-shadow: 0 2px 8px rgba(59, 86, 224, 0.25);
}

.container_AI .rate_input_wrap {
  display: inline-flex;
  align-items: center;
  background: #ffffff;
  border: 1.5px solid #cbd5e1;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
  transition: all 0.2s ease;
}

.container_AI .rate_input_wrap:focus-within {
  border-color: #3b56e0;
  box-shadow: 0 0 0 3px rgba(59, 86, 224, 0.15);
}

.container_AI .rate_input {
  width: 76px;
  padding: 7px 10px;
  font-size: 14.5px;
  font-weight: 700;
  color: #0f172a;
  border: none;
  outline: none;
  background: transparent;
  text-align: right;
  font-family: inherit;
}

.container_AI .rate_unit {
  padding: 7px 12px 7px 6px;
  font-size: 13.5px;
  font-weight: 700;
  color: #64748b;
  background: #f8fafc;
  border-left: 1px solid #e2e8f0;
}

.container_AI .control_helper_text {
  font-size: 13px;
  color: #475569;
  font-style: italic;
  margin-top: 4px;
}

.container_AI .table_dep_input {
  width: 58px;
  padding: 4px 6px;
  font-size: 13px;
  font-weight: 700;
  color: #0f172a;
  background: #ffffff;
  border: 1.5px solid #cbd5e1;
  border-radius: 6px;
  text-align: right;
  outline: none;
  font-family: inherit;
  transition: all 0.15s ease;
}

.container_AI .table_dep_input:focus {
  border-color: #3b56e0;
  box-shadow: 0 0 0 2px rgba(59, 86, 224, 0.2);
}

.container_AI .card_dep_input {
  width: 54px;
  padding: 3px 6px;
  font-size: 13px;
  font-weight: 700;
  color: #0f172a;
  background: #ffffff;
  border: 1.5px solid #cbd5e1;
  border-radius: 6px;
  text-align: right;
  outline: none;
  font-family: inherit;
  transition: all 0.15s ease;
}

.container_AI .card_dep_input:focus {
  border-color: #3b56e0;
  box-shadow: 0 0 0 2px rgba(59, 86, 224, 0.2);
}

.container_AI .table_input_cell {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 3px;
}

.container_AI .unit_tag {
  font-size: 12px;
  font-weight: 700;
  color: #64748b;
}

.container_AI .is_hidden {
  display: none !important;
}

@media (max-width: 900px) {
  .container_AI .control_grid {
    grid-template-columns: 1fr;
  }
}

"""


# =========================================================================
# BUILD INDEX.HTML (OFFICIAL ASSIGNED KPI PAGE)
# =========================================================================

# =========================================================================
# BUILD INTERACTIVE INDEX.HTML (SEPTEMBER 2026 KPI CALCULATOR)
# =========================================================================
def build_interactive_t9_index_html():
    html = []
    html.append('<!DOCTYPE html>')
    html.append('<html lang="vi">')
    html.append('<head>')
    html.append('  <meta charset="UTF-8">')
    html.append('  <meta name="viewport" content="width=device-width, initial-scale=1.0">')
    html.append('  <title>Công cụ tính toán & đề xuất KPI quý 4/2026 từ tháng 9 — Tạp chí điện tử Tri thức - Znews</title>')
    html.append(f'  <style>{css_scoped}</style>')
    html.append('</head>')
    html.append('<body>')
    html.append('<article class="container_AI">')
    html.append('  <div class="wrap">')

    # Top Bar Navigation
    html.append('    <nav class="top_bar_nav">')
    html.append('      <a href="index.html" class="top_nav_link active">🎯 Tính KPI từ tháng 9 (Công cụ mới)</a>')
    html.append('      <a href="kpi_phe_duyet.html" class="top_nav_link">📋 Phương án TB T8–T9 đã duyệt</a>')
    html.append('      <a href="detail.html" class="top_nav_link">📑 Báo cáo giải thích chi tiết</a>')
    html.append('    </nav>')

    # Header
    html.append('    <header class="top_header">')
    html.append('      <div class="brand_area">')
    html.append('        <div class="brand_kicker">Tạp chí điện tử Tri thức - Znews • Ban biên tập</div>')
    html.append('        <div class="brand_title">Công cụ tính toán & đề xuất KPI quý 4/2026 từ tháng 9</div>')
    html.append('        <div class="brand_sub">Dựa trên dữ liệu thực tế tháng 9/2026 quy đổi 30 ngày • Tùy chỉnh tỷ lệ tăng trưởng và loại trừ ảnh hưởng Zalo theo thời gian thực</div>')
    html.append('      </div>')
    html.append('      <div>')
    html.append('        <a href="detail.html" class="nav_btn_main">📑 Giải thích chi tiết & bối cảnh dữ liệu →</a>')
    html.append('      </div>')
    html.append('    </header>')

    # Interactive Control Panel Card
    html.append('    <div class="control_panel_card">')
    html.append('      <div class="control_panel_header">')
    html.append('        <div class="control_panel_title">Bảng điều khiển thông số tính toán KPI</div>')
    html.append('        <div class="badge_kpi badge_15" id="active_mode_badge">Đang áp tỷ lệ toàn bộ: +15,0%</div>')
    html.append('      </div>')
    html.append('      <div class="control_grid">')
    
    # Section 1: Zalo Impact Options (Full row)
    html.append('        <div class="control_section control_section_full">')
    html.append('          <div class="control_label">Ảnh hưởng truy cập Zalo (Cơ sở dữ liệu tháng 9)</div>')
    html.append('          <div class="chip_group" id="zalo_chips">')
    html.append('            <div class="chip active" data-zalo="real">Trừ Zalo thực tế (2,1%)</div>')
    html.append('            <div class="chip" data-zalo="hypo">Trừ Zalo giả định (5,0%)</div>')
    html.append('            <div class="chip" data-zalo="none">Không trừ Zalo (Số gốc T9 quy đổi)</div>')
    html.append('          </div>')
    html.append('          <div class="control_helper_text" id="zalo_status_note">Mức nền T9 sau trừ Zalo thực tế (2,13%): 25,47M/tháng • 848.949 lượt/ngày (T9 gồm 29 ngày dữ liệu thực tế, quy đổi đủ 30 ngày).</div>')
    html.append('        </div>')

    # Section 2: Mode Toggle
    html.append('        <div class="control_section">')
    html.append('          <div class="control_label">Chế độ phân bổ tỷ lệ tăng trưởng</div>')
    html.append('          <div class="chip_group" id="mode_chips">')
    html.append('            <div class="chip active" data-mode="all">Áp tỷ lệ tăng toàn bộ ban</div>')
    html.append('            <div class="chip" data-mode="custom">Tỷ lệ tăng tùy từng ban</div>')
    html.append('          </div>')
    html.append('          <div class="control_desc" id="mode_desc_note">Áp một tỷ lệ tăng trưởng đồng nhất cho toàn bộ 14 ban biên tập.</div>')
    html.append('        </div>')

    # Section 3: Preset Rates + Custom Rate Input
    html.append('        <div class="control_section">')
    html.append('          <div class="control_label">Thiết lập tỷ lệ tăng trưởng đề xuất</div>')
    html.append('          <div class="chip_group" id="rate_chips">')
    html.append('            <div class="chip" data-rate="10">+10%</div>')
    html.append('            <div class="chip active" data-rate="15">+15%</div>')
    html.append('            <div class="chip" data-rate="20">+20%</div>')
    html.append('            <div class="chip" data-rate="50">+50%</div>')
    html.append('            <div class="rate_input_wrap">')
    html.append('              <input type="number" id="global_rate_input" class="rate_input" value="15" step="0.5" min="-50" max="200">')
    html.append('              <div class="rate_unit">%</div>')
    html.append('            </div>')
    html.append('          </div>')
    html.append('          <div class="control_helper_text" id="rate_helper_note">Chọn nhanh tỷ lệ đặt sẵn hoặc nhập con số tăng trưởng tùy ý vào ô trên.</div>')
    html.append('        </div>')

    html.append('      </div>')
    html.append('    </div>')

    # 4 Overview Metric Cards (Live Reactive)
    html.append('    <div class="kpi_grid_4">')
    # Card 1: Ngày
    html.append('      <div class="kpi_metric_card highlight_day">')
    html.append('        <div class="kpi_metric_label">KPI truy cập theo ngày (toàn trang)</div>')
    html.append('        <div class="kpi_metric_val val_green" id="metric_day">976.291</div>')
    html.append('        <div class="kpi_metric_sub">Lượt xem trung bình mỗi ngày trong Quý 4 (92 ngày)</div>')
    html.append('      </div>')
    # Card 2: Tháng
    html.append('      <div class="kpi_metric_card highlight_month">')
    html.append('        <div class="kpi_metric_label">KPI truy cập trung bình tháng</div>')
    html.append('        <div class="kpi_metric_val val_blue" id="metric_month">29,94M</div>')
    html.append('        <div class="kpi_metric_sub">Trung bình mỗi tháng trong Quý 4 (T10, T11, T12)</div>')
    html.append('      </div>')
    # Card 3: Cả Quý 4
    html.append('      <div class="kpi_metric_card highlight_quarter">')
    html.append('        <div class="kpi_metric_label">KPI truy cập quý 4</div>')
    html.append('        <div class="kpi_metric_val val_purple" id="metric_q4">89,82M</div>')
    html.append('        <div class="kpi_metric_sub">Tổng 3 tháng: T10 (31 ngày) + T11 (30 ngày) + T12 (31 ngày)</div>')
    html.append('      </div>')
    # Card 4: Cả năm
    html.append('      <div class="kpi_metric_card">')
    html.append('        <div class="kpi_metric_label">Dự kiến cả năm 2026</div>')
    html.append('        <div class="kpi_metric_val" id="metric_year">586,28M</div>')
    html.append('        <div class="kpi_metric_sub">')
    html.append('          <div class="badge_kpi badge_15" id="metric_year_pct">-26,7% vs 2025</div>')
    html.append('        </div>')
    html.append('      </div>')
    html.append('    </div>')

    # Master KPI Table
    html.append('    <div class="card">')
    html.append('      <div class="dep_card_header">')
    html.append('        <div>')
    html.append('          <h3>Bảng tổng hợp chỉ tiêu: Ngày • tháng • quý 4/2026 & dự báo năm</h3>')
    html.append('        </div>')
    html.append('        <div class="controls_bar" id="master_filter_chips">')
    html.append('          <div class="chip active" data-filter="all">Tất cả (19 đơn vị)</div>')
    html.append('          <div class="chip" data-filter="blocks">Chỉ xem 4 khối</div>')
    html.append('          <div class="chip" data-filter="deps">Chỉ xem 14 ban</div>')
    html.append('        </div>')
    html.append('      </div>')
    html.append('      <div class="table_responsive">')
    html.append('        <table class="kpi_table" id="master_kpi_table">')
    html.append('          <thead>')
    html.append('            <tr>')
    html.append('              <th>Đơn vị / ban</th>')
    html.append('              <th class="cell_center">Tỷ lệ tăng</th>')
    html.append('              <th class="cell_num">Cơ sở T9 (nền)</th>')
    html.append('              <th class="cell_num cell_day_hl">KPI ngày</th>')
    html.append('              <th class="cell_num cell_primary">KPI tháng</th>')
    html.append('              <th class="cell_num cell_bold">KPI quý 4</th>')
    html.append('              <th class="cell_num cell_bold">Cả năm 2026</th>')
    html.append('              <th class="cell_num cell_bold">So với 2025</th>')
    html.append('            </tr>')
    html.append('          </thead>')
    html.append('          <tbody>')

    # Pre-render initial data
    DEPS_INFO = [
      {"id": "xh", "name": "Xã hội", "block": "Khối Uy tín", "base": 1832748.64, "day": 70255, "th": 2154498, "q4": 6463494, "yr": 33890494, "pct": -54.1},
      {"id": "pl", "name": "Pháp luật", "block": "Khối Uy tín", "base": 1112166.48, "day": 42633, "th": 1307413, "q4": 3922240, "yr": 28565240, "pct": -47.7},
      {"id": "tg", "name": "Thế giới", "block": "Khối Uy tín", "base": 844548.36, "day": 32374, "th": 992814, "q4": 2978441, "yr": 45320441, "pct": 12.1},
      {"id": "xb", "name": "Xuất bản", "block": "Khối Uy tín", "base": 1069556.27, "day": 41000, "th": 1257323, "q4": 3771968, "yr": 13632968, "pct": -1.7},
      {"id": "kd", "name": "Kinh doanh", "block": "Khối Kinh doanh", "base": 3468334.28, "day": 132953, "th": 4077218, "q4": 12231653, "yr": 54813653, "pct": -26.5},
      {"id": "cn", "name": "Công nghệ", "block": "Khối Kinh doanh", "base": 1674749.54, "day": 64199, "th": 1968766, "q4": 5906297, "yr": 26843297, "pct": -22.9},
      {"id": "xe", "name": "Xe", "block": "Khối Kinh doanh", "base": 821007.29, "day": 31472, "th": 965150, "q4": 2895449, "yr": 14241449, "pct": -16.9},
      {"id": "ds", "name": "Đời sống", "block": "Khối Lifestyle", "base": 1751488.83, "day": 67140, "th": 2059300, "q4": 6177899, "yr": 52908899, "pct": -20.2},
      {"id": "ls", "name": "Lifestyle", "block": "Khối Lifestyle", "base": 553746.55, "day": 21227, "th": 650974, "q4": 1952923, "yr": 12319590, "pct": -26.7},
      {"id": "sk", "name": "Sức khỏe", "block": "Khối Lifestyle", "base": 1890585.83, "day": 72472, "th": 2222822, "q4": 6668465, "yr": 34327465, "pct": -36.7},
      {"id": "gd", "name": "Giáo dục", "block": "Khối Lifestyle", "base": 474675.62, "day": 18196, "th": 558000, "q4": 1674000, "yr": 12591000, "pct": -31.5},
      {"id": "dl", "name": "Du lịch", "block": "Khối Lifestyle", "base": 908208.04, "day": 34815, "th": 1067645, "q4": 3202934, "yr": 20248934, "pct": -18.3},
      {"id": "tt", "name": "Thể thao", "block": "Khối Truy cập", "base": 6452862.82, "day": 247360, "th": 7585699, "q4": 22757096, "yr": 173141096, "pct": -18.8},
      {"id": "gt", "name": "Giải trí", "block": "Khối Truy cập", "base": 2613781.07, "day": 100195, "th": 3072645, "q4": 9217935, "yr": 63439935, "pct": -34.4}
    ]

    BLOCKS_INFO = [
      {"id": "b_uytin", "name": "Khối Uy tín", "deps": ["xh", "pl", "tg", "xb"], "base": 4859019.74, "day": 186262, "th": 5712048, "q4": 17136143, "yr": 121409143, "pct": -33.5},
      {"id": "b_kinhdoanh", "name": "Khối Kinh doanh", "deps": ["kd", "cn", "xe"], "base": 5964091.11, "day": 228624, "th": 7011134, "q4": 21033399, "yr": 95898399, "pct": -24.2},
      {"id": "b_lifestyle", "name": "Khối Lifestyle", "deps": ["ds", "ls", "sk", "gd", "dl"], "base": 5578704.88, "day": 213850, "th": 6558741, "q4": 19676221, "yr": 132395775, "pct": -26.7},
      {"id": "b_truycap", "name": "Khối Truy cập", "deps": ["tt", "gt"], "base": 9066643.89, "day": 347555, "th": 10658344, "q4": 31975031, "yr": 236581031, "pct": -23.7}
    ]

    for blk in BLOCKS_INFO:
        html.append(f'            <tr class="row_block prog_row_block" id="row_{blk["id"]}">')
        html.append(f'              <td><strong>{blk["name"]}</strong></td>')
        html.append(f'              <td class="cell_center"><div class="badge_kpi badge_15" id="badge_rate_{blk["id"]}">+15,0%</div></td>')
        html.append(f'              <td class="cell_num" id="base_{blk["id"]}">{fmt_tr(blk["base"], 2)}</td>')
        html.append(f'              <td class="cell_num cell_day_hl" id="day_{blk["id"]}">{fmt_day(blk["day"])}</td>')
        html.append(f'              <td class="cell_num cell_primary" id="th_{blk["id"]}">{fmt_tr(blk["th"], 2)}</td>')
        html.append(f'              <td class="cell_num cell_bold" id="q4_{blk["id"]}">{fmt_tr(blk["q4"], 2)}</td>')
        html.append(f'              <td class="cell_num cell_bold" id="yr_{blk["id"]}">{fmt_tr(blk["yr"], 2)}</td>')
        html.append(f'              <td class="cell_num cell_bold" id="pct_{blk["id"]}">{fmt_pct(blk["pct"], 1)}</td>')
        html.append('            </tr>')

        for d in DEPS_INFO:
            if d["id"] in blk["deps"]:
                html.append(f'            <tr class="prog_row_dep" id="row_dep_{d["id"]}">')
                html.append(f'              <td>&nbsp;&nbsp;↳ {d["name"]}</td>')
                html.append(f'              <td class="cell_center">')
                html.append(f'                <div class="badge_kpi badge_15" id="badge_rate_{d["id"]}">+15,0%</div>')
                html.append(f'                <div class="table_input_cell is_hidden" id="input_wrap_table_{d["id"]}">')
                html.append(f'                  <input type="number" class="table_dep_input" data-dep="{d["id"]}" value="15" step="0.5">')
                html.append('                  <div class="unit_tag">%</div>')
                html.append('                </div>')
                html.append('              </td>')
                html.append(f'              <td class="cell_num" id="base_{d["id"]}">{fmt_tr(d["base"], 2)}</td>')
                html.append(f'              <td class="cell_num cell_day_hl" id="day_{d["id"]}">{fmt_day(d["day"])}</td>')
                html.append(f'              <td class="cell_num cell_primary" id="th_{d["id"]}">{fmt_tr(d["th"], 2)}</td>')
                html.append(f'              <td class="cell_num cell_bold" id="q4_{d["id"]}">{fmt_tr(d["q4"], 2)}</td>')
                html.append(f'              <td class="cell_num" id="yr_{d["id"]}">{fmt_tr(d["yr"], 2)}</td>')
                html.append(f'              <td class="cell_num" id="pct_{d["id"]}">{fmt_pct(d["pct"], 1)}</td>')
                html.append('            </tr>')

    # Total Row
    html.append('            <tr class="row_total prog_row_total" id="row_total_znews">')
    html.append('              <td><strong>Toàn Znews</strong></td>')
    html.append('              <td class="cell_center"><div class="badge_kpi badge_15" id="badge_rate_total">+15,0%</div></td>')
    html.append('              <td class="cell_num cell_bold" id="base_total">25,47M</td>')
    html.append('              <td class="cell_num cell_day_hl cell_bold" id="day_total">976.291</td>')
    html.append('              <td class="cell_num cell_primary cell_bold" id="th_total">29,94M</td>')
    html.append('              <td class="cell_num cell_bold" id="q4_total">89,82M</td>')
    html.append('              <td class="cell_num cell_bold" id="yr_total">586,28M</td>')
    html.append('              <td class="cell_num cell_bold" id="pct_total">-26,7%</td>')
    html.append('            </tr>')

    html.append('          </tbody>')
    html.append('        </table>')
    html.append('      </div>')
    html.append('    </div>')

    # 14 Department Cards Grid
    html.append('    <div class="card">')
    html.append('      <div class="dep_card_header">')
    html.append('        <div>')
    html.append('          <h3>Chi tiết KPI từng ban (14 ban biên tập)</h3>')
    html.append('        </div>')
    html.append('      </div>')
    html.append('      <div class="dep_grid">')
    for d in DEPS_INFO:
        html.append('        <div class="dep_card">')
        html.append('          <div>')
        html.append('            <div class="dep_card_header">')
        html.append(f'              <div class="dep_name">{d["name"]}</div>')
        html.append('              <div class="dep_tags">')
        html.append(f'                <div class="dep_block_tag">{d["block"]}</div>')
        html.append(f'                <div class="badge_kpi badge_15" id="card_badge_{d["id"]}">+15,0%</div>')
        html.append(f'                <div class="table_input_cell is_hidden" id="card_input_wrap_{d["id"]}">')
        html.append(f'                  <input type="number" class="card_dep_input" data-dep="{d["id"]}" value="15" step="0.5">')
        html.append('                  <div class="unit_tag">%</div>')
        html.append('                </div>')
        html.append('              </div>')
        html.append('            </div>')
        html.append('            <div class="dep_target_boxes">')
        html.append('              <div class="target_box box_day">')
        html.append('                <div class="target_box_label">Mỗi ngày</div>')
        html.append(f'                <div class="target_box_val" id="card_day_{d["id"]}">{fmt_day(d["day"])}</div>')
        html.append('              </div>')
        html.append('              <div class="target_box">')
        html.append('                <div class="target_box_label">Mỗi tháng</div>')
        html.append(f'                <div class="target_box_val" id="card_th_{d["id"]}">{fmt_tr(d["th"], 2)}</div>')
        html.append('              </div>')
        html.append('              <div class="target_box">')
        html.append('                <div class="target_box_label">Cả quý 4</div>')
        html.append(f'                <div class="target_box_val" id="card_q4_{d["id"]}">{fmt_tr(d["q4"], 2)}</div>')
        html.append('              </div>')
        html.append('            </div>')
        html.append('            <div class="dep_stat_row">')
        html.append(f'              <div>Cơ sở T9: <strong id="card_base_{d["id"]}">{fmt_tr(d["base"], 2)}</strong></div>')
        html.append(f'              <div>Cả năm 2026: <strong id="card_yr_{d["id"]}">{fmt_tr(d["yr"], 2)}</strong> (<strong id="card_pct_{d["id"]}">{fmt_pct(d["pct"], 1)}</strong> vs 2025)</div>')
        html.append('            </div>')
        html.append('          </div>')
        html.append('        </div>')
    html.append('      </div>')
    html.append('    </div>')

    # Comparison Matrix Card (Section 3 from Excel)
    html.append('    <div class="card">')
    html.append('      <div class="dep_card_header">')
    html.append('        <div>')
    html.append('          <h3>So sánh 4 mốc tăng trưởng (+10%, +15%, +20%, +50%) theo cơ sở tháng 9</h3>')
    html.append('        </div>')
    html.append('      </div>')
    html.append('      <div class="control_desc" id="compare_desc_note">KPI trung bình tháng (quy đổi 30 ngày) cho 14 ban và 4 khối theo cơ sở Zalo đang chọn.</div>')
    html.append('      <div class="table_responsive">')
    html.append('        <table class="kpi_table" id="comparison_matrix_table">')
    html.append('          <thead>')
    html.append('            <tr>')
    html.append('              <th>Đơn vị / ban</th>')
    html.append('              <th class="cell_num">Cơ sở T9 (nền)</th>')
    html.append('              <th class="cell_num">Mức +10%</th>')
    html.append('              <th class="cell_num cell_primary">Mức +15%</th>')
    html.append('              <th class="cell_num">Mức +20%</th>')
    html.append('              <th class="cell_num cell_challenge">Mức +50%</th>')
    html.append('            </tr>')
    html.append('          </thead>')
    html.append('          <tbody id="comparison_tbody">')
    # Pre-render comparison rows
    for blk in BLOCKS_INFO:
        b = blk["base"]
        html.append(f'            <tr class="row_block prog_row_block" id="cmp_row_{blk["id"]}">')
        html.append(f'              <td><strong>{blk["name"]}</strong></td>')
        html.append(f'              <td class="cell_num" id="cmp_base_{blk["id"]}">{fmt_tr(b, 2)}</td>')
        html.append(f'              <td class="cell_num" id="cmp_10_{blk["id"]}">{fmt_tr(b*1.10, 2)}</td>')
        html.append(f'              <td class="cell_num cell_primary" id="cmp_15_{blk["id"]}">{fmt_tr(b*1.15, 2)}</td>')
        html.append(f'              <td class="cell_num" id="cmp_20_{blk["id"]}">{fmt_tr(b*1.20, 2)}</td>')
        html.append(f'              <td class="cell_num cell_challenge" id="cmp_50_{blk["id"]}">{fmt_tr(b*1.50, 2)}</td>')
        html.append('            </tr>')
        for d in DEPS_INFO:
            if d["id"] in blk["deps"]:
                db = d["base"]
                html.append(f'            <tr class="prog_row_dep" id="cmp_row_dep_{d["id"]}">')
                html.append(f'              <td>&nbsp;&nbsp;↳ {d["name"]}</td>')
                html.append(f'              <td class="cell_num" id="cmp_base_{d["id"]}">{fmt_tr(db, 2)}</td>')
                html.append(f'              <td class="cell_num" id="cmp_10_{d["id"]}">{fmt_tr(db*1.10, 2)}</td>')
                html.append(f'              <td class="cell_num cell_primary" id="cmp_15_{d["id"]}">{fmt_tr(db*1.15, 2)}</td>')
                html.append(f'              <td class="cell_num" id="cmp_20_{d["id"]}">{fmt_tr(db*1.20, 2)}</td>')
                html.append(f'              <td class="cell_num cell_challenge" id="cmp_50_{d["id"]}">{fmt_tr(db*1.50, 2)}</td>')
                html.append('            </tr>')
    # Total row in comparison
    tot_base = 25468459.62
    html.append('            <tr class="row_total prog_row_total" id="cmp_row_total">')
    html.append('              <td><strong>Toàn Znews</strong></td>')
    html.append(f'              <td class="cell_num cell_bold" id="cmp_base_total">{fmt_tr(tot_base, 2)}</td>')
    html.append(f'              <td class="cell_num cell_bold" id="cmp_10_total">{fmt_tr(tot_base*1.10, 2)}</td>')
    html.append(f'              <td class="cell_num cell_primary cell_bold" id="cmp_15_total">{fmt_tr(tot_base*1.15, 2)}</td>')
    html.append(f'              <td class="cell_num cell_bold" id="cmp_20_total">{fmt_tr(tot_base*1.20, 2)}</td>')
    html.append(f'              <td class="cell_num cell_challenge cell_bold" id="cmp_50_total">{fmt_tr(tot_base*1.50, 2)}</td>')
    html.append('            </tr>')
    html.append('          </tbody>')
    html.append('        </table>')
    html.append('      </div>')
    html.append('    </div>')

    # Big CTA Footer Banner
    html.append('    <div class="cta_footer_card">')
    html.append('      <div class="cta_footer_content">')
    html.append('        <div class="cta_footer_title">Tài liệu và phương án liên quan</div>')
    html.append('        <div class="cta_footer_desc">Xem phương án đã giao chỉ tiêu chính thức theo trung bình T8–T9 hoặc đọc toàn bộ báo cáo phân tích tác động biến động truy cập.</div>')
    html.append('      </div>')
    html.append('      <div class="chip_group">')
    html.append('        <a href="kpi_phe_duyet.html" class="btn_cta_large">📋 Xem phương án TB T8–T9 đã duyệt</a>')
    html.append('        <a href="detail.html" class="btn_cta_large">📑 Xem báo cáo giải thích chi tiết</a>')
    html.append('      </div>')
    html.append('    </div>')

    # Footer
    html.append('    <footer class="page_footer">')
    html.append('      <div>Bản quyền Tạp chí điện tử Tri thức - Znews • Lưu hành nội bộ Ban biên tập</div>')
    html.append('    </footer>')

    html.append('  </div>') # end wrap
    html.append('</article>')

    # Reactive JavaScript Engine
    js = r"""
(function() {
  const DEPARTMENTS = [
    { id: 'xh', name: 'Xã hội', block: 'b_uytin', t9_scaled: 1872666.21, zalo_real: 1832748.64, zalo_hypo: 1779032.90, lk_9t: 27427000, yr_2025: 73774000 },
    { id: 'pl', name: 'Pháp luật', block: 'b_uytin', t9_scaled: 1136389.66, zalo_real: 1112166.48, zalo_hypo: 1079570.17, lk_9t: 24643000, yr_2025: 54589000 },
    { id: 'tg', name: 'Thế giới', block: 'b_uytin', t9_scaled: 862942.76, zalo_real: 844548.36, zalo_hypo: 819795.62, lk_9t: 42342000, yr_2025: 40418000 },
    { id: 'xb', name: 'Xuất bản', block: 'b_uytin', t9_scaled: 1092851.38, zalo_real: 1069556.27, zalo_hypo: 1038208.81, lk_9t: 9861000, yr_2025: 13870000 },
    { id: 'kd', name: 'Kinh doanh', block: 'b_kinhdoanh', t9_scaled: 3543875.17, zalo_real: 3468334.28, zalo_hypo: 3366681.41, lk_9t: 42582000, yr_2025: 74594000 },
    { id: 'cn', name: 'Công nghệ', block: 'b_kinhdoanh', t9_scaled: 1711225.86, zalo_real: 1674749.54, zalo_hypo: 1625664.57, lk_9t: 20937000, yr_2025: 34822000 },
    { id: 'xe', name: 'Xe', block: 'b_kinhdoanh', t9_scaled: 838888.97, zalo_real: 821007.29, zalo_hypo: 796944.52, lk_9t: 11346000, yr_2025: 17137000 },
    { id: 'ds', name: 'Đời sống', block: 'b_lifestyle', t9_scaled: 1789636.55, zalo_real: 1751488.83, zalo_hypo: 1700154.72, lk_9t: 46731000, yr_2025: 66302000 },
    { id: 'ls', name: 'Lifestyle', block: 'b_lifestyle', t9_scaled: 565807.24, zalo_real: 553746.55, zalo_hypo: 537516.88, lk_9t: 10366667, yr_2025: 16816959 },
    { id: 'sk', name: 'Sức khỏe', block: 'b_lifestyle', t9_scaled: 1931763.10, zalo_real: 1890585.83, zalo_hypo: 1835174.95, lk_9t: 27659000, yr_2025: 54215000 },
    { id: 'gd', name: 'Giáo dục', block: 'b_lifestyle', t9_scaled: 485014.14, zalo_real: 474675.62, zalo_hypo: 460763.43, lk_9t: 10917000, yr_2025: 18389000 },
    { id: 'dl', name: 'Du lịch', block: 'b_lifestyle', t9_scaled: 927988.97, zalo_real: 908208.04, zalo_hypo: 881589.52, lk_9t: 17046000, yr_2025: 24790000 },
    { id: 'tt', name: 'Thể thao', block: 'b_truycap', t9_scaled: 6593407.24, zalo_real: 6452862.82, zalo_hypo: 6263736.88, lk_9t: 150384000, yr_2025: 213207000 },
    { id: 'gt', name: 'Giải trí', block: 'b_truycap', t9_scaled: 2670709.66, zalo_real: 2613781.07, zalo_hypo: 2537174.17, lk_9t: 54222000, yr_2025: 96760000 }
  ];

  const BLOCKS = [
    { id: 'b_uytin', name: 'Khối Uy tín', deps: ['xh', 'pl', 'tg', 'xb'], lk_9t: 104273000, yr_2025: 182651000 },
    { id: 'b_kinhdoanh', name: 'Khối Kinh doanh', deps: ['kd', 'cn', 'xe'], lk_9t: 74865000, yr_2025: 126553000 },
    { id: 'b_lifestyle', name: 'Khối Lifestyle', deps: ['ds', 'ls', 'sk', 'gd', 'dl'], lk_9t: 112719554, yr_2025: 180512120 },
    { id: 'b_truycap', name: 'Khối Truy cập', deps: ['tt', 'gt'], lk_9t: 204606000, yr_2025: 309967000 }
  ];

  const TOTAL_LK_9T = 496464023;
  const TOTAL_YR_2025 = 799681703;

  let state = {
    zaloMode: 'real',
    rateMode: 'all',
    globalRate: 15.0,
    depRates: {
      xh: 15.0, pl: 15.0, tg: 15.0, xb: 15.0,
      kd: 15.0, cn: 15.0, xe: 15.0,
      ds: 15.0, ls: 15.0, sk: 15.0, gd: 15.0, dl: 15.0,
      tt: 15.0, gt: 15.0
    }
  };

  function fmtDay(n) {
    return Math.round(n).toString().replace(/\B(?=(\d{3})+(?!\d))/g, ".");
  }

  function fmtTr(n, dec) {
    if (dec === undefined) dec = 2;
    const v = n / 1000000.0;
    return v.toLocaleString('vi-VN', { minimumFractionDigits: dec, maximumFractionDigits: dec }) + 'M';
  }

  function fmtPct(p, dec) {
    if (dec === undefined) dec = 1;
    const sign = p > 0 ? '+' : '';
    return sign + p.toLocaleString('vi-VN', { minimumFractionDigits: dec, maximumFractionDigits: dec }) + '%';
  }

  function getBadgeClass(r) {
    if (r >= 50) return 'badge_challenge';
    if (r >= 20) return 'badge_20';
    if (r >= 15) return 'badge_15';
    if (r >= 10) return 'badge_10';
    return 'badge_bar';
  }

  function recalculate() {
    let depRes = {};
    let blkRes = {};
    BLOCKS.forEach(b => {
      blkRes[b.id] = { base: 0, day: 0, q4: 0, lk_9t: b.lk_9t, yr_25: b.yr_2025 };
    });
    let totRes = { base: 0, day: 0, q4: 0, lk_9t: TOTAL_LK_9T, yr_25: TOTAL_YR_2025 };

    DEPARTMENTS.forEach(d => {
      let base = d.zalo_real;
      if (state.zaloMode === 'hypo') base = d.zalo_hypo;
      else if (state.zaloMode === 'none') base = d.t9_scaled;

      let rate = state.rateMode === 'all' ? state.globalRate : (state.depRates[d.id] !== undefined ? state.depRates[d.id] : 15.0);
      let day = (base / 30.0) * (1.0 + rate / 100.0);
      let q4 = day * 92.0;
      let th = q4 / 3.0;
      let yr_26 = d.lk_9t + q4;
      let pct_25 = ((yr_26 - d.yr_2025) / d.yr_2025) * 100.0;

      depRes[d.id] = { base, rate, day, th, q4, yr_26, pct_25 };

      // Sum to block
      let blk = blkRes[d.block];
      blk.base += base;
      blk.day += day;
      blk.q4 += q4;

      // Sum to total
      totRes.base += base;
      totRes.day += day;
      totRes.q4 += q4;
    });

    BLOCKS.forEach(b => {
      let blk = blkRes[b.id];
      blk.th = blk.q4 / 3.0;
      blk.yr_26 = blk.lk_9t + blk.q4;
      blk.pct_25 = ((blk.yr_26 - blk.yr_25) / blk.yr_25) * 100.0;
      blk.implied_rate = ((blk.th / blk.base) - 1.0) * 100.0;
    });

    totRes.th = totRes.q4 / 3.0;
    totRes.yr_26 = totRes.lk_9t + totRes.q4;
    totRes.pct_25 = ((totRes.yr_26 - totRes.yr_25) / totRes.yr_25) * 100.0;
    totRes.implied_rate = ((totRes.th / totRes.base) - 1.0) * 100.0;

    return { depRes, blkRes, totRes };
  }

  function render() {
    const { depRes, blkRes, totRes } = recalculate();

    // 1. Top 4 Metric Cards
    const elDay = document.getElementById('metric_day');
    const elMonth = document.getElementById('metric_month');
    const elQ4 = document.getElementById('metric_q4');
    const elYear = document.getElementById('metric_year');
    const elYearPct = document.getElementById('metric_year_pct');

    if (elDay) elDay.textContent = fmtDay(totRes.day);
    if (elMonth) elMonth.textContent = fmtTr(totRes.th, 2);
    if (elQ4) elQ4.textContent = fmtTr(totRes.q4, 2);
    if (elYear) elYear.textContent = fmtTr(totRes.yr_26, 2);
    if (elYearPct) {
      elYearPct.textContent = fmtPct(totRes.pct_25, 1) + ' vs 2025';
      elYearPct.className = 'badge_kpi ' + (totRes.pct_25 >= 0 ? 'badge_20' : 'badge_15');
    }

    // 2. Active Mode Badge in Control Header
    const activeBadge = document.getElementById('active_mode_badge');
    if (activeBadge) {
      if (state.rateMode === 'all') {
        activeBadge.textContent = 'Đang áp tỷ lệ toàn bộ: ' + fmtPct(state.globalRate, 1);
        activeBadge.className = 'badge_kpi ' + getBadgeClass(state.globalRate);
      } else {
        activeBadge.textContent = 'Đang bật chế độ: Tùy chỉnh từng ban';
        activeBadge.className = 'badge_kpi badge_challenge';
      }
    }

    // 3. Master Table Rows
    // Total row
    const elBaseTot = document.getElementById('base_total');
    const elDayTot = document.getElementById('day_total');
    const elThTot = document.getElementById('th_total');
    const elQ4Tot = document.getElementById('q4_total');
    const elYrTot = document.getElementById('yr_total');
    const elPctTot = document.getElementById('pct_total');
    const elBadgeTot = document.getElementById('badge_rate_total');

    if (elBaseTot) elBaseTot.textContent = fmtTr(totRes.base, 2);
    if (elDayTot) elDayTot.textContent = fmtDay(totRes.day);
    if (elThTot) elThTot.textContent = fmtTr(totRes.th, 2);
    if (elQ4Tot) elQ4Tot.textContent = fmtTr(totRes.q4, 2);
    if (elYrTot) elYrTot.textContent = fmtTr(totRes.yr_26, 2);
    if (elPctTot) elPctTot.textContent = fmtPct(totRes.pct_25, 1);
    if (elBadgeTot) {
      elBadgeTot.textContent = fmtPct(totRes.implied_rate, 1);
      elBadgeTot.className = 'badge_kpi ' + getBadgeClass(totRes.implied_rate);
    }

    // Blocks
    BLOCKS.forEach(b => {
      const blk = blkRes[b.id];
      const elBase = document.getElementById('base_' + b.id);
      const elDay = document.getElementById('day_' + b.id);
      const elTh = document.getElementById('th_' + b.id);
      const elQ4 = document.getElementById('q4_' + b.id);
      const elYr = document.getElementById('yr_' + b.id);
      const elPct = document.getElementById('pct_' + b.id);
      const elBadge = document.getElementById('badge_rate_' + b.id);

      if (elBase) elBase.textContent = fmtTr(blk.base, 2);
      if (elDay) elDay.textContent = fmtDay(blk.day);
      if (elTh) elTh.textContent = fmtTr(blk.th, 2);
      if (elQ4) elQ4.textContent = fmtTr(blk.q4, 2);
      if (elYr) elYr.textContent = fmtTr(blk.yr_26, 2);
      if (elPct) elPct.textContent = fmtPct(blk.pct_25, 1);
      if (elBadge) {
        elBadge.textContent = fmtPct(blk.implied_rate, 1);
        elBadge.className = 'badge_kpi ' + getBadgeClass(blk.implied_rate);
      }
    });

    // Departments
    DEPARTMENTS.forEach(d => {
      const res = depRes[d.id];
      const elBase = document.getElementById('base_' + d.id);
      const elDay = document.getElementById('day_' + d.id);
      const elTh = document.getElementById('th_' + d.id);
      const elQ4 = document.getElementById('q4_' + d.id);
      const elYr = document.getElementById('yr_' + d.id);
      const elPct = document.getElementById('pct_' + d.id);
      const elBadge = document.getElementById('badge_rate_' + d.id);
      const elWrapInput = document.getElementById('input_wrap_table_' + d.id);

      if (elBase) elBase.textContent = fmtTr(res.base, 2);
      if (elDay) elDay.textContent = fmtDay(res.day);
      if (elTh) elTh.textContent = fmtTr(res.th, 2);
      if (elQ4) elQ4.textContent = fmtTr(res.q4, 2);
      if (elYr) elYr.textContent = fmtTr(res.yr_26, 2);
      if (elPct) elPct.textContent = fmtPct(res.pct_25, 1);

      if (elBadge && elWrapInput) {
        if (state.rateMode === 'all') {
          elBadge.textContent = fmtPct(res.rate, 1);
          elBadge.className = 'badge_kpi ' + getBadgeClass(res.rate);
          elWrapInput.classList.add('is_hidden');
          elBadge.classList.remove('is_hidden');
        } else {
          elWrapInput.classList.remove('is_hidden');
          elBadge.classList.add('is_hidden');
          const input = elWrapInput.querySelector('input');
          if (input && document.activeElement !== input) {
            input.value = res.rate;
          }
        }
      }

      // Department Cards
      const cDay = document.getElementById('card_day_' + d.id);
      const cTh = document.getElementById('card_th_' + d.id);
      const cQ4 = document.getElementById('card_q4_' + d.id);
      const cBase = document.getElementById('card_base_' + d.id);
      const cYr = document.getElementById('card_yr_' + d.id);
      const cPct = document.getElementById('card_pct_' + d.id);
      const cBadge = document.getElementById('card_badge_' + d.id);
      const cWrapInput = document.getElementById('card_input_wrap_' + d.id);

      if (cDay) cDay.textContent = fmtDay(res.day);
      if (cTh) cTh.textContent = fmtTr(res.th, 2);
      if (cQ4) cQ4.textContent = fmtTr(res.q4, 2);
      if (cBase) cBase.textContent = fmtTr(res.base, 2);
      if (cYr) cYr.textContent = fmtTr(res.yr_26, 2);
      if (cPct) cPct.textContent = fmtPct(res.pct_25, 1);

      if (cBadge && cWrapInput) {
        if (state.rateMode === 'all') {
          cBadge.textContent = fmtPct(res.rate, 1);
          cBadge.className = 'badge_kpi ' + getBadgeClass(res.rate);
          cWrapInput.classList.add('is_hidden');
          cBadge.classList.remove('is_hidden');
        } else {
          cWrapInput.classList.remove('is_hidden');
          cBadge.classList.add('is_hidden');
          const cInput = cWrapInput.querySelector('input');
          if (cInput && document.activeElement !== cInput) {
            cInput.value = res.rate;
          }
        }
      }
    });

    // 4. Update Comparison Matrix Table
    BLOCKS.forEach(b => {
      const blk = blkRes[b.id];
      const base = blk.base;
      const cBase = document.getElementById('cmp_base_' + b.id);
      const c10 = document.getElementById('cmp_10_' + b.id);
      const c15 = document.getElementById('cmp_15_' + b.id);
      const c20 = document.getElementById('cmp_20_' + b.id);
      const c50 = document.getElementById('cmp_50_' + b.id);
      if (cBase) cBase.textContent = fmtTr(base, 2);
      if (c10) c10.textContent = fmtTr(base * 1.10, 2);
      if (c15) c15.textContent = fmtTr(base * 1.15, 2);
      if (c20) c20.textContent = fmtTr(base * 1.20, 2);
      if (c50) c50.textContent = fmtTr(base * 1.50, 2);
    });

    DEPARTMENTS.forEach(d => {
      const res = depRes[d.id];
      const base = res.base;
      const cBase = document.getElementById('cmp_base_' + d.id);
      const c10 = document.getElementById('cmp_10_' + d.id);
      const c15 = document.getElementById('cmp_15_' + d.id);
      const c20 = document.getElementById('cmp_20_' + d.id);
      const c50 = document.getElementById('cmp_50_' + d.id);
      if (cBase) cBase.textContent = fmtTr(base, 2);
      if (c10) c10.textContent = fmtTr(base * 1.10, 2);
      if (c15) c15.textContent = fmtTr(base * 1.15, 2);
      if (c20) c20.textContent = fmtTr(base * 1.20, 2);
      if (c50) c50.textContent = fmtTr(base * 1.50, 2);
    });

    const cmpTotBase = totRes.base;
    const cmpTotBaseEl = document.getElementById('cmp_base_total');
    const cmpTot10 = document.getElementById('cmp_10_total');
    const cmpTot15 = document.getElementById('cmp_15_total');
    const cmpTot20 = document.getElementById('cmp_20_total');
    const cmpTot50 = document.getElementById('cmp_50_total');
    if (cmpTotBaseEl) cmpTotBaseEl.textContent = fmtTr(cmpTotBase, 2);
    if (cmpTot10) cmpTot10.textContent = fmtTr(cmpTotBase * 1.10, 2);
    if (cmpTot15) cmpTot15.textContent = fmtTr(cmpTotBase * 1.15, 2);
    if (cmpTot20) cmpTot20.textContent = fmtTr(cmpTotBase * 1.20, 2);
    if (cmpTot50) cmpTot50.textContent = fmtTr(cmpTotBase * 1.50, 2);
  }

  // EVENT LISTENERS
  // 1. Zalo Chips
  const zaloChips = document.querySelectorAll('#zalo_chips .chip');
  const zaloNote = document.getElementById('zalo_status_note');
  zaloChips.forEach(chip => {
    chip.addEventListener('click', function() {
      zaloChips.forEach(c => c.classList.remove('active'));
      this.classList.add('active');
      state.zaloMode = this.getAttribute('data-zalo');
      if (zaloNote) {
        if (state.zaloMode === 'real') {
          zaloNote.textContent = 'Mức nền T9 sau trừ Zalo thực tế (2,13%): 25,47M/tháng • 848.949 lượt/ngày (T9 gồm 29 ngày dữ liệu thực tế, quy đổi đủ 30 ngày).';
        } else if (state.zaloMode === 'hypo') {
          zaloNote.textContent = 'Mức nền T9 sau trừ Zalo giả định (5,0%): 24,72M/tháng • 824.067 lượt/ngày (Loại trừ 5,0% lượng truy cập do Zalo).';
        } else {
          zaloNote.textContent = 'Mức nền T9 gốc quy đổi đủ 30 ngày: 26,02M/tháng • 867.439 lượt/ngày (Không trừ ảnh hưởng Zalo).';
        }
      }
      render();
    });
  });

  // 2. Mode Chips
  const modeChips = document.querySelectorAll('#mode_chips .chip');
  const modeNote = document.getElementById('mode_desc_note');
  modeChips.forEach(chip => {
    chip.addEventListener('click', function() {
      modeChips.forEach(c => c.classList.remove('active'));
      this.classList.add('active');
      state.rateMode = this.getAttribute('data-mode');
      if (modeNote) {
        if (state.rateMode === 'all') {
          modeNote.textContent = 'Áp một tỷ lệ tăng trưởng đồng nhất cho toàn bộ 14 ban biên tập.';
        } else {
          modeNote.textContent = 'Chế độ tùy từng ban: Bạn có thể nhập tỷ lệ riêng cho từng ban ở bảng hoặc thẻ bên dưới. Dùng nút/ô nhập ở đây để áp nhanh toàn bộ.';
        }
      }
      render();
    });
  });

  // 3. Preset Rate Chips
  const rateChips = document.querySelectorAll('#rate_chips .chip');
  const globalInput = document.getElementById('global_rate_input');
  rateChips.forEach(chip => {
    chip.addEventListener('click', function() {
      rateChips.forEach(c => c.classList.remove('active'));
      this.classList.add('active');
      const val = parseFloat(this.getAttribute('data-rate'));
      state.globalRate = val;
      if (globalInput) globalInput.value = val;
      // If in custom mode, update all depRates
      DEPARTMENTS.forEach(d => {
        state.depRates[d.id] = val;
      });
      render();
    });
  });

  // 4. Custom Global Rate Input
  if (globalInput) {
    globalInput.addEventListener('input', function() {
      const val = parseFloat(this.value) || 0;
      state.globalRate = val;
      // Sync chips
      rateChips.forEach(c => {
        if (parseFloat(c.getAttribute('data-rate')) === val) {
          c.classList.add('active');
        } else {
          c.classList.remove('active');
        }
      });
      // If in custom mode, update all depRates
      if (state.rateMode === 'custom') {
        DEPARTMENTS.forEach(d => {
          state.depRates[d.id] = val;
        });
      }
      render();
    });
  }

  // 5. Per-department Table & Card Inputs
  function bindDepInput(inputEl) {
    inputEl.addEventListener('input', function() {
      const depId = this.getAttribute('data-dep');
      const val = parseFloat(this.value) || 0;
      state.depRates[depId] = val;

      // Sync other input for same dep
      document.querySelectorAll('input[data-dep="' + depId + '"]').forEach(inp => {
        if (inp !== inputEl) inp.value = val;
      });

      // Switch to custom mode if currently 'all'
      if (state.rateMode === 'all') {
        state.rateMode = 'custom';
        modeChips.forEach(c => {
          if (c.getAttribute('data-mode') === 'custom') c.classList.add('active');
          else c.classList.remove('active');
        });
        if (modeNote) modeNote.textContent = 'Chế độ tùy từng ban: Bạn có thể nhập tỷ lệ riêng cho từng ban ở bảng hoặc thẻ bên dưới.';
      }

      render();
    });
  }

  document.querySelectorAll('.table_dep_input').forEach(bindDepInput);
  document.querySelectorAll('.card_dep_input').forEach(bindDepInput);

  // 6. Master Table Filter Chips
  const filterChips = document.querySelectorAll('#master_filter_chips .chip');
  filterChips.forEach(chip => {
    chip.addEventListener('click', function() {
      filterChips.forEach(c => c.classList.remove('active'));
      this.classList.add('active');
      const filter = this.getAttribute('data-filter');
      const rows = document.querySelectorAll('#master_kpi_table tbody tr');
      rows.forEach(r => {
        if (filter === 'all') {
          r.classList.remove('is_hidden');
        } else if (filter === 'blocks') {
          if (r.classList.contains('prog_row_block') || r.classList.contains('prog_row_total')) {
            r.classList.remove('is_hidden');
          } else {
            r.classList.add('is_hidden');
          }
        } else if (filter === 'deps') {
          if (r.classList.contains('prog_row_dep')) {
            r.classList.remove('is_hidden');
          } else {
            r.classList.add('is_hidden');
          }
        }
      });
    });
  });

  // Initial render
  render();
})();
"""
    html.append(f'<script>{js}</script>')
    html.append('</body>')
    html.append('</html>')
    return "\n".join(html)



def build_kpi_phe_duyet_html():
    html = []
    html.append('<!DOCTYPE html>')
    html.append('<html lang="vi">')
    html.append('<head>')
    html.append('  <meta charset="UTF-8">')
    html.append('  <meta name="viewport" content="width=device-width, initial-scale=1.0">')
    html.append('  <title>Bảng giao chỉ tiêu KPI quý 4/2026 (Phương án TB T8–T9 đã phê duyệt) — Tạp chí điện tử Tri thức - Znews</title>')
    html.append(f'  <style>{css_scoped}</style>')
    html.append('</head>')
    html.append('<body>')
    html.append('<article class="container_AI">')
    html.append('  <div class="wrap">')
    
    # Top Bar Navigation
    html.append('    <nav class="top_bar_nav">')
    html.append('      <a href="index.html" class="top_nav_link">🎯 Tính KPI từ tháng 9 (Công cụ mới)</a>')
    html.append('      <a href="kpi_phe_duyet.html" class="top_nav_link active">📋 Phương án TB T8–T9 đã duyệt</a>')
    html.append('      <a href="detail.html" class="top_nav_link">📑 Báo cáo giải thích chi tiết</a>')
    html.append('    </nav>')
    
    # Header
    html.append('    <header class="top_header">')
    html.append('      <div class="brand_area">')
    html.append('        <div class="brand_kicker">Tạp chí điện tử Tri thức - Znews • Ban biên tập</div>')
    html.append('        <div class="brand_title">Bảng giao chỉ tiêu KPI quý 4/2026</div>')
    html.append('        <div class="brand_sub">Chỉ tiêu chính thức theo ngày • tháng • cả quý 4 cho 14 ban & 4 khối</div>')
    html.append('      </div>')
    html.append('      <div>')
    html.append('        <a href="detail.html" class="nav_btn_main">📑 Giải thích chi tiết & bối cảnh dữ liệu →</a>')
    html.append('      </div>')
    html.append('    </header>')

    # 4 Overview Metric Cards
    html.append('    <div class="kpi_grid_4">')
    # Card 1: Ngày
    html.append('      <div class="kpi_metric_card highlight_day">')
    html.append('        <div class="kpi_metric_label">KPI truy cập theo ngày (toàn trang)</div>')
    html.append(f'        <div class="kpi_metric_val val_green">{fmt_day(approved_total["day"])}</div>')
    html.append('      </div>')
    # Card 2: Tháng
    html.append('      <div class="kpi_metric_card highlight_month">')
    html.append('        <div class="kpi_metric_label">KPI truy cập theo tháng (toàn trang)</div>')
    html.append(f'        <div class="kpi_metric_val val_blue">{fmt_tr(approved_total["th"], 2)}M</div>')
    html.append('      </div>')
    # Card 3: Cả Quý 4
    html.append('      <div class="kpi_metric_card highlight_quarter">')
    html.append('        <div class="kpi_metric_label">KPI truy cập quý 4</div>')
    html.append(f'        <div class="kpi_metric_val val_purple">{fmt_tr(approved_total["q4"], 2)}M</div>')
    html.append('      </div>')
    # Card 4: Cả năm
    html.append('      <div class="kpi_metric_card">')
    html.append('        <div class="kpi_metric_label">Dự kiến cả năm 2026</div>')
    html.append(f'        <div class="kpi_metric_val">{fmt_tr(approved_total["yr_26"], 2)}M</div>')
    html.append('      </div>')
    html.append('    </div>')

    # Master KPI Table
    html.append('    <div class="card">')
    html.append('      <div class="dep_card_header">')
    html.append('        <div>')
    html.append('          <h3>Bảng giao chỉ tiêu: Ngày • tháng • quý 4/2026</h3>')
    html.append('        </div>')
    html.append('        <div class="controls_bar" id="master_filter_chips">')
    html.append('          <div class="chip active" data-filter="all">Tất cả (19 đơn vị)</div>')
    html.append('          <div class="chip" data-filter="blocks">Chỉ xem 4 khối</div>')
    html.append('          <div class="chip" data-filter="deps">Chỉ xem 14 ban</div>')
    html.append('        </div>')
    html.append('      </div>')
    html.append('      <div class="table_responsive">')
    html.append('        <table class="kpi_table" id="master_kpi_table">')
    html.append('          <thead>')
    html.append('            <tr>')
    html.append('              <th>Đơn vị / ban</th>')
    html.append('              <th class="cell_num cell_day_hl">KPI ngày</th>')
    html.append('              <th class="cell_num cell_primary">KPI tháng</th>')
    html.append('              <th class="cell_num cell_bold">KPI quý 4</th>')
    html.append('              <th class="cell_center">Mức tăng chốt</th>')
    html.append('              <th class="cell_num">TB T8–T9 (nền)</th>')
    html.append('            </tr>')
    html.append('          </thead>')
    html.append('          <tbody>')

    for blk in all_blocks:
        b_item = approved_blocks[blk]
        html.append('            <tr class="row_block prog_row_block">')
        html.append(f'              <td><strong>{blk}</strong></td>')
        html.append(f'              <td class="cell_num cell_day_hl">{fmt_day(b_item["day"])}</td>')
        html.append(f'              <td class="cell_num cell_primary">{fmt_tr(b_item["th"], 2)}M</td>')
        html.append(f'              <td class="cell_num cell_bold">{fmt_tr(b_item["q4"], 2)}M</td>')
        html.append(f'              <td class="cell_center"><div class="badge_kpi badge_15">+{b_item["pct"]:.1f}%</div></td>')
        html.append(f'              <td class="cell_num cell_bold">{fmt_tr(b_item["tb"], 2)}M</td>')
        html.append('            </tr>')

        for d in deps_by_block[blk]:
            d_item = approved_deps[d]
            pct_badge_cls = "badge_20" if d_item["pct"] == 20 else ("badge_10" if d_item["pct"] == 10 else "badge_15")
            html.append('            <tr class="prog_row_dep">')
            html.append(f'              <td>&nbsp;&nbsp;↳ {d}</td>')
            html.append(f'              <td class="cell_num cell_day_hl">{fmt_day(d_item["day"])}</td>')
            html.append(f'              <td class="cell_num cell_primary">{fmt_tr(d_item["th"], 2)}M</td>')
            html.append(f'              <td class="cell_num cell_bold">{fmt_tr(d_item["q4"], 2)}M</td>')
            html.append(f'              <td class="cell_center"><div class="badge_kpi {pct_badge_cls}">+{d_item["pct"]}%</div></td>')
            html.append(f'              <td class="cell_num">{fmt_tr(d_item["tb"], 2)}M</td>')
            html.append('            </tr>')

    # Total Row
    html.append('            <tr class="row_total prog_row_total">')
    html.append('              <td><strong>Toàn Znews</strong></td>')
    html.append(f'              <td class="cell_num cell_day_hl">{fmt_day(approved_total["day"])}</td>')
    html.append(f'              <td class="cell_num cell_primary cell_bold">{fmt_tr(approved_total["th"], 2)}M</td>')
    html.append(f'              <td class="cell_num cell_bold">{fmt_tr(approved_total["q4"], 2)}M</td>')
    html.append(f'              <td class="cell_center"><div class="badge_kpi badge_15">+{approved_total["pct"]:.1f}%</div></td>')
    html.append(f'              <td class="cell_num cell_bold">{fmt_tr(approved_total["tb"], 2)}M</td>')
    html.append('            </tr>')

    html.append('          </tbody>')
    html.append('        </table>')
    html.append('      </div>')
    html.append('    </div>')

    # 14 Department Cards Grid
    html.append('    <div class="card">')
    html.append('      <div class="dep_card_header">')
    html.append('        <div>')
    html.append('          <h3>Chi tiết KPI từng ban</h3>')
    html.append('        </div>')
    html.append('      </div>')
    html.append('      <div class="dep_grid">')
    for d in all_deps:
        d_item = approved_deps[d]
        pct_badge_cls = "badge_20" if d_item["pct"] == 20 else ("badge_10" if d_item["pct"] == 10 else "badge_15")
        html.append('        <div class="dep_card">')
        html.append('          <div>')
        html.append('            <div class="dep_card_header">')
        html.append(f'              <div class="dep_name">{d}</div>')
        html.append('              <div class="dep_tags">')
        html.append(f'                <div class="dep_block_tag">{d_item["khoi"]}</div>')
        html.append(f'                <div class="badge_kpi {pct_badge_cls}">+{d_item["pct"]}%</div>')
        html.append('              </div>')
        html.append('            </div>')
        html.append('            <div class="dep_target_boxes">')
        html.append('              <div class="target_box box_day">')
        html.append('                <div class="target_box_label">Mỗi ngày</div>')
        html.append(f'                <div class="target_box_val">{fmt_day(d_item["day"])}</div>')
        html.append('              </div>')
        html.append('              <div class="target_box">')
        html.append('                <div class="target_box_label">Mỗi tháng</div>')
        html.append(f'                <div class="target_box_val">{fmt_tr(d_item["th"], 2)}M</div>')
        html.append('              </div>')
        html.append('              <div class="target_box">')
        html.append('                <div class="target_box_label">Cả quý 4</div>')
        html.append(f'                <div class="target_box_val">{fmt_tr(d_item["q4"], 2)}M</div>')
        html.append('              </div>')
        html.append('            </div>')
        html.append('            <div class="dep_stat_row">')
        html.append(f'              <div>TB T8–T9 (nền): <strong>{fmt_tr(d_item["tb"], 2)}M</strong></div>')
        html.append(f'              <div>Cả năm 2026: <strong>{fmt_tr(d_item["yr_26"], 2)}M ({fmt_pct(d_item["pct_yr"])})</strong></div>')
        html.append('            </div>')
        html.append('          </div>')
        html.append('        </div>')
    html.append('      </div>')
    html.append('    </div>')

    # Big CTA Footer Banner linking to detail.html
    html.append('    <div class="cta_footer_card">')
    html.append('      <div class="cta_footer_content">')
    html.append('        <div class="cta_footer_title">Báo cáo giải thích chi tiết & bối cảnh dữ liệu</div>')
    html.append('        <div class="cta_footer_desc">Xem phân tích bối cảnh biến động tháng 8, tiến độ 9 tháng và căn cứ đề xuất mục tiêu quý 4.</div>')
    html.append('      </div>')
    html.append('      <div>')
    html.append('        <a href="detail.html" class="btn_cta_large">📑 Mở trang giải thích chi tiết & bối cảnh dữ liệu →</a>')
    html.append('      </div>')
    html.append('    </div>')
    
    # Footer
    html.append('    <footer class="page_footer">')
    html.append('      <div>Bản quyền Tạp chí điện tử Tri thức - Znews &bull; Lưu hành nội bộ Ban biên tập</div>')
    html.append('    </footer>')

    html.append('  </div>') # end wrap
    html.append('</article>')

    # JS for Index Table Filter
    js = """
(function() {
  const chips = document.querySelectorAll('#master_filter_chips .chip');
  chips.forEach(chip => {
    chip.addEventListener('click', function() {
      chips.forEach(c => c.classList.remove('active'));
      this.classList.add('active');
      const filter = this.getAttribute('data-filter');
      const rows = document.querySelectorAll('#master_kpi_table tbody tr');
      rows.forEach(r => {
        if (filter === 'all') {
          r.classList.remove('hidden_element');
        } else if (filter === 'blocks') {
          if (r.classList.contains('prog_row_block') || r.classList.contains('prog_row_total')) {
            r.classList.remove('hidden_element');
          } else {
            r.classList.add('hidden_element');
          }
        } else if (filter === 'deps') {
          if (r.classList.contains('prog_row_dep')) {
            r.classList.remove('hidden_element');
          } else {
            r.classList.add('hidden_element');
          }
        }
      });
    });
  });
})();
"""
    html.append(f'<script>{js}</script>')
    html.append('</body>')
    html.append('</html>')
    return "\n".join(html)


# =========================================================================
# BUILD DETAIL.HTML (FULL ORIGINAL ANALYSIS REPORT)
# =========================================================================
def build_detail_html():
    html = []
    html.append('<!DOCTYPE html>')
    html.append('<html lang="vi">')
    html.append('<head>')
    html.append('  <meta charset="UTF-8">')
    html.append('  <meta name="viewport" content="width=device-width, initial-scale=1.0">')
    html.append('  <title>Truy cập Znews 2025–2026 & báo cáo KPI quý 4/2026 — Tạp chí điện tử Tri thức - Znews</title>')
    html.append(f'  <style>{css_scoped}</style>')
    html.append('</head>')
    html.append('<body>')
    html.append('<article class="container_AI">')
    html.append('  <div class="wrap">')
    
    # Top Nav Bar linking to index.html
    html.append('    <div class="top_nav_back_bar">')
    html.append('      <div class="brand_kicker">Tạp chí điện tử Tri thức - Znews • Ban biên tập</div>')
    html.append('      <div><a href="index.html" class="nav_btn_back">← Về bảng giao chỉ tiêu KPI quý 4 chính thức</a></div>')
    html.append('    </div>')
    
    # Top Alert Banner explaining approved policy
    html.append('    <div class="policy_banner">')
    html.append('      <div class="policy_header">')
    html.append('        <div>')
    html.append('          <div class="policy_title">Thông báo: Chỉ tiêu KPI quý 4/2026 đã được phê duyệt chính thức</div>')
    html.append('          <div class="policy_sub">Ban biên tập đã chốt phương án: Khối Uy tín +15%, Khối Kinh doanh +15%, Khối Lifestyle +15% (riêng Lifestyle +10%), Khối Truy cập: Giải trí +15%, Thể thao +20%.</div>')
    html.append('        </div>')
    html.append('        <div><a href="index.html" class="nav_btn_main">Xem bảng giao chỉ tiêu theo ngày & tháng →</a></div>')
    html.append('      </div>')
    html.append('    </div>')
    
    # HEADER
    html.append('    <header class="page_header">')
    html.append('      <div class="badge_bar">')
    html.append('        <div class="meta_badge">Báo cáo dữ liệu Ban biên tập</div>')
    html.append('        <div class="meta_subtext">Dữ liệu chốt đến 29/09/2026 • Đơn vị: Triệu lượt truy cập</div>')
    html.append('      </div>')
    html.append('      <h1>Truy cập Znews 2025–2026 & mục tiêu KPI quý 4/2026</h1>')
    html.append('      <p class="page_desc">Đánh giá toàn cảnh tăng trưởng 7 tháng đầu năm, phân tích mức độ sụt giảm sâu sau biến động T8–T9/2026, đối chiếu tiến độ KPI 9 tháng và chi tiết <strong>4 kịch bản KPI Quý 4/2026</strong> cùng các động lực tăng trưởng cốt lõi.</p>')
    html.append('    </header>')
    
    # 4 HEADLINE KPI CARDS
    html.append('    <section class="grid_4col">')
    # Card 1: 7T Growth
    html.append('      <div class="kpi_card_head">')
    html.append('        <div class="kpi_label">7 tháng đầu 2026 vs cùng kỳ</div>')
    html.append(f'        <div class="kpi_value_huge negative">{fmt_pct(toan_t7["pct_7t"])}</div>')
    html.append(f'        <div class="kpi_sub">Đạt <strong class="num">{fmt_tr(toan_t7["t7_2026"], 2)} tr</strong> (vs {fmt_tr(toan_t7["t7_2025"], 2)} tr 2025)</div>')
    html.append('      </div>')
    # Card 2: T8-T9 Drop
    html.append('      <div class="kpi_card_head alert_card">')
    html.append('        <div class="kpi_label">Biến động T8–T9/2026</div>')
    html.append(f'        <div class="kpi_value_huge negative">{fmt_pct(toan_t7["pct_T8T9_2026_vs_cung_ky"])}</div>')
    html.append(f'        <div class="kpi_sub">Trung bình đạt <strong class="num">{fmt_tr(toan_tb, 2)} tr</strong>/tháng</div>')
    html.append('      </div>')
    # Card 3: Q4 KPI Target (HIGHLIGHT)
    html.append('      <div class="kpi_card_head highlight">')
    html.append('        <div class="kpi_label">Mục tiêu KPI quý 4 (4 kịch bản)</div>')
    html.append(f'        <div class="kpi_value_huge accent">{fmt_tr(toan_m10_q4, 2)}–{fmt_tr(toan_m50_q4, 2)} tr</div>')
    html.append(f'        <div class="kpi_sub">Mỗi tháng: <strong class="num cell_primary">{fmt_tr(toan_m10_th, 2)}–{fmt_tr(toan_m50_th, 2)} tr</strong> (+10% đến +50%)</div>')
    html.append('      </div>')
    # Card 4: Full Year Forecast
    html.append('      <div class="kpi_card_head">')
    html.append('        <div class="kpi_label">Kịch bản cả năm 2026 dự kiến</div>')
    html.append(f'        <div class="kpi_value_huge">{fmt_tr(toan_m10_yr, 2)}–{fmt_tr(toan_m50_yr, 2)} tr</div>')
    html.append(f'        <div class="kpi_sub">{fmt_pct(toan_m10_pct_yr)} – {fmt_pct(toan_m50_pct_yr)} vs 2025 ({fmt_tr(toan_yr_25, 1)} tr)</div>')
    html.append('      </div>')
    html.append('    </section>')
    
    # =======================================================
    # STICKY 3-PART NAVIGATION TABS
    # =======================================================
    html.append('    <nav class="main_nav_tabs" id="page_nav">')
    html.append('      <a href="#part1" class="nav_tab active" data-part="part1">')
    html.append('        <div class="nav_tab_badge">PHẦN 1</div>')
    html.append('        <div class="nav_tab_title">Ảnh hưởng truy cập sau biến động T8</div>')
    html.append('        <div class="nav_tab_desc">Diễn biến 2025–2026 • Tăng trưởng 7T • Sụt giảm T8–T9 • Tiến độ KPI 9T</div>')
    html.append('      </a>')
    html.append('      <a href="#part2" class="nav_tab" data-part="part2">')
    html.append('        <div class="nav_tab_badge">PHẦN 2</div>')
    html.append('        <div class="nav_tab_title">Đề xuất mức KPI mới cho Q4 & Cả năm</div>')
    html.append('        <div class="nav_tab_desc">4 Mốc kịch bản (+10%, +15%, +20%, +50%) • Kế hoạch cả năm 2026</div>')
    html.append('      </a>')
    html.append('      <a href="#part3" class="nav_tab" data-part="part3">')
    html.append('        <div class="nav_tab_badge">PHẦN 3</div>')
    html.append('        <div class="nav_tab_title">Cơ sở & Lý do đề xuất KPI mới</div>')
    html.append('        <div class="nav_tab_desc">Thực trạng hụt hơi • Đòn bẩy Zalo OA • Tín hiệu hồi phục Google</div>')
    html.append('      </a>')
    html.append('    </nav>')
    
    # =======================================================
    # PART 1: ẢNH HƯỞNG VỀ TRUY CẬP SAU THAY ĐỔI VÀO THÁNG 8
    # =======================================================
    html.append('    <div class="dashboard_part" id="part1">')
    html.append('      <div class="part_banner part1_banner">')
    html.append('        <div class="part_badge">PHẦN I</div>')
    html.append('        <h2 class="part_title">Ảnh hưởng về truy cập sau thay đổi vào tháng 8</h2>')
    html.append('        <p class="part_desc">Đánh giá toàn cảnh từ giai đoạn tăng trưởng ổn định 7 tháng đầu năm đến cú sốc sụt giảm sâu trong tháng 8–9/2026 và mức độ hụt hơi so với tiến độ KPI năm 2026.</p>')
    html.append('      </div>')
    
    # SECTION 01: MONTHLY TRENDS
    html.append('      <section class="section_block" id="sec01">')
    html.append('        <div class="section_header">')
    html.append('          <div class="section_title_wrap">')
    html.append('            <div class="section_num">01</div>')
    html.append('            <div>')
    html.append('              <div class="section_title">Diễn biến truy cập theo tháng (2025–2026)</div>')
    html.append('              <div class="section_sub">So sánh cùng kỳ 2025 vs 2026 và dải mục tiêu Quý 4/2026 (+10% đến +50%)</div>')
    html.append('            </div>')
    html.append('          </div>')
    html.append('        </div>')
    html.append('        <div class="card">')
    html.append('          <div class="controls_bar" id="monthly_block_chips">')
    html.append('            <div class="chip active" data-entity="Toàn Znews">Toàn Znews</div>')
    html.append('            <div class="chip" data-entity="Khối Uy tín">Khối Uy tín</div>')
    html.append('            <div class="chip" data-entity="Khối Kinh doanh">Khối Kinh doanh</div>')
    html.append('            <div class="chip" data-entity="Khối Lifestyle">Khối Lifestyle</div>')
    html.append('            <div class="chip" data-entity="Khối Truy cập">Khối Truy cập</div>')
    html.append('          </div>')
    html.append('          <div class="controls_bar" id="monthly_dep_chips">')
    for d in all_deps:
        html.append(f'            <div class="chip chip_sm" data-entity="{d}">{d}</div>')
    html.append('          </div>')
    html.append(build_monthly_chart_svg())
    html.append('        </div>')
    html.append('      </section>')
    
    # SECTION 02: 7-MONTH GROWTH
    html.append('      <section class="section_block" id="sec02">')
    html.append('        <div class="section_header">')
    html.append('          <div class="section_title_wrap">')
    html.append('            <div class="section_num">02</div>')
    html.append('            <div>')
    html.append('              <div class="section_title">Tăng trưởng 7 tháng đầu năm (Giai đoạn trước biến động)</div>')
    html.append('              <div class="section_sub">Toàn trang giảm nhẹ -6,5% vs cùng kỳ 2025; Khối Truy cập là khối duy nhất tăng trưởng (+2,4%)</div>')
    html.append('            </div>')
    html.append('          </div>')
    html.append('        </div>')
    html.append('        <div class="grid_2col">')
    html.append('          <div class="card">')
    html.append('            <h3>Tăng trưởng 14 chuyên mục (7T/2026 vs 7T/2025)</h3>')
    html.append('            <p>Xếp hạng theo % tăng/giảm cùng đánh giá mục tiêu</p>')
    html.append(build_t7_growth_bar_svg())
    html.append('          </div>')
    html.append('          <div class="card">')
    html.append('            <h3>Quy mô truy cập 4 khối & toàn trang (7T/2025 vs 7T/2026)</h3>')
    html.append('            <p>Điểm xám: 7T/2025 | Điểm xanh: 7T/2026 (triệu lượt)</p>')
    html.append(build_t7_dumbbell_svg())
    html.append('          </div>')
    html.append('        </div>')
    html.append('      </section>')
    
    # SECTION 03: T8-T9 DROP (ZERO TEXT OVERLAP)
    html.append('      <section class="section_block" id="sec03">')
    html.append('        <div class="section_header">')
    html.append('          <div class="section_title_wrap">')
    html.append('            <div class="section_num">03</div>')
    html.append('            <div>')
    html.append('              <div class="section_title">Mức độ sụt giảm T8–T9/2026 sau biến động</div>')
    html.append('              <div class="section_sub">So sánh T8–T9/2026 so với cùng kỳ 2025: Toàn trang sụt giảm 58,1%; 13/14 ban giảm trên 40%</div>')
    html.append('            </div>')
    html.append('          </div>')
    html.append('        </div>')
    html.append('        <div class="card">')
    html.append('          <h3>Tỷ lệ sụt giảm trung bình tháng T8–T9/2026 vs cùng kỳ 2025</h3>')
    html.append('          <p>Trục 0% ở bên trái, thanh bar mở rộng sang phải, đảm bảo không che lấp nhãn đơn vị</p>')
    html.append(build_drop_t8t9_svg())
    html.append('        </div>')
    html.append('      </section>')
    
    # SECTION 04: TIẾN ĐỘ THỰC HIỆN KPI 9 THÁNG & CÚ SỐC THÁNG 8 (NEW)
    html.append('      <section class="section_block" id="sec04">')
    html.append('        <div class="section_header">')
    html.append('          <div class="section_title_wrap">')
    html.append('            <div class="section_num">04</div>')
    html.append('            <div>')
    html.append('              <div class="section_title">Tiến độ thực hiện KPI năm 2026 theo ban & Cú sốc tháng 8</div>')
    html.append('              <div class="section_sub">So sánh tỷ lệ hoàn thành KPI 7 tháng, 8 tháng và 9 tháng đầu năm 2026 so với mốc chuẩn (58,3% → 66,7% → 75,0%)</div>')
    html.append('            </div>')
    html.append('          </div>')
    html.append('        </div>')
    
    # 4 Stat Cards for KPI Progress
    html.append('        <div class="grid_4col">')
    # Card 1: 7T Progress
    html.append('          <div class="kpi_card_head">')
    html.append('            <div class="kpi_label">Tiến độ 7 tháng (trước biến động)</div>')
    html.append('            <div class="kpi_value_huge">52,7%</div>')
    html.append('            <div class="kpi_sub">Mốc chuẩn: <strong>58,3%</strong> (Đạt 439,9 / 834,2 tr. Thể thao 61,4%, Đời sống 59,4%, Thế giới 90,0% vượt chuẩn)</div>')
    html.append('          </div>')
    # Card 2: Shock Month 8
    html.append('          <div class="kpi_card_head warn_card">')
    html.append('            <div class="kpi_label">Bước ngoặt tháng 8 (chững lại)</div>')
    html.append('            <div class="kpi_value_huge warning_val">56,5%</div>')
    html.append('            <div class="kpi_sub">Mốc chuẩn: <strong>66,7%</strong> (Hụt 10,2 điểm %. Tháng 8 chỉ nhích thêm 3,8% so với mức tăng 7,5%/tháng trước đó)</div>')
    html.append('          </div>')
    # Card 3: 9M Status
    html.append('          <div class="kpi_card_head alert_card">')
    html.append('            <div class="kpi_label">Hiện trạng sau 9 tháng</div>')
    html.append('            <div class="kpi_value_huge negative">59,5%</div>')
    html.append('            <div class="kpi_sub">Mốc chuẩn: <strong>75,0%</strong> (Hụt 15,5 điểm %. 13/14 chuyên mục chậm tiến độ, Xã hội 31,9%, Pháp luật 39,5%)</div>')
    html.append('          </div>')
    # Card 4: Q4 Impossible Gap
    html.append('          <div class="kpi_card_head alert_card">')
    html.append('            <div class="kpi_label">Thách thức quý 4 nếu giữ KPI cũ</div>')
    html.append('            <div class="kpi_value_huge negative">+298,1%</div>')
    html.append('            <div class="kpi_sub">Còn thiếu <strong>337,74 tr</strong>. Mỗi tháng cần <strong>112,58 tr</strong> (gấp 4 lần thực tế T8–T9: 28,28 tr) — Bất khả thi!</div>')
    html.append('          </div>')
    html.append('        </div>')
    
    # Progress Table Card
    html.append('        <div class="card">')
    html.append('          <div class="dep_card_header">')
    html.append('            <div>')
    html.append('              <h3>Bảng chi tiết tiến độ KPI 2026 qua các mốc 7T, 8T, 9T (19 đơn vị)</h3>')
    html.append('              <p>Vạch đen trên thanh tiến độ thể hiện mốc chuẩn thời gian: 7T = 58,3% | 8T = 66,7% | 9T = 75,0%</p>')
    html.append('            </div>')
    html.append('            <div class="controls_bar" id="prog_filter_chips">')
    html.append('              <div class="chip active" data-filter="all">Tất cả (19)</div>')
    html.append('              <div class="chip" data-filter="blocks">Chỉ xem khối</div>')
    html.append('              <div class="chip" data-filter="deps">Chỉ xem ban</div>')
    html.append('              <div class="chip" data-filter="heavy_lag">Chậm nặng (&gt;300%)</div>')
    html.append('            </div>')
    html.append('          </div>')
    
    html.append('          <div class="table_responsive">')
    html.append('            <table class="kpi_table" id="prog_table">')
    html.append('              <thead>')
    html.append('                <tr>')
    html.append('                  <th>Đơn vị / Ban</th>')
    html.append('                  <th class="cell_num">KPI Năm 2026</th>')
    html.append('                  <th class="cell_num">Đạt 7T (Chuẩn 58,3%)</th>')
    html.append('                  <th class="cell_num">Đạt 8T (Chuẩn 66,7%)</th>')
    html.append('                  <th class="cell_num">Đạt 9T (Chuẩn 75,0%)</th>')
    html.append('                  <th class="cell_num">Còn thiếu</th>')
    html.append('                  <th class="cell_num">Cần/tháng Q4</th>')
    html.append('                  <th class="cell_center">Cần tăng vs TB T8–T9</th>')
    html.append('                </tr>')
    html.append('              </thead>')
    html.append('              <tbody>')
    
    for item in tien_do_kpi:
        name = item["ten"]
        khoi = item["khoi"]
        kpi_nam = item["kpi_nam_2026"] / 1000000.0
        d7 = item["dat_7t"] / 1000000.0
        p7 = item["pct_kpi_7t"]
        d8 = item["dat_8t"] / 1000000.0
        p8 = item["pct_kpi_8t"]
        d9 = item["dat_9t"] / 1000000.0
        p9 = item["pct_kpi_9t"]
        thieu = item["con_thieu"] / 1000000.0
        can_th = item["can_moi_thang_q4"] / 1000000.0
        can_pct = item["pct_can_thang_vs_tb_T8T9"]
    
        is_total = (name == "Toàn Znews")
        is_block = (name in all_blocks)
        is_heavy_lag = (can_pct > 300.0)
    
        row_class = "row_total" if is_total else ("row_block" if is_block else "")
        cat_class = "prog_row_total" if is_total else ("prog_row_block" if is_block else "prog_row_dep")
        if is_heavy_lag:
            cat_class += " prog_row_heavylag"
    
        indent = "" if (is_total or is_block) else "&nbsp;&nbsp;↳ "
        display_name = f"<strong>{name}</strong>" if (is_total or is_block) else f"{indent}{name}"
    
        svg_bar_7t = build_mini_progress_svg(p7, benchmarks.get("7t", 58.3))
        svg_bar_8t = build_mini_progress_svg(p8, benchmarks.get("8t", 66.7))
        svg_bar_9t = build_mini_progress_svg(p9, benchmarks.get("9t", 75.0))
    
        cls_p7 = "pct_good" if p7 >= 58.3 else ("pct_warn" if p7 >= 50.0 else "pct_bad")
        cls_p8 = "pct_good" if p8 >= 66.7 else ("pct_warn" if p8 >= 58.0 else "pct_bad")
        cls_p9 = "pct_good" if p9 >= 75.0 else ("pct_warn" if p9 >= 65.0 else "pct_bad")
    
        if can_pct > 300.0:
            badge_req = f'<div class="badge_critical">+{can_pct:.1f}%</div>'
        elif can_pct > 100.0:
            badge_req = f'<div class="badge_warning">+{can_pct:.1f}%</div>'
        elif can_pct > 0.0:
            badge_req = f'<div class="badge_warning">+{can_pct:.1f}%</div>'
        else:
            badge_req = f'<div class="badge_success">{can_pct:.1f}%</div>'
    
        html.append(f'                <tr class="{row_class} {cat_class}">')
        html.append(f'                  <td>{display_name}</td>')
        html.append(f'                  <td class="cell_num cell_bold">{fmt_tr(kpi_nam * 1000, 2)} tr</td>')
        html.append(f'                  <td class="cell_num"><div class="prog_cell"><div class="prog_val_line"><strong class="num">{fmt_tr(d7 * 1000, 2)} tr</strong><strong class="prog_pct {cls_p7}">({p7:.1f}%)</strong></div>{svg_bar_7t}</div></td>')
        html.append(f'                  <td class="cell_num"><div class="prog_cell"><div class="prog_val_line"><strong class="num">{fmt_tr(d8 * 1000, 2)} tr</strong><strong class="prog_pct {cls_p8}">({p8:.1f}%)</strong></div>{svg_bar_8t}</div></td>')
        html.append(f'                  <td class="cell_num"><div class="prog_cell"><div class="prog_val_line"><strong class="num">{fmt_tr(d9 * 1000, 2)} tr</strong><strong class="prog_pct {cls_p9}">({p9:.1f}%)</strong></div>{svg_bar_9t}</div></td>')
        html.append(f'                  <td class="cell_num">{fmt_tr(thieu * 1000, 2)} tr</td>')
        html.append(f'                  <td class="cell_num cell_primary">{fmt_tr(can_th * 1000, 2)} tr</td>')
        html.append(f'                  <td class="cell_center">{badge_req}</td>')
        html.append('                </tr>')
    
    html.append('              </tbody>')
    html.append('            </table>')
    html.append('          </div>')
    html.append('        </div>')
    html.append('      </section>')
    html.append('    </div>') # end part1
    
    # =======================================================
    # PART 2: ĐỀ XUẤT CÁC MỨC KPI MỚI CHO QUÝ 4 VÀ CẢ NĂM 2026
    # =======================================================
    html.append('    <div class="dashboard_part" id="part2">')
    html.append('      <div class="part_banner part2_banner">')
    html.append('        <div class="part_badge">PHẦN II</div>')
    html.append('        <h2 class="part_title">Đề xuất các mức KPI mới cho Quý 4 & Cả năm 2026</h2>')
    html.append('        <p class="part_desc">Xây dựng 4 kịch bản KPI thực tế và phân cấp mục tiêu dựa trên thực tế sau biến động T8–T9: Mức +10% (Cơ sở), Mức +15% (Phấn đấu), Mức +20% (Thử thách) và Mức +50% (Cần thiết để lấy lại truy cập).</p>')
    html.append('      </div>')
    
    # SECTION 05: CORE EMPHASIS - KPI QUÝ 4/2026 TỪNG BAN & TỪNG THÁNG (4 TIERS)
    html.append('      <section class="section_block" id="sec05">')
    html.append('        <div class="section_header">')
    html.append('          <div class="section_title_wrap">')
    html.append('            <div class="section_num">05</div>')
    html.append('            <div>')
    html.append('              <div class="section_title">Mục tiêu KPI Quý 4/2026 từng ban & từng tháng (Trọng tâm)</div>')
    html.append('              <div class="section_sub">Chi tiết 4 mức mục tiêu: +10% (Cơ sở), +15% (Phấn đấu), +20% (Thử thách) và +50% (Cần thiết để lấy lại truy cập)</div>')
    html.append('            </div>')
    html.append('          </div>')
    html.append('        </div>')
    
    # 4 Blocks summary hero cards
    html.append('        <div class="card">')
    html.append('          <h3>Tổng hợp 4 kịch bản KPI Quý 4/2026 của 4 Khối & Toàn trang</h3>')
    html.append('          <p>Khoảng giá trị trải dài từ mốc Cơ sở (+10%) đến mốc Phục hồi truy cập (+50%). Tổng Q4 = KPI tháng × 3.</p>')
    html.append('          <div class="grid_4col card_hero_inner">')
    for blk in all_blocks:
        b_kpi = kpi_4tiers[blk]
        html.append('            <div class="kpi_card_head">')
        html.append(f'              <div class="kpi_label">{blk}</div>')
        html.append(f'              <div class="kpi_value_huge accent">{fmt_tr(b_kpi["m10"]["q4"], 2)}–{fmt_tr(b_kpi["m50"]["q4"], 2)} tr</div>')
        html.append(f'              <div class="kpi_sub">Mỗi tháng: <strong class="num cell_primary">{fmt_tr(b_kpi["m10"]["th"], 2)}–{fmt_tr(b_kpi["m50"]["th"], 2)} tr</strong></div>')
        html.append('            </div>')
    html.append('          </div>')
    html.append('        </div>')
    
    # Master Table Card
    html.append('        <div class="card">')
    html.append('          <div class="dep_card_header">')
    html.append('            <div>')
    html.append('              <h3>Bảng phân bổ KPI Quý 4/2026 chi tiết 4 mốc (19 đơn vị)</h3>')
    html.append('              <p>Chọn các nút bên phải để làm nổi bật mốc KPI cần quan sát</p>')
    html.append('            </div>')
    # 4-Tier Switcher Chips
    html.append('            <div class="controls_bar" id="kpi_tier_chips">')
    html.append('              <div class="chip active" data-tier="all">Xem cả 4 mức</div>')
    html.append('              <div class="chip" data-tier="10">+10% (Cơ sở)</div>')
    html.append('              <div class="chip" data-tier="15">+15% (Phấn đấu)</div>')
    html.append('              <div class="chip" data-tier="20">+20% (Thử thách)</div>')
    html.append('              <div class="chip" data-tier="50">+50% (Lấy lại truy cập)</div>')
    html.append('            </div>')
    html.append('          </div>')
    
    # Master 19-row Table with 4 tiers
    html.append('          <div class="table_responsive">')
    html.append('            <table class="kpi_table">')
    html.append('              <thead>')
    html.append('                <tr>')
    html.append('                  <th>Đơn vị / Ban</th>')
    html.append('                  <th class="cell_num">TB T8–T9</th>')
    html.append('                  <th class="cell_num col_10">KPI/Tháng (+10%)</th>')
    html.append('                  <th class="cell_num col_15">KPI/Tháng (+15%)</th>')
    html.append('                  <th class="cell_num col_20">KPI/Tháng (+20%)</th>')
    html.append('                  <th class="cell_num col_50">KPI/Tháng (+50%)</th>')
    html.append('                  <th class="cell_num col_10">Tổng Q4 (+10%)</th>')
    html.append('                  <th class="cell_num col_20">Tổng Q4 (+20%)</th>')
    html.append('                  <th class="cell_num col_50">Tổng Q4 (+50%)</th>')
    html.append('                  <th class="cell_num">Cả năm (+10% → +50%)</th>')
    html.append('                </tr>')
    html.append('              </thead>')
    html.append('              <tbody>')
    
    for blk in all_blocks:
        b_item = kpi_4tiers[blk]
        html.append('                <tr class="row_block">')
        html.append(f'                  <td><strong>{blk}</strong></td>')
        html.append(f'                  <td class="cell_num">{fmt_tr(b_item["tb"], 2)} tr</td>')
        html.append(f'                  <td class="cell_num col_10 cell_primary">{fmt_tr(b_item["m10"]["th"], 2)} tr</td>')
        html.append(f'                  <td class="cell_num col_15 cell_primary">{fmt_tr(b_item["m15"]["th"], 2)} tr</td>')
        html.append(f'                  <td class="cell_num col_20 cell_challenge">{fmt_tr(b_item["m20"]["th"], 2)} tr</td>')
        html.append(f'                  <td class="cell_num col_50 cell_recover">{fmt_tr(b_item["m50"]["th"], 2)} tr</td>')
        html.append(f'                  <td class="cell_num col_10 cell_bold">{fmt_tr(b_item["m10"]["q4"], 2)} tr</td>')
        html.append(f'                  <td class="cell_num col_20 cell_challenge">{fmt_tr(b_item["m20"]["q4"], 2)} tr</td>')
        html.append(f'                  <td class="cell_num col_50 cell_recover">{fmt_tr(b_item["m50"]["q4"], 2)} tr</td>')
        html.append(f'                  <td class="cell_num">{fmt_tr(b_item["m10"]["yr"], 1)} → {fmt_tr(b_item["m50"]["yr"], 1)} tr ({fmt_pct(b_item["m10"]["pct_yr"])} → {fmt_pct(b_item["m50"]["pct_yr"])})</td>')
        html.append('                </tr>')
    
        for d in deps_by_block[blk]:
            d_item = kpi_4tiers[d]
            html.append('                <tr>')
            html.append(f'                  <td>&nbsp;&nbsp;↳ {d}</td>')
            html.append(f'                  <td class="cell_num">{fmt_tr(d_item["tb"], 2)} tr</td>')
            html.append(f'                  <td class="cell_num col_10 cell_primary">{fmt_tr(d_item["m10"]["th"], 2)} tr</td>')
            html.append(f'                  <td class="cell_num col_15 cell_primary">{fmt_tr(d_item["m15"]["th"], 2)} tr</td>')
            html.append(f'                  <td class="cell_num col_20 cell_challenge">{fmt_tr(d_item["m20"]["th"], 2)} tr</td>')
            html.append(f'                  <td class="cell_num col_50 cell_recover">{fmt_tr(d_item["m50"]["th"], 2)} tr</td>')
            html.append(f'                  <td class="cell_num col_10 cell_bold">{fmt_tr(d_item["m10"]["q4"], 2)} tr</td>')
            html.append(f'                  <td class="cell_num col_20 cell_challenge">{fmt_tr(d_item["m20"]["q4"], 2)} tr</td>')
            html.append(f'                  <td class="cell_num col_50 cell_recover">{fmt_tr(d_item["m50"]["q4"], 2)} tr</td>')
            html.append(f'                  <td class="cell_num">{fmt_tr(d_item["m10"]["yr"], 1)} → {fmt_tr(d_item["m50"]["yr"], 1)} tr (<strong class="cell_neg">{fmt_pct(d_item["m10"]["pct_yr"])} → {fmt_pct(d_item["m50"]["pct_yr"])}</strong>)</td>')
            html.append('                </tr>')
    
    # Total row
    t_item = kpi_4tiers["Toàn Znews"]
    html.append('                <tr class="row_total">')
    html.append('                  <td><strong>TOÀN ZNEWS</strong></td>')
    html.append(f'                  <td class="cell_num">{fmt_tr(t_item["tb"], 2)} tr</td>')
    html.append(f'                  <td class="cell_num col_10">{fmt_tr(t_item["m10"]["th"], 2)} tr</td>')
    html.append(f'                  <td class="cell_num col_15">{fmt_tr(t_item["m15"]["th"], 2)} tr</td>')
    html.append(f'                  <td class="cell_num col_20">{fmt_tr(t_item["m20"]["th"], 2)} tr</td>')
    html.append(f'                  <td class="cell_num col_50">{fmt_tr(t_item["m50"]["th"], 2)} tr</td>')
    html.append(f'                  <td class="cell_num col_10">{fmt_tr(t_item["m10"]["q4"], 2)} tr</td>')
    html.append(f'                  <td class="cell_num col_20">{fmt_tr(t_item["m20"]["q4"], 2)} tr</td>')
    html.append(f'                  <td class="cell_num col_50">{fmt_tr(t_item["m50"]["q4"], 2)} tr</td>')
    html.append(f'                  <td class="cell_num">{fmt_tr(t_item["m10"]["yr"], 1)} → {fmt_tr(t_item["m50"]["yr"], 1)} tr ({fmt_pct(t_item["m10"]["pct_yr"])} → {fmt_pct(t_item["m50"]["pct_yr"])})</td>')
    html.append('                </tr>')
    
    html.append('              </tbody>')
    html.append('            </table>')
    html.append('          </div>')
    html.append('        </div>')
    
    # Grouped Bar Chart
    html.append('        <div class="card">')
    html.append('          <h3>So sánh mục tiêu tháng Quý 4/2026 theo từng ban (TB vs +10% vs +20% vs +50%)</h3>')
    html.append('          <p>Cột hiển thị theo thứ tự: TB T8–T9 (nhạt) → +10% Cơ sở → +20% Thử thách → +50% Lấy lại truy cập (đậm nhất)</p>')
    html.append(build_kpi_comparison_svg())
    html.append('        </div>')
    
    # 14 Detailed Department Cards
    html.append('        <div class="dep_grid">')
    for d in all_deps:
        d_item = kpi_4tiers[d]
        blk = dep_block_map[d]
        html.append('          <div class="dep_card">')
        html.append('            <div>')
        html.append('              <div class="dep_card_header">')
        html.append(f'                <div class="dep_name">{d}</div>')
        html.append(f'                <div class="dep_block_tag">{blk}</div>')
        html.append('              </div>')
        html.append('              <div class="dep_stat_row">')
        html.append('                <div class="stat_box">')
        html.append('                  <div class="stat_box_label">Trung bình T8–T9/2026</div>')
        html.append(f'                  <div class="stat_box_val">{fmt_tr(d_item["tb"], 2)} tr</div>')
        html.append('                </div>')
        html.append('                <div class="stat_box">')
        html.append('                  <div class="stat_box_label">Q4/2025 Thực tế</div>')
        html.append(f'                  <div class="stat_box_val">{fmt_tr(d_item["q4_25"], 2)} tr</div>')
        html.append('                </div>')
        html.append('              </div>')
        
        # 4 Targets breakdown
        html.append('              <div class="target_row">')
        html.append('                <div class="target_tier">+10% (Cơ sở):</div>')
        html.append(f'                <div class="target_val">{fmt_tr(d_item["m10"]["th"], 2)} tr/tháng &bull; Q4: {fmt_tr(d_item["m10"]["q4"], 2)} tr</div>')
        html.append('              </div>')
        html.append('              <div class="target_row">')
        html.append('                <div class="target_tier">+15% (Phấn đấu):</div>')
        html.append(f'                <div class="target_val">{fmt_tr(d_item["m15"]["th"], 2)} tr/tháng &bull; Q4: {fmt_tr(d_item["m15"]["q4"], 2)} tr</div>')
        html.append('              </div>')
        html.append('              <div class="target_row">')
        html.append('                <div class="target_tier">+20% (Thử thách):</div>')
        html.append(f'                <div class="target_val">{fmt_tr(d_item["m20"]["th"], 2)} tr/tháng &bull; Q4: {fmt_tr(d_item["m20"]["q4"], 2)} tr</div>')
        html.append('              </div>')
        html.append('              <div class="target_row gold">')
        html.append('                <div class="target_tier">+50% (Lấy lại truy cập):</div>')
        html.append(f'                <div class="target_val gold">{fmt_tr(d_item["m50"]["th"], 2)} tr/tháng &bull; Q4: {fmt_tr(d_item["m50"]["q4"], 2)} tr</div>')
        html.append('              </div>')
        html.append('            </div>')
        
        html.append('            <div class="dep_footer_row">')
        html.append(f'              <div>Cả năm 2026: <strong>{fmt_tr(d_item["m10"]["yr"], 2)}–{fmt_tr(d_item["m50"]["yr"], 2)} tr</strong></div>')
        html.append(f'              <div>Tăng trưởng vs 2025: <strong class="cell_neg">{fmt_pct(d_item["m10"]["pct_yr"])} → {fmt_pct(d_item["m50"]["pct_yr"])}</strong></div>')
        html.append('            </div>')
        html.append('          </div>')
    html.append('        </div>')
    html.append('      </section>')
    
    # SECTION 06: FULL YEAR FORECAST
    html.append('      <section class="section_block" id="sec06">')
    html.append('        <div class="section_header">')
    html.append('          <div class="section_title_wrap">')
    html.append('            <div class="section_num">06</div>')
    html.append('            <div>')
    html.append('              <div class="section_title">Kịch bản cả năm 2026 so với 2025 (4 Mức KPI)</div>')
    html.append('              <div class="section_sub">Kịch bản cả năm 2026 biến thiên từ 589,79 triệu (-26,2% ở mức +10%) lên 623,74 triệu (-22,0% ở mức +50% phục hồi truy cập)</div>')
    html.append('            </div>')
    html.append('          </div>')
    html.append('        </div>')
    html.append('        <div class="grid_2col">')
    html.append('          <div class="card">')
    html.append('            <h3>Quy mô cả năm 2025 vs 2026 (4 Khối + Toàn trang)</h3>')
    html.append('            <p>Điểm xám: 2025 | Xanh: Mức +10% | Tím đen: Mức +50% (triệu lượt)</p>')
    html.append(build_year_dumbbell_svg())
    html.append('          </div>')
    html.append('          <div class="card">')
    html.append('            <h3>Tăng trưởng cả năm 2026 vs 2025 theo 14 chuyên mục</h3>')
    html.append('            <p>Hiển thị khoảng % tăng/giảm từ mức +10% đến mức +50%</p>')
    html.append(build_year_growth_bar_svg())
    html.append('          </div>')
    html.append('        </div>')
    html.append('      </section>')
    html.append('    </div>') # end part2
    
    # =======================================================
    # PART 3: CƠ SỞ & LÝ DO ĐỀ XUẤT MỨC KPI MỚI
    # =======================================================
    html.append('    <div class="dashboard_part" id="part3">')
    html.append('      <div class="part_banner part3_banner">')
    html.append('        <div class="part_badge">PHẦN III</div>')
    html.append('        <h2 class="part_title">Cơ sở & Lý do đề xuất mức KPI mới</h2>')
    html.append('        <p class="part_desc">Lý giải nguyên nhân không thể giữ KPI cũ và phân tích chi tiết 2 đòn bẩy tăng trưởng cốt lõi giúp Quý 4 phục hồi: Kênh Zalo OA và Thuật toán đề xuất của Google.</p>')
    html.append('      </div>')
    
    html.append('      <section class="section_block" id="sec07">')
    html.append('        <div class="section_header">')
    html.append('          <div class="section_title_wrap">')
    html.append('            <div class="section_num">07</div>')
    html.append('            <div>')
    html.append('              <div class="section_title">Nhận định chuyên sâu & Luận cứ chiến lược KPI Quý 4/2026</div>')
    html.append('              <div class="section_sub">Căn cứ thực tiễn từ đà sụt giảm và lộ trình phục hồi lưu lượng dựa trên 2 động lực cốt lõi</div>')
    html.append('            </div>')
    html.append('          </div>')
    html.append('        </div>')
    
    # 3 Pillars of Strategic Rationale
    html.append('        <div class="reason_grid">')
    
    # Card 1: Tại sao không thể giữ KPI cũ
    html.append('          <div class="reason_card">')
    html.append('            <div class="reason_header">')
    html.append('              <div class="reason_icon icon_shock">⚠️</div>')
    html.append('              <div>')
    html.append('                <div class="reason_title">Tại sao không thể giữ KPI đầu năm?</div>')
    html.append('                <div class="section_sub">Cú sốc sụt giảm sâu & Khoảng cách bất khả thi</div>')
    html.append('              </div>')
    html.append('            </div>')
    html.append('            <div class="reason_body">')
    html.append('              Biến động tháng 8–9/2026 đã khiến lưu lượng toàn trang giảm <strong>58,1%</strong>, kéo mức trung bình tháng về <strong>28,28 triệu lượt</strong>. Sau 9 tháng, toàn trang mới đạt <strong>59,5%</strong> kế hoạch năm (chuẩn là 75,0%), còn thiếu tới <strong>337,74 triệu lượt</strong>.')
    html.append('              <ul class="reason_bullets">')
    html.append('                <li><strong>Áp lực phi thực tế:</strong> Nếu giữ nguyên KPI cũ, mỗi tháng Quý 4 cần đạt <strong>112,58 triệu lượt</strong>, tức phải tăng <strong>+298,1% (gấp 4 lần)</strong> so với thực tế hiện tại.</li>')
    html.append('                <li><strong>Mức tăng bất khả thi ở các ban:</strong> Xã hội cần tăng <strong>+955,4%</strong>, Pháp luật tăng <strong>+721,8%</strong>, Giải trí tăng <strong>+399,6%</strong>, Đời sống tăng <strong>+366,3%</strong>.</li>')
    html.append('                <li><strong>Kết luận:</strong> Việc giữ nguyên KPI cũ sẽ tạo áp lực quá tải, làm triệt tiêu động lực của đội ngũ. Cần tái lập KPI dựa trên trung bình T8–T9 làm mốc chặn đáy để phục hồi từng bước.</li>')
    html.append('              </ul>')
    html.append('            </div>')
    html.append('          </div>')
    
    # Card 2: Đòn bẩy 1 - Zalo OA
    html.append('          <div class="reason_card">')
    html.append('            <div class="reason_header">')
    html.append('              <div class="reason_icon icon_zalo">💬</div>')
    html.append('              <div>')
    html.append('                <div class="reason_title">Đòn bẩy 1: Khai thác Kênh Zalo OA</div>')
    html.append('                <div class="section_sub">Tiếp cận trực tiếp độc giả trung thành không qua tìm kiếm</div>')
    html.append('              </div>')
    html.append('            </div>')
    html.append('            <div class="reason_body">')
    html.append('              Zalo là nền tảng tin nhắn lớn nhất Việt Nam với hơn 75 triệu người dùng hoạt động. Hệ thống Zalo Official Account (OA) của Znews sở hữu tệp người theo dõi trung thành, là kênh kéo traffic trực tiếp vô cùng hiệu quả.')
    html.append('              <ul class="reason_bullets">')
    html.append('                <li><strong>Bắn tin chủ động (Broadcast):</strong> Thay vì phụ thuộc vào tìm kiếm, Znews chủ động gửi các tin nóng, bài phóng sự độc quyền, tuyến bài thể thao/giải trí vào các khung giờ vàng (8h–9h, 11h30–12h30, 20h–21h).</li>')
    html.append('                <li><strong>Tạo lưu lượng tức thời (Instant Traffic):</strong> Mỗi đợt phát tin Zalo OA có thể tạo ra hàng trăm nghìn lượt đọc trong thời gian ngắn, giúp bù đắp ngay lập tức phần thiếu hụt từ Google.</li>')
    html.append('                <li><strong>Cá nhân hóa nội dung:</strong> Phân luồng chủ đề theo sở thích của độc giả (bóng đá, sức khỏe, tài chính, lối sống) để nâng cao tỷ lệ mở đọc (CTR) và thời gian đọc bài.</li>')
    html.append('              </ul>')
    html.append('            </div>')
    html.append('          </div>')
    
    # Card 3: Đòn bẩy 2 - Google Domain Warmup
    html.append('          <div class="reason_card">')
    html.append('            <div class="reason_header">')
    html.append('              <div class="reason_icon icon_google">🔍</div>')
    html.append('              <div>')
    html.append('                <div class="reason_title">Đòn bẩy 2: Google quen dần với tên miền mới</div>')
    html.append('                <div class="section_sub">Thuật toán lập chỉ mục ổn định & Mở luồng Google Discover</div>')
    html.append('              </div>')
    html.append('            </div>')
    html.append('            <div class="reason_body">')
    html.append('              Sau giai đoạn chuyển dịch tên miền vào tháng 8, hệ thống bot tìm kiếm của Google (Googlebot) cần thời gian từ 6 đến 8 tuần để quét lại dữ liệu (crawl budget), lập lại chỉ mục (indexing) và đánh giá lại độ uy tín (Domain Authority).')
    html.append('              <ul class="reason_bullets">')
    html.append('                <li><strong>Tên miền mới đã "ấm máy" (Domain Warm-up):</strong> Đến cuối tháng 9 và bước sang Quý 4, hệ thống máy chủ và cấu trúc sitemap mới đã được Google nhận diện ổn định, giảm thiểu lỗi thu thập dữ liệu.</li>')
    html.append('                <li><strong>Mở lại đề xuất Google Discover:</strong> Google đã bắt đầu đề xuất trở lại các bài viết chất lượng cao của Znews trên luồng Khám phá (Discover) của hàng chục triệu người dùng Android/iOS.</li>')
    html.append('                <li><strong>Thu hồi thứ hạng từ khóa:</strong> Các chuyên mục thế mạnh (Thể thao, Kinh doanh, Công nghệ, Xe) bắt đầu lấy lại vị trí top tìm kiếm tự nhiên (Organic Search), tạo dòng truy cập tự nhiên bền vững.</li>')
    html.append('              </ul>')
    html.append('            </div>')
    html.append('          </div>')
    
    # Card 4: Tổng kết & Lộ trình 4 Mốc KPI
    html.append('          <div class="reason_card">')
    html.append('            <div class="reason_header">')
    html.append('              <div class="reason_icon icon_shock">🎯</div>')
    html.append('              <div>')
    html.append('                <div class="reason_title">Lộ trình 4 Mốc KPI Quý 4/2026</div>')
    html.append('                <div class="section_sub">Chiến lược phục hồi từng nấc thang vững chắc</div>')
    html.append('              </div>')
    html.append('            </div>')
    html.append('            <div class="reason_body">')
    html.append('              Sự kết hợp giữa <strong>Zalo OA</strong> (đòn bẩy chủ động) và <strong>Google SEO/Discover</strong> (phục hồi tự nhiên) tạo cơ sở kỹ thuật vững chắc để Znews đặt mục tiêu tăng trưởng dương trong Quý 4:')
    html.append('              <ul class="reason_bullets">')
    html.append('                <li><strong>Mốc +10% (Cơ sở - 31,11 tr/th):</strong> Mức chặn đáy tối thiểu để giữ ổn định hệ thống.</li>')
    html.append('                <li><strong>Mốc +15% (Phấn đấu - 32,52 tr/th):</strong> Tận dụng đà bắn tin Zalo OA đều đặn hàng tuần.</li>')
    html.append('                <li><strong>Mốc +20% (Thử thách - 33,94 tr/th):</strong> Vượt mốc tâm lý 100 triệu lượt/quý khi Google Discover hồi phục.</li>')
    html.append('                <li><strong>Mốc +50% (Phục hồi - 42,43 tr/th):</strong> Thu hẹp đà giảm cả năm 2026 xuống <strong>-22,0%</strong>, tiệm cận kế hoạch đầu năm và tạo bàn đạp mạnh mẽ cho năm 2027.</li>')
    html.append('              </ul>')
    html.append('            </div>')
    html.append('          </div>')
    
    html.append('        </div>') # end reason_grid
    
    # Action Matrix for 4 Blocks
    html.append('        <div class="card card_spaced">')
    html.append('          <h3>Ma trận hành động theo 4 Khối biên tập trong Quý 4/2026</h3>')
    html.append('          <p>Phân công trọng tâm tác chiến để kích hoạt tối đa 2 đòn bẩy Zalo OA và Google Search/Discover</p>')
    html.append('          <div class="matrix_grid">')
    
    html.append('            <div class="matrix_card">')
    html.append('              <div class="matrix_title">1. Khối Truy cập</div>')
    html.append('              <div class="matrix_sub"><strong>Mũi nhọn kéo traffic:</strong> Thể thao & Giải trí chiếm 39% dung lượng toàn trang. Trọng tâm: Tường thuật trực tiếp sự kiện lớn cuối năm, khai thác tin nóng tức thời và phối hợp bắn tin Zalo OA khung giờ vàng tối.</div>')
    html.append('            </div>')
    
    html.append('            <div class="matrix_card">')
    html.append('              <div class="matrix_title">2. Khối Lifestyle</div>')
    html.append('              <div class="matrix_sub"><strong>Tối ưu Google Discover:</strong> Đời sống, Sức khỏe, Du lịch, Giáo dục, Lifestyle. Trọng tâm: Tuyến bài hình ảnh đẹp, infographic chuyên sâu, bắt trend mùa lễ hội, ẩm thực cuối năm để lên top đề xuất Discover.</div>')
    html.append('            </div>')
    
    html.append('            <div class="matrix_card">')
    html.append('              <div class="matrix_title">3. Khối Kinh doanh</div>')
    html.append('              <div class="matrix_sub"><strong>Tối ưu SEO chuyên sâu:</strong> Kinh doanh, Công nghệ, Xe. Trọng tâm: Bắt trọn từ khóa mua sắm cuối năm, xu hướng bất động sản, tài chính, ra mắt xe và thiết bị công nghệ mới.</div>')
    html.append('            </div>')
    
    html.append('            <div class="matrix_card">')
    html.append('              <div class="matrix_title">4. Khối Uy tín</div>')
    html.append('              <div class="matrix_sub"><strong>Củng cố Domain Trust:</strong> Xã hội, Pháp luật, Thế giới, Xuất bản. Trọng tâm: Giữ vững uy tín thương hiệu, tạo nguồn tin xác thực (E-E-A-T) giúp Google nhanh chóng nâng điểm tín nhiệm cho tên miền mới.</div>')
    html.append('            </div>')
    
    html.append('          </div>')
    
    # Callout banner for Data adjustment & notes
    html.append('          <div class="callout_banner">')
    html.append('            <div class="callout_title">📌 Ghi chú điều chỉnh số liệu & Minh bạch dữ liệu</div>')
    html.append('            <div class="callout_text">')
    html.append('              Dữ liệu ngày 08/12/2025 của chuyên mục <em>Lifestyle</em> đã được điều chỉnh về số chuẩn (91.774 lượt thay vì 19.177.465 do lỗi nhập thừa số), đưa tổng lượt truy cập năm 2025 của Lifestyle về 16,82 triệu, Khối Lifestyle về 180,51 triệu và Toàn Znews về 799,68 triệu. Dữ liệu tháng 9/2026 được chốt đến hết ngày 29/09/2026. Số liệu các khối và toàn trang được tổng hợp chuẩn xác từ 14 chuyên mục thành phần.')
    html.append('            </div>')
    html.append('          </div>')
    
    html.append('        </div>')
    html.append('      </section>')
    html.append('    </div>') # end part3
    
    # FOOTER
    html.append('    <footer class="page_footer">')
    html.append('      <div>Nguồn dữ liệu: <strong>Tong hop truy cap 2025-2026.xlsx</strong> &bull; Sheet "Tiến độ KPI 2026" & "Truy cập (new)" (Cập nhật 29/09/2026)</div>')
    html.append('      <div>Bản quyền Tạp chí điện tử Tri thức - Znews &bull; Lưu hành nội bộ Ban biên tập</div>')
    html.append('    </footer>')
    
    
    # Bottom CTA linking to index.html
    html.append('    <div class="cta_footer_card">')
    html.append('      <div class="cta_footer_content">')
    html.append('        <div class="cta_footer_title">Đã nắm rõ bối cảnh và cơ sở đề xuất?</div>')
    html.append('        <div class="cta_footer_desc">Bấm nút bên dưới để quay lại bảng giao chỉ tiêu KPI quý 4/2026 chính thức phân bổ theo ngày, tháng và cả quý cho từng ban biên tập.</div>')
    html.append('      </div>')
    html.append('      <div>')
    html.append('        <a href="index.html" class="btn_cta_large">← Trở về bảng giao chỉ tiêu KPI quý 4</a>')
    html.append('      </div>')
    html.append('    </div>')
    html.append('  </div>') # wrap
    html.append('</article>') # container_AI
    
    # EMBEDDED JAVASCRIPT FOR INTERACTIVITY (NO INLINE STYLE ATTRIBUTES)
    client_data_json = json.dumps({
        "monthly": monthly_series,
        "kpi": {k: {"tb": v["tb"], "m10": v["m10"]["th"], "m15": v["m15"]["th"], "m20": v["m20"]["th"], "m50": v["m50"]["th"]} for k, v in kpi_4tiers.items()}
    }, ensure_ascii=False)
    
    js_script = f"""
    (function() {{
      const rawData = {client_data_json};
      const W = 960, H = 440, L = 65, R = 45, T = 45, B = 60;
      const PW = W - L - R, PH = H - T - B;
      const xs = [];
      for (let i = 0; i < 12; i++) xs.push(L + i * (PW / 11.0));
    
      function fmtTr(k) {{
        const v = k / 1000.0;
        return v.toLocaleString('vi-VN', {{ minimumFractionDigits: 1, maximumFractionDigits: 2 }}) + ' tr';
      }}
    
      // 1. Line chart updater
      function updateLineChart(name) {{
        const s = rawData.monthly[name];
        if (!s) return;
        const kpi = rawData.kpi[name];
        if (!kpi) return;
    
        let maxVal = Math.max(...s.vals_2025, ...s.vals_2026, kpi.m10, kpi.m20, kpi.m50);
        maxVal = Math.ceil((maxVal * 1.15) / 1000) * 1000;
        if (maxVal < 1000) maxVal = 1000;
    
        function getY(val) {{
          return T + PH - (val / maxVal) * PH;
        }}
    
        const yTicks = [0, maxVal * 0.25, maxVal * 0.5, maxVal * 0.75, maxVal];
        const gridLines = document.querySelectorAll('.grid_line');
        const yLabels = document.querySelectorAll('.axis_label_y');
        yTicks.forEach((yt, idx) => {{
          const yp = getY(yt);
          if (gridLines[idx]) {{
            gridLines[idx].setAttribute('y1', yp.toFixed(1));
            gridLines[idx].setAttribute('y2', yp.toFixed(1));
          }}
          if (yLabels[idx]) {{
            yLabels[idx].setAttribute('y', (yp + 4).toFixed(1));
            yLabels[idx].textContent = fmtTr(yt);
          }}
        }});
    
        const p25 = s.vals_2025.map((v, i) => `${{xs[i].toFixed(1)}},${{getY(v).toFixed(1)}}`).join(' ');
        const path25 = document.getElementById('path_2025');
        if (path25) path25.setAttribute('d', `M ${{p25.replace(/ /g, ' L ')}}`);
    
        const p26 = s.vals_2026.map((v, i) => `${{xs[i].toFixed(1)}},${{getY(v).toFixed(1)}}`).join(' ');
        const path26 = document.getElementById('path_2026');
        if (path26) path26.setAttribute('d', `M ${{p26.replace(/ /g, ' L ')}}`);
    
        const dots25 = document.querySelectorAll('.dot_2025');
        dots25.forEach((d, i) => {{
          if (s.vals_2025[i] !== undefined) {{
            d.setAttribute('cy', getY(s.vals_2025[i]).toFixed(1));
          }}
        }});
    
        const dots26 = document.querySelectorAll('.dot_2026');
        dots26.forEach((d, i) => {{
          if (s.vals_2026[i] !== undefined) {{
            d.setAttribute('cy', getY(s.vals_2026[i]).toFixed(1));
          }}
        }});
    
        const yT9 = getY(s.vals_2026[8]);
        const yM10 = getY(kpi.m10);
        const yM20 = getY(kpi.m20);
        const yM50 = getY(kpi.m50);
    
        const poly = document.getElementById('poly_target');
        if (poly) {{
          const ptsPoly = `${{xs[8].toFixed(1)}},${{yT9.toFixed(1)}} ${{xs[9].toFixed(1)}},${{yM50.toFixed(1)}} ${{xs[10].toFixed(1)}},${{yM50.toFixed(1)}} ${{xs[11].toFixed(1)}},${{yM50.toFixed(1)}} ${{xs[11].toFixed(1)}},${{yM10.toFixed(1)}} ${{xs[10].toFixed(1)}},${{yM10.toFixed(1)}} ${{xs[9].toFixed(1)}},${{yM10.toFixed(1)}} ${{xs[8].toFixed(1)}},${{yT9.toFixed(1)}}`;
          poly.setAttribute('points', ptsPoly);
        }}
    
        const pM10 = document.getElementById('path_target_m10');
        if (pM10) {{
          const d10 = `M ${{xs[8].toFixed(1)}},${{yT9.toFixed(1)}} L ${{xs[9].toFixed(1)}},${{yM10.toFixed(1)}} L ${{xs[10].toFixed(1)}},${{yM10.toFixed(1)}} L ${{xs[11].toFixed(1)}},${{yM10.toFixed(1)}}`;
          pM10.setAttribute('d', d10);
        }}
    
        const pM20 = document.getElementById('path_target_m20');
        if (pM20) {{
          const d20 = `M ${{xs[8].toFixed(1)}},${{yT9.toFixed(1)}} L ${{xs[9].toFixed(1)}},${{yM20.toFixed(1)}} L ${{xs[10].toFixed(1)}},${{yM20.toFixed(1)}} L ${{xs[11].toFixed(1)}},${{yM20.toFixed(1)}}`;
          pM20.setAttribute('d', d20);
        }}
    
        const pM50 = document.getElementById('path_target_m50');
        if (pM50) {{
          const d50 = `M ${{xs[8].toFixed(1)}},${{yT9.toFixed(1)}} L ${{xs[9].toFixed(1)}},${{yM50.toFixed(1)}} L ${{xs[10].toFixed(1)}},${{yM50.toFixed(1)}} L ${{xs[11].toFixed(1)}},${{yM50.toFixed(1)}}`;
          pM50.setAttribute('d', d50);
        }}
    
        const dotsM10 = document.querySelectorAll('.dot_target_10');
        dotsM10.forEach(d => d.setAttribute('cy', yM10.toFixed(1)));
    
        const dotsM20 = document.querySelectorAll('.dot_target_20');
        dotsM20.forEach(d => d.setAttribute('cy', yM20.toFixed(1)));
    
        const dotsM50 = document.querySelectorAll('.dot_target_50');
        dotsM50.forEach(d => d.setAttribute('cy', yM50.toFixed(1)));
    
        const lblT1 = document.getElementById('lbl_t1');
        if (lblT1) {{
          lblT1.setAttribute('y', (getY(s.vals_2026[0]) - 12).toFixed(1));
          lblT1.textContent = `${{fmtTr(s.vals_2026[0])}}`;
        }}
    
        const lblT8 = document.getElementById('lbl_t8');
        if (lblT8) {{
          lblT8.setAttribute('y', (getY(s.vals_2026[7]) - 12).toFixed(1));
          lblT8.textContent = `${{fmtTr(s.vals_2026[7])}}`;
        }}
    
        const lblT9 = document.getElementById('lbl_t9');
        if (lblT9) {{
          lblT9.setAttribute('y', (yT9 + 18).toFixed(1));
          lblT9.textContent = `${{fmtTr(s.vals_2026[8])}}`;
        }}
    
        const lblTarget = document.getElementById('lbl_target');
        if (lblTarget) {{
          lblTarget.setAttribute('y', (yM50 - 12).toFixed(1));
          lblTarget.textContent = `Dải mục tiêu Q4: ${{fmtTr(kpi.m10)}}–${{fmtTr(kpi.m50)}}/tháng`;
        }}
      }}
    
      // 2. Entity chips listener
      const allChips = document.querySelectorAll('#monthly_block_chips .chip, #monthly_dep_chips .chip');
      allChips.forEach(chip => {{
        chip.addEventListener('click', function() {{
          allChips.forEach(c => c.classList.remove('active'));
          this.classList.add('active');
          const entity = this.getAttribute('data-entity');
          updateLineChart(entity);
        }});
      }});
    
      // 3. 4-Tier switcher (+10%, +15%, +20%, +50%)
      const tierChips = document.querySelectorAll('#kpi_tier_chips .chip');
      const cols10 = document.querySelectorAll('.col_10');
      const cols15 = document.querySelectorAll('.col_15');
      const cols20 = document.querySelectorAll('.col_20');
      const cols50 = document.querySelectorAll('.col_50');
      
      const rows10 = document.querySelectorAll('.row_tier_10');
      const rows15 = document.querySelectorAll('.row_tier_15');
      const rows20 = document.querySelectorAll('.row_tier_20');
      const rows50 = document.querySelectorAll('.row_tier_50');
    
      tierChips.forEach(chip => {{
        chip.addEventListener('click', function() {{
          tierChips.forEach(c => c.classList.remove('active'));
          this.classList.add('active');
          const tier = this.getAttribute('data-tier');
    
          // Clear all highlights
          cols10.forEach(c => c.classList.remove('table_col_highlight', 'table_col_highlight_gold'));
          cols15.forEach(c => c.classList.remove('table_col_highlight', 'table_col_highlight_gold'));
          cols20.forEach(c => c.classList.remove('table_col_highlight', 'table_col_highlight_gold'));
          cols50.forEach(c => c.classList.remove('table_col_highlight', 'table_col_highlight_gold'));
    
          rows10.forEach(r => r.classList.remove('tier_focus', 'tier_focus_50'));
          rows15.forEach(r => r.classList.remove('tier_focus', 'tier_focus_50'));
          rows20.forEach(r => r.classList.remove('tier_focus', 'tier_focus_50'));
          rows50.forEach(r => r.classList.remove('tier_focus', 'tier_focus_50'));
    
          if (tier === '10') {{
            cols10.forEach(c => c.classList.add('table_col_highlight'));
            rows10.forEach(r => r.classList.add('tier_focus'));
          }} else if (tier === '15') {{
            cols15.forEach(c => c.classList.add('table_col_highlight'));
            rows15.forEach(r => r.classList.add('tier_focus'));
          }} else if (tier === '20') {{
            cols20.forEach(c => c.classList.add('table_col_highlight'));
            rows20.forEach(r => r.classList.add('tier_focus'));
          }} else if (tier === '50') {{
            cols50.forEach(c => c.classList.add('table_col_highlight_gold'));
            rows50.forEach(r => r.classList.add('tier_focus_50'));
          }}
        }});
      }});
    
      // 4. Progress Table Filter (All / Blocks / Deps / Heavy Lag)
      const progChips = document.querySelectorAll('#prog_filter_chips .chip');
      const progRowsBlock = document.querySelectorAll('.prog_row_block');
      const progRowsDep = document.querySelectorAll('.prog_row_dep');
      const progRowsTotal = document.querySelectorAll('.prog_row_total');
    
      progChips.forEach(chip => {{
        chip.addEventListener('click', function() {{
          progChips.forEach(c => c.classList.remove('active'));
          this.classList.add('active');
          const filter = this.getAttribute('data-filter');
    
          const allProgRows = document.querySelectorAll('#prog_table tbody tr');
          allProgRows.forEach(r => {{
            if (filter === 'all') {{
              r.classList.remove('hidden_element');
            }} else if (filter === 'blocks') {{
              if (r.classList.contains('prog_row_block') || r.classList.contains('prog_row_total')) {{
                r.classList.remove('hidden_element');
              }} else {{
                r.classList.add('hidden_element');
              }}
            }} else if (filter === 'deps') {{
              if (r.classList.contains('prog_row_dep')) {{
                r.classList.remove('hidden_element');
              }} else {{
                r.classList.add('hidden_element');
              }}
            }} else if (filter === 'heavy_lag') {{
              if (r.classList.contains('prog_row_heavylag')) {{
                r.classList.remove('hidden_element');
              }} else {{
                r.classList.add('hidden_element');
              }}
            }}
          }});
        }});
      }});
    
      // 5. Sticky Navigation ScrollSpy
      const navTabs = document.querySelectorAll('.main_nav_tabs .nav_tab');
      const partSections = ['part1', 'part2', 'part3'].map(id => document.getElementById(id));
    
      navTabs.forEach(tab => {{
        tab.addEventListener('click', function(e) {{
          navTabs.forEach(t => t.classList.remove('active'));
          this.classList.add('active');
        }});
      }});
    
      window.addEventListener('scroll', function() {{
        const scrollPos = window.scrollY + 180;
        let currentPart = 'part1';
        partSections.forEach(section => {{
          if (section && section.offsetTop <= scrollPos) {{
            currentPart = section.getAttribute('id');
          }}
        }});
        navTabs.forEach(tab => {{
          if (tab.getAttribute('data-part') === currentPart) {{
            tab.classList.add('active');
          }} else {{
            tab.classList.remove('active');
          }}
        }});
      }});
    
    }})();
    """
    
    html.append(f'<script>{js_script}</script>')
    html.append('</body>')
    html.append('</html>')
    
    full_html = "\n".join(html)
    
    
    return full_html


# =========================================================================
# GENERATE AND VALIDATE BOTH FILES
# =========================================================================
def validate_html(html_str, filename):
    print(f"Validating {filename}...")
    style_matches = re.findall(r'\bstyle\s*=', html_str)
    assert len(style_matches) == 0, f"{filename}: Found inline style attributes: {style_matches}"

    span_matches = re.findall(r'<\/?span\b', html_str)
    assert len(span_matches) == 0, f"{filename}: Found span tags: {span_matches}"

    btn_matches = re.findall(r'<\/?button\b', html_str)
    assert len(btn_matches) == 0, f"{filename}: Found button tags: {btn_matches}"

    assert "data:image" not in html_str, f"{filename}: Found base64 images!"
    assert '<article class="container_AI">' in html_str, f"{filename}: Missing container_AI"
    assert '<div class="wrap">' in html_str, f"{filename}: Missing wrap"
    print(f"PASS: {filename} 100% compliant with Znews CMS rules!")

print("Generating index.html (Interactive September 2026 KPI Calculator)...")
index_html = build_interactive_t9_index_html()

print("Generating kpi_phe_duyet.html (Approved KPI Assignment Dashboard)...")
kpi_phe_duyet_html = build_kpi_phe_duyet_html()

print("Generating detail.html (Full Explanatory Report)...")
detail_html = build_detail_html()

validate_html(index_html, "index.html")
validate_html(kpi_phe_duyet_html, "kpi_phe_duyet.html")
validate_html(detail_html, "detail.html")

with open("index.html", "w", encoding="utf-8") as f:
    f.write(index_html)

with open("kpi_phe_duyet.html", "w", encoding="utf-8") as f:
    f.write(kpi_phe_duyet_html)

with open("detail.html", "w", encoding="utf-8") as f:
    f.write(detail_html)

print("SUCCESS: All 3 pages (index.html, kpi_phe_duyet.html, detail.html) generated and saved successfully!")

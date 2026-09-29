# -*- coding: utf-8 -*-
"""
Production-grade generator for Znews Q4 2026 Static Dashboard.
100% compliance with Znews CMS:
- No inline style="" anywhere in HTML or JS
- No <span> tags anywhere (div/em/strong/b/small used instead)
- No <button> tags anywhere (div.chip / a.chip used instead)
- No base64 images (pure inline SVG)
- Fully responsive, mobile font size increased ~15%
- Full-bleed 100vw layout scoped in .container_AI
- Numbers formatted in Vietnamese locale (1.000,00)
- Emphasis on monthly and Q4 KPI for every department
- Section 03 fixed: clear column layout, zero text-chart overlap
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

toan_kpi = kpi_dict["Toàn Znews"]
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
# SVG CHARTS BUILDERS
# ==========================================

def build_monthly_chart_svg():
    W, H = 960, 430
    L, R, T, B = 65, 45, 45, 60
    PW, PH = W - L - R, H - T - B
    xs = [L + i * (PW / 11.0) for i in range(12)]
    
    s25 = monthly_series["Toàn Znews"]["vals_2025"]
    s26 = monthly_series["Toàn Znews"]["vals_2026"]
    m10_val = toan_kpi["muc_10"]["kpi_moi_thang"]
    m15_val = toan_kpi["muc_15"]["kpi_moi_thang"]
    
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
    svg.append('    <stop offset="0%" stop-color="#e0e7ff" stop-opacity="0.6"/>')
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
        x = xs[i]
        svg.append(f'<line class="axis_tick" x1="{x:.1f}" y1="{T+PH}" x2="{x:.1f}" y2="{T+PH+6}" stroke="#c7cdda" stroke-width="1.5"/>')
        thang_lbl = f"T{i+1}"
        svg.append(f'<text class="axis_label_x" x="{x:.1f}" y="{T+PH+24}" text-anchor="middle" fill="#14161c" font-size="13" font-weight="600" font-family="Manrope">{thang_lbl}</text>')

    y_t9 = get_y(s26[8])
    y_m10 = get_y(m10_val)
    y_m15 = get_y(m15_val)
    
    target_poly = f"{xs[8]:.1f},{y_t9:.1f} {xs[9]:.1f},{y_m15:.1f} {xs[10]:.1f},{y_m15:.1f} {xs[11]:.1f},{y_m15:.1f} {xs[11]:.1f},{y_m10:.1f} {xs[10]:.1f},{y_m10:.1f} {xs[9]:.1f},{y_m10:.1f} {xs[8]:.1f},{y_t9:.1f}"
    svg.append(f'<polygon id="poly_target" points="{target_poly}" fill="url(#targetGrad)"/>')

    pts_2025 = [f"{xs[i]:.1f},{get_y(s25[i]):.1f}" for i in range(12)]
    d_2025 = "M " + " L ".join(pts_2025)
    svg.append(f'<path id="path_2025" d="{d_2025}" fill="none" stroke="#94a3b8" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>')

    for i in range(12):
        svg.append(f'<circle class="dot_2025" cx="{xs[i]:.1f}" cy="{get_y(s25[i]):.1f}" r="3.5" fill="#ffffff" stroke="#94a3b8" stroke-width="2"/>')

    pts_2026 = [f"{xs[i]:.1f},{get_y(s26[i]):.1f}" for i in range(9)]
    d_2026 = "M " + " L ".join(pts_2026)
    svg.append(f'<path id="path_2026" d="{d_2026}" fill="none" stroke="#3b56e0" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"/>')

    for i in range(9):
        svg.append(f'<circle class="dot_2026" cx="{xs[i]:.1f}" cy="{get_y(s26[i]):.1f}" r="4.5" fill="#3b56e0" stroke="#ffffff" stroke-width="2"/>')

    pts_m10 = [f"{xs[8]:.1f},{y_t9:.1f}"] + [f"{xs[i]:.1f},{y_m10:.1f}" for i in range(9, 12)]
    d_m10 = "M " + " L ".join(pts_m10)
    svg.append(f'<path id="path_target_m10" d="{d_m10}" fill="none" stroke="#3b56e0" stroke-width="2.5" stroke-dasharray="6,4" stroke-linecap="round"/>')

    pts_m15 = [f"{xs[8]:.1f},{y_t9:.1f}"] + [f"{xs[i]:.1f},{y_m15:.1f}" for i in range(9, 12)]
    d_m15 = "M " + " L ".join(pts_m15)
    svg.append(f'<path id="path_target_m15" d="{d_m15}" fill="none" stroke="#98a6ee" stroke-width="2.5" stroke-dasharray="6,4" stroke-linecap="round"/>')

    for i in range(9, 12):
        svg.append(f'<circle class="dot_target_10" cx="{xs[i]:.1f}" cy="{y_m10:.1f}" r="4" fill="#ffffff" stroke="#3b56e0" stroke-width="2"/>')
        svg.append(f'<circle class="dot_target_15" cx="{xs[i]:.1f}" cy="{y_m15:.1f}" r="4" fill="#ffffff" stroke="#98a6ee" stroke-width="2"/>')

    svg.append(f'<text id="lbl_t1" class="chart_val_lbl" x="{xs[0]:.1f}" y="{get_y(s26[0])-12:.1f}" text-anchor="middle" fill="#3b56e0" font-size="12" font-weight="700" font-family="Manrope">{fmt_tr(s26[0], 1)} tr</text>')
    svg.append(f'<text id="lbl_t8" class="chart_val_lbl" x="{xs[7]:.1f}" y="{get_y(s26[7])-12:.1f}" text-anchor="middle" fill="#c2410c" font-size="12" font-weight="700" font-family="Manrope">{fmt_tr(s26[7], 1)} tr</text>')
    svg.append(f'<text id="lbl_t9" class="chart_val_lbl" x="{xs[8]:.1f}" y="{y_t9+18:.1f}" text-anchor="middle" fill="#c2410c" font-size="12" font-weight="700" font-family="Manrope">{fmt_tr(s26[8], 1)} tr</text>')
    svg.append(f'<text id="lbl_target" class="chart_val_lbl" x="{xs[11]:.1f}" y="{y_m15-12:.1f}" text-anchor="end" fill="#3b56e0" font-size="12" font-weight="800" font-family="Manrope">Mục tiêu Q4: {fmt_tr(m10_val, 1)}–{fmt_tr(m15_val, 1)} tr/tháng</text>')

    svg.append('</svg>')
    return "\n".join(svg)


def build_t7_growth_bar_svg():
    sorted_deps = sorted(all_deps, key=lambda d: growth_dict[d]["pct_7t"], reverse=True)
    W, H = 510, 520
    row_h = 32
    top_offset = 45
    x_zero = 205
    scale = 2.45
    
    svg = []
    svg.append(f'<svg class="chart_svg" viewBox="0 0 {W} {H}" width="100%" height="auto" xmlns="http://www.w3.org/2000/svg">')
    svg.append(f'<line x1="{x_zero}" y1="{top_offset-15}" x2="{x_zero}" y2="{top_offset + 14 * row_h}" stroke="#14161c" stroke-width="1.5"/>')
    svg.append(f'<text x="{x_zero}" y="{top_offset-22}" text-anchor="middle" fill="#6c7280" font-size="11" font-weight="700" font-family="Manrope">0%</text>')
    
    for i, name in enumerate(sorted_deps):
        y = top_offset + i * row_h
        item = growth_dict[name]
        pct = item["pct_7t"]
        danh_gia = item["danh_gia"]
        bar_len = abs(pct) * scale
        
        if pct >= 0:
            fill_col = "#16a34a" if pct > 10 else "#3b56e0"
            bx = x_zero
            val_x = x_zero + bar_len + 6
            val_anchor = "start"
            val_col = fill_col
        else:
            fill_col = "#c2410c"
            bx = x_zero - bar_len
            val_x = x_zero - bar_len - 6
            val_anchor = "end"
            val_col = "#c2410c"
            
        if i % 2 == 1:
            svg.append(f'<rect x="10" y="{y-14}" width="{W-20}" height="{row_h}" fill="#fbfcfe" rx="4"/>')
            
        weight = "700" if pct > 0 else "500"
        svg.append(f'<text x="10" y="{y+4}" fill="#14161c" font-size="13" font-weight="{weight}" font-family="Be Vietnam Pro">{name}</text>')
        svg.append(f'<rect x="{bx:.1f}" y="{y-8}" width="{bar_len:.1f}" height="16" fill="{fill_col}" rx="3"/>')
        svg.append(f'<text x="{val_x:.1f}" y="{y+4}" text-anchor="{val_anchor}" fill="{val_col}" font-size="12" font-weight="700" font-family="Manrope">{fmt_pct(pct)}</text>')
        
        badge_bg = "#ecfdf5" if "Vượt" in danh_gia else ("#eff6ff" if "Đạt" in danh_gia else ("#fffbeb" if "dưới" in danh_gia else "#fef2f2"))
        badge_fg = "#15803d" if "Vượt" in danh_gia else ("#1d4ed8" if "Đạt" in danh_gia else ("#b45309" if "dưới" in danh_gia else "#991b1b"))
        svg.append(f'<rect x="420" y="{y-10}" width="78" height="20" fill="{badge_bg}" rx="10"/>')
        svg.append(f'<text x="459" y="{y+4}" text-anchor="middle" fill="{badge_fg}" font-size="10" font-weight="700" font-family="Be Vietnam Pro">{danh_gia}</text>')

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
    
    svg = []
    svg.append(f'<svg class="chart_svg" viewBox="0 0 {W} {H}" width="100%" height="auto" xmlns="http://www.w3.org/2000/svg">')
    svg.append('<circle cx="150" cy="22" r="5" fill="#94a3b8"/>')
    svg.append('<text x="162" y="26" fill="#6c7280" font-size="12" font-family="Be Vietnam Pro">7T/2025</text>')
    svg.append('<circle cx="240" cy="22" r="5" fill="#3b56e0"/>')
    svg.append('<text x="252" y="26" fill="#14161c" font-size="12" font-weight="700" font-family="Be Vietnam Pro">7T/2026</text>')

    for i, r in enumerate(rows):
        y = top_offset + i * row_h
        is_total = (r["name"] == "Toàn Znews")
        bg_col = "#eef2ff" if is_total else ("#f8fafc" if i % 2 == 1 else "#ffffff")
        stroke_col = "#c7d2fe" if is_total else "#e9ebf1"
        svg.append(f'<rect x="10" y="{y-18}" width="{W-20}" height="{row_h-8}" fill="{bg_col}" stroke="{stroke_col}" stroke-width="1" rx="10"/>')
        
        font_weight = "800" if is_total else "700"
        text_color = "#3b56e0" if is_total else "#14161c"
        svg.append(f'<text x="24" y="{y+6}" fill="{text_color}" font-size="14" font-weight="{font_weight}" font-family="Be Vietnam Pro">{r["name"]}</text>')
        
        if is_total:
            x_min, x_max = 400000.0, 500000.0
        else:
            x_min, x_max = 50000.0, 200000.0
            
        def get_db_x(val):
            clamp_val = max(x_min, min(x_max, val))
            return 175.0 + ((clamp_val - x_min) / (x_max - x_min)) * 230.0

        x25 = get_db_x(r["t7_25"])
        x26 = get_db_x(r["t7_26"])
        bar_col = "#16a34a" if r["pct"] > 0 else "#f87171"
        svg.append(f'<line x1="{x25:.1f}" y1="{y+6}" x2="{x26:.1f}" y2="{y+6}" stroke="{bar_col}" stroke-width="4" stroke-linecap="round"/>')
        svg.append(f'<circle cx="{x25:.1f}" cy="{y+6}" r="6.5" fill="#94a3b8" stroke="#ffffff" stroke-width="1.5"/>')
        svg.append(f'<circle cx="{x26:.1f}" cy="{y+6}" r="7.5" fill="#3b56e0" stroke="#ffffff" stroke-width="2"/>')
        
        svg.append(f'<text x="{x25:.1f}" y="{y+26}" text-anchor="middle" fill="#64748b" font-size="11" font-weight="600" font-family="Manrope">{fmt_tr(r["t7_25"], 1)} tr</text>')
        svg.append(f'<text x="{x26:.1f}" y="{y-6}" text-anchor="middle" fill="#3b56e0" font-size="12" font-weight="800" font-family="Manrope">{fmt_tr(r["t7_26"], 1)} tr</text>')

        badge_bg = "#ecfdf5" if r["pct"] > 0 else "#fef2f2"
        badge_fg = "#16a34a" if r["pct"] > 0 else "#c2410c"
        svg.append(f'<rect x="425" y="{y-7}" width="65" height="24" fill="{badge_bg}" rx="12"/>')
        svg.append(f'<text x="457" y="{y+9}" text-anchor="middle" fill="{badge_fg}" font-size="12" font-weight="800" font-family="Manrope">{fmt_pct(r["pct"])}</text>')

    svg.append('</svg>')
    return "\n".join(svg)


# =========================================================================
# SECTION 03: MỨC ĐỘ SỤT GIẢM T8-T9/2026 (FIXED: NO TEXT OVERLAP)
# =========================================================================
def build_drop_t8t9_svg():
    # Sort from deepest drop to least drop
    sorted_by_drop = sorted(all_deps, key=lambda d: growth_dict[d]["pct_T8T9_2026_vs_cung_ky"])
    
    W, H = 960, 520
    top_offset = 55
    row_h = 31
    x_zero = 240
    scale = 7.5  # 1% = 7.5px -> 80% = 600px -> x = 840
    
    svg = []
    svg.append(f'<svg class="chart_svg" viewBox="0 0 {W} {H}" width="100%" height="auto" xmlns="http://www.w3.org/2000/svg">')
    
    # Axis line at 0%
    svg.append(f'<line x1="{x_zero}" y1="{top_offset-20}" x2="{x_zero}" y2="{top_offset + 14 * row_h}" stroke="#14161c" stroke-width="1.5"/>')
    svg.append(f'<text x="{x_zero}" y="{top_offset-28}" text-anchor="middle" fill="#14161c" font-size="12" font-weight="700" font-family="Manrope">0%</text>')

    # Reference grid at -20%, -40%, -60%, -80%
    for ref_pct in [-20, -40, -60, -80]:
        rx = x_zero + abs(ref_pct) * scale
        svg.append(f'<line x1="{rx:.1f}" y1="{top_offset-15}" x2="{rx:.1f}" y2="{top_offset + 14 * row_h}" stroke="#e2e8f0" stroke-width="1" stroke-dasharray="3,3"/>')
        svg.append(f'<text x="{rx:.1f}" y="{top_offset-28}" text-anchor="middle" fill="#94a3b8" font-size="11" font-weight="600" font-family="Manrope">{ref_pct}%</text>')

    # Benchmark Line: Toàn Znews (-58,1%)
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
        
        # Alternating background
        if i % 2 == 1:
            svg.append(f'<rect x="10" y="{y-14}" width="{W-20}" height="{row_h}" fill="#f8fafc" rx="4"/>')
            
        # Department name: clean column on the left (x=20)
        svg.append(f'<text x="20" y="{y+4}" fill="#14161c" font-size="13" font-weight="700" font-family="Be Vietnam Pro">{name}</text>')
        
        # Block pill badge: placed between x=135 and x=220
        svg.append(f'<rect x="135" y="{y-9}" width="85" height="19" fill="#eef2f6" rx="5"/>')
        svg.append(f'<text x="177" y="{y+4}" text-anchor="middle" fill="#64748b" font-size="11" font-weight="600" font-family="Be Vietnam Pro">{blk_short}</text>')
        
        # Bar extends from x_zero (240) to the right
        bar_len = abs(pct) * scale
        fill_col = "#fb923c" if pct > -45 else ("#ea580c" if pct > -60 else "#c2410c")
        svg.append(f'<rect x="{x_zero}" y="{y-8}" width="{bar_len:.1f}" height="16" fill="{fill_col}" rx="3"/>')
        
        # Value label placed cleanly to the right of the bar (x >= 270)
        val_x = x_zero + bar_len + 8
        svg.append(f'<text x="{val_x:.1f}" y="{y+4}" text-anchor="start" fill="{fill_col}" font-size="12" font-weight="800" font-family="Manrope">{fmt_pct(pct)}</text>')

    svg.append('</svg>')
    return "\n".join(svg)


def build_kpi_comparison_svg():
    W, H = 960, 440
    PW = 860
    L, T = 60, 40
    row_h = 26
    max_k = 10500.0
    scale = (PW - 160) / max_k
    
    svg = []
    svg.append(f'<svg class="chart_svg" viewBox="0 0 {W} {H}" width="100%" height="auto" xmlns="http://www.w3.org/2000/svg">')
    svg.append('<rect x="180" y="12" width="14" height="10" fill="#c9d0f6" rx="2"/>')
    svg.append('<text x="200" y="21" fill="#6c7280" font-size="12" font-family="Be Vietnam Pro">TB T8–T9 thực tế</text>')
    svg.append('<rect x="330" y="12" width="14" height="10" fill="#6072dd" rx="2"/>')
    svg.append('<text x="350" y="21" fill="#14161c" font-size="12" font-weight="600" font-family="Be Vietnam Pro">KPI Tháng Mức +10%</text>')
    svg.append('<rect x="500" y="12" width="14" height="10" fill="#3b56e0" rx="2"/>')
    svg.append('<text x="520" y="21" fill="#14161c" font-size="12" font-weight="700" font-family="Be Vietnam Pro">KPI Tháng Mức +15%</text>')

    for i, name in enumerate(all_deps):
        y = T + 20 + i * row_h
        item = kpi_dict[name]
        tb = item["tb_thang_T8T9_2026"]
        m10 = item["muc_10"]["kpi_moi_thang"]
        m15 = item["muc_15"]["kpi_moi_thang"]
        
        if i % 2 == 1:
            svg.append(f'<rect x="10" y="{y-12}" width="{W-20}" height="{row_h}" fill="#f8f9fe" rx="4"/>')
            
        svg.append(f'<text x="20" y="{y+5}" fill="#14161c" font-size="13" font-weight="600" font-family="Be Vietnam Pro">{name}</text>')
        
        bx = 140
        w_tb = tb * scale
        w_m10 = m10 * scale
        w_m15 = m15 * scale
        bar_h = 5.5
        svg.append(f'<rect x="{bx}" y="{y-8}" width="{w_tb:.1f}" height="{bar_h}" fill="#c9d0f6" rx="2"/>')
        svg.append(f'<rect x="{bx}" y="{y-1}" width="{w_m10:.1f}" height="{bar_h}" fill="#6072dd" rx="2"/>')
        svg.append(f'<rect x="{bx}" y="{y+6}" width="{w_m15:.1f}" height="{bar_h}" fill="#3b56e0" rx="2"/>')
        
        val_txt = f"{fmt_tr(tb, 2)} → {fmt_tr(m10, 2)}–{fmt_tr(m15, 2)} tr"
        svg.append(f'<text x="{bx + w_m15 + 12:.1f}" y="{y+5}" fill="#14161c" font-size="11" font-weight="700" font-family="Manrope">{val_txt}</text>')

    svg.append('</svg>')
    return "\n".join(svg)


def build_year_dumbbell_svg():
    W, H = 510, 480
    top_offset = 60
    row_h = 75
    
    rows = [
        {"name": "Khối Truy cập", "y25": 309966, "y26_10": 240922, "pct_10": -22.3},
        {"name": "Khối Lifestyle", "y25": 199598, "y26_10": 131723, "pct_10": -34.0},
        {"name": "Khối Uy tín", "y25": 182651, "y26_10": 122370, "pct_10": -33.0},
        {"name": "Khối Kinh doanh", "y25": 126553, "y26_10": 94778, "pct_10": -25.1},
        {"name": "Toàn Znews", "y25": 818767, "y26_10": 589793, "pct_10": -28.0}
    ]
    
    svg = []
    svg.append(f'<svg class="chart_svg" viewBox="0 0 {W} {H}" width="100%" height="auto" xmlns="http://www.w3.org/2000/svg">')
    svg.append('<circle cx="150" cy="22" r="5" fill="#94a3b8"/>')
    svg.append('<text x="162" y="26" fill="#6c7280" font-size="12" font-family="Be Vietnam Pro">Cả năm 2025</text>')
    svg.append('<circle cx="260" cy="22" r="5" fill="#3b56e0"/>')
    svg.append('<text x="272" y="26" fill="#14161c" font-size="12" font-weight="700" font-family="Be Vietnam Pro">Cả năm 2026 (PA C)</text>')

    for i, r in enumerate(rows):
        y = top_offset + i * row_h
        is_total = (r["name"] == "Toàn Znews")
        bg_col = "#eef2ff" if is_total else ("#f8fafc" if i % 2 == 1 else "#ffffff")
        stroke_col = "#c7d2fe" if is_total else "#e9ebf1"
        svg.append(f'<rect x="10" y="{y-18}" width="{W-20}" height="{row_h-8}" fill="{bg_col}" stroke="{stroke_col}" stroke-width="1" rx="10"/>')
        
        font_weight = "800" if is_total else "700"
        text_color = "#3b56e0" if is_total else "#14161c"
        svg.append(f'<text x="24" y="{y+6}" fill="{text_color}" font-size="14" font-weight="{font_weight}" font-family="Be Vietnam Pro">{r["name"]}</text>')
        
        if is_total:
            x_min, x_max = 500000.0, 850000.0
        else:
            x_min, x_max = 80000.0, 320000.0
            
        def get_db_x(val):
            clamp_val = max(x_min, min(x_max, val))
            return 175.0 + ((clamp_val - x_min) / (x_max - x_min)) * 230.0

        x25 = get_db_x(r["y25"])
        x26_10 = get_db_x(r["y26_10"])
        svg.append(f'<line x1="{x25:.1f}" y1="{y+6}" x2="{x26_10:.1f}" y2="{y+6}" stroke="#f87171" stroke-width="4" stroke-linecap="round"/>')
        svg.append(f'<circle cx="{x25:.1f}" cy="{y+6}" r="6.5" fill="#94a3b8" stroke="#ffffff" stroke-width="1.5"/>')
        svg.append(f'<circle cx="{x26_10:.1f}" cy="{y+6}" r="7.5" fill="#3b56e0" stroke="#ffffff" stroke-width="2"/>')
        
        svg.append(f'<text x="{x25:.1f}" y="{y+26}" text-anchor="middle" fill="#64748b" font-size="11" font-weight="600" font-family="Manrope">{fmt_tr(r["y25"], 1)} tr</text>')
        svg.append(f'<text x="{x26_10:.1f}" y="{y-6}" text-anchor="middle" fill="#3b56e0" font-size="12" font-weight="800" font-family="Manrope">{fmt_tr(r["y26_10"], 1)} tr</text>')

        pct_lbl = f"{fmt_pct(r['pct_10'])}"
        svg.append(f'<rect x="425" y="{y-7}" width="65" height="24" fill="#fef2f2" rx="12"/>')
        svg.append(f'<text x="457" y="{y+9}" text-anchor="middle" fill="#c2410c" font-size="12" font-weight="800" font-family="Manrope">{pct_lbl}</text>')

    svg.append('</svg>')
    return "\n".join(svg)


def build_year_growth_bar_svg():
    sorted_deps_yr = sorted(all_deps, key=lambda d: kpi_dict[d]["muc_10"]["pct_ca_nam_vs_2025"], reverse=True)
    W, H = 510, 520
    row_h = 32
    top_offset = 45
    x_zero = 190
    scale = 2.6
    
    svg = []
    svg.append(f'<svg class="chart_svg" viewBox="0 0 {W} {H}" width="100%" height="auto" xmlns="http://www.w3.org/2000/svg">')
    svg.append(f'<line x1="{x_zero}" y1="{top_offset-15}" x2="{x_zero}" y2="{top_offset + 14 * row_h}" stroke="#14161c" stroke-width="1.5"/>')
    svg.append(f'<text x="{x_zero}" y="{top_offset-22}" text-anchor="middle" fill="#6c7280" font-size="11" font-weight="700" font-family="Manrope">0%</text>')

    for i, name in enumerate(sorted_deps_yr):
        y = top_offset + i * row_h
        item = kpi_dict[name]
        pct = item["muc_10"]["pct_ca_nam_vs_2025"]
        is_the_gioi = (name == "Thế giới")
        is_xuat_ban = (name == "Xuất bản")
        
        row_bg = "#ecfdf5" if is_the_gioi else ("#fefce8" if is_xuat_ban else ("#fbfcfe" if i % 2 == 1 else "#ffffff"))
        svg.append(f'<rect x="10" y="{y-14}" width="{W-20}" height="{row_h}" fill="{row_bg}" rx="4"/>')
        
        bar_len = abs(pct) * scale
        if pct >= 0:
            fill_col = "#16a34a"
            bx = x_zero
            val_x = x_zero + bar_len + 6
            val_anchor = "start"
            val_col = "#16a34a"
        else:
            fill_col = "#ca8a04" if is_xuat_ban else "#c2410c"
            bx = x_zero - bar_len
            val_x = x_zero - bar_len - 6
            val_anchor = "end"
            val_col = fill_col

        weight = "800" if (is_the_gioi or is_xuat_ban) else "500"
        svg.append(f'<text x="15" y="{y+4}" fill="#14161c" font-size="13" font-weight="{weight}" font-family="Be Vietnam Pro">{name}</text>')
        svg.append(f'<rect x="{bx:.1f}" y="{y-8}" width="{bar_len:.1f}" height="16" fill="{fill_col}" rx="3"/>')
        svg.append(f'<text x="{val_x:.1f}" y="{y+4}" text-anchor="{val_anchor}" fill="{val_col}" font-size="12" font-weight="700" font-family="Manrope">{fmt_pct(pct)}</text>')
        
        if is_the_gioi:
            svg.append(f'<rect x="400" y="{y-10}" width="98" height="20" fill="#d1fae5" rx="10"/>')
            svg.append(f'<text x="449" y="{y+4}" text-anchor="middle" fill="#065f46" font-size="10" font-weight="800" font-family="Be Vietnam Pro">★ Duy nhất tăng</text>')
        elif is_xuat_ban:
            svg.append(f'<rect x="400" y="{y-10}" width="98" height="20" fill="#fef08a" rx="10"/>')
            svg.append(f'<text x="449" y="{y+4}" text-anchor="middle" fill="#854d0e" font-size="10" font-weight="700" font-family="Be Vietnam Pro">Gần đi ngang</text>')

    svg.append('</svg>')
    return "\n".join(svg)


# ==========================================
# ASSEMBLE FULL HTML WITH ZERO STYLE ATTRIBUTES
# ==========================================

css_scoped = """
@import url('https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:ital,wght@0,400;0,500;0,600;0,700;1,400&family=Manrope:wght@500;600;700;800&display=swap');

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

.container_AI p {
  color: #525866;
  font-size: 14.5px;
}

.container_AI .page_header {
  margin-bottom: 32px;
}

.container_AI .badge_bar {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 12px;
  flex-wrap: wrap;
}

.container_AI .meta_badge {
  background-color: #e0e7ff;
  color: #3730a3;
  font-size: 11px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  padding: 4px 12px;
  border-radius: 9999px;
  display: inline-block;
}

.container_AI .meta_subtext {
  font-size: 13px;
  color: #64748b;
  font-weight: 500;
}

.container_AI .page_desc {
  font-size: 16px;
  line-height: 1.6;
  color: #475569;
  margin-top: 10px;
  max-width: 900px;
}

.container_AI .card {
  background-color: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.03);
}

.container_AI .card_hero {
  background-color: #ffffff;
  border: 2px solid #3b56e0;
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 4px 14px rgba(59, 86, 224, 0.08);
  margin-bottom: 24px;
}

.container_AI .card_hero_inner {
  margin-top: 18px;
}

.container_AI .section_block {
  margin-bottom: 48px;
}

.container_AI .section_header {
  border-top: 2px solid #3b56e0;
  padding-top: 14px;
  margin-bottom: 20px;
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 12px;
}

.container_AI .section_title_wrap {
  display: flex;
  align-items: baseline;
  gap: 10px;
}

.container_AI .section_num {
  font-family: 'Manrope', sans-serif;
  font-weight: 800;
  font-size: 20px;
  color: #3b56e0;
}

.container_AI .section_title {
  font-size: 20px;
  font-weight: 700;
  color: #14161c;
}

.container_AI .section_sub {
  font-size: 13px;
  color: #64748b;
  margin-top: 4px;
}

.container_AI .grid_4col {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
  margin-bottom: 36px;
}

.container_AI .grid_2col {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}

.container_AI .grid_3col {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
}

.container_AI .kpi_card_head {
  background-color: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 14px;
  padding: 18px 20px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.container_AI .kpi_card_head.highlight {
  border-color: #3b56e0;
  background-color: #f7f8fe;
}

.container_AI .kpi_label {
  font-size: 12px;
  font-weight: 600;
  color: #64748b;
  text-transform: uppercase;
  letter-spacing: 0.04em;
  margin-bottom: 8px;
}

.container_AI .kpi_value_huge {
  font-family: 'Manrope', sans-serif;
  font-size: 25px;
  font-weight: 800;
  line-height: 1.15;
  color: #14161c;
}

.container_AI .kpi_value_huge.accent {
  color: #3b56e0;
}

.container_AI .kpi_value_huge.negative {
  color: #c2410c;
}

.container_AI .kpi_sub {
  font-size: 12px;
  color: #64748b;
  margin-top: 8px;
  font-weight: 500;
}

.container_AI .controls_bar {
  display: flex;
  gap: 8px;
  align-items: center;
  flex-wrap: wrap;
  margin-bottom: 18px;
}

.container_AI .chip {
  padding: 7px 14px;
  border-radius: 8px;
  background-color: #ffffff;
  border: 1px solid #cbd5e1;
  color: #475569;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  user-select: none;
  transition: all 0.15s ease;
  display: inline-block;
  text-decoration: none;
}

.container_AI .chip:hover {
  background-color: #f1f5f9;
  border-color: #94a3b8;
  color: #1e293b;
}

.container_AI .chip.active {
  background-color: #3b56e0;
  border-color: #3b56e0;
  color: #ffffff;
  font-weight: 700;
}

.container_AI .chip_sm {
  padding: 5px 10px;
  font-size: 12px;
  border-radius: 6px;
}

/* Department Showcase Cards */
.container_AI .dep_kpi_card {
  background-color: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 14px;
  padding: 20px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.02);
  transition: transform 0.15s ease, box-shadow 0.15s ease;
}

.container_AI .dep_kpi_card:hover {
  border-color: #94a3b8;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.container_AI .dep_card_header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 12px;
  padding-bottom: 12px;
  border-bottom: 1px solid #f1f5f9;
}

.container_AI .dep_name {
  font-size: 17px;
  font-weight: 800;
  color: #14161c;
}

.container_AI .dep_block_tag {
  font-size: 11px;
  font-weight: 700;
  padding: 3px 8px;
  border-radius: 6px;
  background-color: #f1f5f9;
  color: #475569;
}

.container_AI .dep_baseline {
  background-color: #f8fafc;
  border-radius: 8px;
  padding: 8px 12px;
  margin-bottom: 12px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 12.5px;
}

.container_AI .dep_kpi_box_highlight {
  background-color: #f0f3fe;
  border: 1.5px solid #c7d2fe;
  border-radius: 10px;
  padding: 12px 14px;
  margin-bottom: 10px;
  transition: background-color 0.2s ease, border-color 0.2s ease;
}

.container_AI .dep_kpi_box_highlight.q4_box {
  background-color: #ffffff;
  border: 1.5px solid #3b56e0;
}

.container_AI .kpi_box_title {
  font-size: 11px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.04em;
  color: #3b56e0;
  margin-bottom: 6px;
}

.container_AI .kpi_target_row {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  margin-bottom: 4px;
  padding: 3px 6px;
  border-radius: 4px;
}

.container_AI .kpi_target_row.tier_focus {
  background-color: #e0e7ff;
}

.container_AI .target_tier {
  font-size: 12px;
  font-weight: 600;
  color: #475569;
}

.container_AI .target_number {
  font-family: 'Manrope', sans-serif;
  font-size: 16px;
  font-weight: 800;
  color: #14161c;
}

.container_AI .target_number.primary {
  color: #3b56e0;
  font-size: 17px;
}

.container_AI .target_number.q4_val {
  color: #1e1b4b;
  font-size: 17px;
}

.container_AI .dep_card_footer {
  font-size: 12px;
  color: #64748b;
  border-top: 1px solid #f1f5f9;
  padding-top: 10px;
  display: flex;
  justify-content: space-between;
}

/* Master Data Table */
.container_AI .table_responsive {
  width: 100%;
  overflow-x: auto;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  background-color: #ffffff;
  margin-top: 14px;
  margin-bottom: 24px;
}

.container_AI .kpi_table {
  width: 100%;
  border-collapse: collapse;
  text-align: left;
  font-size: 13.5px;
}

.container_AI .kpi_table th {
  background-color: #f8fafc;
  color: #475569;
  font-weight: 700;
  padding: 12px 14px;
  border-bottom: 2px solid #e2e8f0;
  white-space: nowrap;
}

.container_AI .kpi_table td {
  padding: 11px 14px;
  border-bottom: 1px solid #f1f5f9;
  color: #1e293b;
  white-space: nowrap;
}

.container_AI .kpi_table tr.row_block {
  background-color: #f7f8fe;
  font-weight: 700;
}

.container_AI .kpi_table tr.row_block td {
  color: #1e293b;
  border-bottom: 1px solid #e2e8f0;
  border-top: 1px solid #e2e8f0;
}

.container_AI .kpi_table tr.row_total {
  background-color: #3b56e0;
  color: #ffffff;
  font-weight: 800;
  font-size: 14px;
}

.container_AI .kpi_table tr.row_total td {
  color: #ffffff;
  border-bottom: none;
}

.container_AI .cell_num {
  text-align: right;
  font-family: 'Manrope', sans-serif;
  font-feature-settings: 'tnum' 1;
}

.container_AI .cell_bold {
  font-weight: 700;
}

.container_AI .cell_primary {
  color: #3b56e0;
  font-weight: 700;
}

.container_AI .cell_neg {
  color: #c2410c;
  font-weight: 600;
}

.container_AI .cell_pos {
  color: #16a34a;
  font-weight: 600;
}

.container_AI .table_col_highlight {
  background-color: #f0f3fe;
}

/* Strategic Insights Box (Section 06) */
.container_AI .insights_box {
  background-color: #f7f8fe;
  border: 1px solid #e0e7ff;
  border-radius: 16px;
  padding: 28px;
}

.container_AI .insight_item {
  margin-bottom: 18px;
  padding-bottom: 18px;
  border-bottom: 1px solid #eef2ff;
  display: flex;
  gap: 14px;
  align-items: flex-start;
}

.container_AI .insight_item:last-child {
  margin-bottom: 0;
  padding-bottom: 0;
  border-bottom: none;
}

.container_AI .insight_num {
  width: 26px;
  height: 26px;
  background-color: #3b56e0;
  color: #ffffff;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: 'Manrope', sans-serif;
  font-size: 12px;
  font-weight: 800;
  flex-shrink: 0;
  margin-top: 2px;
}

.container_AI .insight_text {
  font-size: 14.5px;
  line-height: 1.6;
  color: #334155;
}

.container_AI .insight_text strong {
  color: #0f172a;
}

.container_AI .page_footer {
  margin-top: 56px;
  padding-top: 24px;
  border-top: 1px solid #e2e8f0;
  display: flex;
  justify-content: space-between;
  align-items: center;
  color: #64748b;
  font-size: 13px;
  flex-wrap: wrap;
  gap: 12px;
}

.container_AI .chart_svg {
  display: block;
  overflow: visible;
}

.container_AI .card_spaced {
  margin-top: 24px;
}

.container_AI .hidden_element {
  display: none !important;
}

@media (max-width: 760px) {
  .container_AI {
    font-size: 17px;
  }
  .container_AI .wrap {
    padding: 20px 14px 60px 14px;
  }
  .container_AI h1 {
    font-size: 24px;
  }
  .container_AI .grid_4col, .container_AI .grid_2col, .container_AI .grid_3col {
    grid-template-columns: 1fr;
    gap: 14px;
  }
  .container_AI .kpi_value_huge {
    font-size: 22px;
  }
  .container_AI .card {
    padding: 16px;
  }
}
"""

html = []
html.append('<!DOCTYPE html>')
html.append('<html lang="vi">')
html.append('<head>')
html.append('  <meta charset="UTF-8">')
html.append('  <meta name="viewport" content="width=device-width, initial-scale=1.0">')
html.append('  <title>Truy cập Znews 2025–2026 & Mục tiêu KPI Quý 4/2026 (Phương án C)</title>')
html.append(f'  <style>{css_scoped}</style>')
html.append('</head>')
html.append('<body>')
html.append('<article class="container_AI">')
html.append('  <div class="wrap">')

# HEADER
html.append('    <header class="page_header">')
html.append('      <div class="badge_bar">')
html.append('        <div class="meta_badge">Báo cáo dữ liệu Ban biên tập</div>')
html.append('        <div class="meta_subtext">Dữ liệu đến ngày 29/09/2026 • Đơn vị: Triệu lượt truy cập</div>')
html.append('      </div>')
html.append('      <h1>Truy cập Znews 2025–2026 & Mục tiêu KPI Quý 4/2026</h1>')
html.append('      <p class="page_desc">Đánh giá toàn cảnh tăng trưởng 7 tháng đầu năm, phân tích mức độ sụt giảm sâu sau biến động T8–T9/2026 và chi tiết mục tiêu KPI Quý 4/2026 theo <strong>Phương án C</strong> (mức khả thi duy nhất: tăng 10–15% so với mức trung bình tháng T8–T9).</p>')
html.append('    </header>')

# 4 HEADLINE KPI CARDS
html.append('    <section class="grid_4col">')
# Card 1: 7T Growth
html.append('      <div class="kpi_card_head">')
html.append('        <div class="kpi_label">7 Tháng Đầu 2026 vs Cùng Kỳ</div>')
html.append(f'        <div class="kpi_value_huge negative">{fmt_pct(toan_t7["pct_7t"])}</div>')
html.append(f'        <div class="kpi_sub">Đạt <strong class="num">{fmt_tr(toan_t7["t7_2026"], 2)} tr</strong> (vs {fmt_tr(toan_t7["t7_2025"], 2)} tr 2025)</div>')
html.append('      </div>')
# Card 2: T8-T9 Drop
html.append('      <div class="kpi_card_head">')
html.append('        <div class="kpi_label">Biến Động T8–T9/2026</div>')
html.append(f'        <div class="kpi_value_huge negative">{fmt_pct(toan_t7["pct_T8T9_2026_vs_cung_ky"])}</div>')
html.append(f'        <div class="kpi_sub">Trung bình đạt <strong class="num">{fmt_tr(toan_kpi["tb_thang_T8T9_2026"], 2)} tr</strong>/tháng</div>')
html.append('      </div>')
# Card 3: Q4 KPI Target (HIGHLIGHT)
html.append('      <div class="kpi_card_head highlight">')
html.append('        <div class="kpi_label">Mục Tiêu KPI Quý 4/2026 (PA C)</div>')
html.append(f'        <div class="kpi_value_huge accent">{fmt_tr(toan_kpi["muc_10"]["tong_q4"], 2)}–{fmt_tr(toan_kpi["muc_15"]["tong_q4"], 2)} tr</div>')
html.append(f'        <div class="kpi_sub">Mỗi tháng: <strong class="num cell_primary">{fmt_tr(toan_kpi["muc_10"]["kpi_moi_thang"], 2)}–{fmt_tr(toan_kpi["muc_15"]["kpi_moi_thang"], 2)} tr</strong> (+10%–+15%)</div>')
html.append('      </div>')
# Card 4: Full Year Forecast
html.append('      <div class="kpi_card_head">')
html.append('        <div class="kpi_label">Kịch Bản Cả Năm 2026 (PA C)</div>')
html.append(f'        <div class="kpi_value_huge">{fmt_tr(toan_kpi["muc_10"]["ca_nam_2026"], 2)}–{fmt_tr(toan_kpi["muc_15"]["ca_nam_2026"], 2)} tr</div>')
html.append(f'        <div class="kpi_sub">{fmt_pct(toan_kpi["muc_10"]["pct_ca_nam_vs_2025"])} – {fmt_pct(toan_kpi["muc_15"]["pct_ca_nam_vs_2025"])} vs 2025 ({fmt_tr(toan_kpi["ca_nam_2025"], 1)} tr)</div>')
html.append('      </div>')
html.append('    </section>')

# SECTION 01: MONTHLY TRENDS
html.append('    <section class="section_block">')
html.append('      <div class="section_header">')
html.append('        <div class="section_title_wrap">')
html.append('          <div class="section_num">01</div>')
html.append('          <div>')
html.append('            <div class="section_title">Diễn biến truy cập theo tháng (2025–2026)</div>')
html.append('            <div class="section_sub">Đường nét liền xanh: thực tế 2026; đường xám: 2025; đường nét đứt: dải mục tiêu KPI Quý 4 (Phương án C: +10% đến +15%)</div>')
html.append('          </div>')
html.append('        </div>')
html.append('      </div>')
html.append('      <div class="card">')
html.append('        <div class="controls_bar" id="monthly_chips">')
html.append('          <div class="chip active" data-entity="Toàn Znews">Toàn Znews</div>')
for blk in all_blocks:
    html.append(f'          <div class="chip" data-entity="{blk}">{blk}</div>')
html.append('        </div>')
html.append('        <div class="controls_bar" id="monthly_dep_chips">')
for dep in all_deps:
    html.append(f'          <div class="chip chip_sm" data-entity="{dep}">{dep}</div>')
html.append('        </div>')
html.append(build_monthly_chart_svg())
html.append('      </div>')
html.append('    </section>')

# SECTION 02: 7-MONTH GROWTH
html.append('    <section class="section_block">')
html.append('      <div class="section_header">')
html.append('        <div class="section_title_wrap">')
html.append('          <div class="section_num">02</div>')
html.append('          <div>')
html.append('            <div class="section_title">Tăng trưởng 7 tháng đầu năm (Giai đoạn trước biến động)</div>')
html.append('            <div class="section_sub">So sánh 7T/2026 vs 7T/2025: Toàn trang giảm 6,5%; chỉ 4/14 chuyên mục tăng trưởng dương; Khối Truy cập là khối duy nhất tăng</div>')
html.append('          </div>')
html.append('        </div>')
html.append('      </div>')
html.append('      <div class="grid_2col">')
html.append('        <div class="card">')
html.append('          <h3>Tăng trưởng 14 chuyên mục (7T/2026 vs 7T/2025)</h3>')
html.append('          <p>Xếp hạng theo % tăng/giảm cùng đánh giá mục tiêu</p>')
html.append(build_t7_growth_bar_svg())
html.append('        </div>')
html.append('        <div class="card">')
html.append('          <h3>Quy mô truy cập 4 Khối & Toàn trang (7T/2025 vs 7T/2026)</h3>')
html.append('          <p>Điểm xám: 7T/2025 | Điểm xanh: 7T/2026 (đơn vị: triệu lượt)</p>')
html.append(build_t7_dumbbell_svg())
html.append('        </div>')
html.append('      </div>')
html.append('    </section>')

# SECTION 03: T8-T9 DROP (UPGRADED LAYOUT: ZERO TEXT OVERLAP)
html.append('    <section class="section_block">')
html.append('      <div class="section_header">')
html.append('        <div class="section_title_wrap">')
html.append('          <div class="section_num">03</div>')
html.append('          <div>')
html.append('            <div class="section_title">Mức độ sụt giảm T8–T9/2026 sau biến động</div>')
html.append('            <div class="section_sub">So sánh T8–T9/2026 so với cùng kỳ 2025: Toàn trang sụt giảm 58,1%; 13/14 ban giảm trên 40%</div>')
html.append('          </div>')
html.append('        </div>')
html.append('      </div>')
html.append('      <div class="card">')
html.append(build_drop_t8t9_svg())
html.append('      </div>')
html.append('    </section>')

# SECTION 04: CORE EMPHASIS - KPI QUÝ 4/2026 TỪNG BAN & TỪNG THÁNG
html.append('    <section class="section_block">')
html.append('      <div class="section_header">')
html.append('        <div class="section_title_wrap">')
html.append('          <div class="section_num">04</div>')
html.append('          <div>')
html.append('            <div class="section_title">Mục tiêu KPI Quý 4/2026 từng Ban & từng Tháng (Phương án C)</div>')
html.append('            <div class="section_sub">Chi tiết mức KPI từng tháng (T10, T11, T12) và tổng Quý 4 cho từng ban biên tập (Mức +10% cơ sở và Mức +15% phấn đấu)</div>')
html.append('          </div>')
html.append('        </div>')
html.append('      </div>')

# Overview block cards (Toàn trang & 4 Khối)
html.append('      <div class="card_hero">')
html.append('        <h3>Tổng hợp chỉ tiêu KPI Quý 4/2026 theo Phương án C</h3>')
html.append('        <p>Cơ chế: KPI mỗi tháng T10–T12 = TB tháng T8–T9/2026 × (1 + 10% hoặc 15%). Tổng Q4 = KPI tháng × 3.</p>')
html.append('        <div class="grid_4col card_hero_inner">')
for blk in all_blocks:
    b_kpi = kpi_dict[blk]
    html.append('          <div class="kpi_card_head">')
    html.append(f'            <div class="kpi_label">{blk}</div>')
    html.append(f'            <div class="kpi_value_huge accent">{fmt_tr(b_kpi["muc_10"]["tong_q4"], 2)}–{fmt_tr(b_kpi["muc_15"]["tong_q4"], 2)} tr</div>')
    html.append(f'            <div class="kpi_sub">Mỗi tháng: <strong class="num cell_primary">{fmt_tr(b_kpi["muc_10"]["kpi_moi_thang"], 2)}–{fmt_tr(b_kpi["muc_15"]["kpi_moi_thang"], 2)} tr</strong></div>')
    html.append('          </div>')
html.append('        </div>')
html.append('      </div>')

# Master Table Card
html.append('      <div class="card">')
html.append('        <div class="dep_card_header">')
html.append('          <div>')
html.append('            <h3>Bảng phân bổ KPI Quý 4/2026 chi tiết 19 đơn vị</h3>')
html.append('            <p>Nhóm theo từng Khối và Toàn Znews (số liệu gốc: nghìn lượt truy cập)</p>')
html.append('          </div>')
html.append('          <div class="controls_bar" id="kpi_tier_chips">')
html.append('            <div class="chip active" data-tier="both">Xem cả 2 mức</div>')
html.append('            <div class="chip" data-tier="10">Mức +10% (Cơ sở)</div>')
html.append('            <div class="chip" data-tier="15">Mức +15% (Phấn đấu)</div>')
html.append('          </div>')
html.append('        </div>')

# Master 19-row Table
html.append('        <div class="table_responsive">')
html.append('          <table class="kpi_table">')
html.append('            <thead>')
html.append('              <tr>')
html.append('                <th>Đơn vị / Ban</th>')
html.append('                <th class="cell_num">TB T8–T9</th>')
html.append('                <th class="cell_num col_10">KPI Tháng (+10%)</th>')
html.append('                <th class="cell_num col_15">KPI Tháng (+15%)</th>')
html.append('                <th class="cell_num col_10">Tổng Q4 (+10%)</th>')
html.append('                <th class="cell_num col_15">Tổng Q4 (+15%)</th>')
html.append('                <th class="cell_num">% vs Q4/2025</th>')
html.append('                <th class="cell_num">Cả năm 2026</th>')
html.append('              </tr>')
html.append('            </thead>')
html.append('            <tbody>')

for blk in all_blocks:
    blk_item = kpi_dict[blk]
    html.append('              <tr class="row_block">')
    html.append(f'                <td><strong>{blk}</strong></td>')
    html.append(f'                <td class="cell_num">{fmt_tr(blk_item["tb_thang_T8T9_2026"], 2)} tr</td>')
    html.append(f'                <td class="cell_num cell_primary col_10">{fmt_tr(blk_item["muc_10"]["kpi_moi_thang"], 2)} tr</td>')
    html.append(f'                <td class="cell_num cell_primary col_15">{fmt_tr(blk_item["muc_15"]["kpi_moi_thang"], 2)} tr</td>')
    html.append(f'                <td class="cell_num cell_bold col_10">{fmt_tr(blk_item["muc_10"]["tong_q4"], 2)} tr</td>')
    html.append(f'                <td class="cell_num cell_bold col_15">{fmt_tr(blk_item["muc_15"]["tong_q4"], 2)} tr</td>')
    html.append(f'                <td class="cell_num cell_neg">{fmt_pct(blk_item["muc_10"]["pct_q4_vs_q4_2025"])}</td>')
    html.append(f'                <td class="cell_num">{fmt_tr(blk_item["muc_10"]["ca_nam_2026"], 1)} tr ({fmt_pct(blk_item["muc_10"]["pct_ca_nam_vs_2025"])})</td>')
    html.append('              </tr>')
    
    for dep in deps_by_block[blk]:
        d_item = kpi_dict[dep]
        html.append('              <tr>')
        html.append(f'                <td>&nbsp;&nbsp;↳ {dep}</td>')
        html.append(f'                <td class="cell_num">{fmt_tr(d_item["tb_thang_T8T9_2026"], 2)} tr</td>')
        html.append(f'                <td class="cell_num cell_primary col_10">{fmt_tr(d_item["muc_10"]["kpi_moi_thang"], 2)} tr</td>')
        html.append(f'                <td class="cell_num cell_primary col_15">{fmt_tr(d_item["muc_15"]["kpi_moi_thang"], 2)} tr</td>')
        html.append(f'                <td class="cell_num cell_bold col_10">{fmt_tr(d_item["muc_10"]["tong_q4"], 2)} tr</td>')
        html.append(f'                <td class="cell_num cell_bold col_15">{fmt_tr(d_item["muc_15"]["tong_q4"], 2)} tr</td>')
        q4_pct_class = "cell_pos" if d_item["muc_10"]["pct_q4_vs_q4_2025"] > 0 else "cell_neg"
        html.append(f'                <td class="cell_num {q4_pct_class}">{fmt_pct(d_item["muc_10"]["pct_q4_vs_q4_2025"])}</td>')
        yr_pct_class = "cell_pos" if d_item["muc_10"]["pct_ca_nam_vs_2025"] > 0 else "cell_neg"
        html.append(f'                <td class="cell_num">{fmt_tr(d_item["muc_10"]["ca_nam_2026"], 1)} tr (<strong class="{yr_pct_class}">{fmt_pct(d_item["muc_10"]["pct_ca_nam_vs_2025"])}</strong>)</td>')
        html.append('              </tr>')

html.append('              <tr class="row_total">')
html.append('                <td><strong>TOÀN ZNEWS</strong></td>')
html.append(f'                <td class="cell_num">{fmt_tr(toan_kpi["tb_thang_T8T9_2026"], 2)} tr</td>')
html.append(f'                <td class="cell_num col_10">{fmt_tr(toan_kpi["muc_10"]["kpi_moi_thang"], 2)} tr</td>')
html.append(f'                <td class="cell_num col_15">{fmt_tr(toan_kpi["muc_15"]["kpi_moi_thang"], 2)} tr</td>')
html.append(f'                <td class="cell_num col_10">{fmt_tr(toan_kpi["muc_10"]["tong_q4"], 2)} tr</td>')
html.append(f'                <td class="cell_num col_15">{fmt_tr(toan_kpi["muc_15"]["tong_q4"], 2)} tr</td>')
html.append(f'                <td class="cell_num">{fmt_pct(toan_kpi["muc_10"]["pct_q4_vs_q4_2025"])}</td>')
html.append(f'                <td class="cell_num">{fmt_tr(toan_kpi["muc_10"]["ca_nam_2026"], 1)} tr ({fmt_pct(toan_kpi["muc_10"]["pct_ca_nam_vs_2025"])})</td>')
html.append('              </tr>')

html.append('            </tbody>')
html.append('          </table>')
html.append('        </div>')

# Grouped bar chart comparing TB T8-T9 vs KPI month
html.append('        <h3>So sánh trực quan: TB tháng T8–T9 vs Mục tiêu KPI tháng</h3>')
html.append('        <p>Cột nhạt: TB T8–T9; Cột vừa: KPI Tháng +10%; Cột đậm: KPI Tháng +15%</p>')
html.append(build_kpi_comparison_svg())
html.append('      </div>')

# 14 DEPARTMENT SHOWCASE CARDS (USER SPECIAL EMPHASIS)
html.append('      <div class="card card_spaced">')
html.append('        <div class="dep_card_header">')
html.append('          <div>')
html.append('            <h3>Thẻ tra cứu KPI chi tiết từng Ban (14 Chuyên mục)</h3>')
html.append('            <p>Nhấp vào các khối bên dưới để lọc nhanh các ban tương ứng</p>')
html.append('          </div>')
html.append('        </div>')
html.append('        <div class="controls_bar" id="dep_filter_chips">')
html.append('          <div class="chip active" data-filter="all">Tất cả 14 Ban</div>')
for blk in all_blocks:
    html.append(f'          <div class="chip" data-filter="{blk}">{blk}</div>')
html.append('        </div>')

# Cards Grid
html.append('        <div class="grid_3col" id="dep_cards_grid">')
for dep in all_deps:
    d_item = kpi_dict[dep]
    blk = dep_block_map[dep]
    tb = d_item["tb_thang_T8T9_2026"]
    m10_th = d_item["muc_10"]["kpi_moi_thang"]
    m15_th = d_item["muc_15"]["kpi_moi_thang"]
    m10_q4 = d_item["muc_10"]["tong_q4"]
    m15_q4 = d_item["muc_15"]["tong_q4"]
    pct_q4_10 = d_item["muc_10"]["pct_q4_vs_q4_2025"]
    yr_26_10 = d_item["muc_10"]["ca_nam_2026"]
    pct_yr_10 = d_item["muc_10"]["pct_ca_nam_vs_2025"]
    
    html.append(f'          <div class="dep_kpi_card" data-block="{blk}">')
    html.append('            <div class="dep_card_header">')
    html.append('              <div>')
    html.append(f'                <div class="dep_name">{dep}</div>')
    html.append(f'                <div class="meta_subtext">{blk}</div>')
    html.append('              </div>')
    html.append(f'              <div class="dep_block_tag">{blk.replace("Khối ", "")}</div>')
    html.append('            </div>')
    
    html.append('            <div class="dep_baseline">')
    html.append('              <div>Thực tế TB T8–T9:</div>')
    html.append(f'              <div class="num cell_bold">{fmt_tr(tb, 2)} tr/tháng</div>')
    html.append('            </div>')
    
    # BOX 1: KPI MỖI THÁNG
    html.append('            <div class="dep_kpi_box_highlight">')
    html.append('              <div class="kpi_box_title">🎯 KPI MỖI THÁNG T10–T12</div>')
    html.append('              <div class="kpi_target_row row_tier_10">')
    html.append('                <div class="target_tier">Mức +10% (Cơ sở):</div>')
    html.append(f'                <div class="target_number primary">{fmt_tr(m10_th, 2)} tr</div>')
    html.append('              </div>')
    html.append('              <div class="kpi_target_row row_tier_15">')
    html.append('                <div class="target_tier">Mức +15% (Phấn đấu):</div>')
    html.append(f'                <div class="target_number primary">{fmt_tr(m15_th, 2)} tr</div>')
    html.append('              </div>')
    html.append('            </div>')

    # BOX 2: TỔNG KPI QUÝ 4
    html.append('            <div class="dep_kpi_box_highlight q4_box">')
    html.append('              <div class="kpi_box_title">🏆 TỔNG KPI CẢ QUÝ 4/2026</div>')
    html.append('              <div class="kpi_target_row row_tier_10">')
    html.append('                <div class="target_tier">Mức +10%:</div>')
    html.append(f'                <div class="target_number q4_val">{fmt_tr(m10_q4, 2)} tr</div>')
    html.append('              </div>')
    html.append('              <div class="kpi_target_row row_tier_15">')
    html.append('                <div class="target_tier">Mức +15%:</div>')
    html.append(f'                <div class="target_number q4_val">{fmt_tr(m15_q4, 2)} tr</div>')
    html.append('              </div>')
    html.append('            </div>')

    # FOOTER COMPARISON
    q4_color = "cell_pos" if pct_q4_10 > 0 else "cell_neg"
    yr_color = "cell_pos" if pct_yr_10 > 0 else "cell_neg"
    html.append('            <div class="dep_card_footer">')
    html.append(f'              <div>Vs Q4/2025: <strong class="{q4_color}">{fmt_pct(pct_q4_10)}</strong></div>')
    html.append(f'              <div>Cả năm: <strong class="num {yr_color}">{fmt_pct(pct_yr_10)}</strong></div>')
    html.append('            </div>')
    
    html.append('          </div>')

html.append('        </div>')
html.append('      </div>')
html.append('    </section>')

# SECTION 05: FULL YEAR FORECAST
html.append('    <section class="section_block">')
html.append('      <div class="section_header">')
html.append('        <div class="section_title_wrap">')
html.append('          <div class="section_num">05</div>')
html.append('          <div>')
html.append('            <div class="section_title">Kịch bản cả năm 2026 so với 2025 (Nếu hoàn thành PA C)</div>')
html.append('            <div class="section_sub">Nếu đạt Phương án C, cả năm 2026 đạt 589,79–594,04 triệu lượt (-28,0% đến -27,4% so với năm 2025)</div>')
html.append('          </div>')
html.append('        </div>')
html.append('      </div>')
html.append('      <div class="grid_2col">')
html.append('        <div class="card">')
html.append('          <h3>Quy mô cả năm 2025 vs 2026 dự kiến (4 Khối + Toàn trang)</h3>')
html.append('          <p>Điểm xám: Cả năm 2025 | Điểm xanh: Cả năm 2026 (triệu lượt)</p>')
html.append(build_year_dumbbell_svg())
html.append('        </div>')
html.append('        <div class="card">')
html.append('          <h3>Tăng trưởng cả năm 2026 vs 2025 theo 14 chuyên mục</h3>')
html.append('          <p>Thế giới là ban duy nhất tăng (+12,6%); Xuất bản gần đi ngang (-1,7%)</p>')
html.append(build_year_growth_bar_svg())
html.append('        </div>')
html.append('      </div>')
html.append('    </section>')

# SECTION 06: STRATEGIC INSIGHTS & METHODOLOGY
html.append('    <section class="section_block">')
html.append('      <div class="section_header">')
html.append('        <div class="section_title_wrap">')
html.append('          <div class="section_num">06</div>')
html.append('          <div>')
html.append('            <div class="section_title">Nhận định chuyên sâu & Phương pháp tính toán</div>')
html.append('            <div class="section_sub">Căn cứ thực tiễn và nguyên tắc phân bổ chỉ tiêu do Ban biên tập đề xuất</div>')
html.append('          </div>')
html.append('        </div>')
html.append('      </div>')
html.append('      <div class="insights_box">')

insights = [
    ("1", "<strong>7 tháng đầu năm 2026:</strong> Toàn trang giảm 6,5% so với cùng kỳ 2025. Chỉ 4/14 chuyên mục đạt tăng trưởng dương: <em>Thế giới</em> (+63,5%), <em>Thể thao</em> (+10,2%, hoàn thành mục tiêu), <em>Đời sống</em> (+8,5%) và <em>Du lịch</em> (+2,4%). Khối Truy cập là khối duy nhất duy trì tăng trưởng (+2,4%), trong khi Khối Uy tín giảm sâu nhất (-19,2%)."),
    ("2", "<strong>Biến động mạnh từ tháng 8/2026:</strong> Sang tháng 8 và tháng 9/2026, lượng truy cập toàn trang sụt giảm nghiêm trọng 58,1% so với cùng kỳ năm 2025. Mức trung bình tháng của toàn trang chỉ còn 28,28 triệu lượt (so với mức 65–75 triệu lượt/tháng của giai đoạn trước)."),
    ("3", "<strong>Bản chất Phương án C (Khả thi duy nhất):</strong> Mục tiêu KPI mỗi tháng T10, T11, T12 được tính toán bằng mức trung bình thực tế tháng T8–T9 nhân với hệ số tăng trưởng 10% (mức cơ sở) hoặc 15% (mức phấn đấu), chia đều cho 3 tháng. Toàn trang hướng đến mức <strong>31,11 – 32,52 triệu lượt/tháng</strong>, tương ứng tổng Quý 4 đạt <strong>93,33 – 97,57 triệu lượt</strong>."),
    ("4", "<strong>Kịch bản cả năm 2026:</strong> Nếu hoàn thành Phương án C, cả năm 2026 Znews sẽ đạt 589,79 – 594,04 triệu lượt, giảm 27,4% – 28,0% so với năm 2025 (818,77 triệu). Theo khối: Truy cập giảm khoảng -22%, Kinh doanh giảm -25%, Uy tín giảm -33%, Lifestyle giảm -34%. Chuyên mục <em>Thế giới</em> là điểm sáng duy nhất duy trì tăng trưởng dương cả năm (+12,6% – +12,9%), trong khi Lifestyle giảm sâu nhất (-66%, một phần do lượng truy cập đột biến kỷ lục tháng 12/2025)."),
    ("5", "<strong>Độ nhạy của kịch bản mục tiêu:</strong> Việc nâng mục tiêu Quý 4 từ mức +10% lên +15% chỉ cải thiện kết quả cả năm khoảng 0,6 điểm phần trăm (từ -28,0% lên -27,4%), do quy mô nền truy cập hiện tại đã xuống mức thấp."),
    ("6", "<strong>Loại trừ Phương án A và B:</strong> Các phương án A và B (đặt mục tiêu bù đủ kế hoạch ban đầu của cả năm) đòi hỏi lượng truy cập Quý 4 phải tăng trưởng trên 100% so với giai đoạn T8–T9. Đây là kịch bản hoàn toàn phi thực tế và bất khả thi trong điều kiện biến động hiện nay."),
    ("7", "<strong>Ghi chú phạm vi dữ liệu:</strong> Dữ liệu tháng 9/2026 được chốt đến hết ngày 29/09/2026. Chuyên mục <em>Xuất bản</em> bao gồm Sách hay và Văn hóa đọc; <em>Du lịch</em> bao gồm Ẩm thực; <em>Giải trí</em> bao gồm Phim ảnh, Âm nhạc và Thời trang Sao. Số liệu các khối và toàn trang được tổng hợp chuẩn xác từ các chuyên mục thành phần.")
]

for num, text in insights:
    html.append('        <div class="insight_item">')
    html.append(f'          <div class="insight_num">{num}</div>')
    html.append(f'          <div class="insight_text">{text}</div>')
    html.append('        </div>')

html.append('      </div>')
html.append('    </section>')

# FOOTER
html.append('    <footer class="page_footer">')
html.append('      <div>Nguồn dữ liệu: <strong>Tong hop truy cap 2025-2026.xlsx</strong> (Cập nhật 29/09/2026)</div>')
html.append('      <div>Bản quyền Báo điện tử Tri thức (Znews) • Lưu hành nội bộ</div>')
html.append('    </footer>')

html.append('  </div>') # wrap
html.append('</article>') # container_AI

# EMBEDDED JAVASCRIPT FOR INTERACTIVITY (NO INLINE STYLE ATTRIBUTES)
client_data_json = json.dumps({
    "monthly": monthly_series,
    "kpi": {k: {"tb": v["tb_thang_T8T9_2026"], "m10": v["muc_10"]["kpi_moi_thang"], "m15": v["muc_15"]["kpi_moi_thang"]} for k, v in kpi_dict.items()}
}, ensure_ascii=False)

js_script = f"""
(function() {{
  const rawData = {client_data_json};
  const W = 960, H = 430, L = 65, R = 45, T = 45, B = 60;
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

    let maxVal = Math.max(...s.vals_2025, ...s.vals_2026, kpi.m10, kpi.m15);
    maxVal = Math.ceil((maxVal * 1.15) / 1000) * 1000;
    if (maxVal < 1000) maxVal = 1000;

    function getY(v) {{
      return T + PH - (v / maxVal) * PH;
    }}

    const yLabels = document.querySelectorAll('.axis_label_y');
    const yLines = document.querySelectorAll('.grid_line');
    const steps = [0, 0.25, 0.5, 0.75, 1.0];
    steps.forEach((st, idx) => {{
      const val = maxVal * st;
      const y = getY(val);
      if (yLines[idx]) {{
        yLines[idx].setAttribute('y1', y);
        yLines[idx].setAttribute('y2', y);
      }}
      if (yLabels[idx]) {{
        yLabels[idx].setAttribute('y', y + 4);
        yLabels[idx].textContent = (val / 1000).toLocaleString('vi-VN', {{ maximumFractionDigits: 1 }}) + ' tr';
      }}
    }});

    const pts25 = s.vals_2025.map((v, i) => `${{xs[i].toFixed(1)}},${{getY(v).toFixed(1)}}`).join(' L ');
    const p25 = document.getElementById('path_2025');
    if (p25) p25.setAttribute('d', 'M ' + pts25);

    const dots25 = document.querySelectorAll('.dot_2025');
    s.vals_2025.forEach((v, i) => {{
      if (dots25[i]) dots25[i].setAttribute('cy', getY(v).toFixed(1));
    }});

    const pts26 = s.vals_2026.map((v, i) => `${{xs[i].toFixed(1)}},${{getY(v).toFixed(1)}}`).join(' L ');
    const p26 = document.getElementById('path_2026');
    if (p26) p26.setAttribute('d', 'M ' + pts26);

    const dots26 = document.querySelectorAll('.dot_2026');
    s.vals_2026.forEach((v, i) => {{
      if (dots26[i]) dots26[i].setAttribute('cy', getY(v).toFixed(1));
    }});

    const yT9 = getY(s.vals_2026[8]);
    const yM10 = getY(kpi.m10);
    const yM15 = getY(kpi.m15);

    const poly = document.getElementById('poly_target');
    if (poly) {{
      const ptsPoly = `${{xs[8].toFixed(1)}},${{yT9.toFixed(1)}} ${{xs[9].toFixed(1)}},${{yM15.toFixed(1)}} ${{xs[10].toFixed(1)}},${{yM15.toFixed(1)}} ${{xs[11].toFixed(1)}},${{yM15.toFixed(1)}} ${{xs[11].toFixed(1)}},${{yM10.toFixed(1)}} ${{xs[10].toFixed(1)}},${{yM10.toFixed(1)}} ${{xs[9].toFixed(1)}},${{yM10.toFixed(1)}} ${{xs[8].toFixed(1)}},${{yT9.toFixed(1)}}`;
      poly.setAttribute('points', ptsPoly);
    }}

    const pM10 = document.getElementById('path_target_m10');
    if (pM10) {{
      const d10 = `M ${{xs[8].toFixed(1)}},${{yT9.toFixed(1)}} L ${{xs[9].toFixed(1)}},${{yM10.toFixed(1)}} L ${{xs[10].toFixed(1)}},${{yM10.toFixed(1)}} L ${{xs[11].toFixed(1)}},${{yM10.toFixed(1)}}`;
      pM10.setAttribute('d', d10);
    }}

    const pM15 = document.getElementById('path_target_m15');
    if (pM15) {{
      const d15 = `M ${{xs[8].toFixed(1)}},${{yT9.toFixed(1)}} L ${{xs[9].toFixed(1)}},${{yM15.toFixed(1)}} L ${{xs[10].toFixed(1)}},${{yM15.toFixed(1)}} L ${{xs[11].toFixed(1)}},${{yM15.toFixed(1)}}`;
      pM15.setAttribute('d', d15);
    }}

    const dotsM10 = document.querySelectorAll('.dot_target_10');
    dotsM10.forEach(d => d.setAttribute('cy', yM10.toFixed(1)));

    const dotsM15 = document.querySelectorAll('.dot_target_15');
    dotsM15.forEach(d => d.setAttribute('cy', yM15.toFixed(1)));

    const lblT1 = document.getElementById('lbl_t1');
    if (lblT1) {{
      lblT1.setAttribute('y', (getY(s.vals_2026[0]) - 12).toFixed(1));
      lblT1.textContent = fmtTr(s.vals_2026[0]);
    }}

    const lblT8 = document.getElementById('lbl_t8');
    if (lblT8) {{
      lblT8.setAttribute('y', (getY(s.vals_2026[7]) - 12).toFixed(1));
      lblT8.textContent = fmtTr(s.vals_2026[7]);
    }}

    const lblT9 = document.getElementById('lbl_t9');
    if (lblT9) {{
      lblT9.setAttribute('y', (yT9 + 18).toFixed(1));
      lblT9.textContent = fmtTr(s.vals_2026[8]);
    }}

    const lblTarget = document.getElementById('lbl_target');
    if (lblTarget) {{
      lblTarget.setAttribute('y', (yM15 - 12).toFixed(1));
      lblTarget.textContent = `Mục tiêu Q4: ${{fmtTr(kpi.m10)}}–${{fmtTr(kpi.m15)}}/tháng`;
    }}
  }}

  const allChips = document.querySelectorAll('#monthly_chips .chip, #monthly_dep_chips .chip');
  allChips.forEach(chip => {{
    chip.addEventListener('click', function() {{
      allChips.forEach(c => c.classList.remove('active'));
      this.classList.add('active');
      const name = this.getAttribute('data-entity');
      updateLineChart(name);
    }});
  }});

  // 2. Department cards filter
  const filterChips = document.querySelectorAll('#dep_filter_chips .chip');
  const depCards = document.querySelectorAll('.dep_kpi_card');
  filterChips.forEach(chip => {{
    chip.addEventListener('click', function() {{
      filterChips.forEach(c => c.classList.remove('active'));
      this.classList.add('active');
      const filter = this.getAttribute('data-filter');
      depCards.forEach(card => {{
        if (filter === 'all' || card.getAttribute('data-block') === filter) {{
          card.classList.remove('hidden_element');
        }} else {{
          card.classList.add('hidden_element');
        }}
      }});
    }});
  }});

  // 3. KPI Tier switch (Both / +10% / +15%)
  const tierChips = document.querySelectorAll('#kpi_tier_chips .chip');
  const cols10 = document.querySelectorAll('.col_10');
  const cols15 = document.querySelectorAll('.col_15');
  const rowsTier10 = document.querySelectorAll('.row_tier_10');
  const rowsTier15 = document.querySelectorAll('.row_tier_15');

  tierChips.forEach(chip => {{
    chip.addEventListener('click', function() {{
      tierChips.forEach(c => c.classList.remove('active'));
      this.classList.add('active');
      const tier = this.getAttribute('data-tier');

      if (tier === 'both') {{
        cols10.forEach(c => c.classList.remove('table_col_highlight'));
        cols15.forEach(c => c.classList.remove('table_col_highlight'));
        rowsTier10.forEach(r => r.classList.remove('tier_focus'));
        rowsTier15.forEach(r => r.classList.remove('tier_focus'));
      }} else if (tier === '10') {{
        cols10.forEach(c => c.classList.add('table_col_highlight'));
        cols15.forEach(c => c.classList.remove('table_col_highlight'));
        rowsTier10.forEach(r => r.classList.add('tier_focus'));
        rowsTier15.forEach(r => r.classList.remove('tier_focus'));
      }} else if (tier === '15') {{
        cols10.forEach(c => c.classList.remove('table_col_highlight'));
        cols15.forEach(c => c.classList.add('table_col_highlight'));
        rowsTier10.forEach(r => r.classList.remove('tier_focus'));
        rowsTier15.forEach(r => r.classList.add('tier_focus'));
      }}
    }});
  }});
}})();
"""

html.append(f'<script>{js_script}</script>')
html.append('</body>')
html.append('</html>')

full_html = "\n".join(html)

# ==========================================
# STRICT CONSTRAINT VALIDATION
# ==========================================
print("Validating constraints strictly...")

style_matches = re.findall(r'\bstyle\s*=', full_html)
assert len(style_matches) == 0, f"Found inline style attributes: {style_matches}"

span_matches = re.findall(r'<\/?span\b', full_html)
assert len(span_matches) == 0, f"Found span tags: {span_matches}"

btn_matches = re.findall(r'<\/?button\b', full_html)
assert len(btn_matches) == 0, f"Found button tags: {btn_matches}"

assert "data:image" not in full_html, "Found base64 images!"

assert '<article class="container_AI">' in full_html, "Missing <article class=\"container_AI\">"
assert '<div class="wrap">' in full_html, "Missing <div class=\"wrap\">"

with open("index.html", "w", encoding="utf-8") as f:
    f.write(full_html)

print("SUCCESS: index.html generated and passed 100% of strict constraints!")

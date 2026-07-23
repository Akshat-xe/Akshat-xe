import os
import json
import warnings
from datetime import datetime

warnings.filterwarnings("ignore")

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "contributions.json")
OUTPUT_SVG = os.path.join(os.path.dirname(__file__), "..", "contrib-heatmap.svg")

# Premium Minimalist Palette (3-4 refined shades: Dark Charcoal -> Deep Wine -> Ruby Crimson)
PALETTE = [
    "#16161a",  # Level 0: Matte charcoal (empty day)
    "#3d1419",  # Level 1: Subdued deep wine
    "#801b25",  # Level 2: Rich studio crimson
    "#d62839",  # Level 3: Premium ruby red accent (high activity)
]

MONTH_NAMES = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

def render_heatmap():
    if not os.path.exists(DATA_PATH):
        print(f"Error: {DATA_PATH} not found. Run fetch_contributions.py first.")
        return

    with open(DATA_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    days = data.get("days", [])
    total_contribs = data.get("total_contributions", 0)
    current_streak = data.get("current_streak", 0)
    longest_streak = data.get("longest_streak", 0)

    weeks = []
    current_week = []
    
    if days:
        first_date = datetime.strptime(days[0]["date"], "%Y-%m-%d")
        gh_first_day = (first_date.weekday() + 1) % 7
        for _ in range(gh_first_day):
            current_week.append(None)

    for day in days:
        current_week.append(day)
        if len(current_week) == 7:
            weeks.append(current_week)
            current_week = []

    if current_week:
        while len(current_week) < 7:
            current_week.append(None)
        weeks.append(current_week)

    # Keep latest 53 weeks
    weeks = weeks[-53:]

    # Dimensions
    box_size = 11
    box_gap = 4
    margin_x = 45
    margin_y = 55
    width = 860
    height = 200

    # Month labels positioning
    month_labels = []
    last_month = None
    for w_idx, week in enumerate(weeks):
        for day in week:
            if day:
                d_obj = datetime.strptime(day["date"], "%Y-%m-%d")
                if d_obj.month != last_month:
                    last_month = d_obj.month
                    m_x = margin_x + w_idx * (box_size + box_gap)
                    month_labels.append((m_x, MONTH_NAMES[d_obj.month - 1]))
                    break

    # Build SVG content
    svg_parts = []
    svg_parts.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">')
    svg_parts.append('<defs>')
    svg_parts.append('''
        <style>
            .bg { fill: #0d0e12; rx: 12px; stroke: #22252e; stroke-width: 1.2px; }
            .title { font-family: "SFMono-Regular", Consolas, monospace; font-size: 13px; font-weight: 600; fill: #8b949e; }
            .total-count { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; font-size: 15px; font-weight: 800; fill: #d62839; }
            .total-label { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; font-size: 12px; font-weight: 500; fill: #8b949e; }
            .month-text { font-family: "SFMono-Regular", Consolas, monospace; font-size: 10px; fill: #767c88; }
            .day-text { font-family: "SFMono-Regular", Consolas, monospace; font-size: 9px; fill: #5c626e; }
            .stat-badge { font-family: "SFMono-Regular", Consolas, monospace; font-size: 11px; fill: #c9d1d9; font-weight: 600; }
            .stat-val { fill: #d62839; font-weight: 700; }
            .legend-text { font-family: "SFMono-Regular", Consolas, monospace; font-size: 10px; fill: #5c626e; }
            
            .day-box {
                rx: 2.5px;
                ry: 2.5px;
                transform-origin: center;
                opacity: 1;
                animation: diagonal-reveal 0.65s cubic-bezier(0.16, 1, 0.3, 1) forwards;
            }
            
            @keyframes diagonal-reveal {
                0% { opacity: 0; transform: scale(0.15); }
                70% { transform: scale(1.08); }
                100% { opacity: 1; transform: scale(1); }
            }
        </style>
    ''')
    svg_parts.append('</defs>')

    # Background card
    svg_parts.append(f'<rect class="bg" width="{width}" height="{height}" />')

    # Header
    svg_parts.append(f'<text x="20" y="28" class="title">akshat@github ~ $ ./contributions.sh</text>')
    
    # Highlighted Total Contributions
    svg_parts.append(f'<text x="{width - 20}" y="28" text-anchor="end">'
                     f'<tspan class="total-count">{total_contribs:,}</tspan> '
                     f'<tspan class="total-label">contributions in last year</tspan>'
                     f'</text>')

    # Month Labels
    for m_x, m_name in month_labels:
        svg_parts.append(f'<text x="{m_x}" y="47" class="month-text">{m_name}</text>')

    # Day Labels
    for d_idx, d_name in enumerate(["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]):
        if d_name in ["Mon", "Wed", "Fri"]:
            d_y = margin_y + d_idx * (box_size + box_gap) + 9
            svg_parts.append(f'<text x="22" y="{d_y}" class="day-text">{d_name}</text>')

    # Heatmap Grid Boxes
    for w_idx, week in enumerate(weeks):
        for d_idx, day in enumerate(week):
            if not day:
                continue
            x = margin_x + w_idx * (box_size + box_gap)
            y = margin_y + d_idx * (box_size + box_gap)
            
            raw_level = day.get("level", 0)
            # Map 0..5 levels cleanly to 4 palette steps:
            # 0 -> 0 (matte charcoal)
            # 1 -> 1 (wine)
            # 2..3 -> 2 (crimson)
            # 4..5 -> 3 (ruby red accent)
            if raw_level == 0:
                p_idx = 0
            elif raw_level == 1:
                p_idx = 1
            elif raw_level in (2, 3):
                p_idx = 2
            else:
                p_idx = 3

            color = PALETTE[p_idx]
            count = day.get("count", 0)
            date_str = day.get("date", "")
            
            # Slower, cinematic wave animation delay (0.025s per col + 0.03s per row)
            delay = (w_idx * 0.025) + (d_idx * 0.03)
            
            svg_parts.append(
                f'<rect class="day-box" x="{x}" y="{y}" width="{box_size}" height="{box_size}" '
                f'fill="{color}" style="animation-delay: {delay:.3f}s;">'
                f'<title>{count} contribution{"s" if count != 1 else ""} on {date_str}</title>'
                f'</rect>'
            )

    # Footer Stats (Clean: Current Streak & Longest Streak only, removed Best Day)
    footer_y = height - 16
    svg_parts.append(f'<text x="20" y="{footer_y}" class="stat-badge">'
                    f'🔥 Current Streak: <tspan class="stat-val">{current_streak} days</tspan> &#160;&#160;&#183;&#160;&#160; '
                    f'🏆 Longest Streak: <tspan class="stat-val">{longest_streak} days</tspan>'
                    f'</text>')

    # Legend
    legend_start_x = width - 130
    svg_parts.append(f'<text x="{legend_start_x - 30}" y="{footer_y}" class="legend-text">Less</text>')
    for l_idx, l_color in enumerate(PALETTE):
        lx = legend_start_x + l_idx * (11 + 4)
        ly = footer_y - 9
        svg_parts.append(f'<rect x="{lx}" y="{ly}" width="11" height="11" rx="2.5" fill="{l_color}" />')
    svg_parts.append(f'<text x="{legend_start_x + len(PALETTE) * 15 + 5}" y="{footer_y}" class="legend-text">More</text>')

    svg_parts.append('</svg>')

    with open(OUTPUT_SVG, "w", encoding="utf-8") as f:
        f.write("\n".join(svg_parts))

    print(f"Successfully rendered premium heatmap SVG: {OUTPUT_SVG}")

if __name__ == "__main__":
    render_heatmap()

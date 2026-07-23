import os

OUTPUT_SVG = os.path.join(os.path.dirname(__file__), "..", "info-card.svg")

def make_info_card():
    width = 430
    height = 390

    svg_parts = []
    svg_parts.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">')
    svg_parts.append('<defs>')
    svg_parts.append('''
        <style>
            @keyframes pulseBorder {
                0% { stroke: #2a2e39; filter: drop-shadow(0 0 2px rgba(214,40,57,0.2)); }
                50% { stroke: #801b25; filter: drop-shadow(0 0 8px rgba(214,40,57,0.6)); }
                100% { stroke: #2a2e39; filter: drop-shadow(0 0 2px rgba(214,40,57,0.2)); }
            }
            .card-bg {
                fill: #0d0e12;
                rx: 12px;
                stroke: #801b25;
                stroke-width: 1.5px;
                animation: pulseBorder 4s ease-in-out infinite;
            }
            .top-bar { fill: #16181f; rx: 12px 12px 0 0; }
            .btn-red { fill: #ff4d4d; }
            .btn-yellow { fill: #ffbd2e; }
            .btn-green { fill: #27c93f; }
            
            .term-title {
                font-family: "JetBrains Mono", "Fira Code", "SFMono-Regular", Consolas, monospace;
                font-size: 11px;
                fill: #8b949e;
                font-weight: 600;
            }
            
            .line {
                font-family: "JetBrains Mono", "Fira Code", "SFMono-Regular", Consolas, monospace;
                font-size: 11.5px;
                opacity: 1;
                animation: line-fade 0.4s ease-out forwards;
            }
            
            @keyframes line-fade {
                0% { opacity: 0; transform: translateY(6px); }
                100% { opacity: 1; transform: translateY(0); }
            }

            @keyframes statusGlow {
                0% { fill: #ff3b4e; filter: drop-shadow(0 0 2px #ff3b4e); }
                50% { fill: #ff6b7a; filter: drop-shadow(0 0 7px #ff6b7a); }
                100% { fill: #ff3b4e; filter: drop-shadow(0 0 2px #ff3b4e); }
            }
            .status-dot {
                animation: statusGlow 2s infinite ease-in-out;
            }

            .prompt-user { fill: #ff4d4d; font-weight: 700; }
            .prompt-colon { fill: #8b949e; font-weight: 500; }
            .prompt-path { fill: #58a6ff; font-weight: 600; }
            .prompt-symbol { fill: #ff4d4d; font-weight: 800; }
            .cmd { fill: #ffffff; font-weight: 700; filter: drop-shadow(0 0 3px rgba(255,255,255,0.4)); }
            .key { fill: #8b949e; font-weight: 500; }
            .val { fill: #f0f6fc; font-weight: 600; }
            .accent { fill: #ff4d4d; font-weight: 700; filter: drop-shadow(0 0 4px rgba(255,77,77,0.4)); }
            .subtext { fill: #ff4d4d; font-style: italic; font-size: 11.5px; font-weight: 700; filter: drop-shadow(0 0 5px rgba(255,77,77,0.5)); }
            .separator { fill: #262c36; }
            .badge { fill: #161013; stroke: #4a151b; stroke-width: 1.2; rx: 5; }
            .badge-txt { fill: #ff4d4d; font-size: 10px; font-weight: 700; font-family: "JetBrains Mono", Consolas, monospace; }
        </style>
    ''')
    svg_parts.append('</defs>')

    # Background & Top Window Bar
    svg_parts.append(f'<rect class="card-bg" width="{width}" height="{height}" />')
    svg_parts.append(f'<rect class="top-bar" width="{width}" height="32" />')

    # Window Controls (macOS style dots)
    svg_parts.append('<circle cx="18" cy="16" r="5.5" class="btn-red" />')
    svg_parts.append('<circle cx="34" cy="16" r="5.5" class="btn-yellow" />')
    svg_parts.append('<circle cx="50" cy="16" r="5.5" class="btn-green" />')
    svg_parts.append(f'<text x="{width / 2}" y="20" text-anchor="middle" class="term-title">akshat@evershtar ~ $ neofetch</text>')

    # Real Terminal Info Rows
    rows = [
        {"y": 56, "delay": 0.05, "content": '<tspan class="prompt-user">akshat@evershtar</tspan><tspan class="prompt-colon">:</tspan><tspan class="prompt-path">~</tspan><tspan class="prompt-symbol"> $ </tspan><tspan class="cmd">neofetch</tspan>'},
        {"y": 64, "delay": 0.1, "content": '<tspan class="separator">---------------------------------------</tspan>'},
        {"y": 88, "delay": 0.15, "content": '<tspan class="key">Institute:</tspan> <tspan class="val">Newton School of Tech (NST)</tspan>'},
        {"y": 112, "delay": 0.2, "content": '<tspan class="key">Role     :</tspan> <tspan class="accent">Founder &amp; Lead Builder @ Ever Shtar</tspan>'},
        {"y": 136, "delay": 0.25, "content": '<tspan class="key">Exp      :</tspan> <tspan class="val">17 y/o (1.5+ Years Building)</tspan>'},
        {"y": 160, "delay": 0.3, "content": '<tspan class="key">Focus    :</tspan> <tspan class="val">Full-Stack Web · AI · Automation</tspan>'},
        {"y": 184, "delay": 0.35, "content": '<tspan class="key">Products :</tspan> <tspan class="val">Pleiades Shtar · Lens Shtar · Shipped</tspan>'},
        {"y": 208, "delay": 0.4, "content": '<tspan class="key">Stack    :</tspan> <tspan class="val">Python · JS · FastAPI · React · HTML</tspan>'},
        {"y": 232, "delay": 0.45, "content": '<tspan class="key">Status   :</tspan> <tspan class="status-dot">●</tspan> <tspan class="accent">Building what shouldn\'t exist yet</tspan>'},
        {"y": 244, "delay": 0.5, "content": '<tspan class="separator">---------------------------------------</tspan>'},
        {"y": 268, "delay": 0.55, "content": '<tspan class="subtext">"Great systems should feel invisible."</tspan>'},
    ]

    for r in rows:
        svg_parts.append(
            f'<text x="20" y="{r["y"]}" class="line" style="animation-delay: {r["delay"]}s;">'
            f'{r["content"]}'
            f'</text>'
        )

    # Color Palette Blocks
    colors = ["#16161a", "#3d1419", "#801b25", "#d62839", "#ffffff"]
    block_start_y = 294
    block_start_x = 20
    block_w = 24
    block_h = 15
    
    svg_parts.append(f'<g class="line" style="animation-delay: 0.6s;">')
    for idx, c in enumerate(colors):
        bx = block_start_x + idx * (block_w + 6)
        svg_parts.append(f'<rect x="{bx}" y="{block_start_y}" width="{block_w}" height="{block_h}" rx="3" fill="{c}" />')
    svg_parts.append('</g>')

    # Highlight Badges
    svg_parts.append(f'<g class="line" style="animation-delay: 0.65s;">')
    svg_parts.append(f'<rect x="20" y="330" width="122" height="24" class="badge" />')
    svg_parts.append(f'<text x="81" y="346" text-anchor="middle" class="badge-txt">⚡ SHIPPED APPS</text>')
    
    svg_parts.append(f'<rect x="150" y="330" width="128" height="24" class="badge" />')
    svg_parts.append(f'<text x="214" y="346" text-anchor="middle" class="badge-txt">🚀 100% SOLO BUILT</text>')

    svg_parts.append(f'<rect x="286" y="330" width="124" height="24" class="badge" />')
    svg_parts.append(f'<text x="348" y="346" text-anchor="middle" class="badge-txt">🌐 EVER SHTAR</text>')
    svg_parts.append('</g>')

    svg_parts.append('</svg>')

    with open(OUTPUT_SVG, "w", encoding="utf-8") as f:
        f.write("\n".join(svg_parts))

    print(f"Successfully generated glowing real-terminal info card SVG: {OUTPUT_SVG}")

if __name__ == "__main__":
    make_info_card()

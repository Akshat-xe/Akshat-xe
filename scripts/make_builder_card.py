import os

OUTPUT_SVG = os.path.join(os.path.dirname(__file__), "..", "builder-card.svg")

def make_builder_card():
    width = 860
    height = 250

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
                font-size: 12px;
                opacity: 1;
                animation: line-fade 0.4s ease-out forwards;
            }
            
            @keyframes line-fade {
                0% { opacity: 0; transform: translateY(6px); }
                100% { opacity: 1; transform: translateY(0); }
            }

            @keyframes blink {
                0%, 100% { opacity: 1; }
                50% { opacity: 0; }
            }
            .cursor {
                fill: #ff4d4d;
                animation: blink 1s infinite;
                filter: drop-shadow(0 0 4px #ff4d4d);
            }

            .prompt-user { fill: #ff4d4d; font-weight: 700; }
            .prompt-colon { fill: #8b949e; font-weight: 500; }
            .prompt-path { fill: #58a6ff; font-weight: 600; }
            .prompt-symbol { fill: #ff4d4d; font-weight: 800; }
            .cmd { fill: #ffffff; font-weight: 700; filter: drop-shadow(0 0 3px rgba(255,255,255,0.4)); }
            .val { fill: #d0d7de; font-weight: 500; }
            .val-bold { fill: #ffffff; font-weight: 700; }
            .accent { fill: #ff4d4d; font-weight: 700; filter: drop-shadow(0 0 4px rgba(255,77,77,0.4)); }
            .separator { fill: #262c36; }
            .quote { fill: #ff4d4d; font-style: italic; font-size: 12.5px; font-weight: 700; filter: drop-shadow(0 0 6px rgba(255,77,77,0.5)); }
        </style>
    ''')
    svg_parts.append('</defs>')

    # Background & Top Window Bar
    svg_parts.append(f'<rect class="card-bg" width="{width}" height="{height}" />')
    svg_parts.append(f'<rect class="top-bar" width="{width}" height="34" />')

    # Window Controls (macOS style dots)
    svg_parts.append('<circle cx="18" cy="17" r="5.5" class="btn-red" />')
    svg_parts.append('<circle cx="34" cy="17" r="5.5" class="btn-yellow" />')
    svg_parts.append('<circle cx="50" cy="17" r="5.5" class="btn-green" />')
    svg_parts.append(f'<text x="{width / 2}" y="21" text-anchor="middle" class="term-title">akshat@evershtar: ~/builder (zsh)</text>')

    # Spacious, un-clustered terminal content lines
    rows = [
        {"y": 58, "delay": 0.05, "content": '<tspan class="prompt-user">akshat@evershtar</tspan><tspan class="prompt-colon">:</tspan><tspan class="prompt-path">~/builder</tspan><tspan class="prompt-symbol"> $ </tspan><tspan class="cmd">cat profile.md --verbose</tspan>'},
        {"y": 80, "delay": 0.1, "content": '<tspan class="val-bold">17-year-old founder &amp; developer studying at </tspan><tspan class="accent">Newton School of Technology (NST)</tspan><tspan class="val-bold">.</tspan>'},
        {"y": 100, "delay": 0.15, "content": '<tspan class="val">1.5+ years building websites, digital products, and AI tools — shipped to real clients</tspan>'},
        {"y": 120, "delay": 0.2, "content": '<tspan class="val">across India and internationally, without a team, without funding, without shortcuts.</tspan>'},
        {"y": 138, "delay": 0.25, "content": '<tspan class="separator">---------------------------------------------------------------------------------------------------</tspan>'},
        {"y": 160, "delay": 0.3, "content": '<tspan class="prompt-user">akshat@evershtar</tspan><tspan class="prompt-colon">:</tspan><tspan class="prompt-path">~/studio</tspan><tspan class="prompt-symbol"> $ </tspan><tspan class="cmd">cat studio-information.md</tspan> <tspan class="cursor">█</tspan>'},
        {"y": 182, "delay": 0.35, "content": '<tspan class="val">I run </tspan><tspan class="accent">Ever Shtar</tspan><tspan class="val"> — a digital studio delivering high-converting websites, automation systems,</tspan>'},
        {"y": 202, "delay": 0.4, "content": '<tspan class="val">and intelligence products. Work spans cafes, real estate, fintech, and wellness.</tspan>'},
        {"y": 224, "delay": 0.45, "content": '<tspan class="quote">"Great systems should feel invisible."</tspan>'},
    ]

    for r in rows:
        svg_parts.append(
            f'<text x="28" y="{r["y"]}" class="line" style="animation-delay: {r["delay"]}s;">'
            f'{r["content"]}'
            f'</text>'
        )

    svg_parts.append('</svg>')

    with open(OUTPUT_SVG, "w", encoding="utf-8") as f:
        f.write("\n".join(svg_parts))

    print(f"Successfully generated spacious Builder Card SVG: {OUTPUT_SVG}")

if __name__ == "__main__":
    make_builder_card()

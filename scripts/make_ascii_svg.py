import os
import sys
from PIL import Image, ImageEnhance
import cv2
import numpy as np

PHOTO_PATH = os.path.join(os.path.dirname(__file__), "..", "akshatphoto.png")
OUTPUT_SVG = os.path.join(os.path.dirname(__file__), "..", "akshat-ascii.svg")

RAMP = " .':;!~+-=xX%#$@"

def make_ascii_svg():
    if not os.path.exists(PHOTO_PATH):
        print(f"Error: {PHOTO_PATH} does not exist.")
        sys.exit(1)

    print(f"Processing high-resolution photo from {PHOTO_PATH}...")
    img = Image.open(PHOTO_PATH)
    r, g, b, a = img.split()

    bbox = a.getbbox()
    if bbox:
        img = img.crop(bbox)
        a = a.crop(bbox)

    gray = img.convert("L")

    # CLAHE contrast enhancement
    img_np = np.array(gray)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    enhanced_np = clahe.apply(img_np)
    enhanced_img = Image.fromarray(enhanced_np)

    enhancer = ImageEnhance.Contrast(enhanced_img)
    enhanced_img = enhancer.enhance(1.35)

    # Full resolution photo grid (105 cols) for maximum sharpness
    target_width = 105
    aspect_ratio = 0.52
    target_height = int(target_width * (enhanced_img.height / enhanced_img.width) * aspect_ratio)

    resized = enhanced_img.resize((target_width, target_height), Image.Resampling.LANCZOS)
    alpha_resized = a.resize((target_width, target_height), Image.Resampling.LANCZOS)

    pixels = np.array(resized)
    alpha_np = np.array(alpha_resized)

    lines = []
    ramp_len = len(RAMP)
    for y in range(target_height):
        line_chars = []
        for x in range(target_width):
            if alpha_np[y, x] < 40:
                line_chars.append(" ")
            else:
                val = pixels[y, x]
                idx = int(((255 - val) / 255.0) * (ramp_len - 1))
                idx = max(0, min(ramp_len - 1, idx))
                line_chars.append(RAMP[idx])
        lines.append("".join(line_chars))

    # Exact matching card container dimensions (430x390)
    svg_width = 430
    svg_height = 390

    char_width = 3.8
    char_height = 6.3

    # Perfectly centered in container
    start_x = (svg_width - (target_width * char_width)) / 2
    start_y = 44

    svg_parts = []
    svg_parts.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {svg_width} {svg_height}" width="{svg_width}" height="{svg_height}">')
    svg_parts.append('<defs>')
    svg_parts.append(f'''
        <style>
            @keyframes pulseBorder {{
                0% {{ stroke: #2a2e39; filter: drop-shadow(0 0 2px rgba(214,40,57,0.2)); }}
                50% {{ stroke: #801b25; filter: drop-shadow(0 0 8px rgba(214,40,57,0.6)); }}
                100% {{ stroke: #2a2e39; filter: drop-shadow(0 0 2px rgba(214,40,57,0.2)); }}
            }}
            .card-bg {{
                fill: #0d0e12;
                rx: 12px;
                stroke: #801b25;
                stroke-width: 1.5px;
                animation: pulseBorder 4s ease-in-out infinite;
            }}
            .top-bar {{ fill: #16181f; rx: 12px 12px 0 0; }}
            .btn-red {{ fill: #ff4d4d; }}
            .btn-yellow {{ fill: #ffbd2e; }}
            .btn-green {{ fill: #27c93f; }}
            
            .term-title {{
                font-family: "JetBrains Mono", "Fira Code", "SFMono-Regular", Consolas, monospace;
                font-size: 11px;
                fill: #8b949e;
                font-weight: 600;
            }}
            
            .ascii-text {{
                font-family: "JetBrains Mono", "Fira Code", "SFMono-Regular", Consolas, monospace;
                font-size: 6.2px;
                fill: #d62839;
                white-space: pre;
                letter-spacing: -0.2px;
                font-weight: 600;
            }}

            @keyframes lineWipe {{
                0% {{ width: 0px; }}
                100% {{ width: {svg_width}px; }}
            }}
            .clip-rect {{
                animation: lineWipe 0.25s ease-out forwards;
            }}

            @keyframes scanline {{
                0% {{ transform: translateY(35px); opacity: 0.3; }}
                50% {{ opacity: 0.8; }}
                100% {{ transform: translateY(380px); opacity: 0.3; }}
            }}
            .scan-line {{
                stroke: url(#scan-grad);
                stroke-width: 1.5;
                animation: scanline 3s linear infinite;
            }}
        </style>
        <linearGradient id="scan-grad" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stop-color="#d62839" stop-opacity="0" />
            <stop offset="50%" stop-color="#ff4d4d" stop-opacity="0.8" />
            <stop offset="100%" stop-color="#d62839" stop-opacity="0" />
        </linearGradient>
    ''')

    total_lines = len(lines)
    dur_per_line = 0.02
    for i in range(total_lines):
        start_time = i * dur_per_line
        svg_parts.append(f'<clipPath id="line-clip-{i}">')
        svg_parts.append(f'  <rect class="clip-rect" x="0" y="0" width="{svg_width}" height="{svg_height}" style="animation-delay: {start_time:.3f}s;">')
        svg_parts.append(f'    <animate attributeName="width" from="0" to="{svg_width}" dur="0.25s" begin="{start_time:.3f}s" fill="freeze" />')
        svg_parts.append('  </rect>')
        svg_parts.append('</clipPath>')

    svg_parts.append('</defs>')

    # Background card & Top Window Bar
    svg_parts.append(f'<rect class="card-bg" width="{svg_width}" height="{svg_height}" />')
    svg_parts.append(f'<rect class="top-bar" width="{svg_width}" height="32" />')

    # Window Controls
    svg_parts.append('<circle cx="18" cy="16" r="5.5" class="btn-red" />')
    svg_parts.append('<circle cx="34" cy="16" r="5.5" class="btn-yellow" />')
    svg_parts.append('<circle cx="50" cy="16" r="5.5" class="btn-green" />')
    svg_parts.append(f'<text x="{svg_width / 2}" y="20" text-anchor="middle" class="term-title">akshat@evershtar ~ $ ./portrait</text>')

    # ASCII Rows
    for i, line in enumerate(lines):
        y_pos = start_y + i * char_height
        safe_line = line.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        svg_parts.append(
            f'<g clip-path="url(#line-clip-{i})">'
            f'<text x="{start_x:.1f}" y="{y_pos:.1f}" class="ascii-text">{safe_line}</text>'
            f'</g>'
        )

    # Live animated scanline effect
    svg_parts.append(f'<line x1="5" y1="0" x2="{svg_width - 5}" y2="0" class="scan-line" />')

    svg_parts.append('</svg>')

    with open(OUTPUT_SVG, "w", encoding="utf-8") as f:
        f.write("\n".join(svg_parts))

    print(f"Successfully restored full-resolution ASCII SVG portrait: {OUTPUT_SVG}")

if __name__ == "__main__":
    make_ascii_svg()

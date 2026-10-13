import cv2

RAMP = " .`:-=+*cs#%@"  # 亮度由亮到暗（純白對應空格，主體落在深色字元）
WIDTH = 80              # 字元寬度

img = cv2.imread("source-prepped.png", cv2.IMREAD_GRAYSCALE)
aspect_ratio = img.shape[0] / img.shape[1]
height = int(WIDTH * aspect_ratio * 0.5)  # 終端機字元高寬比約 2:1
resized = cv2.resize(img, (WIDTH, height), interpolation=cv2.INTER_AREA)

lines = []
for row in resized:
    line = "".join(RAMP[int((pixel / 255) * (len(RAMP) - 1))] for pixel in row)
    lines.append(line.rstrip())

# 構建帶有 SMIL 動畫的 SVG
font_size = 8
line_height = 9.5
svg_w = WIDTH * 5.2
svg_h = height * line_height + 20

svg_parts = [
    f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {svg_w} {svg_h}" width="370">',
    '<style>',
    '  .ascii { font-family: monospace; font-size: 8px; fill: #c9d1d9; white-space: pre; }',
    '</style>',
    f'<rect width="100%" height="100%" fill="#0d1117" rx="6"/>'
]

for idx, line in enumerate(lines):
    y = 20 + idx * line_height
    delay = idx * 0.04
    # 利用 clipPath 或直接 opacity 延遲逐行打字
    svg_parts.append(
        f'<text x="15" y="{y}" class="ascii" opacity="0">'
        f'{line}'
        f'<animate attributeName="opacity" to="1" dur="0.05s" begin="{delay:.2f}s" fill="freeze" />'
        f'</text>'
    )

svg_parts.append('</svg>')

with open("avi-ascii.svg", "w", encoding="utf-8") as f:
    f.write("\n".join(svg_parts))
print("avi-ascii.svg generated.")
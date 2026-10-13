import numpy as np
from PIL import Image

RAMP = " .`:-=+*cs#%@"  # 稀疏 -> 密集；深色底上，越亮的地方用越密的字元
WIDTH = 80              # 字元寬度
FONT_SIZE = 8
CHAR_W = FONT_SIZE * 0.6  # 等寬字型的字寬約為字高的 0.6
LINE_H = 9.5
PAD = 15

img = Image.open("source-prepped.png").convert("LA")
aspect_ratio = img.height / img.width
height = int(WIDTH * aspect_ratio * CHAR_W / LINE_H)  # 補償字元的高寬比
small = np.array(img.resize((WIDTH, height), Image.LANCZOS)).astype(float)
gray, alpha = small[:, :, 0] / 255, small[:, :, 1] / 255

# 只用人物本身的明暗來拉伸對比，讓臉部用到完整的字元範圍
fg = gray[alpha >= 0.5]
lo, hi = np.percentile(fg, 2), np.percentile(fg, 98)
gray = np.clip((gray - lo) / max(hi - lo, 1e-6), 0, 1)

lines = []
for g_row, a_row in zip(gray, alpha):
    chars = []
    for g, a in zip(g_row, a_row):
        if a < 0.5:
            chars.append(" ")  # 去背後的背景 -> 空白
        else:
            # 人物最暗處也至少給一個 "."，輪廓才不會斷掉
            chars.append(RAMP[1 + int(g * (len(RAMP) - 2))])
    lines.append("".join(chars).rstrip())

# 去掉上下空白行
while lines and not lines[0].strip():
    lines.pop(0)
while lines and not lines[-1].strip():
    lines.pop()

svg_w = WIDTH * CHAR_W + PAD * 2
svg_h = len(lines) * LINE_H + PAD * 2

svg_parts = [
    f'<svg xmlns="http://www.w3.org/2000/svg" xml:space="preserve" viewBox="0 0 {svg_w:.0f} {svg_h:.0f}" width="370">',
    '<style>',
    f'  .ascii {{ font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; font-size: {FONT_SIZE}px; fill: #c9d1d9; white-space: pre; }}',
    '</style>',
    f'<rect width="100%" height="100%" fill="#0d1117" rx="6" stroke="#30363d"/>',
]

for idx, line in enumerate(lines):
    y = PAD + FONT_SIZE + idx * LINE_H
    delay = idx * 0.05
    # 每一行用一個由左往右展開的 clipPath 做「打字」效果，印完就停住不循環
    svg_parts.append(
        f'<clipPath id="c{idx}"><rect x="{PAD}" y="{y - FONT_SIZE}" width="0" height="{LINE_H}">'
        f'<animate attributeName="width" from="0" to="{WIDTH * CHAR_W:.0f}" dur="0.35s" begin="{delay:.2f}s" fill="freeze"/>'
        f'</rect></clipPath>'
        f'<text x="{PAD}" y="{y:.1f}" class="ascii" clip-path="url(#c{idx})" textLength="{len(line) * CHAR_W:.1f}">{line}</text>'
    )

svg_parts.append('</svg>')

with open("avi-ascii.svg", "w", encoding="utf-8") as f:
    f.write("\n".join(svg_parts))
print("avi-ascii.svg generated.")
print("\n".join(lines))

import json

PALETTE = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353", "#69f0a0"]

with open("data/contributions.json", "r", encoding="utf-8") as f:
    days = json.load(f)

svg_parts = [
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 860 140" width="860">',
    '<style>',
    '  .box { rx: 2px; ry: 2px; animation: slideIn 0.3s ease forwards; opacity: 0; }',
    '  @keyframes slideIn { from { transform: translateY(8px); opacity: 0; } to { transform: translateY(0); opacity: 1; } }',
    '</style>',
    '<rect width="100%" height="100%" fill="#0d1117" rx="6" stroke="#30363d"/>'
]

# 53 週 × 7 天佈局
for idx, day in enumerate(days[-371:]):  # 抓近 53 週 (53 * 7 = 371)
    col = idx // 7
    row = idx % 7
    x = 25 + col * 15
    y = 20 + row * 15
    color = PALETTE[min(day["level"], 5)]
    delay = (col * 0.015) + (row * 0.01)  # 對角線依序滑入
    svg_parts.append(
        f'<rect x="{x}" y="{y}" width="11" height="11" fill="{color}" class="box" '
        f'style="animation-delay: {delay:.2f}s;"/>'
    )

svg_parts.append('</svg>')

with open("contrib-heatmap.svg", "w", encoding="utf-8") as f:
    f.write("\n".join(svg_parts))
print("contrib-heatmap.svg generated.")
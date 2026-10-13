import json
from datetime import date

PALETTE = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353", "#69f0a0"]
CELL, GAP = 11, 4
STEP = CELL + GAP
LEFT, TOP = 40, 40

with open("data/contributions.json", "r", encoding="utf-8") as f:
    data = json.load(f)
days = data["days"][-371:]  # 近 53 週

# 依實際星期幾排版（星期日在最上面），不靠索引硬算，第一週不完整也不會錯位
first = date.fromisoformat(days[0]["date"])
offset = (first.weekday() + 1) % 7  # Python 星期一=0，換成星期日=0

svg_w, svg_h = 860, 200
parts = [
    f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {svg_w} {svg_h}" width="{svg_w}">',
    '<style>',
    '  .box { opacity: 0; animation: slideIn 0.35s ease-out forwards; }',
    '  @keyframes slideIn { from { opacity: 0; transform: translateY(-6px); } to { opacity: 1; transform: translateY(0); } }',
    '  .lbl { font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; font-size: 10px; fill: #7d8590; }',
    '  .stat { font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; font-size: 12px; fill: #c9d1d9; }',
    '  .hi { fill: #39d353; font-weight: bold; }',
    '</style>',
    f'<rect width="{svg_w}" height="{svg_h}" fill="#0d1117" rx="6" stroke="#30363d"/>',
]

# 星期標籤
for row, name in [(1, "Mon"), (3, "Wed"), (5, "Fri")]:
    parts.append(f'<text x="8" y="{TOP + row * STEP + 9}" class="lbl">{name}</text>')

last_month = None
for i, day in enumerate(days):
    idx = i + offset
    col, row = idx // 7, idx % 7
    x, y = LEFT + col * STEP, TOP + row * STEP
    d = date.fromisoformat(day["date"])
    # 月份標籤：每個月第一次出現的那一欄
    if row == 0 or i == 0:
        if d.month != last_month:
            last_month = d.month
            if col < 52:
                parts.append(f'<text x="{x}" y="{TOP - 10}" class="lbl">{d.strftime("%b")}</text>')
    color = PALETTE[min(day["level"], 5)]
    delay = col * 0.018 + row * 0.03  # 對角線依序滑入
    parts.append(
        f'<rect x="{x}" y="{y}" width="{CELL}" height="{CELL}" rx="2" fill="{color}" class="box" '
        f'style="animation-delay: {delay:.2f}s"><title>{day["count"]} on {day["date"]}</title></rect>'
    )

# 底部：統計 + Less→More 圖例
fy = TOP + 7 * STEP + 28
parts.append(
    f'<text x="{LEFT}" y="{fy}" class="stat"><tspan class="hi">{data["total"]:,}</tspan> contributions in the last year'
    f'  ·  current streak <tspan class="hi">{data["current_streak"]}</tspan>d'
    f'  ·  longest <tspan class="hi">{data["longest_streak"]}</tspan>d</text>'
)
lx = svg_w - 40 - 5 * STEP - 70
parts.append(f'<text x="{lx}" y="{fy}" class="lbl">Less</text>')
for i, c in enumerate(PALETTE[:5]):
    parts.append(f'<rect x="{lx + 30 + i * STEP}" y="{fy - 10}" width="{CELL}" height="{CELL}" rx="2" fill="{c}"/>')
parts.append(f'<text x="{lx + 30 + 5 * STEP + 4}" y="{fy}" class="lbl">More</text>')

parts.append('</svg>')

with open("contrib-heatmap.svg", "w", encoding="utf-8") as f:
    f.write("\n".join(parts))
print("contrib-heatmap.svg generated.")

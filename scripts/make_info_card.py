lines_data = [
    ("OS", "macOS Sonoma / Arch Linux"),
    ("Host", "GitHub Profile CLI"),
    ("Kernel", "Quantitative & Systems"),
    ("Uptime", "Active 365+ days"),
    ("Stack", "Python, SQL, RAG, LaTeX"),
    ("Interests", "Econometrics, Time Series, FinTech"),
]

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 450 320" width="490">
  <style>
    .base {{ font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 13px; }}
    .title {{ fill: #58a6ff; font-weight: bold; }}
    .key {{ fill: #7ee787; font-weight: bold; }}
    .val {{ fill: #c9d1d9; }}
    .fade {{ animation: fadeIn 0.4s ease forwards; opacity: 0; }}
    @keyframes fadeIn {{ to {{ opacity: 1; }} }}
  </style>
  <rect width="100%" height="100%" fill="#0d1117" rx="6" stroke="#30363d"/>
  <text x="25" y="40" class="base title">user@profile ~ $ neofetch</text>
  <path d="M 25 55 L 425 55" stroke="#30363d" stroke-width="1"/>
'''

for i, (k, v) in enumerate(lines_data):
    delay = 0.2 + i * 0.12
    y = 85 + i * 32
    svg += f'''  <g class="fade" style="animation-delay: {delay:.2f}s;">
    <text x="25" y="{y}" class="base key">{k}:</text>
    <text x="120" y="{y}" class="base val">{v}</text>
  </g>\n'''

svg += '</svg>'

with open("info-card.svg", "w", encoding="utf-8") as f:
    f.write(svg)
print("info-card.svg generated.")
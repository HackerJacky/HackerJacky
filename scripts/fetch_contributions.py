import json
import os
import re

import requests
from bs4 import BeautifulSoup

USERNAME = "HackerJacky"
url = f"https://github.com/users/{USERNAME}/contributions"
resp = requests.get(url, timeout=30, headers={"User-Agent": "profile-art-bot"})
resp.raise_for_status()  # 抓取失敗就直接報錯，不會 commit 空白圖
soup = BeautifulSoup(resp.text, "html.parser")

# 每一格的實際貢獻數放在對應的 <tool-tip for="格子id"> 裡，例如 "3 contributions on ..."
counts = {}
for tip in soup.find_all("tool-tip"):
    m = re.match(r"(\d+) contribution", tip.get_text(strip=True))
    counts[tip.get("for")] = int(m.group(1)) if m else 0

days = []
for cell in soup.find_all("td", class_="ContributionCalendar-day"):
    date = cell.get("data-date")
    if not date:
        continue
    days.append({
        "date": date,
        "level": int(cell.get("data-level", "0")),
        "count": counts.get(cell.get("id"), 0),
    })

if not days:
    raise SystemExit("No contribution cells found — GitHub page layout may have changed.")

# GitHub 的表格是「一列一個星期幾」，抓下來的順序不是時間順序，要依日期排序
days.sort(key=lambda d: d["date"])


def streaks(days):
    longest = current = run = 0
    for d in days:
        run = run + 1 if d["count"] > 0 else 0
        longest = max(longest, run)
    # 目前連續天數：從最後一天往回數（今天還沒提交不算斷）
    for i, d in enumerate(reversed(days)):
        if d["count"] > 0:
            current += 1
        elif i > 0:
            break
    return current, longest


current, longest = streaks(days)
best = max(days, key=lambda d: d["count"])
data = {
    "username": USERNAME,
    "total": sum(d["count"] for d in days),
    "current_streak": current,
    "longest_streak": longest,
    "best_day": {"date": best["date"], "count": best["count"]},
    "days": days,
}

os.makedirs("data", exist_ok=True)  # Actions 上沒有空的 data/ 資料夾，要自己建
with open("data/contributions.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)
print(f"Fetched {len(days)} days, {data['total']} contributions.")

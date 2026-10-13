import json
import requests
from bs4 import BeautifulSoup

USERNAME = "你的GitHub帳號名稱"  # 記得修改
url = f"https://github.com/users/{USERNAME}/contributions"
resp = requests.get(url)
soup = BeautifulSoup(resp.text, "html.parser")

days = []
for cell in soup.find_all("td", class_="ContributionCalendar-day"):
    level = cell.get("data-level", "0")
    date = cell.get("data-date", "")
    days.append({"date": date, "level": int(level)})

with open("data/contributions.json", "w", encoding="utf-8") as f:
    json.dump(days, f, indent=2)
print(f"Fetched {len(days)} days of contributions.")
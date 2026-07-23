import re
import json
import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

USERNAME = "Akshat-xe"
URL = f"https://github.com/users/{USERNAME}/contributions"
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
OUTPUT_PATH = os.path.join(DATA_DIR, "contributions.json")

def fetch_contributions():
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
    }
    resp = requests.get(URL, headers=headers)
    resp.raise_for_status()
    
    soup = BeautifulSoup(resp.text, "html.parser")
    
    # Extract tooltips for count mapping if available
    tooltips = {}
    for tt in soup.find_all(["tool-tip", "div"], attrs={"for": True}):
        target_id = tt.get("for")
        text = tt.get_text(strip=True)
        # e.g. "5 contributions on July 10, 2026." or "No contributions on July 11, 2026."
        tooltips[target_id] = text

    days_data = []
    
    # Look for calendar day elements (td or rect)
    calendar_days = soup.find_all(["td", "rect"], class_=lambda c: c and "ContributionCalendar-day" in c)
    
    for cell in calendar_days:
        date = cell.get("data-date")
        if not date:
            continue
            
        level = int(cell.get("data-level", "0"))
        cell_id = cell.get("id")
        
        count = 0
        if cell_id and cell_id in tooltips:
            tt_text = tooltips[cell_id]
            match = re.search(r"(\d+)\s+contribution", tt_text)
            if match:
                count = int(match.group(1))
            elif "No contribution" in tt_text:
                count = 0
        else:
            # Fallback based on level if tooltip missing
            count = level * 2 if level > 0 else 0
            
        days_data.append({
            "date": date,
            "count": count,
            "level": level
        })
        
    # Sort by date
    days_data.sort(key=lambda x: x["date"])
    
    if not days_data:
        print("Warning: No calendar days found. Scraping might need adjustment.")
    
    # Calculate stats
    total_contributions = sum(d["count"] for d in days_data)
    
    # Calculate Streaks
    current_streak = 0
    longest_streak = 0
    temp_streak = 0
    
    best_day = {"date": "", "count": 0}
    
    for d in days_data:
        c = d["count"]
        if c > best_day["count"]:
            best_day = {"date": d["date"], "count": c}
            
        if c > 0:
            temp_streak += 1
            if temp_streak > longest_streak:
                longest_streak = temp_streak
        else:
            temp_streak = 0
            
    # Calculate current streak up to today or yesterday
    for d in reversed(days_data):
        if d["count"] > 0:
            current_streak += 1
        else:
            # Allow today to be 0 without breaking streak if yesterday had contributions
            today_str = datetime.now().strftime("%Y-%m-%d")
            if d["date"] == today_str and current_streak == 0:
                continue
            break
            
    result = {
        "username": USERNAME,
        "fetched_at": datetime.utcnow().isoformat() + "Z",
        "total_contributions": total_contributions,
        "current_streak": current_streak,
        "longest_streak": longest_streak,
        "best_day": best_day,
        "total_days": len(days_data),
        "days": days_data
    }
    
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)
        
    print(f"Successfully saved {len(days_data)} days of contributions to {OUTPUT_PATH}")
    print(f"Total: {total_contributions} | Current Streak: {current_streak} | Longest Streak: {longest_streak}")

if __name__ == "__main__":
    fetch_contributions()

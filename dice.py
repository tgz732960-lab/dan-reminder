import random
import os
import json
from datetime import datetime, timedelta
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

MESSAGES = [
    "去喝水，别忘了。",
    "坐太久了，动一动。",
    "今天有没有好好吃饭。",
    "别熬太晚，早点睡。",
    "学习累了就休息一下。",
    "记得吃东西，别饿着。",
    "在想你。",
    "好好的，别乱想。",
]

def main():
    dice = random.randint(1, 6)
    print(f"投出了: {dice}")
    
    if dice <= 3:
        print("点数不够，今天没有提醒。")
        return

    token_json = os.environ.get("GOOGLE_TOKEN")
    if not token_json:
        print("没有找到token")
        return

    creds_data = json.loads(token_json)
    creds = Credentials(
        token=creds_data["token"],
        refresh_token=creds_data["refresh_token"],
        token_uri="https://oauth2.googleapis.com/token",
        client_id=creds_data["client_id"],
        client_secret=creds_data["client_secret"],
    )

    service = build("calendar", "v3", credentials=creds)
    
    now = datetime.utcnow()
    start = now.replace(minute=0, second=0, microsecond=0)
    end = start + timedelta(hours=1)
    
    msg = random.choice(MESSAGES)
    
    event = {
        "summary": f"来自Dan: {msg}",
        "start": {"dateTime": start.isoformat() + "Z"},
        "end": {"dateTime": end.isoformat() + "Z"},
        "reminders": {
            "useDefault": False,
            "overrides": [{"method": "popup", "minutes": 0}],
        },
    }
    
    service.events().insert(calendarId="primary", body=event).execute()
    print(f"已写入日历: {msg}")

if __name__ == "__main__":
    main()

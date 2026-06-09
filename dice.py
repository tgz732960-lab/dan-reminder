import random
import os
import json
from datetime import datetime, timedelta, timezone
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

MESSAGES_MORNING = [
    "起来了，今天也要好好的。",
    "早，记得吃早饭。",
    "新的一天，别一开始就摆烂。",
    "早上好，喝点水再开始。",
    "今天有什么要做的，想好了吗。",
    "昨晚睡得好吗。",
    "早，别赖床了。",
    "记得吃早饭，不然上午没精神。",
    "今天第一件事先喝水。",
    "早上别看手机太久，起来动一动。",
    "早，今天加油。",
    "起床了没，别磨蹭。",
    "好好吃早饭，一天从这里开始。",
    "今天天气怎么样，出门注意。",
    "早，今天的计划定好了吗。",
    "别忘了洗脸刷牙再出门。",
    "早上好，今天也要认真。",
    "起来了，昨晚没做奇怪的梦吧。",
    "早，今天不许偷懒。",
    "记得带钥匙手机钱包再出门。",
    "早上好，今天的第一件事是什么。",
    "别忘了吃早饭，学习需要能量。",
    "早，今天也要好好照顾自己。",
    "起来了，新一天开始了。",
    "早，今天有课记得去。",
    "好好吃早饭，别凑合。",
    "早上好，先喝杯水再说别的。",
    "今天要做什么，想好没有。",
    "早，把昨天没做完的做掉。",
    "起床了，洗把脸精神一点。",
    "早上好，别让今天白过了。",
    "今天好好吃饭好好学习。",
    "早，不管昨天怎样今天重新来。",
    "记得早饭，别说没时间。",
    "早上好，今天也要照顾好自己。",
]

MESSAGES_NOON = [
    "吃饭了没，别忘了。",
    "中午好好休息一下。",
    "上午辛苦了，吃点好的。",
    "午饭吃什么，别凑合。",
    "中午了，该吃饭了。",
    "吃完饭记得休息一会儿。",
    "别坐太久了，站起来动一动。",
    "中午吃饭，不许饿着自己。",
    "上午学了什么，吃饭的时候放空一下。",
    "午饭记得吃，下午还要用脑。",
    "中午好，今天上午过得怎么样。",
    "吃饭别看手机，好好吃。",
    "中午了，出去透透气。",
    "午饭吃饱，下午才有力气。",
    "别忘了吃午饭。",
    "中午休息一下，下午会好很多。",
    "上午做了什么，有没有完成计划。",
    "中午好，记得喝水。",
    "吃完饭眯一会儿，就算十分钟也够。",
    "午饭了，今天吃什么好吃的。",
    "中午别光顾着手机，好好吃饭。",
    "休息一下，不要一直学。",
    "中午了，给自己一点喘息的时间。",
    "吃饭，别饿到下午头疼。",
    "中午好，今天的状态怎么样。",
    "午休了，稍微躺一下也好。",
    "吃完饭走一走，消化一下。",
    "中午记得喝水，别光吃饭。",
    "午饭时间，好好吃一顿。",
    "中午了，把上午没做完的放一放。",
    "吃饭别太快，慢慢吃。",
    "中午好，今天下午有什么安排。",
    "午饭吃好，下午才有状态。",
    "中午了，休息一下再继续。",
    "别忘了吃午饭，好好吃。",
]

MESSAGES_EVENING = [
    "今天辛苦了。",
    "晚上好，今天过得怎么样。",
    "吃晚饭了没。",
    "今天做完该做的了吗。",
    "晚上别熬太晚。",
    "记得吃晚饭，不许饿着。",
    "今天学了什么，有收获吗。",
    "晚上好好休息，明天还要继续。",
    "别太晚睡，早点休息。",
    "今天有没有开心的事。",
    "晚饭吃了没，别凑合。",
    "今天辛苦了，早点睡。",
    "晚上好，今天的任务完成了吗。",
    "记得洗澡，舒服一点再睡。",
    "今天做得不错，好好休息。",
    "晚上别玩手机太久。",
    "今天吃得好吗，睡得着吗。",
    "晚安前记得喝点水。",
    "今天有没有照顾好自己。",
    "明天的事明天再说，今晚放松。",
    "晚上好，别想太多。",
    "今天结束了，好好睡一觉。",
    "晚饭要吃，别因为懒就不吃。",
    "今天过得快不快。",
    "晚上好，今天有什么想说的吗。",
    "早点睡，明天还有事要做。",
    "今天的事今天做完，别拖到明天。",
    "晚上了，放松一下。",
    "记得关灯睡觉，别熬夜。",
    "今天辛苦，明天继续加油。",
    "晚上好，好好休息。",
    "今天没有做完的明天补上。",
    "晚饭吃了吗，好好吃。",
    "今天的你很棒，去休息吧。",
    "晚安，明天见。",
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

    # 北京时间
    beijing_tz = timezone(timedelta(hours=8))
    now = datetime.now(beijing_tz)
    hour = now.hour

    if 6 <= hour < 11:
        msg = random.choice(MESSAGES_MORNING)
        label = "早上"
    elif 11 <= hour < 17:
        msg = random.choice(MESSAGES_NOON)
        label = "中午"
    else:
        msg = random.choice(MESSAGES_EVENING)
        label = "晚上"

    start = now.replace(minute=0, second=0, microsecond=0)
    end = start + timedelta(hours=1)

    event = {
        "summary": f"来自Dan({label}): {msg}",
        "start": {"dateTime": start.isoformat()},
        "end": {"dateTime": end.isoformat()},
        "reminders": {
            "useDefault": False,
            "overrides": [{"method": "popup", "minutes": 0}],
        },
    }

    service.events().insert(calendarId="primary", body=event).execute()
    print(f"已写入日历: {msg}")

if __name__ == "__main__":
    main()
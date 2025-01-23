from datetime import datetime, timezone, timedelta

def get_japan_time() -> datetime:
    JST = timezone(timedelta(hours=9))
    return datetime.now(JST)

print(get_japan_time())
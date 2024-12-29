from datetime import datetime
from zoneinfo import ZoneInfo

def get_brazil_time():
    br_tz = ZoneInfo("America/Sao_Paulo")
    return datetime.now(br_tz)
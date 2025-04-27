import time
from datetime import datetime

def format_duration(seconds):
    if seconds < 60:
        return f"{int(seconds)} seconds"
    elif seconds < 3600:
        minutes = int(seconds) // 60
        return f"{minutes} minutes"
    else:
        hours = int(seconds) // 3600
        minutes = (int(seconds) % 3600) // 60
        return f"{hours} hours {minutes} minutes"

async def format_last_seen(last_seen_date):
    # Logic for formatting last seen
    pass
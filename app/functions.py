from datetime import datetime, timedelta


async def get_message_moscow_time(time):
    moscow_time = time + timedelta(hours=3)
    return moscow_time

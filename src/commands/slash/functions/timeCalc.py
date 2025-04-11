from datetime import timedelta, datetime
import time

region_offsets = {
    "central_europe": "+2",
    "western_europe": "+1",
    "northern_europe": "+2",
    "southern_europe": "+2",
    "eastern_europe": "+3",
    "middle_east": "+3",
    "southeast_asia": "+7",
    "south_asia": "+5.5",
    "central_asia": "+6",
    "sub_saharan_africa": "+3",
    "north_africa": "+1",
    "caribbean": "-5",
    "central_america": "-6",
    "northen_america": "-4",
    "pacific_islands": "+12"
}

def get_time(region_key: str):
    offsetStr = region_offsets.get(region_key.lower())
    if not offsetStr:
        return time.time()
    
    offset_hours = float(offsetStr)
    offset = timedelta(hours=int(offset_hours), minutes=(offset_hours % 1) * 60)
    
    region_time = datetime.utcnow() + offset
    unix_timestamp = int(time.mktime(region_time.timetuple()))
    return unix_timestamp, offsetStr
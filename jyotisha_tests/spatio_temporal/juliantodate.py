import math
from datetime import datetime, timedelta

def julian_date_to_datetime(jd):
    jd = jd + 0.5
    z = math.floor(jd)
    f = jd - z
    if z < 2299161:
        a = z
    else:
        alpha = math.floor((z - 1867216.25) / 36524.25)
        a = z + 1 + alpha - math.floor(alpha / 4)
    b = a + 1524
    c = math.floor((b - 122.1) / 365.25)
    d = math.floor(365.25 * c)
    e = math.floor((b - d) / 30.6001)
    day = b - d - math.floor(30.6001 * e) + f
    if e < 14:
        month = e - 1
    else:
        month = e - 13
    if month > 2:
        year = c - 4716
    else:
        year = c - 4715
    hours = (day - math.floor(day)) * 24
    minutes = (hours - math.floor(hours)) * 60
    seconds = (minutes - math.floor(minutes)) * 60
    microseconds = (seconds - math.floor(seconds)) * 1000000
    day = int(math.floor(day))
    hours = int(math.floor(hours))
    minutes = int(math.floor(minutes))
    seconds = int(math.floor(seconds))
    microseconds = int(round(microseconds))
    date = datetime(year, month, day, hours, minutes, seconds, microseconds)
    return date

import os
import time
import re
from datetime import datetime
import pandas as pd
from haversine import haversine, Unit

# Operations
# operator functions
def distance(loc1, loc2, units=Unit.METERS):
    d = haversine(loc1, loc2, unit=units)
    return d

def delta_t(t1,t2):
    dt = (t2 - t1).seconds  # difference in time in seconds
    return dt

def sys_delta_t(t):
    timestamp = pd.Timestamp(datetime.utcnow(), tz='UTC').tz_convert(None)
    dt = delta_t(t, timestamp)
    return dt

def v_diff(v1, v2):
    dv = v2 - v1
    return dv

def t_diff(tmp1, tmp2):
    dtmp = tmp2 - tmp1
    return dtmp

def ddm2dec(dms_str):
    """Return decimal representation of DDM (degree decimal minutes)

    >>> ddm2dec("45° 17,896' N")
    48.8866111111F
    """

    dms_str = re.sub(r'\s', '', dms_str)

    sign = -1 if re.search('[swSW]', dms_str) else 1

    numbers = [*filter(len, re.split('\D+', dms_str, maxsplit=4))]

    degree = numbers[0]
    minute_decimal = numbers[1]
    decimal_val = numbers[2] if len(numbers) > 2 else '0'
    minute_decimal += "." + decimal_val

    return round(sign * (int(degree) + float(minute_decimal) / 60), 6)

def dec2dms(deg, pretty_print=None, ndp=4):
    """Convert from decimal degrees to degrees, minutes, seconds."""

    m, s = divmod(abs(deg)*3600, 60)
    d, m = divmod(m, 60)
    if deg < 0:
        d = -d
    d, m = int(d), int(m)

    if pretty_print:
        if pretty_print=='latitude':
            hemi = 'N' if d>=0 else 'S'
        elif pretty_print=='longitude':
            hemi = 'E' if d>=0 else 'W'
        else:
            hemi = '?'
        return '{d:d}° {m:d}′ {s:.{ndp:d}f}″ {hemi:1s}'.format(
                    d=abs(d), m=m, s=s, hemi=hemi, ndp=ndp)
    return d, m, s


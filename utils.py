"""
Core mathematical utilities for Ethiopian and Gregorian calendar conversions.
Uses Julian Day Numbers (JDN) as an intermediary.
"""

# constants for Ethiopian Calendar (EC)
EC_EPOCH_JDN = 1724221  # JDN of Meskerem 1, 1 EC


def ec_to_jdn(year: int, month: int, day: int) -> int:
    """
    Converts Ethiopian date to Julian Day Number (JDN).
    
    Formula based on the 4-year cycle where every 4th year is leap.
    """
    return (
        EC_EPOCH_JDN
        + (year - 1) * 365
        + ((year - 1) // 4)
        + (month - 1) * 30
        + day
        - 1
    )


def jdn_to_ec(jdn: int) -> tuple[int, int, int]:
    """
    Converts Julian Day Number (JDN) to Ethiopian date (year, month, day).
    """
    r = jdn - EC_EPOCH_JDN
    n = r // 1461
    r %= 1461
    
    # handle the leap year day (last day of the 4-year cycle)
    y_in_cycle = min(r // 365, 3)
    d_in_year = r - (y_in_cycle * 365)
    
    year = 4 * n + y_in_cycle + 1
    month = (d_in_year // 30) + 1
    day = (d_in_year % 30) + 1
    
    return year, month, day


def gc_to_jdn(year: int, month: int, day: int) -> int:
    """
    Converts Gregorian date to Julian Day Number (JDN).
    Standard algorithm from Peter Baum, "Date Algorithms".
    """
    a = (14 - month) // 12
    y = year + 4800 - a
    m = month + 12 * a - 3
    return day + (153 * m + 2) // 5 + 365 * y + y // 4 - y // 100 + y // 400 - 32045


def jdn_to_gc(jdn: int) -> tuple[int, int, int]:
    """
    Converts Julian Day Number (JDN) to Gregorian date (year, month, day).
    """
    f = jdn + 1401 + (((4 * jdn + 274277) // 146097) * 3) // 4 - 38
    e = 4 * f + 3
    g = (e % 1461) // 4
    h = 5 * g + 2
    day = (h % 153) // 5 + 1
    month = ((h // 153 + 2) % 12) + 1
    year = e // 1461 - 4716 + (14 - month) // 12
    return year, month, day

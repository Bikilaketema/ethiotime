from datetime import date
from typing import Union
import utils


class CalendarService:
    """
    Service for Ethiopian and Gregorian calendar conversions.
    """

    @staticmethod
    def is_ec_leap_year(year: int) -> bool:
        """
        Determines if an Ethiopian year is a leap year (Pagume has 6 days).
        Rule: A year is a leap year if it's divisible by 4.
        """
        return year % 4 == 0

    @staticmethod
    def _validate_ec_date(year: int, month: int, day: int):
        """
        Validates Ethiopian date parameters.
        Raises ValueError if any parameter is out of range or invalid.
        """
        if not all(isinstance(x, int) for x in [year, month, day]):
            raise ValueError("Year, month, and day must be integers.")

        if month < 1 or month > 13:
            raise ValueError(f"Month must be between 1 and 13. Got {month}.")

        if month <= 12:
            if day < 1 or day > 30:
                raise ValueError(f"Day must be between 1 and 30 for month {month}. Got {day}.")
        else:
            # Pagume (month 13)
            max_days = 6 if CalendarService.is_ec_leap_year(year) else 5
            if day < 1 or day > max_days:
                raise ValueError(
                    f"Day must be between 1 and {max_days} for Pagume in year {year}. Got {day}."
                )

    @staticmethod
    def ec_to_gc(year: int, month: int, day: int) -> date:
        """
        Converts an Ethiopian date to a Gregorian date.
        
        Args:
            year: Ethiopian year (Amete Mihret)
            month: Ethiopian month (1-13)
            day: Ethiopian day (1-30 or 1-6 for Pagume)
            
        Returns:
            datetime.date object (Gregorian calendar)
        """
        CalendarService._validate_ec_date(year, month, day)
        jdn = utils.ec_to_jdn(year, month, day)
        y, m, d = utils.jdn_to_gc(jdn)
        return date(y, m, d)

    @staticmethod
    def gc_to_ec(g_date: Union[date, str]) -> tuple[int, int, int]:
        """
        Converts a Gregorian date to an Ethiopian date.
        
        Args:
            g_date: datetime.date object or ISO string (YYYY-MM-DD)
            
        Returns:
            tuple[int, int, int]: (year, month, day) in Ethiopian calendar
        """
        if isinstance(g_date, str):
            try:
                g_date = date.fromisoformat(g_date)
            except ValueError:
                raise ValueError("String input must be in YYYY-MM-DD format.")
        
        if not isinstance(g_date, date):
            raise ValueError("Input must be a datetime.date object or ISO string.")
            
        jdn = utils.gc_to_jdn(g_date.year, g_date.month, g_date.day)
        return utils.jdn_to_ec(jdn)

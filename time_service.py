from . import utils

class TimeService:
    """
    Service for Ethiopian and Standard time conversions.
    Ethiopian time begins at 6 AM (06:00) standard time.
    """

    @staticmethod
    def standard_to_ethiopian(hour: int) -> int:
        """
        Converts standard hour (0-23) to Ethiopian hour (1-12).
        
        Rule: Ethiopian hour = (standard hour - 6) mod 12
        """
        if not isinstance(hour, int):
             raise ValueError("Hour must be an integer.")
        if hour < 0 or hour > 23:
            raise ValueError(f"Standard hour must be between 0 and 23. Got {hour}.")

        eth_hour = (hour - 6) % 12
        return 12 if eth_hour == 0 else eth_hour

    @staticmethod
    def ethiopian_to_standard(hour: int) -> int:
        """
        Converts Ethiopian hour (1-12) to standard hour (1-12).
        The result is the standard 12-hour clock representation.
        
        Rule: Standard hour = (Ethiopian hour + 6) mod 12
        """
        if not isinstance(hour, int):
             raise ValueError("Hour must be an integer.")
        if hour < 1 or hour > 12:
            raise ValueError(f"Ethiopian hour must be between 1 and 12. Got {hour}.")

        std_12_hour = (hour + 6) % 12
        return 12 if std_12_hour == 0 else std_12_hour

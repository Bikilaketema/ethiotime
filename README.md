# ethiotime

A production-ready, pure-Python library for Ethiopian calendar and time conversions. Designed for accuracy, reliability, and ease of use in any Python project (including FastAPI).

## Features

- **Robust Calendar Conversion**: Bi-directional conversion between Ethiopian (Amete Mihret) and Gregorian calendars.
- **Leap Year Support**: Handles the Ethiopian 4-year cycle, including the 6-day Pagume month.
- **Ethiopian Time Conversion**: Converts standard 24-hour time to the 12-hour Ethiopian system (where the day starts at 6 AM).
- **Production-Grade Validation**: Strict type checking and value range validation for all inputs.
- **Zero Dependencies**: Pure Python implementation with no external requirements.

## Installation

### From PyPI
```bash
pip install ethiotime
```

### Local Development
To use the library locally or contribute to it:
```bash
git clone https://github.com/TODO/ethiotime.git
cd ethiotime
pip install -e .
```

## Publishing to PyPI

To publish a new version of the library:

1.  **Build the package**:
    ```bash
    python3 -m pip install --upgrade build
    python3 -m build
    ```
2.  **Upload to PyPI** (requires a PyPI account):
    ```bash
    python3 -m pip install --upgrade twine
    python3 -m twine upload dist/*
    ```

## Usage

### Calendar Conversion

```python
from datetime import date
from ethiotime import CalendarService

# Ethiopian to Gregorian
# Example: Meskerem 1, 2017 EC
g_date = CalendarService.ec_to_gc(2017, 1, 1)
print(g_date)  # 2024-09-11

# Gregorian to Ethiopian
# Supports datetime.date objects or ISO strings (YYYY-MM-DD)
e_date_1 = CalendarService.gc_to_ec(date(2024, 9, 11))
e_date_2 = CalendarService.gc_to_ec("2024-09-11")

print(e_date_1)  # (2017, 1, 1)
print(e_date_2)  # (2017, 1, 1)
```

### Time Conversion

```python
from ethiotime import TimeService

# Standard Hour (0-23) to Ethiopian Hour (1-12)
# 6 AM (06:00) standard time is 12:00 in Ethiopia
eth_hour = TimeService.standard_to_ethiopian(6)
print(eth_hour)  # 12

# Ethiopian Hour (1-12) to Standard 12-hour clock
# 12:00 Ethiopian is 6:00 standard
std_hour = TimeService.ethiopian_to_standard(12)
print(std_hour)  # 6
```

## Validation & Edge Cases

The library strictly validates all inputs:
- Month must be 1-13.
- Pagume (Month 13) is validated as 5 days for regular years and 6 days for leap years.
- Standard hours must be 0-23.
- Ethiopian hours must be 1-12.
- All inputs must be integers; otherwise, a `ValueError` is raised.

## Testing

To run the exhaustive test suite:

```bash
python3 -m unittest discover ethiotime/tests
```

## License

MIT

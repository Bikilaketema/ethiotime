import unittest
from datetime import date
from ..calendar_service import CalendarService


class TestCalendarService(unittest.TestCase):
    def test_ec_to_gc_conversions(self):
        # EC 2016-01-01 -> GC 2023-09-11
        self.assertEqual(CalendarService.ec_to_gc(2016, 1, 1), date(2023, 9, 11))
        
        # EC 2016-13-06 (leap Pagume) -> GC 2024-09-10
        self.assertEqual(CalendarService.ec_to_gc(2016, 13, 6), date(2024, 9, 10))

        # EC 2017-01-01 -> GC 2024-09-11
        self.assertEqual(CalendarService.ec_to_gc(2017, 1, 1), date(2024, 9, 11))

        # EC 2015-13-05 (end of year edge) -> GC 2023-09-10
        self.assertEqual(CalendarService.ec_to_gc(2015, 13, 5), date(2023, 9, 10))

        # EC 2019-01-01 -> GC 2026-09-11 (Meskerem 1 in year following non-leap)
        self.assertEqual(CalendarService.ec_to_gc(2019, 1, 1), date(2026, 9, 11))

    def test_gc_to_ec_conversions(self):
        # GC 2023-09-11 -> EC 2016-01-01
        self.assertEqual(CalendarService.gc_to_ec(date(2023, 9, 11)), (2016, 1, 1))
        
        # GC 2024-09-10 -> EC 2016-13-06
        self.assertEqual(CalendarService.gc_to_ec(date(2024, 9, 10)), (2016, 13, 6))

        # GC 2024-09-11 -> EC 2017-01-01
        self.assertEqual(CalendarService.gc_to_ec(date(2024, 9, 11)), (2017, 1, 1))

        # Test string input support
        self.assertEqual(CalendarService.gc_to_ec("2024-09-11"), (2017, 1, 1))

    def test_round_trip_conversions(self):
        # Round trip EC -> GC -> EC
        test_dates = [(2016, 1, 1), (2016, 13, 6), (2017, 1, 1), (2015, 13, 5)]
        for year, month, day in test_dates:
            g_date = CalendarService.ec_to_gc(year, month, day)
            e_year, e_month, e_day = CalendarService.gc_to_ec(g_date)
            self.assertEqual((year, month, day), (e_year, e_month, e_day))

        # Round trip GC -> EC -> GC
        test_dates_gc = [date(2023, 9, 11), date(2024, 9, 10), date(2024, 9, 11)]
        for g_date in test_dates_gc:
            e_year, e_month, e_day = CalendarService.gc_to_ec(g_date)
            g_date_back = CalendarService.ec_to_gc(e_year, e_month, e_day)
            self.assertEqual(g_date, g_date_back)

    def test_month_boundaries_and_transitions(self):
        # EC 2016-12-30 -> next month (Pagume 1)
        g_current = CalendarService.ec_to_gc(2016, 12, 30)
        g_next = CalendarService.ec_to_gc(2016, 13, 1)
        self.assertEqual((g_next - g_current).days, 1)

        # EC 2016-13-06 (Leap Pagume) -> next month (Meskerem 1 2017)
        g_current = CalendarService.ec_to_gc(2016, 13, 6)
        g_next = CalendarService.ec_to_gc(2017, 1, 1)
        self.assertEqual((g_next - g_current).days, 1)

    def test_leap_year_validation(self):
        # 2015 EC is not a leap year (Pagume has 5 days)
        self.assertFalse(CalendarService.is_ec_leap_year(2015))
        # Valid: Pagume 5, 2015
        CalendarService.ec_to_gc(2015, 13, 5)
        # Invalid: Pagume 6, 2015
        with self.assertRaises(ValueError):
            CalendarService.ec_to_gc(2015, 13, 6)
            
        # 2016 EC is a leap year (Pagume has 6 days)
        self.assertTrue(CalendarService.is_ec_leap_year(2016))
        # Valid: Pagume 6, 2016
        CalendarService.ec_to_gc(2016, 13, 6)
        # Invalid: Pagume 7, 2016
        with self.assertRaises(ValueError):
            CalendarService.ec_to_gc(2016, 13, 7)

    def test_invalid_date_validation(self):
        # Month 0
        with self.assertRaises(ValueError):
            CalendarService.ec_to_gc(2016, 0, 1)
        # Month 14
        with self.assertRaises(ValueError):
            CalendarService.ec_to_gc(2016, 14, 1)
        # Day 0
        with self.assertRaises(ValueError):
            CalendarService.ec_to_gc(2016, 1, 0)
        # Day 31 in a 30-day month
        with self.assertRaises(ValueError):
            CalendarService.ec_to_gc(2016, 1, 31)

    def test_type_validation(self):
        val_errors = [
            ("2016", 1, 1),
            (2016, "1", 1),
            (2016, 1, "1"),
            (2016, 1.5, 1),
            (None, 1, 1),
            (2016, None, 1),
            (2016, 1, None)
        ]
        for y, m, d in val_errors:
            with self.subTest(y=y, m=m, d=d):
                with self.assertRaises(ValueError):
                    CalendarService.ec_to_gc(y, m, d)

        # GC to EC type check
        with self.assertRaises(ValueError):
            CalendarService.gc_to_ec("invalid-date-format")
        with self.assertRaises(ValueError):
            CalendarService.gc_to_ec(None)


if __name__ == "__main__":
    unittest.main()

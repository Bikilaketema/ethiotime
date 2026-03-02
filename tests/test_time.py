import unittest
from time_service import TimeService


class TestTimeService(unittest.TestCase):
    def test_standard_to_ethiopian(self):
        # std 6 -> eth 12
        self.assertEqual(TimeService.standard_to_ethiopian(6), 12)
        # std 5 -> eth 11
        self.assertEqual(TimeService.standard_to_ethiopian(5), 11)
        # std 18 -> eth 12
        self.assertEqual(TimeService.standard_to_ethiopian(18), 12)
        # std 0 -> eth 6
        self.assertEqual(TimeService.standard_to_ethiopian(0), 6)

    def test_full_24h_cycle(self):
        """Test every hour in a 24h day for wrap-around consistency."""
        # Mapping: (Standard 24h) -> (Ethiopian 1-12)
        # 0->6, 1->7, 2->8, 3->9, 4->10, 5->11, 6->12, 7->1, 8->2, 9->3, 10->4, 11->5,
        # 12->6, 13->7, 14->8, 15->9, 16->10, 17->11, 18->12, 19->1, 20->2, 21->3, 22->4, 23->5
        expected_mapping = {
            0: 6, 1: 7, 2: 8, 3: 9, 4: 10, 5: 11, 6: 12, 7: 1, 8: 2, 9: 3, 10: 4, 11: 5,
            12: 6, 13: 7, 14: 8, 15: 9, 16: 10, 17: 11, 18: 12, 19: 1, 20: 2, 21: 3, 22: 4, 23: 5
        }
        for std, eth in expected_mapping.items():
            with self.subTest(std=std):
                self.assertEqual(TimeService.standard_to_ethiopian(std), eth)

    def test_reversibility(self):
        """Ensure standard -> Ethiopian -> standard (12h basis) returns original."""
        for std in range(24):
            eth = TimeService.standard_to_ethiopian(std)
            std_back = TimeService.ethiopian_to_standard(eth)
            # eth_to_std returns 1-12, so we compare with std % 12 (adjusting 0 to 12)
            expected_12h = std % 12
            if expected_12h == 0: expected_12h = 12
            self.assertEqual(std_back, expected_12h)

    def test_ethiopian_to_standard_wrap(self):
        # eth 1 -> std 7
        self.assertEqual(TimeService.ethiopian_to_standard(1), 7)
        # eth 12 -> std 6
        self.assertEqual(TimeService.ethiopian_to_standard(12), 6)
        # eth 6 -> std 12
        self.assertEqual(TimeService.ethiopian_to_standard(6), 12)

    def test_invalid_input(self):
        # Standard hour out of range
        with self.assertRaises(ValueError):
            TimeService.standard_to_ethiopian(24)
        with self.assertRaises(ValueError):
            TimeService.standard_to_ethiopian(-1)
            
        # Ethiopian hour out of range
        with self.assertRaises(ValueError):
            TimeService.ethiopian_to_standard(13)
        with self.assertRaises(ValueError):
            TimeService.ethiopian_to_standard(0)

    def test_type_validation(self):
        val_errors = ["6", 6.5, None]
        for val in val_errors:
            with self.subTest(val=val):
                with self.assertRaises(ValueError):
                    TimeService.standard_to_ethiopian(val)
                with self.assertRaises(ValueError):
                    TimeService.ethiopian_to_standard(val)


if __name__ == "__main__":
    unittest.main()

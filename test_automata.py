import unittest

from automata import TimeDFA, TimeNFA


class TestTimeDFA(unittest.TestCase):
    def test_valid_times(self):
        for value in ("00:00", "09:30", "12:45", "23:59"):
            self.assertTrue(TimeDFA().simulate(value).accepted, value)

    def test_invalid_times(self):
        for value in ("9:30", "24:00", "12:60", "12-30", "09:300", ""):
            self.assertFalse(TimeDFA().simulate(value).accepted, value)


class TestTimeNFA(unittest.TestCase):
    def test_valid_times(self):
        for value in ("01:00 AM", "09:30 pm", "11:59 PM", "12:45 AM"):
            self.assertTrue(TimeNFA().simulate(value).accepted, value)

    def test_invalid_times(self):
        for value in ("1:00 AM", "00:00 AM", "13:00 PM", "12:60 PM", "09:30", ""):
            self.assertFalse(TimeNFA().simulate(value).accepted, value)


if __name__ == "__main__":
    unittest.main()

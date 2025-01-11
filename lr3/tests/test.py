import unittest
from lr3.Paket.getweatherdata import utc_timezone

class TestWeatherData(unittest.TestCase):
    def test_utc_offset(self):
        self.assertEqual(utc_timezone(3600), 'UTC+1')
        self.assertEqual(utc_timezone(-7200), 'UTC-2')

if __name__ == '__main__':
    unittest.main()

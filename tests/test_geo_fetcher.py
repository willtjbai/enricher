from unittest import TestCase

from enricher.geo_fetcher import get_country_from_ips


class TestGeoFetcher(TestCase):
    def test_get_country_from_ips(self):
        # Test case for normal ip
        self.assertEqual(get_country_from_ips('104.193.9.182'), ['The Netherlands'], 'Not able to fetch country')
        # Test case for invalid ip
        with self.assertRaises(Exception):
            get_country_from_ips('0.0.0.0')

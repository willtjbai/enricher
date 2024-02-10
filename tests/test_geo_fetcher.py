from unittest import TestCase

from enricher.geo_fetcher import get_country_from_ips


class TestGeoFetcher(TestCase):
    def test_get_country_from_ips(self):
        self.assertEqual(get_country_from_ips('104.193.9.182'), ['The Netherlands'], 'Not able to fetch country')

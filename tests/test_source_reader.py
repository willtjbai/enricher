import os
import pathlib
from unittest import TestCase

from enricher.model import Ip2CountryTask
from enricher.source_reader import CsvSource


class TestCsvSource(TestCase):
    def test_read_source(self):
        self.assertEqual(
            CsvSource(file_path=os.path.dirname(os.path.realpath(__file__))+'/../resources/sample_input.csv',
                      required_columns=("id", "ip")).read_source(),
            None,
            "Should return None when any required column is not presented")
        self.assertEqual(
            CsvSource(file_path=os.path.dirname(os.path.realpath(__file__))+'/../resources/sample_input.csv',
                      required_columns=("user_id", "ip_address")).read_source(),
            [Ip2CountryTask("1", "10.1.111.123"), Ip2CountryTask("3", "104.193.9.182")],
            "Should only return rows with valid IP format")

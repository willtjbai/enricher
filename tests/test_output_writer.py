import csv
from unittest import TestCase
import tempfile

from enricher.model import *
from enricher.output_writer import CsvWriter


class TestCsvWriter(TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_write_output(self):
        file_path = self.temp_dir.name + "/temp.csv"
        writer = CsvWriter(path=file_path)
        flag = writer.write_output([Result("1", "NL")])
        self.assertTrue(flag, "Failed to write CSV")

        # Check written content of the CSV
        with open(file_path, 'r') as f:
            reader = list(csv.DictReader(f))
            self.assertEqual(len(reader), 1, "Csv count not match")
            self.assertEqual(reader[0]['uid'], "1", "Written Id not match")
            self.assertEqual(reader[0]['country'], "NL", "Written Country not match")

        self.assertFalse(writer.write_output([]), "Should return False when output is empty")

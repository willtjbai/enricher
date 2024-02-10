import csv
import logging
import os
from abc import ABC, abstractmethod


class BaseWriter(ABC):
    """
    Base writer, new writer should extend this class
    """
    @abstractmethod
    def write_output(self, output: list) -> bool:
        pass

    @abstractmethod
    def destination_location(self):
        pass


class CsvWriter(BaseWriter):
    """
    CSV writer, write a list of object to CSV file
    """
    def __init__(self, path: str):
        self.path = path

    def write_output(self, output: list) -> bool:
        try:
            if output:
                self._write_csv_file(output)
                return True
            else:
                raise Exception("Output list is empty!")
        except Exception as e:
            logging.error(f"Error writing CSV to output path: {e}")
            return False

    def destination_location(self):
        return os.path.abspath(self.path)

    def _write_csv_file(self, output):
        if not os.path.exists(os.path.dirname(self.path)):
            os.makedirs(os.path.dirname(self.path))
        with open(self.path, "w", newline="") as file:
            writer = csv.writer(file)
            # Write the header row
            writer.writerow(list(output[0].__dict__.keys()))

            for item in output:
                writer.writerow(list(item.__dict__.values()))

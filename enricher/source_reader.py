import csv
import logging
import os
from abc import ABC, abstractmethod
from typing import Optional

from enricher.model import Ip2CountryTask
from enricher.utils import *


class DataSource(ABC):
    """
    Source reader, new source should extend DataSource
    """
    @abstractmethod
    def read_source(self) -> Optional[list]:
        pass

    @abstractmethod
    def del_source(self):
        """
        Delete the source file to avoid storing PII
        """
        pass

    @abstractmethod
    def source_location(self):
        pass


class CsvSource(DataSource):
    def __init__(self, file_path, required_columns):
        super().__init__()
        self.file_path = file_path
        self.required_columns = required_columns

    def read_source(self) -> Optional[list]:
        tasks = None
        try:
            tasks = list(map(lambda t: Ip2CountryTask(t[0], t[1]), self._read_csv()))
        except Exception as e:
            logging.error(f"Fail to read source data: {e}")
        finally:
            return tasks

    def del_source(self):
        if os.path.exists(self.file_path):
            os.remove(self.file_path)

    def source_location(self):
        return os.path.abspath(self.file_path)

    def _read_csv(self) -> Optional[list[tuple[str, str]]]:
        valid_rows = []
        with open(self.file_path, 'r') as f:
            reader = csv.DictReader(f, skipinitialspace=True)
            if not set(self.required_columns).issubset(set(reader.fieldnames)):
                raise Exception(
                    f"Missing required columns in the CSV file. Columns required: {str(self.required_columns)}, exist columns: {str(reader.fieldnames)}")

            for row in reader:
                # noinspection PyTypeChecker
                uid, ip = row['user_id'], row['ip_address']
                if is_valid_ip_address(ip):
                    valid_rows.append((uid, ip))
                else:
                    write_failed_row(uid, 'Invalid ip format')
        return valid_rows

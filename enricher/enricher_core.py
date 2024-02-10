import logging
import os

from enricher.output_writer import BaseWriter, CsvWriter
from enricher.source_reader import DataSource, CsvSource
from enricher.utils import parse_args


def enrich_data(source: DataSource, writer: BaseWriter, del_source: bool):
    # 1. Read id and ip into task list
    ip_tasks = source.read_source()
    logging.info(f"Starting {len(ip_tasks)} tasks from source {source.source_location()}")
    logging.debug(f"Tasks: {ip_tasks}")
    # 2. Enrich country info
    id_country = list(filter(None, map(lambda t: t.execute(), ip_tasks)))
    logging.info(f"Finish getting country from {len(id_country)} tasks")
    logging.debug(f"Result: {id_country}")
    # 3. Export id + enriched information
    write_success = writer.write_output(id_country)
    # 4. Delete source file
    if write_success:
        logging.info(f"Successfully write output to {writer.destination_location()}")
        if del_source:
            source.del_source()
        return True
    else:
        logging.warning("Failed to enrich resources, please check logging for details")
        return False


def main():
    args = parse_args()
    cur_path = os.path.dirname(os.path.realpath(__file__))
    log_level = args.loglevel if args.loglevel else 'INFO'
    input_file_path = args.file if args.file else cur_path + '/../resources/sample_input.csv'
    output_file_path = args.output if args.output else cur_path + '/../out/enriched_data_output.csv'
    del_flag = bool(args.file)

    logging.basicConfig(level=log_level,
                        format='%(asctime)s %(levelname)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')

    # Enrich data from CSV source and write to CSV
    enrich_data(source=CsvSource(file_path=input_file_path,
                                 required_columns=("user_id", "ip_address")),
                writer=CsvWriter(path=output_file_path),
                del_source=del_flag)

    logging.info("Finish")


if __name__ == '__main__':
    main()

import ipaddress
import os
import re
from datetime import datetime


def is_valid_ip_address(address):
    try:
        ipaddress.ip_address(address)
        return True
    except ValueError:
        return False


def write_failed_row(uid, msg, path=os.path.dirname(os.path.realpath(__file__))+'/../out/failed_rows.log'):
    if not os.path.exists(os.path.dirname(path)):
        os.makedirs(os.path.dirname(path))
    with open(path, 'a') as error_file:
        time = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
        error_file.write(f"{time}, User_id: {uid}, error msg: {mask_ip(msg)}\n")


def mask_ip(text):
    # Define the regex pattern to identify IP addresses
    ip_pattern = r"((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)"
    return re.sub(ip_pattern, "**********", text)


def parse_args():
    import argparse
    # Parse the arguments
    parser = argparse.ArgumentParser(description="Data enricher")
    parser.add_argument('-f', '--file', help="Input file")
    parser.add_argument('-o', '--output', help="Output file")
    parser.add_argument('-ll', '--loglevel', help="Log level")
    return parser.parse_args()

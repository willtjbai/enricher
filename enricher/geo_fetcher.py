import logging

import geoip2.webservice
import geoip2.errors
import os
from dotenv import load_dotenv

load_dotenv()
_account = os.getenv('ACCOUNT_ID')
_api_key = os.getenv('LICENSE_KEY')


def get_country_from_ips(*ips) -> list:
    with geoip2.webservice.Client(int(_account), _api_key, host='geolite.info') as client:
        return list(map(lambda ip: client.country(ip).country.name, ips))


# Test
if __name__ == '__main__':
    print(get_country_from_ips("104.193.9.182"))

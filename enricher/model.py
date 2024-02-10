from enricher.geo_fetcher import get_country_from_ips
from enricher.utils import write_failed_row


class BaseTask(object):

    def __init__(self, uid):
        self.uid = uid

    def execute(self):
        pass


class Ip2CountryTask(BaseTask):
    def __init__(self, uid, ip):
        super().__init__(uid)
        self.ip = ip

    def execute(self):
        try:
            c = get_country_from_ips(self.ip)
            if c:
                return Result(self.uid, c[0])
            else:
                raise Exception(f"Failed to get country for {self.uid}")
        except Exception as e:
            write_failed_row(self.uid, f"Failed to get country from ip {e}")
            return None

    def __repr__(self):
        ip = self.ip
        # Find the index of the second dot ('.') in the string
        second_dot_index = ip.find('.', ip.find('.') + 1) + 1
        first_half = ip[:second_dot_index]
        second_half = ip[second_dot_index:]
        return (f"Ip2CountryTask(uid={self.uid}, "
                f"ip={first_half}{''.join('*' if char != '.' else char for char in second_half)}")

    def __eq__(self, other):
        return self.uid == other.uid and self.ip == other.ip

class Result(object):
    def __init__(self, uid, country):
        self.uid = uid
        self.country = country

    def __repr__(self):
        return f"Result(uid={self.uid}, country={self.country})"
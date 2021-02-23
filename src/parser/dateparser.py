from datetime import datetime
from time import struct_time, strftime


class DateParser(object):

    DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

    @classmethod
    def parse_datetime(cls, date: datetime):
        return date.strftime(cls.DATE_FORMAT)

    @classmethod
    def parse_struct_time(cls, date: struct_time):
        return strftime(cls.DATE_FORMAT, date)

from datetime import datetime
from time import struct_time, strftime
from multipledispatch import dispatch


class DateParser(object):

    DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

    @classmethod
    @dispatch(type, datetime)
    def parse(cls, date: datetime):
        return date.strftime(cls.DATE_FORMAT)

    @classmethod
    @dispatch(type, struct_time)
    def parse(cls, date: struct_time):
        return strftime(cls.DATE_FORMAT, date)

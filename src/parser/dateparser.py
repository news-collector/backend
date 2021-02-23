from datetime import datetime


class DateParser(object):

    DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

    @classmethod
    def parse(cls, date: datetime):
        return date.strftime(cls.DATE_FORMAT)

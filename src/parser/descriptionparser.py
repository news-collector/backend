
class DescriptionParser(object):

    @classmethod
    def parse(cls, description: str):
        return description.split(sep="<", maxsplit=1)[0]

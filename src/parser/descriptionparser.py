
class DescriptionParser(object):

    @classmethod
    def parse(cls, description: str):
        return cls.__trim_html_tags_from_right(description)

    @classmethod
    def __trim_html_tags_from_right(cls, string: str):
        return string.split(sep="<", maxsplit=1)[0]


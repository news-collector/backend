from PyDictionary import PyDictionary as PyDict


class SynonymsUtil(object):

    def __init__(self):
        self.__py_dict = PyDict()

    def find_synonyms(self, word: str, synonyms_count: int = 5):
        synonyms = self.__py_dict.synonym(word)
        return [word] + synonyms[:synonyms_count] if synonyms is not None else [word]

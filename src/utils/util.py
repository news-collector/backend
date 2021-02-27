import os
import sys

from PyDictionary import PyDictionary as PyDict


class SynonymsUtil(object):

    def __init__(self):
        self.__py_dict = PyDict()

    def find_synonyms(self, word: str, synonyms_count: int = 5):
        with HiddenPrints():
            synonyms = self.__py_dict.synonym(word)
            return [word] + synonyms[:synonyms_count] if synonyms is not None else [word]


class HiddenPrints:
    def __enter__(self):
        self._original_stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.close()
        sys.stdout = self._original_stdout

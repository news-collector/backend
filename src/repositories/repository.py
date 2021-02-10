from abc import ABC
from src.configs import db_config
import mysql.connector as mysql


class Repository(ABC):

    def __init__(self):
        self.__db_config = db_config.config
        self._connection = mysql.connect(**self.__db_config)
        self._cursor = self._connection.cursor(dictionary=True, buffered=True)

from src.configs import db_config
import mysql.connector as mysql


class Repository(object):

    def __init__(self):
        self.__db_config = db_config.config
        self._connection = mysql.connect(**self.__db_config)
        self._cursor = self._connection.cursor(dictionary=True, buffered=True)


class WebsiteRepository(Repository):

    def __init__(self):
        super().__init__()


class NewsRepository(Repository):

    def __init__(self):
        super().__init__()

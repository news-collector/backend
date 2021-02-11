from mysql.connector import MySQLConnection
from mysql.connector.cursor import MySQLCursor

from src.configs import db_config
import mysql.connector as mysql


class Repository(object):

    def __init__(self):
        self._connection: MySQLConnection = mysql.connect(**db_config.config)
        self._cursor: MySQLCursor = self._connection.cursor(dictionary=True, buffered=True)


class WebsiteRepository(Repository):
    pass


class NewsRepository(Repository):
    pass


class FeedRepository(Repository):
    pass

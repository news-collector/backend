from copy import deepcopy
from dataclasses import asdict

from mysql.connector import MySQLConnection
from mysql.connector.cursor import MySQLCursor

from src.configs import db_config
import mysql.connector as mysql
from src.models.entities import WebsiteEntity, NewsEntity, FeedEntity, UserEntity
from pypika import Table, Field, MySQLQuery as Query
from pypika.dialects import QueryBuilder
from mysql.connector.errors import Error as DBError
import logging
from typing import List, Dict, Type

logging.getLogger().setLevel(logging.INFO)

websites = Table('websites')
news = Table('news')
feeds = Table('rss_feeds')
users = Table('users')


def make_fields(table: Table, column_names: List[str]) -> List[Field]:
    return [table.field(name) for name in column_names]


def query_to_str(query: QueryBuilder, remove_double_quote_mark=True):
    return str(query).replace('"', '') if remove_double_quote_mark else str(query)


class Repository(object):

    def __init__(self, table: Table, fields: Dict[str, Field], entity: Type):
        self._connection: MySQLConnection = mysql.connect(**db_config.config)
        self._cursor: MySQLCursor = self._connection.cursor(dictionary=True, buffered=True)
        self._table = table
        self._fields = fields
        self._entity = entity

    def get_by_id(self, _id: int):
        bare_query = Query.from_(self._table).select(self._table.star).where(self._fields['id'] == _id)
        query = query_to_str(bare_query)

        record = None

        try:
            self._cursor.execute(query)
            record = self._cursor.fetchone()
        except DBError as e:
            logging.error(f"Repository [{self._table}]: get_by_id -> [{e.errno}]{e.msg}")
        else:
            if record:
                record = self._entity(**record)
            logging.info(f"Repository [{self._table}]: get_by_id -> Record for id={_id} is {record}")

        return record

    def get_all(self):
        bare_query = Query.from_(self._table).select(self._table.star)
        query = query_to_str(bare_query)

        records = None

        try:
            self._cursor.execute(query)
            records = self._cursor.fetchall()
        except DBError as e:
            logging.error(f"Repository [{self._table}]: get_all -> [{e.errno}]{e.msg}")
        else:
            if records:
                records = [self._entity(**record) for record in records]
            logging.info(f"Repository [{self._table}]: get_all -> Found {len(records)} records")

        return records

    def delete_by_id(self, _id: int) -> int:
        bare_query = Query.from_(self._table).delete().where(self._fields['id'] == _id)
        query = query_to_str(bare_query)

        rows_count = 0

        try:
            self._cursor.execute(query)
        except DBError as e:
            logging.error(f"Repository [{self._table}]: delete_by_id -> [{e.errno}]{e.msg}")
            self._connection.rollback()
        else:
            self._connection.commit()
            rows_count = self._cursor.rowcount
            logging.info(f"Repository [{self._table}]: delete_by_id -> Deleted record with id = {_id}")

        return rows_count

    def delete_all(self) -> int: # TODO check
        bare_query = Query.from_(self._table).delete().where(self._fields['id'] > 0)
        query = query_to_str(bare_query)

        rows_count = 0

        try:
            self._cursor.execute(query)
        except DBError as e:
            logging.error(f"Repository [{self._table}]: delete_by_id -> [{e.errno}]{e.msg}")
            self._connection.rollback()
        else:
            self._connection.commit()
            rows_count = self._cursor.rowcount
            logging.info(f"Repository [{self._table}]: delete_by_id -> Deleted {rows_count} record/s")

        return rows_count

    def save(self, entity):
        dict_copy = deepcopy(self._fields)
        dict_copy.pop('id')

        entity_as_dict = asdict(entity)
        entity_values = [entity_as_dict[key] for key in entity_as_dict if key in dict_copy]

        bare_query = Query.into(self._table).columns(*dict_copy.values()).insert(*entity_values)
        query = query_to_str(bare_query)

        entity_id = None

        try:
            self._cursor.execute(query)
        except DBError as e:
            logging.error(f"Repository [{self._table}]: save -> [{e.errno}]{e.msg}")
            self._connection.rollback()
        else:
            self._connection.commit()
            entity_id = self._cursor.lastrowid
            logging.info(f"Repository [{self._table}]: save -> Saved {entity} with id={entity_id}")

        return entity_id


class WebsiteRepository(Repository):

    def __init__(self):
        field_list = make_fields(websites, list(WebsiteEntity.__annotations__.keys()))
        field_dict = {field.name: field for field in field_list}
        field_dict['id'] = field_dict.pop('website_id')
        super().__init__(websites, field_dict, WebsiteEntity)


class NewsRepository(Repository):

    def __init__(self):
        field_list = make_fields(news, list(NewsEntity.__annotations__.keys()))
        field_dict = {field.name: field for field in field_list}
        field_dict['id'] = field_dict.pop('news_id')
        super().__init__(news, field_dict, NewsEntity)


class FeedRepository(Repository):

    def __init__(self):
        field_list = make_fields(feeds, list(FeedEntity.__annotations__.keys()))
        field_dict = {field.name: field for field in field_list}
        field_dict['id'] = field_dict.pop('feed_id')
        super().__init__(feeds, field_dict, FeedEntity)


class UserRepository(Repository):

    def __init__(self):
        field_list = make_fields(users, list(UserEntity.__annotations__.keys()))
        field_dict = {field.name: field for field in field_list}
        field_dict['id'] = field_dict.pop('user_id')
        super().__init__(users, field_dict, UserEntity)

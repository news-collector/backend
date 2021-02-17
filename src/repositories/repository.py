from mysql.connector import MySQLConnection
from mysql.connector.cursor import MySQLCursor
from abc import abstractmethod

from src.configs import db_config
import mysql.connector as mysql
from src.models.entities import WebsiteEntity, NewsEntity, FeedEntity
from pypika import Table, Field, MySQLQuery as Query
from mysql.connector.errors import Error as DBError
import logging
from typing import List, Dict, Type

logging.getLogger().setLevel(logging.INFO)

websites = Table('websites')
news = Table('news')
feeds = Table('rss_feeds')


def make_fields(table: Table, column_names: List[str]) -> List[Field]:
    columns = []

    for name in column_names:
        columns.append(table.field(name))

    return columns


class Repository(object):

    def __init__(self, table: Table, fields: Dict[str, Field], entity: Type):
        self._connection: MySQLConnection = mysql.connect(**db_config.config)
        self._cursor: MySQLCursor = self._connection.cursor(dictionary=True, buffered=True)
        self._table = table
        self._fields = fields
        self._entity = entity

    def _get_by_id(self, _id: int):
        query = str(Query.from_(self._table).select(self._table.star).where(self._fields['id'] == _id))
        self._cursor.execute(query)
        record = self._cursor.fetchone()
        if record:
            record = self._entity(**record)
        return record

    @abstractmethod
    def get_by_id(self, _id: int):
        pass

    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def delete_by_id(self, _id: int) -> int:
        pass

    @abstractmethod
    def delete_all(self) -> int:
        pass

    @abstractmethod
    def save(self, entity):
        pass


class WebsiteRepository(Repository):

    def __init__(self):
        fields = make_fields(websites, ['website_id', 'website_name', 'website_link'])
        d = {'id': fields[0], 'fields': fields}
        super().__init__(websites, d, WebsiteEntity)

    def get_by_id(self, _id: int):
        return self._get_by_id(_id)

    # def get_by_id(self, _id: int):
    #     query = str(Query.from_(websites).select(websites.star).where(websites.website_id == _id))
    #     self._cursor.execute(query)
    #     record = self._cursor.fetchone()
    #     if record:
    #         record = WebsiteEntity(**record)
    #     logging.info(f"WebsiteRepository: get_by_id -> Record for id={_id} is {record}")
    #     return record
    #
    # def get_all(self):
    #     query = str(Query.from_(websites).select(websites.star))
    #     self._cursor.execute(query)
    #     records = self._cursor.fetchall()
    #     if records:
    #         records = [WebsiteEntity(**record) for record in records]
    #     logging.info(f"WebsiteRepository: get_all -> Found {len(records)} records")
    #     return records
    #
    # def delete_by_id(self, _id: int) -> int:
    #     query = str(Query.from_(websites).delete().where(websites.website_id == _id))
    #     rows_count = 0
    #     try:
    #         self._cursor.execute(query)
    #     except DBError as e:
    #         logging.error(f"WebsiteRepository: delete_by_id -> [{e.errno}]{e.msg}")
    #         self._connection.rollback()
    #     else:
    #         self._connection.commit()
    #         rows_count = self._cursor.rowcount
    #         logging.info(f"WebsiteRepository: delete_by_id -> Deleted {rows_count} record/s")
    #     return rows_count
    #
    # def delete_all(self) -> int:
    #     query = str(Query.from_(websites).delete())
    #     rows_count = 0
    #     try:
    #         self._cursor.execute(query)
    #     except DBError as e:
    #         logging.error(f"WebsiteRepository: delete_all -> [{e.errno}]{e.msg}")
    #         self._connection.rollback()
    #     else:
    #         self._connection.commit()
    #         rows_count = self._cursor.rowcount
    #         logging.info(f"WebsiteRepository: delete_all -> Deleted {rows_count} record/s")
    #     return rows_count
    #
    # def save(self, entity: WebsiteEntity):
    #     query = str(Query.into(websites).columns(websites.website_name, websites.website_link)
    #                 .insert(entity.website_name, entity.website_link))
    #     entity_id = None
    #
    #     try:
    #         self._cursor.execute(query)
    #     except DBError as e:
    #         logging.error(f"WebsiteRepository: save -> [{e.errno}]{e.msg}")
    #         self._connection.rollback()
    #     else:
    #         self._connection.commit()
    #         entity_id = self._cursor.lastrowid
    #         logging.info(f"WebsiteRepository: save -> Saved {entity} with id={entity_id}")
    #
    #     return entity_id


class NewsRepository(Repository):

    def get_by_id(self, _id: int):
        query = str(Query.from_(news).select(news.star).where(news.news_id == _id))
        self._cursor.execute(query)
        record = self._cursor.fetchone()
        if record:
            record = NewsEntity(**record)
        logging.info(f"NewsRepository: get_by_id -> Record for id={_id} is {record}")
        return record

    def get_all(self):
        query = str(Query.from_(news).select(news.star))
        self._cursor.execute(query)
        records = self._cursor.fetchall()
        if records:
            records = [NewsEntity(**record) for record in records]
        logging.info(f"NewsRepository: get_all -> Found {len(records)} records")
        return records

    def delete_by_id(self, _id: int) -> int:
        query = str(Query.from_(news).delete().where(news.news_id == _id))
        rows_count = 0
        try:
            self._cursor.execute(query)
        except DBError as e:
            logging.error(f"NewsRepository: delete_by_id -> [{e.errno}]{e.msg}")
            self._connection.rollback()
        else:
            self._connection.commit()
            rows_count = self._cursor.rowcount
            logging.info(f"NewsRepository: delete_by_id -> Deleted {rows_count} record/s")
        return rows_count

    def delete_all(self) -> int:
        query = str(Query.from_(news).delete())
        rows_count = 0
        try:
            self._cursor.execute(query)
        except DBError as e:
            logging.error(f"NewsRepository: delete_all -> [{e.errno}]{e.msg}")
            self._connection.rollback()
        else:
            self._connection.commit()
            rows_count = self._cursor.rowcount
            logging.info(f"NewsRepository: delete_all -> Deleted {rows_count} record/s")
        return rows_count

    def save(self, entity: NewsEntity):
        query = str(Query.into(news)
                    .columns(news.feed_id, news.news_title, news.news_link,
                             news.news_description, news.news_img_link, news.publish_date)
                    .insert(entity.feed_id, entity.news_title, entity.news_link,
                            entity.news_description, entity.news_img_link, entity.publish_date))
        entity_id = None

        try:
            self._cursor.execute(query)
        except DBError as e:
            logging.error(f"NewsRepository: save -> [{e.errno}]{e.msg}")
            self._connection.rollback()
        else:
            self._connection.commit()
            entity_id = self._cursor.lastrowid
            logging.info(f"NewsRepository: save -> Saved {entity} with id={entity_id}")

        return entity_id


class FeedRepository(Repository):
    def get_by_id(self, _id: int):
        query = str(Query.from_(feeds).select(feeds.star).where(feeds.feed_id == _id))
        self._cursor.execute(query)
        record = self._cursor.fetchone()
        if record:
            record = FeedEntity(**record)
        logging.info(f"FeedRepository: get_by_id -> Record for id={_id} is {record}")
        return record

    def get_all(self):
        query = str(Query.from_(feeds).select(feeds.star))
        self._cursor.execute(query)
        records = self._cursor.fetchall()
        if records:
            records = [FeedEntity(**record) for record in records]
        logging.info(f"FeedRepository: get_all -> Found {len(records)} records")
        return records

    def delete_by_id(self, _id: int) -> int:
        query = str(Query.from_(feeds).delete().where(feeds.feed_id == _id))
        rows_count = 0
        try:
            self._cursor.execute(query)
        except DBError as e:
            logging.error(f"FeedRepository: delete_by_id -> [{e.errno}]{e.msg}")
            self._connection.rollback()
        else:
            self._connection.commit()
            rows_count = self._cursor.rowcount
            logging.info(f"FeedRepository: delete_by_id -> Deleted {rows_count} record/s")
        return rows_count

    def delete_all(self) -> int:
        query = str(Query.from_(feeds).delete())
        rows_count = 0
        try:
            self._cursor.execute(query)
        except DBError as e:
            logging.error(f"FeedRepository: delete_all -> [{e.errno}]{e.msg}")
            self._connection.rollback()
        else:
            self._connection.commit()
            rows_count = self._cursor.rowcount
            logging.info(f"FeedRepository: delete_all -> Deleted {rows_count} record/s")
        return rows_count

    def save(self, entity: FeedEntity):
        query = str(Query.into(feeds)
                    .columns(feeds.website_id, feeds.feed_name, feeds.feed_link)
                    .insert(entity.website_id, entity.feed_name, entity.feed_link))
        entity_id = None

        try:
            self._cursor.execute(query)
        except DBError as e:
            logging.error(f"FeedRepository: save -> [{e.errno}]{e.msg}")
            self._connection.rollback()
        else:
            self._connection.commit()
            entity_id = self._cursor.lastrowid
            logging.info(f"FeedRepository: save -> Saved {entity} with id={entity_id}")

        return entity_id

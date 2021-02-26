from datetime import datetime, timedelta
from time import mktime

from src.models.entities import FeedEntity, NewsEntity
from src.parser.dateparser import DateParser
from src.parser.descriptionparser import DescriptionParser
from src.parser.newsparser import NewsParser
from src.repositories.repository import NewsRepository, FeedRepository
import feedparser
from typing import List
import logging


class Service(object):
    pass


class UserService(Service):
    pass


class FeedService(Service):
    pass


class NewsService(Service):

    def __init__(self):
        self._feed_repository = FeedRepository()
        self._news_repository = NewsRepository()
        self.upper_publish_date_boundary = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        self.lower_publish_date_boundary = self.upper_publish_date_boundary - timedelta(days=1)

    def delete_outdated(self):
        return self._news_repository.delete_outdated()

    def parse_saved_news_by_keywords(self, keywords: List[str], synonyms: bool = False):
        news_list = self._news_repository.get_all()
        return NewsParser.parse_news_by_keywords(news_list, keywords, synonyms)

    def scrap_and_save_news(self):
        news_list = self.scrap_news_from_all_feeds()
        return self._news_repository.save_all(news_list)

    def scrap_news_from_all_feeds(self):
        feed_list = self._feed_repository.get_all()

        news_list = []

        for feed in feed_list:
            news_from_feed = self.scrap_news_from_feed(feed)
            news_list = news_list + news_from_feed

        logging.info(f"NewsService: scrap_news_from_all_feeds -> Scrapped {len(news_list)} news")

        return news_list

    def scrap_news_from_feed(self, feed: FeedEntity):
        feed_parsed = feedparser.parse(feed.feed_link)

        news_list = [self.__news_entry_to_news_entity(entry, feed.feed_id)
                     for entry in feed_parsed.entries if self.__satisfies_parsing_condition(entry)]

        logging.info(f"NewsService: scrap_news_from_feed ->"
                     f" Scrapped {len(news_list)} news from feed with id = {feed.feed_id}")

        return news_list

    def __satisfies_parsing_condition(self, entry) -> bool:
        if "published_parsed" not in entry:
            return entry["title"]
        else:
            publish_datetime = datetime.fromtimestamp(mktime(entry["published_parsed"]))

            return entry["title"] and self.__is_date_in_boundaries(publish_datetime)

    def __is_date_in_boundaries(self, date: datetime) -> bool:
        lower_boundary_time_diff = (date - self.lower_publish_date_boundary).total_seconds()
        higher_boundary_time_diff = (self.upper_publish_date_boundary - date).total_seconds()
        return lower_boundary_time_diff > 0 and higher_boundary_time_diff > 0

    def __news_entry_to_news_entity(self, entry, feed_id):

        if "summary" in entry and (parsed_summary := DescriptionParser.parse(entry["summary"])) != "":
            description = parsed_summary
        else:
            description = "No description provided."

        if "published_parsed" in entry:
            publish_date = DateParser.parse(entry["published_parsed"])
        else:
            publish_date = DateParser.parse(datetime.now())

        return NewsEntity(
            feed_id,
            entry["title"],
            entry["link"],
            description,
            publish_date
        )


class WebsiteService(Service):
    pass

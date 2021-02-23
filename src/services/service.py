from datetime import datetime, timedelta
from time import mktime

from src.models.entities import FeedEntity, NewsEntity
from src.parser.dateparser import DateParser
from src.parser.descriptionparser import DescriptionParser
from src.repositories.repository import NewsRepository, FeedRepository
import feedparser


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

    def scrap_and_save_news(self):
        news_list = self.scrap_news_from_all_feeds()
        return self._news_repository.save_all(news_list)

    def scrap_news_from_all_feeds(self):
        feed_list = self._feed_repository.get_all()

        news_list = []

        for feed in feed_list:
            news_from_feed = self.scrap_news_from_feed(feed)
            news_list = news_list + news_from_feed

        return news_list

    def scrap_news_from_feed(self, feed: FeedEntity):
        feed_parsed = feedparser.parse(feed.feed_link)

        news_list = [self.__news_entry_to_news_entity(entry, feed.feed_id)
                     for entry in feed_parsed.entries if self.__satisfies_parsing_condition(entry)]

        return news_list

    def __satisfies_parsing_condition(self, entry) -> bool:
        if "published_parsed" not in entry:
            return entry["title"]
        else:
            publish_datetime = datetime.fromtimestamp(mktime(entry["published_parsed"]))
            today_boundary = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)  # TODO extract to other place so that it doesn't calculate boundaries with every news
            yesterday_boundary = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=1)

            return entry["title"] and self.__is_date_between(publish_datetime, yesterday_boundary, today_boundary)

    def __is_date_between(self, date: datetime, lower_boundary: datetime, upper_boundary: datetime) -> bool:
        lower_boundary_time_diff = (date - lower_boundary).total_seconds()
        higher_boundary_time_diff = (upper_boundary - date).total_seconds()
        return lower_boundary_time_diff > 0 and higher_boundary_time_diff > 0

    def __news_entry_to_news_entity(self, entry, feed_id):
        description = DescriptionParser.parse(entry["summary"]) if "summary" in entry else "No description provided."

        if "published_parsed" in entry:
            publish_date = DateParser.parse_struct_time(entry["published_parsed"])
        else:
            publish_date = DateParser.parse_datetime(datetime.now())

        news_image_link = ""

        return NewsEntity(
            feed_id,
            entry["title"],
            entry["link"],
            description,
            news_image_link,
            publish_date
        )


class WebsiteService(Service):
    pass

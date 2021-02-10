from dataclasses import dataclass
from datetime import datetime


@dataclass
class WebsiteEntity(object):

    website_id: int
    website_name: str
    website_link: str


@dataclass
class NewsEntity(object):

    news_id: int
    feed_id: int
    news_title: str
    news_link: str
    news_description: str
    news_img_link: str
    publish_date: datetime


@dataclass
class FeedEntity(object):

    feed_id: int
    website_id: int
    feed_name: str
    feed_link: str

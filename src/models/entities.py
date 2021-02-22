from dataclasses import dataclass
from datetime import datetime


@dataclass
class WebsiteEntity(object):

    website_name: str
    website_link: str
    website_id: int = None


@dataclass
class NewsEntity(object):

    feed_id: int
    news_title: str
    news_link: str
    news_description: str
    news_img_link: str
    publish_date: str
    news_id: int = None


@dataclass
class FeedEntity(object):

    website_id: int
    feed_name: str
    feed_link: str
    feed_id: int = None


@dataclass
class UserEntity(object):

    user_id: int
    user_authkey: str
    last_activity_time: datetime

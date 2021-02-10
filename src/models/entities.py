from dataclasses import dataclass


@dataclass
class WebsiteEntity(object):

    website_id: int
    website_name: str
    website_link: str

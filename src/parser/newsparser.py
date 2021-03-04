from collections import defaultdict
from typing import List

from src.models.entities import NewsEntity
from src.utils.util import SynonymsUtil


class NewsParser(object):

    @classmethod
    def parse_news_by_keywords(cls, news_list: List[NewsEntity], keywords: List[str], synonyms: bool = False):
        if synonyms:
            return cls.__parse_news_by_keywords_and_synonyms(news_list, keywords)
        return cls.__parse_news_by_keywords(news_list, keywords)

    @classmethod
    def __parse_news_by_keywords_and_synonyms(cls, news_list: List[NewsEntity], keywords: List[str]):
        synonyms_util = SynonymsUtil()
        parsed_news_with_keywords = defaultdict(list)
        keywords_with_synonyms = {keyword: synonyms_util.find_synonyms(keyword) for keyword in keywords}
        for news in news_list:
            news_content = (news.news_description + news.news_title).lower()
            for keyword in keywords:
                if cls.__news_content_contains_any_word(news_content, keywords_with_synonyms[keyword]):
                    parsed_news_with_keywords[news].append(keyword)
        return parsed_news_with_keywords

    @classmethod
    def __parse_news_by_keywords(cls, news_list: List[NewsEntity], keywords: List[str]):
        parsed_news_with_keywords = defaultdict(list)
        for news in news_list:
            news_content = (news.news_description + news.news_title).lower()
            for keyword in keywords:
                if cls.__news_content_contains_any_word(news_content, [keyword]):
                    parsed_news_with_keywords[news].append(keyword)
        return parsed_news_with_keywords

    @classmethod
    def __news_content_contains_any_word(cls, news_content: str, words_list: List[str]) -> bool:
        return any([word in news_content for word in words_list])

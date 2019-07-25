from enum import Enum
from datetime import datetime, timedelta

class ParsabilityType(Enum):

    RSS = "RSS"

    DIV_NAME = "DIV_NAME"

    CDATA = "CDATA"

    CUSTOM = "CUSTOM"

    NOT_IMPLEMENTED = "NOT_IMPLEMENTED"

    WORDPRESS = "WORDPRESS"

    MEDIUM = "MEDIUM"

class Scraper(object):

    def __init__(self, name, parsability_type=ParsabilityType.NOT_IMPLEMENTED, rss_url="", home_url="",):

        self.name = name
        self.parsability_type = parsability_type
        self.rss_url = rss_url
        self.last_polled_time = self.get_last_polled_time()
        self.home_url = home_url

    def poll(self, *args, **kwargs):

        if not (datetime.utcnow() - self.last_polled_time > timedelta(days=1)):
            return

        self._poll(*args, **kwargs)

        #continue polling
        pass

    def get_all_posts(self, page):
        raise Exception('Not Implemented')

    def _poll(self, page):
        raise Exception('Not Implemented')

    def parse(self):
        pass

    def to_json(self):
        return {

        }

    def get_last_polled_time(self):
        return datetime.now() - timedelta(days=4)


class Article(object):

    def __init__(self, name=None, date_published=None, author=None, author_bio=None, author_profile_image=None,
                 comments=[],):

        self.name = name
        self.date_published = date_published
        self.author = author
        self.author_bio = author_bio
        self.author_profile_image = author_profile_image
        self.comments = comments

    def add_comment(self, comment):

        self.comments.append(comment)
        return self.comments


class Comment(object):
    def __init__(self, author="", content="", date_published=None, parent_comment=None):

        self.author = author
        self.content = content
        self.date_published = date_published
        self.parent_comment = parent_comment
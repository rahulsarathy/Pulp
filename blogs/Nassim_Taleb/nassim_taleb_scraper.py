from blogs.parsability import Scraper
from blogs.models import Article, Blog
from urllib.request import urlopen, Request as req
import vcr
from datetime import datetime
from time import mktime
from bs4 import BeautifulSoup
import feedparser
from utils.s3_utils import get_object, put_object, upload_file, get_location, BUCKET_NAME, upload_article, create_article_url
from django.core.exceptions import ObjectDoesNotExist
from django.utils.timezone import make_aware
from blogs.Medium.medium import MediumScraper

class NassimTalebScraper(MediumScraper):
    def __init__(self, name_id="nntaleb"):
        super().__init__(name_id=name_id)

    # def _poll(self):
    #     xml = feedparser.parse(self.rss_url)
    #     latest_entry = xml['entries'][0]
    #     title = latest_entry['title']
    #     permalink = latest_entry['link']
    #     date_published = make_aware(datetime.fromtimestamp(mktime(latest_entry['published_parsed'])))
    #     author = latest_entry['author']
    #     content = latest_entry['content'][0]['value']
    #
    #     self.handle_s3(title=title, permalink=permalink, date_published=date_published, author=author, content=content)


    # USE WITH PROXY FLEET TO PREVENT RATE LIMITS
    def get_all_posts(self, page):
        pass
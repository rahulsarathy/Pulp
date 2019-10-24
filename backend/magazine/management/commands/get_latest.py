
from django.core.management.base import BaseCommand
from utils.blog_utils import blog_map


class Command(BaseCommand):

    def handle(self, *args, **options):
        correct_scraper = options['blog_name'][0]
        self.scrape_blog(correct_scraper)

    def add_arguments(self, parser):
        parser.add_argument('blog_name', nargs='+', type=str)

    def scrape_blog(self, correct_scraper):
        scraper = blog_map(correct_scraper)
        scraper = scraper()

        scraper.poll()
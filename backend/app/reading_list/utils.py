import logging
import os
from datetime import datetime
import json
import time
import re

from utils.s3_utils import put_object, check_file, get_article_id
from reading_list.models import ReadingListItem, Article
from pulp.globals import HTML_BUCKET, POCKET_CONSUMER_KEY
from reading_list.serializers import ReadingListItemSerializer
from django.core.cache import cache
from django.conf import settings
from django.utils.timezone import now
from rest_framework import status
from progress.types import update_add_to_reading_list_status, update_reading_list, update_delivery, update_page_count


import requests
from urllib.parse import urlparse, urljoin
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from bs4 import BeautifulSoup


def get_reading_list(user):
    my_reading = ReadingListItem.objects.filter(reader=user, archived=False).order_by('-date_added')
    serializer = ReadingListItemSerializer(my_reading, many=True)
    json_response = serializer.data
    return json_response


def get_archive_list(user):
    my_archive = ReadingListItem.objects.filter(reader=user, archived=True).order_by('-date_added')
    serializer = ReadingListItemSerializer(my_archive, many=True)
    json_response = serializer.data
    return JsonResponse(json_response, safe=False)

def add_article(link):
    validate = URLValidator()
    try:
        validate(link)
    except ValidationError:
        raise


    article, article_created = fill_article_fields(link)

    if delegate_task(article, article_created):
        from reading_list.tasks import handle_pages_task
        handle_pages_task.delay(link)

# 1. Validate URL
# 2. Get Parsed Article JSON
# 3. Add Article to DB
# 4. Convert article to PDF and count pages
# 5. Choose if Article should be set to deliver
def add_to_reading_list(user, link, date_added=None, send_updates=True):
    # Validate url
    validate = URLValidator()
    try:
        validate(link)
    except ValidationError:
        raise

    # Choose to not send updates if running a large import to avoid spamming websocket
    if send_updates:
        update_add_to_reading_list_status(user, link, 30)

    article, article_created = fill_article_fields(link)

    if send_updates:
        update_add_to_reading_list_status(user, link, 70)

    reading_list_item, reading_list_item_created = ReadingListItem.objects.get_or_create(
        reader=user, article=article
    )
    # Some instapaper links come with a timestamp
    if date_added is not None:
        reading_list_item.date_added = date_added
        reading_list_item.save()
    else:
        reading_list_item.date_added = now()
        reading_list_item.save()

    if send_updates:
        update_add_to_reading_list_status(user, link, 75)

    if delegate_task(article, article_created):
        from reading_list.tasks import handle_pages_task
        handle_pages_task.delay(link, user.email)
    else:
        if reading_list_item_created:
            # If process skips handle_pages_task, we still need to decide whether or not to add article
            # to user reading list
            handle_pages(article, user)

    if send_updates:
        update_add_to_reading_list_status(user, link, 90)

    update_reading_list(user)

    return reading_list_item

# decide whether or not to undergo the expensive task of counting article pages
def delegate_task(article, article_created):
    article_id = get_article_id(article.permalink)
    article_key = "{}.html".format(article_id)
    s3_has = check_file(article_key, HTML_BUCKET)
    if article.page_count is None or article_created or not s3_has:
        return True
    else:
        return False


def fill_article_fields(link):
    try:
        article = Article.objects.get(permalink=link)
        # skip finding mercury response if already created
        if not article.mercury_response is None:
            return article, False
    except Article.DoesNotExist:
        pass

    article_json = get_parsed(link)
    title = article_json.get('title')
    soup = BeautifulSoup(article_json.get('content', None), 'html.parser')
    article_text = soup.getText()
    article_json['parsed_text'] = article_text
    preview_text = article_text[:347] + '...'
    custom_id = get_article_id(link)
    article, article_created = Article.objects.get_or_create(
        title=title, permalink=link, mercury_response=article_json, preview_text=preview_text, custom_id=custom_id
    )
    return article, article_created

# Check for mercury response in
# 1. cache
# 2. DB
# 3. create mercury response
def get_parsed(url):
    # validate url
    validate = URLValidator()
    try:
        validate(url)
    except ValidationError:
        raise

    # check cache for URL
    if url in cache:
        json_response = json.loads(cache.get(url))
        return json_response
    # check if mercury response is already stored in DB
    else:
        try:
            my_article = Article.objects.get(permalink=url)
            json_response = my_article.mercury_response
            return json_response
        except Article.DoesNotExist:
            pass

    # generate mercury response via parser express server
    data = {'url': url}
    parser_url = 'http://{}:3000/api/mercury'.format(settings.PARSER_HOST)
    try:
        response = requests.post(parser_url, data=data)
    except requests.exceptions.RequestException as e:  # This is the correct syntax
        logging.warning("Could not connect to parser with {}".format(e))
        raise

    try:
        response_string = response.content.decode("utf-8")

        # mercury response is naive because contains some errors such as broken links and bootstrap classnames
        naive_response = json.loads(response_string)

        # call fix_mercury to fix these naive errors
        domain = urlparse(url).netloc
        json_response = fix_mercury(naive_response, domain)

        new_response_string = json.dumps(json_response)

    except json.decoder.JSONDecodeError:
        logging.warning("JSON decode error from {}".format(url))
        logging.warning("response_string is {}".format(response_string))
        raise
    except Exception as e:
        logging.warning("Could not get mercury for {} with error: {}".format(url, e))
        raise

    if not json_response.get('error', False):
        cache.set(url, new_response_string)

    return json_response

def is_absolute(url):
	return bool(urlparse(url).netloc)

def fix_mercury(mercury_response, domain):

    soup = BeautifulSoup(mercury_response.get('content', '<div></div>'), 'html.parser')

    prefix = 'http://' + domain
    links = soup.find_all('a')
    for link in links:
        href = link.get('href', ' ')
        if not is_absolute(href):
            link['href'] = urljoin(prefix, href)

    images = soup.find_all('img')
    for image in images:
        src = image.get('src', ' ')
        if not is_absolute(src):
            image['src'] = urljoin(prefix, src)

    # remove class attributes
    REMOVE_ATTRIBUTES = ['class']
    for tag in soup.recursiveChildGenerator():
        # print("tag is ", tag)
        try:
            key_list = list(tag.attrs.keys())
            # print("key list is ", key_list)
            for key in key_list:
                if key in REMOVE_ATTRIBUTES:
                    del tag.attrs[key]
        except AttributeError:
            pass

    mercury_response['content'] = str(soup)
    return mercury_response


# Create HTML file for article 3 column format and store in AWS S3
def html_to_s3(article):
    url = article.permalink
    article_id = get_article_id(url)
    template_soup = inject_json_into_html(article)

    article_key = "{}.html".format(article_id)
    f = open(article_key, "w+")
    f.write(str(template_soup))
    f.close()

    # upload object to S3 with permalink as metadata
    metadata = {
        'url': url
    }
    put_object(HTML_BUCKET, article_key, article_key, metadata)
    os.remove(article_key)
    return

def inject_json_into_html(article):
    url = article.permalink
    json_response = get_parsed(url)

    # Extract variables from json source
    date_string = None
    content = json_response.get('content')
    author = json_response.get('author')
    date_published = json_response.get('date_published')
    title = json_response.get('title')
    domain = json_response.get('domain')

    # Format Date String
    try:
        if date_published is not None:
            date_object = datetime.strptime(date_published[:10], '%Y-%m-%d')
            date_string = date_object.strftime('Originally published on %B %-d, %Y')
    except:
        date_string = None

    # Populate html template with extracted variables
    template_soup = BeautifulSoup(open('./pdf/template.html'), 'html.parser')
    template_container = template_soup.select_one('.container')
    if title is not None:
        template_container.select_one('.title').string = title
    if author is not None:
        template_container.select_one('#author').string = 'By ' + author
    if date_string is not None:
        template_container.select_one('#date').string = date_string
    template_container.select_one('#domain').string = domain

    soup = BeautifulSoup(content, 'html.parser')

    # find one layer of links and remove them, but preserve inner content
    # for link in soup.findAll('a'):
    #     innerhtml = "".join([str(x) for x in link.contents])
    #     link.insert_after(BeautifulSoup(innerhtml, 'html.parser'))
    #     link.extract()

    template_container.select_one('.main-content').insert(0, soup)
    return template_soup

# get pages for article if not done already
# decide whether to set reading list item to deliver or not
def handle_pages(article, user=None):
    url = article.permalink

    # Count pages of article
    if article.page_count is None:
        page_count = get_page_count(url)
        if page_count is None:
            logging.warning("Puppeteer failed for {}".format(url))
            return
        article.page_count = page_count
        article.save()
    else:
        page_count = article.page_count

    # for backfill_pages command
    if user is None:
        return page_count

    update_page_count(user, article.permalink, page_count)

    # Set to_deliver for ReadingListItem
    rlist_item, created = ReadingListItem.objects.get_or_create(
        reader=user, article=article
    )
    # Check if we should check this article to to_deliver
    to_deliver = decide_to_deliver(user, url, page_count)
    rlist_item.to_deliver = to_deliver
    rlist_item.save()

    update_delivery(user, article.permalink, to_deliver)

    return page_count

def decide_to_deliver(user, url, page_count):
    if page_count is None:
        return False
    current_pages = get_selected_pages(user, url)
    total_pages = page_count + current_pages
    if total_pages > 50:
        to_deliver = False
    else:
        to_deliver = True

    return to_deliver

def get_selected_pages(user, permalink):
    rlist_items = ReadingListItem.objects.filter(reader=user)
    total_pages = 0
    for item in rlist_items:
        if item.to_deliver:
            if item.article.page_count is None:
                item.to_deliver = False
                item.save()
            else:
                total_pages = total_pages + item.article.page_count

    custom_id = get_article_id(permalink)
    article, created = Article.objects.get_or_create(
        permalink=permalink, custom_id=custom_id
    )

    reading_list_item, created = ReadingListItem.objects.get_or_create(
        reader=user, article=article
    )

    return total_pages

# Get articles staged for delivery
def get_staged_articles(user):
    total = 0
    staged = []
    reading_list_items = ReadingListItem.objects.filter(reader=user)
    # Find out which articles we want to include in the magazine
    for item in reading_list_items:
        if item.to_deliver:
            new_total = total + item.article.page_count
            if new_total > 50:
                return
            staged.append(item.article)
    return staged


def get_page_count(url):
    article_id = get_article_id(url)
    # If file is not uploaded, then uploaded
    if not check_file('{}.html'.format(article_id), HTML_BUCKET):
        try:
            article = Article.objects.get(permalink=url)
            html_to_s3(article)
        except Article.DoesNotExist:
            return None

    data = {'html_id': article_id}
    puppeteer_url = 'http://{}:4000/api/print'.format(settings.PUPPETEER_HOST)
    try:
        response = contact_puppeteer(url)
    except requests.exceptions.ConnectionError:
        logging.warning("failed to connect to puppeteer for {}".format(url))
        return None
    try:
        response_string = response.content.decode("utf-8")
        json_response = json.loads(response_string)
        pages = json_response.get('pages')
        html_id = json_response.get('html_id')
    except json.decoder.JSONDecodeError:
        logging.warning("JSON decode error from {}".format(response_string))
        return None
    except AttributeError:
        logging.warning("attribute error from {}".format(url))
        return None

    return pages

def contact_puppeteer(url):
    article_id = get_article_id(url)
    data = {'html_id': article_id}
    puppeteer_url = 'http://{}:4000/api/print'.format(settings.PUPPETEER_HOST)
    try:
        response = requests.post(puppeteer_url, data=data)
    except requests.exceptions.ConnectionError:
        raise
    return response

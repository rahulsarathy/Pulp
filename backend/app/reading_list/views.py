import json

from reading_list.models import Article, ReadingListItem
from reading_list.utils import get_parsed, html_to_s3, get_reading_list, \
    add_to_reading_list, get_archive_list, decide_to_deliver
from instapaper.serializers import InstapaperCredentialsSerializer
from pocket.serializers import PocketCredentialsSerializer
from instapaper.models import InstapaperCredentials
from pocket.models import PocketCredentials
from progress.types import update_add_to_reading_list_status
from newspaper import Article as Art

from rest_framework.decorators import api_view
from rest_framework.exceptions import NotFound
from django.core.exceptions import ValidationError
from django.http import JsonResponse, HttpResponse
import traceback
from django.views.decorators.cache import cache_page



@api_view(['GET'])
def get_reading(request):
    user = request.user
    if not user.is_authenticated:
        return JsonResponse(data={'error': 'Invalid request.'}, status=403)
    return JsonResponse(get_reading_list(user), safe=False)

@api_view(['POST'])
def handle_add_to_reading_list(request):
    user = request.user
    if not user.is_authenticated:
        return JsonResponse(data={'error': 'Invalid request.'}, status=403)
    link = request.POST['link']
    update_add_to_reading_list_status(user, link, 0)

    # handle validation error
    try:
        add_to_reading_list(user, link)
    except ValidationError:
        return JsonResponse(data={'error': 'Invalid URL.'}, status=400)
    except json.decoder.JSONDecodeError:
        return JsonResponse(data={'error': 'Invalid URL.'}, status=400)
    except Exception:
        traceback.print_exc()
        update_add_to_reading_list_status(user, link, 100)
        return JsonResponse(data={'error': 'Error while adding to reading list. Try again or contact support.'}, status=400)

    update_add_to_reading_list_status(user, link, 100)
    return JsonResponse(get_reading_list(user), safe=False)


@api_view(['GET'])
def get_archive(request):
    user = request.user
    if not user.is_authenticated:
        return JsonResponse(data={'error': 'Invalid request.'}, status=403)
    return get_archive_list(user)


@api_view(['POST'])
def archive_item(request):
    user = request.user
    if not user.is_authenticated:
        return JsonResponse(data={'error': 'Invalid request.'}, status=403)
    link = request.POST['link']
    try:
        article = Article.objects.get(permalink=link)
    except Article.DoesNotExist:
        raise NotFound(detail='Article not found', code=404)
    try:
        reading_list_item = ReadingListItem.objects.get(article=article, reader=user)
        reading_list_item.archived = True
        reading_list_item.save()
        return JsonResponse(get_reading_list(user), safe=False)
    except ReadingListItem.DoesNotExist:
        raise NotFound(detail='ReadingListItem with link: %s not found.' % link, code=404)

@api_view(['POST'])
def unarchive(request):
    user = request.user
    if not user.is_authenticated:
        return JsonResponse(data={'error': 'Invalid request.'}, status=403)
    link = request.POST['link']
    try:
        article = Article.objects.get(permalink=link)
    except Article.DoesNotExist:
        raise NotFound(detail='Article not found', code=404)
    try:
        reading_list_item = ReadingListItem.objects.get(article=article, reader=user)
        reading_list_item.archived = False
        reading_list_item.save()
        return get_archive_list(user)
    except ReadingListItem.DoesNotExist:
        raise NotFound(detail='Archived Reading List Item with link: %s not found.' % link, code=404)


@api_view(['POST'])
def remove_from_reading_list(request):
    user = request.user
    if not user.is_authenticated:
        return JsonResponse(data={'error': 'Invalid request.'}, status=403)

    link = request.POST['link']
    try:
        article = Article.objects.get(permalink=link)
    except Article.DoesNotExist:
        raise NotFound(detail='Article not found', code=404)
    try:
        reading_list_item = ReadingListItem.objects.get(article=article, reader=user)
        reading_list_item.delete()
    except ReadingListItem.DoesNotExist:
        raise NotFound(detail='ReadingListItem with link: %s not found.' % link, code=404)

    # Remove from instapaper sync
    try:
        credentials = InstapaperCredentials.objects.get(owner=user)
        polled_bookmarks = credentials.polled_bookmarks
        polled_bookmarks.pop(link, None)
        credentials.save()
    except InstapaperCredentials.DoesNotExist:
        # nothing to remove
        pass
    return JsonResponse(get_reading_list(user), safe=False)

@cache_page(60 * 15)
@api_view(['GET'])
def get_summary(request):
    url = request.GET['url']
    newspaper_article = Art(url)
    try:
        newspaper_article.download()
    except Art.ArticleException:
        return HttpResponse(status=403)
    newspaper_article.parse()
    newspaper_article.nlp()
    summary = newspaper_article.summary
    title = newspaper_article.title
    result = {
        'summary': summary,
        'title': title
    }
    return JsonResponse(result, safe=True)


@api_view(['POST'])
def update_deliver(request):
    user = request.user

    if not user.is_authenticated:
        return JsonResponse(data={'error': 'Invalid request.'}, status=403)

    link = request.POST['permalink']
    to_deliver = request.POST.get('to_deliver') == 'true'
    # Get Article to get Reading list item


    try:
        article = Article.objects.get(permalink=link)
    except Article.DoesNotExist:
        raise NotFound(detail='Article not found', code=404)

    if to_deliver:
        # if overflow over page limit, then force to_deliver to False
        to_deliver = decide_to_deliver(user, link, article.page_count)

    try:
        reading_list_item = ReadingListItem.objects.get(article=article, reader=user)
        reading_list_item.to_deliver = to_deliver
        reading_list_item.save()
        return JsonResponse(get_reading_list(user), safe=False)
    except ReadingListItem.DoesNotExist:
        raise NotFound(detail='ReadingListItem with link: %s not found.' % link, code=404)
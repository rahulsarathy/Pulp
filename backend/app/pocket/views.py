import re

from pulp.globals import POCKET_CONSUMER_KEY
from django.core.cache import cache
from .models import PocketCredentials
from pocket.tasks import import_pocket

from django.shortcuts import render
from django.utils import timezone
import requests
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from rest_framework.decorators import api_view
from .tasks import import_pocket, retrieve_pocket

 #Method is triggered when user starts pocket integration from frontend modal
@api_view(['POST'])
def request_pocket(request):
    user = request.user
    if not user.is_authenticated:
        return JsonResponse(data={'error': 'Invalid request.'}, status=403)
    # Get pocket code from consumer key
    hostname = request.get_host()
    redirect_uri = 'http://{}/api/pocket/authenticate_pocket'.format(hostname)
    data = {'consumer_key': POCKET_CONSUMER_KEY, 'redirect_uri': redirect_uri}
    code = get_pocket_code(data)
    url = 'https://getpocket.com/auth/authorize?request_token={code}&redirect_uri=' \
          '{redirect_uri}'.format(code=code, redirect_uri=redirect_uri)
    key = request.user.email + 'pocket'
    cache.set(key, code)
    # Send the user a url w/ code that links the user to our consumer key
    # User will redirect to this URL
    return HttpResponse(url)

def get_pocket_code(data):
    url = 'https://getpocket.com/v3/oauth/request'
    response = requests.post(url, data=data)
    response_string = response.text
    code = response_string.partition("code=")[2]
    return code


@api_view(['POST'])
def remove_pocket(request):
    user = request.user
    if not user.is_authenticated:
        return JsonResponse(data={'error': 'Invalid request.'}, status=403)

    try:
        credentials = PocketCredentials.objects.get(owner=user)
    except PocketCredentials.DoesNotExist:
        return JsonResponse(data={'error': 'Could not find pocket credentials.'}, status=403)
    credentials.delete()
    return HttpResponse(status=200)

def get_access_token(code):
    url = 'https://getpocket.com/v3/oauth/authorize'
    data = {'consumer_key': POCKET_CONSUMER_KEY, 'code': code}
    response = requests.post(url, data=data)
    response_string = response.text
    result = re.search('access_token=(.*)&username', response_string)
    access_token = result.group(1)
    return access_token

# this method is hit as a webhook
@api_view(['GET'])
def authenticate_pocket(request):
    user = request.user
    if not user.is_authenticated:
        return JsonResponse(data={'error': 'Invalid request.'}, status=403)
    # Get code linking user to our consumer key from cache
    key = user.email + 'pocket'
    code = cache.get(key)

    # get access token for user
    access_token = get_access_token(code)

    try:
        # update pocket access token
        credentials = PocketCredentials.objects.get(owner=user)
        credentials.token = access_token
        credentials.invalid = False
        credentials.save()
    except PocketCredentials.DoesNotExist:
        # create credentials with new acess token
        PocketCredentials(owner=request.user, token=access_token, invalid=False).save()

    import_pocket.delay(request.user.email)

    return HttpResponseRedirect('/')

@api_view(['POST'])
def sync_pocket(request):
    user = request.user
    if not user.is_authenticated:
        return JsonResponse(data={'error': 'Invalid request.'}, status=403)
    try:
        credentials = PocketCredentials.objects.get(owner=user)
        if credentials.invalid:
            return JsonResponse(data={'error': 'Invalid Pocket Credentials.'}, status=403)
    except PocketCredentials.DoesNotExist:
        return JsonResponse(data={'error': 'Invalid Pocket Credentials.'}, status=403)

    import_pocket.delay(user.email)
    now = timezone.now()
    return JsonResponse(now, safe=False)
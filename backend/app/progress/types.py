from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import hashlib
from reading_list.serializers import ReadingListItemSerializer

def get_channel_id(email):
    hash_string = 'user email' + email
    encoded = hash_string.encode('utf-8')
    final_id = hashlib.sha224(encoded).hexdigest()[:20]
    return final_id

def update_add_to_reading_list_status(user, link, percent):
    channel_layer = get_channel_layer()
    channel_id = get_channel_id(user.email)
    async_to_sync(channel_layer.group_send)(
        channel_id,
        {
            'type': 'add_to_reading_list',
            'link': link,
            'percent': percent,
        }
    )

def update_instapaper_queue_status(user, completed, total):
    channel_layer = get_channel_layer()
    channel_id = get_channel_id(user.email)
    async_to_sync(channel_layer.group_send)(
        channel_id,
        {
            'type': 'instapaper_queue',
            'total': total,
            'completed': completed
        }
    )

def update_pocket_queue_status(user, completed, total):
    channel_layer = get_channel_layer()
    channel_id = get_channel_id(user.email)
    async_to_sync(channel_layer.group_send)(
        channel_id,
        {
            'type': 'pocket_queue',
            'total': total,
            'completed': completed
        }
    )

def update_page_count(user, link, page_count):
    channel_layer = get_channel_layer()
    channel_id = get_channel_id(user.email)
    async_to_sync(channel_layer.group_send)(
        channel_id,
        {
            'type': 'page_count',
            'link': link,
            'page_count': page_count,
        }
    )

def update_delivery(user, link, to_deliver):
    channel_layer = get_channel_layer()
    channel_id = get_channel_id(user.email)
    async_to_sync(channel_layer.group_send)(
        channel_id,
        {
            'type': 'to_deliver',
            'to_deliver': to_deliver,
            'link': link,
        }
    )

def update_reading_list(user):
    from reading_list.utils import get_reading_list
    channel_layer = get_channel_layer()
    channel_id = get_channel_id(user.email)
    reading_list = get_reading_list(user)

    async_to_sync(channel_layer.group_send)(
        channel_id,
        {
            'type': 'reading_list',
            'reading_list': reading_list,
        }
    )
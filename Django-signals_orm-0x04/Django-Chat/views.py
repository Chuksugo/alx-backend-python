from .models import Message
from django.db.models import Prefetch

def get_top_level_messages_with_replies():
    messages = Message.objects.filter(parent_message__isnull=True)\
        .select_related('sender', 'receiver')\
        .prefetch_related(
            Prefetch('replies', queryset=Message.objects.select_related('sender', 'receiver'))
        )
    return messages

def get_replies_recursive(message):
    return [
        {
            "message": reply,
            "replies": get_replies_recursive(reply)
        }
        for reply in message.replies.all().select_related('sender', 'receiver')
    ]

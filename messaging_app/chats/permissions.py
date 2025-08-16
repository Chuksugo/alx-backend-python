# chats/permissions.py
from rest_framework.permissions import BasePermission
from .models import Conversation
from rest_framework import permissions

class IsParticipant(BasePermission):  # <--- renamed
    """
    Custom permission for conversation participants.
    """
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        if request.method in ('GET', 'HEAD', 'OPTIONS'):
            return True

        conversation_id = view.kwargs.get('conversation_pk') or view.kwargs.get('pk')
        if conversation_id:
            try:
                conversation = Conversation.objects.get(id=conversation_id)
                return request.user in conversation.participants.all()
            except Conversation.DoesNotExist:
                return False

        return False

    def has_object_permission(self, request, view, obj):
        if request.method in ('GET', 'HEAD', 'OPTIONS'):
            return True

        if hasattr(obj, 'participants'):
            return request.user in obj.participants.all()

        if hasattr(obj, 'conversation'):
            return request.user in obj.conversation.participants.all()

        return False

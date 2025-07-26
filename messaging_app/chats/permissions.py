from rest_framework.permissions import BasePermission
from .models import Conversation


class IsParticipant(BasePermission):
    """
    Custom permission to allow access only to participants of a conversation.
    """

    def has_permission(self, request, view):
        # For nested routes like /conversations/{conversation_pk}/messages/
        conversation_id = view.kwargs.get('conversation_pk')
        if conversation_id:
            try:
                conversation = Conversation.objects.get(id=conversation_id)
                return request.user in conversation.participants.all()
            except Conversation.DoesNotExist:
                return False

        # For non-nested routes like /conversations/
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Handles permission for individual objects
        if hasattr(obj, 'participants'):
            return request.user in obj.participants.all()

        if hasattr(obj, 'conversation'):
            return request.user in obj.conversation.participants.all()

        return False

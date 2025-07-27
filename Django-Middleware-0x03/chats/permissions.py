from rest_framework.permissions import BasePermission
from .models import Conversation


class IsParticipantOfConversation(BasePermission):
    """
    Custom permission:
    - Authenticated users can access safe methods
    - Only participants of a conversation can PUT, PATCH, DELETE, POST
    """

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        # Allow read-only methods
        if request.method in ('GET', 'HEAD', 'OPTIONS'):
            return True

        # For write methods, ensure user is participant
        conversation_id = view.kwargs.get('conversation_pk') or view.kwargs.get('pk')
        if conversation_id:
            try:
                conversation = Conversation.objects.get(id=conversation_id)
                return request.user in conversation.participants.all()
            except Conversation.DoesNotExist:
                return False

        return False

    def has_object_permission(self, request, view, obj):
        # Read-only access for safe methods
        if request.method in ('GET', 'HEAD', 'OPTIONS'):
            return True

        # Write permissions: check if user is a participant
        if hasattr(obj, 'participants'):
            return request.user in obj.participants.all()

        if hasattr(obj, 'conversation'):
            return request.user in obj.conversation.participants.all()

        return False

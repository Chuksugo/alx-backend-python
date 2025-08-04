from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.views.decorators.cache import cache_page
from .models import Conversation, Message, CustomUser
from django.shortcuts import render
from .serializers import ConversationSerializer, MessageSerializer
from .permissions import IsParticipant
from .filters import MessageFilter  # <-- NEW
from .pagination import MessagePagination  # <-- NEW


class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated, IsParticipant]
    filter_backends = [filters.SearchFilter]
    search_fields = ['participants__username', 'participants__email']

    def get_queryset(self):
        return Conversation.objects.filter(participants=self.request.user)

    def create(self, request, *args, **kwargs):
        participants_ids = request.data.get('participants', [])
        if not participants_ids:
            return Response({"error": "Participants are required."}, status=status.HTTP_400_BAD_REQUEST)

        conversation = Conversation.objects.create()
        participants = CustomUser.objects.filter(id__in=participants_ids)
        conversation.participants.set(participants)
        conversation.save()

        serializer = self.get_serializer(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsParticipant]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]  # <-- UPDATED
    filterset_class = MessageFilter  # <-- NEW
    search_fields = ['message_body', 'sender__username']
    ordering_fields = ['timestamp']
    ordering = ['-timestamp']
    pagination_class = MessagePagination  # <-- NEW

    def get_queryset(self):
        conversation_id = self.kwargs.get('conversation_pk')
        conversation = get_object_or_404(Conversation, id=conversation_id)

        if self.request.user not in conversation.participants.all():
            return Message.objects.none()

        return Message.objects.filter(conversation=conversation)

    def perform_create(self, serializer):
        conversation_id = self.kwargs.get('conversation_pk')
        conversation = get_object_or_404(Conversation, id=conversation_id)

        if self.request.user not in conversation.participants.all():
            return Response({"error": "You are not a participant of this conversation."}, status=status.HTTP_403_FORBIDDEN)

        serializer.save(conversation=conversation, sender=self.request.user)



@cache_page(60)  # cache for 60 seconds
def conversation_view(request):
    messages = Message.objects.filter(receiver=request.user)
    return render(request, 'chats/conversation.html', {'messages': messages})
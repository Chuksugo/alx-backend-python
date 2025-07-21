from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import Conversation, Message, CustomUser
from .serializers import ConversationSerializer, MessageSerializer


class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['participants__username', 'participants__email']

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
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    search_fields = ['message_body', 'sender__username']
    ordering_fields = ['timestamp']
    ordering = ['-timestamp']

    def get_queryset(self):
        conversation_id = self.kwargs.get('conversation_pk')  # for NestedDefaultRouter
        return Message.objects.filter(conversation_id=conversation_id)

    def perform_create(self, serializer):
        conversation_id = self.kwargs.get('conversation_pk')
        conversation = get_object_or_404(Conversation, id=conversation_id)

        # You can use self.request.user if authentication is in place
        sender_id = self.request.data.get('sender')
        sender = get_object_or_404(CustomUser, id=sender_id)

        serializer.save(conversation=conversation, sender=sender)

from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Conversation, Message, CustomUser
from .serializers import ConversationSerializer, MessageSerializer
from .permissions import IsParticipant


class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated, IsParticipant]
    filter_backends = [filters.SearchFilter]
    search_fields = ['participants__username', 'participants__email']

    def get_queryset(self):
        # Return only conversations that include the authenticated user
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
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    search_fields = ['message_body', 'sender__username']
    ordering_fields = ['timestamp']
    ordering = ['-timestamp']

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

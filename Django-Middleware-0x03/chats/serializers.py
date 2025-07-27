from rest_framework import serializers
from .models import CustomUser, Conversation, Message


class UserSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(required=False)

    class Meta:
        model = CustomUser
        fields = ['id', 'user_id', 'username', 'email', 'first_name', 'last_name', 'phone_number']


class MessageSerializer(serializers.ModelSerializer):
    sender_email = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = ['message_id', 'sender_email', 'message_body', 'sent_at']

    def get_sender_email(self, obj):
        return obj.sender.email if obj.sender else None


class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'created_at', 'messages']

    def get_messages(self, obj):
        messages = obj.messages.all()
        return MessageSerializer(messages, many=True).data

    def validate(self, data):
        if not data.get('participants'):
            raise serializers.ValidationError("A conversation must have at least one participant.")
        return data

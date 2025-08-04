from django.db import models
from django.contrib.auth.models import User
from .managers import UnreadMessagesManager  # ✅ import the manager

class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    parent_message = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        related_name='replies',
        on_delete=models.CASCADE
    )

    # ✅ Register custom managers
    objects = models.Manager()
    unread = UnreadMessagesManager()

    def __str__(self):
        return f"From {self.sender} to {self.receiver} at {self.timestamp}"

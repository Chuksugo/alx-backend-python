from django.test import TestCase
from django.contrib.auth.models import User
from .models import Message, Notification

class NotificationSignalTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='alice', password='testpass')
        self.user2 = User.objects.create_user(username='bob', password='testpass')

    def test_notification_created_on_message(self):
        msg = Message.objects.create(sender=self.user1, receiver=self.user2, content="Hello Bob")
        self.assertEqual(Notification.objects.count(), 1)
        notif = Notification.objects.first()
        self.assertEqual(notif.user, self.user2)
        self.assertEqual(notif.message, msg)

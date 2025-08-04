from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib.auth import get_user_model
from django.shortcuts import render
from .models import Message

User = get_user_model()

@login_required
def delete_user(request):
    if request.method == "POST":
        user = request.user
        user.delete()
        return redirect('home')  # or your login/home page

def user_messages(request):
    messages = Message.objects.filter(sender=request.user)\
        .select_related('receiver')\
        .prefetch_related('replies')
    return render(request, 'messages/user_messages.html', {'messages': messages})

def threaded_messages(request):
    top_messages = Message.objects.filter(parent_message__isnull=True)\
        .select_related('sender', 'receiver')\
        .prefetch_related('replies')

    return render(request, 'messages/threaded.html', {'messages': top_messages})


def unread_inbox_view(request):
    # ✅ Use the custom manager
    unread_messages = Message.unread.for_user(request.user)
    return render(request, 'messages/unread_inbox.html', {'messages': unread_messages})


def unread_inbox_view(request):
    unread_messages = Message.unread.unread_for_user(request.user)
    return render(request, 'messages/unread.html', {'messages': unread_messages})

# chats/middleware.py
import logging
from datetime import datetime
from django.http import HttpResponseForbidden
import time
from django.http import JsonResponse
from collections import defaultdict

# Configure logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# File handler to log to 'requests.log'
file_handler = logging.FileHandler('requests.log')  # logs to root directory
formatter = logging.Formatter('%(message)s')
file_handler.setFormatter(formatter)

# Prevent duplicate handlers during dev reload
if not logger.handlers:
    logger.addHandler(file_handler)

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Determine user
        user = request.user.username if request.user.is_authenticated else 'Anonymous'
        # Log timestamp, user, and path
        logger.info(f"{datetime.now()} - User: {user} - Path: {request.path}")

        # Continue processing the request
        response = self.get_response(request)
        return response


class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Get current hour in 24-hour format
        current_hour = datetime.now().hour

        # Allow only between 18:00 (6PM) and 21:00 (9PM)
        if not (18 <= current_hour <= 21):
            return HttpResponseForbidden("Access to chat is restricted outside 6PM to 9PM.")

        return self.get_response(request)


class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Dictionary to track messages: {ip_address: [timestamps]}
        self.message_logs = defaultdict(list)
        self.time_window = 60  # 60 seconds
        self.max_messages = 5  # Max 5 messages per window

    def __call__(self, request):
        # Only apply rate limiting on POST requests to the chat endpoint
        if request.method == 'POST' and request.path.startswith('/chats/'):
            ip = self.get_client_ip(request)
            now = time.time()

            # Filter out old timestamps outside the time window
            recent_timestamps = [
                ts for ts in self.message_logs[ip] if now - ts < self.time_window
            ]
            self.message_logs[ip] = recent_timestamps

            if len(recent_timestamps) >= self.max_messages:
                return JsonResponse(
                    {'error': 'Rate limit exceeded: Max 5 messages per minute.'},
                    status=429
                )

            self.message_logs[ip].append(now)

        response = self.get_response(request)
        return response

    def get_client_ip(self, request):
        # Get IP from X-Forwarded-For if present (e.g., behind a proxy)
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0].strip()
        return request.META.get('REMOTE_ADDR')
    

class RolepermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Allow access to non-protected routes (e.g., admin, login, static)
        if request.path.startswith('/admin') or not request.user.is_authenticated:
            return self.get_response(request)

        # Check for user role
        user = request.user

        # Let's assume user roles are stored in user.profile.role
        # You may need to adjust this if role is stored differently
        if hasattr(user, 'profile'):
            role = getattr(user.profile, 'role', None)
        else:
            role = getattr(user, 'role', None)

        if role not in ['admin', 'moderator']:
            return JsonResponse({'error': 'Forbidden: Insufficient role permissions'}, status=403)

        return self.get_response(request)

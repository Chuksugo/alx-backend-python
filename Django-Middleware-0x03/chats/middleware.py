# chats/middleware.py
import logging
from datetime import datetime

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

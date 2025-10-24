import os
from django.core.wsgi import get_wsgi_application
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ride_booking_angeles.settings')
application = get_wsgi_application()

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.settings")
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
from api.services.tokenservice import refreshToken
import time
import logging
logger_info = logging.getLogger('django.info')


if __name__ == '__main__':
    while True:
        logger_info.info("Check the AccessToken now...")
        refreshToken()
        time.sleep(1200)

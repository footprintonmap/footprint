"""
WSGI config for footprint project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/howto/deployment/wsgi/
"""
import os
import sys
from django.core.wsgi import get_wsgi_application

import pymysql

pymysql.install_as_MySQLdb()

sys.path.append('/home/ubuntu/footprint/back/footprint')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "footprint.settings")

application = get_wsgi_application()
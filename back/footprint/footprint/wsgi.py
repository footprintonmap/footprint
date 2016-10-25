"""
WSGI config for footprint project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "footprint.settings")

application = get_wsgi_application()


#wsgi.py
# import os, sys
# # Calculate the path based on the location of the WSGI script.
# apache_configuration= os.path.dirname(__file__)
# project = os.path.dirname(apache_configuration)
# workspace = os.path.dirname(project)
# sys.path.append(workspace)
# sys.path.append(project)

# # Add the path to 3rd party django application and to django itself.
# sys.path.append('/home/ubuntu/footprint/back/footprint')
# os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.apache.override'
# import django.core.handlers.wsgi
# application = django.core.handlers.wsgi.WSGIHandler()
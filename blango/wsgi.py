"""
WSGI config for blango project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "blango.settings")
# add Production settings
os.environ.setdefault("DJANGO_CONFIGURATION", "Prod")

# update from
#from django.core.wsgi import get_wsgi_application
# to use configurations

from configurations.wsgi import get_wsgi_application

application = get_wsgi_application()


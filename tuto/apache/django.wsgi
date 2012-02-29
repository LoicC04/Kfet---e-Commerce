import os
import sys

path = '/var/www/Kfet---e-Commerce'
if path not in sys.path:
    sys.path.insert(0, path)

path = '/var/www/Kfet---e-Commerce/tuto'
if path not in sys.path:
    sys.path.insert(0, path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'tuto.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

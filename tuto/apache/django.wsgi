import os
import sys

path = '/srv/http'
if path not in sys.path:
    sys.path.insert(0, '/srv/http')

path = '/srv/http/tuto'
if path not in sys.path:
    sys.path.insert(0, '/srv/http/tuto')

os.environ['DJANGO_SETTINGS_MODULE'] = 'tuto.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

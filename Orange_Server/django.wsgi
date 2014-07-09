import os
import sys

sys.path.append('/home/jcsla/Orange_Server/')
os.environ['DJANGO_SETTINGS_MODULE'] = 'Orange_Server.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

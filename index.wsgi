import os, sys

BASE_DIR = os.path.dirname(__file__)

# Add the app's directory to the PYTHONPATH
sys.path.append(BASE_DIR)
sys.path.append(os.path.join(BASE_DIR, 'ss'))

os.environ["DJANGO_SETTINGS_MODULE"] = 'ss.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

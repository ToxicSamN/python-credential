"""
WSGI config for credentialstore project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/howto/deployment/wsgi/
"""

import os
import platform
import sys

from django.core.wsgi import get_wsgi_application

#os.environ.setdefault("DJANGO_SETTINGS_MODULE", "credentialstore.settings")
print('WSGI ENVIRONMENT')
print(os.environ)

api_path = '/u01/code/python-credential/credentialstore'
sys.path.append(api_path)
os.environ['DJANGO_SETTINGS_MODULE'] = 'credentialstore.settings'

application = get_wsgi_application()

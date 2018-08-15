"""
Django settings for credentialstore project.

Generated by 'django-admin startproject' using Django 2.0.5.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os
import ldap
import logging.config
from django.utils.log import DEFAULT_LOGGING
from configparser import ConfigParser
from django_auth_ldap.config import LDAPSearch, LDAPSearchUnion, NestedActiveDirectoryGroupType

parser = ConfigParser()

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_FILE = os.path.join('credentialstore', 'environment.conf')

parser.read(os.path.join(BASE_DIR, ENV_FILE))
settings_dict = parser.__dict__['_sections']['ENV']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
LOGLEVEL = 'INFO'
if settings_dict.get('django_debug', None):
    if settings_dict['django_debug'] == "True":
        DEBUG = True
        LOGLEVEL = 'DEBUG'

# Disable Django's logging setup
LOGGING_CONFIG = None

# Setup logging
logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'console': {
            # exact format is not important, this is the minimum information
            'format': '%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
        },
        'django.server': DEFAULT_LOGGING['formatters']['django.server'],
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'console',
        },
        'django.server': DEFAULT_LOGGING['handlers']['django.server'],
        'applogfile': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join('/u01/log', 'credentialstore.log'),
            'maxBytes': 1024*1024*15, # 15MB
            'backupCount': 10,
        },
    },
    'loggers': {
    # root logger
        '': {
            'level': 'WARNING',
            'handlers': ['console'],
        },
        'credentialstore': {
            'level': LOGLEVEL,
            'handlers': ['console', 'applogfile'],
            'propogate': False
        },
        'django.server': DEFAULT_LOGGING['loggers']['django.server'],
    },
})

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = settings_dict['django_secret']
os.environ['DJANGO_SECRET'] = SECRET_KEY
os.environ['RSA_PRIV'] = settings_dict['rsa_priv']
os.environ['RSA_PUB'] = settings_dict['rsa_pub']



print('DEBUG Enabled: {}'.format(DEBUG))

# This setting is required to protect your site against some CSRF
# attacks. If you use a wildcard, you must perform your own validation
# of the Host HTTP header, or otherwise ensure that you aren’t vulnerable
# to this category of attacks
ALLOWED_HOSTS = ['*']


# HTTPS Settings

#SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
#SECURE_SSL_REDIRECT = True
#SESSION_COOKIE_SECURE = True
#CSRF_COOKIE_SECURE = True


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'api',
    'accounts',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'credentialstore.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
        'DIRS': [BASE_DIR + '/templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'credentialstore.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# django_auth_ldap
AUTH_LDAP_SERVER_URI = settings_dict['ldap_uri']
AD_CERT_FILE = os.path.join(BASE_DIR, '/etc/pki/tls/certs/cert.crt')
ldap.set_option(ldap.OPT_PROTOCOL_VERSION, 3)
ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_ALLOW)
ldap.set_option(ldap.OPT_X_TLS_CACERTFILE, AD_CERT_FILE)
# LDAP_IGNORE_CERT_ERRORS = True

AUTH_LDAP_BIND_DN = settings_dict['bind_account']
AUTH_LDAP_BIND_PASSWORD = settings_dict['bind_passwd']

AUTH_LDAP_USER_SEARCH = LDAPSearchUnion(
    LDAPSearch(settings_dict['ldap_search1'],
               ldap.SCOPE_SUBTREE,
               "(sAMAccountName=%(user)s)"),
    LDAPSearch(settings_dict['ldap_search2'],
               ldap.SCOPE_SUBTREE,
               "(sAMAccountName=%(user)s)"),
    LDAPSearch(settings_dict['ldap_search3'],
               ldap.SCOPE_SUBTREE,
               "(sAMAccountName=%(user)s)"),
)
AUTH_LDAP_ALWAYS_UPDATE_USER = True
AUTH_LDAP_USER_ATTR_MAP = {
    "first_name": "givenName",
    "last_name": "sn",
    "email": "mail"
}

AUTH_LDAP_GROUP_SEARCH = LDAPSearch(settings_dict['ldap_grp_search'],
                                    ldap.SCOPE_SUBTREE,
                                    "(objectClass=group)")
AUTH_LDAP_USER_FLAGS_BY_GROUP = {
    'is_active': settings_dict['ldap_active'],
    'is_staff': settings_dict['ldap_staff'],
    'is_superuser': settings_dict['ldap_super'],
}

AUTH_LDAP_GROUP_TYPE = NestedActiveDirectoryGroupType()
AUTH_LDAP_FIND_GROUP_PERMS = True
AUTH_LDAP_MIRROR_GROUPS = [settings_dict['ldap_mirror_groups']]
AUTH_LDAP_REQUIRE_GROUP = settings_dict['ldap_active']
AUTH_LDAP_CACHE_GROUPS = True
AUTH_LDAP_GROUP_CACHE_TIMEOUT = 3600

AUTH_LDAP_CONNECTION_OPTIONS = {
    ldap.OPT_DEBUG_LEVEL: 0,
    ldap.OPT_REFERRALS: 0,
}

AUTHENTICATION_BACKENDS = (
    'django_auth_ldap.backend.LDAPBackend',
    'django.contrib.auth.backends.ModelBackend',
)

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "assets"),
)
STATIC_ROOT = '/'  # os.path.join(BASE_DIR, "assets/")

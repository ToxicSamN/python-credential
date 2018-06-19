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
from django_auth_ldap.config import LDAPSearch, LDAPSearchUnion, NestedActiveDirectoryGroupType


# Setup the Logging handlers
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'stream_to_console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler'
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'django_auth_ldap': {
            'handlers': ['stream_to_console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    }
}

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ['DJANGO_SECRET']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
if os.environ.get('DJANGO_DEBUG'):
    if os.environ['DJANGO_DEBUG'] == "True":
        DEBUG = True

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
AUTH_LDAP_SERVER_URI = os.environ['LDAP_URI']  # dev parameter only
AD_CERT_FILE = os.path.join(BASE_DIR, '/etc/pki/tls/certs/cert.crt')
ldap.set_option(ldap.OPT_PROTOCOL_VERSION, 3)
ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_ALLOW)
ldap.set_option(ldap.OPT_X_TLS_CACERTFILE, AD_CERT_FILE)
# LDAP_IGNORE_CERT_ERRORS = True

AUTH_LDAP_BIND_DN = os.environ['BIND_ACCOUNT']  # dev parameter only
AUTH_LDAP_BIND_PASSWORD = os.environ['BIND_PASSWD']  # dev parameter only

AUTH_LDAP_USER_SEARCH = LDAPSearchUnion(
    LDAPSearch(os.environ['LD_SEARCH1'],  # dev parameter only
               ldap.SCOPE_SUBTREE,
               "(sAMAccountName=%(user)s)"),
    LDAPSearch(os.environ['LD_SEARCH2'],  # dev parameter only
               ldap.SCOPE_SUBTREE,
               "(sAMAccountName=%(user)s)"),
)
AUTH_LDAP_ALWAYS_UPDATE_USER = True
AUTH_LDAP_USER_ATTR_MAP = {
    "first_name": "givenName",
    "last_name": "sn",
    "email": "mail"
}

AUTH_LDAP_GROUP_SEARCH = LDAPSearch(os.environ['LD_GRP_SEARCH'],  # dev parameter only
                                    ldap.SCOPE_SUBTREE,
                                    "(objectClass=group)")
AUTH_LDAP_USER_FLAGS_BY_GROUP = {
    'is_active': os.environ['LD_ACTIVE'],  # dev parameter only
    'is_staff': os.environ['LD_STAFF'],  # dev parameter only
    'is_superuser': os.environ['LD_SUPER'],  # dev parameter only
}

AUTH_LDAP_GROUP_TYPE = NestedActiveDirectoryGroupType()
AUTH_LDAP_FIND_GROUP_PERMS = True
AUTH_LDAP_REQUIRE_GROUP = os.environ['LD_ACTIVE']  # dev parameter only
AUTH_LDAP_CACHE_GROUPS = True
AUTH_LDAP_GROUP_CACHE_TIMEOUT = 3600

AUTH_LDAP_CONNECTION_OPTIONS = {
    ldap.OPT_DEBUG_LEVEL: 0,
    ldap.OPT_REFERRALS: 0,
}

AUTHENTICATION_BACKENDS = (
    'django_auth_ldap.backend.LDAPBackend',
    'django.contrib.auth.backends.ModelBackend'
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
STATIC_ROOT = os.path.join(BASE_DIR, "static/")

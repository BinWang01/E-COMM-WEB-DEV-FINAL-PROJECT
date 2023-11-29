"""
Django settings for bookr project.

Generated by 'django-admin startproject' using Django 4.0.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""
import os
#import netifaces
from pathlib import Path
from configurations import Configuration, values
import dj_database_url

class Dev(Configuration):
    # Build paths inside the project like this: os.path.join(BASE_DIR, ...)
    #BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    BASE_DIR = Path(__file__).resolve().parent.parent

    # Quick-start development settings - unsuitable for production
    # See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

    # SECURITY WARNING: keep the secret key used in production secret!
    SECRET_KEY = 'f83724fc40a4953f514da56d02dd4d38'

    # SECURITY WARNING: don't run with debug turned on in production!
    DEBUG = values.BooleanValue(True)

    # Find out what the IP addresses are at run time
    # This is necessary because otherwise Gunicorn will reject the connections
    """ def ip_addresses():
        ip_list = []
        for interface in netifaces.interfaces():
            addrs = netifaces.ifaddresses(interface)
            for x in (netifaces.AF_INET, netifaces.AF_INET6):
                if x in addrs:
                    ip_list.append(addrs[x][0]['addr'])
        return ip_list """

    #ALLOWED_HOSTS = ip_addresses()
    ALLOWED_HOSTS = ['157.245.136.116','mscisba.rocks','127.0.0.1', 'localhost']
    CSRF_TRUSTED_ORIGINS = ['https://mscisba.rocks','https://www.mscisba.rocks']

    # Application definition

    INSTALLED_APPS = [
        "data.adminconfig.DataAdminConfig",
        #'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        "data.apps.DataConfig",
        "crispy_forms",
        "crispy_bootstrap5",
        "debug_toolbar",
    ]

    STATIC_ROOT = "/home/django/django_project/django_project/static/"
    STATIC_URL = "/static/"

    MEDIA_ROOT = "/home/django/django_project/django_project/static/media"
    MEDIA_URL = "/media/"

    MIDDLEWARE = [
        "debug_toolbar.middleware.DebugToolbarMiddleware",
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ]

    ROOT_URLCONF = 'django_project.urls'

    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [os.path.join(BASE_DIR, "django_project", "templates")],
            'APP_DIRS': True,
            'OPTIONS': {
                'context_processors': [
                    'django.template.context_processors.debug',
                    'django.template.context_processors.request',
                    'django.contrib.auth.context_processors.auth',
                    'django.contrib.messages.context_processors.messages',
                ],
                'builtins':[
                    'data.templatetags.custom_tags'
                ]
            },
        },
    ]

    CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"

    CRISPY_TEMPLATE_PACK = "bootstrap5"

    #CRISPY_TEMPLATE_PACK = 'bootstrap4'

    WSGI_APPLICATION = 'django_project.wsgi.application'

    DATABASES = values.DatabaseURLValue(
        f'sqlite:///{BASE_DIR}/db.sqlite3',
        environ_prefix='DJANGO'
    )

    # Database
    # https://docs.djangoproject.com/en/2.2/ref/settings/#databases

    """ DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'django',
            'USER': 'django',
            'PASSWORD': 'cfd610d98e29e2a4d6ecb2db42087614',
            'HOST': 'localhost',
            'PORT': '5432',
            'OPTIONS': {'sslmode': 'require'},
        }
    } """

    """ DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    } """


    """ DATABASE_URL = "sqlite:///" + BASE_DIR + "db.sqlite3"
    DATABASES = {
        "default": dj_database_url.config(default=DATABASE_URL)
    } """

    # Password validation
    # https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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


    # Internationalization
    # https://docs.djangoproject.com/en/2.2/topics/i18n/

    LANGUAGE_CODE = 'en-us'

    TIME_ZONE = 'UTC'

    USE_I18N = True

    USE_L10N = True

    USE_TZ = True

    INTERNAL_IPS = ['127.0.0.1','157.245.136.116']


class Prod(Dev):
    DEBUG = False
    SECRET_KEY = values.SecretValue()
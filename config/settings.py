from pathlib import Path
import os
from psycopg2.extensions import register_adapter, AsIs


# Фикс для кодировки
def adapt_utf8(value):
    if isinstance(value, str):
        return AsIs("E'%s'" % value.replace("\\", "\\\\").replace("'", "''"))
    return value


register_adapter(str, adapt_utf8)

if os.name == 'nt':  # Для Windows
    GDAL_LIBRARY_PATH = r'C:\OSGeo4W\bin\gdal310.dll'  # Соответствует версии 3.10
    GEOS_LIBRARY_PATH = r'C:\OSGeo4W\bin\geos_c.dll'
else:
    # Линукс-контейнер
    os.environ["GDAL_LIBRARY_PATH"] = "/usr/lib/libgdal.so"

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure--)bfm)9bzk&9mqk^ywd=8gg7d6j5o@lp-m-*h@%92%cq%d3_5a'

DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',
    'trucks',
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

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'unload_db',
        'USER': 'user',
        'PASSWORD': 'password',
        'HOST': 'db',
        'PORT': '5432',
        'OPTIONS': {
            'client_encoding': 'UTF8',
            'options': '-c search_path=public',
            'connect_timeout': 5,
        },
    }
}

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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

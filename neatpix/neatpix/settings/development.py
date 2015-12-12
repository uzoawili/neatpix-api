"""
Development specific settings for this project.
"""

from django_envie.workroom import convertfiletovars
convertfiletovars()

from .base import *


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'neatpix',
        'USER': os.getenv('DATABASE_USER'),
        'PASSWORD': os.getenv('DATABASE_PASSWORD'),
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

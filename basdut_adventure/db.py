import psycopg
from django.conf import settings


def get_connection():
    return psycopg.connect(settings.DATABASE_URL)
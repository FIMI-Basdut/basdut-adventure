import psycopg
from django.conf import settings
from django.db import connection, InternalError, DatabaseError, transaction


def get_connection():
    return psycopg.connect(settings.DATABASE_URL)

def execute_query(query, params=None, fetch=False):
    try:
        with transaction.atomic():
            with connection.cursor() as cursor:
                cursor.execute("SET search_path TO TikTakTuk, public;")
                cursor.execute(query, params)
                if fetch:
                    columns = [col[0] for col in cursor.description]
                    return [dict(zip(columns, row)) for row in cursor.fetchall()]
    except Exception as e:
        print(f"Error: {e}")
        return None
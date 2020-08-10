from datetime import datetime, timezone

from django.db import connection


def get_time_difference(timestamp):
    difference = datetime.now(timezone.utc) - timestamp
    if difference.days:
        return str(difference.days) + ' days'
    else:
        hours = difference.seconds / (60 * 60)
        if hours > 1:
            return str(round(hours)) + ' hours'
        else:
            minutes = difference.seconds / 60
            if minutes > 1:
                return str(round(minutes)) + ' minutes'

    return str(round(difference.seconds)) + ' seconds'


def success_object(status, msg, msg_data):
    return {'status': status, msg: msg_data}


def failed_object(status, msg_data):
    return {'status': status, "msg": msg_data}


def dict_fetch_all(query):
    "Return all rows from a cursor as a dict"
    with connection.cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()
        if len(rows):
            columns = [col[0] for col in cursor.description]
            results = [dict(zip(columns, row))for row in rows]
        else:
            results = {}

    return results
from datetime import datetime, timezone


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


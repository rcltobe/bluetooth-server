from datetime import datetime, timedelta, timezone


def datetime_now():
    t_delta = timedelta(hours=9)
    JST = timezone(t_delta, 'JST')
    now = datetime.now(JST)
    return now


def datetime_today():
    now = datetime_now()
    return now.replace(hour=0, minute=0, second=0, microsecond=0)


def is_same_day(a: datetime, b: datetime):
    return a.year == b.year and \
           a.month == b.month and \
           a.day == b.day

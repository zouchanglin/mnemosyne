import re
from datetime import datetime
import pytz


def is_chinese(text):
    pattern = re.compile(r'[\u4e00-\u9fa5]+')
    result = pattern.search(text)
    return result is not None


def is_english(text):
    pattern = re.compile(r'[a-zA-Z]+')
    result = pattern.search(text)
    return result is not None


def get_now_time():
    return datetime.now(pytz.timezone('Asia/Shanghai'))


def get_now_timestamp():
    return int(get_now_time().timestamp())


def get_now_timestamp_milli():
    return int(get_now_time().timestamp() * 1000)


def get_today_end_timestamp():
    today = datetime.now(pytz.timezone('Asia/Shanghai'))
    return int(datetime(today.year, today.month, today.day, 23, 59, 59, 999999).timestamp())


def get_n_days_end_timestamp(n):
    """
    获得n天后的23:59:59.999999的时间戳
    :param n: >0表示n天后，<0表示n天前
    :return:
    """
    today = datetime.now(pytz.timezone('Asia/Shanghai'))
    return int(datetime(today.year, today.month, today.day, 23, 59, 59, 999999).timestamp()) + n * 24 * 60 * 60


def timestamp_2_datetime(ts):
    return datetime.fromtimestamp(ts, pytz.timezone('Asia/Shanghai'))

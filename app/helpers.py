from datetime import datetime, timedelta

from dateutil.parser import parse


def day_of_year_getter(date_vals):
    # takes in an object with a list stored in the values attribute
    str_list = date_vals.values
    rt_list = []
    for date_str in str_list:
        date_format = '%m-%d-%Y'
        current_date = datetime.strptime(date_str, date_format)
        # day_delta = current_date - START_DATE
        day_delta = current_date.timetuple().tm_yday
        rt_list.append(day_delta)
    return rt_list


def date_transformer(date_str):
    # parses string to create date obj
    new_date = parse(date_str)
    return new_date


def single_day_oy_getter(y, m, d):
    # takes in month day and year vals
    date_ = datetime(y, m, d)
    day_delta = date_.timetuple().tm_yday
    return day_delta


def day_of_year_add_subtract(date_str, _days):
    # takes in date string
    date_format = '%m-%d-%Y'
    current_date = datetime.strptime(date_str, date_format)
    rt_list = []
    plus_day = current_date + timedelta(days=_days)
    rt_list.append(plus_day.timetuple().tm_yday)
    minus_day = current_date - timedelta(days=_days)
    rt_list.append(minus_day.timetuple().tm_yday)
    # returns a list with 0 = plus_day and 1 = minus_day
    return rt_list


def get_add_subtract_days(month_, day_, year_, _days):
    # this will return a list of daysofyear for plotting and linear regression
    current_date = datetime(year_, month_, day_)
    rt_list = [current_date.timetuple().tm_yday]
    # adds current_date
    for d in range(1, _days + 1):
        rt_list.append((current_date + timedelta(days=d)).timetuple().tm_yday)
        rt_list.append((current_date - timedelta(days=d)).timetuple().tm_yday)
    return rt_list


class Dummy:
    def __init__(self, _val):
        self.values = []
        self.values.append(_val)

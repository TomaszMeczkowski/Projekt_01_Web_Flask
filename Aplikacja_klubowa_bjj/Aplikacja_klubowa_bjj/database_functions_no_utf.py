# -*- coding: utf-8 -*-

import datetime
import time


def month_converter(data):

    months = ["January", "February", "March", "April", "May", "June", "July", "August", "September",
              "October", "November", "December"]

    if type(data) == str and data in months:
        month = months.index(data) + 1
        return month

    elif type(data) == int:
        month = months[data - 1]
        return month

    else:
        print(u"\n**Zle uzycie funckcji month converter**\n")


def czas(dane):

    if dane == "year":
        return datetime.date.today().year  # Type INT

    elif dane == "month":
        return datetime.date.today().month  # Type INT

    elif dane == "day":
        return datetime.date.today().day

    elif dane == "hour":
        return int(time.strftime('%H', time.localtime()))

    elif dane == "min":
        return int(time.strftime('%M', time.localtime()))

    elif dane == "sec":
        return int(time.strftime('%S', time.localtime()))

    else:
        print(u"\n***Zle uzycie funkcji czasu***\n")


def mysql_data_converter(dane):
    data = dane.split("-")
    year = data[0]
    month = month_converter(int(str(int(data[1], 10))))  # Parsowanie stringa ze wzgledu na fromaty 01,02 miesiecy
    day = data[2]
    return f"{day} {month} {year}"


def data_for_user():
    day_now, month_now, year_now = czas('day'), month_converter(czas('month')), czas('year')
    return day_now, month_now, year_now

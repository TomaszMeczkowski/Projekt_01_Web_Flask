# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-

import datetime
import time


def month_converter(data):

    months = ["Styczeñ", "Luty", "Marzec", "Kwiecieñ", "Maj", "Czerwiec", "Lipiec", "Sierpieñ", "Wrzesieñ",
              "PaŸdziernik", "Listopad", "Grudzieñ"]

    if type(data) == str and data in months:
        month = months.index(data) + 1
        return month

    elif type(data) == int:
        month = months[data - 1]
        return month

    else:
        print("\n**Z³e u¿ycie funckcji month converter**\n")


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
        print("\n***Z³e u¿ycie funkcji czasu***\n")


def mysql_data_converter(dane):
    data = dane.split("-")
    year = data[0]
    month = month_converter(int(str(int(data[1], 10))))  # Parsowanie stringa ze wzglêdu na fromaty 01,02 miesiêcy
    day = data[2]
    return f"{day} {month} {year}"


def data_for_user():
    day_now, month_now, year_now = czas('day'), month_converter(czas('month')), czas('year')
    return day_now, month_now, year_now

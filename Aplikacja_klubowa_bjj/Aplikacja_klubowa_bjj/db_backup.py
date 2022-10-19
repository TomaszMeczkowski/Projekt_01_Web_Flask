import mysql.connector
from database_functions import month_converter, czas, mysql_data_converter, data_for_user
from pathlib import Path
from os import mkdir, makedirs, path, system
import numpy as np
import matplotlib.pyplot as plt
from time import sleep
import pandas as pd
import xlsxwriter
from faker import Faker
from random import choice, randint


class BazaDanych:

    def __init__(self, user, password):
        self.user = user
        self.password = password


    #def osoby_update(self, parametr, docelowa_wart, id_osoby):
    #    db, cursor_object = self.data_base_connector()
    #    zapytanie = f"UPDATE klub_zt.osoby_trenujace SET {parametr} = '{docelowa_wart}' WHERE (id = {id_osoby});"
    #    cursor_object.execute(zapytanie)
    #    db.commit()
    #    db.close()

    #def osoby_delete(self, id_osoby):
    #    db, cursor_object = self.data_base_connector()
    #    zapytanie = f"UPDATE klub_zt.osoby_trenujace SET imie = '', nazwisko = '', pas = '', belki = 0 " \
    #                f"WHERE (id = '{id_osoby}');"

    #    cursor_object.execute(zapytanie)
    #    db.commit()
    #    db.close()

    #def print_to_txt(self):

    #    db, cursor_object = self.data_base_connector()
    #    dane = "SELECT * FROM osoby_trenujace;"
    #    cursor_object.execute(dane)
    #    wyniki = cursor_object.fetchall()
    #    db.commit()
    #    db.close()

    #    day, month, year = data_for_user()
    #    hour, minutes = czas("hour"), czas("min")

    #    script_path = Path(__file__).parent.resolve()
    #    path_dir = path.join(script_path, "Wydruki")

    #    try:
    #        mkdir(path_dir)
    #    except FileExistsError:
    #        pass

    #    file = open("Wydruki/Lista_osób_trenuj¹cych.txt", "w", encoding="UTF-8")
    #    file.write(f"Data wydruku: {day} {month} {year}, "
    #               f"czas: {hour}:{minutes}  \n\n"
    #               f"\nid   imie   nazwisko   pas   belki\n\n")

    #    for i in wyniki:
    #        if i[1] == '':
    #            file.write(f"{i[0]}.\n")
    #        else:
    #            file.write(f"{i[0]}. {i[1]}, {i[2]}, {i[3]}, {i[4]}\n")

    #    file.close()

    #    system(rf"{path_dir}/Lista_osób_trenuj¹cych.txt")

    #def print_to_excel(self):
    #    db, cursor_object = self.data_base_connector()
    #    dane = "SELECT * FROM osoby_trenujace;"
    #    cursor_object.execute(dane)
    #    lista_osob = cursor_object.fetchall()
    #    db.commit()
    #    db.close()

    #    script_path = Path(__file__).parent.resolve()
    #    path_dir = path.join(script_path, "Wydruki")
    #    lista_id, lista_imion, lista_nazwisk, lista_pasow, lista_belek = [], [], [], [], []

    #    for i in lista_osob:
    #        lista_id.append(i[0])
    #        lista_imion.append(i[1])
    #        lista_nazwisk.append(i[2])
    #        lista_pasow.append(i[3])
    #        lista_belek.append(i[4])

    #    try:
    #        mkdir(path_dir)
    #    except FileExistsError:
    #        pass

    #    df = pd.DataFrame({'id': lista_id,
    #                       "Imie": lista_imion,
    #                       "Nazwisko": lista_nazwisk,
    #                       "Pas": lista_pasow,
    #                       "Belki": lista_belek})
    #    writer = pd.ExcelWriter('Wydruki/Lista_osób_trenuj¹cych.xlsx', engine='xlsxwriter')
    #    df.to_excel(writer, sheet_name='Wydruk', index=False)

    #    worksheet = writer.sheets['Wydruk']
    #    format1 = writer.book.add_format({'align': "center"})

    #    worksheet.set_column(0, 0, 5, format1)
    #    worksheet.set_column(1, 1, 10, format1)
    #    worksheet.set_column(2, 2, 15, format1)
    #    worksheet.set_column(3, 3, 15, format1)
    #    worksheet.set_column(4, 4, 8, format1)

    #    writer.close()
    #    system(rf"{path_dir}/Lista_osób_trenuj¹cych.xlsx")




    #def dane_osobowe_imie(self, id_osoby):
    #    db, cursor_object = self.data_base_connector()
    #    zapytanie = f"SELECT imie FROM osoby_trenujace WHERE id = {id_osoby} LIMIT 1"
    #    cursor_object.execute(zapytanie)
    #    dane_osobowe = cursor_object.fetchall()
    #    db.commit()
    #    db.close()

    #    try:
    #        imie = dane_osobowe[0][0]
    #    except IndexError:
    #        imie = False

    #    return imie

    #def dane_osobowe_naziwsko(self, id_osoby):
    #    db, cursor_object = self.data_base_connector()
    #    zapytanie = f"SELECT nazwisko FROM osoby_trenujace WHERE id = {id_osoby} LIMIT 1"
    #    cursor_object.execute(zapytanie)
    #    dane_osobowe = cursor_object.fetchall()
    #    db.commit()
    #    db.close()

    #    try:
    #        nazwisko = dane_osobowe[0][0]
    #    except IndexError:
    #        nazwisko = False

    #    return nazwisko

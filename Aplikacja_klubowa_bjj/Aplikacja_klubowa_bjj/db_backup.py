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

    def inicjowanie_bazy_danych(self):
        db = mysql.connector.connect(user=self.user, password=self.password, host='127.0.0.1', port=3306)
        cursor_object = db.cursor()
        cursor_object.execute("CREATE DATABASE IF NOT EXISTS klub_zt")
        db.commit()
        db.close()

    def data_base_connector(self):
        databse_connector = mysql.connector.connect(user=self.user, password=self.password, host='127.0.0.1', port=3306,
                                                    database="klub_zt")
        cursor_object_db = databse_connector.cursor()
        return databse_connector, cursor_object_db

    def inicjowanie_tabel(self):
        db, cursor_object = self.data_base_connector()

        cursor_object.execute("CREATE DATABASE IF NOT EXISTS klub_zt")

        creat_table = "CREATE TABLE IF NOT EXISTS osoby_trenujace" \
                      "(" \
                      "id INT NOT NULL AUTO_INCREMENT, " \
                      "imie VARCHAR(30) NOT NULL, " \
                      "nazwisko VARCHAR(45) NOT NULL, " \
                      "pas VARCHAR(15) NOT NULL," \
                      "belki INT NOT NULL, " \
                      "PRIMARY KEY (id), UNIQUE INDEX id_UNIQUE (id ASC) VISIBLE" \
                      ");"

        cursor_object.execute(creat_table)

        creat_table = "CREATE TABLE IF NOT EXISTS karnety" \
                      "(" \
                      "id int NOT NULL, " \
                      "aktywny_karnet tinyint NOT NULL, " \
                      "miesiac varchar(45) NOT NULL, " \
                      "typ_karnetu varchar(45) NOT NULL," \
                      "dostepne_treningi_ogolnie int NOT NULL," \
                      "pozostale_treningi_w_miesiacu int NOT NULL," \
                      "plec varchar(15), " \
                      "PRIMARY KEY (id), UNIQUE KEY id_UNIQUE (id)" \
                      ")"

        cursor_object.execute(creat_table)

        creat_table = "CREATE TABLE IF NOT EXISTS dodatkowe_info_osoby" \
                      "(" \
                      "id_osoby int NOT NULL," \
                      "pierwszy_trening DATE NOT NULL, " \
                      "data_urodzenia DATE NULL, " \
                      "PRIMARY KEY (id_osoby), " \
                      "UNIQUE INDEX id_dodatkowe_info_osoby_UNIQUE (id_osoby ASC)VISIBLE);"

        cursor_object.execute(creat_table)

        creat_table = "CREATE TABLE IF NOT EXISTS statystyki_klubowe" \
                      "(id INT NOT NULL AUTO_INCREMENT," \
                      "ilosc_wejsc INT NOT NULL," \
                      "miesiac varchar(45) NOT NULL," \
                      "rok INT NOT NULL," \
                      "PRIMARY KEY (id), UNIQUE KEY id_UNIQUE (id));"

        cursor_object.execute(creat_table)

        creat_table = "CREATE TABLE IF NOT EXISTS statystyki_osobowe" \
                      "(id INT NOT NULL AUTO_INCREMENT," \
                      "id_osoby INT NOT NULL," \
                      "id_rekordu INT NOT NULL," \
                      "ilosc_wejsc INT NOT NULL," \
                      "miesiac VARCHAR(45) NOT NULL," \
                      "rok INT NOT NULL," \
                      "PRIMARY KEY (id), UNIQUE KEY id_UNIQUE (id));"

        cursor_object.execute(creat_table)

        db.commit()
        db.close()

    def dodawanie_osob(self, imie, nazwisko, pas, belki):
        db, cursor_object = self.data_base_connector()
        zapytanie = "INSERT INTO osoby_trenujace(imie, nazwisko, pas, belki) VALUES(%s,%s,%s,%s)"
        wartosci = (imie, nazwisko, pas, belki)
        cursor_object.execute(zapytanie, wartosci)

        zapytanie = f"SELECT id FROM osoby_trenujace WHERE imie = '{imie}' AND nazwisko = '{nazwisko}';"
        cursor_object.execute(zapytanie)
        id_osoby = cursor_object.fetchall()[0][0]
        zapytanie = "INSERT INTO karnety(id, aktywny_karnet, miesiac, typ_karnetu, dostepne_treningi_ogolnie, " \
                    "pozostale_treningi_w_miesiacu) VALUES(%s,%s,%s,%s,%s,%s);"
        wartosci = (id_osoby, False, 0, 0, 0, 0)

        try:
            cursor_object.execute(zapytanie, wartosci)
        except mysql.connector.errors.IntegrityError:
            #print(f"{colored('*Error: Taka osoba istnieje juz w bazie danych*', 'red')}")
            db.close()
            return False

        db.commit()
        db.close()
        return True

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

    #def reset_bazy_danych(self):
    #    db, cursor_object = self.data_base_connector()
    #    zapytanie = f"DROP DATABASE IF EXISTS klub_zt;"

    #    cursor_object.execute(zapytanie)
    #    db.commit()
    #    db.close()

    #    self.inicjowanie_bazy_danych()
    #    self.inicjowanie_tabel()

    #def show_all_people(self):

    #    db, cursor_object = self.data_base_connector()
    #    dane = "SELECT * FROM osoby_trenujace;"
    #    cursor_object.execute(dane)
    #    wyniki = cursor_object.fetchall()
    #    db.commit()
    #    db.close()
        
    #    return wyniki
    
    #def show_all_people_sorted_by_alf_imie(self):

    #    db, cursor_object = self.data_base_connector()
    #    dane = "SELECT DISTINCT id, imie, nazwisko, pas, belki FROM osoby_trenujace ORDER BY imie;"
    #    cursor_object.execute(dane)
    #    wyniki = cursor_object.fetchall()
    #    db.commit()
    #    db.close()

    #    return wyniki

    #def show_all_people_sorted_by_alf_nazwisko(self):

    #    db, cursor_object = self.data_base_connector()
    #    dane = "SELECT DISTINCT id, imie, nazwisko, pas, belki FROM osoby_trenujace ORDER BY nazwisko;"
    #    cursor_object.execute(dane)
    #    wyniki = cursor_object.fetchall()
    #    db.commit()
    #    db.close()

    #    return wyniki

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

    def ticket_sell(self, id_osoby, active, month, typ, amount, plec):
        db, cursor_object = self.data_base_connector()
        zapytanie = f"UPDATE klub_zt.karnety SET aktywny_karnet = {active}, miesiac = '{month}', " \
                    f"typ_karnetu = '{typ}', dostepne_treningi_ogolnie = '{amount}'," \
                    f" pozostale_treningi_w_miesiacu = '{amount}', plec = '{plec}' WHERE (id = {id_osoby});"
        cursor_object.execute(zapytanie)
        db.commit()
        db.close()

    def auto_ticket_month_check(self):
        db, cursor_object = self.data_base_connector()

        zapytanie = f"SELECT id FROM karnety WHERE aktywny_karnet = 1;"
        cursor_object.execute(zapytanie)
        wyniki = cursor_object.fetchall()
        db.commit()
        db.close()

        lista_aktywnych_id = []
        for i in wyniki:
            lista_aktywnych_id.append(i[0])

        current_month = month_converter(czas("month"))

        db, cursor_object = self.data_base_connector()

        zapytanie = f"SELECT miesiac FROM karnety WHERE aktywny_karnet = 1 LIMIT 1;"
        cursor_object.execute(zapytanie)
        wyniki = cursor_object.fetchall()
        db.commit()
        db.close()

        try:
            month_data = wyniki[0][0]
        except IndexError:
            month_data = None

        if month_data == current_month:
            pass
        else:
            for i in lista_aktywnych_id:
                db, cursor_object = self.data_base_connector()
                zapytanie = f"UPDATE klub_zt.karnety SET aktywny_karnet = {False}, miesiac = '{current_month}' " \
                            f"WHERE (id = {i});"

                cursor_object.execute(zapytanie)
                db.commit()
                db.close()

    def key_giveaway(self, id_osoby):
        db, cursor_object = self.data_base_connector()
        zapytanie = f"SELECT aktywny_karnet, dostepne_treningi_ogolnie, pozostale_treningi_w_miesiacu " \
                    f"FROM karnety WHERE id = {id_osoby};"
        cursor_object.execute(zapytanie)
        wynik = cursor_object.fetchall()
        db.commit()
        db.close()

        active = bool(wynik[0][0])
        amount_left = wynik[0][2] - 1
        if amount_left == -1:
            active = False

        if active:
            db, cursor_object = self.data_base_connector()
            zapytanie = f"UPDATE klub_zt.karnety SET pozostale_treningi_w_miesiacu = {amount_left} " \
                        f"WHERE id = {id_osoby};"
            cursor_object.execute(zapytanie)
            db.commit()
            db.close()

            self.statystyki_klubowe_wejscia()
            self.statystyki_osobowe_wejscia(id_osoby)

            #print(colored("\nMo¿na wydaæ kluczyk\n", "green"))
            
            return True

        else:
            #print(colored("\nBrak aktywnego karnetu\n", "red"))
            
            return False

    #def ticket_check(self, id_osoby):
    #    db, cursor_object = self.data_base_connector()
    #    zapytanie = f"SELECT aktywny_karnet, pozostale_treningi_w_miesiacu " \
    #                f"FROM karnety WHERE id = {id_osoby};"
    #    cursor_object.execute(zapytanie)
    #    wynik = cursor_object.fetchall()
    #    db.commit()
    #    db.close()

    #    activ = bool(wynik[0][0])
    #    amount_left = wynik[0][1]

    #    if activ and 0 < amount_left < 800:
    #        #print(f"{colored('Karnet jest aktywny', 'green')}"
    #              #f"\nPozosta³a iloœæ wejœæ do wykorzystania: {amount_left}")
    #        pass

    #    elif activ and amount_left > 800:
    #        #print(f"{colored('Karnet jest aktywny', 'green')}"
    #              #f"\nPozosta³a iloœæ wejœæ do wykorzystania: {colored('Nielimitowany dostêp', 'green')}\n")
    #        pass

    #    else:
    #        #print(f"{colored('Karnet zosta³ wykorzystany', 'red')}")
    #        pass

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

    def id_finder(self, imie, nazwisko):
        db, cursor_object = self.data_base_connector()
        zapytanie = f"SELECT id FROM osoby_trenujace WHERE imie = '{imie}' AND nazwisko = '{nazwisko}'"
        cursor_object.execute(zapytanie)
        wynik = cursor_object.fetchall()
        db.commit()
        db.close()

        try:
            id_osoby = wynik[0][0]
        except IndexError:
            id_osoby = False

        return id_osoby

    def statystyki_klubowe_wejscia(self):
        db, cursor_object = self.data_base_connector()

        month = month_converter(czas("month"))
        year = czas("year")
        zapytanie = f"SELECT id, ilosc_wejsc, miesiac, rok FROM statystyki_klubowe " \
                    f"WHERE miesiac = '{month}' AND rok = {year}"

        cursor_object.execute(zapytanie)
        wyniki = cursor_object.fetchall()

        if not wyniki:
            zapytanie = f"INSERT INTO statystyki_klubowe(ilosc_wejsc, miesiac, rok) VALUES(%s, %s, %s) "
            wartosci = (1, month, year)
            cursor_object.execute(zapytanie, wartosci)

        else:
            id_wpisu = wyniki[0][0]
            ilosc_wejsc = wyniki[0][1] + 1
            zapytanie = f"UPDATE klub_zt.statystyki_klubowe SET ilosc_wejsc = {ilosc_wejsc} WHERE (id = {id_wpisu});"
            cursor_object.execute(zapytanie)

        db.commit()
        db.close()

    #def stat_entry(self):
    #    db, cursor_object = self.data_base_connector()

    #    zapytanie = f"SELECT * FROM statystyki_klubowe;"
    #    cursor_object.execute(zapytanie)
    #    wyniki = cursor_object.fetchall()
    #    choice = True

    #    try:
    #        wyniki[0][1]
    #    except IndexError:
    #        #print(f"{colored('Brak danych w bazie', 'red')}")
    #        choice = False

    #    db.commit()
    #    db.close()

    #    if choice:
    #        print("Iloœæ wejœæ | Data")
    #        for i in wyniki:
    #            print(f"{i[1]}          | {i[2]} {i[3]}")

    def statystyki_osobowe_wejscia(self, id_osoby):
        db, cursor_object = self.data_base_connector()
        zapytanie = f"SELECT * FROM statystyki_osobowe WHERE id_osoby = {id_osoby};"
        cursor_object.execute(zapytanie)
        wyniki = cursor_object.fetchall()

        day, month, year = data_for_user()

        if not wyniki:
            zapytanie = f"INSERT INTO statystyki_osobowe(id_osoby, id_rekordu, ilosc_wejsc, miesiac, rok)" \
                        f"VALUES(%s, %s, %s, %s, %s);"
            wartosci = (id_osoby, 1, 1, month, year)
            cursor_object.execute(zapytanie, wartosci)

            zapytanie = f"INSERT INTO dodatkowe_info_osoby(id_osoby, pierwszy_trening)" \
                        f"VALUES(%s, %s);"
            month = czas("month")
            pierwszy_trening = f"{year}-{month}-{day}"
            wartosci = (id_osoby, pierwszy_trening)
            cursor_object.execute(zapytanie, wartosci)

        else:
            zapytanie = f"SELECT id_rekordu, ilosc_wejsc, id FROM statystyki_osobowe " \
                        f"WHERE miesiac = '{month}' AND rok = {year} AND id_osoby = {id_osoby} LIMIT 1;"
            cursor_object.execute(zapytanie)
            wyniki = cursor_object.fetchall()

            zapytanie = f"SELECT id_rekordu FROM statystyki_osobowe " \
                        f"WHERE (id_osoby = {id_osoby});"
            cursor_object.execute(zapytanie)
            wyniki_2 = list(cursor_object.fetchall()[0])
            id_rekordu = max(wyniki_2)

            if not wyniki:
                zapytanie = f"INSERT INTO statystyki_osobowe(id_osoby, id_rekordu, ilosc_wejsc, miesiac, rok)" \
                            f"VALUES(%s, %s, %s, %s, %s);"
                id_rekordu += 1
                wartosci = (id_osoby, id_rekordu, 1, month, year)
                cursor_object.execute(zapytanie, wartosci)

            else:
                ilosc_wejsc = wyniki[0][1] + 1
                id_input = wyniki[0][2]
                zapytanie = f"UPDATE klub_zt.statystyki_osobowe SET ilosc_wejsc = {ilosc_wejsc} " \
                            f"WHERE (id_rekordu = {id_rekordu} AND id_osoby = {id_osoby} AND id = {id_input});"
                cursor_object.execute(zapytanie)

        db.commit()
        db.close()

    #def stat_entry_by_id(self, id_osoby):
    #    db, cursor_object = self.data_base_connector()

    #    zapytanie = f"SELECT ilosc_wejsc, miesiac, rok FROM statystyki_osobowe WHERE id_osoby = {id_osoby};"
    #    cursor_object.execute(zapytanie)
    #    wyniki = cursor_object.fetchall()
    #    choice = True

    #    try:
    #        wyniki[0][1]
    #    except IndexError:
    #        #print(f"{colored('Brak danych statystycznych dla podanego id', 'red')}")
    #        choice = False

    #    db.commit()
    #    db.close()

    #    if choice:
    #        print("Iloœæ treningów | Data")
    #        counter = 0
    #        for i in wyniki:
    #            print(f" {' ':3s}  {str(i[0]):9s} | {i[1]} {i[2]}")
    #            counter += i[0]

    #        db, cursor_object = self.data_base_connector()

    #        zapytanie = f"SELECT pierwszy_trening FROM dodatkowe_info_osoby WHERE id_osoby = {id_osoby} LIMIT 1;"
    #        cursor_object.execute(zapytanie)
    #        first_day = str(cursor_object.fetchall()[0][0])
    #        first_day = mysql_data_converter(first_day)

    #        #print(f"\n£¹czna iloœæ treningów: {colored(str(counter), 'blue')}")
    #        #print(f"Pierwszy trening: {colored(str(first_day), 'blue')}")

    #        db.commit()
    #        db.close()


    #def dev_tool_statistics_01(self):
    #    db, cursor_object = self.data_base_connector()

    #    counter = 0
    #    rok = 2016  # Rok pocz¹tkowy danych

    #    for j in range(5):

    #        zapytanie = f"INSERT INTO dodatkowe_info_osoby(id_osoby, pierwszy_trening) VALUES(%s, %s)"
    #        wartosci = (j + 1, "2022-01-01")
    #        cursor_object.execute(zapytanie, wartosci)

    #        for i in range(36):
    #            id_osoby = j + 1
    #            id_rekordu = i + 1
    #            ilosc_wejsc = int(np.random.randint(low=0, high=31, size=1))

    #            if i == 0:
    #                counter = 0

    #            counter += 1
    #            if counter > 12:
    #                counter = 1
    #                rok += 1

    #            miesiac = month_converter(counter)

    #            zapytanie = f"INSERT INTO statystyki_osobowe(id_osoby, id_rekordu, ilosc_wejsc, miesiac, rok) " \
    #                        f"VALUES(%s, %s, %s, %s, %s);"
    #            wartosci = (id_osoby, id_rekordu, ilosc_wejsc, miesiac, rok)
    #            cursor_object.execute(zapytanie, wartosci)

    #    db.commit()
    #    db.close()

    #def dev_tool_osoby(self):

    #    fake_data = Faker(["pl_PL"])
    #    pasy = ["Czarny", "Br¹zowy", "Purpurowy", "Niebieski", "Bia³y"]
    #    osoby = []

    #    for i in range(100):
    #        imie = fake_data.name().split()[0]
    #        nazwisko = fake_data.name().split()[1]
    #        pas = choice(pasy)
    #        belki = randint(0, 4)
    #        osoba = [imie, nazwisko, pas, belki]
    #        osoby.append(osoba)

    #    for large_data in range(1):
    #        for i in range(0, len(osoby)):
    #            self.dodawanie_osob(osoby[i][0], osoby[i][1], osoby[i][2], osoby[i][3])

    #    # Aktywowanie karnetów dla za³adowanych osoób pierwszych osób
    #    for i in range(len(osoby) + 1):
    #        self.ticket_sell(i, True, f"{month_converter(czas('month'))}", "Open", 999, "M/K")


    #def dev_tool_klub_stat(self):

    #    db, cursor_object = self.data_base_connector()

    #    counter = 0
    #    rok = 2016  # Rok pocz¹tkowy danych

    #    for i in range(12):
    #        ilosc_wejsc = int(np.random.randint(low=0, high=31 * 60, size=1))

    #        if i == 0:
    #            counter = 0

    #        counter += 1
    #        if counter > 12:
    #            counter = 1
    #            rok += 1

    #        miesiac = month_converter(counter)

    #        zapytanie = f"INSERT INTO statystyki_klubowe(ilosc_wejsc, miesiac, rok) " \
    #                    f"VALUES(%s, %s, %s);"
    #        wartosci = (ilosc_wejsc, miesiac, rok)
    #        cursor_object.execute(zapytanie, wartosci)

    #    db.commit()
    #    db.close()

    #def plot_osoba(self, id_osoby):
    #    db, cursor_object = self.data_base_connector()

    #    zapytanie = f"SELECT ilosc_wejsc, miesiac, rok FROM statystyki_osobowe WHERE id_osoby = {id_osoby};"
    #    cursor_object.execute(zapytanie)
    #    wyniki = cursor_object.fetchall()
    #    db.commit()
    #    db.close()
    #    ilosc_wejsc, daty = [], []

    #    try:
    #        wyniki[0][0]
    #    except IndexError:
    #        #print(f"{colored('Brak danych statystycznych dla podanego id', 'red')}")
    #        return False

    #    for i in wyniki:
    #        ilosc_wejsc.append(i[0])
    #        daty.append(str(month_converter(i[1])) + "-" + str(i[2]))

    #    ilosc_wejsc = np.array(ilosc_wejsc)

    #    x, y = np.array(daty), np.array(ilosc_wejsc)

    #    fig, ax = plt.subplots()
    #    ax.plot(x, y, 'o-', linewidth=2.0)
    #    ax.set(xlabel="Data", ylabel="Iloœæ treningów", title=f"Aktywnoœæ u¿ytkownika o id = {id_osoby}")
    #    fig.autofmt_xdate()

    #    day, month, year = data_for_user()
    #    fig.text(0.8, 0.02, f"Data wydruku: {day} {month} {year}", ha='center',
    #             fontweight='light', fontsize='x-small')
    #    ax.grid()

    #    script_path = Path(__file__).parent.resolve()
    #    path_dir = path.join(script_path, "Wydruki", "Aktywnosc_personalnie")

    #    try:
    #        makedirs(path_dir)
    #    except FileExistsError:
    #        pass

    #    fig.savefig(rf"{path_dir}/aktywnosc_osoby_id = {id_osoby}.png")

    #    #print(f"\n{colored('Wykres zosta³ zapisany na dysku', 'green')}\n")
    #    plt.show()

        
    #    return True

    def plot_klub(self):
        db, cursor_object = self.data_base_connector()

        zapytanie = f"SELECT ilosc_wejsc, miesiac, rok FROM statystyki_klubowe;"
        cursor_object.execute(zapytanie)
        wyniki = cursor_object.fetchall()
        db.commit()
        db.close()

        try:
            wyniki[0][0]
        except IndexError:
            #print(f"'Brak danych statystycznych klubu")
            return False

        ilosc_wejsc, daty = [], []

        for i in wyniki:
            ilosc_wejsc.append(i[0])
            daty.append(str(month_converter(i[1])) + "-" + str(i[2]))

        x = np.array(daty)
        y = np.array(ilosc_wejsc)

        fig, ax = plt.subplots()
        ax.plot(x, y, 'o-', linewidth=2.0)
        ax.set(xlabel="Data", ylabel="Iloœæ wejœæ na sale", title=f"Aktywnoœæ klubowiczów")
        fig.autofmt_xdate()

        day, month, year = data_for_user()
        fig.text(0.8, 0.02, f"Data wydruku: {day} {month} {year}", ha='center',
                 fontweight='light', fontsize='x-small')
        ax.grid()

        script_path = Path(__file__).parent.resolve()
        path_dir = path.join(script_path, "Wydruki", "Aktywnosc_klubu")

        try:
            makedirs(path_dir)
        except FileExistsError:
            pass

        fig.savefig(rf"{path_dir}/aktywnosc_klubu.png")

        #print(f"\n{colored('Wykres zosta³ zapisany na dysku', 'green')}\n")
        plt.show()

        return True


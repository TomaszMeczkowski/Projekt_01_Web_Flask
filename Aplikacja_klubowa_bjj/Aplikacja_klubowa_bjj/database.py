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
            #print(f"{colored('*Error: Taka osoba istnieje ju� w bazie danych*', 'red')}")
            db.close()
            return False

        db.commit()
        db.close()
        return True

    def dodawanie_osob_parametry(self):
        print("__Dodawanie nowej osoby__")
        imie = input("Podaj imi� osoby trenuj�cej:\n")
        nazwisko = input("Podaj nazwisko osoby trenuj�cej:\n")

        while True:
            pas = input("Podaj kolor pasa (Czarny/Br�zowy/Purpurowy/Niebieski/Bia�y):\n").capitalize()

            pasy = ["Czarny", "Br�zowy", "Purpurowy", "Niebieski", "Bia�y"]

            if pas not in pasy:
                pass
                #print(f"\n{colored('Nie ma takiego pasa', 'red')}\n")

            else:
                break

        while True:
            try:
                belki = int(input("Podaj ilo�� belek (0-4):\n"))
                if 0 <= belki <= 4:
                    break
                else:
                    pass
                    #print(f"\n{colored('Niew�a�ciwa ilo�� belek', 'red')}\n")
            except ValueError:
                pass
                #print(f"\n{colored('Nieprawid�owe dane', 'red')}\n")

        
        print(f"\nWprowadzone dane:\n"
              f"{imie}, {nazwisko}, pas: {pas}, ilo�� belek na pasie: {belki}")

        choice = int(input(f"\n1. Zatwierdzi� \n2. Poprawi�\n0. Menu\n"))

        if choice == 1:
            return self.dodawanie_osob(imie, nazwisko, pas, belki)
        elif choice == 0:
            return False
        else:
            clear_screen()
            return self.dodawanie_osob_parametry()

    def osoby_update(self, parametr, docelowa_wart, id_osoby):
        db, cursor_object = self.data_base_connector()
        zapytanie = f"UPDATE klub_zt.osoby_trenujace SET {parametr} = '{docelowa_wart}' WHERE (id = {id_osoby});"
        cursor_object.execute(zapytanie)
        db.commit()
        db.close()

    def osoby_update_parametry(self):
        while True:
            try:
                id_osoby = int(input("\nPodaj id osoby kt�rej dane maj� zosta� zmienione:\n"))
                if type(self.dane_osobowe_imie(id_osoby)) == str:
                    break
                else:

                    #print(f"\n{colored('Brak takiej osoby w bazie danych', 'red')}\n")

                    try:
                        choice = int(input(f"\n1. Podaj nowe id"
                                           f"\n0. Powr�t\n"))
                    except ValueError:
                        choice = 1

                    if choice == 1:
                        pass
                    else:
                        id_osoby = False
                        break

            except ValueError:
                #print(f"{colored('*Error: Niew�a�ciwe dane*', 'red')}\n")
                pass

        if not id_osoby:
            return False

        while True:
            try:
                parametr = int(input("\nWybierz co ma zosta� zmienione: "
                                     "\n1.imie "
                                     "\n2.nazwisko"
                                     "\n3.pas "
                                     "\n4.belki\n"))
                if 1 <= parametr <= 4:
                    break
                else:
                    pass

            except ValueError:
                pass

        parametr_list = ["imie", "nazwisko", "pas", "belki"]
        parametr = parametr_list[parametr - 1]

        docelowa_wart = input("\nPodaj poprawne dane: \n")

        db, cursor_object = mysql.connector.connect(user=self.user, password=self.password, host='127.0.0.1', port=3306,
                                                    database="klub_zt")
        dane = f"SELECT {parametr} FROM osoby_trenujace WHERE (id = {id_osoby});"
        cursor_object.execute(dane)
        wynik = cursor_object.fetchall()
        db.commit()
        db.close()

        clear_screen()
        print(f"\n___Proponowane zmiany___"
              f"\nCo zmieniamy: {parametr}"
              f"\nStare dane: {wynik[0][0]}"
              f"\nNowe dane: {docelowa_wart}"
              f"\nid osoby kt�rej dane zostan� zmieione: {id_osoby}")

        choice = int(input(f"\n1. Zatwierdzi� \n2. Poprawi�\n0. Menu (Porzuci� zmiany)\n"))
        if choice == 1:
            self.osoby_update(parametr, docelowa_wart, id_osoby)
            return True
        elif choice == 0:
            return False
        else:
            clear_screen()
            return self.osoby_update_parametry()

    def osoby_delete(self, id_osoby):
        db, cursor_object = self.data_base_connector()
        zapytanie = f"UPDATE klub_zt.osoby_trenujace SET imie = '', nazwisko = '', pas = '', belki = 0 " \
                    f"WHERE (id = '{id_osoby}');"

        cursor_object.execute(zapytanie)
        db.commit()
        db.close()

    def osoby_delete_parametry(self):
        while True:
            try:
                id_osoby = int(input("\nPodaj id osoby kt�rej dane maj� zosta� usuni�te:\n"))
                if type(self.dane_osobowe_imie(id_osoby)) == str:
                    break
                else:
                    #print(f"\n{colored('Brak takiej osoby w bazie danych', 'red')}\n")

                    try:
                        choice = int(input(f"\n1. Podaj nowe id"
                                           f"\n0. Powr�t\n"))
                    except ValueError:
                        choice = 1

                    if choice == 1:
                        pass
                    else:
                        id_osoby = False
                        break

            except ValueError:
                #print(f"{colored('*Error: Niew�a�ciwe dane*', 'red')}\n")
                pass

        if not id_osoby:
            return False

        clear_screen()
        print(f"Dane osoby o id={id_osoby} zostan� usuni�te z bazy")

        while True:
            try:
                choice = int(input(f"\n1. Zatwierdzi� \n2. Poprawi�\n0. Menu (porzu� zmiany)\n"))
                if choice in [1, 2, 0]:
                    break
                else:
                    pass
            except ValueError:
                pass

        if choice == 1:
            self.osoby_delete(id_osoby)
            return True
        elif choice == 0:
            return False
        else:
            return self.osoby_delete_parametry()

    def reset_bazy_danych(self):
        db, cursor_object = self.data_base_connector()
        zapytanie = f"DROP DATABASE IF EXISTS klub_zt;"

        cursor_object.execute(zapytanie)
        db.commit()
        db.close()

        self.inicjowanie_bazy_danych()
        self.inicjowanie_tabel()

    def show_all_people(self):

        db, cursor_object = self.data_base_connector()
        dane = "SELECT * FROM osoby_trenujace;"
        cursor_object.execute(dane)
        wyniki = cursor_object.fetchall()
        db.commit()
        db.close()

        #print(colored(f"{'id':4s} {'Imie':11s} {'Nazwisko':18s} {'Pas':10s} Belki", 'cyan'))
        #print("_" * 50)
        for i in wyniki:
            if i[1] == '':
                print(f"{i[0]}.")
            else:
                #color_pick = color_belt_picker(i[3])
                belt = i[3]

                if i[3] == "Bia�y":
                    pass
                else:
                    while len(belt) < 19:
                        belt += " "

                print(f"{(str(i[0]) + '.'):4s} {i[1]:8s} |  {i[2]:12s}  |  {belt:14s}  |  {i[4]}")
        print("_" * 50)

    def show_all_people_sorted_by_alf_imie(self):

        db, cursor_object = self.data_base_connector()
        dane = "SELECT DISTINCT id, imie, nazwisko, pas, belki FROM osoby_trenujace ORDER BY imie;"
        cursor_object.execute(dane)
        wyniki = cursor_object.fetchall()
        db.commit()
        db.close()

        #print(colored(f"{'id':4s} {'Imie':11s} {'Nazwisko':18s} {'Pas':10s} Belki", 'cyan'))
        #print("_" * 50)
        for i in wyniki:
            if i[1] == '':
                print(f"{i[0]}.")
            else:
                
                belt = i[3]

                if i[3] == "Bia�y":
                    pass
                else:
                    while len(belt) < 19:
                        belt += " "

                print(f"{(str(i[0]) + '.'):4s} {i[1]:8s} |  {i[2]:12s}  |  {belt:14s}  |  {i[4]}")
        print("_" * 50)

    def show_all_people_sorted_by_alf_nazwisko(self):

        db, cursor_object = self.data_base_connector()
        dane = "SELECT DISTINCT id, imie, nazwisko, pas, belki FROM osoby_trenujace ORDER BY nazwisko;"
        cursor_object.execute(dane)
        wyniki = cursor_object.fetchall()
        db.commit()
        db.close()

        print(colored(f"{'id':4s} {'Imie':11s} {'Nazwisko':18s} {'Pas':10s} Belki", 'cyan'))
        print("_" * 50)
        for i in wyniki:
            if i[1] == '':
                print(f"{i[0]}.")
            else:
                color_pick = color_belt_picker(i[3])
                belt = colored(i[3], color_pick)

                if i[3] == "Bia�y":
                    pass
                else:
                    while len(belt) < 19:
                        belt += " "

                print(f"{(str(i[0]) + '.'):4s} {i[1]:8s} |  {i[2]:12s}  |  {belt:14s}  |  {i[4]}")
        print("_" * 50)

    def print_to_txt(self):

        db, cursor_object = self.data_base_connector()
        dane = "SELECT * FROM osoby_trenujace;"
        cursor_object.execute(dane)
        wyniki = cursor_object.fetchall()
        db.commit()
        db.close()

        day, month, year = data_for_user()
        hour, minutes = czas("hour"), czas("min")

        script_path = Path(__file__).parent.resolve()
        path_dir = path.join(script_path, "Wydruki")

        try:
            mkdir(path_dir)
        except FileExistsError:
            pass

        file = open("Wydruki/Lista_os�b_trenuj�cych.txt", "w", encoding="UTF-8")
        file.write(f"Data wydruku: {day} {month} {year}, "
                   f"czas: {hour}:{minutes}  \n\n"
                   f"\nid   imie   nazwisko   pas   belki\n\n")

        for i in wyniki:
            if i[1] == '':
                file.write(f"{i[0]}.\n")
            else:
                file.write(f"{i[0]}. {i[1]}, {i[2]}, {i[3]}, {i[4]}\n")

        file.close()

        system(rf"{path_dir}/Lista_os�b_trenuj�cych.txt")

    def print_to_excel(self):
        db, cursor_object = self.data_base_connector()
        dane = "SELECT * FROM osoby_trenujace;"
        cursor_object.execute(dane)
        lista_osob = cursor_object.fetchall()
        db.commit()
        db.close()

        script_path = Path(__file__).parent.resolve()
        path_dir = path.join(script_path, "Wydruki")
        lista_id, lista_imion, lista_nazwisk, lista_pasow, lista_belek = [], [], [], [], []

        for i in lista_osob:
            lista_id.append(i[0])
            lista_imion.append(i[1])
            lista_nazwisk.append(i[2])
            lista_pasow.append(i[3])
            lista_belek.append(i[4])

        try:
            mkdir(path_dir)
        except FileExistsError:
            pass

        df = pd.DataFrame({'id': lista_id,
                           "Imie": lista_imion,
                           "Nazwisko": lista_nazwisk,
                           "Pas": lista_pasow,
                           "Belki": lista_belek})
        writer = pd.ExcelWriter('Wydruki/Lista_os�b_trenuj�cych.xlsx', engine='xlsxwriter')
        df.to_excel(writer, sheet_name='Wydruk', index=False)

        worksheet = writer.sheets['Wydruk']
        format1 = writer.book.add_format({'align': "center"})

        worksheet.set_column(0, 0, 5, format1)
        worksheet.set_column(1, 1, 10, format1)
        worksheet.set_column(2, 2, 15, format1)
        worksheet.set_column(3, 3, 15, format1)
        worksheet.set_column(4, 4, 8, format1)

        writer.close()
        system(rf"{path_dir}/Lista_os�b_trenuj�cych.xlsx")

    def ticket_sell(self, id_osoby, active, month, typ, amount, plec):
        db, cursor_object = self.data_base_connector()
        zapytanie = f"UPDATE klub_zt.karnety SET aktywny_karnet = {active}, miesiac = '{month}', " \
                    f"typ_karnetu = '{typ}', dostepne_treningi_ogolnie = '{amount}'," \
                    f" pozostale_treningi_w_miesiacu = '{amount}', plec = '{plec}' WHERE (id = {id_osoby});"
        cursor_object.execute(zapytanie)
        db.commit()
        db.close()

    def ticket_sell_parametry(self):
        clear_screen()
        while True:
            try:
                id_osoby = int(input("\nPodaj id osoby kupuj�cej karnet:\n"))
                if type(self.dane_osobowe_imie(id_osoby)) == str:
                    break
                else:
                    print(f"\n{colored('Brak takiej osoby w bazie danych', 'red')}\n")

                    try:
                        choice = int(input(f"\n1. Podaj nowe id"
                                           f"\n0. Powr�t\n"))
                    except ValueError:
                        choice = 1

                    if choice == 1:
                        pass
                    else:
                        id_osoby = False
                        break

            except ValueError:
                print(f"{colored('*Error: Niew�a�ciwe dane*', 'red')}\n")
                pass

        if not id_osoby:
            return False

        month = month_converter(czas("month"))

        karnety_men = {"1 Wej�cie": [1, "30z�"],
                       "4 Wej�cia": [4, "100z�"],
                       "8 Wej��": [8, "140z�"],
                       "15 Wej��": [15, "160z�"],
                       "Dzieci 4-7 lat": [999, "120z�"],
                       "Dzieci 8-15 lat": [999, "130z�"],
                       "Open": [999, "220z�"]}

        karnety_women = {"1 Wej�cie": [1, "30z�"],
                         "4 Wej�cia": [4, "100z�"],
                         "8 Wej��": [8, "120z�"],
                         "15 Wej��": [15, "140z�"],
                         "Dzieci 4-7 lat": [999, "120z�"],
                         "Dzieci 8-15 lat": [999, "130z�"],
                         "Open": [999, "200z�"]}

        clear_screen()
        sex = input("\nK - Kobieta / M - M�czyzna\n").upper()
        clear_screen()
        print("\n\n___Dost�pne karnety___\n")
        if sex == "K" or sex == "KOBIETA":
            sex = "Kobieta"
            for i, j in karnety_women.items():
                print(f"{i} - {j[1]}")

        elif sex == "M" or sex == "MʯCZYZNA":
            sex = "M�czyzna"
            for i, j in karnety_men.items():
                print(f"{i} - {j[1]}")

        while True:
            try:
                typ = input("\nPodaj dok�adny typ karnetu do zakupu:\n").capitalize()

                if typ == "1":
                    typ = "1 Wej�cie"
                elif typ == "4":
                    typ = "4 Wej�cia"
                elif typ == "8":
                    typ = "8 Wej��"
                elif typ == "15":
                    typ = "15 Wej��"
                elif typ == "Dzieci 4-7":
                    typ = "Dziecie 4-7 lat"
                elif typ == "Dzieci 8-15":
                    typ = "Dzieci 8-15 lat"

                amount = karnety_men.get(typ)[0]
                break
            except TypeError:
                print(f"\n{colored('*Error: Niew�a�ciwe dane*', 'red')}\n")

        clear_screen()
        print(f"\n___Wprowadzone dane___\n"
              f"\nid osoby kupuj�cej karnet: {id_osoby}"
              f"\nP�e�: {sex}"
              f"\nTyp karnetu: {typ}"
              f"\nMiesi�c: {month}"
              f"\n")

        while True:
            try:
                choice = int(input("\n1. Zatwierd�"
                                   "\n2. Popraw"
                                   "\n"
                                   "\n0. Menu (porzu� zmiany)\n"))
                if choice in [1, 2, 0]:
                    break
                else:
                    pass
            except ValueError:
                pass

        if choice == 1:
            self.ticket_sell(id_osoby, True, month, typ, amount, sex)
            return True
        elif choice == 0:
            return False
        else:
            return self.ticket_sell_parametry()

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

            print(colored("\nMo�na wyda� kluczyk\n", "green"))
            
            return True

        else:
            print(colored("\nBrak aktywnego karnetu\n", "red"))
            
            return False

    def key_giveaway_parametry(self):
        while True:
            try:
                id_osoby = int(input("\nPodaj id osoby trenuj�cej:\n"))
                if type(self.dane_osobowe_imie(id_osoby)) == str:
                    break
                else:
                    print(f"\n{colored('Brak takiej osoby w bazie danych', 'red')}\n")

                    try:
                        choice = int(input(f"\n1. Podaj nowe id"
                                           f"\n0. Powr�t\n"))
                    except ValueError:
                        choice = 1

                    if choice == 1:
                        pass
                    else:
                        id_osoby = False
                        break

            except ValueError:
                print(f"{colored('*Error: Niew�a�ciwe dane*', 'red')}\n")
                pass

        if not id_osoby:
            return False

        return self.key_giveaway(id_osoby)

    def ticket_check(self, id_osoby):
        db, cursor_object = self.data_base_connector()
        zapytanie = f"SELECT aktywny_karnet, pozostale_treningi_w_miesiacu " \
                    f"FROM karnety WHERE id = {id_osoby};"
        cursor_object.execute(zapytanie)
        wynik = cursor_object.fetchall()
        db.commit()
        db.close()

        activ = bool(wynik[0][0])
        amount_left = wynik[0][1]

        if activ and 0 < amount_left < 800:
            print(f"{colored('Karnet jest aktywny', 'green')}"
                  f"\nPozosta�a ilo�� wej�� do wykorzystania: {amount_left}")

        elif activ and amount_left > 800:
            print(f"{colored('Karnet jest aktywny', 'green')}"
                  f"\nPozosta�a ilo�� wej�� do wykorzystania: {colored('Nielimitowany dost�p', 'green')}\n")

        else:
            print(f"{colored('Karnet zosta� wykorzystany', 'red')}")

    def ticket_check_parametry(self):
        while True:
            try:
                id_osoby = int(input("\nPodaj id osoby trenuj�cej\n"))
                if type(self.dane_osobowe_imie(id_osoby)) == str:
                    break
                else:
                    print(f"\n{colored('Brak takiej osoby w bazie danych', 'red')}\n")

                    try:
                        choice = int(input(f"\n1. Podaj nowe id"
                                           f"\n0. Powr�t\n"))
                    except ValueError:
                        choice = 1

                    if choice == 1:
                        pass
                    else:
                        id_osoby = False
                        break

            except ValueError:
                print(f"{colored('*Error: Niew�a�ciwe dane*', 'red')}\n")

        if not id_osoby:
            return False

        if type(self.dane_osobowe_imie(id_osoby)) == str and type(self.dane_osobowe_naziwsko(id_osoby)):
            print(f"W�a�ciciel karnetu: {colored(self.dane_osobowe_imie(id_osoby), 'blue')} "
                  f"{colored(self.dane_osobowe_naziwsko(id_osoby), 'blue')}\n")

            return self.ticket_check(id_osoby)

        else:
            print(f"{colored('Brak osoby o takim id w bazie danych', 'red')}")

    def dane_osobowe_imie(self, id_osoby):
        db, cursor_object = self.data_base_connector()
        zapytanie = f"SELECT imie FROM osoby_trenujace WHERE id = {id_osoby} LIMIT 1"
        cursor_object.execute(zapytanie)
        dane_osobowe = cursor_object.fetchall()
        db.commit()
        db.close()

        try:
            imie = dane_osobowe[0][0]
        except IndexError:
            imie = False

        return imie

    def dane_osobowe_naziwsko(self, id_osoby):
        db, cursor_object = self.data_base_connector()
        zapytanie = f"SELECT nazwisko FROM osoby_trenujace WHERE id = {id_osoby} LIMIT 1"
        cursor_object.execute(zapytanie)
        dane_osobowe = cursor_object.fetchall()
        db.commit()
        db.close()

        try:
            nazwisko = dane_osobowe[0][0]
        except IndexError:
            nazwisko = False

        return nazwisko

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

    def id_finder_parametry(self):
        clear_screen()
        print("\nPodaj dane osoby trenuj�cej")
        imie = input("\nImi�: ")
        nazwisko = input("Nazwisko: ")
        id_osoby = self.id_finder(imie, nazwisko)

        if id_osoby:
            print(f"\nid szukanej osoby: {colored(self.id_finder(imie, nazwisko), 'blue')}")
        else:
            print(f"\n{colored('Brak takiej osoby w bazie danych', 'red')}")

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

    def stat_entry(self):
        db, cursor_object = self.data_base_connector()

        zapytanie = f"SELECT * FROM statystyki_klubowe;"
        cursor_object.execute(zapytanie)
        wyniki = cursor_object.fetchall()
        choice = True

        try:
            wyniki[0][1]
        except IndexError:
            print(f"{colored('Brak danych w bazie', 'red')}")
            choice = False

        db.commit()
        db.close()

        if choice:
            print("Ilo�� wej�� | Data")
            for i in wyniki:
                print(f"{i[1]}          | {i[2]} {i[3]}")

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

    def stat_entry_by_id(self, id_osoby):
        db, cursor_object = self.data_base_connector()

        zapytanie = f"SELECT ilosc_wejsc, miesiac, rok FROM statystyki_osobowe WHERE id_osoby = {id_osoby};"
        cursor_object.execute(zapytanie)
        wyniki = cursor_object.fetchall()
        choice = True

        try:
            wyniki[0][1]
        except IndexError:
            print(f"{colored('Brak danych statystycznych dla podanego id', 'red')}")
            choice = False

        db.commit()
        db.close()

        if choice:
            print("Ilo�� trening�w | Data")
            counter = 0
            for i in wyniki:
                print(f" {' ':3s}  {str(i[0]):9s} | {i[1]} {i[2]}")
                counter += i[0]

            db, cursor_object = self.data_base_connector()

            zapytanie = f"SELECT pierwszy_trening FROM dodatkowe_info_osoby WHERE id_osoby = {id_osoby} LIMIT 1;"
            cursor_object.execute(zapytanie)
            first_day = str(cursor_object.fetchall()[0][0])
            first_day = mysql_data_converter(first_day)

            #print(f"\n��czna ilo�� trening�w: {colored(str(counter), 'blue')}")
            #print(f"Pierwszy trening: {colored(str(first_day), 'blue')}")

            db.commit()
            db.close()

            

    def stat_entry_by_id_parametry(self):
        while True:
            try:
                id_osoby = int(input("\nPodaj id osoby trenuj�cej\n"))
                if type(self.dane_osobowe_imie(id_osoby)) == str:
                    break
                else:
                    print(f"\n{colored('Brak takiej osoby w bazie danych', 'red')}\n")

                    try:
                        choice = int(input(f"\n1. Podaj nowe id"
                                           f"\n0. Powr�t\n"))
                    except ValueError:
                        choice = 1

                    if choice == 1:
                        pass
                    else:
                        id_osoby = False
                        break

            except ValueError:
                print(f"{colored('*Error: Niew�a�ciwe dane*', 'red')}\n")

        if not id_osoby:
            return False

        if type(self.dane_osobowe_imie(id_osoby)) == str and type(self.dane_osobowe_naziwsko(id_osoby)):
            print(f"\n\nDane u�ytkownika: {colored(self.dane_osobowe_imie(id_osoby), 'blue')} "
                  f"{colored(self.dane_osobowe_naziwsko(id_osoby), 'blue')}\n")

            self.stat_entry_by_id(id_osoby)

        else:
            print(f"{colored('Brak osoby o takim id w bazie danych', 'red')}")

    def dev_tool_statistics_01(self):
        db, cursor_object = self.data_base_connector()

        counter = 0
        rok = 2016  # Rok pocz�tkowy danych

        for j in range(5):

            zapytanie = f"INSERT INTO dodatkowe_info_osoby(id_osoby, pierwszy_trening) VALUES(%s, %s)"
            wartosci = (j + 1, "2022-01-01")
            cursor_object.execute(zapytanie, wartosci)

            for i in range(36):
                id_osoby = j + 1
                id_rekordu = i + 1
                ilosc_wejsc = int(np.random.randint(low=0, high=31, size=1))

                if i == 0:
                    counter = 0

                counter += 1
                if counter > 12:
                    counter = 1
                    rok += 1

                miesiac = month_converter(counter)

                zapytanie = f"INSERT INTO statystyki_osobowe(id_osoby, id_rekordu, ilosc_wejsc, miesiac, rok) " \
                            f"VALUES(%s, %s, %s, %s, %s);"
                wartosci = (id_osoby, id_rekordu, ilosc_wejsc, miesiac, rok)
                cursor_object.execute(zapytanie, wartosci)

        db.commit()
        db.close()

    def dev_tool_osoby(self):
        print("�adowanie os�b prefediniowanych do bazy danych...")
        # osoby = [
        #     ["Tomek", "M�czkowski", "Purpurowy", 2],
        #     ["Olga", "Zabulewicz", "Purpurowy", 2],
        #     ["Alicja", "Kardas", "Niebieski", 3],
        #     ["Ola", "Warczak", "Purpurowy", 3],
        #     ["Jacek", "Sasin", "Niebieski", 2],
        #     ["Tomek", "Kowalski", "Czarny", 2],
        #     ["Olga", "Kownacka", "Br�zowy", 4],
        #     ["Alicja", "Nazaruk", "Purpurowy", 3],
        #     ["Ola", "Warcz", "Niebieski", 3],
        #     ["Jacek", "Sass", "Bia�y", 1]
        # ]

        fake_data = Faker(["pl_PL"])
        pasy = ["Czarny", "Br�zowy", "Purpurowy", "Niebieski", "Bia�y"]
        osoby = []

        for i in range(100):
            imie = fake_data.name().split()[0]
            nazwisko = fake_data.name().split()[1]
            pas = choice(pasy)
            belki = randint(0, 4)
            osoba = [imie, nazwisko, pas, belki]
            osoby.append(osoba)

        # Je�eli chcemy wiecej powt�rze� danych trzeba zmieni� range(i) na wi�ksze i
        for large_data in range(1):
            for i in range(0, len(osoby)):
                self.dodawanie_osob(osoby[i][0], osoby[i][1], osoby[i][2], osoby[i][3])

        # Aktywowanie karnet�w dla za�adowanych oso�b pierwszych os�b
        for i in range(len(osoby) + 1):
            self.ticket_sell(i, True, f"{month_converter(czas('month'))}", "Open", 999, "M/K")

        sleep(2)

    def dev_tool_klub_stat(self):

        db, cursor_object = self.data_base_connector()

        counter = 0
        rok = 2016  # Rok pocz�tkowy danych

        for i in range(12):
            ilosc_wejsc = int(np.random.randint(low=0, high=31 * 60, size=1))

            if i == 0:
                counter = 0

            counter += 1
            if counter > 12:
                counter = 1
                rok += 1

            miesiac = month_converter(counter)

            zapytanie = f"INSERT INTO statystyki_klubowe(ilosc_wejsc, miesiac, rok) " \
                        f"VALUES(%s, %s, %s);"
            wartosci = (ilosc_wejsc, miesiac, rok)
            cursor_object.execute(zapytanie, wartosci)

        db.commit()
        db.close()

    def plot_osoba(self, id_osoby):
        db, cursor_object = self.data_base_connector()

        zapytanie = f"SELECT ilosc_wejsc, miesiac, rok FROM statystyki_osobowe WHERE id_osoby = {id_osoby};"
        cursor_object.execute(zapytanie)
        wyniki = cursor_object.fetchall()
        db.commit()
        db.close()
        ilosc_wejsc, daty = [], []

        try:
            wyniki[0][0]
        except IndexError:
            #print(f"{colored('Brak danych statystycznych dla podanego id', 'red')}")
            return False

        for i in wyniki:
            ilosc_wejsc.append(i[0])
            daty.append(str(month_converter(i[1])) + "-" + str(i[2]))

        ilosc_wejsc = np.array(ilosc_wejsc)

        x, y = np.array(daty), np.array(ilosc_wejsc)

        fig, ax = plt.subplots()
        ax.plot(x, y, 'o-', linewidth=2.0)
        ax.set(xlabel="Data", ylabel="Ilo�� trening�w", title=f"Aktywno�� u�ytkownika o id = {id_osoby}")
        fig.autofmt_xdate()

        day, month, year = data_for_user()
        fig.text(0.8, 0.02, f"Data wydruku: {day} {month} {year}", ha='center',
                 fontweight='light', fontsize='x-small')
        ax.grid()

        script_path = Path(__file__).parent.resolve()
        path_dir = path.join(script_path, "Wydruki", "Aktywnosc_personalnie")

        try:
            makedirs(path_dir)
        except FileExistsError:
            pass

        fig.savefig(rf"{path_dir}/aktywnosc_osoby_id = {id_osoby}.png")

        #print(f"\n{colored('Wykres zosta� zapisany na dysku', 'green')}\n")
        plt.show()

        
        return True

    def plot_osoba_parametry(self):
        while True:
            try:
                id_osoby = int(input("\nPodaj id osoby kt�rej aktywno�� zostanie pokazana na wykresie:\n"))
                if type(self.dane_osobowe_imie(id_osoby)) == str:
                    break
                else:
                    #print(f"\n{colored('Brak takiej osoby w bazie danych', 'red')}\n")

                    try:
                        choice = int(input(f"\n1. Podaj nowe id"
                                           f"\n0. Powr�t\n"))
                    except ValueError:
                        choice = 1

                    if choice == 1:
                        pass
                    else:
                        id_osoby = False
                        break

            except ValueError:
                #print(f"{colored('*Error: Niew�a�ciwe dane*', 'red')}\n")
                pass

        if not id_osoby:
            return False

        return self.plot_osoba(id_osoby)

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
            #print(f"{colored('Brak danych statystycznych klubu', 'red')}")
            return False

        ilosc_wejsc, daty = [], []

        for i in wyniki:
            ilosc_wejsc.append(i[0])
            daty.append(str(month_converter(i[1])) + "-" + str(i[2]))

        x = np.array(daty)
        y = np.array(ilosc_wejsc)

        fig, ax = plt.subplots()
        ax.plot(x, y, 'o-', linewidth=2.0)
        ax.set(xlabel="Data", ylabel="Ilo�� wej�� na sale", title=f"Aktywno�� klubowicz�w")
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

        #print(f"\n{colored('Wykres zosta� zapisany na dysku', 'green')}\n")
        plt.show()

        return True


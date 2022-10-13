from .database_functions_no_utf import month_converter, czas, mysql_data_converter, data_for_user
import numpy as np
#from .database_functions import month_converter, czas, mysql_data_converter, data_for_user


class BazaDanych:

    def __init__(self, mysql):

        print("DataBase log: FILE ENTERED")
        self.mysql = mysql

    def inicjowanie_tabel_bazy_danych(self):
        print("DataBase log: Inicjowanie tabel bazy danych (method ENTERED)")

        db = self.mysql.connect()
        cursor_object = db.cursor()

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
                      "miesiac int NOT NULL, " \
                      "typ_karnetu varchar(45) NOT NULL," \
                      "dostepne_treningi_ogolnie int NOT NULL," \
                      "pozostale_treningi_w_miesiacu int NOT NULL," \
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
                      "miesiac int NOT NULL," \
                      "rok INT NOT NULL," \
                      "PRIMARY KEY (id), UNIQUE KEY id_UNIQUE (id));"

        cursor_object.execute(creat_table)

        creat_table = "CREATE TABLE IF NOT EXISTS statystyki_osobowe" \
                      "(id INT NOT NULL AUTO_INCREMENT," \
                      "id_osoby INT NOT NULL," \
                      "id_rekordu INT NOT NULL," \
                      "ilosc_wejsc INT NOT NULL," \
                      "miesiac int NOT NULL," \
                      "rok INT NOT NULL," \
                      "PRIMARY KEY (id), UNIQUE KEY id_UNIQUE (id));"

        cursor_object.execute(creat_table)

        db.commit()
        db.close()

        print("DataBase log: Inicjowanie tabel bazy danych (method COMPLETED)")
        self.auto_ticket_month_check()

    def data_base_connector(self):
        db = self.mysql.connect()
        cursor_object = db.cursor()
        return db, cursor_object

    # Metoda dzialajaca (niepotrzebna w aktualnym projekcie)
    def inicjowanie_stored_procedure(self):
        db, cursor_object = self.data_base_connector()
        print("DataBase log: Inicjowanie stored procedure (method ENTERED)")

        zapytanie = "DROP PROCEDURE IF EXISTS `adding_new_person`"

        cursor_object.execute(zapytanie)

        zapytanie = """CREATE DEFINER=`root`@`localhost` PROCEDURE `adding_new_person`(
	                    IN p_name VARCHAR(40),
                        IN p_lastname VARCHAR(60),
                        IN p_belt VARCHAR(40),
                        IN p_stripe int
                    )
                    BEGIN
	                    if(select exists (select 1 from osoby_trenujace where imie = p_name AND nazwisko = p_lastname)) then
		                    select 'Uzytkownik jest juz w bazie';
	                    else
		                    insert into osoby_trenujace
                            (
			                    imie,
                                nazwisko,
                                pas,
                                belki
                            )
                            values
                            (
			                    p_name,
                                p_lastname,
                                p_belt,
                                p_stripe
                            );
                            end if ;
                    END"""

        cursor_object.execute(zapytanie)

        db.commit()
        db.close()
 
    def reset_bazy_danych(self):
        print("DataBase log: Reset bazy danych (method ENTERED)")

        db, cursor_object = self.data_base_connector()
        zapytanie = f"DROP TABLE IF EXISTS " \
                    f"osoby_trenujace, karnety, dodatkowe_info_osoby, statystyki_klubowe, statystyki_osobowe;"

        cursor_object.execute(zapytanie)
        db.commit()
        db.close()

        print("DataBase log: Reset bazy danych (method COMPLETED)")
        self.inicjowanie_tabel_bazy_danych()

    def adding_people(self, imie, nazwisko, pas, belki):
        print("DataBase log: adding people (method ENTERED)")

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
        except:
            # *Error: Taka osoba istnieje juz w bazie danych*
            db.close()
            print("DataBase log: adding people (method __FAILED__: Probably person already in DB)")
            return False

        db.commit()
        db.close()
        print("DataBase log: adding people (method COMPLETED)")
        return True

    def training_people_report(self):

        print("DataBase log: training people report (method ENTERED)")
        db, cursor_object = self.data_base_connector()
        zapytanie = "SELECT * FROM osoby_trenujace;"
        cursor_object.execute(zapytanie)
        data_lista_osob = cursor_object.fetchall()
        db.commit()
        db.close()

        print("DataBase log: training people report (method COMPLETED)")
        return data_lista_osob

    def id_finder(self, imie, nazwisko):

        print("DataBase log: id finder (method ENTERED)")

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

        print("DataBase log: id finder (method COMPLETED)")
        return id_osoby

    def key_giveaway(self, id_osoby):

        # Dodac walidacje czy taka osoba istnieje w bazie danych (glownie czy ma karnet)
        print("DataBase log: key giveaway (method ENTERED)")
        
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
            zapytanie = f"UPDATE klub_zt_flask.karnety SET pozostale_treningi_w_miesiacu = {amount_left} " \
                        f"WHERE id = {id_osoby};"
            cursor_object.execute(zapytanie)
            db.commit()
            db.close()

            self.statystyki_klubowe_wejscia()
            self.statystyki_osobowe_wejscia(id_osoby)

            print("DataBase log: key giveaway (method COMPLETED)")
            return True

        else:
            print("DataBase log: key giveaway (method COMPLETED)")
            return False

    def statystyki_klubowe_wejscia(self):

        print("DataBase log: statystyki klubowe wejscia (method ENTERED)")

        db, cursor_object = self.data_base_connector()

        month = czas("month")
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
            zapytanie = f"UPDATE klub_zt_flask.statystyki_klubowe SET ilosc_wejsc = {ilosc_wejsc} WHERE (id = {id_wpisu});"
            cursor_object.execute(zapytanie)

        db.commit()
        db.close()

        print("DataBase log: statystyki klubowe wejscia (method COMPLETED)")

    def statystyki_osobowe_wejscia(self, id_osoby):

        print("DataBase log: statystyki osobowe wejscia (method ENTERED)")

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
                zapytanie = f"UPDATE klub_zt_flask.statystyki_osobowe SET ilosc_wejsc = {ilosc_wejsc} " \
                            f"WHERE (id_rekordu = {id_rekordu} AND id_osoby = {id_osoby} AND id = {id_input});"
                cursor_object.execute(zapytanie)

        db.commit()
        db.close()

        print("DataBase log: statystyki osobowe wejscia (method COMPLETED)")


    def plot_club_activity(self):

        print("DataBase log: plot club activity 2 (method ENTERED)")

        db, cursor_object = self.data_base_connector()

        zapytanie = f"SELECT ilosc_wejsc, miesiac, rok FROM statystyki_klubowe;"
        cursor_object.execute(zapytanie)
        wyniki = cursor_object.fetchall()
        db.commit()
        db.close()

        results = dict()
        years = []

        for i in wyniki:
            year = i[2]
            if year not in years:
                years.append(year)
                results[year] = {"Labels": [], "Values": []}

        for i in wyniki:
            if i[1] < 10:
                string = "0" + str(i[1])
                results[i[2]]["Labels"].append(string + "-" + str(i[2]))
            else:
                results[i[2]]["Labels"].append(str(i[1]) + "-" + str(i[2]))

            results[i[2]]["Values"].append(i[0])

        years.reverse()
        years_descending = years
        print("DataBase log: plot club activity 2 (method COMPLETED)")

        if years == []:
            return False, False, False

        return True, results, years_descending

       

    def ticket_sell_validate(self, imie, nazwisko, karnet):
        print("DataBase log: ticket sell validate (method ENTERED)")
        user_id = self.id_finder(imie, nazwisko)
        month = czas("month")

        if karnet == "Dzieci":
            amount = 999

        elif karnet == "1":
            amount = 1

        elif karnet == "4":
            amount = 4

        elif karnet == "8":
            amount = 8

        elif karnet == 15:
            amount = 15

        elif karnet == "Open":
            amount = 999


        active = True
        typ = karnet

        print("DataBase log: ticket sell validate (method COMPLETED)")
        return self.ticket_sell(user_id, active, month, typ, amount)


    def ticket_sell(self, id_osoby, active, month, typ, amount):
        print("DataBase log: ticket sell (method ENTERED)")
        db, cursor_object = self.data_base_connector()
        zapytanie = f"UPDATE klub_zt_flask.karnety SET aktywny_karnet = {active}, miesiac = '{month}', " \
                    f"typ_karnetu = '{typ}', dostepne_treningi_ogolnie = '{amount}'," \
                    f" pozostale_treningi_w_miesiacu = '{amount}' WHERE (id = {id_osoby});"
        cursor_object.execute(zapytanie)
        db.commit()
        db.close()

        print("DataBase log: ticket sell (method COMPLETED)")
        return True

    def auto_ticket_month_check(self):
        print("DataBase log: auto ticket month check (method ENTERED)")
        db, cursor_object = self.data_base_connector()

        zapytanie = f"SELECT id FROM karnety WHERE aktywny_karnet = 1;"
        cursor_object.execute(zapytanie)
        wyniki = cursor_object.fetchall()
        db.commit()
        db.close()

        lista_aktywnych_id = []
        for i in wyniki:
            lista_aktywnych_id.append(i[0])

        current_month = czas("month")

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
                zapytanie = f"UPDATE klub_zt_flask.karnety SET aktywny_karnet = {False}, miesiac = '{current_month}' " \
                            f"WHERE (id = {i});"

                cursor_object.execute(zapytanie)
                db.commit()
                db.close()
        print("DataBase log: auto ticket month check (method COMPLETED)")

    def dev_tool_klub_stat(self):

        print("DataBase log: dev tool klub stat (method ENTERED)")
        db, cursor_object = self.data_base_connector()

        counter = 0
        rok = 2018

        for i in range(36):
            ilosc_wejsc = int(np.random.randint(low=0, high=31 * 60, size=1))

            if i == 0:
                counter = 0

            counter += 1
            if counter > 12:
                counter = 1
                rok += 1
                 
            miesiac = counter

            zapytanie = f"insert into statystyki_klubowe(ilosc_wejsc, miesiac, rok) " \
                        f"values(%s, %s, %s);"
            wartosci = (ilosc_wejsc, miesiac, rok)
            cursor_object.execute(zapytanie, wartosci)

        db.commit()
        db.close()

        print("DataBase log: dev tool klub stat (method COMPLETED)")

    def dev_tool_osoby(self):
        print("DataBase log: dev tool osoby (method ENTERED)")

        osoby = [
                 ["Tomek", "Meczkowski", "Purpurowy", 2],
                 ["Olga", "Zabulewicz", "Czarny", 2],
                 ["Jacek", "Kowalski", "Niebieski", 4],
                 ["Alicja", "Kardas", "Niebieski", 3],
                 ["Ewa", "Szklanko", "Czarny", 2]
                 ]

        for osoba in osoby:
            self.adding_people(osoba[0], osoba[1], osoba[2], osoba[3])

        print("DataBase log: dev tool osoby (method COMPLETED)")

     
    def dev_tool_statistics_for_people_01_05(self):
        print("DataBase log: dev tool osoby statystyki (method ENTERED)")

        db, cursor_object = self.data_base_connector()

        counter = 0
        rok = 2018

        for j in range(5):

            zapytanie = f"INSERT INTO dodatkowe_info_osoby(id_osoby, pierwszy_trening) VALUES(%s, %s)"
            wartosci = (j + 1, "2018-01-01")
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

                miesiac = counter

                zapytanie = f"INSERT INTO statystyki_osobowe(id_osoby, id_rekordu, ilosc_wejsc, miesiac, rok) " \
                            f"VALUES(%s, %s, %s, %s, %s);"
                wartosci = (id_osoby, id_rekordu, ilosc_wejsc, miesiac, rok)
                cursor_object.execute(zapytanie, wartosci)

        db.commit()
        db.close()

        print("DataBase log: dev tool osoby statystyki (method COMPLETED)")

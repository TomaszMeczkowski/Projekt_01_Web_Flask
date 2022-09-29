import mysql.connector


class BazaDanych:

    def __init__(self, user, password):
        self.user = user
        self.password = password
        print("DB FILE ENTERED")

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

    def dodawanie_osob(self, imie, nazwisko, pas, belki):
        db, cursor_object = self.data_base_connector()

        print("Connection Done")

        zapytanie = "INSERT INTO osoby_trenujace(imie, nazwisko, pas, belki) VALUES(%s,%s,%s,%s)"
        wartosci = (imie, nazwisko, pas, belki)
        cursor_object.execute(zapytanie, wartosci)

        zapytanie = f"SELECT id FROM osoby_trenujace WHERE imie = '{imie}' AND nazwisko = '{nazwisko}';"
        cursor_object.execute(zapytanie)
        id_osoby = cursor_object.fetchall()[0][0]
        zapytanie = "INSERT INTO karnety(id, aktywny_karnet, miesiac, typ_karnetu, dostepne_treningi_ogolnie, " \
                    "pozostale_treningi_w_miesiacu) VALUES(%s,%s,%s,%s,%s,%s);"
        wartosci = (id_osoby, False, 0, 0, 0, 0)


        print("ADDING PEOPLE IN PROGRES")

        try:
            cursor_object.execute(zapytanie, wartosci)
            db.commit()

        except mysql.connector.errors.IntegrityError:
            #Error: Taka osoba istnieje juz w bazie danych*
            db.close()
            return False

        
        db.close()
        return True


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

   


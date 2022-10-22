"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import Flask, render_template, request, json, redirect
#from flask.scaffold import _matching_loader_thinks_module_is_package
from flaskext.mysql import MySQL
from Aplikacja_klubowa_bjj import app
#from werkzeug.security import generate_password_hash
from .database import BazaDanych


mysql = MySQL()

#konfiguracja MySQL
app.config['MYSQL_DATABASE_USER']=None
app.config['MYSQL_DATABASE_PASSWORD']=None
app.config['MYSQL_DATABASE_DB']='klub_zt_flask'
app.config['MYSQL_DATABASE_HOST']='127.0.0.1'
app.config['MYSQL_DATABASE_PORT']=3306
configuration_mysql = False
mysql.init_app(app)


## Dev made log in 
#app.config['MYSQL_DATABASE_USER']="root"
#app.config['MYSQL_DATABASE_PASSWORD']="" # Dopisac aktualne haslo
#configuration_mysql = True
#database_instance = BazaDanych(mysql)
#database_instance.inicjowanie_tabel_bazy_danych()
dev_tools = True
#db_log_info = True  # Zmienic plik tak zeby db logi w terminalu pokazywaly sie w zaleznosci od tej wartosci


@app.route('/')
@app.route('/home')
def home(message=""):
    """Renders the home page."""

    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
        message = message        
    )

@app.route('/Dev_Tools', methods=('GET', 'POST'))
def dev_tools(message=""):
    """Renders the home page."""
    if configuration_mysql:

        if request.method == "POST":
            method = request.form['opcje']
            if method == "RESET":
                database_instance.reset_bazy_danych()

            elif method == "PRE-OSOBY":
                database_instance.dev_tool_osoby()

            elif method == "STAT-OSOBY":
                database_instance.dev_tool_statistics_for_people_01_05()

            elif method == "STAT-KLUB":
                database_instance.dev_tool_klub_stat()

            else:
                pass


        return render_template(
            'dev_tools.html',
            title='Dev page',
            year=datetime.now().year,
            message = message,
            dev_tools = dev_tools
            )
    else:
        return json.dumps({'message':'Musisz sie zalogowac na portalu'})

@app.route('/Konto', methods=('GET', 'POST'))
def acc():
    """Renders the home page."""

    if request.method == "POST":

        global configuration_mysql
         
        if not configuration_mysql:
            username = request.form['user_name_mysql']
            password = request.form['password_mysql']
            
            if username and password:
        
                app.config['MYSQL_DATABASE_USER']=username
                app.config['MYSQL_DATABASE_PASSWORD']=password

                try:
                    db = mysql.connect()
                    configuration_mysql = True
                    db.close()

                    global database_instance

                    database_instance = BazaDanych(mysql)
                    database_instance.inicjowanie_tabel_bazy_danych()

                    # Jezeli udalo siê zalogowac to dodac informacje 
                    return home(message="zalogowany")

                except:
                    pass
                    # Dodac informacje ze nie udalo sie zalogowac (niewlasciwe dane lub coœ innego)   
                     
    if configuration_mysql:
        return acc_on()

    return render_template(
        'account.html',
        title='Konto',
        year=datetime.now().year
    )

@app.route('/Konto', methods=('GET', 'POST'))
def acc_on():
    """Renders the contact page."""

    if request.method == "POST":

        global configuration_mysql

        app.config['MYSQL_DATABASE_USER']=None
        app.config['MYSQL_DATABASE_PASSWORD']=None
        configuration_mysql = False

        return home(message="wylogowany")

    return render_template(
        'account_on.html',
        title='Konto',
        year=datetime.now().year,
        message='',
        dev_tools = dev_tools
    )

@app.route('/kontakt')
def kontakt():
    """Renders the contact page."""
    return render_template(
        'kontakt.html',
        title='Kontakt',
        year=datetime.now().year,
        message=''
    )

@app.route('/o mnie')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='O mnie',
        year=datetime.now().year,
        message=''
    )

@app.route('/obsluga_wydawanie', methods=('GET', 'POST'))
def obsluga_wyd():
    """Renders the about page."""
    message = False
    data = ""

    if not configuration_mysql:
        return acc()
    
    if request.method == "POST":
        name = request.form['name']
        last_name = request.form['last_name']
        

        user_id = database_instance.id_finder(name, last_name)
        message = True

        if user_id:
            
            if database_instance.key_giveaway(user_id):
                data = "succes"

            else:
                data = "failed"

        else:
            data = "missing person"


    return render_template(
        'obsluga_klienta/obsluga_wydawanie.html',
        title='Obsluga klienta',
        year=datetime.now().year,
        message=message,
        data = data
    )

@app.route('/obsluga_sprzedaz', methods=('GET', 'POST'))
def obsluga_sell():
    """Renders the about page."""
    message = ""

    if not configuration_mysql:
        return acc()

    if request.method == "POST":
        name = request.form['name_selling_ticket']
        last_name = request.form['last_name_selling_ticket']
        karnet = request.form['karnet']

        if database_instance.ticket_sell_validate(name, last_name, karnet):
            message = "sold"
            # Dodaæ komunikat ¿e uda³o siê sprzedaæ

        else:
            message = "failed"
            # Nie ma takiej osoby w bazie
            

    return render_template(
        'obsluga_klienta/obsluga_sprzedaz.html',
        title='Obsluga klienta',
        year=datetime.now().year,
        message=message
    )

@app.route('/obsluga_check', methods=('GET', 'POST'))
def obsluga_check():
    """Renders the about page."""
    data = False
    imie = ""
    nazwisko = ""

    if not configuration_mysql:
        return acc()

    if request.method == "POST":
        imie = request.form['name']
        nazwisko = request.form['last_name']

        if imie and nazwisko:
            user_id = database_instance.id_finder(imie, nazwisko)

            if user_id:
                data = database_instance.ticket_check(user_id)

            else:
               data = True, -1



    return render_template(
        'obsluga_klienta/obsluga_check.html',
        title='Obsluga klienta',
        year=datetime.now().year,
        data=data,
        imie = imie,
        nazwisko = nazwisko
    )

@app.route('/obsluga_id_finder', methods=('GET', 'POST'))
def obsluga_id_finder():
    """Renders the about page."""

    message = False

    if not configuration_mysql:
        return acc()

    if request.method == "POST":
        imie = request.form['name']
        nazwisko = request.form['last_name']

        db = mysql.connect()
        cursor = db.cursor()
        zapytanie = f"SELECT id FROM osoby_trenujace WHERE imie = '{imie}' AND nazwisko = '{nazwisko}'"
        cursor.execute(zapytanie)
        result = cursor.fetchall()
        db.commit()
        db.close()

        if imie and nazwisko:
            try:
                user_id = result[0][0]
                message = (True, True, imie, nazwisko, user_id)

            except IndexError:
                message = (True, False)
            
    return render_template(
        'obsluga_klienta/obsluga_id_finder.html',
        title='Obsluga klienta',
        year=datetime.now().year,
        message=message
    )        

@app.route('/baza_dodaj_osobe', methods=('GET', 'POST'))
def baza_dodaj_osobe():
    """Renders the about page."""
    message = ""
    data = None

    if not configuration_mysql:
        return acc()

    if request.method == "POST":
        name = request.form['name']
        last_name = request.form['last_name']
        belt = request.form['pas']
        stripe = request.form['belki']        

        if name and last_name and belt and stripe:
            
            if database_instance.adding_people(name, last_name, belt, stripe):
                message = "added"
                data = name, last_name
                #"Uzytkownik zostal pomyslnie dodany bo bazy"
            
            else:
                message = "error"
                #"*ERROR* : Uzytkownik juz znajduje sie bazie danych"
        
    return render_template(
        'baza_danych/baza_dodaj_osobe.html',
        title='Baza danych',
        year=datetime.now().year,
        message = message,
        data = data
    )

@app.route('/baza_poprawianie', methods=('GET', 'POST'))
def baza_popraw():
    """Renders the about page."""
    person_found, decision = False, False

    if not configuration_mysql:
        return acc()

    if request.method == "POST":

        user_number = request.form.get('user_id')

        if user_number:
            
            if database_instance.id_validator(user_number):
                user_id = user_number
                decision, imie, nazwisko, pas, belki = database_instance.dane_osobwe(user_id)

                if user_id:
                    person_found = True
                    return baza_popraw_cd(imie, nazwisko, pas, belki, user_id)

            else:
                # Nie ma takiej osoby, zwracamy komunikat
                decision = True

    return render_template(
        'baza_danych/baza_popraw_dane_osoby.html',
        title='Baza danych',
        year=datetime.now().year,
        osoba = person_found,
        decision = decision
    )

@app.route('/baza_poprawianie_cd', methods=('GET', 'POST'))
def baza_popraw_cd(imie, nazwisko, pas, belki, user_id):
    """Renders the about page."""

    if not configuration_mysql:
        return acc()

    if request.method == "POST":
        parametr = request.form.get('parametr')
        new_data = request.form.get('new_data')

        print(parametr, new_data)

        if parametr and new_data:
            if database_instance.osoby_update(parametr, new_data, user_id):
                # Tutaj odpalamy powiadomienie ¿e wszystko siê uda³o
                pass
            
    return render_template(
        'baza_danych/baza_popraw_dane_osoby_cd.html',
        title='Baza danych',
        year=datetime.now().year,
        imie = imie,
        nazwisko = nazwisko,
        pas = pas,
        belki = belki
    )

@app.route('/baza_pokaz')
def baza_pokaz():
    """Renders the about page."""

    if not configuration_mysql:
        return acc()

    data_lista_osob = database_instance.training_people_report()

    return render_template(
        'baza_danych/baza_pokaz_wszystkich.html',
        title='Baza danych',
        year=datetime.now().year,
        message='',
        headings = ("Id", "Imie", "Nazwisko", "Pas", "Belki"),
        data = data_lista_osob
    )

@app.route('/baza_usun')
def baza_usun():
    """Renders the about page."""

    if not configuration_mysql:
        return acc()

    return render_template(
        'baza_danych/baza_usun_dane_osoby.html',
        title='Baza danych',
        year=datetime.now().year,
        message=''
    )

@app.route('/statystyki_klubu', methods=('GET', 'POST'))
def statystyki_klubu():
    """Renders the about page."""

    if not configuration_mysql:
        return acc()
    
    choice, data, years = database_instance.plot_club_activity()

    return render_template(
        'statystyki/statystyki_klub.html',
        title='Statystyki',
        year=datetime.now().year,
        choice = choice,
        data = data,
        years = years
    )

@app.route('/statystyki', methods=('GET', 'POST'))
def statystyki_osob():
    """Renders the about page."""

    choice, data, years, total = False, None, None, None
    missing_person = True
    name, last_name, user_belt, user_stripe = None, None, None, None

    if not configuration_mysql:
        return acc()

    if request.method == "POST":
        name = request.form['name']
        last_name = request.form['last_name']

        user_id = database_instance.id_finder(name, last_name)
        user_belt = database_instance.belt_finder(name, last_name)
        user_stripe = database_instance.stripe_finder(name, last_name)

        if user_id:
            missing_person = False
            choice, data, years, total = database_instance.plot_user_activity(user_id)

        else:
            choice = True

    return render_template(
        'statystyki/statystyki_osoby.html',
        title='Statystyki',
        year=datetime.now().year,
        choice = choice,
        data = data,
        years = years,
        total = total,
        missing_person = missing_person,
        imie = name,
        nazwisko = last_name,
        pas = user_belt,
        belki = user_stripe
    )

@app.route('/projekt info')
def about_project():
    """Renders the about page."""
    return render_template(
        'o_projekcie.html',
        title='O projekcie',
        year=datetime.now().year,
        message=''
    )
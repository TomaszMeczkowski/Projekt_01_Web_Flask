"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import Flask, render_template, request, json
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
#dev_tools = True
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
                    return home(message="Udalo sie zalogowac")

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

        return home(message="Zostales wylogowany")

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

    if not configuration_mysql:
        return acc()
    
    if request.method == "POST":
        name = request.form['name']
        last_name = request.form['last_name']
        #user_id = request.form['user_id']   # Wylaczono z uzytku lacznie z html. obsluga_wydawanie (input field)

        user_id = database_instance.id_finder(name, last_name)

        if user_id:
            # JEST TAKA OSOBA

            if database_instance.key_giveaway(user_id):
                # Kluczyk wydany
                pass
            else:
                # Karnet nieaktywny
                pass

        else:
            pass
            # Nie ma takiej osoby


    return render_template(
        'obsluga_klienta/obsluga_wydawanie.html',
        title='Obsluga klienta',
        year=datetime.now().year,
        message='',
    )

@app.route('/obsluga_sprzedaz', methods=('GET', 'POST'))
def obsluga_sell():
    """Renders the about page."""

    if not configuration_mysql:
        return acc()

    if request.method == "POST":
        print("DEBUG: POST METHOD ENTERED")
        name = request.form['name_selling_ticket']
        last_name = request.form['last_name_selling_ticket']
        karnet = request.form['karnet']

        print("DEBUG: REQUEST FORM COMPLETED")

        if database_instance.ticket_sell_validate(name, last_name, karnet):
            return json.dumps({'message':'Sprzedano karnet'})
            # Dodaæ komunikat ¿e uda³o siê sprzedaæ
            

    return render_template(
        'obsluga_klienta/obsluga_sprzedaz.html',
        title='Obsluga klienta',
        year=datetime.now().year,
        message=''
    )

@app.route('/obsluga_check')
def obsluga_check():
    """Renders the about page."""

    if not configuration_mysql:
        return acc()

    return render_template(
        'obsluga_klienta/obsluga_check.html',
        title='Obsluga klienta',
        year=datetime.now().year,
        message=''
    )

@app.route('/obsluga_id_finder', methods=('GET', 'POST'))
def obsluga_id_finder():
    """Renders the about page."""

    message = ""

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
    
    if not configuration_mysql:
        return acc()

    if request.method == "POST":
        name = request.form['name']
        last_name = request.form['last_name']
        belt = request.form['pas']
        stripe = request.form['belki']        

        if name and last_name and belt and stripe:
            
            if database_instance.adding_people(name, last_name, belt, stripe):
                return json.dumps({'message':'User created succesfully'})
            else:
                return json.dumps({'error':'User already in DB or another error occur'})
        
    return render_template(
        'baza_danych/baza_dodaj_osobe.html',
        title='Baza danych',
        year=datetime.now().year,
        message=''
    )

@app.route('/baza_poprawianie')
def baza_popraw():
    """Renders the about page."""

    if not configuration_mysql:
        return acc()

    return render_template(
        'baza_danych/baza_popraw_dane_osoby.html',
        title='Baza danych',
        year=datetime.now().year,
        message=''
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
    
    choice, data, years = database_instance.plot_club_activity_2()

    return render_template(
        'statystyki/statystyki_klub.html',
        title='Statystyki',
        year=datetime.now().year,
        choice = choice,
        data = data,
        years = years
    )

@app.route('/statystyki')
def statystyki_osob():
    """Renders the about page."""

    if not configuration_mysql:
        return acc()

    return render_template(
        'statystyki/statystyki_osoby.html',
        title='Statystyki',
        year=datetime.now().year
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
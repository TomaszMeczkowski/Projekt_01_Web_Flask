"""
Routes and views for the flask application.
"""

from cgitb import reset
from datetime import datetime
from email import message
from pkgutil import get_loader
from flask import Flask, render_template, request
from flask.scaffold import _matching_loader_thinks_module_is_package
from flaskext.mysql import MySQL
from Aplikacja_klubowa_bjj import app
from werkzeug.security import generate_password_hash
#from .database import BazaDanych
#import mysql.connector

mysql = MySQL()

#konfiguracja MySQL
app.config['MYSQL_DATABASE_USER']=None
app.config['MYSQL_DATABASE_PASSWORD']=None
app.config['MYSQL_DATABASE_DB']='klub_zt'
app.config['MYSQL_DATABASE_HOST']='127.0.0.1'
app.config['MYSQL_DATABASE_PORT']=3306
configuration_mysql = False
mysql.init_app(app)


## Dev made log in 
#app.config['MYSQL_DATABASE_USER']="root"
#app.config['MYSQL_DATABASE_PASSWORD']=None  # Dopisac aktualne haslo
#configuration_mysql = True

## Przykladowe zapytanie do bazy
#conn = mysql.connect()
#cursor = conn.cursor()
#imie = "Natasza"
#nazwisko = "Bruno"
#zapytanie = f"SELECT id FROM osoby_trenujace WHERE imie = '{imie}' AND nazwisko = '{nazwisko}'"
#cursor.execute(zapytanie)
#user_id = cursor.fetchall()
#print(user_id[0][0])



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
                    conn = mysql.connect()
                    configuration_mysql = True

                    # Jezeli udalo siê zalogowac to dodac informacje 
                    return home(message="Udalo sie zalogowac")

                except:
                    pass
                    # Dodac informacje ze nie udalo sie zalogowac (niewlasciwe dane)       

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
        message=''
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
        pass
        #name = request.form['name']
        #last_name = request.form['last_name']
        #user_id = request.form['user_id']

        # Metoda podejmujaca decyzje co dalej majac juz dane 

    return render_template(
        'obsluga_klienta/obsluga_wydawanie.html',
        title='Obsluga klienta',
        year=datetime.now().year,
        message='',
    )

@app.route('/obsluga_sprzedaz')
def obsluga_sell():
    """Renders the about page."""

    if not configuration_mysql:
        return acc()

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

        conn = mysql.connect()
        cursor = conn.cursor()
        zapytanie = f"SELECT id FROM osoby_trenujace WHERE imie = '{imie}' AND nazwisko = '{nazwisko}'"
        cursor.execute(zapytanie)
        result = cursor.fetchall()
       
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
            

            conn = mysql.connect()
            cursor = conn.cursor()

            cursor.callproc('adding_new_person', (name, last_name, belt, stripe))
            data = cursor.fetchall()

            if len(data) is 0:
                conn.commit()
                return json.dumps({'message':'User created succesfully'})
            else:
                return json.dumps({'error':str(data[0])})

            # Stronka po odpaleniu dodawaniu nowych osób dochodzi tutaj ale nie dodaje mi osoby do bazy
            # TUTAJ KONTYNUOWAÆ PRACE , NA GÓRZE DODAÆ HAS£O DO MySQL 
            # stored procedure sprawdzone (dzia³a jak siê u¿yje bezpoœrednio w mysql-u)
            # kopia stored porcedure jest w tym samym folderze co projekt

            # RUSZY£O !!!! Brakowa³o commita idioto
            # Ale nie chce mi ruszaæ jak pobieram dane z okienek wybieralnych belt, stripe trzeb coœ tam naprawiæ

        else:
            return json.dumps({'html':'<span>Wypelnij wszystkie pola!</span>'})

        
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

    conn = mysql.connect()
    cursor = conn.cursor()
    zapytanie = "SELECT * FROM osoby_trenujace;"
    cursor.execute(zapytanie)
    data_lista_osob = cursor.fetchall()

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

    return render_template(
        'statystyki/statystyki_klub.html',
        title='Statystyki',
        year=datetime.now().year
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
"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template
from Aplikacja_klubowa_bjj import app

@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
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

@app.route('/obsluga_wydawanie')
def obsluga_wyd():
    """Renders the about page."""
    return render_template(
        'obsluga_klienta/obsluga_wydawanie.html',
        title='Obsluga klienta',
        year=datetime.now().year,
        message=''
    )

@app.route('/obsluga_sprzedaz')
def obsluga_sell():
    """Renders the about page."""
    return render_template(
        'obsluga_klienta/obsluga_sprzedaz.html',
        title='Obsluga klienta',
        year=datetime.now().year,
        message=''
    )

@app.route('/obsluga_check')
def obsluga_check():
    """Renders the about page."""
    return render_template(
        'obsluga_klienta/obsluga_check.html',
        title='Obsluga klienta',
        year=datetime.now().year,
        message=''
    )

@app.route('/obsluga_id_finder')
def obsluga_id_finder():
    """Renders the about page."""
    return render_template(
        'obsluga_klienta/obsluga_id_finder.html',
        title='Obsluga klienta',
        year=datetime.now().year,
        message=''
    )

@app.route('/baza_dodaj_osobe')
def baza_dodaj_osobe():
    """Renders the about page."""
    return render_template(
        'baza_danych/baza_dodaj_osobe.html',
        title='Baza danych',
        year=datetime.now().year,
        message=''
    )

@app.route('/baza_poprawianie')
def baza_popraw():
    """Renders the about page."""
    return render_template(
        'baza_danych/baza_popraw_dane_osoby.html',
        title='Baza danych',
        year=datetime.now().year,
        message=''
    )

@app.route('/baza_pokaz')
def baza_pokaz():
    """Renders the about page."""
    return render_template(
        'baza_danych/baza_pokaz_wszystkich.html',
        title='Baza danych',
        year=datetime.now().year,
        message=''
    )

@app.route('/baza_usun')
def baza_usun():
    """Renders the about page."""
    return render_template(
        'baza_danych/baza_usun_dane_osoby.html',
        title='Baza danych',
        year=datetime.now().year,
        message=''
    )

@app.route('/statystyki_klubu')
def statystyki_klubu():
    """Renders the about page."""
    return render_template(
        'statystyki/statystyki_klub.html',
        title='Statystyki',
        year=datetime.now().year,
        message=''
    )

@app.route('/statystyki')
def statystyki_osob():
    """Renders the about page."""
    return render_template(
        'statystyki/statystyki_osoby.html',
        title='Statystyki',
        year=datetime.now().year,
        message=''
    )
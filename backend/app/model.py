from main import db

class Klinika(db.Model):
    _tablename_ = 'klinika'
    id_kliniki = db.Column(db.Integer, primary_key=True, nullable=False)
    nazwa = db.Column(db.String(50), nullable=False)
    id_adresu = db.Column(db.Integer, db.ForeignKey('adresy.id_adresu'), nullable=False)

    pracownicy = db.relationship('Pracownik', back_populates='klinika', lazy=True)
    wlasciciele = db.relationship('Wlasciciele', back_populates='klinika', lazy=True)

class Wlasciciele(db.Model):
    _tablename_ = 'wlasciciele'
    id_wlasciciela = db.Column(db.Integer, primary_key=True, nullable=False)
    nazwisko = db.Column(db.String(40), nullable=False)
    imie = db.Column(db.String(20), nullable=False)
    nr_telefonu = db.Column(db.String(20))
    id_adresu = db.Column(db.Integer, db.ForeignKey('adresy.id_adresu'), nullable=False)
    id_kliniki = db.Column(db.Integer, db.ForeignKey('klinika.id_kliniki'), nullable=False)

    klinika = db.relationship('Klinika', back_populates='wlasciciele')

class Adresy(db.Model):
    _tablename_ = 'adresy'
    id_adresu = db.Column(db.Integer, primary_key=True, nullable=False)
    miasto = db.Column(db.String(35), nullable=False)
    ulica = db.Column(db.String(40))
    nr_lokalu = db.Column(db.String(5), nullable=False)
    id_poczty = db.Column(db.Integer, db.ForeignKey('poczty.id_poczty'), nullable=False)

    adresy_wlasciciele = db.relationship('Wlasciciele', backref='adres', lazy=True)
    adresy_pracownicy = db.relationship('Pracownik', backref='adres', lazy=True)
    adresy_klienci = db.relationship('Klienci', backref='adres', lazy=True)

class Poczty(db.Model):
    _tablename_ = 'poczty'
    id_poczty = db.Column(db.Integer, primary_key=True, nullable=False)
    kod_pocztowy = db.Column(db.String(6), nullable=False)
    poczta = db.Column(db.String(30), nullable=False)

    poczty_adresy = db.relationship('Adresy', backref='poczta', lazy=True)

class Pracownik(db.Model):
    _tablename_ = 'pracownik'
    id_pracownika = db.Column(db.Integer, primary_key=True, nullable=False)
    nazwisko = db.Column(db.String(40), nullable=False)
    imie = db.Column(db.String(20), nullable=False)
    data_urodzenia = db.Column(db.DateTime, nullable=False)
    plec = db.Column(db.String(1), nullable=False)
    data_zatrudnienia = db.Column(db.DateTime, nullable=False)
    nr_telefonu = db.Column(db.String(20))
    pesel = db.Column(db.String(11))
    data_zwolnienia = db.Column(db.DateTime)
    id_stanowiska = db.Column(db.Integer, db.ForeignKey('stanowiska.id_stanowiska'), nullable=False)
    id_adresu = db.Column(db.Integer, db.ForeignKey('adresy.id_adresu'), nullable=False)
    id_kliniki = db.Column(db.Integer, db.ForeignKey('klinika.id_kliniki'), nullable=False)

    klinika = db.relationship('Klinika', back_populates='pracownicy')

class PracownicyKliniki(db.Model):
    _tablename_ = 'pracownicy_kliniki'
    id_pracownika = db.Column(db.Integer, db.ForeignKey('pracownik.id_pracownika'), primary_key=True, nullable=False)
    godziny_pracy_od = db.Column(db.DateTime, nullable=False)
    godziny_pracy_do = db.Column(db.DateTime, nullable=False)

class Stanowiska(db.Model):
    _tablename_ = 'stanowiska'
    id_stanowiska = db.Column(db.Integer, primary_key=True, nullable=False)
    nazwa_stanowiska = db.Column(db.String(30), nullable=False)
    wynagrodzenie = db.Column(db.Numeric(10, 2))

    pracownicy = db.relationship('Pracownik', backref='stanowisko', lazy=True)

class Weterynarze(db.Model):
    _tablename_ = 'weterynarze'
    id_pracownika = db.Column(db.Integer, db.ForeignKey('pracownik.id_pracownika'), primary_key=True, nullable=False)
    doswiadczenie = db.Column(db.String(150), nullable=False)
    kwalifikacje = db.Column(db.String(100), nullable=False)
    ocena = db.Column(db.Numeric(2,1))
    status = db.Column(db.String(20))

class WizytaWeterynarz(db.Model):
    _tablename_ = 'wizyta_weterynarz'
    id_wizyty = db.Column(db.Integer, db.ForeignKey('terminarz.id_wizyty'), primary_key=True, nullable=False)
    id_pracownika = db.Column(db.Integer, db.ForeignKey('weterynarze.id_pracownika'), primary_key=True, nullable=False)

class Terminarz(db.Model):
    _tablename_ = 'terminarz'
    id_wizyty = db.Column(db.Integer, primary_key=True, nullable=False)
    data_wizyty = db.Column(db.Date, nullable=False)
    godzina_wizyty_od = db.Column(db.DateTime, nullable=False)
    id_pupila = db.Column(db.Integer, db.ForeignKey('zwierzak.id_pupila'), nullable=False)
    id_uslugi = db.Column(db.Integer, db.ForeignKey('uslugi.id_uslugi'), nullable=False)
    opis_dolegliwosci = db.Column(db.String(500))

    usluga = db.relationship('Uslugi', backref='terminy', lazy=True)

class Uslugi(db.Model):
    _tablename_ = 'uslugi'
    id_uslugi = db.Column(db.Integer, primary_key=True, nullable=False)
    nazwa = db.Column(db.String(50), nullable=False)
    opis = db.Column(db.String(200))
    cena = db.Column(db.Numeric(5, 2))
    dostepnosc = db.Column(db.String(20))

class Klienci(db.Model):
    _tablename_ = 'klienci'
    id_klienta = db.Column(db.Integer, primary_key=True, nullable=False)
    imie = db.Column(db.String(20), nullable=False)
    nazwisko = db.Column(db.String(40), nullable=False)
    nr_telefonu = db.Column(db.String(20))
    adres_email = db.Column(db.String(40))
    haslo = db.Column(db.String(128), nullable=False)
    id_adresu = db.Column(db.Integer, db.ForeignKey('adresy.id_adresu'), nullable=False)

    zwierzaki = db.relationship('Zwierzak', backref='klient', lazy=True)

class Zwierzak(db.Model):
    _tablename_ = 'zwierzak'
    id_pupila = db.Column(db.Integer, primary_key=True, nullable=False)
    imie = db.Column(db.String(40))
    wiek = db.Column(db.String(5), nullable=False)
    opis = db.Column(db.String(200))
    plec = db.Column(db.String(6))
    id_klienta = db.Column(db.Integer, db.ForeignKey('klienci.id_klienta'), nullable=False)
    id_rasy = db.Column(db.Integer, db.ForeignKey('rasa.id_rasy'), nullable=False)

class Rasa(db.Model):
    _tablename_ = 'rasa'
    id_rasy = db.Column(db.Integer, primary_key=True, nullable=False)
    nazwa = db.Column(db.String(20), nullable=False)
    nazwa_dluga = db.Column(db.String(40))
    cechy_charakterystyczne = db.Column(db.String(2000))

    zwierzaki = db.relationship('Zwierzak', backref='rasa', lazy=True)
from main import db

class Adresy(db.Model):
    _tablename_ = 'adresy'
    id_adresu = db.Column(db.Integer, primary_key=True, nullable=False)
    miasto = db.Column(db.String(35), nullable=False)
    ulica = db.Column(db.String(40))
    nr_lokalu = db.Column(db.String(5), nullable=False)
    id_poczty = db.Column(db.Integer, db.ForeignKey('poczty.id_poczty'), nullable=False)

    adresy_weterynarze = db.relationship('Weterynarze', backref='adres', lazy=True)
    adresy_klienci = db.relationship('Klienci', backref='adres', lazy=True)

class Poczty(db.Model):
    _tablename_ = 'poczty'
    id_poczty = db.Column(db.Integer, primary_key=True, nullable=False)
    kod_pocztowy = db.Column(db.String(6), nullable=False)
    poczta = db.Column(db.String(30), nullable=False)

    poczty_adresy = db.relationship('Adresy', backref='poczta', lazy=True)

class Weterynarze(db.Model):
    _tablename_ = 'weterynarze'
    id_weterynarza = db.Column(db.Integer, primary_key=True, nullable=False)
    nazwisko = db.Column(db.String(40), nullable=False)
    imie = db.Column(db.String(20), nullable=False)
    data_urodzenia = db.Column(db.DateTime, nullable=False)
    plec = db.Column(db.String(1), nullable=False)
    data_zatrudnienia = db.Column(db.DateTime, nullable=False)
    nr_telefonu = db.Column(db.String(20))
    pesel = db.Column(db.String(11))
    doswiadczenie = db.Column(db.String(150), nullable=False)
    kwalifikacje = db.Column(db.String(100), nullable=False)
    ocena = db.Column(db.Numeric(2,1))
    wyksztalcenie = db.Column(db.String(100), nullable=False)
    id_adresu = db.Column(db.Integer, db.ForeignKey('adresy.id_adresu'), nullable=False)

class WizytaWeterynarz(db.Model):
    _tablename_ = 'wizyta_weterynarz'
    id_wizyty = db.Column(db.Integer, db.ForeignKey('terminarz.id_wizyty'), primary_key=True, nullable=False)
    id_weterynarza = db.Column(db.Integer, db.ForeignKey('weterynarze.id_weterynarza'), primary_key=True, nullable=False)

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

class Gatunki(db.Model):
    _tablename_ = 'gatunki'
    id_gatunku = db.Column(db.Integer, primary_key=True, nullable=False)
    nazwa = db.Column(db.String(50), nullable=False)

    rasy = db.relationship('Rasa', backref='gatunek', lazy=True)


class Rasa(db.Model):
    _tablename_ = 'rasa'
    id_rasy = db.Column(db.Integer, primary_key=True, nullable=False)
    rasa = db.Column(db.String(50), nullable=False)
    id_gatunku = db.Column(db.Integer, db.ForeignKey('gatunki.id_gatunku'), nullable=False)
    cechy_charakterystyczne = db.Column(db.String(2000))

    zwierzaki = db.relationship('Zwierzak', backref='rasa', lazy=True)

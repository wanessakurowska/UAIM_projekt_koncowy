from main import db

# Klinika and its related tables
class Klinika(db.Model):
    __tablename__ = 'klinika'
    id_kliniki = db.Column(db.Integer, primary_key=True, nullable=False)
    nazwa = db.Column(db.String(50), nullable=False)
    id_adresu = db.Column(db.Integer, db.ForeignKey('adresy.id_adresu'), nullable=False)

    pracownicy = db.relationship('Pracownik', back_populates='klinika', lazy=True)
    wlasciciele = db.relationship('Wlasciciele', back_populates='klinika', lazy=True)


class Wlasciciele(db.Model):
    __tablename__ = 'wlasciciele'
    id_wlasciciela = db.Column(db.Integer, primary_key=True, nullable=False)
    nazwisko = db.Column(db.String(40), nullable=False)
    imie = db.Column(db.String(20), nullable=False)
    nr_telefonu = db.Column(db.String(20))
    id_adresu = db.Column(db.Integer, db.ForeignKey('adresy.id_adresu'), nullable=False)
    id_kliniki = db.Column(db.Integer, db.ForeignKey('klinika.id_kliniki'), nullable=False)

    klinika = db.relationship('Klinika', back_populates='wlasciciele')


# Address-related tables
class Adresy(db.Model):
    __tablename__ = 'adresy'
    id_adresu = db.Column(db.Integer, primary_key=True, nullable=False)
    miasto = db.Column(db.String(35), nullable=False)
    ulica = db.Column(db.String(40))
    nr_lokalu = db.Column(db.String(5), nullable=False)
    id_poczty = db.Column(db.Integer, db.ForeignKey('poczty.id_poczty'), nullable=False)

    adresy_wlasciciele = db.relationship('Wlasciciele', backref='adres', lazy=True)
    adresy_pracownicy = db.relationship('Pracownik', backref='adres', lazy=True)
    adresy_klienci = db.relationship('Klienci', backref='adres', lazy=True)


# Postal Codes
class Poczty(db.Model):
    __tablename__ = 'poczty'
    id_poczty = db.Column(db.Integer, primary_key=True, nullable=False)
    kod_pocztowy = db.Column(db.String(6), nullable=False)
    poczta = db.Column(db.String(30), nullable=False)

    poczty_adresy = db.relationship('Adresy', backref='poczta', lazy=True)


# Employee-related tables
class Pracownik(db.Model):
    __tablename__ = 'pracownik'
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
    __tablename__ = 'pracownicy_kliniki'
    id_pracownika = db.Column(db.Integer, db.ForeignKey('pracownik.id_pracownika'), primary_key=True, nullable=False)
    godziny_pracy_od = db.Column(db.DateTime, nullable=False)
    godziny_pracy_do = db.Column(db.DateTime, nullable=False)


# Job-related tables
class Stanowiska(db.Model):
    __tablename__ = 'stanowiska'
    id_stanowiska = db.Column(db.Integer, primary_key=True, nullable=False)
    nazwa_stanowiska = db.Column(db.String(30), nullable=False)
    wynagrodzenie = db.Column(db.Numeric(10, 2))

    pracownicy = db.relationship('Pracownik', backref='stanowisko', lazy=True)


# Veterinary-specific tables
class Weterynarze(db.Model):
    __tablename__ = 'weterynarze'
    id_pracownika = db.Column(db.Integer, db.ForeignKey('pracownik.id_pracownika'), primary_key=True, nullable=False)
    doswiadczenie = db.Column(db.String(150), nullable=False)
    kwalifikacje = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(20))


class WizytaWeterynarz(db.Model):
    __tablename__ = 'wizyta_weterynarz'
    id_wizyty = db.Column(db.Integer, db.ForeignKey('terminarz.id_wizyty'), primary_key=True, nullable=False)
    id_pracownika = db.Column(db.Integer, db.ForeignKey('weterynarze.id_pracownika'), primary_key=True, nullable=False)


# Schedule-related tables
class Terminarz(db.Model):
    __tablename__ = 'terminarz'
    id_wizyty = db.Column(db.Integer, primary_key=True, nullable=False)
    data_wizyty = db.Column(db.Date, nullable=False)
    godzina_wizyty_od = db.Column(db.DateTime, nullable=False)
    cena = db.Column(db.Numeric(5, 2))
    id_pupila = db.Column(db.Integer, db.ForeignKey('zwierzak.id_pupila'), nullable=False)

class Uslugi(db.Model):
    __tablename__ = 'uslugi'
    id_uslugi = db.Column(db.Integer, primary_key=True, nullable=False)
    nazwa = db.Column(db.String(50), nullable=False)
    opis = db.Column(db.String(200))
    cena = db.Column(db.Numeric(5, 2))
    dostepnosc = db.Column(db.String(20))

    
class WizytaUslugi(db.Model):
    __tablename__ = 'wizyta_uslugi'
    id_wizyty = db.Column(db.Integer, db.ForeignKey('terminarz.id_wizyty'), primary_key=True, nullable=False)
    powod_wizyty = db.Column(db.Integer, db.ForeignKey('uslugi.id_pupila'), primary_key=True, nullable=False)

class SpotkanieDoleglosci(db.Model):
    __tablename__ = 'spotkanie_doleglosci'
    id_wizyty = db.Column(db.Integer, db.ForeignKey('terminarz.id_wizyty'), primary_key=True, nullable=False)
    id_doleglosci = db.Column(db.Integer, db.ForeignKey('doleglosci.id_doleglosci'), primary_key=True, nullable=False)


# Client and Animal-related tables
class Klienci(db.Model):
    __tablename__ = 'klienci'
    id_klienta = db.Column(db.Integer, primary_key=True, nullable=False)
    imie = db.Column(db.String(20), nullable=False)
    nazwisko = db.Column(db.String(40), nullable=False)
    nr_telefonu = db.Column(db.String(20))
    adres_email = db.Column(db.String(40))
    id_adresu = db.Column(db.Integer, db.ForeignKey('adresy.id_adresu'), nullable=False)

    zwierzaki = db.relationship('Zwierzak', backref='klient', lazy=True)


class Zwierzak(db.Model):
    __tablename__ = 'zwierzak'
    id_pupila = db.Column(db.Integer, primary_key=True, nullable=False)
    imie = db.Column(db.String(40))
    wiek = db.Column(db.String(5), nullable=False)
    opis = db.Column(db.String(200))
    plec = db.Column(db.String(6))
    id_klienta = db.Column(db.Integer, db.ForeignKey('klienci.id_klienta'), nullable=False)
    id_rasy = db.Column(db.Integer, db.ForeignKey('rasa.id_rasy'), nullable=False)


class Rasa(db.Model):
    __tablename__ = 'rasa'
    id_rasy = db.Column(db.Integer, primary_key=True, nullable=False)
    nazwa = db.Column(db.String(20), nullable=False)
    nazwa_dluga = db.Column(db.String(40))
    cechy_charakterystyczne = db.Column(db.String(2000))

    zwierzaki = db.relationship('Zwierzak', backref='rasa', lazy=True)


class Doleglosci(db.Model):
    __tablename__ = 'doleglosci'
    id_doleglosci = db.Column(db.Integer, primary_key=True, nullable=False)
    nazwa = db.Column(db.String(50), nullable=False)
    opis = db.Column(db.String(200))
    sposob_leczenia = db.Column(db.String(200), nullable=False)

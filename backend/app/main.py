from datetime import datetime

from flask import Flask

from database import db, Klinika, Adresy, Poczty, Wlasciciele, Pracownik, Stanowiska, Terminarz, Weterynarze, Klienci, \
    Zwierzak, Rasa, Doleglosci, WizytaWeterynarz, SpotkanieDoleglosci, PracownicyKliniki

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@localhost/klinika'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)


def init_data():
    db.create_all()

    # Ensure resetting sequences for PostgreSQL compatibility
    db.session.execute("ALTER SEQUENCE poczty_id_poczty_seq RESTART WITH 1;")
    db.session.execute("ALTER SEQUENCE adresy_id_adresu_seq RESTART WITH 1;")
    db.session.execute("ALTER SEQUENCE klinika_id_kliniki_seq RESTART WITH 1;")
    db.session.execute("ALTER SEQUENCE wlasciciele_id_wlasciciela_seq RESTART WITH 1;")
    db.session.execute("ALTER SEQUENCE stanowiska_id_stanowiska_seq RESTART WITH 1;")
    db.session.execute("ALTER SEQUENCE pracownik_id_pracownika_seq RESTART WITH 1;")
    db.session.execute("ALTER SEQUENCE weterynarze_id_weterynarza_seq RESTART WITH 1;")
    db.session.execute("ALTER SEQUENCE klienci_id_klienta_seq RESTART WITH 1;")
    db.session.execute("ALTER SEQUENCE zwierzak_id_pupila_seq RESTART WITH 1;")
    db.session.execute("ALTER SEQUENCE doleglosci_id_doleglosci_seq RESTART WITH 1;")
    db.session.execute("ALTER SEQUENCE terminarz_id_wizyty_seq RESTART WITH 1;")
    db.session.execute("ALTER SEQUENCE wizytaweterynarz_id_seq RESTART WITH 1;")
    db.session.execute("ALTER SEQUENCE spotkannedoleglosci_id_seq RESTART WITH 1;")
    db.session.commit()

    if Adresy.query.first():
        print("Dane już istnieją. Inicjalizacja pominięta.")
        return
    #poczty
    poczta1 = Poczty(kod_pocztowy="00-001", poczta="Warszawa")
    poczta2 = Poczty(kod_pocztowy="00-002", poczta="Warszawa")
    poczta3 = Poczty(kod_pocztowy="00-003", poczta="Warszawa")
    poczta4 = Poczty(kod_pocztowy="00-004", poczta="Warszawa")
    poczta5 = Poczty(kod_pocztowy="00-005", poczta="Warszawa")

    db.session.add_all([poczta1, poczta2, poczta3, poczta4, poczta5])
    db.session.commit()

    #adresy
    adres1 = Adresy(miasto="Warszawa", ulica="Nowa", nr_lokalu="1", id_poczty=poczta1.id_poczty)
    adres2 = Adresy(miasto="Warszawa", ulica="Kolorowa", nr_lokalu="2", id_poczty=poczta2.id_poczty)
    adres3 = Adresy(miasto="Warszawa", ulica="Kasimira", nr_lokalu="3", id_poczty=poczta3.id_poczty)
    adres4 = Adresy(miasto="Warszawa", ulica="Kasimira", nr_lokalu="4", id_poczty=poczta3.id_poczty)
    adres5 = Adresy(miasto="Warszawa", ulica="Wolna", nr_lokalu="5", id_poczty=poczta4.id_poczty)
    adres6 = Adresy(miasto="Warszawa", ulica="Wiejska", nr_lokalu="6", id_poczty=poczta5.id_poczty)

    db.session.add_all([adres1, adres2, adres3, adres4, adres5, adres6])
    db.session.commit()

    #klinika
    klinika1 = Klinika(nazwa="Klinika Weterynaryjna", id_adresu=adres1.id_adresu)

    db.session.add(klinika1)
    db.session.commit()

    #wlasciciele
    wlasciciel1 = Wlasciciele(nazwisko="Kowalski", imie="Jan", nr_telefonu="123456789", id_adresu=adres2.id_adresu,
                              id_kliniki=klinika1.id_kliniki)
    db.session.add(wlasciciel1)
    db.session.commit()

    #stanowiska
    stanowisko1 = Stanowiska(nazwa_stanowiska="Weterynarz", wynagrodzenie=6000.00)
    stanowisko2 = Stanowiska(nazwa_stanowiska="Asystent Weterynarza", wynagrodzenie=3000.00)

    db.session.add_all([stanowisko1, stanowisko2])
    db.session.commit()

    #pracownicy
    pracownik1 = Pracownik(nazwisko="Mazur", imie="Marek", data_urodzenia=datetime(1980, 5, 15), plec="M",
                           data_zatrudnienia=datetime(2010, 1, 1), nr_telefonu="123123123", pesel="12345678901",
                           id_stanowiska=stanowisko1.id_stanowiska, id_adresu=adres3.id_adresu,
                           id_kliniki=klinika1.id_kliniki)
    pracownik2 = Pracownik(nazwisko="Zielińska", imie="Elżbieta", data_urodzenia=datetime(1992, 3, 25), plec="K",
                           data_zatrudnienia=datetime(2015, 6, 20), nr_telefonu="321321321", pesel="98765432109",
                           id_stanowiska=stanowisko2.id_stanowiska, id_adresu=adres4.id_adresu,
                           id_kliniki=klinika1.id_kliniki)

    db.session.add_all([pracownik1, pracownik2])
    db.session.commit()

    #weterynarze
    weterynarz1 = Weterynarze(id_pracownika=pracownik1.id_pracownika, doswiadczenie="5 lat w weterynarii",
                              kwalifikacje="Specjalista w chirurgii", status="Aktywny")

    db.session.add(weterynarz1)
    db.session.commit()

    #pracownicy_kliniki
    pracownik_kliniki1 = PracownicyKliniki(id_pracownika=pracownik2.id_pracownika, godziny_pracy_od="10:00",
                                          godziny_pracy_do="18:00")

    db.session.add(pracownik_kliniki1)
    db.session.commit()

    #klienci
    klient1 = Klienci(imie="Piotr", nazwisko="Wiśniewski", nr_telefonu="654654654", adres_email="piotr@example.com",
                      id_adresu=adres5.id_adresu)
    klient2 = Klienci(imie="Magdalena", nazwisko="Szymańska", nr_telefonu="456456456", adres_email="magda@example.com",
                      id_adresu=adres6.id_adresu)

    db.session.add_all([klient1, klient2])
    db.session.commit()

    #rasy
    rasa1 = Rasa(nazwa="Labrador", nazwa_dluga="Labrador Retriever",
                 cechy_charakterystyczne="Szczupła budowa ciała, przyjacielski temperament")
    rasa2 = Rasa(nazwa="Buldog", nazwa_dluga="Buldog Angielski",
                 cechy_charakterystyczne="Krępa budowa ciała, duża głowa")

    db.session.add_all([rasa1, rasa2])
    db.session.commit()

    #zwierzaki
    zwierzak1 = Zwierzak(imie="Burek", wiek="5", opis="Zwierzak rasy Labrador, bardzo energiczny", plec="M",
                         id_klienta=klient1.id_klienta, id_rasy=rasa1.id_rasy)
    zwierzak2 = Zwierzak(imie="Puszek", wiek="3", opis="Buldog Angielski, bardzo spokojny", plec="M",
                         id_klienta=klient2.id_klienta, id_rasy=rasa2.id_rasy)

    db.session.add_all([zwierzak1, zwierzak2])
    db.session.commit()

    #doleglosci
    doleglosc1 = Doleglosci(nazwa="Katar", opis="Zakażenie górnych dróg oddechowych",
                            sposob_leczenia="Leczenie objawowe, odpoczynek")
    doleglosc2 = Doleglosci(nazwa="Ból brzucha", opis="Problemy żołądkowe, ból brzucha",
                            sposob_leczenia="Zmiana diety, leki przeciwbólowe")

    db.session.add_all([doleglosc1, doleglosc2])
    db.session.commit()

    #terminarz
    terminarz1 = Terminarz(data_wizyty=datetime(2025, 2, 15), godzina_wizyty_od=datetime(2025, 2, 15, 10, 0),
                           cena=100.00, powod_wizyty="Kontrola zdrowia", id_pupila=zwierzak1.id_pupila)
    terminarz2 = Terminarz(data_wizyty=datetime(2025, 2, 16), godzina_wizyty_od=datetime(2025, 2, 16, 11, 0),
                           cena=150.00, powod_wizyty="Ból brzucha", id_pupila=zwierzak2.id_pupila)

    db.session.add_all([terminarz1, terminarz2])
    db.session.commit()

    #wizyta_wet
    wizyta_weterynarz1 = WizytaWeterynarz(id_wizyty=terminarz1.id_wizyty, id_pracownika=weterynarz1.id_pracownika)
    wizyta_weterynarz2 = WizytaWeterynarz(id_wizyty=terminarz2.id_wizyty, id_pracownika=weterynarz1.id_pracownika)

    db.session.add_all([wizyta_weterynarz1, wizyta_weterynarz2])
    db.session.commit()

    #spotkanie_dol
    spotkanie_doleglosci1 = SpotkanieDoleglosci(id_wizyty=terminarz1.id_wizyty, id_doleglosci=doleglosc1.id_doleglosci)
    spotkanie_doleglosci2 = SpotkanieDoleglosci(id_wizyty=terminarz2.id_wizyty, id_doleglosci=doleglosc2.id_doleglosci)

    db.session.add_all([spotkanie_doleglosci1, spotkanie_doleglosci2])
    db.session.commit()

if __name__ == '__main__':
    with app.app_context():
        init_data()
from model import Klinika, Adresy, Poczty, Wlasciciele, Pracownik, Stanowiska, Terminarz, Weterynarze, Klienci, \
    Zwierzak, Rasa, Doleglosci, WizytaWeterynarz, SpotkanieDoleglosci, PracownicyKliniki, Uslugi
from datetime import datetime
from main import app, db
from werkzeug.security import generate_password_hash

@app.cli.command("create_db")
def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()
    print("Baza danych została utworzona.")

@app.cli.command("initialize_data")
def init_data():
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
    weterynarz1 = Weterynarze(id_pracownika=pracownik1.id_pracownika, doswiadczenie="10 lat w weterynarii",
                              kwalifikacje="Specjalista w chirurgii", ocena=4.0, status="Aktywny")
    weterynarz2 = Weterynarze(id_pracownika=pracownik2.id_pracownika, doswiadczenie="2 lata w weterynarii",
                              kwalifikacje="Asystentka", ocena=4.5, status="Aktywny")

    db.session.add_all([weterynarz1, weterynarz2])
    db.session.commit()

    #pracownicy_kliniki
    pracownik_kliniki1 = PracownicyKliniki(id_pracownika=pracownik2.id_pracownika, godziny_pracy_od=datetime(3000, 1, 1, 10, 0),
                                          godziny_pracy_do=datetime(3000, 1, 1, 18, 0))

    db.session.add(pracownik_kliniki1)
    db.session.commit()

    #klienci
    klient1 = Klienci(imie="Piotr", nazwisko="Wiśniewski", nr_telefonu="654654654", adres_email="piotrwisniewski@gmail.com", haslo=generate_password_hash("Piotrulo321", method="pbkdf2:sha256"),
                      id_adresu=adres5.id_adresu)
    klient2 = Klienci(imie="Magdalena", nazwisko="Szymańska", nr_telefonu="456456456", adres_email="magda_sz@wp.pl", haslo=generate_password_hash("SzMagda.1", method="pbkdf2:sha256"), 
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

    #uslugi
    usluga1 = Uslugi(nazwa="Badanie kontrolne", opis="Standardowe badanie stanu zdrowia", cena=100.00, dostepnosc="Dostępna")
    usluga2 = Uslugi(nazwa="Szczepienie", opis="Podanie szczepionki ochronnej", cena=80.00, dostepnosc="Dostępna")
    usluga3 = Uslugi(nazwa="Sterylizacja", opis="Zabieg chirurgiczny sterylizacji", cena=300.00, dostepnosc="Ograniczona")
    usluga4 = Uslugi(nazwa="Czipowanie", opis="Zabieg implantacji mikroczipa", cena=150.00, dostepnosc="Dostępna")

    db.session.add_all([usluga1, usluga2, usluga3, usluga4])
    db.session.commit()

    #terminarz
    terminarz1 = Terminarz(data_wizyty=datetime(2025, 2, 15), godzina_wizyty_od=datetime(2025, 2, 15, 10, 0),
                           id_pupila=zwierzak1.id_pupila, id_uslugi=usluga1.id_uslugi)
    terminarz2 = Terminarz(data_wizyty=datetime(2025, 2, 16), godzina_wizyty_od=datetime(2025, 2, 16, 11, 0),
                           id_pupila=zwierzak1.id_pupila, id_uslugi=usluga2.id_uslugi)

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

@app.cli.command("show_data")
def show_data():
    # Poczty
    print("Poczty:")
    for poczta in Poczty.query.all():
        print(f"ID: {poczta.id_poczty}, Kod Pocztowy: {poczta.kod_pocztowy}, Poczta: {poczta.poczta}")
    print()

    # Adresy
    print("Adresy:")
    for adres in Adresy.query.all():
        print(f"ID: {adres.id_adresu}, Miasto: {adres.miasto}, Ulica: {adres.ulica}, Nr Lokalu: {adres.nr_lokalu}, ID Poczty: {adres.id_poczty}")
    print()

    # Klinika
    print("Klinika:")
    for klinika in Klinika.query.all():
        print(f"ID: {klinika.id_kliniki}, Nazwa: {klinika.nazwa}, ID Adresu: {klinika.id_adresu}")
    print()

    # Właściciele
    print("Właściciele:")
    for wlasciciel in Wlasciciele.query.all():
        print(f"ID: {wlasciciel.id_wlasciciela}, Imię: {wlasciciel.imie}, Nazwisko: {wlasciciel.nazwisko}, Nr Telefonu: {wlasciciel.nr_telefonu}, ID Adresu: {wlasciciel.id_adresu}, ID Kliniki: {wlasciciel.id_kliniki}")
    print()

    # Stanowiska
    print("Stanowiska:")
    for stanowisko in Stanowiska.query.all():
        print(f"ID: {stanowisko.id_stanowiska}, Nazwa Stanowiska: {stanowisko.nazwa_stanowiska}, Wynagrodzenie: {stanowisko.wynagrodzenie}")
    print()

    # Pracownicy
    print("Pracownicy:")
    for pracownik in Pracownik.query.all():
        print(f"ID: {pracownik.id_pracownika}, Imię: {pracownik.imie}, Nazwisko: {pracownik.nazwisko}, Data Urodzenia: {pracownik.data_urodzenia}, Plec: {pracownik.plec}, Data Zatrudnienia: {pracownik.data_zatrudnienia}, Nr Telefonu: {pracownik.nr_telefonu}, PESEL: {pracownik.pesel}, ID Stanowiska: {pracownik.id_stanowiska}, ID Adresu: {pracownik.id_adresu}, ID Kliniki: {pracownik.id_kliniki}")
    print()

    # Weterynarze
    print("Weterynarze:")
    for weterynarz in Weterynarze.query.all():
        print(f"ID Pracownika: {weterynarz.id_pracownika}, Doświadczenie: {weterynarz.doswiadczenie}, Kwalifikacje: {weterynarz.kwalifikacje}, Ocena: {weterynarz.ocena}, Status: {weterynarz.status}")
    print()

    # Klienci
    print("Klienci:")
    for klient in Klienci.query.all():
        print(f"ID: {klient.id_klienta}, Imię: {klient.imie}, Nazwisko: {klient.nazwisko}, Nr Telefonu: {klient.nr_telefonu}, Adres Email: {klient.adres_email}, ID Adresu: {klient.id_adresu}")
    print()

    # Zwierzaki
    print("Zwierzaki:")
    for zwierzak in Zwierzak.query.all():
        print(f"ID: {zwierzak.id_pupila}, Imię: {zwierzak.imie}, Wiek: {zwierzak.wiek}, Opis: {zwierzak.opis}, Płeć: {zwierzak.plec}, ID Klienta: {zwierzak.id_klienta}, ID Rasy: {zwierzak.id_rasy}")
    print()

    # Rasy
    print("Rasy:")
    for rasa in Rasa.query.all():
        print(f"ID: {rasa.id_rasy}, Nazwa: {rasa.nazwa}, Nazwa Długa: {rasa.nazwa_dluga}, Cechy Charakterystyczne: {rasa.cechy_charakterystyczne}")
    print()

    # Dolegliwości
    print("Dolegliwości:")
    for doleglosc in Doleglosci.query.all():
        print(f"ID: {doleglosc.id_doleglosci}, Nazwa: {doleglosc.nazwa}, Opis: {doleglosc.opis}, Sposób Leczenia: {doleglosc.sposob_leczenia}")
    print()

    # Terminarz
    print("Terminarz:")
    for terminarz in Terminarz.query.all():
        print(f"ID Wizyty: {terminarz.id_wizyty}, Data Wizyty: {terminarz.data_wizyty}, Godzina Wizyty: {terminarz.godzina_wizyty_od}, ID Pupila: {terminarz.id_pupila}, ID Usługi: {terminarz.id_uslugi}")
    print()

    # Wizyty Weterynarzy
    print("Wizyty Weterynarzy:")
    for wizyta in WizytaWeterynarz.query.all():
        print(f"ID Wizyty: {wizyta.id_wizyty}, ID Pracownika: {wizyta.id_pracownika}")
    print()

    # Uslugi
    print("Uslugi:")
    for usluga in Uslugi.query.all():
        print(f"ID Uslugi: {usluga.id_uslugi}, Nazwa Uslugi: {usluga.nazwa}, Opis Uslugi: {usluga.opis}, Cena Uslugi: {usluga.cena}, Dostepnosc Uslugi: {usluga.dostepnosc}")
    print()

    # Spotkania Dolegliwości
    print("Spotkania Dolegliwości:")
    for spotkanie in SpotkanieDoleglosci.query.all():
        print(f"ID Wizyty: {spotkanie.id_wizyty}, ID Dolegliwości: {spotkanie.id_doleglosci}")
    print()
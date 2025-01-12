from model import Adresy, Poczty, Terminarz, Weterynarze, Klienci, Zwierzak, Rasa, WizytaWeterynarz, Uslugi, Gatunki
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
    adres1 = Adresy(miasto="Warszawa", ulica="Chodkiewicza", nr_lokalu="15A", id_poczty=poczta1.id_poczty)
    adres2 = Adresy(miasto="Warszawa", ulica="Berestecka", nr_lokalu="46", id_poczty=poczta1.id_poczty)
    adres3 = Adresy(miasto="Warszawa", ulica="Nowa", nr_lokalu="1", id_poczty=poczta1.id_poczty)
    adres4 = Adresy(miasto="Warszawa", ulica="Świętokrzyska", nr_lokalu="22", id_poczty=poczta2.id_poczty)
    adres5 = Adresy(miasto="Warszawa", ulica="Kolorowa", nr_lokalu="2", id_poczty=poczta2.id_poczty)
    adres6 = Adresy(miasto="Warszawa", ulica="Kasimira", nr_lokalu="3", id_poczty=poczta3.id_poczty)
    adres7 = Adresy(miasto="Warszawa", ulica="Jasna", nr_lokalu="17", id_poczty=poczta3.id_poczty)
    adres8 = Adresy(miasto="Warszawa", ulica="Kasimira", nr_lokalu="4", id_poczty=poczta3.id_poczty)
    adres9 = Adresy(miasto="Warszawa", ulica="Wolna", nr_lokalu="5", id_poczty=poczta4.id_poczty)
    adres10 = Adresy(miasto="Warszawa", ulica="Wiejska", nr_lokalu="6", id_poczty=poczta5.id_poczty)

    db.session.add_all([adres1, adres2, adres3, adres4, adres5, adres6, adres7, adres8, adres9, adres10])
    db.session.commit()

    #weterynarze
    weterynarz1 = Weterynarze(nazwisko="Mazur", imie="Marek", data_urodzenia=datetime(1980, 5, 15), plec="M",
                           data_zatrudnienia=datetime(2010, 1, 1), nr_telefonu="123123123", pesel="12345678901", 
                           doswiadczenie="10 lat w weterynarii", kwalifikacje="Specjalista w chirurgii", ocena=4.0, 
                           wyksztalcenie="Wydział Medycyny Weterynaryjnej, Szkoła Główna Gospodarstwa Wiejskiego w Warszawie", 
                           id_adresu=adres3.id_adresu)
    weterynarz2 = Weterynarze(nazwisko="Zielińska", imie="Elżbieta", data_urodzenia=datetime(1992, 3, 25), plec="K",
                           data_zatrudnienia=datetime(2015, 6, 20), nr_telefonu="321321321", pesel="98765432109", 
                           doswiadczenie="2 lata w weterynarii", kwalifikacje="Asystentka", ocena=4.5, 
                           wyksztalcenie="Wydział Weterynaryjny Uniwersytetu Warszawskiego", id_adresu=adres4.id_adresu)

    db.session.add_all([weterynarz1, weterynarz2])
    db.session.commit()

    #klienci
    klient1 = Klienci(imie="Piotr", nazwisko="Wiśniewski", nr_telefonu="654654654", adres_email="piotrwisniewski@gmail.com", haslo=generate_password_hash("Piotrulo321", method="pbkdf2:sha256"),
                      id_adresu=adres5.id_adresu)
    klient2 = Klienci(imie="Magdalena", nazwisko="Szymańska", nr_telefonu="456456456", adres_email="magda_sz@wp.pl", haslo=generate_password_hash("SzMagda.1", method="pbkdf2:sha256"), 
                      id_adresu=adres6.id_adresu)
    klient3 = Klienci(imie="Marek", nazwisko="Mostowiak", nr_telefonu="111222333", adres_email="m_most@o2.pl", haslo=generate_password_hash("MostowiaK99", method="pbkdf2:sha256"), 
                      id_adresu=adres7.id_adresu)

    db.session.add_all([klient1, klient2, klient3])
    db.session.commit()

    # gatunki
    gatunek1 = Gatunki(nazwa="Pies")
    gatunek2 = Gatunki(nazwa="Kot")
    gatunek3 = Gatunki(nazwa="Gryzoń")

    db.session.add_all([gatunek1, gatunek2, gatunek3])
    db.session.commit()

    # Rasy dla gatunku "Pies"
    rasa1 = Rasa(rasa="Labrador", id_gatunku=gatunek1.id_gatunku, cechy_charakterystyczne="Szczupła budowa ciała, przyjacielski temperament")
    rasa2 = Rasa(rasa="Buldog", id_gatunku=gatunek1.id_gatunku, cechy_charakterystyczne="Krępa budowa ciała, duża głowa")
    rasa3 = Rasa(rasa="Owczarek Niemiecki", id_gatunku=gatunek1.id_gatunku, cechy_charakterystyczne="Silna budowa, inteligencja, lojalność")
    rasa4 = Rasa(rasa="Golden Retriever", id_gatunku=gatunek1.id_gatunku, cechy_charakterystyczne="Przyjacielski, gęste złote futro")
    rasa5 = Rasa(rasa="Chihuahua", id_gatunku=gatunek1.id_gatunku, cechy_charakterystyczne="Najmniejszy pies, duże uszy, energiczny")
    rasa6 = Rasa(rasa="Mops", id_gatunku=gatunek1.id_gatunku, cechy_charakterystyczne="Krępa budowa, krótka kufa, wesoły temperament")

    # Rasy dla gatunku "Kot"
    rasa7 = Rasa(rasa="Perski", id_gatunku=gatunek2.id_gatunku, cechy_charakterystyczne="Długie futro, spokojny temperament")
    rasa8 = Rasa(rasa="Syjamski", id_gatunku=gatunek2.id_gatunku, cechy_charakterystyczne="Smukły, krótkowłosy, niebieskie oczy")
    rasa9 = Rasa(rasa="Maine Coon", id_gatunku=gatunek2.id_gatunku, cechy_charakterystyczne="Duży, długowłosy, łagodny")
    rasa10 = Rasa(rasa="Ragdoll", id_gatunku=gatunek2.id_gatunku, cechy_charakterystyczne="Duży, łagodny, jedwabiste futro")
    rasa11 = Rasa(rasa="Sfinks", id_gatunku=gatunek2.id_gatunku, cechy_charakterystyczne="Bez sierści, ciepła skóra, przyjacielski")
    rasa12 = Rasa(rasa="Brytyjski Krótkowłosy", id_gatunku=gatunek2.id_gatunku, cechy_charakterystyczne="Krępa budowa, krótkie gęste futro")

    # Rasy dla gatunku "Gryzoń"
    rasa13 = Rasa(rasa="Chomik Syryjski", id_gatunku=gatunek3.id_gatunku, cechy_charakterystyczne="Mały, samotniczy, łatwy w opiece")
    rasa14 = Rasa(rasa="Chomik Dżungarski", id_gatunku=gatunek3.id_gatunku, cechy_charakterystyczne="Mały, aktywny, przyjacielski")
    rasa15 = Rasa(rasa="Świnka Morska", id_gatunku=gatunek3.id_gatunku, cechy_charakterystyczne="Łagodna, stadna, potrzebuje towarzystwa")
    rasa16 = Rasa(rasa="Mysz Domowa", id_gatunku=gatunek3.id_gatunku, cechy_charakterystyczne="Mała, szybka, aktywna nocą")
    rasa17 = Rasa(rasa="Szczur", id_gatunku=gatunek3.id_gatunku, cechy_charakterystyczne="Inteligentny, towarzyski, łatwy do tresury")
    rasa18 = Rasa(rasa="Koszatniczka", id_gatunku=gatunek3.id_gatunku, cechy_charakterystyczne="Mały gryzoń, aktywny w dzień, potrzebuje towarzystwa")

    db.session.add_all([
        rasa1, rasa2, rasa3, rasa4, rasa5, rasa6, 
        rasa7, rasa8, rasa9, rasa10, rasa11, rasa12, 
        rasa13, rasa14, rasa15, rasa16, rasa17, rasa18
    ])
    db.session.commit()

    #zwierzaki
    zwierzak1 = Zwierzak(imie="Burek", wiek="5", opis="Zwierzak rasy Labrador, bardzo energiczny", plec="M",
                         id_klienta=klient1.id_klienta, id_rasy=rasa1.id_rasy)
    zwierzak2 = Zwierzak(imie="Puszek", wiek="3", opis="Buldog Angielski, bardzo spokojny", plec="M",
                         id_klienta=klient2.id_klienta, id_rasy=rasa2.id_rasy)

    db.session.add_all([zwierzak1, zwierzak2])
    db.session.commit()

    #uslugi
    usluga1 = Uslugi(nazwa="Badanie kontrolne", opis="Standardowe badanie stanu zdrowia", cena=100.00, dostepnosc="Dostępna")
    usluga2 = Uslugi(nazwa="Szczepienie", opis="Podanie szczepionki ochronnej", cena=80.00, dostepnosc="Dostępna")
    usluga3 = Uslugi(nazwa="Sterylizacja", opis="Zabieg chirurgiczny sterylizacji", cena=300.00, dostepnosc="Ograniczona")
    usluga4 = Uslugi(nazwa="Czipowanie", opis="Zabieg implantacji mikroczipa", cena=150.00, dostepnosc="Dostępna")

    db.session.add_all([usluga1, usluga2, usluga3, usluga4])
    db.session.commit()

    #terminarz
    terminarz1 = Terminarz(data_wizyty=datetime(2025, 1, 15), godzina_wizyty_od=datetime(2025, 1, 15, 10, 0),
                           id_pupila=zwierzak1.id_pupila, id_uslugi=usluga1.id_uslugi, opis_dolegliwosci="Ból brzucha")
    terminarz2 = Terminarz(data_wizyty=datetime(2025, 1, 16), godzina_wizyty_od=datetime(2025, 1, 16, 11, 0),
                           id_pupila=zwierzak1.id_pupila, id_uslugi=usluga2.id_uslugi, opis_dolegliwosci="Katar")
    terminarz3 = Terminarz(data_wizyty=datetime(2025, 1, 11), godzina_wizyty_od=datetime(2025, 1, 11, 12, 0),
                           id_pupila=zwierzak2.id_pupila, id_uslugi=usluga1.id_uslugi, opis_dolegliwosci="Osłabienie")
    terminarz4 = Terminarz(data_wizyty=datetime(2025, 1, 14), godzina_wizyty_od=datetime(2025, 1, 14, 14, 0),
                           id_pupila=zwierzak2.id_pupila, id_uslugi=usluga1.id_uslugi, opis_dolegliwosci="Mały apetyt")
    terminarz5 = Terminarz(data_wizyty=datetime(2025, 1, 5), godzina_wizyty_od=datetime(2025, 1, 5, 10, 0),
                           id_pupila=zwierzak1.id_pupila, id_uslugi=usluga1.id_uslugi, opis_dolegliwosci="Test przeszłość")
    

    db.session.add_all([terminarz1, terminarz2, terminarz3, terminarz4, terminarz5])
    db.session.commit()

    #wizyta_wet
    wizyta_weterynarz1 = WizytaWeterynarz(id_wizyty=terminarz1.id_wizyty, id_weterynarza=weterynarz1.id_weterynarza)
    wizyta_weterynarz2 = WizytaWeterynarz(id_wizyty=terminarz2.id_wizyty, id_weterynarza=weterynarz2.id_weterynarza)
    wizyta_weterynarz2 = WizytaWeterynarz(id_wizyty=terminarz3.id_wizyty, id_weterynarza=weterynarz2.id_weterynarza)
    wizyta_weterynarz2 = WizytaWeterynarz(id_wizyty=terminarz4.id_wizyty, id_weterynarza=weterynarz1.id_weterynarza)
    wizyta_weterynarz2 = WizytaWeterynarz(id_wizyty=terminarz5.id_wizyty, id_weterynarza=weterynarz1.id_weterynarza)

    db.session.add_all([wizyta_weterynarz1, wizyta_weterynarz2])
    db.session.commit()
    print("Dane zostały dodane.")

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

    # Weterynarze
    print("Weterynarze:")
    for weterynarz in Weterynarze.query.all():
        print(f"ID: {weterynarz.id_weterynarza}, Imię: {weterynarz.imie}, Nazwisko: {weterynarz.nazwisko}, "
      f"Data Urodzenia: {weterynarz.data_urodzenia}, Plec: {weterynarz.plec}, "
      f"Data Zatrudnienia: {weterynarz.data_zatrudnienia}, Nr Telefonu: {weterynarz.nr_telefonu}, "
      f"PESEL: {weterynarz.pesel}, ID Adresu: {weterynarz.id_adresu}, "
      f"Doświadczenie: {weterynarz.doswiadczenie}, Kwalifikacje: {weterynarz.kwalifikacje}, "
      f"Ocena: {weterynarz.ocena}, Wykształcenie: {weterynarz.wyksztalcenie}")
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

        # Gatunki
    print("Gatunki:")
    for gatunek in Gatunki.query.all():
        print(f"ID: {gatunek.id_gatunku}, Nazwa: {gatunek.nazwa}")
    print()

    # Rasy
    print("Rasy:")
    for rasa in Rasa.query.all():
        print(f"ID: {rasa.id_rasy}, Rasa: {rasa.rasa}, ID Gatunku: {rasa.id_gatunku}, Cechy Charakterystyczne: {rasa.cechy_charakterystyczne}")
    print()

    # Terminarz
    print("Terminarz:")
    for terminarz in Terminarz.query.all():
        print(f"ID Wizyty: {terminarz.id_wizyty}, Data Wizyty: {terminarz.data_wizyty}, Godzina Wizyty: {terminarz.godzina_wizyty_od}, ID Pupila: {terminarz.id_pupila}, ID Usługi: {terminarz.id_uslugi}, Dolegliwości: {terminarz.opis_dolegliwosci}")
    print()

    # Wizyty Weterynarzy
    print("Wizyty Weterynarzy:")
    for wizyta in WizytaWeterynarz.query.all():
        print(f"ID Wizyty: {wizyta.id_wizyty}, ID Weterynarza: {wizyta.id_weterynarza}")
    print()

    # Uslugi
    print("Uslugi:")
    for usluga in Uslugi.query.all():
        print(f"ID Uslugi: {usluga.id_uslugi}, Nazwa Uslugi: {usluga.nazwa}, Opis Uslugi: {usluga.opis}, Cena Uslugi: {usluga.cena}, Dostepnosc Uslugi: {usluga.dostepnosc}")
    print()

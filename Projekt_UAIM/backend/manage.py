from model import Adresy, Poczty, Terminarz, Weterynarze, Klienci, Zwierzak, Rasa, WizytaWeterynarz, Uslugi, Gatunki
from datetime import datetime
from main import app, db
from werkzeug.security import generate_password_hash
from view import *

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
                           doswiadczenie="2 lata w weterynarii", kwalifikacje="Internistka", ocena=4.5, 
                           wyksztalcenie="Wydział Weterynaryjny Uniwersytetu Warszawskiego", id_adresu=adres4.id_adresu)
    weterynarz3 = Weterynarze(nazwisko="Nowak", imie="Anna", data_urodzenia=datetime(1985, 7, 19), plec="K",
                           data_zatrudnienia=datetime(2018, 5, 15), nr_telefonu="555123456", pesel="90041212345", 
                           doswiadczenie="8 lat w weterynarii", kwalifikacje="Specjalistka w dermatologii", ocena=5.0, 
                           wyksztalcenie="Wydział Medycyny Weterynaryjnej, Szkoła Główna Gospodarstwa Wiejskiego w Warszawie", 
                           id_adresu=adres5.id_adresu)
    weterynarz4 = Weterynarze(nazwisko="Kowalski", imie="Jan", data_urodzenia=datetime(1985, 7, 19), plec="M",
                           data_zatrudnienia=datetime(2020, 2, 10), nr_telefonu="555654321", pesel="85071965432", 
                           doswiadczenie="15 lat w weterynarii", kwalifikacje="Specjalista w gastrologii, dietetyk", ocena=4.8, 
                           wyksztalcenie="Wydział Weterynaryjny Uniwersytetu Warszawskiego", id_adresu=adres6.id_adresu)

    db.session.add_all([weterynarz1, weterynarz2, weterynarz3, weterynarz4])
    db.session.commit()

    #klienci
    klient1 = Klienci(imie="Piotr", nazwisko="Wiśniewski", nr_telefonu="654654654", adres_email="piotrwisniewski@gmail.com", haslo=generate_password_hash("Piotrulo321", method="pbkdf2:sha256"),
                      id_adresu=adres5.id_adresu)
    klient2 = Klienci(imie="Magdalena", nazwisko="Szymańska", nr_telefonu="456456456", adres_email="magda_sz@wp.pl", haslo=generate_password_hash("SzMagda.1", method="pbkdf2:sha256"), 
                      id_adresu=adres6.id_adresu)
    klient3 = Klienci(imie="Marek", nazwisko="Mostowiak", nr_telefonu="111222333", adres_email="m_most@o2.pl", haslo=generate_password_hash("MostowiaK99", method="pbkdf2:sha256"), 
                      id_adresu=adres7.id_adresu)
    klient4 = Klienci(imie="Anna", nazwisko="Kowalczyk", nr_telefonu="789123456", adres_email="a.kowalczyk@gmail.com", haslo=generate_password_hash("AnnaPass123", method="pbkdf2:sha256"), 
                      id_adresu=adres7.id_adresu)
    klient5 = Klienci(imie="Marek", nazwisko="Mostowiak", nr_telefonu="987654321", adres_email="tomasz.nowak@wp.pl", haslo=generate_password_hash("NowakPass456", method="pbkdf2:sha256"), 
                      id_adresu=adres7.id_adresu)
    klient6 = Klienci(imie="Marek", nazwisko="Mostowiak", nr_telefonu="456789123", adres_email="k.zielinska@gmail.com", haslo=generate_password_hash("Karolina789", method="pbkdf2:sha256"), 
                      id_adresu=adres7.id_adresu)

    db.session.add_all([klient1, klient2, klient3, klient4, klient5, klient6])
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
    rasa6 = Rasa(rasa="Yorkshire Terrier", id_gatunku=gatunek1.id_gatunku, cechy_charakterystyczne="Mały, długowłosy, energiczny")

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
    zwierzak1 = Zwierzak(imie="Burek", wiek="5", opis="Bardzo energiczny", plec="M",
                         id_klienta=klient1.id_klienta, id_rasy=rasa1.id_rasy)
    zwierzak2 = Zwierzak(imie="Puszek", wiek="3", opis="Bardzo spokojny", plec="M",
                         id_klienta=klient1.id_klienta, id_rasy=rasa2.id_rasy)
    zwierzak3 = Zwierzak(imie="Max", wiek="2", opis="Energiczny i bardzo przyjacielski", plec="M",
                         id_klienta=klient1.id_klienta, id_rasy=rasa3.id_rasy)
    zwierzak4 = Zwierzak(imie="Bella", wiek="4", opis="Uwielbia spacery i dzieci", plec="F",
                         id_klienta=klient2.id_klienta, id_rasy=rasa4.id_rasy)
    zwierzak5 = Zwierzak(imie="Lucky", wiek="1", opis="Mały, ale bardzo energiczny", plec="M",
                         id_klienta=klient2.id_klienta, id_rasy=rasa5.id_rasy)
    zwierzak6 = Zwierzak(imie="Luna", wiek="3", opis="Spokojna i urocza", plec="F",
                         id_klienta=klient3.id_klienta, id_rasy=rasa6.id_rasy)
    zwierzak7 = Zwierzak(imie="Simba", wiek="2", opis="Królewski wygląd i usposobienie", plec="M",
                         id_klienta=klient3.id_klienta, id_rasy=rasa9.id_rasy)
    zwierzak8 = Zwierzak(imie="Milo", wiek="5", opis="Bardzo spokojny i kochający dzieci", plec="M",
                         id_klienta=klient4.id_klienta, id_rasy=rasa7.id_rasy)
    zwierzak9 = Zwierzak(imie="Cleo", wiek="4", opis="Spokojna i towarzyska", plec="F",
                         id_klienta=klient4.id_klienta, id_rasy=rasa8.id_rasy)
    zwierzak10 = Zwierzak(imie="Ginger", wiek="1", opis="Mała, ale bardzo aktywnay", plec="F",
                         id_klienta=klient5.id_klienta, id_rasy=rasa13.id_rasy)
    zwierzak11 = Zwierzak(imie="Puffy", wiek="2", opis="Uwielbia towarzystwo i zabawę", plec="M",
                         id_klienta=klient5.id_klienta, id_rasy=rasa15.id_rasy)
    zwierzak12 = Zwierzak(imie="Rocky", wiek="3", opis="Towarzyski i bardzo inteligentny", plec="M",
                         id_klienta=klient6.id_klienta, id_rasy=rasa17.id_rasy)
    zwierzak13 = Zwierzak(imie="Chloe", wiek="6", opis="Aktywna i potrzebuje towarzystwa", plec="F",
                         id_klienta=klient6.id_klienta, id_rasy=rasa18.id_rasy)

    db.session.add_all([
        zwierzak1, zwierzak2, zwierzak3, zwierzak4,
        zwierzak5, zwierzak6, zwierzak7, zwierzak8,
        zwierzak9, zwierzak10, zwierzak11, zwierzak12,
        zwierzak13
    ])
    db.session.commit()

    #uslugi
    usluga1 = Uslugi(nazwa="Badanie kontrolne", opis="Standardowe badanie stanu zdrowia", cena=100.00)
    usluga2 = Uslugi(nazwa="Szczepienie", opis="Podanie szczepionki ochronnej", cena=80.00)
    usluga3 = Uslugi(nazwa="Kastracja", opis="Zabieg kastracji w znieczuleniu ogólnym", cena=300.00)
    usluga4 = Uslugi(nazwa="Czipowanie", opis="Zabieg implantacji mikroczipa", cena=150.00)
    usluga5 = Uslugi(nazwa="RTG", opis="Prześwietlenie rentgenowskie", cena=200.00)
    usluga6 = Uslugi(nazwa="USG", opis="Badanie ultrasonograficzne", cena=250.00)
    usluga7 = Uslugi(nazwa="Konsultacja dietetyczna", opis="Indywidualna konsultacja dietetyczna", cena=120.00)
    usluga8 = Uslugi(nazwa="Czyszczenie zębów", opis="Czyszczenie kamienia nazębnego w znieczuleniu ogólnym", cena=250.00)

    db.session.add_all([
        usluga1, usluga2, usluga3, usluga4,
        usluga5, usluga6, usluga7, usluga8
    ])
    db.session.commit()

    #terminarz
    terminarz1 = Terminarz(data_wizyty=datetime(2025, 1, 5), godzina_wizyty_od=datetime(2025, 1, 5, 15, 0),
                           id_pupila=zwierzak1.id_pupila, id_uslugi=usluga1.id_uslugi, opis_dolegliwosci="Osłabienie")
    terminarz2 = Terminarz(data_wizyty=datetime(2025, 1, 9), godzina_wizyty_od=datetime(2025, 1, 9, 10, 0),
                           id_pupila=zwierzak1.id_pupila, id_uslugi=usluga2.id_uslugi, opis_dolegliwosci="Wszystko w porządku")
    terminarz3 = Terminarz(data_wizyty=datetime(2025, 1, 6), godzina_wizyty_od=datetime(2025, 1, 6, 12, 0),
                           id_pupila=zwierzak2.id_pupila, id_uslugi=usluga3.id_uslugi, opis_dolegliwosci="Wszystko w porządku")
    terminarz4 = Terminarz(data_wizyty=datetime(2025, 1, 7), godzina_wizyty_od=datetime(2025, 1, 7, 14, 0),
                           id_pupila=zwierzak2.id_pupila, id_uslugi=usluga4.id_uslugi, opis_dolegliwosci="Wszystko w porządku")
    terminarz5 = Terminarz(data_wizyty=datetime(2025, 1, 8), godzina_wizyty_od=datetime(2025, 1, 8, 10, 0),
                           id_pupila=zwierzak3.id_pupila, id_uslugi=usluga5.id_uslugi, opis_dolegliwosci="Złamanie łapy")
    terminarz6 = Terminarz(data_wizyty=datetime(2025, 1, 9), godzina_wizyty_od=datetime(2025, 1, 9, 11, 0),
                           id_pupila=zwierzak3.id_pupila, id_uslugi=usluga6.id_uslugi, opis_dolegliwosci="Zapalenie wątroby")
    terminarz7 = Terminarz(data_wizyty=datetime(2025, 1, 10), godzina_wizyty_od=datetime(2025, 1, 10, 15, 0),
                           id_pupila=zwierzak4.id_pupila, id_uslugi=usluga7.id_uslugi, opis_dolegliwosci="Alergia pokarmowa")
    terminarz8 = Terminarz(data_wizyty=datetime(2025, 1, 11), godzina_wizyty_od=datetime(2025, 1, 11, 10, 0),
                           id_pupila=zwierzak4.id_pupila, id_uslugi=usluga2.id_uslugi, opis_dolegliwosci="Wszystko w porządku")
    terminarz9 = Terminarz(data_wizyty=datetime(2025, 1, 6), godzina_wizyty_od=datetime(2025, 1, 6, 13, 0),
                           id_pupila=zwierzak5.id_pupila, id_uslugi=usluga8.id_uslugi, opis_dolegliwosci="Zapalenie dziąseł")
    terminarz10 = Terminarz(data_wizyty=datetime(2025, 1, 7), godzina_wizyty_od=datetime(2025, 1, 7, 15, 0),
                           id_pupila=zwierzak5.id_pupila, id_uslugi=usluga3.id_uslugi, opis_dolegliwosci="Wszystko w porządku")
    terminarz11 = Terminarz(data_wizyty=datetime(2025, 1, 8), godzina_wizyty_od=datetime(2025, 1, 8, 11, 0),
                           id_pupila=zwierzak6.id_pupila, id_uslugi=usluga4.id_uslugi, opis_dolegliwosci="Wszystko w porządku")
    terminarz12 = Terminarz(data_wizyty=datetime(2025, 1, 9), godzina_wizyty_od=datetime(2025, 1, 9, 12, 0),
                           id_pupila=zwierzak6.id_pupila, id_uslugi=usluga5.id_uslugi, opis_dolegliwosci="Złamanie łapy")
    terminarz13 = Terminarz(data_wizyty=datetime(2025, 1, 4), godzina_wizyty_od=datetime(2025, 1, 4, 15, 0),
                           id_pupila=zwierzak7.id_pupila, id_uslugi=usluga6.id_uslugi, opis_dolegliwosci="Zapalenie trzustki")
    terminarz14 = Terminarz(data_wizyty=datetime(2025, 1, 5), godzina_wizyty_od=datetime(2025, 1, 5, 10, 0),
                           id_pupila=zwierzak7.id_pupila, id_uslugi=usluga1.id_uslugi, opis_dolegliwosci="Ból nogi")
    terminarz15 = Terminarz(data_wizyty=datetime(2025, 1, 4), godzina_wizyty_od=datetime(2025, 1, 4, 12, 0),
                           id_pupila=zwierzak8.id_pupila, id_uslugi=usluga2.id_uslugi, opis_dolegliwosci="Wszystko w porządku")
    terminarz16 = Terminarz(data_wizyty=datetime(2025, 1, 6), godzina_wizyty_od=datetime(2025, 1, 6, 14, 0),
                           id_pupila=zwierzak8.id_pupila, id_uslugi=usluga5.id_uslugi, opis_dolegliwosci="Złamanie łapy")
    terminarz17 = Terminarz(data_wizyty=datetime(2025, 1, 7), godzina_wizyty_od=datetime(2025, 1, 7, 10, 0),
                           id_pupila=zwierzak9.id_pupila, id_uslugi=usluga8.id_uslugi, opis_dolegliwosci="Zapalenie dziąseł")
    terminarz18 = Terminarz(data_wizyty=datetime(2025, 1, 8), godzina_wizyty_od=datetime(2025, 1, 8, 12, 0),
                           id_pupila=zwierzak9.id_pupila, id_uslugi=usluga4.id_uslugi, opis_dolegliwosci="Katar")
    terminarz19 = Terminarz(data_wizyty=datetime(2025, 1, 9), godzina_wizyty_od=datetime(2025, 1, 9, 15, 0),
                           id_pupila=zwierzak10.id_pupila, id_uslugi=usluga3.id_uslugi, opis_dolegliwosci="Wszystko w porządku")
    terminarz20 = Terminarz(data_wizyty=datetime(2025, 1, 10), godzina_wizyty_od=datetime(2025, 1, 10, 10, 0),
                           id_pupila=zwierzak10.id_pupila, id_uslugi=usluga1.id_uslugi, opis_dolegliwosci="Ból nogi")
    terminarz21 = Terminarz(data_wizyty=datetime(2025, 1, 11), godzina_wizyty_od=datetime(2025, 1, 11, 12, 0),
                           id_pupila=zwierzak11.id_pupila, id_uslugi=usluga7.id_uslugi, opis_dolegliwosci="Alergia pokarmowa")
    terminarz22 = Terminarz(data_wizyty=datetime(2025, 1, 12), godzina_wizyty_od=datetime(2025, 1, 12, 14, 0),
                           id_pupila=zwierzak11.id_pupila, id_uslugi=usluga8.id_uslugi, opis_dolegliwosci="Zapalenie dziąseł")
    terminarz23 = Terminarz(data_wizyty=datetime(2025, 1, 6), godzina_wizyty_od=datetime(2025, 1, 6, 10, 0),
                           id_pupila=zwierzak12.id_pupila, id_uslugi=usluga7.id_uslugi, opis_dolegliwosci="Alergia pokarmowa")
    terminarz24 = Terminarz(data_wizyty=datetime(2025, 1, 8), godzina_wizyty_od=datetime(2025, 1, 8, 13, 0),
                           id_pupila=zwierzak12.id_pupila, id_uslugi=usluga6.id_uslugi, opis_dolegliwosci="Zapalenie płuc")
    terminarz25 = Terminarz(data_wizyty=datetime(2025, 1, 9), godzina_wizyty_od=datetime(2025, 1, 9, 16, 0),
                           id_pupila=zwierzak13.id_pupila, id_uslugi=usluga4.id_uslugi, opis_dolegliwosci="Wszystko w porządku")
    terminarz26 = Terminarz(data_wizyty=datetime(2025, 1, 10), godzina_wizyty_od=datetime(2025, 1, 10, 16, 0),
                           id_pupila=zwierzak13.id_pupila, id_uslugi=usluga3.id_uslugi, opis_dolegliwosci="Wszystko w porządku")
    terminarz27 = Terminarz(data_wizyty=datetime(2025, 1, 27), godzina_wizyty_od=datetime(2025, 1, 27, 10, 0),
                           id_pupila=zwierzak1.id_pupila, id_uslugi=usluga6.id_uslugi, opis_dolegliwosci="Zapalenie wątroby")
    terminarz28 = Terminarz(data_wizyty=datetime(2025, 1, 27), godzina_wizyty_od=datetime(2025, 1, 27, 11, 0),
                           id_pupila=zwierzak2.id_pupila, id_uslugi=usluga5.id_uslugi, opis_dolegliwosci="Złamanie łapy")
    terminarz29 = Terminarz(data_wizyty=datetime(2025, 1, 27), godzina_wizyty_od=datetime(2025, 1, 27, 12, 0),
                           id_pupila=zwierzak3.id_pupila, id_uslugi=usluga3.id_uslugi, opis_dolegliwosci="Wszystko w porządku")
    terminarz30 = Terminarz(data_wizyty=datetime(2025, 1, 28), godzina_wizyty_od=datetime(2025, 1, 28, 11, 0),
                           id_pupila=zwierzak4.id_pupila, id_uslugi=usluga2.id_uslugi, opis_dolegliwosci="Wszystko w porządku")
    terminarz31 = Terminarz(data_wizyty=datetime(2025, 1, 28), godzina_wizyty_od=datetime(2025, 1, 28, 12, 0),
                           id_pupila=zwierzak5.id_pupila, id_uslugi=usluga1.id_uslugi, opis_dolegliwosci="Reakcja alergiczna")
    terminarz32 = Terminarz(data_wizyty=datetime(2025, 1, 28), godzina_wizyty_od=datetime(2025, 1, 28, 13, 0),
                           id_pupila=zwierzak6.id_pupila, id_uslugi=usluga8.id_uslugi, opis_dolegliwosci="Zapalenie dziąseł")
    terminarz33 = Terminarz(data_wizyty=datetime(2025, 1, 29), godzina_wizyty_od=datetime(2025, 1, 29, 12, 0),
                           id_pupila=zwierzak7.id_pupila, id_uslugi=usluga7.id_uslugi, opis_dolegliwosci="Alergia pokarmowa")
    terminarz34 = Terminarz(data_wizyty=datetime(2025, 1, 29), godzina_wizyty_od=datetime(2025, 1, 29, 13, 0),
                           id_pupila=zwierzak8.id_pupila, id_uslugi=usluga6.id_uslugi, opis_dolegliwosci="Zapalenie trzustki")
    terminarz35 = Terminarz(data_wizyty=datetime(2025, 1, 29), godzina_wizyty_od=datetime(2025, 1, 29, 14, 0),
                           id_pupila=zwierzak9.id_pupila, id_uslugi=usluga1.id_uslugi, opis_dolegliwosci="Ból brzucha")
    terminarz36 = Terminarz(data_wizyty=datetime(2025, 1, 30), godzina_wizyty_od=datetime(2025, 1, 30, 11, 0),
                           id_pupila=zwierzak10.id_pupila, id_uslugi=usluga2.id_uslugi, opis_dolegliwosci="Wszystko w porządku")
    terminarz37 = Terminarz(data_wizyty=datetime(2025, 1, 30), godzina_wizyty_od=datetime(2025, 1, 30, 12, 0),
                           id_pupila=zwierzak11.id_pupila, id_uslugi=usluga3.id_uslugi, opis_dolegliwosci="Wszystko w porządku")
    terminarz38 = Terminarz(data_wizyty=datetime(2025, 1, 30), godzina_wizyty_od=datetime(2025, 1, 30, 13, 0),
                           id_pupila=zwierzak12.id_pupila, id_uslugi=usluga4.id_uslugi, opis_dolegliwosci="Wszystko w porządku")
    terminarz39 = Terminarz(data_wizyty=datetime(2025, 1, 31), godzina_wizyty_od=datetime(2025, 1, 31, 12, 0),
                           id_pupila=zwierzak13.id_pupila, id_uslugi=usluga3.id_uslugi, opis_dolegliwosci="Wszystko w porządku")
    terminarz40 = Terminarz(data_wizyty=datetime(2025, 1, 31), godzina_wizyty_od=datetime(2025, 1, 31, 13, 0),
                           id_pupila=zwierzak1.id_pupila, id_uslugi=usluga7.id_uslugi, opis_dolegliwosci="Alergia pokarmowa")
    terminarz41 = Terminarz(data_wizyty=datetime(2025, 1, 31), godzina_wizyty_od=datetime(2025, 1, 31, 14, 0),
                           id_pupila=zwierzak1.id_pupila, id_uslugi=usluga8.id_uslugi, opis_dolegliwosci="Zapalenie dziąseł")
    terminarz42 = Terminarz(data_wizyty=datetime(2025, 1, 28), godzina_wizyty_od=datetime(2025, 1, 28, 14, 0),
                           id_pupila=zwierzak1.id_pupila, id_uslugi=usluga5.id_uslugi, opis_dolegliwosci="Złamanie łapy")
    
    db.session.add_all([
        terminarz1, terminarz2, terminarz3, terminarz4, terminarz5,
        terminarz6, terminarz7, terminarz8, terminarz9, terminarz10,
        terminarz11, terminarz12, terminarz13, terminarz14, terminarz15,
        terminarz16, terminarz17, terminarz18, terminarz19, terminarz20,
        terminarz21, terminarz22, terminarz23, terminarz24, terminarz25,
        terminarz26, terminarz27, terminarz28, terminarz29, terminarz30,
        terminarz31, terminarz32, terminarz33, terminarz34, terminarz35,
        terminarz36, terminarz37, terminarz38, terminarz39, terminarz40,
        terminarz41, terminarz42
    ])
    db.session.commit()

    #wizyta_wet
    wizyta_weterynarz1 = WizytaWeterynarz(id_wizyty=terminarz1.id_wizyty, id_weterynarza=weterynarz2.id_weterynarza)
    wizyta_weterynarz2 = WizytaWeterynarz(id_wizyty=terminarz2.id_wizyty, id_weterynarza=weterynarz2.id_weterynarza)
    wizyta_weterynarz3 = WizytaWeterynarz(id_wizyty=terminarz3.id_wizyty, id_weterynarza=weterynarz1.id_weterynarza)
    wizyta_weterynarz4 = WizytaWeterynarz(id_wizyty=terminarz4.id_wizyty, id_weterynarza=weterynarz2.id_weterynarza)
    wizyta_weterynarz5 = WizytaWeterynarz(id_wizyty=terminarz5.id_wizyty, id_weterynarza=weterynarz1.id_weterynarza)
    wizyta_weterynarz6 = WizytaWeterynarz(id_wizyty=terminarz6.id_wizyty, id_weterynarza=weterynarz4.id_weterynarza)
    wizyta_weterynarz7 = WizytaWeterynarz(id_wizyty=terminarz7.id_wizyty, id_weterynarza=weterynarz4.id_weterynarza)
    wizyta_weterynarz8 = WizytaWeterynarz(id_wizyty=terminarz8.id_wizyty, id_weterynarza=weterynarz2.id_weterynarza)
    wizyta_weterynarz9 = WizytaWeterynarz(id_wizyty=terminarz9.id_wizyty, id_weterynarza=weterynarz1.id_weterynarza)
    wizyta_weterynarz10 = WizytaWeterynarz(id_wizyty=terminarz10.id_wizyty, id_weterynarza=weterynarz1.id_weterynarza)
    wizyta_weterynarz11 = WizytaWeterynarz(id_wizyty=terminarz11.id_wizyty, id_weterynarza=weterynarz2.id_weterynarza)
    wizyta_weterynarz12 = WizytaWeterynarz(id_wizyty=terminarz12.id_wizyty, id_weterynarza=weterynarz1.id_weterynarza)
    wizyta_weterynarz13 = WizytaWeterynarz(id_wizyty=terminarz13.id_wizyty, id_weterynarza=weterynarz4.id_weterynarza)
    wizyta_weterynarz14 = WizytaWeterynarz(id_wizyty=terminarz14.id_wizyty, id_weterynarza=weterynarz1.id_weterynarza)
    wizyta_weterynarz15 = WizytaWeterynarz(id_wizyty=terminarz15.id_wizyty, id_weterynarza=weterynarz2.id_weterynarza)
    wizyta_weterynarz16 = WizytaWeterynarz(id_wizyty=terminarz16.id_wizyty, id_weterynarza=weterynarz1.id_weterynarza)
    wizyta_weterynarz17 = WizytaWeterynarz(id_wizyty=terminarz17.id_wizyty, id_weterynarza=weterynarz1.id_weterynarza)
    wizyta_weterynarz18 = WizytaWeterynarz(id_wizyty=terminarz18.id_wizyty, id_weterynarza=weterynarz2.id_weterynarza)
    wizyta_weterynarz19 = WizytaWeterynarz(id_wizyty=terminarz19.id_wizyty, id_weterynarza=weterynarz1.id_weterynarza)
    wizyta_weterynarz20 = WizytaWeterynarz(id_wizyty=terminarz20.id_wizyty, id_weterynarza=weterynarz1.id_weterynarza)
    wizyta_weterynarz21 = WizytaWeterynarz(id_wizyty=terminarz21.id_wizyty, id_weterynarza=weterynarz4.id_weterynarza)
    wizyta_weterynarz22 = WizytaWeterynarz(id_wizyty=terminarz22.id_wizyty, id_weterynarza=weterynarz1.id_weterynarza)
    wizyta_weterynarz23 = WizytaWeterynarz(id_wizyty=terminarz23.id_wizyty, id_weterynarza=weterynarz4.id_weterynarza)
    wizyta_weterynarz24 = WizytaWeterynarz(id_wizyty=terminarz24.id_wizyty, id_weterynarza=weterynarz2.id_weterynarza)
    wizyta_weterynarz25 = WizytaWeterynarz(id_wizyty=terminarz25.id_wizyty, id_weterynarza=weterynarz2.id_weterynarza)
    wizyta_weterynarz26 = WizytaWeterynarz(id_wizyty=terminarz26.id_wizyty, id_weterynarza=weterynarz1.id_weterynarza)
    wizyta_weterynarz27 = WizytaWeterynarz(id_wizyty=terminarz27.id_wizyty, id_weterynarza=weterynarz2.id_weterynarza)
    wizyta_weterynarz28 = WizytaWeterynarz(id_wizyty=terminarz28.id_wizyty, id_weterynarza=weterynarz2.id_weterynarza)
    wizyta_weterynarz29 = WizytaWeterynarz(id_wizyty=terminarz29.id_wizyty, id_weterynarza=weterynarz1.id_weterynarza)
    wizyta_weterynarz30 = WizytaWeterynarz(id_wizyty=terminarz30.id_wizyty, id_weterynarza=weterynarz2.id_weterynarza)
    wizyta_weterynarz31 = WizytaWeterynarz(id_wizyty=terminarz31.id_wizyty, id_weterynarza=weterynarz2.id_weterynarza)
    wizyta_weterynarz32 = WizytaWeterynarz(id_wizyty=terminarz32.id_wizyty, id_weterynarza=weterynarz2.id_weterynarza)
    wizyta_weterynarz33 = WizytaWeterynarz(id_wizyty=terminarz33.id_wizyty, id_weterynarza=weterynarz2.id_weterynarza)
    wizyta_weterynarz34 = WizytaWeterynarz(id_wizyty=terminarz34.id_wizyty, id_weterynarza=weterynarz2.id_weterynarza)
    wizyta_weterynarz35 = WizytaWeterynarz(id_wizyty=terminarz35.id_wizyty, id_weterynarza=weterynarz2.id_weterynarza)
    wizyta_weterynarz36 = WizytaWeterynarz(id_wizyty=terminarz36.id_wizyty, id_weterynarza=weterynarz2.id_weterynarza)
    wizyta_weterynarz37 = WizytaWeterynarz(id_wizyty=terminarz37.id_wizyty, id_weterynarza=weterynarz1.id_weterynarza)
    wizyta_weterynarz38 = WizytaWeterynarz(id_wizyty=terminarz38.id_wizyty, id_weterynarza=weterynarz2.id_weterynarza)
    wizyta_weterynarz39 = WizytaWeterynarz(id_wizyty=terminarz39.id_wizyty, id_weterynarza=weterynarz1.id_weterynarza)
    wizyta_weterynarz40 = WizytaWeterynarz(id_wizyty=terminarz40.id_wizyty, id_weterynarza=weterynarz2.id_weterynarza)
    wizyta_weterynarz41 = WizytaWeterynarz(id_wizyty=terminarz41.id_wizyty, id_weterynarza=weterynarz2.id_weterynarza)
    wizyta_weterynarz42 = WizytaWeterynarz(id_wizyty=terminarz42.id_wizyty, id_weterynarza=weterynarz2.id_weterynarza)

    db.session.add_all([
        wizyta_weterynarz1, wizyta_weterynarz2, wizyta_weterynarz3, wizyta_weterynarz4, wizyta_weterynarz5,
        wizyta_weterynarz6, wizyta_weterynarz7, wizyta_weterynarz8, wizyta_weterynarz9, wizyta_weterynarz10,
        wizyta_weterynarz11, wizyta_weterynarz12, wizyta_weterynarz13, wizyta_weterynarz14, wizyta_weterynarz15,
        wizyta_weterynarz16, wizyta_weterynarz17, wizyta_weterynarz18, wizyta_weterynarz19, wizyta_weterynarz20,
        wizyta_weterynarz21, wizyta_weterynarz22, wizyta_weterynarz23, wizyta_weterynarz24, wizyta_weterynarz25,
        wizyta_weterynarz26, wizyta_weterynarz27, wizyta_weterynarz28, wizyta_weterynarz29, wizyta_weterynarz30,
        wizyta_weterynarz31, wizyta_weterynarz32, wizyta_weterynarz33, wizyta_weterynarz34, wizyta_weterynarz35,
        wizyta_weterynarz36, wizyta_weterynarz37, wizyta_weterynarz38, wizyta_weterynarz39, wizyta_weterynarz40,
        wizyta_weterynarz41, wizyta_weterynarz42
    ])
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
        print(f"ID Wizyty: {wizyta.id_wizyty}, ID Pracownika: {wizyta.id_weterynarza}")
    print()

    # Uslugi
    print("Uslugi:")
    for usluga in Uslugi.query.all():
        print(f"ID Uslugi: {usluga.id_uslugi}, Nazwa Uslugi: {usluga.nazwa}, Opis Uslugi: {usluga.opis}, Cena Uslugi: {usluga.cena}")
    print()

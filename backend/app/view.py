from flask import request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from datetime import datetime, timedelta
from model import Weterynarze, Pracownik, Klinika, Uslugi, Terminarz, Zwierzak, WizytaWeterynarz, Klienci, Rasa, Gatunki
from main import app, db

SECRET_KEY = "21xuaim2024Zx37"

# Rejestracja klienta
@app.route("/api/register", methods=["POST"])
def register():
    dane = request.json
    imie = dane.get("imie")
    nazwisko = dane.get("nazwisko")
    adres_email = dane.get("adres_email")
    haslo = dane.get("haslo")
    nr_telefonu = dane.get("nr_telefonu")
    id_adresu = dane.get("id_adresu")

    if not all([imie, nazwisko, adres_email, haslo, nr_telefonu, id_adresu]):
        return jsonify({"error": "Brak wymaganych danych"}), 400

    if Klienci.query.filter_by(adres_email=adres_email).first():
        return jsonify({"error": "Adres email już istnieje"}), 400

    haslo_hash = generate_password_hash(haslo, method="pbkdf2:sha256")

    nowy_klient = Klienci(
        imie=imie,
        nazwisko=nazwisko,
        adres_email=adres_email,
        nr_telefonu=nr_telefonu,
        id_adresu=id_adresu,
        haslo=haslo_hash
    )
    db.session.add(nowy_klient)
    db.session.commit()

    return jsonify({"message": "Rejestracja zakończona sukcesem"}), 201


# Logowanie klienta
@app.route("/api/login", methods=["POST"])
def login():
    try:
        dane = request.json
        adres_email = dane.get("adres_email")
        haslo = dane.get("haslo")

        if not adres_email or not haslo:
            return jsonify({"error": "Brak wymaganych danych"}), 400

        klient = Klienci.query.filter_by(adres_email=adres_email).first()

        if not klient or not check_password_hash(klient.haslo, haslo):
            return jsonify({"error": "Nieprawidłowy adres email lub hasło"}), 401

        token = jwt.encode(
            {
                "id": klient.id_klienta,
                "exp": datetime.utcnow() + timedelta(hours=24)
            },
            SECRET_KEY,
            algorithm="HS256"
        )
        return jsonify({"token": token}), 200

    except Exception as e:
        print(f"Błąd logowania: {e}")
        return jsonify({"error": "Wewnętrzny błąd serwera"}), 500


def require_authorization(f):
    def wrapper(*args, **kwargs):
        token = None

        if "Authorization" in request.headers:
            token = request.headers["Authorization"].split(" ")[1]

        if not token:
            return jsonify({"error": "Brak tokenu JWT"}), 401

        try:
            dane = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            aktualny_klient = Klienci.query.get(dane["id"])
            if not aktualny_klient:
                raise Exception("Nieprawidłowy klient")
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token wygasł"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Token nieprawidłowy"}), 401
        except Exception as e:
            return jsonify({"error": f"Błąd tokenu: {str(e)}"}), 401

        return f(aktualny_klient, *args, **kwargs)

    wrapper.__name__ = f.__name__
    return wrapper


@app.route("/api/book-appointment", methods=["POST"])
@require_authorization
def book_appointment(aktualny_klient):
    dane = request.json
    id_pupila = dane.get("id_pupila")
    id_weterynarza = dane.get("id_weterynarza")
    data_wizyty = dane.get("data_wizyty")
    godzina_wizyty_od = dane.get("godzina_wizyty_od")
    id_uslugi = dane.get("id_uslugi")
    opis_dolegliwosci = dane.get("opis_dolegliwosci")

    if not all([id_pupila, id_weterynarza, data_wizyty, godzina_wizyty_od, id_uslugi, opis_dolegliwosci]):
        return jsonify({"error": "Brak wymaganych danych"}), 400
    
    weterynarz = Weterynarze.query.filter_by(id_pracownika=id_weterynarza).first()
    if not weterynarz:
        return jsonify({"error": "Podany weterynarz nie istnieje"}), 404
    
    zwierzak = Zwierzak.query.filter_by(id_pupila=id_pupila, id_klienta=aktualny_klient.id_klienta).first()
    if not zwierzak:
        return jsonify({"error": "Pupil nie należy do tego klienta"}), 403

    usluga = Uslugi.query.get(id_uslugi)
    if not usluga:
        return jsonify({"error": "Usługa nie istnieje"}), 404
    
    # Sprawdzanie, czy termin jest w przeszłości
    teraz = datetime.now()
    termin = datetime.strptime(f"{data_wizyty} {godzina_wizyty_od.split('T')[1]}", "%Y-%m-%d %H:%M")
    if termin <= teraz:
        return jsonify({"error": "Nie można umawiać wizyt na daty w przeszłości"}), 400
    
    # Sprawdzanie, czy termin przypada na weekend
    if termin.weekday() >= 5:  # 5 - sobota, 6 - niedziela
        return jsonify({"error": "Nie można umawiać wizyt w weekendy"}), 400
    
    # Sprawdzanie godzin pracy kliniki
    opening_hour = datetime.strptime("08:00", "%H:%M").time()
    closing_hour = datetime.strptime("18:00", "%H:%M").time()
    if not (opening_hour <= termin.time() <= closing_hour):
        return jsonify({"error": "Wizyty można umawiać jedynie w godzinach pracy kliniki (08:00-18:00)"}), 400

    termin_zajety = Terminarz.query.join(WizytaWeterynarz).filter(
        Terminarz.data_wizyty == datetime.strptime(data_wizyty, "%Y-%m-%d").date(),
        Terminarz.godzina_wizyty_od == termin,
        WizytaWeterynarz.id_pracownika == id_weterynarza
    ).first()
    if termin_zajety:
        return jsonify({"error": "Termin jest już zajęty dla tego weterynarza"}), 400

    nowa_wizyta = Terminarz(
        id_pupila=id_pupila,
        data_wizyty=datetime.strptime(data_wizyty, "%Y-%m-%d"),
        godzina_wizyty_od=termin,
        id_uslugi=id_uslugi,
        opis_dolegliwosci=opis_dolegliwosci
    )
    db.session.add(nowa_wizyta)
    db.session.commit()

    przypisanie_weterynarza = WizytaWeterynarz(
        id_wizyty=nowa_wizyta.id_wizyty,
        id_pracownika=id_weterynarza
    )
    db.session.add(przypisanie_weterynarza)
    db.session.commit()
    
    return jsonify({
        "message": "Wizyta została zarejestrowana",
        "id_wizyty": nowa_wizyta.id_wizyty,
        "id_weterynarza": id_weterynarza,
        "id_uslugi": id_uslugi,
        "id_pupila": id_pupila,
        "opis_dolegliwosci": opis_dolegliwosci
    }), 201



# Dodaj zwierzaka
@app.route("/api/add-pet", methods=["POST"])
@require_authorization
def add_pet(aktualny_klient):
    dane = request.json
    imie = dane.get("imie")
    wiek = dane.get("wiek")
    opis = dane.get("opis")
    plec = dane.get("plec")
    id_rasy = dane.get("id_rasy")

    if not all([imie, wiek, id_rasy]):
        return jsonify({"error": "Brak wymaganych danych"}), 400

    rasa = Rasa.query.get(id_rasy)
    if not rasa:
        return jsonify({"error": "Nie znaleziono wybranej rasy"}), 404

    nowy_zwierzak = Zwierzak(
        imie=imie,
        wiek=wiek,
        opis=opis,
        plec=plec,
        id_klienta=aktualny_klient.id_klienta,
        id_rasy=id_rasy
    )
    db.session.add(nowy_zwierzak)
    db.session.commit()

    return jsonify({"message": "Zwierzak został dodany", "id_pupila": nowy_zwierzak.id_pupila}), 201


# METODY GET

# Pobranie listy weterynarzy
@app.route('/veterinarian-list', methods=['GET'])
def get_veterinarians():
    weterynarze = Weterynarze.query.all()

    if not weterynarze:
        return jsonify({
            "error": "Brak weterynarzy w bazie danych."
        }), 404

    wynik = []
    for weterynarz in weterynarze:
        pracownik = Pracownik.query.get(weterynarz.id_pracownika)
        if pracownik:
            klinika = Klinika.query.get(pracownik.id_kliniki)
            wynik.append({
                "id": weterynarz.id_pracownika,
                "imię": pracownik.imie,
                "nazwisko": pracownik.nazwisko,
                "doświadczenie": weterynarz.doswiadczenie,
                "kwalifikacje": weterynarz.kwalifikacje,
                "ocena": weterynarz.ocena,
                "status": weterynarz.status,
                "klinika": klinika.nazwa if klinika else None
            })

    return jsonify(wynik), 200

# Pobranie katalogu usług
@app.route('/service-list', methods=['GET'])
def get_services():
    uslugi = Uslugi.query.all() 

    if not uslugi:
        return jsonify({
            "error": "Brak usług w bazie danych."
        }), 404

    wynik = [
        {
            "id": usluga.id_uslugi,
            "nazwa": usluga.nazwa,
            "opis": usluga.opis,
            "cena": float(usluga.cena) if usluga.cena else None,
            "dostepnosc": usluga.dostepnosc
        }
        for usluga in uslugi
    ]

    return jsonify(wynik), 200

# Pobieranie historii wizyt użytkownika
@app.route('/client-appointments', methods=['GET'])
@require_authorization
def get_client_appointments(aktualny_klient):
    # Pobierz wszystkie zwierzaki aktualnego klienta
    zwierzaki = Zwierzak.query.filter_by(id_klienta=aktualny_klient.id_klienta).all()
    if not zwierzaki:
        return jsonify({
            "error": "Nie znaleziono zwierzaków dla zalogowanego klienta."
        }), 404

    # Pobierz wszystkie wizyty dla zwierzaków klienta
    wizyty = Terminarz.query.filter(Terminarz.id_pupila.in_([z.id_pupila for z in zwierzaki])).all()
    if not wizyty:
        return jsonify({
            "error": "Brak wizyt dla zalogowanego klienta."
        }), 404

    # Przetwarzanie wyników
    wynik = []
    for wizyta in wizyty:
        zwierzak = next((z for z in zwierzaki if z.id_pupila == wizyta.id_pupila), None)
        if zwierzak:
            wynik.append({
                "id_wizyty": wizyta.id_wizyty,
                "data_wizyty": wizyta.data_wizyty.strftime('%Y-%m-%d'),
                "godzina_wizyty_od": wizyta.godzina_wizyty_od.strftime('%H:%M'),
                "imie_pupila": zwierzak.imie
            })

    return jsonify(wynik), 200

# Pobieranie szczegółów wizyty na podstawie ID
@app.route('/appointment-details', methods=['GET'])
@require_authorization
def get_appointment_details(aktualny_klient):
    # Pobierz wizyta_id z parametrów żądania
    wizyta_id = request.args.get('wizyta_id', type=int)
    if not wizyta_id:
        return jsonify({
            "error": "Parametr 'wizyta_id' jest wymagany."
        }), 400
    
    wizyta = Terminarz.query.get(wizyta_id)
    if not wizyta:
        return jsonify({
            "error": "Nie znaleziono wizyty o podanym ID."
        }), 404

    # Pobierz informacje o zwierzaku
    zwierzak = Zwierzak.query.get(wizyta.id_pupila)
    if not zwierzak:
        return jsonify({
            "error": "Nie znaleziono zwierzaka powiązanego z tą wizytą."
        }), 404

    # Pobierz usługi związane z wizytą
    usluga = Uslugi.query.get(wizyta.id_uslugi)
    if not usluga:
        return jsonify({
            "error": "Nie znaleziono usługi powiązanej z wizytą."
        }), 404

    # Pobierz weterynarzy przypisanych do wizyty
    weterynarze = WizytaWeterynarz.query.filter_by(id_wizyty=wizyta.id_wizyty).all()
    weterynarz_szczegoly = [
        {
            "id_pracownika": weterynarz.id_pracownika,
            "imie": Pracownik.query.get(weterynarz.id_pracownika).imie,
            "nazwisko": Pracownik.query.get(weterynarz.id_pracownika).nazwisko
        }
        for weterynarz in weterynarze
    ]

    wynik = {
        "id_wizyty": wizyta.id_wizyty,
        "data_wizyty": wizyta.data_wizyty.strftime('%Y-%m-%d'),
        "godzina_wizyty_od": wizyta.godzina_wizyty_od.strftime('%H:%M'),
        "imie_pupila": zwierzak.imie,
        "usluga": {
            "id_uslugi": usluga.id_uslugi,
            "nazwa": usluga.nazwa,
            "opis": usluga.opis,
            "cena": float(usluga.cena) if usluga.cena else None
        },
        "weterynarze": weterynarz_szczegoly
    }

    return jsonify(wynik), 200


@app.route("/api/vet-availability", methods=["GET"])
def check_vet_availability():
    data_wizyty = request.args.get("data_wizyty")
    godzina_wizyty_od = request.args.get("godzina_wizyty_od")
    id_weterynarza = request.args.get("id_weterynarza", type=int)

    if not all([data_wizyty, godzina_wizyty_od, id_weterynarza]):
        return jsonify({"error": "Brak wymaganych danych"}), 400

    termin_zajety = Terminarz.query.join(WizytaWeterynarz).filter(
        Terminarz.data_wizyty == datetime.strptime(data_wizyty, "%Y-%m-%d").date(),
        Terminarz.godzina_wizyty_od == datetime.strptime(godzina_wizyty_od, "%Y-%m-%dT%H:%M"),
        WizytaWeterynarz.id_pracownika == id_weterynarza
    ).first()

    if termin_zajety:
        return jsonify({"available": False, "message": "Termin jest zajęty"}), 200

    return jsonify({"available": True, "message": "Termin jest dostępny"}), 200



# Wyświetlanie danych zwierzaka
@app.route("/api/pet-details/<int:pet_id>", methods=["GET"])
@require_authorization
def get_pet_details(aktualny_klient, pet_id):
    zwierzak = Zwierzak.query.filter_by(id_pupila=pet_id, id_klienta=aktualny_klient.id_klienta).first()

    if not zwierzak:
        return jsonify({"error": "Zwierzak nie został znaleziony lub nie należy do tego klienta"}), 404

    rasa = Rasa.query.get(zwierzak.id_rasy)
    gatunek = Gatunki.query.get(rasa.id_gatunku) if rasa else None

    return jsonify({
        "id_pupila": zwierzak.id_pupila,
        "imie": zwierzak.imie,
        "wiek": zwierzak.wiek,
        "opis": zwierzak.opis,
        "plec": zwierzak.plec,
        "rasa": rasa.rasa if rasa else None,
        "gatunek": gatunek.nazwa if gatunek else None
    }), 200

# Endpoint do pobrania listy ras
@app.route("/api/races", methods=["GET"])
def get_races():
    id_gatunku = request.args.get("id_gatunku", type=int)

    if id_gatunku:
        rasy = Rasa.query.filter_by(id_gatunku=id_gatunku).all()
    else:
        rasy = Rasa.query.all()

    if not rasy:
        return jsonify({"error": "Brak ras w bazie danych."}), 404

    wynik = [
        {"id_rasy": rasa.id_rasy, "rasa": rasa.rasa, "id_gatunku": rasa.id_gatunku}
        for rasa in rasy
    ]
    return jsonify(wynik), 200


# Endpoint do pobrania listy pupili zalogowanego użytkownika
@app.route("/api/my-pets", methods=["GET"])
@require_authorization
def get_my_pets(aktualny_klient):
    # Pobierz zwierzaki należące do zalogowanego klienta
    zwierzaki = Zwierzak.query.filter_by(id_klienta=aktualny_klient.id_klienta).all()
    if not zwierzaki:
        return jsonify({"error": "Nie znaleziono pupili dla zalogowanego użytkownika."}), 404

    # Przetwórz dane zwierzaków
    wynik = [
        {
            "id_pupila": zwierzak.id_pupila,
            "imie": zwierzak.imie,
            "opis": zwierzak.opis,
            "wiek": zwierzak.wiek,
            "plec": zwierzak.plec,
            "rasa": zwierzak.rasa.rasa if zwierzak.rasa else "Nieznana rasa",
            "gatunek": zwierzak.rasa.gatunek.nazwa if zwierzak.rasa and zwierzak.rasa.gatunek else "Nieznany gatunek",
        }
        for zwierzak in zwierzaki
    ]
    return jsonify(wynik), 200

# Endpoint do pobierania zrealizowanych wizyt
@app.route("/api/completed-appointments", methods=["GET"])
@require_authorization
def get_completed_appointments(aktualny_klient):
    try:
        # Pobierz id_pupila z parametrów zapytania
        id_pupila = request.args.get("id_pupila", type=int)

        # Pobierz wizyty powiązane z klientem
        query = (
            Terminarz.query.join(WizytaWeterynarz, Terminarz.id_wizyty == WizytaWeterynarz.id_wizyty)
            .join(Pracownik, WizytaWeterynarz.id_pracownika == Pracownik.id_pracownika)
            .join(Uslugi, Terminarz.id_uslugi == Uslugi.id_uslugi)
            .join(Zwierzak, Terminarz.id_pupila == Zwierzak.id_pupila)
            .filter(Terminarz.id_pupila.in_([z.id_pupila for z in aktualny_klient.zwierzaki]))
            .filter(Terminarz.data_wizyty < datetime.utcnow().date())  # Wizyty zrealizowane (w przeszłości)
            .order_by(Terminarz.data_wizyty, Terminarz.godzina_wizyty_od)
        )

        # Dodaj filtr dla konkretnego pupila, jeśli jest podany
        if id_pupila:
            query = query.filter(Terminarz.id_pupila == id_pupila)

        wizyty = query.all()

        if not wizyty:
            return jsonify({"message": "Brak zrealizowanych wizyt"}), 404

        result = []
        for wizyta in wizyty:
            weterynarz = Pracownik.query.get(
                WizytaWeterynarz.query.filter_by(id_wizyty=wizyta.id_wizyty).first().id_pracownika
            )
            usluga = Uslugi.query.get(wizyta.id_uslugi)
            pupil = Zwierzak.query.get(wizyta.id_pupila)
            result.append({
                "data_wizyty": wizyta.data_wizyty.strftime("%Y-%m-%d"),
                "godzina_wizyty": wizyta.godzina_wizyty_od.strftime("%H:%M"),
                "lekarz": f"{weterynarz.imie} {weterynarz.nazwisko}",
                "powod_wizyty": wizyta.opis_dolegliwosci,
                "usluga": {
                    "nazwa": usluga.nazwa,
                    "opis": usluga.opis
                },
                "pupil": {
                    "imie": pupil.imie,
                    "rasa": pupil.rasa.rasa,
                    "wiek": pupil.wiek
                }
            })

        return jsonify(result), 200
    except Exception as e:
        print(f"Błąd podczas pobierania zrealizowanych wizyt: {e}")
        return jsonify({"error": "Wewnętrzny błąd serwera"}), 500


# Endpoint do pobierania wolnych terminów
@app.route("/api/available-slots", methods=["GET"])
def get_available_slots():
    try:
        date_from = request.args.get("date_from", type=str)
        date_to = request.args.get("date_to", type=str)
        id_weterynarza = request.args.get("id_weterynarza", type=int)

        if not all([date_from, date_to, id_weterynarza]):
            return jsonify({"error": "Brak wymaganych parametrów"}), 400

        date_from = datetime.strptime(date_from, "%Y-%m-%d").date()
        date_to = datetime.strptime(date_to, "%Y-%m-%d").date()

        teraz = datetime.now()
        if date_to < teraz.date():
            return jsonify({"error": "Nie można pobierać terminów w przeszłości"}), 400
        if date_from < teraz.date():
            date_from = teraz.date()

        weterynarz = Weterynarze.query.filter_by(id_pracownika=id_weterynarza).first()
        pracownik = Pracownik.query.filter_by(id_pracownika=id_weterynarza).first()

        if not weterynarz or not pracownik:
            return jsonify({"error": "Nie znaleziono weterynarza"}), 404

        opening_hour = datetime.strptime("09:00", "%H:%M").time()
        closing_hour = datetime.strptime("18:00", "%H:%M").time()

        booked_slots = Terminarz.query.join(WizytaWeterynarz).filter(
            Terminarz.data_wizyty.between(date_from, date_to),
            WizytaWeterynarz.id_pracownika == id_weterynarza
        ).all()

        occupied_times = {(slot.data_wizyty, slot.godzina_wizyty_od.time()) for slot in booked_slots}

        all_slots = []
        current_date = date_from
        while current_date <= date_to:
            current_time = opening_hour
            while current_time < closing_hour:
                is_available = (current_date, current_time) not in occupied_times and (
                    current_date > teraz.date() or (current_date == teraz.date() and current_time > teraz.time())
                )
                all_slots.append({
                    "date": current_date.strftime("%Y-%m-%d"),
                    "time": current_time.strftime("%H:%M"),
                    "available": is_available
                })
                current_time = (datetime.combine(datetime.today(), current_time) + timedelta(minutes=30)).time()
            current_date += timedelta(days=1)

        return jsonify(all_slots), 200

    except Exception as e:
        print(f"Błąd podczas pobierania wolnych terminów: {e}")
        return jsonify({"error": "Wewnętrzny błąd serwera"}), 500

# Pobranie listy gatunków
@app.route("/api/species", methods=["GET"])
def get_species():
    gatunki = Gatunki.query.all()
    if not gatunki:
        return jsonify({"error": "Brak gatunków w bazie danych."}), 404

    wynik = [{"id_gatunku": g.id_gatunku, "nazwa": g.nazwa} for g in gatunki]
    return jsonify(wynik), 200


# METODY PUT

# Edycja danych zwierzaka
@app.route("/api/pet-details/<int:pet_id>/edit", methods=["PUT"])
@require_authorization
def edit_pet_details(aktualny_klient, pet_id):
    dane = request.json
    zwierzak = Zwierzak.query.filter_by(id_pupila=pet_id, id_klienta=aktualny_klient.id_klienta).first()

    if not zwierzak:
        return jsonify({"error": "Zwierzak nie został znaleziony lub nie należy do tego klienta"}), 404

    if "id_rasy" in dane:
        rasa = Rasa.query.get(dane["id_rasy"])
        if not rasa:
            return jsonify({"error": "Wybrana rasa nie istnieje"}), 400
        zwierzak.id_rasy = dane["id_rasy"]

    zwierzak.imie = dane.get("imie", zwierzak.imie)
    zwierzak.wiek = dane.get("wiek", zwierzak.wiek)
    zwierzak.opis = dane.get("opis", zwierzak.opis)
    zwierzak.plec = dane.get("plec", zwierzak.plec)

    db.session.commit()
    return jsonify({"message": "Zwierzak został zaktualizowany"}), 200
from flask import request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from datetime import datetime, timedelta, timezone
from model import Weterynarze, Pracownik, Klinika, Uslugi, Terminarz, Zwierzak, WizytaWeterynarz, Klienci, Rasa
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


# Umów wizytę
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

    termin_zajety = Terminarz.query.join(WizytaWeterynarz).filter(
        Terminarz.data_wizyty == datetime.strptime(data_wizyty, "%Y-%m-%d").date(),
        Terminarz.godzina_wizyty_od == datetime.strptime(godzina_wizyty_od, "%Y-%m-%dT%H:%M"),
        WizytaWeterynarz.id_pracownika == id_weterynarza
    ).first()
    if termin_zajety:
        return jsonify({"error": "Termin jest już zajęty dla tego weterynarza"}), 400

    nowa_wizyta = Terminarz(
        id_pupila=id_pupila,
        data_wizyty=datetime.strptime(data_wizyty, "%Y-%m-%d"),
        godzina_wizyty_od=datetime.strptime(godzina_wizyty_od, "%Y-%m-%dT%H:%M"),
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

    return jsonify({
        "id_pupila": zwierzak.id_pupila,
        "imie": zwierzak.imie,
        "wiek": zwierzak.wiek,
        "opis": zwierzak.opis,
        "plec": zwierzak.plec,
        "id_rasy": zwierzak.id_rasy
    }), 200

# Endpoint do pobrania listy ras
@app.route("/api/races", methods=["GET"])
def get_races():
    try:
        rasy = Rasa.query.all()
        if not rasy:
            return jsonify({"error": "Brak ras w bazie danych."}), 404
        wynik = [{"id_rasy": rasa.id_rasy, "nazwa": rasa.nazwa} for rasa in rasy]
        return jsonify(wynik), 200
    except Exception as e:
        print(f"Błąd podczas pobierania ras: {e}")
        return jsonify({"error": "Wewnętrzny błąd serwera"}), 500

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
            "rasa": zwierzak.rasa.nazwa if zwierzak.rasa else "Nieznana rasa",
        }
        for zwierzak in zwierzaki
    ]
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

    zwierzak.imie = dane.get("imie", zwierzak.imie)
    zwierzak.wiek = dane.get("wiek", zwierzak.wiek)
    zwierzak.opis = dane.get("opis", zwierzak.opis)
    zwierzak.plec = dane.get("plec", zwierzak.plec)
    zwierzak.id_rasy = dane.get("id_rasy", zwierzak.id_rasy)

    db.session.commit()
    return jsonify({"message": "Zwierzak został zaktualizowany"}), 200

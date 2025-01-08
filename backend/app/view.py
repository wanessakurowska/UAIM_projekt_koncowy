from flask import request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from datetime import datetime, timedelta, timezone
from model import Weterynarze, Pracownik, Klinika, Uslugi, Terminarz, Zwierzak, WizytaUslugi, WizytaWeterynarz, Klienci
from main import app, db

SECRET_KEY = "21xuaim2024Zx37"

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



def wymagana_autoryzacja(f):
    def dekorator(*args, **kwargs):
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
    return dekorator

# Pobranie listy weterynarzy
@app.route('/veterinarian-list', methods=['GET'])
def get_veterinarians():
    veterinarians = Weterynarze.query.all()

    if not veterinarians:
        return jsonify({
            "error": "Brak weterynarzy w bazie danych."
        }), 404

    result = []
    for vet in veterinarians:
        pracownik = Pracownik.query.get(vet.id_pracownika)
        if pracownik:
            klinika = Klinika.query.get(pracownik.id_kliniki)
            result.append({
                "id": vet.id_pracownika,
                "imię": pracownik.imie,
                "nazwisko": pracownik.nazwisko,
                "doświadczenie": vet.doswiadczenie,
                "kwalifikacje": vet.kwalifikacje,
                "status": vet.status,
                "klinika": klinika.nazwa if klinika else None
            })

    return jsonify(result), 200

# Pobranie katalogu usług
@app.route('/service-list', methods=['GET'])
def get_services():
    services = Uslugi.query.all() 

    if not services:
        return jsonify({
            "error": "Brak usług w bazie danych."
        }), 404

    result = [
        {
            "id": service.id_uslugi,
            "nazwa": service.nazwa,
            "opis": service.opis,
            "cena": float(service.cena) if service.cena else None,
            "dostepnosc": service.dostepnosc
        }
        for service in services
    ]

    return jsonify(result), 200

# Pobieranie historii wizyt użytkownika
@app.route('/client-appointments', methods=['GET'])
def get_client_appointments():
    # Pobierz client_id z parametrów żądania
    client_id = request.args.get('client_id', type=int)
    if not client_id:
        return jsonify({
            "error": "Parametr 'client_id' jest wymagany."
        }), 400
    
    # Pobierz klienta (użytkownika)
    client = Klienci.query.get(client_id)
    if not client:
        return jsonify({
            "error": "Nie znaleziono użytkownika o podanym ID."
        }), 404

    # Pobierz wszystkie zwierzaki użytkownika
    zwierzaki = Zwierzak.query.filter_by(id_klienta=client_id).all()
    if not zwierzaki:
        return jsonify({
            "error": "Nie znaleziono zwierzaków dla podanego użytkownika."
        }), 404

    # Pobierz wszystkie wizyty dla zwierzaków użytkownika
    appointments = Terminarz.query.filter(Terminarz.id_pupila.in_([z.id_pupila for z in zwierzaki])).all()
    if not appointments:
        return jsonify({
            "error": "Brak wizyt dla podanego użytkownika."
        }), 404

    # Przetwarzanie wyników
    result = []
    for appointment in appointments:
        zwierzak = next((z for z in zwierzaki if z.id_pupila == appointment.id_pupila), None)
        if zwierzak:
            result.append({
                "id_wizyty": appointment.id_wizyty,
                "data_wizyty": appointment.data_wizyty.strftime('%Y-%m-%d'),
                "godzina_wizyty_od": appointment.godzina_wizyty_od.strftime('%H:%M'),
                "imie_pupila": zwierzak.imie
            })

    return jsonify(result), 200

# Pobieranie szczegółów wizyty na podstawie ID
@app.route('/appointment-details', methods=['GET'])
def get_appointment_details():
    # Pobierz appointment_id z parametrów żądania
    appointment_id = request.args.get('appointment_id', type=int)
    if not appointment_id:
        return jsonify({
            "error": "Parametr 'appointment_id' jest wymagany."
        }), 400
    
    appointment = Terminarz.query.get(appointment_id)
    if not appointment:
        return jsonify({
            "error": "Nie znaleziono wizyty o podanym ID."
        }), 404

    # Pobierz informacje o zwierzaku
    zwierzak = Zwierzak.query.get(appointment.id_pupila)
    if not zwierzak:
        return jsonify({
            "error": "Nie znaleziono zwierzaka powiązanego z tą wizytą."
        }), 404

    # Pobierz usługi związane z wizytą
    services = WizytaUslugi.query.filter_by(id_wizyty=appointment.id_wizyty).all()
    service_details = [
        {
            "id_uslugi": service.powod_wizyty,
            "nazwa": Uslugi.query.get(service.powod_wizyty).nazwa
        }
        for service in services
    ]

    # Pobierz weterynarzy przypisanych do wizyty
    veterinarians = WizytaWeterynarz.query.filter_by(id_wizyty=appointment.id_wizyty).all()
    veterinarian_details = [
        {
            "id_pracownika": vet.id_pracownika,
            "imie": Pracownik.query.get(vet.id_pracownika).imie,
            "nazwisko": Pracownik.query.get(vet.id_pracownika).nazwisko
        }
        for vet in veterinarians
    ]

    result = {
        "id_wizyty": appointment.id_wizyty,
        "data_wizyty": appointment.data_wizyty.strftime('%Y-%m-%d'),
        "godzina_wizyty_od": appointment.godzina_wizyty_od.strftime('%H:%M'),
        "cena": float(appointment.cena) if appointment.cena else None,
        "imie_pupila": zwierzak.imie,
        "uslugi": service_details,
        "weterynarze": veterinarian_details
    }

    return jsonify(result), 200

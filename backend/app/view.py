from flask import request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from datetime import datetime, timedelta, timezone
from model import Klienci
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

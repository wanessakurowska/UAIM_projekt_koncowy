import pytest
from main import app, db, Klienci, Rasa, Zwierzak, Weterynarze, Terminarz, WizytaWeterynarz, Uslugi
from datetime import datetime, timedelta
import jwt

@pytest.fixture
def client():
    """Konfiguracja testowego klienta aplikacji Flask"""
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    with app.test_client() as client:
        with app.app_context():
            db.create_all()

            # Dodanie testowego klienta
            test_klient = Klienci(
                imie="Jan",
                nazwisko="Kowalski",
                adres_email="jan.kowalski@example.com",
                haslo="test123",
                nr_telefonu="123456789",
                id_adresu=1
            )
            db.session.add(test_klient)

            # Dodanie testowej rasy
            test_rasa = Rasa(id_rasy=1, rasa="Owczarek", id_gatunku=1)
            db.session.add(test_rasa)

            # Dodanie testowego weterynarza z wymaganymi polami
            test_weterynarz = Weterynarze(
                id_weterynarza=1,
                imie="Anna",
                nazwisko="Nowak",
                data_urodzenia=datetime(1985, 5, 10),
                plec="F",
                data_zatrudnienia=datetime(2020, 1, 15),
                nr_telefonu="123456789",
                pesel="85051012345",
                doswiadczenie="10 lat w pracy z psami",
                kwalifikacje="Specjalista chorób wewnętrznych",
                ocena=4.8,
                wyksztalcenie="Weterynaria - Uniwersytet Warszawski",
                id_adresu=1
            )
            db.session.add(test_weterynarz)

            # Dodanie testowej usługi
            test_usluga = Uslugi(id_uslugi=1, nazwa="Badanie kontrolne", cena=100)
            db.session.add(test_usluga)

            db.session.commit()

        yield client

        with app.app_context():
            db.session.remove()
            db.drop_all()

def generate_token(client_id):
    """Generuje testowy token JWT dla klienta"""
    return jwt.encode(
        {"id": client_id, "exp": datetime.utcnow() + timedelta(hours=24)},
        "21xuaim2024Zx37",
        algorithm="HS256"
    )

def test_add_pet_success(client):
    """Test dodania zwierzaka (poprawne dane)"""
    token = generate_token(1)
    headers = {"Authorization": f"Bearer {token}"}

    data = {
        "imie": "Mika",
        "wiek": "5",
        "opis": "Bardzo spokojna.",
        "plec": "F",
        "id_rasy": 1
    }

    response = client.post("/api/add-pet", headers=headers, json=data)
    assert response.status_code == 201
    assert "id_pupila" in response.json

def test_add_pet_missing_field(client):
    """Test dodania zwierzaka z brakującym polem"""
    token = generate_token(1)
    headers = {"Authorization": f"Bearer {token}"}

    data = {
        "imie": "Rex",
        "opis": "Energiczny pies",
        "plec": "M",
        "id_rasy": 1
    }

    response = client.post("/api/add-pet", headers=headers, json=data)
    assert response.status_code == 400
    assert response.json["error"] == "Brak wymaganych danych"

def test_add_pet_invalid_race(client):
    """Test dodania zwierzaka z nieistniejącą rasą"""
    token = generate_token(1)
    headers = {"Authorization": f"Bearer {token}"}

    data = {
        "imie": "Max",
        "wiek": "2",
        "opis": "Spokojny pies",
        "plec": "M",
        "id_rasy": 999
    }

    response = client.post("/api/add-pet", headers=headers, json=data)
    assert response.status_code == 404
    assert response.json["error"] == "Nie znaleziono wybranej rasy"

def test_add_pet_no_auth(client):
    """Test dodania zwierzaka bez tokenu autoryzacyjnego"""
    data = {
        "imie": "Bella",
        "wiek": "1",
        "opis": "Młody pies",
        "plec": "F",
        "id_rasy": 1
    }

    response = client.post("/api/add-pet", json=data)
    assert response.status_code == 401
    assert response.json["error"] == "Brak tokenu JWT"

def test_book_appointment_success(client):
    """Test rezerwacji wizyty (poprawne dane)"""
    token = generate_token(1)
    headers = {"Authorization": f"Bearer {token}"}

    with app.app_context():
        test_pupil = Zwierzak(imie="Mika", wiek="5", id_klienta=1, id_rasy=1)
        db.session.add(test_pupil)
        db.session.commit()

    test_pupil = Zwierzak.query.filter_by(imie="Mika").first()

    data = {
        "id_pupila": test_pupil.id_pupila,
        "id_weterynarza": 1,
        "data_wizyty": "2025-01-30",
        "godzina_wizyty_od": "2025-01-30T10:00",
        "id_uslugi": 1,
        "opis_dolegliwosci": "Osłabienie"
    }

    response = client.post("/api/book-appointment", headers=headers, json=data)
    assert response.status_code == 201
    assert "id_wizyty" in response.json

def test_book_appointment_invalid_vet(client):
    """Test rezerwacji wizyty z nieistniejącym weterynarzem"""
    token = generate_token(1)
    headers = {"Authorization": f"Bearer {token}"}

    data = {
        "id_pupila": 1,
        "id_weterynarza": 999,
        "data_wizyty": "2025-01-30",
        "godzina_wizyty_od": "2025-01-30T11:00",
        "id_uslugi": 1,
        "opis_dolegliwosci": "Test"
    }

    response = client.post("/api/book-appointment", headers=headers, json=data)
    assert response.status_code == 404
    assert response.json["error"] == "Podany weterynarz nie istnieje"

def test_book_appointment_past_date(client):
    """Test rezerwacji wizyty w przeszłości"""
    token = generate_token(1)
    headers = {"Authorization": f"Bearer {token}"}

    data = {
        "id_pupila": 14,
        "id_weterynarza": 1,
        "data_wizyty": "2024-01-01",
        "godzina_wizyty_od": "2024-01-01T11:00",
        "id_uslugi": 1,
        "opis_dolegliwosci": "Test"
    }

    response = client.post("/api/book-appointment", headers=headers, json=data)
    assert response.status_code == 400
    assert response.json["error"] == "Nie można umawiać wizyt na daty w przeszłości"

import pytest
from main import app, db, Weterynarze, Uslugi, Klienci, Zwierzak, Terminarz, WizytaWeterynarz
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
            
            # Dodanie testowych danych
            test_klient = Klienci(
                imie="Jan",
                nazwisko="Kowalski",
                adres_email="jan.kowalski@example.com",
                haslo="test123",
                nr_telefonu="123456789",
                id_adresu=1
            )
            db.session.add(test_klient)
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

def test_get_veterinarian_list(client):
    """Test dla GET /veterinarian-list"""
    response = client.get("/veterinarian-list")
    assert response.status_code in [200, 404]
    if response.status_code == 200:
        assert isinstance(response.json, list)
    else:
        assert response.json["error"] == "Brak weterynarzy w bazie danych."

def test_get_service_list(client):
    """Test dla GET /service-list"""
    response = client.get("/service-list")
    assert response.status_code in [200, 404]
    if response.status_code == 200:
        assert isinstance(response.json, list)
    else:
        assert response.json["error"] == "Brak usług w bazie danych."

def test_get_vet_availability(client):
    """Test dla GET /api/vet-availability"""
    params = {
        "data_wizyty": "2025-01-31",
        "godzina_wizyty_od": "2025-01-31T10:00",
        "id_weterynarza": 1
    }
    response = client.get("/api/vet-availability", query_string=params)
    assert response.status_code in [200, 400, 404]

def test_get_available_slots(client):
    """Test dla GET /api/available-slots"""
    token = generate_token(1)
    headers = {"Authorization": f"Bearer {token}"}
    
    params = {
        "date_from": "2025-01-30",
        "date_to": "2025-01-31",
        "id_weterynarza": 1
    }
    response = client.get("/api/available-slots", query_string=params, headers=headers)
    assert response.status_code in [200, 400, 404]

def test_get_pet_details(client):
    """Test dla GET /api/pet-details/<int:pet_id>"""
    token = generate_token(1)
    headers = {"Authorization": f"Bearer {token}"}
    
    response = client.get("/api/pet-details/1", headers=headers)
    assert response.status_code in [200, 404]
    
def test_get_my_pets(client):
    """Test dla GET /api/my-pets"""
    token = generate_token(1)
    headers = {"Authorization": f"Bearer {token}"}
    
    response = client.get("/api/my-pets", headers=headers)
    assert response.status_code in [200, 404]

def test_get_appointment_list(client):
    """Test dla GET /appointment-list"""
    token = generate_token(1)
    headers = {"Authorization": f"Bearer {token}"}
    
    response = client.get("/appointment-list", headers=headers)
    assert response.status_code in [200, 404]

def test_get_species(client):
    """Test dla GET /api/species"""
    response = client.get("/api/species")
    assert response.status_code in [200, 404]

def test_get_races(client):
    """Test dla GET /api/races"""
    response = client.get("/api/races", query_string={"id_gatunku": 1})
    assert response.status_code in [200, 404]

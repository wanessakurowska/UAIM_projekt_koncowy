import sys
import os
import pytest
from flask import jsonify
import jwt
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta

# Dodanie folderu backend do ścieżki modułów
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main import db, app, Klienci

@pytest.fixture
def client():
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"  # Użycie bazy w pamięci
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            # Dodaj dane testowe
            test_klient = Klienci(
                imie="Piotr",
                nazwisko="Wiśniewski",
                adres_email="piotrwisniewski@gmail.com",
                haslo=generate_password_hash("Piotrulo321"),
                nr_telefonu="123456789",
                id_adresu=1
            )
            db.session.add(test_klient)
            db.session.commit()
        yield client
        with app.app_context():
            db.session.remove()
            db.drop_all()


def test_register_success(client):
    """Test udanej rejestracji użytkownika"""
    response = client.post("/api/register", json={
        "imie": "Jan",
        "nazwisko": "Kowalski",
        "adres_email": "jan.kowalski@gmail.com",
        "haslo": "Haslo123",
        "nr_telefonu": "123456789",
        "id_adresu": 1
    })
    assert response.status_code == 201
    assert response.json["message"] == "Rejestracja zakończona sukcesem"


def test_register_existing_email(client):
    """Test rejestracji z istniejącym adresem email"""
    response = client.post("/api/register", json={
        "imie": "Piotr",
        "nazwisko": "Wiśniewski",
        "adres_email": "piotrwisniewski@gmail.com",  # Już istniejący email
        "haslo": "NoweHaslo123",
        "nr_telefonu": "987654321",
        "id_adresu": 1
    })
    assert response.status_code == 400
    assert response.json["error"] == "Adres email już istnieje"


def test_login_success(client):
    """Test udanego logowania"""
    response = client.post("/api/login", json={
        "adres_email": "piotrwisniewski@gmail.com",
        "haslo": "Piotrulo321"
    })
    assert response.status_code == 200
    assert "token" in response.json


def test_login_invalid_password(client):
    """Test logowania z niepoprawnym hasłem"""
    response = client.post("/api/login", json={
        "adres_email": "piotrwisniewski@gmail.com",
        "haslo": "NiepoprawneHaslo"
    })
    assert response.status_code == 401
    assert response.json["error"] == "Nieprawidłowy adres email lub hasło"


def test_login_user_not_found(client):
    """Test logowania z nieistniejącym adresem email"""
    response = client.post("/api/login", json={
        "adres_email": "nieistniejacy@gmail.com",
        "haslo": "DowolneHaslo"
    })
    assert response.status_code == 401
    assert response.json["error"] == "Nieprawidłowy adres email lub hasło"


def test_protected_route_no_token(client):
    """Test dostępu do chronionego endpointu bez tokenu"""
    response = client.get("/api/my-pets")
    assert response.status_code == 401
    assert response.json["error"] == "Brak tokenu JWT"


def test_protected_route_invalid_token(client):
    """Test dostępu do chronionego endpointu z nieprawidłowym tokenem"""
    response = client.get("/api/my-pets", headers={
        "Authorization": "Bearer nieprawidlowytoken"
    })
    assert response.status_code == 401
    assert response.json["error"] == "Token nieprawidłowy"


def test_protected_route_expired_token(client):
    """Test dostępu do chronionego endpointu z wygasłym tokenem"""
    expired_token = jwt.encode(
        {"id": 1, "exp": datetime.utcnow() - timedelta(hours=1)},
        "21xuaim2024Zx37",
        algorithm="HS256"
    )
    response = client.get("/api/my-pets", headers={
        "Authorization": f"Bearer {expired_token}"
    })
    assert response.status_code == 401
    assert response.json["error"] == "Token wygasł"


def test_protected_route_valid_token(client):
    """Test dostępu do chronionego endpointu z poprawnym tokenem"""
    valid_token = jwt.encode(
        {"id": 1, "exp": datetime.utcnow() + timedelta(hours=1)},
        "21xuaim2024Zx37",
        algorithm="HS256"
    )
    response = client.get("/api/my-pets", headers={
        "Authorization": f"Bearer {valid_token}"
    })
    assert response.status_code != 401 
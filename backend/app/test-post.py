import requests

url = "http://localhost:5000"
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6NCwiZXhwIjoxNzM2Njk3MDQ5fQ.P9jdqvtkuGB-VEs1ZuOA2mvHsLqjyLqQ3pByoh52PbI"
# Token uzyskany poprzez zalogowanie klientki Julia Portka

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {token}"
}

# TESTY DLA POST add-pet
print("TESTY DLA POST add-pet")

# Przykład pozytywny: poprawne dane
print("\n[Przypadek pozytywny]: poprawne dane")
data = {
    "imie": "Mika",
    "wiek": "10",
    "opis": "Bardzo spokojna.",
    "plec": "F",
    "id_rasy": 3
}
r = requests.post(f"{url}/api/add-pet", headers=headers, json=data)
print("Status code:", r.status_code)
print("Odpowiedź serwera:", r.json())

# Przykład negatywny: brak wymaganego pola
print("\n[Przypadek negatywny]: brak wymaganego pola (wiek)")
data = {
    "imie": "Rex",
    "opis": "Energiczny pies",
    "plec": "M",
    "id_rasy": 1
}
r = requests.post(f"{url}/api/add-pet", headers=headers, json=data)
print("Status code:", r.status_code)
print("Odpowiedź serwera:", r.json())

# Przykład negatywny: nieistniejąca rasa
print("\n[Przypadek negatywny]: nieistniejąca rasa")
data = {
    "imie": "Max",
    "wiek": "2",
    "opis": "Spokojny pies",
    "plec": "M",
    "id_rasy": 999
}
r = requests.post(f"{url}/api/add-pet", headers=headers, json=data)
print("Status code:", r.status_code)
print("Odpowiedź serwera:", r.json())

# Przykład negatywny: brak tokenu autoryzacyjnego
print("\n[Przypadek negatywny]: brak tokenu autoryzacyjnego")
data = {
    "imie": "Bella",
    "wiek": "1",
    "opis": "Młody pies",
    "plec": "F",
    "id_rasy": 1
}
r = requests.post(f"{url}/api/add-pet", json=data)  # Brak headers z tokenem
print("Status code:", r.status_code)
print("Odpowiedź serwera:", r.json())


# TESTY DLA POST book-appointment
print("TESTY DLA POST book-appointment")

# Przykład pozytywny: Poprawne dane
print("\n[Przypadek pozytywny]: Rezerwacja wizyty")
data = {
    "id_pupila": 3, 
    "id_weterynarza": 1,
    "data_wizyty": "2025-01-16",
    "godzina_wizyty_od": "2025-01-16T10:00",
    "id_uslugi": 3,
    "opis_dolegliwosci": "Wylew"
}
r = requests.post(f"{url}/api/book-appointment", headers=headers, json=data)
print("Status code:", r.status_code)
print("Odpowiedź serwera:", r.json())

# Przykład negatywny: Klient (określony tokenem) nie jest właścicielem zwierzaka
print("\n[Przypadek negatywny]: Klient (określony tokenem) nie jest właścicielem zwierzaka")
data = {
    "id_pupila": 3, 
    "id_weterynarza": 1,
    "data_wizyty": "2025-01-18",
    "godzina_wizyty_od": "2025-01-13T10:00",
    "id_uslugi": 3,
    "opis_dolegliwosci": "Wylew"
}
r = requests.post(f"{url}/api/book-appointment", headers=headers, json=data)
print("Status code:", r.status_code)
print("Odpowiedź serwera:", r.json())

# Przykład negatywny: Weterynarz nie istnieje
print("\n[Przypadek negatywny]: Weterynarz nie istnieje")
data = {
    "id_pupila": 1,
    "id_weterynarza": 9999,
    "data_wizyty": "2025-01-15",
    "godzina_wizyty_od": "2025-01-15T10:00",
    "id_uslugi": 3,
    "opis_dolegliwosci": "Wylew"
}
r = requests.post(f"{url}/api/book-appointment", headers=headers, json=data)
print("Status code:", r.status_code)
print("Odpowiedź serwera:", r.json())

# Przypadek negatywny: Termin zajęty
print("\n[Przypadek negatywny]: Termin zajęty")
data = {
    "id_pupila": 3, 
    "id_weterynarza": 1,
    "data_wizyty": "2025-01-15",
    "godzina_wizyty_od": "2025-01-15T10:00",
    "id_uslugi": 3,
    "opis_dolegliwosci": "Wylew"
}
r = requests.post(f"{url}/api/book-appointment", headers=headers, json=data)
print("Status code:", r.status_code)
print("Odpowiedź serwera:", r.json())

# Przypadek negatywny: Termin zajęty
print("\n[Przypadek negatywny]: Termin w ")
data = {
    "id_pupila": 3, 
    "id_weterynarza": 1,
    "data_wizyty": "2025-01-15",
    "godzina_wizyty_od": "2025-01-15T10:00",
    "id_uslugi": 3,
    "opis_dolegliwosci": "Wylew"
}
r = requests.post(f"{url}/api/book-appointment", headers=headers, json=data)
print("Status code:", r.status_code)
print("Odpowiedź serwera:", r.json())

# Przykład negatywny: brak tokenu
print("\n[Przypadek negatywny]: Rezerwacja wizyty bez tokenu")
headers.pop("Authorization")
r = requests.post(f"{url}/api/book-appointment", headers=headers, json=data)
print("Status code:", r.status_code)
print("Odpowiedź serwera:", r.text)

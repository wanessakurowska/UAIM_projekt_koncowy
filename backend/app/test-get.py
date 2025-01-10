import requests
import json

url = "http://localhost:5000"
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MywiZXhwIjoxNzM2NTU0MjA1fQ.cQBze2XrB5ReVcgbO7N81EvqzeKrRxJeUgGrZi5x7BI"
# Token uzyskany poprzez zalogowanie klientki Julia Portka

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {token}"
}
#TEST DLA GET veterinarian-list
print("TEST DLA GET veterinarian-list")

r = requests.get(f"{url}/veterinarian-list")

if r.status_code == 200:
    print("Test przeszedł pomyślnie! Otrzymano listę weterynarzy.")
    # Wyświetlenie zwróconych danych
    print(json.dumps(r.json(), indent=4, ensure_ascii=False))
    print(r.status_code)
elif r.status_code == 404:
    print("Test nieudany: Brak weterynarzy w bazie danych.")
else:
    print(f"Test nieudany: Otrzymano nieoczekiwany kod statusu {r.status_code}")
    print("Treść odpowiedzi:", r.text)

#TEST DLA GET service-list
print("TEST DLA GET service-list")

r = requests.get(f"{url}/service-list")

if r.status_code == 200:
    print("Test przeszedł pomyślnie! Otrzymano listę usług.")
    # Wyświetlenie zwróconych danych
    print(json.dumps(r.json(), indent=4, ensure_ascii=False))
    print(r.status_code)
elif r.status_code == 404:
    print("Test nieudany: Brak usług w bazie danych.")
else:
    print(f"Test nieudany: Otrzymano nieoczekiwany kod statusu {r.status_code}")
    print("Treść odpowiedzi:", r.text)

# TESTY DLA GET vet-availability
print("TESTY DLA GET vet-availability")

# Przykład pozytywny: termin dostępny
print("\n[Przypadek pozytywny]: Termin dostępny")
params = {
    "data_wizyty": "2025-01-15",
    "godzina_wizyty_od": "2025-01-16T10:00",
    "id_weterynarza": 1
}
r = requests.get(f"{url}/api/vet-availability", params=params)
print("Status code:", r.status_code)
print("Odpowiedź serwera:", r.json())


# Przykład pozytywny: termin zajęty
print("\n[Przypadek pozytywny]: Termin zajęty")
params = {
    "data_wizyty": "2025-01-15",
    "godzina_wizyty_od": "2025-01-15T10:00",
    "id_weterynarza": 1
}
r = requests.get(f"{url}/api/vet-availability", params=params)
print("Status code:", r.status_code)
print("Odpowiedź serwera:", r.json())


# Przykład negatywny: brak wymaganych parametrów
print("\n[Przypadek negatywny]: Brak wymaganych parametrów")
params = {
    "data_wizyty": "2025-01-15"
}
r = requests.get(f"{url}/api/vet-availability", params=params)
print("Status code:", r.status_code)
print("Odpowiedź serwera:", r.text)

# TESTY DLA GET pet-details
print("TESTY DLA GET pet-details")

# Przykład pozytywny: poprawne ID
print("\n[Przypadek pozytywny]: poprawne ID")
pet_id = 3
r = requests.get(f"{url}/api/pet-details/{pet_id}", headers=headers)
print("Status code:", r.status_code)
print("Odpowiedź serwera:", r.json())

#TEST POZYTYWNY DLA GET client-appointments
print("TEST POZYTYWNY DLA GET client-appointments")

# Przykład pozytywny: poprawny token 
print("[Przypadek pozytywny] klient istnieje:")
r = requests.get(f"{url}/client-appointments", headers=headers, params=params)
print(json.dumps(r.json(), indent=4, ensure_ascii=False))
print(r.status_code)

#TESTY DLA GET appointment-details
print("TESTY DLA GET appointment-details")

# Przykład pozytywny: poprawne wizyta_id
print("[Przypadek pozytywny] wizyta istnieje:")
params = {"wizyta_id": 5}
r = requests.get(f"{url}/appointment-details", headers=headers, params=params)
print(json.dumps(r.json(), indent=4, ensure_ascii=False))
print(r.status_code)

# Przykład negatywny: brak tokenu
print("[Przypadek negatywny] bez tokenu")
headers.pop("Authorization")
params = {"wizyta_id": 1}
r = requests.post(f"{url}/appointment-details", headers=headers)
print("Odpowiedź serwera:", r.text)
print(r.status_code)

#TEST NEGATYWNY DLA GET client-appointments
print("TEST NEGATYWNY DLA GET client-appointments")

# Przykład negatywny: brak tokenu
print("[Przypadek negatywny] bez tokenu")
r = requests.post(f"{url}/client-appointments", headers=headers)
print("Odpowiedź serwera:", r.text)
print(r.status_code)
import requests
import json

url = 'http://127.0.0.1:5000'

headers = {
    "Content-Type": "application/json"
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

#TESTY DLA GET client-appointments
print("TESTY DLA GET client-appointments")

# Przykład pozytywny: poprawne klient_id
print("[Przypadek pozytywny] klient istnieje:")
params = {"klient_id": 1}
r = requests.get(f"{url}/client-appointments", params=params)
print(json.dumps(r.json(), indent=4, ensure_ascii=False))
print(r.status_code)

# Przykład negatywny: brak klient_id
print("\n[Przypadek negatywny] brak klient_id:")
r = requests.get(f"{url}/client-appointments")
print(json.dumps(r.json(), indent=4, ensure_ascii=False))
print(r.status_code)

# Przykład negatywny: niepoprawne klient_id
params = {"klient_id": 999}
print("\n[Przypadek negatywny] niepoprawne klient_id:")
r = requests.get(f"{url}/client-appointments", params=params)
print(json.dumps(r.json(), indent=4, ensure_ascii=False))
print(r.status_code)

#TESTY DLA GET appointment-details
print("TESTY DLA GET appointment-details")

# Przykład pozytywny: poprawne wizyta_id
print("[Przypadek pozytywny] wizyta istnieje:")
params = {"wizyta_id": 3}
r = requests.get(f"{url}/appointment-details", params=params)
print(json.dumps(r.json(), indent=4, ensure_ascii=False))
print(r.status_code)

# Przykład negatywny: brak wizyta_id
print("\n[Przypadek negatywny] brak wizyta_id:")
r = requests.get(f"{url}/appointment-details")
print(json.dumps(r.json(), indent=4, ensure_ascii=False))
print(r.status_code)

# Przykład negatywny: niepoprawne wizyta_id
params = {"wizyta_id": 999}
print("\n[Przypadek negatywny] niepoprawne wizyta_id:")
r = requests.get(f"{url}/appointment-details", params=params)
print(json.dumps(r.json(), indent=4, ensure_ascii=False))
print(r.status_code)


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
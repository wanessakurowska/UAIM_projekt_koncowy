import requests
import json

url = 'http://127.0.0.1:5000'

#TEST DLA GET veterinarian-list
print("TESTY DLA GET veterinarian-list")

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
print("TESTY DLA GET service-list")

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

# Przykład pozytywny: poprawne client_id
print("[Przypadek pozytywny] klient istnieje:")
params = {"client_id": 1}
r = requests.get(f"{url}/client-appointments", params=params)
print(json.dumps(r.json(), indent=4, ensure_ascii=False))
print(r.status_code)

# Przykład negatywny: brak client_id
print("\n[Przypadek negatywny] brak client_id:")
r = requests.get(f"{url}/client-appointments")
print(json.dumps(r.json(), indent=4, ensure_ascii=False))
print(r.status_code)

# Przykład negatywny: niepoprawne client_id
params = {"client_id": 999}
print("\n[Przypadek negatywny] niepoprawne client_id:")
r = requests.get(f"{url}/client-appointments", params=params)
print(json.dumps(r.json(), indent=4, ensure_ascii=False))
print(r.status_code)

#TESTY DLA GET client-appointments

# Przykład pozytywny: poprawne appointment_id
print("[Przypadek pozytywny] wizyta istnieje:")
params = {"appointment_id": 1}
r = requests.get(f"{url}/appointment-details", params=params)
print(json.dumps(r.json(), indent=4, ensure_ascii=False))
print(r.status_code)

# Przykład negatywny: brak appointment_id
print("\n[Przypadek negatywny] brak appointment_id:")
r = requests.get(f"{url}/appointment-details")
print(json.dumps(r.json(), indent=4, ensure_ascii=False))
print(r.status_code)

# Przykład negatywny: niepoprawne appointment_id
params = {"appointment_id": 999}
print("\n[Przypadek negatywny] niepoprawne appointment_id:")
r = requests.get(f"{url}/appointment-details", params=params)
print(json.dumps(r.json(), indent=4, ensure_ascii=False))
print(r.status_code)
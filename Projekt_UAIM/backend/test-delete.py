import requests

url = "http://localhost:5000"
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6NCwiZXhwIjoxNzM2NzA2NjMzfQ.8m9m4FNuLEk1o29R5rbNaFHd8p1FJPrYxIZo6HAc4FI"
# Token uzyskany poprzez zalogowanie klientki Julia Portka

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {token}"
}

# TESTY DLA DELETE cancel-appointment
print("TESTY DLA DELETE cancel-appointment")

# Przykład pozytywny: Anulowanie wizyty należącej do klienta
print("\n[Przypadek pozytywny]: Anulowanie wizyty należącej do klienta")
appointment_id = 7  # ID istniejącej wizyty powiązanej z klientem
r = requests.delete(f"{url}/api/cancel-appointment/{appointment_id}", headers=headers)
print("Status code:", r.status_code)
print("Odpowiedź serwera:", r.json())

# Przypadek negatywny: Próba anulowania wizyty, która nie istnieje
print("\n[Przypadek negatywny]: Anulowanie wizyty, która nie istnieje")
appointment_id = 9999  # Nieistniejące ID wizyty
r = requests.delete(f"{url}/api/cancel-appointment/{appointment_id}", headers=headers)
print("Status code:", r.status_code)
print("Odpowiedź serwera:", r.json())

# Przypadek negatywny: Próba anulowania wizyty, która nie należy do klienta
print("\n[Przypadek negatywny]: Anulowanie wizyty, która nie należy do klienta")
appointment_id = 2  # ID wizyty należącej do innego klienta
r = requests.delete(f"{url}/api/cancel-appointment/{appointment_id}", headers=headers)
print("Status code:", r.status_code)
print("Odpowiedź serwera:", r.json())

# Przypadek negatywny: Brak tokenu autoryzacyjnego
print("\n[Przypadek negatywny]: Próba anulowania wizyty bez tokenu")
appointment_id = 1  # ID istniejącej wizyty powiązanej z klientem
headers.pop("Authorization")  # Usunięcie tokenu z nagłówka
r = requests.delete(f"{url}/api/cancel-appointment/{appointment_id}", headers=headers)
print("Status code:", r.status_code)
print("Odpowiedź serwera:", r.text)

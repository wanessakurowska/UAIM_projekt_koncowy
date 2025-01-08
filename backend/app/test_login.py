import requests

BASE_URL = "http://localhost:5000"

headers = {
    "Content-Type": "application/json"
}

# 1. Test pozytywny - Logowanie z poprawnymi danymi
print("\n[Przypadek pozytywny]: Logowanie z poprawnymi danymi")
data = {
    "adres_email": "julia.portka@gmail.com",
    "haslo": "BubulekMika14"
}
r = requests.post(f"{BASE_URL}/api/login", headers=headers, json=data)
print("Status code:", r.status_code)
print("Odpowiedź serwera:", r.json())

# 2. Test negatywny - Niepoprawne hasło
print("\n[Przypadek negatywny]: Logowanie z niepoprawnym hasłem")
data = {
    "adres_email": "test@example.com",
    "haslo": "wrongpassword"
}
r = requests.post(f"{BASE_URL}/api/login", headers=headers, json=data)
print(r.json())
print("Status code:", r.status_code)

# 3. Test negatywny - Nieistniejący użytkownik
print("\n[Przypadek negatywny]: Logowanie z nieistniejącym użytkownikiem")
data = {
    "adres_email": "notfound@example.com",
    "haslo": "doesnotmatter"
}
r = requests.post(f"{BASE_URL}/api/login", headers=headers, json=data)
print(r.json())
print("Status code:", r.status_code)

# 4. Test negatywny - Brak danych
print("\n[Przypadek negatywny]: Brak danych logowania")
data = {}
r = requests.post(f"{BASE_URL}/api/login", headers=headers, json=data)
print(r.json())
print("Status code:", r.status_code)

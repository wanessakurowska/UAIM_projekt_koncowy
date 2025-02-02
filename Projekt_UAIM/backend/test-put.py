import requests

url = "http://localhost:5000"
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6NCwiZXhwIjoxNzM2Njk3MDQ5fQ.P9jdqvtkuGB-VEs1ZuOA2mvHsLqjyLqQ3pByoh52PbI"
# Token uzyskany poprzez zalogowanie klientki Julia Portka

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {token}"
}

# TESTY DLA PUT pet-details/edit
print("TESTY DLA PUT pet-details/edit")

# Przykład pozytywny: poprawne dane
print("\n[Przypadek pozytywny]: poprawne dane")
data = {
    "imie": "Reksio",
    "opis": "Bardzo wesoły pies"
}
pet_id = 3
r = requests.put(f"{url}/api/pet-details/{pet_id}/edit", headers=headers, json=data)
print("Status code:", r.status_code)
print("Odpowiedź serwera:", r.json())

# Przykład negatywny: brak tokenu
print("\n[Przypadek negatywny]: brak tokenu")
headers.pop("Authorization")
r = requests.put(f"{url}/api/pet-details/{pet_id}/edit", headers=headers, json=data)
print("Status code:", r.status_code)
print("Odpowiedź serwera:", r.text)

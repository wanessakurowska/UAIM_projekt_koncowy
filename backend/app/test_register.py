import requests

BASE_URL = "http://localhost:5000"

headers = {
    "Content-Type": "application/json"
}

# 1. Test pozytywny: Rejestracja
print("\n[Przypadek pozytywny]: Rejestracja nowego użytkownika")
data = {
    "imie": "Julia",
    "nazwisko": "Portka",
    "adres_email": "julia.portka@gmail.com",
    "haslo": "BubulekMika14",
    "nr_telefonu": "890457638",
    "id_adresu": 7
}
r = requests.post(f"{BASE_URL}/api/register", headers=headers, json=data)
print(r.json())
print("Status code:", r.status_code)

# 2. Test negatywny: Rejestracja z istniejącym emailem
print("\n[Przypadek negatywny]: Rejestracja z istniejącym emailem")
r = requests.post(f"{BASE_URL}/api/register", headers=headers, json=data)
print(r.json())
print("Status code:", r.status_code)
